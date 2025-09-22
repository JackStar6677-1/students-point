"""Modelos de encuestas mejorados para StudentsPoint.

Sistema completo de encuestas que permite:
- Encuestas independientes (no solo vinculadas a posts)
- Filtrado por sede y carrera
- Configuración de visibilidad de resultados
- Exportación de datos para análisis
- Validaciones de seguridad
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator


class Poll(models.Model):
    """Encuesta mejorada con soporte independiente y filtros por sede/carrera."""

    class TipoResultados(models.TextChoices):
        TIEMPO_REAL = "tiempo_real", "Resultados en Tiempo Real"
        AL_CIERRE = "al_cierre", "Resultados al Cierre"
        SOLO_MODERADOR = "solo_moderador", "Solo Visible para Moderadores"

    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        ACTIVA = "activa", "Activa"
        CERRADA = "cerrada", "Cerrada"
        ARCHIVADA = "archivada", "Archivada"

    # Campos básicos
    titulo = models.CharField(max_length=200, validators=[MinLengthValidator(5)], default="Encuesta sin título")
    descripcion = models.TextField(blank=True)
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="encuestas_creadas", null=True, blank=True
    )
    
    # Configuración de la encuesta
    multi = models.BooleanField(default=False, help_text="Permite seleccionar múltiples opciones")
    anonima = models.BooleanField(default=False, help_text="Los votos son anónimos")
    requiere_justificacion = models.BooleanField(default=False, help_text="Requiere comentario al votar")
    
    # Filtros por sede/carrera
    sedes = models.ManyToManyField(
        "campuses.Sede", blank=True, help_text="Sedes que pueden participar (todas si vacío)"
    )
    carreras = models.JSONField(
        default=list, blank=True, help_text="Lista de carreras que pueden participar"
    )
    
    # Configuración de resultados
    mostrar_resultados = models.CharField(
        max_length=20, choices=TipoResultados.choices, default=TipoResultados.TIEMPO_REAL
    )
    
    # Fechas y estado
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    inicia_at = models.DateTimeField(default=timezone.now)
    cierra_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Relación opcional con posts del foro (para mantener compatibilidad)
    post = models.OneToOneField(
        "forum.Post", on_delete=models.CASCADE, related_name="poll", null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["estado", "inicia_at"]),
            models.Index(fields=["creador", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.titulo
    
    @property
    def esta_activa(self) -> bool:
        """Verifica si la encuesta está activa y dentro del periodo de votación."""
        ahora = timezone.now()
        return (
            self.estado == self.Estado.ACTIVA and
            self.inicia_at <= ahora and
            (self.cierra_at is None or self.cierra_at > ahora)
        )
    
    @property
    def total_votos(self) -> int:
        """Total de votos únicos (usuarios que han votado)."""
        return self.votos.values("usuario").distinct().count()
    
    def puede_votar(self, usuario) -> bool:
        """Verifica si un usuario puede votar en esta encuesta."""
        if not self.esta_activa:
            return False
            
        # Verificar sede
        if self.sedes.exists() and usuario.campus:
            if not self.sedes.filter(id=usuario.campus_id).exists():
                return False
                
        # Verificar carrera
        if self.carreras and usuario.career:
            if usuario.career not in self.carreras:
                return False
                
        return True
    
    def puede_ver_resultados(self, usuario) -> bool:
        """Verifica si un usuario puede ver los resultados."""
        # Moderadores y creador siempre pueden ver
        if usuario == self.creador or usuario.role in ["moderator", "director_carrera", "admin_global"]:
            return True
            
        if self.mostrar_resultados == self.TipoResultados.SOLO_MODERADOR:
            return False
        elif self.mostrar_resultados == self.TipoResultados.AL_CIERRE:
            return not self.esta_activa
        else:  # TIEMPO_REAL
            return True


class PollOpcion(models.Model):
    """Opción posible dentro de una encuesta con metadatos adicionales."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    descripcion = models.TextField(blank=True, help_text="Descripción detallada de la opción")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    color = models.CharField(
        max_length=7, blank=True, help_text="Color hexadecimal para gráficos (#RRGGBB)"
    )
    
    class Meta:
        ordering = ["orden", "id"]
        unique_together = ("poll", "texto")

    def __str__(self) -> str:
        return self.texto
    
    @property
    def total_votos(self) -> int:
        """Total de votos para esta opción."""
        return self.votos.count()
    
    @property
    def porcentaje_votos(self) -> float:
        """Porcentaje de votos sobre el total de la encuesta."""
        total_encuesta = self.poll.total_votos
        if total_encuesta == 0:
            return 0.0
        return round((self.total_votos / total_encuesta) * 100, 2)


class PollVoto(models.Model):
    """Registro de votos por usuario y opción con metadatos adicionales."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votos")
    opcion = models.ForeignKey(
        PollOpcion, on_delete=models.CASCADE, related_name="votos"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poll_votes"
    )
    justificacion = models.TextField(blank=True, help_text="Comentario opcional del votante")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # Metadatos del usuario al momento del voto (para análisis)
    sede_voto = models.ForeignKey(
        "campuses.Sede", on_delete=models.SET_NULL, null=True, blank=True
    )
    carrera_voto = models.CharField(max_length=150, blank=True)

    class Meta:
        unique_together = ("poll", "usuario", "opcion")
        indexes = [
            models.Index(fields=["poll", "created_at"]),
            models.Index(fields=["usuario", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.usuario.name} -> {self.opcion.texto}"
    
    def save(self, *args, **kwargs):
        # Guardar metadatos del usuario al momento del voto
        if not self.pk:
            self.sede_voto = self.usuario.campus
            self.carrera_voto = self.usuario.career
        super().save(*args, **kwargs)
        
        # Actualizar analytics cuando se crea un nuevo voto
        analytics, created = PollAnalytics.objects.get_or_create(poll=self.poll)
        if not created:
            analytics.actualizar_estadisticas()


class PollAnalytics(models.Model):
    """Estadísticas y análisis de encuestas para insights."""
    
    poll = models.OneToOneField(Poll, on_delete=models.CASCADE, related_name="analytics")
    total_visualizaciones = models.PositiveIntegerField(default=0)
    total_participantes = models.PositiveIntegerField(default=0)
    tasa_participacion = models.FloatField(default=0.0)  # porcentaje
    
    # Distribución por sede
    distribucion_sedes = models.JSONField(default=dict)
    # Distribución por carrera  
    distribucion_carreras = models.JSONField(default=dict)
    
    # Timestamps
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Poll Analytics"
        verbose_name_plural = "Poll Analytics"
    
    def actualizar_estadisticas(self):
        """Recalcula todas las estadísticas de la encuesta."""
        from django.db.models import Count
        
        # Total de participantes únicos
        self.total_participantes = self.poll.votos.values("usuario").distinct().count()
        
        # Distribución por sede
        sedes_stats = self.poll.votos.values("sede_voto__nombre").annotate(
            count=Count("usuario", distinct=True)
        )
        self.distribucion_sedes = {
            item["sede_voto__nombre"] or "Sin sede": item["count"] 
            for item in sedes_stats
        }
        
        # Distribución por carrera
        carreras_stats = self.poll.votos.values("carrera_voto").annotate(
            count=Count("usuario", distinct=True)
        )
        self.distribucion_carreras = {
            item["carrera_voto"] or "Sin carrera": item["count"]
            for item in carreras_stats
        }
        
        self.save()
    
    def __str__(self):
        return f"Analytics: {self.poll.titulo}"