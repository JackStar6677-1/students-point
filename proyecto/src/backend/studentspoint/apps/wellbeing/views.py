"""API para contenidos de bienestar."""

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BienestarItem
from .serializers import BienestarItemSerializer


class BienestarListView(generics.ListAPIView):
    """Vista heredada para compatibilidad."""
    serializer_class = BienestarItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        carrera = self.request.query_params.get("carrera")
        qs = BienestarItem.objects.filter(activo=True)
        if carrera:
            qs = qs.filter(carrera__iexact=carrera)
        return qs


class BienestarViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para contenidos de bienestar con filtros avanzados."""
    serializer_class = BienestarItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = BienestarItem.objects.filter(activo=True)
        
        # Filtros
        carrera = self.request.query_params.get("carrera")
        tipo = self.request.query_params.get("tipo")
        categoria = self.request.query_params.get("categoria")
        
        if carrera:
            qs = qs.filter(carrera__icontains=carrera)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if categoria:
            qs = qs.filter(categoria=categoria)
            
        return qs

    @action(detail=False, methods=['get'])
    def carreras(self, request):
        """Lista todas las carreras disponibles."""
        carreras = (
            BienestarItem.objects
            .filter(activo=True)
            .values_list('carrera', flat=True)
            .distinct()
            .order_by('carrera')
        )
        return Response(list(carreras))

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de contenido por tipo."""
        carrera = request.query_params.get("carrera")
        qs = BienestarItem.objects.filter(activo=True)
        
        if carrera:
            qs = qs.filter(carrera__icontains=carrera)
        
        stats = {
            'total': qs.count(),
            'por_tipo': {},
            'por_categoria': {},
        }
        
        # Por tipo
        for tipo_key, tipo_name in BienestarItem.Tipos.choices:
            count = qs.filter(tipo=tipo_key).count()
            stats['por_tipo'][tipo_key] = {
                'nombre': tipo_name,
                'cantidad': count
            }
        
        # Por categoría
        for cat_key, cat_name in BienestarItem.Categorias.choices:
            count = qs.filter(categoria=cat_key).count()
            if count > 0:
                stats['por_categoria'][cat_key] = {
                    'nombre': cat_name,
                    'cantidad': count
                }
        
        return Response(stats)
