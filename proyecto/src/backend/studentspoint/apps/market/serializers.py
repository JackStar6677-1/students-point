"""Serializers para el sistema de compra/venta."""

from rest_framework import serializers
from .models import (
    CategoriaProducto, Producto, ProductoFavorito, 
    ProductoReporte, ProductoAnalytics
)


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
            'estado', 'precio', 'moneda', 'campus', 'campus_nombre', 'carrera',
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
        if obj.publicado_at:
            from django.utils import timezone
            from datetime import timedelta
            
            ahora = timezone.now()
            diferencia = ahora - obj.publicado_at
            
            if diferencia.days > 0:
                return f"hace {diferencia.days} día{'s' if diferencia.days > 1 else ''}"
            elif diferencia.seconds > 3600:
                horas = diferencia.seconds // 3600
                return f"hace {horas} hora{'s' if horas > 1 else ''}"
            elif diferencia.seconds > 60:
                minutos = diferencia.seconds // 60
                return f"hace {minutos} minuto{'s' if minutos > 1 else ''}"
            else:
                return "hace unos segundos"
        return None


class ProductoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear productos."""
    
    class Meta:
        model = Producto
        fields = [
            'titulo', 'descripcion', 'categoria', 'url_principal', 
            'tipo_enlace', 'urls_adicionales', 'precio', 'moneda'
        ]
    
    def create(self, validated_data):
        """Crea un nuevo producto."""
        request = self.context.get('request')
        validated_data['vendedor'] = request.user
        validated_data['campus'] = request.user.campus
        validated_data['carrera'] = request.user.career
        
        producto = super().create(validated_data)
        
        # Crear analytics para el producto
        ProductoAnalytics.objects.create(producto=producto)
        
        return producto


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
            'estado', 'precio', 'moneda', 'campus_nombre', 'carrera',
            'created_at', 'visualizaciones', 'es_favorito'
        ]
    
    def get_es_favorito(self, obj):
        """Verifica si el producto es favorito del usuario actual."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoritos.filter(usuario=request.user).exists()
        return False
