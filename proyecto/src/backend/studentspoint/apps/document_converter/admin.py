from django.contrib import admin
from .models import ConversionJob


@admin.register(ConversionJob)
class ConversionJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'tipo_conversion', 'estado', 'usar_ocr', 'created_at']
    list_filter = ['tipo_conversion', 'estado', 'usar_ocr', 'created_at']
    search_fields = ['usuario__email', 'error_mensaje']
    readonly_fields = ['created_at', 'completed_at']
    date_hierarchy = 'created_at'

