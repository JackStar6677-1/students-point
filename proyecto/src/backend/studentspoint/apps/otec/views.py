"""Views para cursos OTEC."""

from django.utils import timezone
from django.db.models import Q
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Curso
from .serializers import CursoSerializer, CursoListSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar cursos y anuncios de clases"""
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = Curso.objects.select_related('autor').all()

    def get_serializer_class(self):
        """Usar serializer simplificado para lista"""
        if self.action == 'list':
            return CursoListSerializer
        return CursoSerializer

    def get_queryset(self):
        """Filtrar y buscar cursos"""
        qs = super().get_queryset()
        
        # Solo mostrar cursos visibles en GET (lista y detalle)
        if self.action in ['list', 'retrieve']:
            qs = qs.filter(visible=True)
        
        # Filtro por tipo
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            qs = qs.filter(tipo=tipo)
        
        # Filtro por categoria
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            qs = qs.filter(categoria__icontains=categoria)
        
        # Filtro por modalidad
        modalidad = self.request.query_params.get('modalidad', None)
        if modalidad:
            qs = qs.filter(modalidad=modalidad)
        
        # Filtro por nivel
        nivel = self.request.query_params.get('nivel', None)
        if nivel:
            qs = qs.filter(nivel=nivel)
        
        # Filtro por gratuito
        gratuito = self.request.query_params.get('gratuito', None)
        if gratuito == 'true':
            qs = qs.filter(Q(es_gratuito=True) | Q(precio__isnull=True))
        
        # Filtro por vigente
        vigente = self.request.query_params.get('vigente', None)
        if vigente == 'true':
            today = timezone.now().date()
            qs = qs.filter(
                fecha_inicio__lte=today
            ).filter(
                Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=today)
            )
        
        # Busqueda por texto
        search = self.request.query_params.get('search', None)
        if search:
            qs = qs.filter(
                Q(titulo__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(categoria__icontains=search) |
                Q(etiquetas__icontains=search)
            )
        
        # Ordenamiento
        ordering = self.request.query_params.get('ordering', '-created_at')
        valid_orderings = [
            'created_at', '-created_at',
            'fecha_inicio', '-fecha_inicio',
            'precio', '-precio',
            'visualizaciones', '-visualizaciones',
            'titulo', '-titulo'
        ]
        if ordering in valid_orderings:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-created_at')
        
        return qs

    def perform_create(self, serializer):
        """Guardar curso con el usuario actual como autor"""
        serializer.save(autor=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Incrementar visualizaciones al ver detalle"""
        instance = self.get_object()
        instance.visualizaciones += 1
        instance.save(update_fields=['visualizaciones'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_cursos(self, request):
        """Obtener cursos del usuario actual"""
        cursos = self.get_queryset().filter(autor=request.user)
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Obtener lista de categorías únicas"""
        categorias = Curso.objects.filter(visible=True).values_list('categoria', flat=True).distinct()
        return Response(sorted(set(categorias)))
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas generales de cursos"""
        qs = Curso.objects.filter(visible=True)
        
        stats = {
            'total_cursos': qs.count(),
            'cursos_personales': qs.filter(tipo=Curso.TipoCurso.ANUNCIO_PERSONAL).count(),
            'cursos_externos': qs.filter(tipo=Curso.TipoCurso.ENLACE_EXTERNO).count(),
            'cursos_gratuitos': qs.filter(Q(es_gratuito=True) | Q(precio__isnull=True)).count(),
            'categorias': qs.values_list('categoria', flat=True).distinct().count(),
        }
        
        return Response(stats)
