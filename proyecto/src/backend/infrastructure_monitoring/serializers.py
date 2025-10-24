"""
Serializers para el sistema de monitoreo de infraestructura.
"""

from rest_framework import serializers
from .models import (
    InfraestructuraItem, ReporteInfraestructura, MetricasInfraestructura,
    MantenimientoProgramado, DashboardConfig, AlertaInfraestructura
)


class InfraestructuraItemSerializer(serializers.ModelSerializer):
    """Serializer para elementos de infraestructura."""
    
    campus_nombre = serializers.CharField(source='campus.name', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.name', read_only=True)
    total_reportes = serializers.SerializerMethodField()
    reportes_abiertos = serializers.SerializerMethodField()
    ultima_metrica = serializers.SerializerMethodField()
    
    class Meta:
        model = InfraestructuraItem
        fields = [
            'id', 'nombre', 'tipo', 'ubicacion', 'descripcion', 'estado_actual',
            'capacidad_maxima', 'responsable', 'responsable_nombre', 'campus',
            'campus_nombre', 'activo', 'created_at', 'updated_at',
            'total_reportes', 'reportes_abiertos', 'ultima_metrica'
        ]
    
    def get_total_reportes(self, obj):
        return obj.reportes.count()
    
    def get_reportes_abiertos(self, obj):
        return obj.reportes.filter(estado__in=['abierto', 'en_proceso']).count()
    
    def get_ultima_metrica(self, obj):
        ultima = obj.metricas.first()
        if ultima:
            return {
                'fecha': ultima.fecha_medicion,
                'ocupacion_actual': ultima.ocupacion_actual,
                'temperatura': ultima.temperatura,
                'calificacion': ultima.calificacion_satisfaccion
            }
        return None


class ReporteInfraestructuraSerializer(serializers.ModelSerializer):
    """Serializer para reportes de infraestructura."""
    
    item_nombre = serializers.CharField(source='item.nombre', read_only=True)
    item_tipo = serializers.CharField(source='item.tipo', read_only=True)
    reportado_por_nombre = serializers.CharField(source='reportado_por.name', read_only=True)
    resuelto_por_nombre = serializers.CharField(source='resuelto_por.name', read_only=True)
    dias_abierto = serializers.SerializerMethodField()
    
    class Meta:
        model = ReporteInfraestructura
        fields = [
            'id', 'item', 'item_nombre', 'item_tipo', 'reportado_por', 'reportado_por_nombre',
            'tipo', 'titulo', 'descripcion', 'prioridad', 'estado', 'fecha_reporte',
            'fecha_resolucion', 'resuelto_por', 'resuelto_por_nombre', 'solucion',
            'imagenes', 'costo_reparacion', 'tiempo_resolucion_horas', 'dias_abierto'
        ]
    
    def get_dias_abierto(self, obj):
        if obj.estado in ['abierto', 'en_proceso']:
            delta = timezone.now() - obj.fecha_reporte
            return delta.days
        return None


class MetricasInfraestructuraSerializer(serializers.ModelSerializer):
    """Serializer para métricas de infraestructura."""
    
    item_nombre = serializers.CharField(source='item.nombre', read_only=True)
    
    class Meta:
        model = MetricasInfraestructura
        fields = [
            'id', 'item', 'item_nombre', 'fecha_medicion', 'ocupacion_actual',
            'ocupacion_promedio', 'tiempo_uso_total', 'temperatura', 'humedad',
            'ruido_db', 'velocidad_wifi', 'calificacion_satisfaccion', 'comentarios'
        ]


class MantenimientoProgramadoSerializer(serializers.ModelSerializer):
    """Serializer para mantenimientos programados."""
    
    item_nombre = serializers.CharField(source='item.nombre', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.name', read_only=True)
    dias_restantes = serializers.SerializerMethodField()
    
    class Meta:
        model = MantenimientoProgramado
        fields = [
            'id', 'item', 'item_nombre', 'tipo', 'titulo', 'descripcion',
            'fecha_programada', 'duracion_estimada_horas', 'responsable',
            'responsable_nombre', 'costo_estimado', 'completado', 'fecha_completado',
            'observaciones', 'dias_restantes'
        ]
    
    def get_dias_restantes(self, obj):
        if not obj.completado:
            delta = obj.fecha_programada - timezone.now()
            return max(0, delta.days)
        return None


class DashboardConfigSerializer(serializers.ModelSerializer):
    """Serializer para configuración del dashboard."""
    
    class Meta:
        model = DashboardConfig
        fields = [
            'id', 'mostrar_metricas_tiempo_real', 'mostrar_reportes_recientes',
            'mostrar_mantenimientos_pendientes', 'mostrar_alertas', 'mostrar_graficos_ocupacion',
            'umbral_ocupacion', 'umbral_temperatura_max', 'umbral_temperatura_min',
            'umbral_ruido', 'recibir_alertas_email', 'recibir_alertas_push',
            'frecuencia_alertas', 'created_at', 'updated_at'
        ]


class AlertaInfraestructuraSerializer(serializers.ModelSerializer):
    """Serializer para alertas de infraestructura."""
    
    item_nombre = serializers.CharField(source='item.nombre', read_only=True)
    item_ubicacion = serializers.CharField(source='item.ubicacion', read_only=True)
    resuelta_por_nombre = serializers.CharField(source='resuelta_por.name', read_only=True)
    horas_activa = serializers.SerializerMethodField()
    
    class Meta:
        model = AlertaInfraestructura
        fields = [
            'id', 'item', 'item_nombre', 'item_ubicacion', 'tipo', 'nivel',
            'titulo', 'mensaje', 'valor_actual', 'valor_umbral', 'activa',
            'fecha_generada', 'fecha_resuelta', 'resuelta_por', 'resuelta_por_nombre',
            'horas_activa'
        ]
    
    def get_horas_activa(self, obj):
        if obj.activa:
            delta = timezone.now() - obj.fecha_generada
            return round(delta.total_seconds() / 3600, 1)
        return None


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas del dashboard."""
    
    total_items = serializers.IntegerField()
    items_operativos = serializers.IntegerField()
    items_mantenimiento = serializers.IntegerField()
    items_fuera_servicio = serializers.IntegerField()
    
    total_reportes = serializers.IntegerField()
    reportes_abiertos = serializers.IntegerField()
    reportes_resueltos_hoy = serializers.IntegerField()
    
    total_alertas = serializers.IntegerField()
    alertas_activas = serializers.IntegerField()
    alertas_criticas = serializers.IntegerField()
    
    mantenimientos_pendientes = serializers.IntegerField()
    mantenimientos_hoy = serializers.IntegerField()
    
    ocupacion_promedio = serializers.FloatField()
    satisfaccion_promedio = serializers.FloatField()
    
    items_mas_usados = serializers.ListField()
    items_problemas = serializers.ListField()
    tendencias_ocupacion = serializers.ListField()
