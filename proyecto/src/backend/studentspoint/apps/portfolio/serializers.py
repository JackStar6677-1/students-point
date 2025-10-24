"""Serializers para el sistema de portafolio."""

from rest_framework import serializers
from .models import (
    Logro, Proyecto, ExperienciaLaboral, Habilidad,
    PortafolioConfig, PortafolioSugerencia, PortafolioAnalytics
)


class LogroSerializer(serializers.ModelSerializer):
    """Serializer para logros."""
    
    class Meta:
        model = Logro
        fields = [
            'id', 'titulo', 'descripcion', 'tipo', 'fecha_obtencion',
            'institucion', 'certificado_url', 'visible', 'created_at'
        ]
        read_only_fields = ['created_at']


class ProyectoSerializer(serializers.ModelSerializer):
    """Serializer para proyectos."""
    
    class Meta:
        model = Proyecto
        fields = [
            'id', 'titulo', 'descripcion', 'tecnologias', 'estado',
            'fecha_inicio', 'fecha_fin', 'url_repositorio', 'url_demo',
            'imagenes', 'visible', 'created_at'
        ]
        read_only_fields = ['created_at']


class ExperienciaLaboralSerializer(serializers.ModelSerializer):
    """Serializer para experiencias laborales."""
    
    class Meta:
        model = ExperienciaLaboral
        fields = [
            'id', 'empresa', 'cargo', 'descripcion', 'tipo_contrato',
            'fecha_inicio', 'fecha_fin', 'actual', 'ubicacion',
            'visible', 'created_at'
        ]
        read_only_fields = ['created_at']


class HabilidadSerializer(serializers.ModelSerializer):
    """Serializer para habilidades."""
    
    class Meta:
        model = Habilidad
        fields = [
            'id', 'nombre', 'categoria', 'nivel', 'descripcion',
            'visible', 'created_at'
        ]
        read_only_fields = ['created_at']


class PortafolioConfigSerializer(serializers.ModelSerializer):
    """Serializer para configuración de portafolio."""
    
    class Meta:
        model = PortafolioConfig
        fields = [
            'titulo_profesional', 'resumen_profesional', 'telefono',
            'linkedin_url', 'github_url', 'portfolio_url',
            'mostrar_contacto', 'mostrar_redes_sociales', 'mostrar_logros',
            'mostrar_proyectos', 'mostrar_experiencia', 'mostrar_habilidades',
            'tema_color', 'incluir_foto', 'foto_url',
            'ultima_generacion', 'version_pdf'
        ]
        read_only_fields = ['ultima_generacion', 'version_pdf']


class PortafolioSugerenciaSerializer(serializers.ModelSerializer):
    """Serializer para sugerencias de portafolio."""
    
    class Meta:
        model = PortafolioSugerencia
        fields = [
            'id', 'tipo', 'titulo', 'descripcion', 'prioridad',
            'completada', 'created_at'
        ]
        read_only_fields = ['created_at']


class PortafolioAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer para analytics de portafolio."""
    
    class Meta:
        model = PortafolioAnalytics
        fields = [
            'completitud_perfil', 'total_logros', 'total_proyectos',
            'total_experiencias', 'total_habilidades',
            'visualizaciones_pdf', 'descargas_pdf', 'ultima_visualizacion',
            'ultima_actualizacion'
        ]


class PortafolioCompletoSerializer(serializers.Serializer):
    """Serializer que combina toda la información del portafolio."""
    
    # Información del usuario
    usuario_nombre = serializers.CharField(source='name')
    usuario_email = serializers.CharField(source='email')
    usuario_campus = serializers.CharField(source='campus.nombre')
    usuario_carrera = serializers.CharField(source='career')
    
    # Configuración
    config = PortafolioConfigSerializer(source='portafolio_config', read_only=True)
    
    # Contenido
    logros = LogroSerializer(many=True, read_only=True)
    proyectos = ProyectoSerializer(many=True, read_only=True)
    experiencias = ExperienciaLaboralSerializer(many=True, read_only=True)
    habilidades = HabilidadSerializer(many=True, read_only=True)
    
    # Analytics
    analytics = PortafolioAnalyticsSerializer(source='portafolio_analytics', read_only=True)
    
    # Sugerencias
    sugerencias = PortafolioSugerenciaSerializer(many=True, read_only=True)
