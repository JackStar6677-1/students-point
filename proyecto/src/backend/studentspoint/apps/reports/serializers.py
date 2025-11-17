"""Serializadores para la API de reportes."""

from rest_framework import serializers

from .models import Reporte, ReporteMedia


class ReporteMediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ReporteMedia
        fields = ["id", "imagen", "url"]
        read_only_fields = ["id"]
    
    def get_url(self, obj):
        """Retorna la URL de la imagen o la URL alternativa."""
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return obj.url


class ReporteSerializer(serializers.ModelSerializer):
    media = ReporteMediaSerializer(many=True, required=False, read_only=True)
    sede_nombre = serializers.CharField(source="sede.nombre", read_only=True)

    class Meta:
        model = Reporte
        fields = [
            "id",
            "sede",
            "sede_nombre",
            "categoria",
            "descripcion",
            "estado",
            "lat",
            "lng",
            "prioridad",
            "creado_at",
            "media",
        ]
        read_only_fields = ["prioridad", "creado_at", "sede_nombre"]
