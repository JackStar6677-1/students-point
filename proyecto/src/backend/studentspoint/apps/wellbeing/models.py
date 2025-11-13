"""Contenidos de bienestar por carrera."""

from django.db import models
from django.utils import timezone


class BienestarItem(models.Model):
    """Recurso de bienestar para una carrera específica."""

    class Tipos(models.TextChoices):
        FISICO = "fisico", "Bienestar Físico"
        MENTAL = "mental", "Bienestar Mental"
        NUTRICIONAL = "nutricional", "Nutrición"

    class Categorias(models.TextChoices):
        # Bienestar Físico
        POSTURA = "postura", "Postura y Ergonomía"
        EJERCICIOS_OCULARES = "oculares", "Cuidado Visual"
        ESTIRAMIENTOS = "estiramientos", "Estiramientos"
        PAUSAS_ACTIVAS = "pausas", "Pausas Activas"
        
        # Bienestar Mental
        ESTRES = "estres", "Manejo del Estrés"
        ANSIEDAD = "ansiedad", "Ansiedad"
        CONCENTRACION = "concentracion", "Concentración"
        DESCANSO = "descanso", "Descanso y Sueño"
        
        # Nutrición
        ALIMENTACION = "alimentacion", "Alimentación Saludable"
        HIDRATACION = "hidratacion", "Hidratación"
        ENERGIA = "energia", "Energía y Rendimiento"

    carrera = models.CharField(
        max_length=150,
        help_text="Nombre de la carrera (ej: Ingeniería en Informática)"
    )
    tipo = models.CharField(
        max_length=15,
        choices=Tipos.choices,
        help_text="Tipo de bienestar"
    )
    categoria = models.CharField(
        max_length=20,
        choices=Categorias.choices,
        default=Categorias.ESTIRAMIENTOS,
        help_text="Categoría específica del contenido"
    )
    titulo = models.CharField(
        max_length=200,
        help_text="Título del recurso"
    )
    descripcion_corta = models.CharField(
        max_length=300,
        blank=True,
        help_text="Descripción breve para preview"
    )
    contenido_md = models.TextField(
        help_text="Contenido en formato Markdown"
    )
    duracion_minutos = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duración estimada en minutos"
    )
    media_url = models.URLField(
        blank=True,
        help_text="URL de video o imagen complementaria"
    )
    orden = models.IntegerField(
        default=0,
        help_text="Orden de visualización (menor primero)"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si está visible para los estudiantes"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenido de Bienestar"
        verbose_name_plural = "Contenidos de Bienestar"
        ordering = ["orden", "tipo", "categoria", "titulo"]
        indexes = [
            models.Index(fields=["carrera", "tipo"]),
            models.Index(fields=["activo", "orden"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.get_tipo_display()} - {self.titulo} ({self.carrera})"
