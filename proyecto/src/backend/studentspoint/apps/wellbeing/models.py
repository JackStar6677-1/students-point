"""Contenidos de bienestar por carrera."""

from django.db import models


class BienestarItem(models.Model):
    """Recurso de bienestar para una carrera específica."""

    class Tipos(models.TextChoices):
        KINE = "kine", "Kinesiología"
        PSICO = "psico", "Psicología"

    carrera = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=Tipos.choices)
    titulo = models.CharField(max_length=200)
    contenido_md = models.TextField()
    media_url = models.URLField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.titulo
