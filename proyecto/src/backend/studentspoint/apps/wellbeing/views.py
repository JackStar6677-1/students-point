"""API para contenidos de bienestar."""

from rest_framework import generics, permissions

from .models import BienestarItem
from .serializers import BienestarItemSerializer


class BienestarListView(generics.ListAPIView):
    serializer_class = BienestarItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        carrera = self.request.query_params.get("carrera")
        qs = BienestarItem.objects.all()
        if carrera:
            qs = qs.filter(carrera__iexact=carrera)
        return qs
