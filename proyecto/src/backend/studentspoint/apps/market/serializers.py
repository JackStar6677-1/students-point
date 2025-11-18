"""Serializers para el sistema de compra/venta."""

from rest_framework import serializers
from .models import (
    CategoriaProducto, Producto, ProductoFavorito, 
    ProductoReporte, ProductoAnalytics
)
from .services import OpenGraphService, ProductoValidationService
from .utils import humanizar_tiempo


class CategoriaProductoSerializer(serializers.ModelSerializer):
    """Serializer para categorías de productos."""
    
    class Meta:
        model = CategoriaProducto
        fields = ['id', 'nombre', 'descripcion', 'icono', 'activa']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para productos."""
    
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_icono = serializers.CharField(source='categoria.icono', read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.name', read_only=True)
    campus_nombre = serializers.CharField(source='campus.nombre', read_only=True)
    es_favorito = serializers.SerializerMethodField()
    tiempo_publicado_humanizado = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id', 'titulo', 'descripcion', 'categoria', 'categoria_nombre', 'categoria_icono',
            'vendedor', 'vendedor_nombre', 'url_principal', 'tipo_enlace', 'urls_adicionales',
            'og_title', 'og_description', 'og_image', 'og_site_name', 'imagen', 'imagen_url',
            'estado', 'precio', 'precio_student_point', 'moneda', 'campus', 'campus_nombre', 'carrera',
            'created_at', 'updated_at', 'publicado_at', 'vendido_at',
            'visualizaciones', 'clicks_enlace', 'es_favorito', 'tiempo_publicado_humanizado'
        ]
        read_only_fields = [
            'vendedor', 'og_title', 'og_description', 'og_image', 'og_site_name',
            'created_at', 'updated_at', 'publicado_at', 'vendido_at',
            'visualizaciones', 'clicks_enlace'
        ]
    
    def get_imagen_url(self, obj):
        """Retorna la URL de la imagen, priorizando imagen manual sobre og_image."""
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return obj.og_image
    
    def get_es_favorito(self, obj):
        """Verifica si el producto es favorito del usuario actual."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoritos.filter(usuario=request.user).exists()
        return False
    
    def get_tiempo_publicado_humanizado(self, obj):
        """Tiempo transcurrido desde la publicación en formato legible."""
        return humanizar_tiempo(obj.publicado_at)


class ProductoCreateSerializer(serializers.ModelSerializer):
    """Serializer SIMPLE para crear productos."""
    
    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'url_principal', 'precio', 'precio_student_point']
    
    def create(self, validated_data):
        """Crea un producto de forma SIMPLE."""
        from django.utils import timezone
        
        request = self.context.get('request')
        
        # Datos del usuario
        validated_data['vendedor'] = request.user
        validated_data['campus'] = request.user.campus if hasattr(request.user, 'campus') else None
        validated_data['carrera'] = request.user.career if hasattr(request.user, 'career') else ""
        
        # Configuración simple
        validated_data['estado'] = 'publicado'
        validated_data['publicado_at'] = timezone.now()
        validated_data['moneda'] = 'CLP'
        validated_data['tipo_enlace'] = 'externo'
        validated_data['acepta_terminos'] = True
        validated_data['acepta_responsabilidad'] = True
        validated_data['fecha_aceptacion_terminos'] = timezone.now()
        
        # Categoría por defecto
        if not validated_data.get('categoria'):
            from .models import CategoriaProducto
            categoria_default, _ = CategoriaProducto.objects.get_or_create(
                nombre='Otros',
                defaults={'descripcion': 'Categoría general', 'activa': True}
            )
            validated_data['categoria'] = categoria_default
        
        # Crear producto
        producto = super().create(validated_data)
        
        # Crear analytics
        try:
            ProductoAnalytics.objects.create(producto=producto)
        except:
            pass
        
        return producto
    
    def update(self, instance, validated_data):
        """Actualiza un producto y actualiza metadatos OpenGraph si cambió la URL."""
        url_principal = validated_data.get('url_principal', instance.url_principal)
        
        # Si cambió la URL, obtener nuevos metadatos
        if url_principal != instance.url_principal:
            metadatos = OpenGraphService.obtener_metadatos_opengraph(url_principal)
            validated_data.update(metadatos)
            
            # Actualizar tipo de enlace si no se especificó
            if not validated_data.get('tipo_enlace'):
                validated_data['tipo_enlace'] = ProductoValidationService.detectar_tipo_enlace(url_principal)
        
        return super().update(instance, validated_data)


class ProductoFavoritoSerializer(serializers.ModelSerializer):
    """Serializer para productos favoritos."""
    
    producto = ProductoSerializer(read_only=True)
    
    class Meta:
        model = ProductoFavorito
        fields = ['id', 'producto', 'created_at']


class ProductoReporteSerializer(serializers.ModelSerializer):
    """Serializer para reportes de productos."""
    
    reportador_nombre = serializers.CharField(source='reportador.name', read_only=True)
    producto_titulo = serializers.CharField(source='producto.titulo', read_only=True)
    
    class Meta:
        model = ProductoReporte
        fields = [
            'id', 'producto', 'producto_titulo', 'reportador', 'reportador_nombre',
            'tipo', 'descripcion', 'resuelto', 'created_at'
        ]
        read_only_fields = ['reportador', 'created_at']
    
    def create(self, validated_data):
        """Crea un nuevo reporte."""
        request = self.context.get('request')
        validated_data['reportador'] = request.user
        return super().create(validated_data)


class ProductoAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer para analytics de productos."""
    
    class Meta:
        model = ProductoAnalytics
        fields = [
            'total_visualizaciones', 'total_clicks', 'total_favoritos', 
            'total_reportes', 'visualizaciones_por_campus', 
            'visualizaciones_por_carrera', 'ultima_actualizacion'
        ]


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de productos."""
    
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_icono = serializers.CharField(source='categoria.icono', read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.name', read_only=True)
    campus_nombre = serializers.CharField(source='campus.nombre', read_only=True)
    es_favorito = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id', 'titulo', 'descripcion', 'categoria_nombre', 'categoria_icono',
            'vendedor_nombre', 'url_principal', 'tipo_enlace', 'og_image', 'imagen_url',
            'estado', 'precio', 'precio_student_point', 'moneda', 'campus_nombre', 'carrera',
            'created_at', 'visualizaciones', 'es_favorito'
        ]
    
    def get_es_favorito(self, obj):
        """Verifica si el producto es favorito del usuario actual."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoritos.filter(usuario=request.user).exists()
        return False
    
    def get_imagen_url(self, obj):
        """Retorna la URL de la imagen, priorizando imagen manual sobre og_image."""
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return obj.og_image
