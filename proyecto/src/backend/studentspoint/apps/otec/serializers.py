"""Serializadores para cursos OTEC."""

from rest_framework import serializers
from .models import Curso, ClaseVideo


class ClaseVideoSerializer(serializers.ModelSerializer):
    """Serializer para clases con video"""
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ClaseVideo
        fields = [
            'id',
            'curso',
            'numero_clase',
            'titulo',
            'descripcion',
            'video',
            'video_url',
            'duracion_segundos',
            'orden',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_video_url(self, obj):
        """Obtener URL absoluta del video"""
        if obj.video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video.url)
            return obj.video.url
        return None
    
    def validate(self, data):
        """Validar que no haya duplicados de numero_clase en el mismo curso"""
        numero_clase = data.get('numero_clase')
        curso = data.get('curso')
        
        if numero_clase and curso:
            # Si estamos actualizando, excluir la instancia actual
            queryset = ClaseVideo.objects.filter(curso=curso, numero_clase=numero_clase)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'numero_clase': f'Ya existe una clase con el número {numero_clase} en este curso'
                })
        
        return data


class CursoSerializer(serializers.ModelSerializer):
    """Serializer completo para cursos"""
    vigente = serializers.SerializerMethodField()
    precio_formateado = serializers.SerializerMethodField()
    autor_nombre = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    modalidad_display = serializers.CharField(source='get_modalidad_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    clases_video = serializers.SerializerMethodField()

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
            
            # Estado
            'visible',
            'vigente',
            'visualizaciones',
            'created_at',
            'updated_at',
            
            # Clases de video (solo para tipo video)
            'clases_video',
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
    
    def get_clases_video(self, obj: Curso):
        """Obtener clases de video si el curso es de tipo video"""
        if obj.tipo == Curso.TipoCurso.CURSO_VIDEO:
            clases = obj.clases_video.all()
            return ClaseVideoSerializer(clases, many=True, context=self.context).data
        return []
    
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
        
        # Si es curso con videos, debe ser gratuito
        if tipo == Curso.TipoCurso.CURSO_VIDEO:
            es_gratuito = data.get('es_gratuito', self.instance.es_gratuito if self.instance else False)
            precio = data.get('precio', self.instance.precio if self.instance else None)
            if not es_gratuito and precio:
                raise serializers.ValidationError({
                    'es_gratuito': 'Los cursos con videos deben ser gratuitos por ahora'
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
