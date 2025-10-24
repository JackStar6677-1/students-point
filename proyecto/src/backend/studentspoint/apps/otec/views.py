"""Views para cursos OTEC."""

from django.utils import timezone
from rest_framework import permissions, viewsets

from .models import Curso
from .serializers import CursoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Curso.objects.all().order_by("-fecha_inicio")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method.lower() == "get":
            today = timezone.now().date()
            qs = qs.filter(visible=True, fecha_inicio__lte=today, fecha_fin__gte=today)
        return qs

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
