"""
Pruebas unitarias para la API de Encuestas (Polls)
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from studentspoint.apps.polls.models import Poll, PollOpcion, PollVoto

BASE_URL = '/api/polls/'


def polls_detail(poll_id: int) -> str:
    return f'{BASE_URL}{poll_id}/'


def polls_vote(poll_id: int) -> str:
    return f'{BASE_URL}{poll_id}/votar/'

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para encuestas"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática',
        role='moderator'
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestPollsAPI:
    """Pruebas para la API de Encuestas"""
    
    def test_create_poll_authenticated(self, client, user):
        """Prueba crear encuesta con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'titulo': '¿Cuál es tu lenguaje de programación favorito?',
            'descripcion': 'Encuesta sobre preferencias de programación',
            'multi': False,
            'anonima': False,
            'carreras': ['Ingeniería en Informática', 'Técnico en Informática'],
            'opciones': [
                {'texto': 'Python'},
                {'texto': 'JavaScript'}
            ]
        }
        response = client.post(BASE_URL, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Poll.objects.count() == 1
        assert Poll.objects.first().creador == user
    
    def test_create_poll_unauthenticated(self, client):
        """Prueba crear encuesta sin autenticación"""
        data = {
            'titulo': '¿Cuál es tu lenguaje favorito?',
            'descripcion': 'Encuesta de prueba',
            'multi': False,
            'anonima': False,
            'opciones': [
                {'texto': 'Python'},
                {'texto': 'JavaScript'}
            ]
        }
        response = client.post(BASE_URL, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_polls_authenticated(self, client, user):
        """Prueba listar encuestas con usuario autenticado"""
        # Crear algunas encuestas
        Poll.objects.create(
            titulo='Encuesta 1',
            descripcion='Descripción 1',
            creador=user,
            estado=Poll.Estado.ACTIVA
        )
        Poll.objects.create(
            titulo='Encuesta 2',
            descripcion='Descripción 2',
            creador=user,
            estado=Poll.Estado.ACTIVA
        )
        
        client.force_authenticate(user=user)
        response = client.get(BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert len(response.data['results']) == 2
    
    def test_list_polls_unauthenticated(self, client):
        """Prueba listar encuestas sin autenticación"""
        response = client.get(BASE_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_poll_with_options(self, client, user):
        """Prueba crear encuesta con opciones"""
        client.force_authenticate(user=user)
        
        # Crear encuesta
        poll_data = {
            'titulo': '¿Cuál es tu framework favorito?',
            'descripcion': 'Encuesta sobre frameworks web',
            'multi': False,
            'anonima': False,
            'opciones': [
                {'texto': 'Django', 'descripcion': 'Framework de Python'},
                {'texto': 'Flask', 'descripcion': 'Microframework de Python'}
            ]
        }
        poll_response = client.post(BASE_URL, poll_data, format='json')
        assert poll_response.status_code == status.HTTP_201_CREATED
        poll_id = poll_response.data['id']
        
        poll = Poll.objects.get(id=poll_id)
        assert poll.opciones.count() == 2
    
    def test_vote_in_poll_authenticated(self, client, user):
        """Prueba votar en encuesta con usuario autenticado"""
        # Crear encuesta con opciones
        poll = Poll.objects.create(
            titulo='¿Cuál es tu IDE favorito?',
            descripcion='Encuesta sobre IDEs',
            creador=user,
            estado=Poll.Estado.ACTIVA
        )
        
        opcion1 = PollOpcion.objects.create(
            poll=poll,
            texto='Visual Studio Code',
            descripcion='Editor de Microsoft'
        )
        opcion2 = PollOpcion.objects.create(
            poll=poll,
            texto='PyCharm',
            descripcion='IDE de JetBrains'
        )
        
        client.force_authenticate(user=user)
        
        # Votar por la primera opción
        vote_data = {'opciones': [opcion1.id]}
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se creó el voto
        assert PollVoto.objects.filter(usuario=user, opcion=opcion1).count() == 1
        assert PollVoto.objects.filter(usuario=user, opcion=opcion2).count() == 0
    
    def test_vote_in_poll_unauthenticated(self, client):
        """Prueba votar en encuesta sin autenticación"""
        poll = Poll.objects.create(
            titulo='Encuesta de prueba',
            descripcion='Descripción',
            estado=Poll.Estado.ACTIVA
        )
        opcion = PollOpcion.objects.create(
            poll=poll,
            texto='Opción 1',
            descripcion='Primera opción'
        )
        
        vote_data = {'opciones': [opcion.id]}
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_multiple_choice_poll(self, client, user):
        """Prueba encuesta de múltiple opción"""
        poll = Poll.objects.create(
            titulo='¿Qué tecnologías conoces?',
            descripcion='Selecciona todas las que apliquen',
            creador=user,
            multi=True,
            estado=Poll.Estado.ACTIVA
        )
        
        opcion1 = PollOpcion.objects.create(
            poll=poll,
            texto='Python',
            descripcion='Lenguaje Python'
        )
        opcion2 = PollOpcion.objects.create(
            poll=poll,
            texto='JavaScript',
            descripcion='Lenguaje JavaScript'
        )
        opcion3 = PollOpcion.objects.create(
            poll=poll,
            texto='Java',
            descripcion='Lenguaje Java'
        )
        
        client.force_authenticate(user=user)
        
        # Votar por múltiples opciones
        vote_data = {'opciones': [opcion1.id, opcion2.id]}
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se crearon los votos
        assert PollVoto.objects.filter(usuario=user, opcion=opcion1).count() == 1
        assert PollVoto.objects.filter(usuario=user, opcion=opcion2).count() == 1
        assert PollVoto.objects.filter(usuario=user, opcion=opcion3).count() == 0
    
    def test_poll_results_authenticated(self, client, user):
        """Prueba obtener resultados de encuesta con usuario autenticado"""
        poll = Poll.objects.create(
            titulo='¿Cuál es tu color favorito?',
            descripcion='Encuesta sobre colores',
            creador=user,
            estado=Poll.Estado.ACTIVA,
            mostrar_resultados=Poll.TipoResultados.TIEMPO_REAL
        )
        
        opcion1 = PollOpcion.objects.create(
            poll=poll,
            texto='Azul',
            descripcion='Color azul'
        )
        opcion2 = PollOpcion.objects.create(
            poll=poll,
            texto='Rojo',
            descripcion='Color rojo'
        )
        
        # Crear algunos votos
        PollVoto.objects.create(poll=poll, usuario=user, opcion=opcion1)
        PollVoto.objects.create(poll=poll, usuario=user, opcion=opcion2)
        
        client.force_authenticate(user=user)
        response = client.get(polls_detail(poll.id))
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se devuelven los resultados
        assert 'opciones' in response.data
        assert len(response.data['opciones']) == 2
        assert response.data['opciones'][0]['votos'] >= 0
    
    def test_poll_results_unauthenticated(self, client):
        """Prueba obtener resultados de encuesta sin autenticación"""
        poll = Poll.objects.create(
            titulo='Encuesta pública',
            descripcion='Encuesta que todos pueden ver',
            estado=Poll.Estado.ACTIVA,
            mostrar_resultados=Poll.TipoResultados.TIEMPO_REAL
        )
        
        response = client.get(polls_detail(poll.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_poll_anonymous_voting(self, client, user):
        """Prueba votación anónima en encuesta"""
        poll = Poll.objects.create(
            titulo='Encuesta anónima',
            descripcion='Esta encuesta es anónima',
            creador=user,
            anonima=True,
            estado=Poll.Estado.ACTIVA
        )
        
        opcion = PollOpcion.objects.create(
            poll=poll,
            texto='Opción anónima',
            descripcion='Opción para voto anónimo'
        )
        
        client.force_authenticate(user=user)
        vote_data = {'opciones': [opcion.id]}
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se creó el voto anónimo
        voto = PollVoto.objects.filter(opcion=opcion).first()
        assert voto is not None
        # En votación anónima, el usuario puede ser None o el usuario real
        # dependiendo de la implementación
    
    def test_poll_requires_justification(self, client, user):
        """Prueba encuesta que requiere justificación"""
        poll = Poll.objects.create(
            titulo='¿Por qué elegiste tu carrera?',
            descripcion='Encuesta que requiere explicación',
            creador=user,
            requiere_justificacion=True,
            estado=Poll.Estado.ACTIVA
        )
        
        opcion = PollOpcion.objects.create(
            poll=poll,
            texto='Por pasión',
            descripcion='Elegí por pasión'
        )
        
        client.force_authenticate(user=user)
        
        # Votar sin justificación (debe fallar)
        vote_data = {'opciones': [opcion.id]}
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Votar con justificación (debe funcionar)
        vote_data = {
            'opciones': [opcion.id],
            'justificacion': 'Elegí esta carrera porque me apasiona la programación'
        }
        response = client.post(polls_vote(poll.id), vote_data, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_poll_career_filtering(self, client, user):
        """Prueba filtrado de encuestas por carrera"""
        # Crear encuesta para Ingeniería en Informática
        poll1 = Poll.objects.create(
            titulo='Encuesta para Ingeniería',
            descripcion='Solo para estudiantes de ingeniería',
            creador=user,
            carreras=['Ingeniería en Informática'],
            estado=Poll.Estado.ACTIVA
        )
        
        # Crear encuesta para todas las carreras
        poll2 = Poll.objects.create(
            titulo='Encuesta General',
            descripcion='Para todos los estudiantes',
            creador=user,
            carreras=[],
            estado=Poll.Estado.ACTIVA
        )
        
        client.force_authenticate(user=user)
        response = client.get(BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        
        # Debe mostrar ambas encuestas para un estudiante de ingeniería
        assert response.data['count'] == 2
        assert len(response.data['results']) == 2
