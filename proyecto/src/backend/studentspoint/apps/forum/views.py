"""Vistas para la API del foro."""

from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema

from studentspoint.apps.accounts.permissions import IsModerator

from .models import BANNED_WORDS, MODERATION_WORDS, Comentario, Foro, Post, PostReporte, VotoPost
from .serializers import (
    ComentarioSerializer,
    ForumDetailSerializer,
    ForoSerializer,
    ModeracionSerializer,
    PostReporteSerializer,
    PostSerializer,
    ScoreSerializer,
    VoteSerializer,
)


class ForoListView(generics.ListAPIView):
    """Lista los foros disponibles filtrando por sede y carrera.

    El frontend utilizará este endpoint para mostrar los foros
    pertinentes al usuario según su sede y carrera.
    
    Foros privados solo son visibles para estudiantes de la carrera correspondiente.
    """

    serializer_class = ForoSerializer

    def get_queryset(self):
        # Asegurar foros por defecto si no existen
        self._ensure_default_foros()
        queryset = Foro.objects.all()
        
        # Filtrar foros según permisos del usuario
        if self.request.user.is_authenticated:
            # Si es admin o moderador, puede ver todos
            if self.request.user.is_staff or self.request.user.role in ['moderator', 'admin_global']:
                pass
            else:
                # Mostrar foros públicos + foros privados de su carrera
                queryset = queryset.filter(
                    Q(es_privado=False) | 
                    Q(es_privado=True, carrera=self.request.user.career)
                )
        else:
            # Usuarios no autenticados solo ven foros públicos
            queryset = queryset.filter(es_privado=False)
        
        # Filtros adicionales
        sede = self.request.query_params.get("sede")
        carrera = self.request.query_params.get("carrera")
        if sede:
            queryset = queryset.filter(sede__slug=sede)
        if carrera:
            queryset = queryset.filter(carrera=carrera)
        return queryset

    def _ensure_default_foros(self):
        if Foro.objects.exists():
            return
        from studentspoint.apps.campuses.models import Sede
        from django.utils.text import slugify
        carreras = [
            "Ingeniería en Informática",
            "Ingeniería en Construcción",
            "Ingeniería en Electricidad",
            "Administración",
            "Contabilidad",
            "Técnico en Informática",
        ]
        sedes = list(Sede.objects.all())
        if not sedes:
            # Crear sede base si no hay
            sedes = [Sede.objects.create(nombre="Sede Central", slug="sede-central")]
        for sede in sedes:
            for carrera in carreras:
                slug = f"{sede.slug}-{slugify(carrera)}"
                Foro.objects.get_or_create(
                    sede=sede,
                    carrera=carrera,
                    defaults={
                        "titulo": f"{carrera} - {sede.nombre}",
                        "slug": slug,
                    },
                )


class PostListCreateView(generics.ListCreateAPIView):
    """Lista posts de un foro y permite crear nuevas publicaciones.
    
    RESTRICCION IMPORTANTE: Los usuarios solo pueden crear posts en el foro
    correspondiente a su carrera. Sin embargo, pueden comentar en posts de
    cualquier foro.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        foro_id = self.request.query_params.get("foro_id")
        if foro_id:
            queryset = queryset.filter(foro_id=foro_id)
        orden = self.request.query_params.get("orden", "nuevo")
        if orden == "top":
            queryset = queryset.order_by("-score")
        else:
            queryset = queryset.order_by("-created_at")
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def perform_create(self, serializer):
        # Obtener el foro donde se va a postear
        foro = serializer.validated_data.get('foro')
        
        # REGLA: Solo se puede postear en el foro de la propia carrera
        # Excepto si es admin o moderador
        if not (self.request.user.is_staff or 
                self.request.user.role in ['moderator', 'admin_global']):
            if not foro.puede_postear(self.request.user):
                raise PermissionDenied(
                    f"Solo puedes crear publicaciones en el foro de tu carrera ({self.request.user.career}). "
                    f"Este foro es para {foro.carrera}. Puedes comentar en posts de otros foros."
                )
        
        post = serializer.save(usuario=self.request.user)
        # Verificar contenido automáticamente
        estado = post.verificar_contenido()
        post.estado = estado
        post.save(update_fields=["estado"])


class CommentCreateView(generics.ListCreateAPIView):
    """Lista y crea comentarios dentro de un post."""

    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return Comentario.objects.filter(post=post).order_by("created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(post=post, usuario=self.request.user)


class PostVoteView(APIView):
    """Registra el voto del usuario para un post."""
    @extend_schema(request=VoteSerializer, responses=ScoreSerializer)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            valor = int(request.data.get("valor"))
        except (TypeError, ValueError):
            return Response({"detail": "valor inválido"}, status=status.HTTP_400_BAD_REQUEST)
        if valor not in (-1, 0, 1):
            return Response({"detail": "valor inválido"}, status=status.HTTP_400_BAD_REQUEST)
        VotoPost.objects.update_or_create(
            post=post, usuario=request.user, defaults={"valor": valor}
        )
        post.score = post.votos.aggregate(score=Sum("valor"))["score"] or 0
        post.save(update_fields=["score"])
        return Response({"score": post.score})


class PostReporteView(generics.CreateAPIView):
    """Permite a usuarios reportar posts inapropiados."""
    
    serializer_class = PostReporteSerializer
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(post=post, usuario=self.request.user)


class PostModeracionView(generics.GenericAPIView):
    """Permite a moderadores moderar posts."""
    
    permission_classes = [IsModerator]
    serializer_class = ModeracionSerializer
    
    @extend_schema(request=ModeracionSerializer, responses=ForumDetailSerializer)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        accion = serializer.validated_data["accion"]
        razon = serializer.validated_data.get("razon", "")
        
        post.moderar(request.user, accion, razon)
        
        return Response({"detail": f"Post {accion}do exitosamente"})


class PostHideView(generics.GenericAPIView):
    """Permite a moderadores ocultar posts."""

    permission_classes = [IsModerator]
    serializer_class = ForumDetailSerializer

    @extend_schema(responses=ForumDetailSerializer)
    def post(self, request, pk):  # pragma: no cover - acción administrativa
        post = get_object_or_404(Post, pk=pk)
        post.estado = Post.Estado.OCULTO
        post.save(update_fields=["estado"])
        return Response({"detail": "post oculto"})


class ModeracionListView(generics.ListAPIView):
    """Lista posts que requieren moderación."""
    
    permission_classes = [IsModerator]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(estado=Post.Estado.REVISION).order_by("-created_at")


class PostReportesListView(generics.ListAPIView):
    """Lista reportes de un post específico."""
    
    permission_classes = [IsModerator]
    serializer_class = PostReporteSerializer
    
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return PostReporte.objects.filter(post=post).order_by("-created_at")

