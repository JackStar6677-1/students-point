"""Serializadores para la app de sedes.

Exponen los modelos para ser consumidos por el frontend.
"""

from rest_framework import serializers

from .models import RecorridoPaso, Sede


class SedeSerializer(serializers.ModelSerializer):
    """Serializa información de :class:`Sede`."""

    class Meta:
        model = Sede
        fields = ["slug", "nombre", "direccion", "lat", "lng"]


class RecorridoPasoSerializer(serializers.ModelSerializer):
    """Serializa un paso de recorrido."""
    
    streetview_data = serializers.ReadOnlyField()

    class Meta:
        model = RecorridoPaso
        fields = [
            "orden", "titulo", "descripcion", "imagen_url", "lat", "lng",
            "usar_streetview", "streetview_heading", "streetview_pitch", 
            "streetview_fov", "imagen_360_url", "imagen_360_thumbnail", "streetview_data"
        ]
