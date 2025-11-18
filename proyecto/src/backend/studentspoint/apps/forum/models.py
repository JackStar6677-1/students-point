"""Modelos básicos para el foro de la aplicación."""

from django.conf import settings
from django.db import models

from .utils import censurar_texto
from .services import ForumPermissionService, PostValidationService


class Foro(models.Model):
    """Espacio de discusión filtrado por sede y carrera.
    
    Cada carrera tiene su propio foro donde los estudiantes pueden crear publicaciones.
    Los foros pueden ser públicos (todos pueden ver) o privados (solo estudiantes de la carrera).
    """

    sede = models.ForeignKey("campuses.Sede", on_delete=models.CASCADE, related_name="foros")
    carrera = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    es_privado = models.BooleanField(
        default=False, 
        help_text="Si es privado, solo estudiantes de la carrera pueden ver el foro"
    )
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['carrera', 'titulo']  # Evitar UnorderedObjectListWarning

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo
    
    def puede_postear(self, usuario):
        """Verifica si un usuario puede crear posts en este foro.
        
        Args:
            usuario: Instancia de usuario de Django
            
        Returns:
            bool: True si el usuario puede postear en este foro
        """
        return ForumPermissionService.puede_postear_en_foro(usuario, self)
    
    def puede_ver(self, usuario):
        """Verifica si un usuario puede ver este foro.
        
        Args:
            usuario: Instancia de usuario de Django (puede ser None para anónimos)
            
        Returns:
            bool: True si el usuario puede ver el foro
        """
        return ForumPermissionService.puede_ver_foro(usuario, self)


class Post(models.Model):
    """Publicación realizada dentro de un :class:`Foro`.
    
    Tipos de publicaciones:
    - Comentario: Publicación estándar con texto
    - Encuesta: Publicación con opciones para votar
    - Imagen: Publicación con imagen (requiere revisión manual)
    - Otro: Otros tipos de contenido
    """

    class Estado(models.TextChoices):
        PUBLICADO = "publicado", "Publicado"
        REVISION = "revision", "En revisión"
        OCULTO = "oculto", "Oculto"
        RECHAZADO = "rechazado", "Rechazado"
    
    class TipoPost(models.TextChoices):
        COMENTARIO = "comentario", "Comentario"
        ENCUESTA = "encuesta", "Encuesta"
        IMAGEN = "imagen", "Imagen"
        ENLACE = "enlace", "Enlace"
        ARCHIVO = "archivo", "Archivo"
        OTRO = "otro", "Otro"

    foro = models.ForeignKey(Foro, on_delete=models.CASCADE, related_name="posts")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    anonimo = models.BooleanField(default=False)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    tipo = models.CharField(
        max_length=20, 
        choices=TipoPost.choices, 
        default=TipoPost.COMENTARIO,
        help_text="Tipo de publicación"
    )
    # Enlace asociado al post (solo para tipo ENLACE)
    enlace_url = models.URLField(null=True, blank=True, help_text="URL asociada al post cuando es de tipo enlace")
    imagen = models.ImageField(
        upload_to='forum/images/', 
        null=True, 
        blank=True,
        help_text="Imagen adjunta (requiere aprobación de administrador)"
    )
    imagen_aprobada = models.BooleanField(
        default=True,  # Auto-aprobar imágenes por defecto
        help_text="True si la imagen fue aprobada por un administrador"
    )
    # Archivo adjunto (solo para tipo ARCHIVO)
    archivo = models.FileField(
        upload_to='forum/files/',
        null=True,
        blank=True,
        help_text="Archivo adjunto para publicaciones de tipo archivo"
    )
    score = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PUBLICADO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos de moderación
    moderado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="posts_moderados"
    )
    razon_moderacion = models.TextField(blank=True)
    moderado_at = models.DateTimeField(null=True, blank=True)
    
    # Campos de reportes
    total_reportes = models.PositiveIntegerField(default=0)
    ultimo_reporte_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.titulo
    
    def save(self, *args, **kwargs):
        """Sobrescribe save para aplicar censura automática de texto."""
        # Aplicar censura al título y cuerpo
        self.titulo = censurar_texto(self.titulo)
        self.cuerpo = censurar_texto(self.cuerpo)
        
        # Auto-aprobar imágenes (no requiere revisión manual)
        if self.imagen and not self.pk:  # Solo en creación
            self.imagen_aprobada = True
        
        super().save(*args, **kwargs)
    
    def verificar_contenido(self):
        """Verifica el contenido del post y determina el estado apropiado.
        
        Returns:
            str: Estado del post según su contenido
        """
        return PostValidationService.determinar_estado_post(
            titulo=self.titulo,
            cuerpo=self.cuerpo,
            tiene_imagen=bool(self.imagen),
            imagen_aprobada=self.imagen_aprobada
        )
    
    def moderar(self, moderador, accion, razon=""):
        """Aplica una acción de moderación al post."""
        from django.utils import timezone
        
        self.moderado_por = moderador
        self.razon_moderacion = razon
        self.moderado_at = timezone.now()
        
        if accion == "aprobar":
            self.estado = Post.Estado.PUBLICADO
            # Si hay imagen pendiente, marcar como aprobada
            if self.imagen and not self.imagen_aprobada:
                self.imagen_aprobada = True
        elif accion == "rechazar":
            self.estado = Post.Estado.RECHAZADO
        elif accion == "ocultar":
            self.estado = Post.Estado.OCULTO
            
        self.save()
        
        # Registrar evento de moderación
        ModeracionEvent.objects.create(
            objeto_tipo="post",
            objeto_id=self.id,
            accion=accion,
            razones_json={"razon": razon, "moderador": moderador.id}
        )
    
    def reportar(self, usuario, tipo, descripcion=""):
        """Registra un reporte sobre el post."""
        from django.utils import timezone
        
        reporte, created = PostReporte.objects.get_or_create(
            post=self,
            usuario=usuario,
            defaults={
                "tipo": tipo,
                "descripcion": descripcion
            }
        )
        
        if created:
            self.total_reportes += 1
            self.ultimo_reporte_at = timezone.now()
            self.save(update_fields=["total_reportes", "ultimo_reporte_at"])
            
            # Si hay muchos reportes, enviar a revisión
            if self.total_reportes >= 3:
                self.estado = Post.Estado.REVISION
                self.save(update_fields=["estado"])
        
        return reporte


class Comentario(models.Model):
    """Comentario asociado a un :class:`Post`.
    
    Los comentarios permiten a los usuarios de cualquier carrera interactuar
    con posts de otros foros, aunque no puedan crear posts directamente.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios"
    )
    anonimo = models.BooleanField(default=False)
    cuerpo = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"Comentario de {self.usuario_id}"
    
    def save(self, *args, **kwargs):
        """Sobrescribe save para aplicar censura automática de texto."""
        # Aplicar censura al cuerpo del comentario
        self.cuerpo = censurar_texto(self.cuerpo)
        super().save(*args, **kwargs)


class VotoPost(models.Model):
    """Registro de votos de usuarios sobre un post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votos")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_votes"
    )
    valor = models.IntegerField(choices=[(-1, -1), (0, 0), (1, 1)])

    class Meta:
        unique_together = ("post", "usuario")


class VotoComentario(models.Model):
    """Registro de votos sobre un comentario."""

    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name="votos")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_votes"
    )
    valor = models.IntegerField(choices=[(-1, -1), (0, 0), (1, 1)])

    class Meta:
        unique_together = ("comentario", "usuario")


class PostReporte(models.Model):
    """Reportes de usuarios sobre posts inapropiados."""
    
    class TipoReporte(models.TextChoices):
        SPAM = "spam", "Spam"
        CONTENIDO_INAPROPIADO = "contenido_inapropiado", "Contenido Inapropiado"
        ACOSO = "acoso", "Acoso"
        DESINFORMACION = "desinformacion", "Desinformación"
        VIOLENCIA = "violencia", "Violencia"
        OTRO = "otro", "Otro"
    
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        RESUELTO = "resuelto", "Resuelto"
        DESCARTADO = "descartado", "Descartado"
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reportes")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reportes_realizados"
    )
    tipo = models.CharField(max_length=30, choices=TipoReporte.choices)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("post", "usuario")
    
    def __str__(self) -> str:
        return f"Reporte de {self.usuario.name} sobre {self.post.titulo}"


class OpcionEncuesta(models.Model):
    """Opciones para posts de tipo encuesta."""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="opciones_encuesta",
        limit_choices_to={'tipo': Post.TipoPost.ENCUESTA}
    )
    texto = models.CharField(max_length=200)
    votos = models.PositiveIntegerField(default=0)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Opción de Encuesta"
        verbose_name_plural = "Opciones de Encuesta"
    
    def __str__(self):
        return f"{self.texto} ({self.votos} votos)"


class VotoEncuesta(models.Model):
    """Registro de votos en encuestas."""
    
    opcion = models.ForeignKey(
        OpcionEncuesta, 
        on_delete=models.CASCADE, 
        related_name="votos_usuarios"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votos_encuestas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('opcion', 'usuario')
        verbose_name = "Voto en Encuesta"
        verbose_name_plural = "Votos en Encuestas"
    
    def __str__(self):
        return f"{self.usuario.name} votó por {self.opcion.texto}"


class ModeracionEvent(models.Model):
    """Historial mínimo de acciones de moderación."""

    objeto_tipo = models.CharField(max_length=20)
    objeto_id = models.PositiveIntegerField()
    score = models.IntegerField(default=0)
    accion = models.CharField(max_length=50)
    razones_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.accion} {self.objeto_tipo}:{self.objeto_id}"

