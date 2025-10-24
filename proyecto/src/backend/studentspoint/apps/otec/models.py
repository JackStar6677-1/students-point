"""Modelos para cursos abiertos OTEC."""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Curso(models.Model):
    """Curso abierto publicado por la comunidad."""

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cursos")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    etiquetas = models.CharField(max_length=200)
    url = models.URLField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    visible = models.BooleanField(default=True)

    def esta_vigente(self) -> bool:
        today = timezone.now().date()
        return self.visible and self.fecha_inicio <= today <= self.fecha_fin

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo
