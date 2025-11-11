"""Serializadores para cursos OTEC."""

from rest_framework import serializers
from .models import Curso


class CursoSerializer(serializers.ModelSerializer):
    """Serializer completo para cursos"""
    vigente = serializers.SerializerMethodField()
    precio_formateado = serializers.SerializerMethodField()
    autor_nombre = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    modalidad_display = serializers.CharField(source='get_modalidad_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)

    class Meta:
        model = Curso
        fields = [
            # IDs y metadata
            'id',
            'autor',
            'autor_nombre',
            
            # Básicos
            'titulo',
            'descripcion',
            'tipo',
            'tipo_display',
            'categoria',
            'etiquetas',
            
            # Detalles
            'modalidad',
            'modalidad_display',
            'nivel',
            'nivel_display',
            'duracion',
            
            # Precio
            'precio',
            'precio_formateado',
            'es_gratuito',
            
            # URLs y contacto
            'url',
            'email_contacto',
            'telefono_contacto',
            'imagen_url',
            
            # Fechas
            'fecha_inicio',
            'fecha_fin',
            
            # Estado
            'visible',
            'vigente',
            'visualizaciones',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 
            'autor', 
            'vigente', 
            'precio_formateado',
            'tipo_display',
            'modalidad_display',
            'nivel_display',
            'visualizaciones', 
            'created_at', 
            'updated_at'
        ]

    def get_autor_nombre(self, obj: Curso) -> str:
        """Obtener nombre del autor de forma segura"""
        try:
            return obj.autor.name if obj.autor else 'Anonimo'
        except:
            return 'Anonimo'
    
    def get_vigente(self, obj: Curso) -> bool:
        return obj.esta_vigente()
    
    def get_precio_formateado(self, obj: Curso) -> str:
        return obj.precio_formateado()
    
    def validate(self, data):
        """Validaciones personalizadas"""
        tipo = data.get('tipo', self.instance.tipo if self.instance else None)
        
        # Si es anuncio personal, debe tener al menos un medio de contacto
        if tipo == Curso.TipoCurso.ANUNCIO_PERSONAL:
            email = data.get('email_contacto', self.instance.email_contacto if self.instance else '')
            telefono = data.get('telefono_contacto', self.instance.telefono_contacto if self.instance else '')
            url = data.get('url', self.instance.url if self.instance else '')
            
            if not any([email, telefono, url]):
                raise serializers.ValidationError({
                    'email_contacto': 'Para anuncios personales, debes proporcionar al menos un medio de contacto (email, telefono o URL)'
                })
        
        # Si es enlace externo, debe tener URL
        if tipo == Curso.TipoCurso.ENLACE_EXTERNO:
            url = data.get('url', self.instance.url if self.instance else '')
            if not url:
                raise serializers.ValidationError({
                    'url': 'Para cursos externos, debes proporcionar la URL del curso'
                })
        
        # Validar fechas
        fecha_inicio = data.get('fecha_inicio', self.instance.fecha_inicio if self.instance else None)
        fecha_fin = data.get('fecha_fin', self.instance.fecha_fin if self.instance else None)
        
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio'
            })
        
        return data


class CursoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de cursos"""
    precio_formateado = serializers.SerializerMethodField()
    autor_nombre = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    modalidad_display = serializers.CharField(source='get_modalidad_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    vigente = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = [
            'id',
            'titulo',
            'descripcion',
            'tipo',
            'tipo_display',
            'categoria',
            'modalidad',
            'modalidad_display',
            'nivel',
            'nivel_display',
            'precio_formateado',
            'imagen_url',
            'fecha_inicio',
            'autor_nombre',
            'vigente',
            'visualizaciones',
        ]
    
    def get_autor_nombre(self, obj: Curso) -> str:
        """Obtener nombre del autor de forma segura"""
        try:
            return obj.autor.name if obj.autor else 'Anonimo'
        except:
            return 'Anonimo'

    def get_precio_formateado(self, obj: Curso) -> str:
        return obj.precio_formateado()
    
    def get_vigente(self, obj: Curso) -> bool:
        return obj.esta_vigente()
