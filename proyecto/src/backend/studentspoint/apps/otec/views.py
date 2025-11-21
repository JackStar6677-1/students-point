"""Views para cursos OTEC."""

from django.utils import timezone
from django.db.models import Q
from rest_framework import permissions, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Curso, ClaseVideo
from .serializers import CursoSerializer, CursoListSerializer, ClaseVideoSerializer


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
            # Un curso es vigente si:
            # - No tiene fecha_inicio O fecha_inicio <= today
            # - No tiene fecha_fin O fecha_fin >= today
            qs = qs.filter(
                Q(fecha_inicio__isnull=True) | Q(fecha_inicio__lte=today)
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
        serializer = self.get_serializer(instance, context={'request': request})
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
            'cursos_video': qs.filter(tipo=Curso.TipoCurso.CURSO_VIDEO).count(),
            'cursos_gratuitos': qs.filter(Q(es_gratuito=True) | Q(precio__isnull=True)).count(),
            'categorias': qs.values_list('categoria', flat=True).distinct().count(),
        }
        
        return Response(stats)


class ClaseVideoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clases con video dentro de cursos"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClaseVideoSerializer
    queryset = ClaseVideo.objects.select_related('curso').all()
    
    def get_serializer_context(self):
        """Asegurar que el serializer tenga el contexto del request"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        """Filtrar clases por curso"""
        qs = super().get_queryset()
        curso_id = self.request.query_params.get('curso_id', None)
        
        if curso_id:
            try:
                curso_id = int(curso_id)
                qs = qs.filter(curso_id=curso_id)
            except (ValueError, TypeError):
                pass
        
        # Solo permitir ver clases de cursos visibles o del usuario actual
        if self.action in ['list', 'retrieve']:
            qs = qs.filter(
                Q(curso__visible=True) | Q(curso__autor=self.request.user)
            )
        
        return qs.order_by('curso', 'orden', 'numero_clase')
    
    def list(self, request, *args, **kwargs):
        """Listar clases - siempre devolver array"""
        try:
            response = super().list(request, *args, **kwargs)
            # Asegurar que siempre devolvemos un array
            if isinstance(response.data, dict) and 'results' in response.data:
                return Response(response.data['results'])
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        """Crear clase con manejo de errores mejorado"""
        try:
            curso_id = request.data.get('curso')
            if not curso_id:
                return Response(
                    {'error': 'Debes especificar el curso'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                curso_id = int(curso_id)
                curso = Curso.objects.get(id=curso_id)
            except (ValueError, TypeError):
                return Response(
                    {'error': 'ID de curso inválido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Curso.DoesNotExist:
                return Response(
                    {'error': 'Curso no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Solo el autor puede agregar clases
            if curso.autor != request.user:
                return Response(
                    {'error': 'Solo el autor del curso puede agregar clases'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Validar que el curso sea de tipo video
            if curso.tipo != Curso.TipoCurso.CURSO_VIDEO:
                return Response(
                    {'error': 'Solo se pueden agregar clases a cursos de tipo video'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar que el video esté presente
            if 'video' not in request.FILES:
                return Response(
                    {'error': 'Debes subir un archivo de video'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(
                {'error': str(e.detail) if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al crear la clase: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def perform_update(self, serializer):
        """Validar permisos al actualizar"""
        instance = serializer.instance
        if instance.curso.autor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Solo el autor del curso puede modificar clases')
        serializer.save()
    
    def perform_destroy(self, instance):
        """Validar permisos al eliminar"""
        if instance.curso.autor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Solo el autor del curso puede eliminar clases')
        instance.delete()
