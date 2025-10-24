"""
Vistas para el sistema de monitoreo de infraestructura.
"""

from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from studentspoint.apps.accounts.permissions import IsModeratorOrDirector
from .models import (
    InfraestructuraItem, ReporteInfraestructura, MetricasInfraestructura,
    MantenimientoProgramado, DashboardConfig, AlertaInfraestructura
)
from .serializers import (
    InfraestructuraItemSerializer, ReporteInfraestructuraSerializer,
    MetricasInfraestructuraSerializer, MantenimientoProgramadoSerializer,
    DashboardConfigSerializer, AlertaInfraestructuraSerializer,
    DashboardStatsSerializer
)


class InfraestructuraItemViewSet(viewsets.ModelViewSet):
    """ViewSet para elementos de infraestructura."""
    
    queryset = InfraestructuraItem.objects.all()
    serializer_class = InfraestructuraItemSerializer
    permission_classes = [IsModeratorOrDirector]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campus = self.request.query_params.get('campus')
        tipo = self.request.query_params.get('tipo')
        estado = self.request.query_params.get('estado')
        
        if campus:
            queryset = queryset.filter(campus_id=campus)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if estado:
            queryset = queryset.filter(estado_actual=estado)
        
        return queryset


class ReporteInfraestructuraViewSet(viewsets.ModelViewSet):
    """ViewSet para reportes de infraestructura."""
    
    queryset = ReporteInfraestructura.objects.all()
    serializer_class = ReporteInfraestructuraSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Los usuarios normales solo ven sus propios reportes
        if not self.request.user.role in ['moderator', 'director_carrera', 'admin_global']:
            queryset = queryset.filter(reportado_por=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(reportado_por=self.request.user)


class DashboardStatsViewSet(viewsets.ViewSet):
    """ViewSet para estadísticas del dashboard."""
    
    permission_classes = [IsModeratorOrDirector]
    
    @extend_schema(responses=DashboardStatsSerializer)
    def list(self, request):
        """Obtiene estadísticas generales del dashboard."""
        
        # Estadísticas básicas
        total_items = InfraestructuraItem.objects.count()
        items_operativos = InfraestructuraItem.objects.filter(estado_actual='operativo').count()
        total_reportes = ReporteInfraestructura.objects.count()
        reportes_abiertos = ReporteInfraestructura.objects.filter(
            estado__in=['abierto', 'en_proceso']
        ).count()
        
        stats = {
            'total_items': total_items,
            'items_operativos': items_operativos,
            'items_mantenimiento': 0,
            'items_fuera_servicio': 0,
            'total_reportes': total_reportes,
            'reportes_abiertos': reportes_abiertos,
            'reportes_resueltos_hoy': 0,
            'total_alertas': 0,
            'alertas_activas': 0,
            'alertas_criticas': 0,
            'mantenimientos_pendientes': 0,
            'mantenimientos_hoy': 0,
            'ocupacion_promedio': 0.0,
            'satisfaccion_promedio': 0.0,
            'items_mas_usados': [],
            'items_problemas': [],
            'tendencias_ocupacion': []
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)