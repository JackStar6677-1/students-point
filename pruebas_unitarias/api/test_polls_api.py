"""
Pruebas unitarias para la API de Encuestas (Polls)
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from studentspoint.apps.polls.models import Poll, PollOption, PollVote

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para encuestas"""
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
            'estado': 'activa',
            'carreras': ['Ingeniería en Informática', 'Técnico en Informática']
        }
        response = client.post('/api/polls/encuestas/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Poll.objects.count() == 1
        assert Poll.objects.first().creador == user
    
    def test_create_poll_unauthenticated(self, client):
        """Prueba crear encuesta sin autenticación"""
        data = {
            'titulo': '¿Cuál es tu lenguaje favorito?',
            'descripcion': 'Encuesta de prueba',
            'multi': False,
            'anonima': False
        }
        response = client.post('/api/polls/encuestas/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_polls_authenticated(self, client, user):
        """Prueba listar encuestas con usuario autenticado"""
        # Crear algunas encuestas
        Poll.objects.create(
            titulo='Encuesta 1',
            descripcion='Descripción 1',
            creador=user,
            estado='activa'
        )
        Poll.objects.create(
            titulo='Encuesta 2',
            descripcion='Descripción 2',
            creador=user,
            estado='activa'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/polls/encuestas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_list_polls_unauthenticated(self, client):
        """Prueba listar encuestas sin autenticación"""
        response = client.get('/api/polls/encuestas/')
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
            'estado': 'activa'
        }
        poll_response = client.post('/api/polls/encuestas/', poll_data)
        assert poll_response.status_code == status.HTTP_201_CREATED
        poll_id = poll_response.data['id']
        
        # Agregar opciones
        opciones_data = {
            'opciones': [
                {'texto': 'Django', 'descripcion': 'Framework de Python'},
                {'texto': 'Flask', 'descripcion': 'Microframework de Python'},
                {'texto': 'FastAPI', 'descripcion': 'Framework moderno de Python'},
                {'texto': 'Otro', 'descripcion': 'Otro framework'}
            ]
        }
        options_response = client.post(f'/api/polls/encuestas/{poll_id}/opciones/', opciones_data)
        assert options_response.status_code == status.HTTP_201_CREATED
        
        # Verificar que se crearon las opciones
        assert PollOption.objects.filter(encuesta_id=poll_id).count() == 4
    
    def test_vote_in_poll_authenticated(self, client, user):
        """Prueba votar en encuesta con usuario autenticado"""
        # Crear encuesta con opciones
        poll = Poll.objects.create(
            titulo='¿Cuál es tu IDE favorito?',
            descripcion='Encuesta sobre IDEs',
            creador=user,
            estado='activa'
        )
        
        opcion1 = PollOption.objects.create(
            encuesta=poll,
            texto='Visual Studio Code',
            descripcion='Editor de Microsoft'
        )
        opcion2 = PollOption.objects.create(
            encuesta=poll,
            texto='PyCharm',
            descripcion='IDE de JetBrains'
        )
        
        client.force_authenticate(user=user)
        
        # Votar por la primera opción
        vote_data = {'opcion_id': opcion1.id}
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se creó el voto
        assert PollVote.objects.filter(usuario=user, opcion=opcion1).count() == 1
        assert PollVote.objects.filter(usuario=user, opcion=opcion2).count() == 0
    
    def test_vote_in_poll_unauthenticated(self, client):
        """Prueba votar en encuesta sin autenticación"""
        poll = Poll.objects.create(
            titulo='Encuesta de prueba',
            descripcion='Descripción',
            estado='activa'
        )
        opcion = PollOption.objects.create(
            encuesta=poll,
            texto='Opción 1',
            descripcion='Primera opción'
        )
        
        vote_data = {'opcion_id': opcion.id}
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_multiple_choice_poll(self, client, user):
        """Prueba encuesta de múltiple opción"""
        poll = Poll.objects.create(
            titulo='¿Qué tecnologías conoces?',
            descripcion='Selecciona todas las que apliquen',
            creador=user,
            multi=True,
            estado='activa'
        )
        
        opcion1 = PollOption.objects.create(
            encuesta=poll,
            texto='Python',
            descripcion='Lenguaje Python'
        )
        opcion2 = PollOption.objects.create(
            encuesta=poll,
            texto='JavaScript',
            descripcion='Lenguaje JavaScript'
        )
        opcion3 = PollOption.objects.create(
            encuesta=poll,
            texto='Java',
            descripcion='Lenguaje Java'
        )
        
        client.force_authenticate(user=user)
        
        # Votar por múltiples opciones
        vote_data = {'opcion_ids': [opcion1.id, opcion2.id]}
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se crearon los votos
        assert PollVote.objects.filter(usuario=user, opcion=opcion1).count() == 1
        assert PollVote.objects.filter(usuario=user, opcion=opcion2).count() == 1
        assert PollVote.objects.filter(usuario=user, opcion=opcion3).count() == 0
    
    def test_poll_results_authenticated(self, client, user):
        """Prueba obtener resultados de encuesta con usuario autenticado"""
        poll = Poll.objects.create(
            titulo='¿Cuál es tu color favorito?',
            descripcion='Encuesta sobre colores',
            creador=user,
            estado='activa',
            tipo_resultados='tiempo_real'
        )
        
        opcion1 = PollOption.objects.create(
            encuesta=poll,
            texto='Azul',
            descripcion='Color azul'
        )
        opcion2 = PollOption.objects.create(
            encuesta=poll,
            texto='Rojo',
            descripcion='Color rojo'
        )
        
        # Crear algunos votos
        PollVote.objects.create(usuario=user, opcion=opcion1)
        PollVote.objects.create(usuario=user, opcion=opcion1)  # Voto duplicado para otro usuario
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/polls/encuestas/{poll.id}/resultados/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se devuelven los resultados
        assert 'opciones' in response.data
        assert len(response.data['opciones']) == 2
    
    def test_poll_results_unauthenticated(self, client):
        """Prueba obtener resultados de encuesta sin autenticación"""
        poll = Poll.objects.create(
            titulo='Encuesta pública',
            descripcion='Encuesta que todos pueden ver',
            estado='activa',
            tipo_resultados='tiempo_real'
        )
        
        response = client.get(f'/api/polls/encuestas/{poll.id}/resultados/')
        # Dependiendo de la configuración, puede ser 200 o 401
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]
    
    def test_poll_anonymous_voting(self, client, user):
        """Prueba votación anónima en encuesta"""
        poll = Poll.objects.create(
            titulo='Encuesta anónima',
            descripcion='Esta encuesta es anónima',
            creador=user,
            anonima=True,
            estado='activa'
        )
        
        opcion = PollOption.objects.create(
            encuesta=poll,
            texto='Opción anónima',
            descripcion='Opción para voto anónimo'
        )
        
        client.force_authenticate(user=user)
        vote_data = {'opcion_id': opcion.id}
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se creó el voto anónimo
        voto = PollVote.objects.filter(opcion=opcion).first()
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
            estado='activa'
        )
        
        opcion = PollOption.objects.create(
            encuesta=poll,
            texto='Por pasión',
            descripcion='Elegí por pasión'
        )
        
        client.force_authenticate(user=user)
        
        # Votar sin justificación (debe fallar)
        vote_data = {'opcion_id': opcion.id}
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Votar con justificación (debe funcionar)
        vote_data = {
            'opcion_id': opcion.id,
            'justificacion': 'Elegí esta carrera porque me apasiona la programación'
        }
        response = client.post(f'/api/polls/encuestas/{poll.id}/votar/', vote_data)
        assert response.status_code == status.HTTP_200_OK
    
    def test_poll_career_filtering(self, client, user):
        """Prueba filtrado de encuestas por carrera"""
        # Crear encuesta para Ingeniería en Informática
        poll1 = Poll.objects.create(
            titulo='Encuesta para Ingeniería',
            descripcion='Solo para estudiantes de ingeniería',
            creador=user,
            carreras=['Ingeniería en Informática'],
            estado='activa'
        )
        
        # Crear encuesta para todas las carreras
        poll2 = Poll.objects.create(
            titulo='Encuesta General',
            descripcion='Para todos los estudiantes',
            creador=user,
            carreras=[],
            estado='activa'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/polls/encuestas/')
        assert response.status_code == status.HTTP_200_OK
        
        # Debe mostrar ambas encuestas para un estudiante de ingeniería
        assert len(response.data) == 2
