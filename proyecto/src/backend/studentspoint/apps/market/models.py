"""Modelos para el sistema de compra/venta segura."""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator


class CategoriaProducto(models.Model):
    """Categorías para organizar productos en el mercado."""
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text="Clase de icono (ej: bi-book, bi-laptop)")
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto publicado en el mercado con enlaces externos seguros."""
    
    class Estados(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"
        VENDIDO = "vendido", "Vendido"
        OCULTO = "oculto", "Oculto"
    
    class TiposEnlace(models.TextChoices):
        FACEBOOK = "facebook", "Facebook Marketplace"
        YAPO = "yapo", "Yapo.cl"
        MERCADOLIBRE = "mercadolibre", "MercadoLibre"
        OTRO = "otro", "Otro"
    
    # Información básica
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="productos_vendidos"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT, related_name="productos")
    
    # Enlaces externos
    url_principal = models.URLField(validators=[URLValidator()], help_text="Enlace principal de venta")
    tipo_enlace = models.CharField(max_length=20, choices=TiposEnlace.choices, default=TiposEnlace.OTRO)
    urls_adicionales = models.JSONField(
        default=list, 
        blank=True, 
        help_text="Lista de URLs adicionales (ej: fotos, videos)"
    )
    
    # Metadatos de OpenGraph (se llenan automáticamente)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.URLField(blank=True)
    og_site_name = models.CharField(max_length=100, blank=True)
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.BORRADOR)
    precio = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, help_text="Precio en CLP")
    moneda = models.CharField(max_length=3, default="CLP")
    
    # Metadatos
    campus = models.ForeignKey(
        "campuses.Sede", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="productos"
    )
    carrera = models.CharField(max_length=150, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publicado_at = models.DateTimeField(null=True, blank=True)
    vendido_at = models.DateTimeField(null=True, blank=True)
    
    # Estadísticas
    visualizaciones = models.PositiveIntegerField(default=0)
    clicks_enlace = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estado', 'publicado_at']),
            models.Index(fields=['categoria', 'estado']),
            models.Index(fields=['campus', 'carrera']),
        ]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Marcar como publicado si cambia de borrador a publicado
        if self.estado == self.Estados.PUBLICADO and not self.publicado_at:
            self.publicado_at = timezone.now()
        
        # Marcar como vendido si cambia a vendido
        if self.estado == self.Estados.VENDIDO and not self.vendido_at:
            self.vendido_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    @property
    def esta_activo(self):
        """Verifica si el producto está activo y visible."""
        return self.estado == self.Estados.PUBLICADO
    
    @property
    def tiempo_publicado(self):
        """Tiempo transcurrido desde la publicación."""
        if self.publicado_at:
            return timezone.now() - self.publicado_at
        return None


class ProductoFavorito(models.Model):
    """Productos marcados como favoritos por usuarios."""
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="productos_favoritos"
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="favoritos")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'producto']
        verbose_name = "Producto Favorito"
        verbose_name_plural = "Productos Favoritos"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.producto.titulo}"


class ProductoReporte(models.Model):
    """Reportes de productos inapropiados o fraudulentos."""
    
    class TiposReporte(models.TextChoices):
        FRAUDE = "fraude", "Posible Fraude"
        INAPROPIADO = "inapropiado", "Contenido Inapropiado"
        SPAM = "spam", "Spam"
        OTRO = "otro", "Otro"
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="reportes")
    reportador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reportes_productos"
    )
    tipo = models.CharField(max_length=20, choices=TiposReporte.choices)
    descripcion = models.TextField()
    resuelto = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['producto', 'reportador']
        verbose_name = "Reporte de Producto"
        verbose_name_plural = "Reportes de Productos"
    
    def __str__(self):
        return f"Reporte: {self.producto.titulo} - {self.tipo}"


class ProductoAnalytics(models.Model):
    """Analytics de productos para insights."""
    
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name="analytics")
    
    # Métricas de engagement
    total_visualizaciones = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    total_favoritos = models.PositiveIntegerField(default=0)
    total_reportes = models.PositiveIntegerField(default=0)
    
    # Distribución por campus/carrera
    visualizaciones_por_campus = models.JSONField(default=dict)
    visualizaciones_por_carrera = models.JSONField(default=dict)
    
    # Timestamps
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytics de Producto"
        verbose_name_plural = "Analytics de Productos"
    
    def actualizar_estadisticas(self):
        """Recalcula todas las estadísticas del producto."""
        from django.db.models import Count
        
        # Actualizar contadores básicos
        self.total_visualizaciones = self.producto.visualizaciones
        self.total_clicks = self.producto.clicks_enlace
        self.total_favoritos = self.producto.favoritos.count()
        self.total_reportes = self.producto.reportes.count()
        
        # Aquí se podrían agregar más estadísticas complejas
        # como distribución por campus/carrera basada en logs de visualización
        
        self.save()
    
    def __str__(self):
        return f"Analytics: {self.producto.titulo}"