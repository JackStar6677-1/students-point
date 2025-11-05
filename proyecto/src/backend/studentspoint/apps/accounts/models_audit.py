"""
Modelos de auditoría para la aplicación de cuentas.
Guarda historial de logins, registros y actividad de usuarios.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class LoginLog(models.Model):
    """Registro de intentos de login (exitosos y fallidos)."""
    
    class Estado(models.TextChoices):
        EXITOSO = "exitoso", "Exitoso"
        FALLIDO = "fallido", "Fallido"
    
    # Usuario (puede ser None si el login falló)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="login_logs"
    )
    
    # Email intentado (útil para logins fallidos)
    email_intentado = models.EmailField()
    
    # Estado del login
    estado = models.CharField(max_length=20, choices=Estado.choices)
    
    # Información de la sesión
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Información adicional
    razon_fallo = models.CharField(max_length=200, blank=True, help_text="Razón si el login falló")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', '-created_at']),
            models.Index(fields=['email_intentado', '-created_at']),
            models.Index(fields=['estado', '-created_at']),
            models.Index(fields=['ip_address', '-created_at']),
        ]
        verbose_name = "Registro de Login"
        verbose_name_plural = "Registros de Login"
    
    def __str__(self):
        return f"{self.email_intentado} - {self.get_estado_display()} - {self.created_at}"


class RegistrationLog(models.Model):
    """Registro de intentos de registro de nuevos usuarios."""
    
    class Estado(models.TextChoices):
        EXITOSO = "exitoso", "Exitoso"
        FALLIDO = "fallido", "Fallido"
        PENDIENTE_VERIFICACION = "pendiente_verificacion", "Pendiente Verificación"
    
    # Usuario creado (puede ser None si el registro falló)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration_logs"
    )
    
    # Email del registro
    email = models.EmailField()
    
    # Nombre intentado
    name_intentado = models.CharField(max_length=150, blank=True)
    
    # Carrera intentada
    career_intentada = models.CharField(max_length=150, blank=True)
    
    # Estado del registro
    estado = models.CharField(max_length=30, choices=Estado.choices)
    
    # Información de la sesión
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Información adicional
    razon_fallo = models.CharField(max_length=200, blank=True, help_text="Razón si el registro falló")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', '-created_at']),
            models.Index(fields=['email', '-created_at']),
            models.Index(fields=['estado', '-created_at']),
        ]
        verbose_name = "Registro de Registro"
        verbose_name_plural = "Registros de Registro"
    
    def __str__(self):
        return f"{self.email} - {self.get_estado_display()} - {self.created_at}"


class UserActivityLog(models.Model):
    """Registro de actividad importante de usuarios en el sistema."""
    
    class TipoActividad(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        REGISTRO = "registro", "Registro"
        VERIFICACION_EMAIL = "verificacion_email", "Verificación de Email"
        CAMBIO_PASSWORD = "cambio_password", "Cambio de Contraseña"
        RECUPERACION_PASSWORD = "recuperacion_password", "Recuperación de Contraseña"
        ACTUALIZACION_PERFIL = "actualizacion_perfil", "Actualización de Perfil"
        CAMBIO_CARRERA = "cambio_carrera", "Cambio de Carrera"
        CREACION_POST = "creacion_post", "Creación de Post"
        CREACION_COMENTARIO = "creacion_comentario", "Creación de Comentario"
        VOTO_POST = "voto_post", "Voto en Post"
        CREACION_PRODUCTO = "creacion_producto", "Creación de Producto"
        CREACION_PROYECTO = "creacion_proyecto", "Creación de Proyecto"
        OTRO = "otro", "Otro"
    
    # Usuario que realizó la actividad
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_logs"
    )
    
    # Tipo de actividad
    tipo = models.CharField(max_length=30, choices=TipoActividad.choices)
    
    # Descripción de la actividad
    descripcion = models.TextField(blank=True)
    
    # Datos adicionales (JSON)
    datos_adicionales = models.JSONField(default=dict, blank=True)
    
    # Información de la sesión
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', '-created_at']),
            models.Index(fields=['tipo', '-created_at']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
    
    def __str__(self):
        return f"{self.usuario.email} - {self.get_tipo_display()} - {self.created_at}"

