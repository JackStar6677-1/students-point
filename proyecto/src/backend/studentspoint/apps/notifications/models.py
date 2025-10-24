"""Models for storing Web Push subscriptions."""

import uuid

from django.conf import settings
from django.db import models


class PushSub(models.Model):
    """Represents a Web Push subscription for a user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.endpoint


class Notificacion(models.Model):
    """Modelo para almacenar notificaciones del sistema."""
    
    TIPOS_NOTIFICACION = [
        ('info', 'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('forum', 'Foro'),
        ('market', 'Mercado'),
        ('portfolio', 'Portafolio'),
        ('campus', 'Campus'),
        ('polls', 'Encuestas'),
        ('academic', 'Académico'),
        ('system', 'Sistema'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_NOTIFICACION, default='info')
    leida = models.BooleanField(default=False)
    data_extra = models.JSONField(default=dict, blank=True)
    url_redirect = models.URLField(blank=True, help_text="URL a la que redirigir al hacer clic")
    icono = models.CharField(max_length=50, blank=True, help_text="Clase de icono FontAwesome")
    prioridad = models.CharField(max_length=10, choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], default='media')
    enviada_push = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    leida_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        indexes = [
            models.Index(fields=['usuario', 'leida']),
            models.Index(fields=['tipo', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.email}"
    
    def marcar_como_leida(self):
        """Marca la notificación como leída."""
        from django.utils import timezone
        self.leida = True
        self.leida_at = timezone.now()
        self.save(update_fields=['leida', 'leida_at'])


class NotificacionTemplate(models.Model):
    """Plantillas para notificaciones automáticas."""
    
    nombre = models.CharField(max_length=100, unique=True)
    titulo_template = models.CharField(max_length=200)
    mensaje_template = models.TextField()
    tipo = models.CharField(max_length=20, choices=Notificacion.TIPOS_NOTIFICACION)
    icono = models.CharField(max_length=50, blank=True)
    prioridad = models.CharField(max_length=10, choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], default='media')
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plantilla de Notificación'
        verbose_name_plural = 'Plantillas de Notificaciones'
    
    def __str__(self):
        return self.nombre


class NotificacionConfig(models.Model):
    """Configuración de notificaciones por usuario."""
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacion_config')
    
    # Configuración de tipos de notificaciones
    recibir_foro = models.BooleanField(default=True)
    recibir_market = models.BooleanField(default=True)
    recibir_portfolio = models.BooleanField(default=True)
    recibir_campus = models.BooleanField(default=True)
    recibir_polls = models.BooleanField(default=True)
    recibir_academic = models.BooleanField(default=True)
    recibir_system = models.BooleanField(default=True)
    
    # Configuración de frecuencia
    frecuencia_email = models.CharField(max_length=20, choices=[
        ('inmediato', 'Inmediato'),
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('nunca', 'Nunca')
    ], default='inmediato')
    
    # Configuración de horarios
    horario_inicio = models.TimeField(default='09:00')
    horario_fin = models.TimeField(default='18:00')
    solo_dias_laborales = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración de Notificaciones'
        verbose_name_plural = 'Configuraciones de Notificaciones'
    
    def __str__(self):
        return f"Config: {self.usuario.email}"
