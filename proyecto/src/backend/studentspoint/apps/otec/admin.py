"""Admin de cursos OTEC."""

from django.contrib import admin

from .models import Curso, ClaseVideo


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'autor', 'categoria', 'visible', 'created_at']
    list_filter = ['tipo', 'modalidad', 'nivel', 'visible', 'es_gratuito']
    search_fields = ['titulo', 'descripcion', 'categoria']
    readonly_fields = ['created_at', 'updated_at', 'visualizaciones']


@admin.register(ClaseVideo)
class ClaseVideoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'numero_clase', 'orden', 'created_at']
    list_filter = ['curso', 'created_at']
    search_fields = ['titulo', 'descripcion', 'curso__titulo']
    readonly_fields = ['created_at', 'updated_at']
