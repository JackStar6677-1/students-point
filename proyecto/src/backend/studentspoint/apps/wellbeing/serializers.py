"""Serializadores para contenidos de bienestar."""

from markdown import markdown
from rest_framework import serializers

from .models import BienestarItem


class BienestarItemSerializer(serializers.ModelSerializer):
    contenido_html = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)

    class Meta:
        model = BienestarItem
        fields = [
            "id",
            "carrera",
            "tipo",
            "tipo_display",
            "categoria",
            "categoria_display",
            "titulo",
            "descripcion_corta",
            "contenido_html",
            "contenido_md",
            "duracion_minutos",
            "media_url",
            "orden",
            "activo",
            "created_at",
            "updated_at",
        ]

    def get_contenido_html(self, obj: BienestarItem) -> str:  # pragma: no cover - librería externa
        return markdown(obj.contenido_md)
