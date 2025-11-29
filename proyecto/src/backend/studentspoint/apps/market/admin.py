from django.contrib import admin
from .models import CategoriaProducto, Producto, ProductoFavorito, ProductoReporte, ProductoAnalytics


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'created_at']
    list_filter = ['activa']
    search_fields = ['nombre', 'descripcion']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo',
        'vendedor',
        'categoria',
        'precio',
        'precio_student_point',
        'estado',
        'visualizaciones',
        'created_at',
    ]
    list_filter = ['estado', 'categoria', 'campus', 'tipo_enlace']
    search_fields = ['titulo', 'descripcion', 'vendedor__email']
    readonly_fields = ['visualizaciones', 'clicks_enlace', 'created_at', 'updated_at', 'publicado_at', 'vendido_at']
    date_hierarchy = 'created_at'


@admin.register(ProductoFavorito)
class ProductoFavoritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'created_at']
    list_filter = ['created_at']
    search_fields = ['usuario__email', 'producto__titulo']


@admin.register(ProductoReporte)
class ProductoReporteAdmin(admin.ModelAdmin):
    list_display = ['producto', 'reportador', 'tipo', 'estado', 'created_at']
    list_filter = ['tipo', 'estado', 'created_at']
    search_fields = ['producto__titulo', 'reportador__email', 'descripcion']


@admin.register(ProductoAnalytics)
class ProductoAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['producto', 'total_visualizaciones', 'total_clicks', 'total_favoritos', 'total_reportes', 'ultima_actualizacion']
    readonly_fields = ['producto', 'total_visualizaciones', 'total_clicks', 'total_favoritos', 'total_reportes', 'ultima_actualizacion']
    search_fields = ['producto__titulo']
