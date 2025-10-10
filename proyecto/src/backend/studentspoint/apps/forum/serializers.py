"""Serializadores para la app de foros."""

from rest_framework import serializers

from .models import Comentario, Foro, Post, PostReporte, OpcionEncuesta, VotoEncuesta


class ForoSerializer(serializers.ModelSerializer):
    """Representa un foro temático."""
    
    puede_postear = serializers.SerializerMethodField()

    class Meta:
        model = Foro
        fields = ["id", "sede", "carrera", "titulo", "slug", "es_privado", "descripcion", "created_at", "puede_postear"]
        read_only_fields = ["created_at"]
    
    def get_puede_postear(self, obj):
        """Indica si el usuario actual puede postear en este foro."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.puede_postear(request.user)
        return False


class OpcionEncuestaSerializer(serializers.ModelSerializer):
    """Serializer para opciones de encuesta."""
    
    class Meta:
        model = OpcionEncuesta
        fields = ["id", "texto", "votos", "orden"]
        read_only_fields = ["votos"]


class PostSerializer(serializers.ModelSerializer):
    """Serializa posts para listado y creación.
    
    Soporta diferentes tipos de publicaciones:
    - comentario: Post estándar con texto
    - encuesta: Post con opciones para votar
    - imagen: Post con imagen adjunta (requiere aprobación)
    - otro: Otros tipos
    
    IMPORTANTE: Para subir imágenes, usar multipart/form-data
    """
    
    usuario_name = serializers.CharField(source="usuario.name", read_only=True)
    usuario_career = serializers.CharField(source="usuario.career", read_only=True)
    usuario_campus = serializers.CharField(source="usuario.campus.nombre", read_only=True)
    total_comentarios = serializers.SerializerMethodField()
    total_reportes = serializers.IntegerField(read_only=True)
    opciones_encuesta = OpcionEncuestaSerializer(many=True, read_only=True)
    foro_info = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "foro",
            "foro_info",
            "usuario",
            "usuario_name",
            "usuario_career",
            "usuario_campus",
            "anonimo",
            "titulo",
            "cuerpo",
            "tipo",
            "imagen",
            "imagen_url",
            "imagen_aprobada",
            "score",
            "estado",
            "created_at",
            "updated_at",
            "total_comentarios",
            "total_reportes",
            "opciones_encuesta",
            "moderado_por",
            "razon_moderacion",
            "moderado_at",
        ]
        read_only_fields = [
            "usuario", "usuario_name", "usuario_career", "usuario_campus",
            "score", "estado", "created_at", "updated_at", "imagen_aprobada",
            "total_comentarios", "total_reportes", "opciones_encuesta",
            "moderado_por", "razon_moderacion", "moderado_at", "foro_info", "imagen_url"
        ]
    
    def get_total_comentarios(self, obj):
        return obj.comentarios.count()
    
    def get_foro_info(self, obj):
        """Información básica del foro."""
        return {
            "id": obj.foro.id,
            "carrera": obj.foro.carrera,
            "titulo": obj.foro.titulo
        }
    
    def get_imagen_url(self, obj):
        """Retorna la URL completa de la imagen si existe."""
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializador de comentarios."""

    usuario_name = serializers.CharField(source="usuario.name", read_only=True)

    class Meta:
        model = Comentario
        fields = [
            "id",
            "post",
            "usuario",
            "usuario_name",
            "anonimo",
            "cuerpo",
            "score",
            "created_at",
        ]
        read_only_fields = ["post", "usuario", "score", "created_at", "usuario_name"]


class VoteSerializer(serializers.Serializer):
    """Payload esperado para registrar un voto."""

    valor = serializers.IntegerField()


class ScoreSerializer(serializers.Serializer):
    """Respuesta que devuelve el score actualizado."""

    score = serializers.IntegerField()


class PostReporteSerializer(serializers.ModelSerializer):
    """Serializer para reportes de posts."""
    
    usuario_name = serializers.CharField(source="usuario.name", read_only=True)
    
    class Meta:
        model = PostReporte
        fields = [
            "id", "post", "usuario", "usuario_name", "tipo", 
            "descripcion", "created_at"
        ]
        read_only_fields = ["usuario", "created_at"]


class ModeracionSerializer(serializers.Serializer):
    """Serializer para acciones de moderación."""
    
    accion = serializers.ChoiceField(choices=["aprobar", "rechazar", "ocultar"])
    razon = serializers.CharField(required=False, allow_blank=True)


class ForumDetailSerializer(serializers.Serializer):
    """Mensaje simple para respuestas sin contenido estructurado."""

    detail = serializers.CharField()
