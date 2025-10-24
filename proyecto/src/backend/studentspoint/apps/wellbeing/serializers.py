"""Serializadores para contenidos de bienestar."""

from markdown import markdown
from rest_framework import serializers

from .models import BienestarItem


class BienestarItemSerializer(serializers.ModelSerializer):
    contenido_html = serializers.SerializerMethodField()

    class Meta:
        model = BienestarItem
        fields = ["id", "carrera", "tipo", "titulo", "contenido_html", "media_url"]

    def get_contenido_html(self, obj: BienestarItem) -> str:  # pragma: no cover - librería externa
        return markdown(obj.contenido_md)
