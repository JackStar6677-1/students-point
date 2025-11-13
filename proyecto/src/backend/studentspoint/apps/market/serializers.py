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
    
    class Meta:
        model = Producto
        fields = [
            'id', 'titulo', 'descripcion', 'categoria', 'categoria_nombre', 'categoria_icono',
            'vendedor', 'vendedor_nombre', 'url_principal', 'tipo_enlace', 'urls_adicionales',
            'og_title', 'og_description', 'og_image', 'og_site_name',
            'estado', 'precio', 'precio_student_point', 'moneda', 'campus', 'campus_nombre', 'carrera',
            'created_at', 'updated_at', 'publicado_at', 'vendido_at',
            'visualizaciones', 'clicks_enlace', 'es_favorito', 'tiempo_publicado_humanizado'
        ]
        read_only_fields = [
            'vendedor', 'og_title', 'og_description', 'og_image', 'og_site_name',
            'created_at', 'updated_at', 'publicado_at', 'vendido_at',
            'visualizaciones', 'clicks_enlace'
        ]
    
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
    """Serializer para crear productos con extracción automática de OpenGraph."""
    
    class Meta:
        model = Producto
        fields = [
            'titulo', 'descripcion', 'categoria', 'url_principal', 
            'tipo_enlace', 'urls_adicionales', 'precio', 'precio_student_point', 'moneda',
            'acepta_terminos', 'acepta_responsabilidad'
        ]
    
    def validate_url_principal(self, value):
        """Valida que la URL sea válida y obligatoria."""
        if not value:
            raise serializers.ValidationError(
                "El enlace principal es OBLIGATORIO. StudentsPoint solo actúa como medio de difusión."
            )
        if not ProductoValidationService.validar_url(value):
            raise serializers.ValidationError("URL inválida")
        return value
    
    def validate(self, data):
        """Valida que se hayan aceptado los términos y condiciones."""
        if not data.get('acepta_terminos'):
            raise serializers.ValidationError({
                'acepta_terminos': 'Debes aceptar los términos y condiciones para publicar en el Marketplace.'
            })
        
        if not data.get('acepta_responsabilidad'):
            raise serializers.ValidationError({
                'acepta_responsabilidad': 'Debes aceptar la responsabilidad legal para publicar en el Marketplace.'
            })
        
        # Validar que el URL principal no esté vacío
        if not data.get('url_principal'):
            raise serializers.ValidationError({
                'url_principal': 'El enlace principal es OBLIGATORIO. No se puede publicar sin un enlace externo.'
            })
        
        return data
    
    def create(self, validated_data):
        """Crea un nuevo producto y obtiene metadatos OpenGraph automáticamente."""
        request = self.context.get('request')
        validated_data['vendedor'] = request.user
        validated_data['campus'] = request.user.campus
        validated_data['carrera'] = request.user.career
        
        # Capturar IP del usuario para fines legales
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            validated_data['ip_aceptacion'] = x_forwarded_for.split(',')[0]
        else:
            validated_data['ip_aceptacion'] = request.META.get('REMOTE_ADDR')
        
        # Detectar tipo de enlace automáticamente si no se especificó
        url_principal = validated_data.get('url_principal')
        if url_principal and not validated_data.get('tipo_enlace'):
            validated_data['tipo_enlace'] = ProductoValidationService.detectar_tipo_enlace(url_principal)
        
        # Obtener metadatos OpenGraph de la URL principal
        if url_principal:
            metadatos = OpenGraphService.obtener_metadatos_opengraph(url_principal)
            validated_data.update(metadatos)
        
        producto = super().create(validated_data)
        
        # Crear analytics para el producto
        ProductoAnalytics.objects.create(producto=producto)
        
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
    
    class Meta:
        model = Producto
        fields = [
            'id', 'titulo', 'descripcion', 'categoria_nombre', 'categoria_icono',
            'vendedor_nombre', 'url_principal', 'tipo_enlace', 'og_image',
            'estado', 'precio', 'precio_student_point', 'moneda', 'campus_nombre', 'carrera',
            'created_at', 'visualizaciones', 'es_favorito'
        ]
    
    def get_es_favorito(self, obj):
        """Verifica si el producto es favorito del usuario actual."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoritos.filter(usuario=request.user).exists()
        return False
