"""Modelos para reportes de infraestructura."""

from django.conf import settings
from django.db import models


class Reporte(models.Model):
    """Reporte de un problema en la infraestructura del campus."""

    class Estados(models.TextChoices):
        ABIERTO = "abierto", "Abierto"
        REVISION = "revision", "En revisión"
        RESUELTO = "resuelto", "Resuelto"

    sede = models.ForeignKey("campuses.Sede", on_delete=models.CASCADE, related_name="reportes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reportes")
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.ABIERTO)
    prioridad = models.IntegerField(default=0)
    creado_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.categoria} ({self.sede})"


class ReporteMedia(models.Model):
    """Archivos asociados a un :class:`Reporte`."""

    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name="media")
    url = models.URLField()

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.url
