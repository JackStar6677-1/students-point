"""Views for Web Push subscription management and testing."""

from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from .models import PushSub, Notificacion
from .serializers import PushSubSerializer, NotificationStatusSerializer, NotificacionSerializer
from .tasks import send_class_push


class PushSubscribeView(generics.CreateAPIView):
    serializer_class = PushSubSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PushTestView(generics.GenericAPIView):
    """Send a dummy notification to check the service worker."""

    serializer_class = NotificationStatusSerializer

    @extend_schema(responses=NotificationStatusSerializer)
    def post(self, request, *args, **kwargs):
        send_class_push.delay(request.user.id, None, None, None, test_only=True)
        return Response({"status": "sent"})


@extend_schema(
    summary="Obtener notificaciones del usuario",
    responses={200: NotificacionSerializer(many=True)}
)
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_notifications(request):
    """Obtiene las notificaciones del usuario actual."""
    notifications = Notificacion.objects.filter(usuario=request.user).order_by('-created_at')[:20]
    serializer = NotificacionSerializer(notifications, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Marcar notificación como leída",
    responses={200: {"status": "ok"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Marca una notificación como leída."""
    try:
        notification = Notificacion.objects.get(id=notification_id, usuario=request.user)
        notification.leida = True
        notification.save()
        return Response({"status": "ok"})
    except Notificacion.DoesNotExist:
        return Response({"error": "Notificación no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Marcar todas las notificaciones como leídas",
    responses={200: {"status": "ok"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Marca todas las notificaciones del usuario como leídas."""
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    return Response({"status": "ok"})
