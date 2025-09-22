"""
Modelos para el sistema de monitoreo de infraestructura.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class InfraestructuraItem(models.Model):
    """Elementos de infraestructura del campus que se monitorean."""
    
    TIPOS_ITEM = [
        ('aula', 'Aula'),
        ('laboratorio', 'Laboratorio'),
        ('biblioteca', 'Biblioteca'),
        ('cafeteria', 'Cafetería'),
        ('gimnasio', 'Gimnasio'),
        ('auditorio', 'Auditorio'),
        ('oficina', 'Oficina'),
        ('estacionamiento', 'Estacionamiento'),
        ('wifi', 'WiFi'),
        ('servidor', 'Servidor'),
        ('aire_acondicionado', 'Aire Acondicionado'),
        ('iluminacion', 'Iluminación'),
        ('otro', 'Otro'),
    ]
    
    ESTADOS_ITEM = [
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('fuera_servicio', 'Fuera de Servicio'),
        ('reparacion', 'En Reparación'),
        ('obsoleto', 'Obsoleto'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPOS_ITEM)
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado_actual = models.CharField(max_length=20, choices=ESTADOS_ITEM, default='operativo')
    capacidad_maxima = models.PositiveIntegerField(null=True, blank=True, help_text="Capacidad máxima de personas")
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='infraestructura_responsable'
    )
    campus = models.ForeignKey(
        'campuses.Sede',
        on_delete=models.CASCADE,
        related_name='infraestructura_items'
    )
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name = 'Elemento de Infraestructura'
        verbose_name_plural = 'Elementos de Infraestructura'
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"


class ReporteInfraestructura(models.Model):
    """Reportes de problemas o actualizaciones de infraestructura."""
    
    TIPOS_REPORTE = [
        ('problema', 'Problema'),
        ('mantenimiento', 'Mantenimiento'),
        ('mejora', 'Mejora'),
        ('incidente', 'Incidente'),
        ('actualizacion', 'Actualización'),
    ]
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    ESTADOS_REPORTE = [
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
        ('cancelado', 'Cancelado'),
    ]
    
    item = models.ForeignKey(InfraestructuraItem, on_delete=models.CASCADE, related_name='reportes')
    reportado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reportes_infraestructura'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    estado = models.CharField(max_length=20, choices=ESTADOS_REPORTE, default='abierto')
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelto_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reportes_resueltos'
    )
    solucion = models.TextField(blank=True)
    imagenes = models.JSONField(default=list, blank=True, help_text="URLs de imágenes del problema")
    costo_reparacion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tiempo_resolucion_horas = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_reporte']
        verbose_name = 'Reporte de Infraestructura'
        verbose_name_plural = 'Reportes de Infraestructura'
    
    def __str__(self):
        return f"{self.titulo} - {self.item.nombre}"


class MetricasInfraestructura(models.Model):
    """Métricas y estadísticas de la infraestructura."""
    
    item = models.ForeignKey(InfraestructuraItem, on_delete=models.CASCADE, related_name='metricas')
    fecha_medicion = models.DateTimeField(auto_now_add=True)
    
    # Métricas de uso
    ocupacion_actual = models.PositiveIntegerField(default=0, help_text="Personas actualmente en el espacio")
    ocupacion_promedio = models.FloatField(default=0.0, help_text="Ocupación promedio en las últimas 24h")
    tiempo_uso_total = models.PositiveIntegerField(default=0, help_text="Tiempo total de uso en minutos")
    
    # Métricas de rendimiento
    temperatura = models.FloatField(null=True, blank=True, help_text="Temperatura en °C")
    humedad = models.FloatField(null=True, blank=True, help_text="Humedad en %")
    ruido_db = models.FloatField(null=True, blank=True, help_text="Nivel de ruido en dB")
    velocidad_wifi = models.FloatField(null=True, blank=True, help_text="Velocidad WiFi en Mbps")
    
    # Métricas de satisfacción
    calificacion_satisfaccion = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de satisfacción de 1 a 5"
    )
    comentarios = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_medicion']
        verbose_name = 'Métrica de Infraestructura'
        verbose_name_plural = 'Métricas de Infraestructura'
    
    def __str__(self):
        return f"Métricas {self.item.nombre} - {self.fecha_medicion}"


class MantenimientoProgramado(models.Model):
    """Mantenimientos programados para la infraestructura."""
    
    TIPOS_MANTENIMIENTO = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('mejora', 'Mejora'),
        ('inspeccion', 'Inspección'),
        ('limpieza', 'Limpieza'),
    ]
    
    item = models.ForeignKey(InfraestructuraItem, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS_MANTENIMIENTO)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_programada = models.DateTimeField()
    duracion_estimada_horas = models.PositiveIntegerField()
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mantenimientos_responsable'
    )
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['fecha_programada']
        verbose_name = 'Mantenimiento Programado'
        verbose_name_plural = 'Mantenimientos Programados'
    
    def __str__(self):
        return f"{self.titulo} - {self.item.nombre}"


class DashboardConfig(models.Model):
    """Configuración del dashboard de monitoreo para administradores."""
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='dashboard_config'
    )
    
    # Configuración de widgets
    mostrar_metricas_tiempo_real = models.BooleanField(default=True)
    mostrar_reportes_recientes = models.BooleanField(default=True)
    mostrar_mantenimientos_pendientes = models.BooleanField(default=True)
    mostrar_alertas = models.BooleanField(default=True)
    mostrar_graficos_ocupacion = models.BooleanField(default=True)
    
    # Configuración de alertas
    umbral_ocupacion = models.PositiveIntegerField(default=80, help_text="Umbral de ocupación para alertas (%)")
    umbral_temperatura_max = models.FloatField(default=30.0, help_text="Temperatura máxima (°C)")
    umbral_temperatura_min = models.FloatField(default=18.0, help_text="Temperatura mínima (°C)")
    umbral_ruido = models.FloatField(default=70.0, help_text="Umbral de ruido (dB)")
    
    # Configuración de notificaciones
    recibir_alertas_email = models.BooleanField(default=True)
    recibir_alertas_push = models.BooleanField(default=True)
    frecuencia_alertas = models.CharField(max_length=20, choices=[
        ('inmediato', 'Inmediato'),
        ('cada_15min', 'Cada 15 minutos'),
        ('cada_hora', 'Cada hora'),
        ('diario', 'Diario')
    ], default='inmediato')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración de Dashboard'
        verbose_name_plural = 'Configuraciones de Dashboard'
    
    def __str__(self):
        return f"Dashboard Config: {self.usuario.email}"


class AlertaInfraestructura(models.Model):
    """Alertas generadas por el sistema de monitoreo."""
    
    TIPOS_ALERTA = [
        ('ocupacion', 'Ocupación'),
        ('temperatura', 'Temperatura'),
        ('ruido', 'Ruido'),
        ('wifi', 'WiFi'),
        ('mantenimiento', 'Mantenimiento'),
        ('incidente', 'Incidente'),
    ]
    
    NIVELES_ALERTA = [
        ('info', 'Informativa'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('critical', 'Crítica'),
    ]
    
    item = models.ForeignKey(InfraestructuraItem, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
    nivel = models.CharField(max_length=10, choices=NIVELES_ALERTA)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    valor_actual = models.FloatField(null=True, blank=True, help_text="Valor que disparó la alerta")
    valor_umbral = models.FloatField(null=True, blank=True, help_text="Umbral configurado")
    activa = models.BooleanField(default=True)
    fecha_generada = models.DateTimeField(auto_now_add=True)
    fecha_resuelta = models.DateTimeField(null=True, blank=True)
    resuelta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_resueltas'
    )
    
    class Meta:
        ordering = ['-fecha_generada']
        verbose_name = 'Alerta de Infraestructura'
        verbose_name_plural = 'Alertas de Infraestructura'
    
    def __str__(self):
        return f"{self.titulo} - {self.item.nombre}"