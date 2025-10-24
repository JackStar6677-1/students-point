"""Serializadores para cursos OTEC."""

from rest_framework import serializers

from .models import Curso


class CursoSerializer(serializers.ModelSerializer):
    vigente = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = [
            "id",
            "titulo",
            "descripcion",
            "etiquetas",
            "url",
            "fecha_inicio",
            "fecha_fin",
            "visible",
            "vigente",
        ]
        read_only_fields = ["vigente"]

    def get_vigente(self, obj: Curso) -> bool:  # pragma: no cover - lógica simple
        return obj.esta_vigente()
