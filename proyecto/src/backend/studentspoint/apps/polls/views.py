"""Vistas mejoradas para el sistema completo de encuestas."""

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from studentspoint.apps.accounts.permissions import IsModeratorOrDirector
from .models import Poll, PollAnalytics
from .serializers import (
    PollListSerializer,
    PollDetailSerializer,
    PollCreateSerializer,
    PollUpdateSerializer,
    PollVoteSerializer,
    PollExportSerializer,
    PollAnalyticsSerializer,
    SimpleStatusSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Lista encuestas disponibles",
        description="Obtiene todas las encuestas que el usuario puede ver, filtradas por permisos."
    ),
    create=extend_schema(
        summary="Crea nueva encuesta",
        description="Permite a moderadores y directores crear encuestas con opciones múltiples."
    )
)
class PollListCreateView(generics.ListCreateAPIView):
    """Lista y crea encuestas con filtros avanzados."""
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titulo", "descripcion"]
    ordering_fields = ["created_at", "inicia_at", "cierra_at", "total_votos"]
    ordering = ["-created_at"]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PollCreateSerializer
        return PollListSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsModeratorOrDirector()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Poll.objects.select_related("creador").prefetch_related("sedes")
        
        # Filtrar por estado
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        else:
            # Por defecto, mostrar solo encuestas activas y cerradas
            queryset = queryset.filter(estado__in=[Poll.Estado.ACTIVA, Poll.Estado.CERRADA])
        
        # Filtrar por sede del usuario
        if user.campus:
            queryset = queryset.filter(
                Q(sedes__isnull=True) | Q(sedes=user.campus)
            ).distinct()
        
        # Filtrar por carrera del usuario
        if user.career:
            queryset = queryset.filter(
                Q(carreras=[]) | Q(carreras__contains=[user.career])
            )
        
        # Filtrar por fechas
        fecha_desde = self.request.query_params.get("fecha_desde")
        if fecha_desde:
            queryset = queryset.filter(inicia_at__gte=fecha_desde)
        
        fecha_hasta = self.request.query_params.get("fecha_hasta")
        if fecha_hasta:
            queryset = queryset.filter(inicia_at__lte=fecha_hasta)
        
        # Filtrar por creador
        creador = self.request.query_params.get("creador")
        if creador:
            queryset = queryset.filter(creador_id=creador)
        
        # Anotar con total de votos
        queryset = queryset.annotate(
            total_votos=Count("votos__usuario", distinct=True)
        )
        
        return queryset


@extend_schema_view(
    retrieve=extend_schema(
        summary="Detalle de encuesta",
        description="Obtiene detalles completos de una encuesta con resultados si el usuario tiene permisos."
    ),
    update=extend_schema(
        summary="Actualiza encuesta",
        description="Permite actualizar ciertos campos de una encuesta (solo al creador o moderadores)."
    ),
    destroy=extend_schema(
        summary="Elimina encuesta",
        description="Elimina una encuesta (solo al creador o administradores)."
    )
)
class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de encuestas."""
    
    queryset = Poll.objects.select_related("creador").prefetch_related(
        "sedes", 
        Prefetch("opciones", queryset=Poll.objects.none()),
        "analytics"
    )
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PollUpdateSerializer
        return PollDetailSerializer
    
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated(), IsModeratorOrDirector()]
        return [permissions.IsAuthenticated()]
    
    def perform_update(self, serializer):
        poll = self.get_object()
        # Solo el creador o moderadores pueden actualizar
        user = self.request.user
        if poll.creador != user and user.role not in ["moderator", "director_carrera", "admin_global"]:
            raise permissions.PermissionDenied("Solo el creador o moderadores pueden actualizar esta encuesta")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        # Solo administradores pueden eliminar
        user = self.request.user
        if user.role != "admin_global" and instance.creador != user:
            raise permissions.PermissionDenied("Solo administradores o el creador pueden eliminar esta encuesta")
        
        instance.delete()


@extend_schema(
    summary="Votar en encuesta",
    description="Registra el voto del usuario autenticado en una encuesta específica.",
    request=PollVoteSerializer,
    responses={200: SimpleStatusSerializer}
)
class PollVoteView(APIView):
    """Registra votos del usuario autenticado para una encuesta."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        
        serializer = PollVoteSerializer(
            data=request.data, 
            context={"poll": poll, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "status": "success",
            "message": "Voto registrado exitosamente"
        })


@extend_schema(
    summary="Exportar resultados de encuesta",
    description="Exporta los resultados de una encuesta en formato CSV o JSON.",
    request=PollExportSerializer,
    responses={200: "Archivo de exportación"}
)
class PollExportView(APIView):
    """Exporta resultados de encuesta en diferentes formatos."""
    
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrDirector]
    
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        
        # Verificar permisos para ver resultados
        if not poll.puede_ver_resultados(request.user):
            return Response(
                {"error": "No tienes permisos para ver los resultados de esta encuesta"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PollExportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data["formato"] == "csv":
            # Exportar CSV
            csv_content = serializer.export_csv(poll)
            response = HttpResponse(csv_content, content_type="text/csv")
            response["Content-Disposition"] = f'attachment; filename="encuesta_{poll.id}_{poll.titulo[:30]}.csv"'
            return response
        
        else:
            # Exportar JSON
            poll_serializer = PollDetailSerializer(poll, context={"request": request})
            response = HttpResponse(
                poll_serializer.data, 
                content_type="application/json"
            )
            response["Content-Disposition"] = f'attachment; filename="encuesta_{poll.id}_{poll.titulo[:30]}.json"'
            return response


@extend_schema(
    summary="Analytics de encuesta",
    description="Obtiene estadísticas detalladas y análisis de una encuesta.",
    responses={200: PollAnalyticsSerializer}
)
class PollAnalyticsView(APIView):
    """Obtiene analytics detallados de una encuesta."""
    
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrDirector]
    
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        
        # Verificar permisos
        user = request.user
        if poll.creador != user and user.role not in ["moderator", "director_carrera", "admin_global"]:
            return Response(
                {"error": "No tienes permisos para ver las estadísticas de esta encuesta"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener o crear analytics
        analytics, created = PollAnalytics.objects.get_or_create(poll=poll)
        if created or analytics.ultima_actualizacion < timezone.now() - timezone.timedelta(minutes=5):
            analytics.actualizar_estadisticas()
        
        serializer = PollAnalyticsSerializer(analytics)
        return Response(serializer.data)


@extend_schema(
    summary="Cerrar encuesta",
    description="Cierra manualmente una encuesta activa.",
    responses={200: SimpleStatusSerializer}
)
class PollCloseView(APIView):
    """Cierra manualmente una encuesta."""
    
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrDirector]
    
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        
        # Verificar permisos
        user = request.user
        if poll.creador != user and user.role not in ["moderator", "director_carrera", "admin_global"]:
            return Response(
                {"error": "No tienes permisos para cerrar esta encuesta"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if poll.estado != Poll.Estado.ACTIVA:
            return Response(
                {"error": "Solo se pueden cerrar encuestas activas"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        poll.estado = Poll.Estado.CERRADA
        poll.cierra_at = timezone.now()
        poll.save()
        
        return Response({
            "status": "success",
            "message": "Encuesta cerrada exitosamente"
        })


@extend_schema(
    summary="Mis encuestas creadas",
    description="Lista las encuestas creadas por el usuario autenticado.",
    responses={200: PollListSerializer(many=True)}
)
class MyPollsView(generics.ListAPIView):
    """Lista encuestas creadas por el usuario autenticado."""
    
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrDirector]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]
    
    def get_queryset(self):
        return Poll.objects.filter(creador=self.request.user).annotate(
            total_votos=Count("votos__usuario", distinct=True)
        ).select_related("creador").prefetch_related("sedes")


@extend_schema(
    summary="Dashboard de encuestas",
    description="Obtiene estadísticas generales del sistema de encuestas.",
    responses={200: "Estadísticas del dashboard"}
)
class PollsDashboardView(APIView):
    """Dashboard con estadísticas generales del sistema de encuestas."""
    
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrDirector]
    
    def get(self, request):
        user = request.user
        
        # Estadísticas básicas
        total_encuestas = Poll.objects.count()
        encuestas_activas = Poll.objects.filter(estado=Poll.Estado.ACTIVA).count()
        encuestas_cerradas = Poll.objects.filter(estado=Poll.Estado.CERRADA).count()
        
        # Encuestas del usuario si es moderador/director
        mis_encuestas = Poll.objects.filter(creador=user).count()
        
        # Top encuestas por participación
        top_encuestas = Poll.objects.annotate(
            participantes=Count("votos__usuario", distinct=True)
        ).order_by("-participantes")[:5]
        
        top_data = []
        for poll in top_encuestas:
            top_data.append({
                "id": poll.id,
                "titulo": poll.titulo,
                "participantes": poll.participantes,
                "estado": poll.estado
            })
        
        # Actividad reciente
        actividad_reciente = Poll.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        
        return Response({
            "estadisticas": {
                "total_encuestas": total_encuestas,
                "encuestas_activas": encuestas_activas,
                "encuestas_cerradas": encuestas_cerradas,
                "mis_encuestas": mis_encuestas,
                "actividad_reciente": actividad_reciente
            },
            "top_encuestas": top_data,
            "usuario": {
                "puede_crear": user.role in ["moderator", "director_carrera", "admin_global"],
                "role": user.role
            }
        })