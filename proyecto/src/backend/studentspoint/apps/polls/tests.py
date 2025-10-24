"""Tests completos para el sistema mejorado de encuestas."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from studentspoint.apps.campuses.models import Sede
from .models import Poll, PollOpcion, PollVoto, PollAnalytics

User = get_user_model()


class PollModelTests(TestCase):
    """Tests para los modelos de encuestas."""
    
    def setUp(self):
        self.sede = Sede.objects.create(
            slug="central", nombre="Sede Central", direccion="Av 1", lat=0, lng=0
        )
        self.moderator = User.objects.create_user(
            email="mod@duocuc.cl", password="pass123", 
            role=User.Roles.MODERATOR, campus=self.sede, career="Informática"
        )
        self.student = User.objects.create_user(
            email="student@duocuc.cl", password="pass123",
            role=User.Roles.STUDENT, campus=self.sede, career="Informática"
        )
    
    def test_crear_encuesta_independiente(self):
        """Test crear encuesta sin vincular a post."""
        poll = Poll.objects.create(
            titulo="Encuesta Test",
            descripcion="Descripción test",
            creador=self.moderator,
            estado=Poll.Estado.ACTIVA
        )
        
        self.assertEqual(poll.titulo, "Encuesta Test")
        self.assertEqual(poll.creador, self.moderator)
        self.assertTrue(poll.esta_activa)
        self.assertIsNone(poll.post)
    
    def test_permisos_votacion(self):
        """Test verificación de permisos para votar."""
        poll = Poll.objects.create(
            titulo="Encuesta Restringida",
            creador=self.moderator,
            estado=Poll.Estado.ACTIVA
        )
        poll.sedes.add(self.sede)
        poll.carreras = ["Informática"]
        poll.save()
        
        # Usuario con permisos
        self.assertTrue(poll.puede_votar(self.student))


class PollAPITests(APITestCase):
    """Tests para la API de encuestas."""
    
    def setUp(self):
        self.sede = Sede.objects.create(
            slug="central", nombre="Sede Central", direccion="Av 1", lat=0, lng=0
        )
        self.moderator = User.objects.create_user(
            email="mod@duocuc.cl", password="pass123", 
            role=User.Roles.MODERATOR, campus=self.sede, career="Informática"
        )
        
        # Login como moderador
        response = self.client.post('/api/auth/login', {
            'email': self.moderator.email,
            'password': 'pass123'
        })
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def test_crear_encuesta_completa(self):
        """Test crear encuesta con todas las opciones."""
        data = {
            'titulo': 'Encuesta Test Completa',
            'descripcion': 'Descripción de prueba',
            'multi': True,
            'opciones': [
                {'texto': 'Opción 1'},
                {'texto': 'Opción 2'}
            ]
        }
        
        response = self.client.post('/api/polls/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        poll = Poll.objects.get(id=response.data['id'])
        self.assertEqual(poll.titulo, data['titulo'])
        self.assertTrue(poll.multi)
        self.assertEqual(poll.opciones.count(), 2)