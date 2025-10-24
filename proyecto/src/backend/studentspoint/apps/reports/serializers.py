"""Serializadores para la API de reportes."""

from rest_framework import serializers

from .models import Reporte, ReporteMedia


class ReporteMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteMedia
        fields = ["url"]


class ReporteSerializer(serializers.ModelSerializer):
    media = ReporteMediaSerializer(many=True, required=False)

    class Meta:
        model = Reporte
        fields = [
            "id",
            "sede",
            "categoria",
            "descripcion",
            "estado",
            "lat",
            "lng",
            "prioridad",
            "creado_at",
            "media",
        ]
        read_only_fields = ["prioridad", "creado_at"]

    def create(self, validated_data):
        media_data = validated_data.pop("media", [])
        reporte = Reporte.objects.create(**validated_data)
        for media in media_data:
            ReporteMedia.objects.create(reporte=reporte, **media)
        return reporte
