"""Views para el sistema de portafolio."""

import io
import os
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .pdf_generator import generate_portfolio_pdf

from django.contrib.auth import get_user_model
from .models import (
    Logro, Proyecto, ExperienciaLaboral, Habilidad,
    PortafolioConfig, PortafolioSugerencia, PortafolioAnalytics
)
from .serializers import (
    LogroSerializer, ProyectoSerializer, ExperienciaLaboralSerializer,
    HabilidadSerializer, PortafolioConfigSerializer, PortafolioSugerenciaSerializer,
    PortafolioAnalyticsSerializer, PortafolioCompletoSerializer
)

User = get_user_model()


class LogroViewSet(viewsets.ModelViewSet):
    """ViewSet para logros."""
    
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Logro.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet para proyectos."""
    
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ExperienciaLaboralViewSet(viewsets.ModelViewSet):
    """ViewSet para experiencias laborales."""
    
    queryset = ExperienciaLaboral.objects.all()
    serializer_class = ExperienciaLaboralSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExperienciaLaboral.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class HabilidadViewSet(viewsets.ModelViewSet):
    """ViewSet para habilidades."""
    
    queryset = Habilidad.objects.all()
    serializer_class = HabilidadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Habilidad.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class PortafolioConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para configuración de portafolio."""
    
    queryset = PortafolioConfig.objects.all()
    serializer_class = PortafolioConfigSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PortafolioConfig.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    def get_object(self):
        """Obtiene o crea la configuración del usuario."""
        obj, created = PortafolioConfig.objects.get_or_create(
            usuario=self.request.user
        )
        return obj


class PortafolioSugerenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para sugerencias de portafolio."""
    
    queryset = PortafolioSugerencia.objects.all()
    serializer_class = PortafolioSugerenciaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PortafolioSugerencia.objects.filter(
            usuario=self.request.user,
            completada=False
        )
    
    @extend_schema(
        summary="Marcar sugerencia como completada",
        responses={200: {"description": "Sugerencia marcada como completada"}}
    )
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Marca una sugerencia como completada."""
        sugerencia = self.get_object()
        sugerencia.completada = True
        sugerencia.save()
        
        # Actualizar analytics
        try:
            analytics = request.user.portafolio_analytics
            analytics.actualizar_estadisticas()
        except PortafolioAnalytics.DoesNotExist:
            PortafolioAnalytics.objects.create(usuario=request.user)
        
        return Response({'message': 'Sugerencia completada'})


class PortafolioAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para analytics de portafolio."""
    
    queryset = PortafolioAnalytics.objects.all()
    serializer_class = PortafolioAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PortafolioAnalytics.objects.filter(usuario=self.request.user)
    
    def get_object(self):
        """Obtiene o crea los analytics del usuario."""
        obj, created = PortafolioAnalytics.objects.get_or_create(
            usuario=self.request.user
        )
        if created:
            obj.actualizar_estadisticas()
        return obj


class PortafolioCompletoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para obtener toda la información del portafolio."""
    
    queryset = User.objects.all()
    serializer_class = PortafolioCompletoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return [self.request.user]
    
    def get_object(self):
        return self.request.user
    
    @extend_schema(
        summary="Generar PDF del portafolio",
        responses={200: {"description": "PDF generado exitosamente"}}
    )
    @action(detail=False, methods=['get'])
    def generar_pdf(self, request):
        """Genera un PDF del portafolio del usuario (DESHABILITADO TEMPORALMENTE)."""
        return Response(
            {'error': 'Generación de PDF deshabilitada temporalmente. WeasyPrint requiere configuración adicional en Windows.'}, 
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    @extend_schema(
        summary="Generar sugerencias automáticas",
        responses={200: {"description": "Sugerencias generadas"}}
    )
    @action(detail=False, methods=['post'])
    def generar_sugerencias(self, request):
        """Genera sugerencias automáticas para mejorar el portafolio."""
        usuario = request.user
        
        # Limpiar sugerencias anteriores no completadas
        PortafolioSugerencia.objects.filter(
            usuario=usuario, 
            completada=False
        ).delete()
        
        sugerencias = []
        
        # Verificar completitud del perfil
        if not usuario.name or len(usuario.name.strip()) < 3:
            sugerencias.append({
                'tipo': 'completar_perfil',
                'titulo': 'Completar nombre completo',
                'descripcion': 'Agrega tu nombre completo para que tu portafolio se vea más profesional.',
                'prioridad': 'alta'
            })
        
        # Verificar configuración de portafolio
        try:
            config = usuario.portafolio_config
            if not config.titulo_profesional:
                sugerencias.append({
                    'tipo': 'completar_perfil',
                    'titulo': 'Agregar título profesional',
                    'descripcion': 'Define tu título profesional o área de especialización.',
                    'prioridad': 'alta'
                })
            
            if not config.resumen_profesional:
                sugerencias.append({
                    'tipo': 'mejorar_descripcion',
                    'titulo': 'Escribir resumen profesional',
                    'descripcion': 'Crea un resumen profesional que destaque tus fortalezas y objetivos.',
                    'prioridad': 'alta'
                })
        except PortafolioConfig.DoesNotExist:
            sugerencias.append({
                'tipo': 'completar_perfil',
                'titulo': 'Configurar portafolio',
                'descripcion': 'Completa la configuración básica de tu portafolio.',
                'prioridad': 'alta'
            })
        
        # Verificar logros
        logros_count = Logro.objects.filter(usuario=usuario, visible=True).count()
        if logros_count == 0:
            sugerencias.append({
                'tipo': 'agregar_logros',
                'titulo': 'Agregar logros y certificaciones',
                'descripcion': 'Incluye certificaciones, premios o logros académicos y profesionales.',
                'prioridad': 'media'
            })
        
        # Verificar proyectos
        proyectos_count = Proyecto.objects.filter(usuario=usuario, visible=True).count()
        if proyectos_count == 0:
            sugerencias.append({
                'tipo': 'agregar_proyectos',
                'titulo': 'Agregar proyectos',
                'descripcion': 'Muestra tus proyectos más importantes con descripción y tecnologías utilizadas.',
                'prioridad': 'alta'
            })
        elif proyectos_count < 3:
            sugerencias.append({
                'tipo': 'agregar_proyectos',
                'titulo': 'Agregar más proyectos',
                'descripcion': 'Incluye al menos 3 proyectos para mostrar tu experiencia.',
                'prioridad': 'media'
            })
        
        # Verificar experiencias
        experiencias_count = ExperienciaLaboral.objects.filter(usuario=usuario, visible=True).count()
        if experiencias_count == 0:
            sugerencias.append({
                'tipo': 'agregar_experiencia',
                'titulo': 'Agregar experiencia laboral',
                'descripcion': 'Incluye prácticas profesionales, trabajos o voluntariados.',
                'prioridad': 'media'
            })
        
        # Verificar habilidades
        habilidades_count = Habilidad.objects.filter(usuario=usuario, visible=True).count()
        if habilidades_count == 0:
            sugerencias.append({
                'tipo': 'mejorar_habilidades',
                'titulo': 'Agregar habilidades',
                'descripcion': 'Lista tus habilidades técnicas y blandas con niveles de competencia.',
                'prioridad': 'alta'
            })
        elif habilidades_count < 5:
            sugerencias.append({
                'tipo': 'mejorar_habilidades',
                'titulo': 'Completar habilidades',
                'descripcion': 'Agrega más habilidades para mostrar tu versatilidad.',
                'prioridad': 'media'
            })
        
        # Crear sugerencias
        for sugerencia_data in sugerencias:
            PortafolioSugerencia.objects.create(
                usuario=usuario,
                **sugerencia_data
            )
        
        return Response({
            'message': f'Se generaron {len(sugerencias)} sugerencias',
            'sugerencias_count': len(sugerencias)
        })
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def generate_pdf(self, request):
        """Generar PDF del portfolio del usuario autenticado."""
        try:
            usuario = request.user
            
            # Obtener datos del portfolio
            logros = Logro.objects.filter(usuario=usuario, visible=True)
            proyectos = Proyecto.objects.filter(usuario=usuario, visible=True)
            experiencias = ExperienciaLaboral.objects.filter(usuario=usuario, visible=True)
            habilidades = Habilidad.objects.filter(usuario=usuario, visible=True)
            
            # Preparar datos para el PDF
            portfolio_data = {
                'nombre': usuario.name,
                'email': usuario.email,
                'telefono': getattr(usuario, 'telefono', ''),
                'linkedin': getattr(usuario, 'linkedin', ''),
                'github': getattr(usuario, 'github', ''),
                'sitio_web': getattr(usuario, 'sitio_web', ''),
                'resumen': getattr(usuario, 'resumen_profesional', ''),
                'habilidades': [h.nombre for h in habilidades],
                'proyectos': [
                    {
                        'titulo': p.titulo,
                        'descripcion': p.descripcion,
                        'tecnologias': p.tecnologias.split(',') if p.tecnologias else [],
                        'enlace': p.enlace
                    } for p in proyectos
                ],
                'experiencia': [
                    {
                        'titulo': e.titulo,
                        'empresa': e.empresa,
                        'fecha_inicio': e.fecha_inicio.strftime('%Y-%m') if e.fecha_inicio else '',
                        'fecha_fin': e.fecha_fin.strftime('%Y-%m') if e.fecha_fin else 'Presente',
                        'descripcion': e.descripcion
                    } for e in experiencias
                ],
                'educacion': [
                    {
                        'titulo': 'Estudiante',
                        'institucion': 'StudentsPoint',
                        'fecha_inicio': '2024',
                        'fecha_fin': 'Presente',
                        'descripcion': 'Plataforma de aprendizaje y desarrollo profesional'
                    }
                ],
                'logros': [l.titulo for l in logros]
            }
            
            # Generar PDF
            pdf_buffer = generate_portfolio_pdf(portfolio_data)
            
            # Crear respuesta HTTP
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="portfolio_{usuario.name.replace(" ", "_")}.pdf"'
            
            return response
            
        except Exception as e:
            return Response({
                'error': f'Error generando PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
