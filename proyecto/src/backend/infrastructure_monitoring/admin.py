"""
Admin para el sistema de monitoreo de infraestructura.
"""

from django.contrib import admin
from .models import (
    InfraestructuraItem, ReporteInfraestructura, MetricasInfraestructura,
    MantenimientoProgramado, DashboardConfig, AlertaInfraestructura
)


@admin.register(InfraestructuraItem)
class InfraestructuraItemAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'ubicacion', 'estado_actual', 'campus', 'activo']
    list_filter = ['tipo', 'estado_actual', 'campus', 'activo']
    search_fields = ['nombre', 'ubicacion', 'descripcion']
    raw_id_fields = ['responsable', 'campus']


@admin.register(ReporteInfraestructura)
class ReporteInfraestructuraAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'item', 'tipo', 'prioridad', 'estado', 'fecha_reporte', 'reportado_por']
    list_filter = ['tipo', 'prioridad', 'estado', 'fecha_reporte']
    search_fields = ['titulo', 'descripcion', 'item__nombre']
    raw_id_fields = ['item', 'reportado_por', 'resuelto_por']


@admin.register(MetricasInfraestructura)
class MetricasInfraestructuraAdmin(admin.ModelAdmin):
    list_display = ['item', 'fecha_medicion', 'ocupacion_actual', 'temperatura', 'calificacion_satisfaccion']
    list_filter = ['fecha_medicion', 'item__tipo']
    search_fields = ['item__nombre', 'comentarios']
    raw_id_fields = ['item']


@admin.register(MantenimientoProgramado)
class MantenimientoProgramadoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'item', 'tipo', 'fecha_programada', 'completado', 'responsable']
    list_filter = ['tipo', 'completado', 'fecha_programada']
    search_fields = ['titulo', 'descripcion', 'item__nombre']
    raw_id_fields = ['item', 'responsable']


@admin.register(DashboardConfig)
class DashboardConfigAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'mostrar_metricas_tiempo_real', 'recibir_alertas_email', 'frecuencia_alertas']
    list_filter = ['mostrar_metricas_tiempo_real', 'recibir_alertas_email', 'frecuencia_alertas']
    search_fields = ['usuario__email', 'usuario__name']
    raw_id_fields = ['usuario']


@admin.register(AlertaInfraestructura)
class AlertaInfraestructuraAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'item', 'tipo', 'nivel', 'activa', 'fecha_generada']
    list_filter = ['tipo', 'nivel', 'activa', 'fecha_generada']
    search_fields = ['titulo', 'mensaje', 'item__nombre']
    raw_id_fields = ['item', 'resuelta_por']