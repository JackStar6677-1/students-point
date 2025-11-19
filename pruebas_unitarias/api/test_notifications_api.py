"""
Pruebas unitarias para la API de Notificaciones
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from studentspoint.apps.notifications.models import Notificacion, NotificacionConfig

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para notificaciones"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestNotificationsAPI:
    """Pruebas para la API de Notificaciones"""
    
    def test_list_notifications_authenticated(self, client, user):
        """Prueba listar notificaciones con usuario autenticado"""
        # Crear algunas notificaciones
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación 1',
            mensaje='Mensaje de prueba 1',
            tipo='info'
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación 2',
            mensaje='Mensaje de prueba 2',
            tipo='success'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/notifications/notificaciones/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_list_notifications_unauthenticated(self, client):
        """Prueba listar notificaciones sin autenticación"""
        response = client.get('/api/notifications/notificaciones/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_notification_authenticated(self, client, user):
        """Prueba crear notificación con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Nueva Notificación',
            'mensaje': 'Este es un mensaje de prueba',
            'tipo': 'info',
            'prioridad': 'media'
        }
        response = client.post('/api/notifications/notificaciones/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Notificacion.objects.count() == 1
        assert Notificacion.objects.first().usuario == user
    
    def test_create_notification_unauthenticated(self, client):
        """Prueba crear notificación sin autenticación"""
        data = {
            'titulo': 'Nueva Notificación',
            'mensaje': 'Este es un mensaje de prueba',
            'tipo': 'info'
        }
        response = client.post('/api/notifications/notificaciones/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_mark_notification_as_read(self, client, user):
        """Prueba marcar notificación como leída"""
        notificacion = Notificacion.objects.create(
            usuario=user,
            titulo='Notificación No Leída',
            mensaje='Esta notificación no está leída',
            tipo='info',
            leida=False
        )
        
        client.force_authenticate(user=user)
        response = client.patch(f'/api/notifications/notificaciones/{notificacion.id}/marcar_leida/')
        assert response.status_code == status.HTTP_200_OK
        
        notificacion.refresh_from_db()
        assert notificacion.leida == True
        assert notificacion.leida_at is not None
    
    def test_mark_all_notifications_as_read(self, client, user):
        """Prueba marcar todas las notificaciones como leídas"""
        # Crear notificaciones leídas y no leídas
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación 1',
            mensaje='Mensaje 1',
            tipo='info',
            leida=False
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación 2',
            mensaje='Mensaje 2',
            tipo='success',
            leida=False
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación 3',
            mensaje='Mensaje 3',
            tipo='warning',
            leida=True
        )
        
        client.force_authenticate(user=user)
        response = client.post('/api/notifications/notificaciones/marcar_todas_leidas/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que todas están leídas
        notificaciones = Notificacion.objects.filter(usuario=user)
        for notif in notificaciones:
            assert notif.leida == True
    
    def test_notification_types_filter(self, client, user):
        """Prueba filtrado por tipo de notificación"""
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación Info',
            mensaje='Mensaje de información',
            tipo='info'
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación Error',
            mensaje='Mensaje de error',
            tipo='error'
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación Foro',
            mensaje='Mensaje del foro',
            tipo='forum'
        )
        
        client.force_authenticate(user=user)
        
        # Filtrar por tipo info
        response = client.get('/api/notifications/notificaciones/?tipo=info')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['tipo'] == 'info'
        
        # Filtrar por tipo error
        response = client.get('/api/notifications/notificaciones/?tipo=error')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['tipo'] == 'error'
    
    def test_notification_read_status_filter(self, client, user):
        """Prueba filtrado por estado de lectura"""
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación Leída',
            mensaje='Esta está leída',
            tipo='info',
            leida=True
        )
        Notificacion.objects.create(
            usuario=user,
            titulo='Notificación No Leída',
            mensaje='Esta no está leída',
            tipo='info',
            leida=False
        )
        
        client.force_authenticate(user=user)
        
        # Filtrar por no leídas
        response = client.get('/api/notifications/notificaciones/?leida=false')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['leida'] == False
        
        # Filtrar por leídas
        response = client.get('/api/notifications/notificaciones/?leida=true')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['leida'] == True
    
    def test_notification_config_creation(self, client, user):
        """Prueba creación de configuración de notificaciones"""
        client.force_authenticate(user=user)
        data = {
            'recibir_foro': True,
            'recibir_market': False,
            'recibir_portfolio': True,
            'recibir_campus': True,
            'recibir_polls': False,
            'recibir_academic': True,
            'recibir_system': True,
            'frecuencia_email': 'diario',
            'horario_inicio': '09:00',
            'horario_fin': '18:00',
            'solo_dias_laborales': True
        }
        response = client.post('/api/notifications/config/', data)
        assert response.status_code == status.HTTP_201_CREATED
        
        config = NotificacionConfig.objects.get(usuario=user)
        assert config.recibir_foro == True
        assert config.recibir_market == False
        assert config.frecuencia_email == 'diario'
    
    def test_notification_config_update(self, client, user):
        """Prueba actualización de configuración de notificaciones"""
        config = NotificacionConfig.objects.create(
            usuario=user,
            recibir_foro=True,
            recibir_market=True,
            frecuencia_email='inmediato'
        )
        
        client.force_authenticate(user=user)
        data = {
            'recibir_foro': False,
            'frecuencia_email': 'semanal'
        }
        response = client.patch(f'/api/notifications/config/{config.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        
        config.refresh_from_db()
        assert config.recibir_foro == False
        assert config.frecuencia_email == 'semanal'
    
    def test_notification_priority_levels(self, client, user):
        """Prueba diferentes niveles de prioridad de notificaciones"""
        client.force_authenticate(user=user)
        
        # Crear notificaciones con diferentes prioridades
        for prioridad in ['baja', 'media', 'alta']:
            data = {
                'titulo': f'Notificación {prioridad.title()}',
                'mensaje': f'Mensaje con prioridad {prioridad}',
                'tipo': 'info',
                'prioridad': prioridad
            }
            response = client.post('/api/notifications/notificaciones/', data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que se crearon correctamente
        assert Notificacion.objects.count() == 3
        assert Notificacion.objects.filter(prioridad='baja').count() == 1
        assert Notificacion.objects.filter(prioridad='media').count() == 1
        assert Notificacion.objects.filter(prioridad='alta').count() == 1
    
    def test_notification_with_extra_data(self, client, user):
        """Prueba notificación con datos extra"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Notificación con Datos Extra',
            'mensaje': 'Esta notificación tiene datos adicionales',
            'tipo': 'forum',
            'data_extra': {
                'post_id': 123,
                'forum_name': 'Foro de Ingeniería',
                'action': 'new_comment'
            },
            'url_redirect': '/forum/posts/123/',
            'icono': 'fa-comment'
        }
        response = client.post('/api/notifications/notificaciones/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        notificacion = Notificacion.objects.first()
        assert notificacion.data_extra['post_id'] == 123
        assert notificacion.data_extra['forum_name'] == 'Foro de Ingeniería'
        assert notificacion.url_redirect == '/forum/posts/123/'
        assert notificacion.icono == 'fa-comment'
