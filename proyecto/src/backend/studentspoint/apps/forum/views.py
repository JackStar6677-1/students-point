"""Vistas para la API del foro."""

from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, Throttled
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema

from studentspoint.apps.accounts.permissions import IsModerator

from .models import Comentario, Foro, Post, PostReporte, VotoPost
from .services import ForumPermissionService
from .serializers import (
    ComentarioSerializer,
    OpcionEncuestaSerializer,
    ForumDetailSerializer,
    ForoSerializer,
    ModeracionSerializer,
    PostReporteSerializer,
    PostSerializer,
    ScoreSerializer,
    VoteSerializer,
)


class EncuestaVotarView(APIView):
    """Permite a un usuario votar por una opción de encuesta."""
    permission_classes = [IsAuthenticated]

    @extend_schema(description="Votar por una opción de encuesta del post", responses=ScoreSerializer)
    def post(self, request, pk, opcion_id):
        post = get_object_or_404(Post, pk=pk)
        if post.tipo != Post.TipoPost.ENCUESTA:
            return Response({"detail": "El post no es una encuesta"}, status=status.HTTP_400_BAD_REQUEST)
        opcion = get_object_or_404(post.opciones_encuesta, pk=opcion_id)
        # Registrar voto único por usuario en la ENCUESTA (no por opción)
        from .models import VotoEncuesta
        # Eliminar votos anteriores del usuario sobre otras opciones de esta encuesta
        VotoEncuesta.objects.filter(usuario=request.user, opcion__post=post).exclude(opcion=opcion).delete()
        # Crear/actualizar voto en esta opción
        VotoEncuesta.objects.update_or_create(opcion=opcion, usuario=request.user)
        # Recalcular votos de todas las opciones
        for opt in post.opciones_encuesta.all():
            opt.votos = opt.votos_usuarios.count()
            opt.save(update_fields=["votos"])
        total = post.opciones_encuesta.aggregate(total=Sum("votos")) or {"total": 0}
        return Response({"total_votos": total.get("total", 0)})


class EncuestaOpcionesListView(generics.ListAPIView):
    """Lista opciones de encuesta de un post."""
    serializer_class = OpcionEncuestaSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return post.opciones_encuesta.all()


class ForoListView(generics.ListAPIView):
    """Lista los foros disponibles filtrando por sede y carrera.

    El frontend utilizará este endpoint para mostrar los foros
    pertinentes al usuario según su sede y carrera.
    
    Foros privados solo son visibles para estudiantes de la carrera correspondiente.
    """

    serializer_class = ForoSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Asegurar foros por defecto si no existen
        self._ensure_default_foros()
        
        # Optimización máxima: usar select_related y solo() para evitar N+1
        queryset = Foro.objects.select_related('sede').only(
            'id', 'sede__id', 'sede__nombre', 'sede__slug',
            'carrera', 'titulo', 'slug', 'es_privado', 
            'descripcion', 'created_at'
        ).order_by('carrera', 'titulo')
        
        # Filtrar foros según permisos del usuario usando el servicio
        queryset = ForumPermissionService.filtrar_foros_visibles(
            self.request.user, queryset
        )
        
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
            sedes = [Sede.objects.create(
                nombre="Sede Central", 
                slug="sede-central",
                lat=-33.4489,
                lng=-70.6693
            )]
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


class PostListCreateView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """Lista posts de un foro y permite crear nuevas publicaciones.
    
    RESTRICCION IMPORTANTE: Los usuarios solo pueden crear posts en el foro
    correspondiente a su carrera. Sin embargo, pueden comentar en posts de
    cualquier foro.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def create(self, request, *args, **kwargs):  # pragma: no cover - thin wrapper
        # Compatibilidad: aceptar 'texto' como alias de 'comentario'
        data = request.data.copy()
        if data.get('tipo') == 'texto':
            data['tipo'] = Post.TipoPost.COMENTARIO

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Optimización: usar select_related y prefetch_related para evitar N+1
        queryset = Post.objects.select_related(
            'foro', 
            'foro__sede', 
            'usuario'
        ).prefetch_related(
            'comentarios',
            'votos',
            'reportes'
        ).all()
        
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
        # Restringir visibilidad según foro privado usando el servicio
        # Para posts necesitamos filtrar por foro, así que usamos una consulta diferente
        user = self.request.user
        if user.is_authenticated:
            if not ForumPermissionService.puede_moderar(user):
                queryset = queryset.filter(
                    Q(foro__es_privado=False) | Q(foro__es_privado=True, foro__carrera=user.career)
                )
        else:
            # Usuarios no autenticados: listar solo foros públicos y limitar cantidad si se pasa ?limit=
            queryset = queryset.filter(foro__es_privado=False)
            try:
                limit = int(self.request.query_params.get("limit", "0"))
                if limit > 0:
                    queryset = queryset[:limit]
            except Exception:
                pass

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """Eliminar un post y actualizar reportes relacionados. Solo para moderadores/admins."""
        # Verificar permisos de moderador/admin
        if not IsModerator().has_permission(request, self):
            return Response(
                {'error': 'No tienes permisos para eliminar posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post = self.get_object()
        
        # Actualizar todos los reportes relacionados a "post_eliminado"
        PostReporte.objects.filter(post=post).update(
            estado=PostReporte.Estado.POST_ELIMINADO
        )
        
        # Eliminar el post
        post.delete()
        
        # 204 No Content no debe tener body
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        # Obtener el foro donde se va a postear
        foro = serializer.validated_data.get('foro')
        
        # REGLA: Solo se puede postear en el foro de la propia carrera
        # Excepto si es admin o moderador
        if not ForumPermissionService.puede_postear_en_foro(self.request.user, foro):
            raise PermissionDenied(
                f"Solo puedes crear publicaciones en el foro de tu carrera ({self.request.user.career}). "
                f"Este foro es para {foro.carrera}. Puedes comentar en posts de otros foros."
            )
        
        # Rate limiting: máximo 5 posts por hora por usuario (anti-spam)
        limite_hora = timezone.now() - timedelta(hours=1)
        creados_ultima_hora = Post.objects.filter(
            usuario=self.request.user,
            created_at__gte=limite_hora
        ).count()
        if creados_ultima_hora >= 5:
            raise Throttled(detail="Has alcanzado el límite de 5 publicaciones por hora. Intenta más tarde.")

        # Manejar imagen, enlace o archivo si se enviaron
        imagen = self.request.FILES.get('imagen')
        archivo = self.request.FILES.get('archivo')
        enlace_url = self.request.data.get('enlace_url')
        if imagen:
            serializer.validated_data['imagen'] = imagen
            serializer.validated_data['tipo'] = Post.TipoPost.IMAGEN
        elif archivo:
            serializer.validated_data['archivo'] = archivo
            serializer.validated_data['tipo'] = Post.TipoPost.ARCHIVO
        elif enlace_url:
            serializer.validated_data['enlace_url'] = enlace_url
            serializer.validated_data['tipo'] = Post.TipoPost.ENLACE
        
        post = serializer.save(usuario=self.request.user)
        # Verificar contenido automáticamente
        estado = post.verificar_contenido()
        post.estado = estado
        post.save(update_fields=["estado"])
        
        # Registrar actividad del usuario
        try:
            from studentspoint.apps.accounts.models_audit import UserActivityLog
            ip_address = self.request.META.get('REMOTE_ADDR')
            user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]
            UserActivityLog.objects.create(
                usuario=self.request.user,
                tipo=UserActivityLog.TipoActividad.CREACION_POST,
                descripcion=f'Post creado: {post.titulo[:50]}...',
                ip_address=ip_address,
                user_agent=user_agent,
                datos_adicionales={
                    'post_id': post.id,
                    'foro': post.foro.titulo,
                    'tipo': post.tipo
                }
            )
        except Exception:
            pass  # No fallar si no hay modelo de auditoría


class CommentCreateView(generics.ListCreateAPIView):
    """Lista y crea comentarios dentro de un post."""

    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return Comentario.objects.filter(post=post).order_by("created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        comentario = serializer.save(post=post, usuario=self.request.user)
        
        # Registrar actividad del usuario
        try:
            from studentspoint.apps.accounts.models_audit import UserActivityLog
            ip_address = self.request.META.get('REMOTE_ADDR')
            user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]
            UserActivityLog.objects.create(
                usuario=self.request.user,
                tipo=UserActivityLog.TipoActividad.CREACION_COMENTARIO,
                descripcion=f'Comentario creado en post: {post.titulo[:50]}...',
                ip_address=ip_address,
                user_agent=user_agent,
                datos_adicionales={
                    'comentario_id': comentario.id,
                    'post_id': post.id
                }
            )
        except Exception:
            pass  # No fallar si no hay modelo de auditoría


class PostVoteView(APIView):
    """Registra el voto del usuario para un post."""
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Crear reporte con manejo de errores mejorado"""
        try:
            post = get_object_or_404(Post, pk=self.kwargs["pk"])
            
            # Validar datos
            tipo = request.data.get('tipo')
            descripcion = request.data.get('descripcion', '')
            
            if not tipo:
                return Response(
                    {'error': 'Debes especificar el tipo de reporte'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el método reportar del modelo (maneja duplicados automáticamente)
            reporte = post.reportar(request.user, tipo, descripcion)
            
            # Serializar el reporte creado/actualizado
            serializer = self.get_serializer(reporte)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al crear el reporte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        
        detalle = {"detail": f"Post {accion}do exitosamente", "estado": post.estado}
        if post.imagen:
            detalle.update({
                "imagen_aprobada": post.imagen_aprobada,
                "imagen_url": request.build_absolute_uri(post.imagen.url) if post.imagen else None,
            })
        return Response(detalle)


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
        qs = Post.objects.filter(estado=Post.Estado.REVISION).order_by("-created_at")
        # Filtros opcionales
        foro_id = self.request.query_params.get("foro_id")
        usuario_id = self.request.query_params.get("usuario_id")
        if foro_id:
            qs = qs.filter(foro_id=foro_id)
        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        return qs


class PostReportesListView(generics.ListAPIView):
    """Lista reportes de un post específico."""
    
    permission_classes = [IsModerator]
    serializer_class = PostReporteSerializer
    
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        qs = PostReporte.objects.filter(post=post).order_by("-created_at")
        estado = self.request.query_params.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class ReporteUpdateView(generics.UpdateAPIView):
    """Permite a moderadores y administradores actualizar el estado de un reporte."""
    permission_classes = [IsModerator]
    serializer_class = PostReporteSerializer

    def get_queryset(self):
        return PostReporte.objects.all()


class TodosReportesListView(generics.ListAPIView):
    """Lista TODOS los reportes del foro - Solo para administradores."""
    
    permission_classes = [IsModerator]
    serializer_class = PostReporteSerializer
    
    def get_queryset(self):
        """Obtener todos los reportes con información del post"""
        qs = PostReporte.objects.select_related(
            'post', 'post__usuario', 'post__foro', 'usuario'
        ).order_by("-created_at")
        
        # Filtros opcionales
        estado = self.request.query_params.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        
        tipo = self.request.query_params.get("tipo")
        if tipo:
            qs = qs.filter(tipo=tipo)
        
        return qs
