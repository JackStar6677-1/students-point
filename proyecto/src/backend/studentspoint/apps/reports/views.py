"""Views para reportes de infraestructura."""

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .models import Reporte, ReporteMedia
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
    
    def get_serializer_context(self):
        """Asegura que el serializer tenga el contexto del request para generar URLs absolutas."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        sede = self.request.query_params.get("sede")
        estado = self.request.query_params.get("estado")
        categoria = self.request.query_params.get("categoria")
        fecha_inicio = self.request.query_params.get("fecha_inicio")
        fecha_fin = self.request.query_params.get("fecha_fin")
        if sede:
            qs = qs.filter(sede__slug=sede)
        if estado:
            qs = qs.filter(estado=estado)
        if categoria:
            qs = qs.filter(categoria__iexact=categoria)
        if fecha_inicio:
            qs = qs.filter(creado_at__date__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(creado_at__date__lte=fecha_fin)
        return qs

    def create(self, request, *args, **kwargs):
        """Sobrescribe create para manejar subida de archivos."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Crear el reporte
        reporte = serializer.save(usuario=request.user)
        
        # Procesar imágenes subidas
        imagenes = []
        # Buscar archivos con nombres que contengan 'imagen' o 'foto'
        for key in request.FILES:
            file = request.FILES[key]
            if file.content_type and file.content_type.startswith('image/'):
                imagenes.append(file)
        
        # Crear ReporteMedia para cada imagen
        for imagen in imagenes:
            ReporteMedia.objects.create(reporte=reporte, imagen=imagen)
        
        # Retornar el reporte con las imágenes
        response_serializer = self.get_serializer(reporte, context={'request': request})
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        # Este método ya no se usa directamente, pero lo mantenemos por compatibilidad
        serializer.save(usuario=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role not in {User.Roles.MODERATOR, User.Roles.ADMIN_GLOBAL}:
            self.permission_denied(request)
        return super().partial_update(request, *args, **kwargs)
