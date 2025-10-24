"""Modelos de la aplicación de sedes y recorridos.

Se definen las entidades necesarias para representar los tours que se
mostrarán en el frontend utilizando Leaflet para el mapa y un sistema de
"slides" para recorrer cada paso.
"""

from django.db import models


class Sede(models.Model):
    """Representa una sede física del DUOC UC.

    El frontend utilizará este modelo para mostrar marcadores en un mapa
    de Leaflet, por lo que incluye las coordenadas geográficas.
    """

    slug = models.SlugField(unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.nombre


class Recorrido(models.Model):
    """Agrupa los pasos de un tour por una sede.

    El título permite distinguir distintos recorridos dentro de una
    misma sede. En el frontend se mostrará como encabezado del tour.
    """

    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="recorridos")
    titulo = models.CharField(max_length=200)

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo


class RecorridoPaso(models.Model):
    """Paso individual dentro de un recorrido.

    Cada paso se mostrará como una diapositiva y opcionalmente como un
    punto en el mapa de Leaflet.
    """

    recorrido = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name="pasos")
    orden = models.PositiveIntegerField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_url = models.URLField()
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    
    # Campos para Street View personalizado
    usar_streetview = models.BooleanField(default=False, help_text="Usar Street View personalizado en lugar de imagen estática")
    streetview_heading = models.FloatField(default=0, help_text="Dirección de la cámara en grados (0-360)")
    streetview_pitch = models.FloatField(default=0, help_text="Inclinación de la cámara (-90 a 90)")
    streetview_fov = models.FloatField(default=90, help_text="Campo de visión (10-120 grados)")
    
    # Imágenes adicionales para Street View personalizado
    imagen_360_url = models.URLField(blank=True, help_text="URL de imagen 360° para Street View personalizado")
    imagen_360_thumbnail = models.URLField(blank=True, help_text="Thumbnail de la imagen 360°")

    class Meta:
        ordering = ["orden"]

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.orden}. {self.titulo}"
    
    @property
    def streetview_data(self):
        """Retorna datos para Street View personalizado."""
        if not self.usar_streetview:
            return None
        
        return {
            'imagen_360': self.imagen_360_url,
            'thumbnail': self.imagen_360_thumbnail,
            'heading': self.streetview_heading,
            'pitch': self.streetview_pitch,
            'fov': self.streetview_fov,
            'lat': self.lat,
            'lng': self.lng
        }
