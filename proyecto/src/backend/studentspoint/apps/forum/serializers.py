"""Serializadores para la app de foros."""

from rest_framework import serializers

from .models import Comentario, Foro, Post, PostReporte, OpcionEncuesta, VotoEncuesta
from .services import ForumPermissionService


class ForoSerializer(serializers.ModelSerializer):
    """Representa un foro temático."""
    
    puede_postear = serializers.SerializerMethodField()
    sede_nombre = serializers.CharField(source='sede.nombre', read_only=True)

    class Meta:
        model = Foro
        fields = ["id", "sede", "sede_nombre", "carrera", "titulo", "slug", "es_privado", "descripcion", "created_at", "puede_postear"]
        read_only_fields = ["created_at", "sede_nombre"]
    
    def get_puede_postear(self, obj):
        """Indica si el usuario actual puede postear en este foro.
        
        Args:
            obj: Instancia del modelo Foro
            
        Returns:
            bool: True si el usuario puede postear en este foro
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        return ForumPermissionService.puede_postear_en_foro(request.user, obj)


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
    - enlace: Post con URL asociada
    - archivo: Post con archivo adjunto
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
            "enlace_url",
            "imagen",
            "imagen_url",
            "imagen_aprobada",
            "archivo",
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

    def validate(self, attrs):
        """Valida consistencia entre tipo de post y campos adjuntos.
        Args:
            attrs (dict): Datos de entrada.
        Returns:
            dict: Datos validados.
        """
        tipo = attrs.get("tipo")
        # Aceptar alias 'texto' como 'comentario' para compatibilidad
        if tipo == 'texto':
            attrs["tipo"] = Post.TipoPost.COMENTARIO
            tipo = attrs["tipo"]
        tiene_imagen = attrs.get("imagen") is not None
        tiene_archivo = attrs.get("archivo") is not None
        enlace = attrs.get("enlace_url")

        if tipo == Post.TipoPost.IMAGEN and not tiene_imagen:
            raise serializers.ValidationError({"imagen": "Se requiere imagen cuando tipo es 'imagen'."})
        if tipo == Post.TipoPost.ARCHIVO and not tiene_archivo:
            raise serializers.ValidationError({"archivo": "Se requiere archivo cuando tipo es 'archivo'."})
        if tipo == Post.TipoPost.ENLACE and not enlace:
            raise serializers.ValidationError({"enlace_url": "Se requiere enlace_url cuando tipo es 'enlace'."})

        # Evitar adjuntar múltiples tipos simultáneamente
        adjuntos = sum([1 if tiene_imagen else 0, 1 if tiene_archivo else 0, 1 if bool(enlace) else 0])
        if adjuntos > 1:
            raise serializers.ValidationError("Solo se permite un tipo de adjunto por publicación (imagen, archivo o enlace).")

        return attrs

    def create(self, validated_data):
        """Crea post y, si corresponde, opciones de encuesta.
        Acepta 'opciones_encuesta' en request.data cuando tipo=encuesta.
        """
        request = self.context.get('request')
        opciones_payload = []
        if request:
            opciones_payload = request.data.get("opciones_encuesta") or []

        post = super().create(validated_data)

        # Crear opciones de encuesta si corresponde
        if post.tipo == Post.TipoPost.ENCUESTA and opciones_payload:
            if isinstance(opciones_payload, (list, tuple)):
                for idx, opcion in enumerate(opciones_payload):
                    texto = opcion.get("texto") if isinstance(opcion, dict) else str(opcion)
                    if texto:
                        OpcionEncuesta.objects.create(post=post, texto=texto, orden=idx)

        return post
    
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
    
    usuario_name = serializers.SerializerMethodField()
    usuario_email = serializers.SerializerMethodField()
    post_titulo = serializers.SerializerMethodField()
    post_cuerpo = serializers.SerializerMethodField()
    post_usuario = serializers.SerializerMethodField()
    post_foro = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    
    class Meta:
        model = PostReporte
        fields = [
            "id", "post", "post_titulo", "post_cuerpo", "post_usuario", "post_foro",
            "usuario", "usuario_name", "usuario_email", "tipo", "tipo_display",
            "descripcion", "estado", "estado_display", "created_at"
        ]
        read_only_fields = ["usuario", "created_at"]
    
    def get_usuario_name(self, obj):
        """Obtener nombre del usuario de forma segura"""
        try:
            return obj.usuario.name if obj.usuario else None
        except:
            return None
    
    def get_usuario_email(self, obj):
        """Obtener email del usuario de forma segura"""
        try:
            return obj.usuario.email if obj.usuario else None
        except:
            return None
    
    def get_post_titulo(self, obj):
        """Obtener título del post de forma segura"""
        try:
            return obj.post.titulo if obj.post else None
        except:
            return None
    
    def get_post_cuerpo(self, obj):
        """Obtener cuerpo del post de forma segura"""
        try:
            return obj.post.cuerpo if obj.post else None
        except:
            return None
    
    def get_post_usuario(self, obj):
        """Obtener nombre del autor del post de forma segura"""
        try:
            return obj.post.usuario.name if obj.post and obj.post.usuario else None
        except:
            return None
    
    def get_post_foro(self, obj):
        """Obtener título del foro de forma segura"""
        try:
            return obj.post.foro.titulo if obj.post and obj.post.foro else None
        except:
            return None


class ModeracionSerializer(serializers.Serializer):
    """Serializer para acciones de moderación."""
    
    accion = serializers.ChoiceField(choices=["aprobar", "rechazar", "ocultar"])
    razon = serializers.CharField(required=False, allow_blank=True)


class ForumDetailSerializer(serializers.Serializer):
    """Mensaje simple para respuestas sin contenido estructurado."""

    detail = serializers.CharField()
