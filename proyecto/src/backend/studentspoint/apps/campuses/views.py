"""Vistas para la app de sedes.

Proveen información para que el frontend pueda mostrar las sedes en un
mapa de Leaflet y los pasos de un recorrido como diapositivas.
"""

from rest_framework.generics import ListAPIView

from .models import RecorridoPaso, Sede
from .serializers import RecorridoPasoSerializer, SedeSerializer


class SedeListView(ListAPIView):
    """Entrega todas las sedes disponibles.

    El frontend usará esta lista para dibujar marcadores en el mapa.
    """

    queryset = Sede.objects.all().order_by("nombre")
    serializer_class = SedeSerializer


class RecorridoPasoListView(ListAPIView):
    """Devuelve los pasos de un recorrido para una sede dada.

    Los pasos se entregan ordenados para que el frontend pueda
    mostrarlos como "slides" y, si corresponde, en el mapa.
    """

    serializer_class = RecorridoPasoSerializer

    def get_queryset(self):
        sede_slug = self.request.query_params.get("sede")
        return RecorridoPaso.objects.filter(
            recorrido__sede__slug=sede_slug
        ).order_by("orden")
