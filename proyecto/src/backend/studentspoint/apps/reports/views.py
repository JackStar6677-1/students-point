"""Views para reportes de infraestructura."""

from rest_framework import permissions, viewsets

from .models import Reporte
from .serializers import ReporteSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ReporteViewSet(viewsets.ModelViewSet):
    """CRUD básico de reportes.

    * Crear: cualquier usuario autenticado puede reportar problemas.
    * Listar: filtra por sede y estado mediante parámetros query.
    * Actualizar: sólo moderadores o administradores pueden cambiar el
      estado del reporte.
    """

    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reporte.objects.all().order_by("-creado_at")

    def get_queryset(self):
        qs = super().get_queryset()
        sede = self.request.query_params.get("sede")
        estado = self.request.query_params.get("estado")
        if sede:
            qs = qs.filter(sede__slug=sede)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role not in {User.Roles.MODERATOR, User.Roles.ADMIN_GLOBAL}:
            self.permission_denied(request)
        return super().partial_update(request, *args, **kwargs)
