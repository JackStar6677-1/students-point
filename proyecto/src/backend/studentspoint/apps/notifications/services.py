"""
Servicio de notificaciones push para StudentsPoint.
"""

import json
import requests
from django.conf import settings
from django.utils import timezone
from pywebpush import webpush, WebPushException
from .models import Notificacion, NotificacionTemplate, NotificacionConfig, PushSub


class NotificationService:
    """Servicio para manejar notificaciones push."""
    
    def __init__(self):
        self.vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', '')
        self.vapid_public_key = getattr(settings, 'VAPID_PUBLIC_KEY', '')
        self.vapid_claims = {
            "sub": getattr(settings, 'VAPID_CLAIMS_SUB', 'mailto:admin@studentspoint.com')
        }
    
    def send_notification(self, usuario, titulo, mensaje, tipo='info', url_redirect='', icono='', prioridad='media', data_extra=None):
        """Envía una notificación a un usuario específico."""
        try:
            # Verificar configuración del usuario
            config = self._get_user_config(usuario)
            if not self._should_send_notification(config, tipo):
                return False
            
            # Crear notificación en base de datos
            notificacion = Notificacion.objects.create(
                usuario=usuario,
                titulo=titulo,
                mensaje=mensaje,
                tipo=tipo,
                url_redirect=url_redirect,
                icono=icono,
                prioridad=prioridad,
                data_extra=data_extra or {}
            )
            
            # Enviar push notification
            self._send_push_notification(usuario, notificacion)
            
            return notificacion
            
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def send_bulk_notification(self, usuarios, titulo, mensaje, tipo='info', url_redirect='', icono='', prioridad='media', data_extra=None):
        """Envía una notificación a múltiples usuarios."""
        notificaciones_enviadas = []
        
        for usuario in usuarios:
            notificacion = self.send_notification(
                usuario=usuario,
                titulo=titulo,
                mensaje=mensaje,
                tipo=tipo,
                url_redirect=url_redirect,
                icono=icono,
                prioridad=prioridad,
                data_extra=data_extra
            )
            if notificacion:
                notificaciones_enviadas.append(notificacion)
        
        return notificaciones_enviadas
    
    def send_template_notification(self, template_name, usuario, context=None):
        """Envía una notificación usando una plantilla."""
        try:
            template = NotificacionTemplate.objects.get(nombre=template_name, activa=True)
            context = context or {}
            
            # Renderizar plantilla con contexto
            titulo = template.titulo_template.format(**(context or {}))
            mensaje = template.mensaje_template.format(**(context or {}))
            
            return self.send_notification(
                usuario=usuario,
                titulo=titulo,
                mensaje=mensaje,
                tipo=template.tipo,
                icono=template.icono,
                prioridad=template.prioridad
            )
            
        except NotificacionTemplate.DoesNotExist:
            print(f"Template {template_name} not found")
            return False
    
    def _get_user_config(self, usuario):
        """Obtiene la configuración de notificaciones del usuario."""
        try:
            return usuario.notificacion_config
        except:
            # Crear configuración por defecto
            return NotificacionConfig.objects.create(usuario=usuario)
    
    def _should_send_notification(self, config, tipo):
        """Verifica si se debe enviar la notificación según la configuración del usuario."""
        if not config:
            return True
        
        # Verificar si el usuario quiere recibir este tipo de notificación
        tipo_config_map = {
            'forum': config.recibir_foro,
            'market': config.recibir_market,
            'portfolio': config.recibir_portfolio,
            'campus': config.recibir_campus,
            'polls': config.recibir_polls,
            'academic': config.recibir_academic,
            'system': config.recibir_system,
        }
        
        return tipo_config_map.get(tipo, True)
    
    def _send_push_notification(self, usuario, notificacion):
        """Envía la notificación push a través de Web Push API."""
        try:
            # Obtener suscripciones activas del usuario
            subscriptions = PushSub.objects.filter(usuario=usuario, activo=True)
            
            if not subscriptions.exists():
                return False
            
            # Preparar payload de la notificación
            payload = {
                'title': notificacion.titulo,
                'body': notificacion.mensaje,
                'icon': '/static/images/icons/icon-192x192.png',
                'badge': '/static/images/icons/icon-192x192.png',
                'data': {
                    'url': notificacion.url_redirect or '/',
                    'notificacion_id': str(notificacion.id),
                    'tipo': notificacion.tipo,
                    'prioridad': notificacion.prioridad
                }
            }
            
            # Enviar a cada suscripción
            for subscription in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.p256dh,
                                "auth": subscription.auth
                            }
                        },
                        data=json.dumps(payload),
                        vapid_private_key=self.vapid_private_key,
                        vapid_claims=self.vapid_claims
                    )
                    notificacion.enviada_push = True
                    notificacion.save(update_fields=['enviada_push'])
                    
                except WebPushException as e:
                    print(f"WebPush error: {e}")
                    # Marcar suscripción como inactiva si hay error
                    if e.response and e.response.status_code == 410:
                        subscription.activo = False
                        subscription.save(update_fields=['activo'])
            
            return True
            
        except Exception as e:
            print(f"Error sending push notification: {e}")
            return False
    
    def mark_as_read(self, notificacion_id, usuario):
        """Marca una notificación como leída."""
        try:
            notificacion = Notificacion.objects.get(id=notificacion_id, usuario=usuario)
            notificacion.marcar_como_leida()
            return True
        except Notificacion.DoesNotExist:
            return False
    
    def get_user_notifications(self, usuario, limit=20, offset=0, unread_only=False):
        """Obtiene las notificaciones de un usuario."""
        queryset = Notificacion.objects.filter(usuario=usuario)
        
        if unread_only:
            queryset = queryset.filter(leida=False)
        
        return queryset[offset:offset + limit]
    
    def get_unread_count(self, usuario):
        """Obtiene el número de notificaciones no leídas de un usuario."""
        return Notificacion.objects.filter(usuario=usuario, leida=False).count()


# Funciones de conveniencia para notificaciones específicas
def notify_forum_post(usuario, post_titulo, foro_nombre):
    """Notifica sobre un nuevo post en el foro."""
    service = NotificationService()
    return service.send_notification(
        usuario=usuario,
        titulo=f"Nuevo post en {foro_nombre}",
        mensaje=f"Se publicó: {post_titulo}",
        tipo='forum',
        url_redirect='/forum/',
        icono='fas fa-comments',
        prioridad='media'
    )

def notify_market_product(usuario, producto_titulo, accion='nuevo'):
    """Notifica sobre actividad en el marketplace."""
    service = NotificationService()
    return service.send_notification(
        usuario=usuario,
        titulo=f"Producto {accion} en el mercado",
        mensaje=f"{producto_titulo}",
        tipo='market',
        url_redirect='/market/',
        icono='fas fa-store',
        prioridad='baja'
    )

def notify_campus_update(usuario, titulo, mensaje):
    """Notifica sobre actualizaciones del campus."""
    service = NotificationService()
    return service.send_notification(
        usuario=usuario,
        titulo=titulo,
        mensaje=mensaje,
        tipo='campus',
        url_redirect='/streetview/',
        icono='fas fa-map',
        prioridad='media'
    )

def notify_poll_created(usuario, encuesta_titulo):
    """Notifica sobre una nueva encuesta."""
    service = NotificationService()
    return service.send_notification(
        usuario=usuario,
        titulo="Nueva encuesta disponible",
        mensaje=f"Participa en: {encuesta_titulo}",
        tipo='polls',
        url_redirect='/encuestas/',
        icono='fas fa-poll',
        prioridad='media'
    )

def notify_academic_update(usuario, titulo, mensaje):
    """Notifica sobre actualizaciones académicas."""
    service = NotificationService()
    return service.send_notification(
        usuario=usuario,
        titulo=titulo,
        mensaje=mensaje,
        tipo='academic',
        url_redirect='/cursos/',
        icono='fas fa-graduation-cap',
        prioridad='alta'
    )
