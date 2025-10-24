"""
Pruebas unitarias para la API de Portfolio (CV/Curriculum)
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from studentspoint.apps.portfolio.models import Logro, Proyecto, ExperienciaLaboral, Habilidad

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para portfolio"""
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


class TestPortfolioAPI:
    """Pruebas para la API de Portfolio"""
    
    def test_create_logro_authenticated(self, client, user):
        """Prueba crear logro con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Certificación Python',
            'descripcion': 'Certificación en programación Python',
            'tipo': 'certificacion',
            'estado': 'obtenido',
            'fecha_obtencion': '2024-01-15',
            'visible': True
        }
        response = client.post('/api/portfolio/logros/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Logro.objects.count() == 1
        assert Logro.objects.first().usuario == user
    
    def test_create_logro_unauthenticated(self, client):
        """Prueba crear logro sin autenticación"""
        data = {
            'titulo': 'Certificación Python',
            'descripcion': 'Certificación en programación Python'
        }
        response = client.post('/api/portfolio/logros/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_logros_authenticated(self, client, user):
        """Prueba listar logros del usuario autenticado"""
        # Crear algunos logros
        Logro.objects.create(
            usuario=user,
            titulo='Logro 1',
            descripcion='Descripción 1',
            tipo='certificacion',
            estado='obtenido'
        )
        Logro.objects.create(
            usuario=user,
            titulo='Logro 2',
            descripcion='Descripción 2',
            tipo='premio',
            estado='obtenido'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/portfolio/logros/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_create_proyecto_authenticated(self, client, user):
        """Prueba crear proyecto con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Sistema Web Django',
            'descripcion': 'Sistema web desarrollado en Django',
            'tecnologias': ['Python', 'Django', 'PostgreSQL'],
            'estado': 'completado',
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-03-01',
            'url_repositorio': 'https://github.com/user/proyecto',
            'visible': True
        }
        response = client.post('/api/portfolio/proyectos/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Proyecto.objects.count() == 1
        assert Proyecto.objects.first().usuario == user
    
    def test_create_experiencia_authenticated(self, client, user):
        """Prueba crear experiencia laboral con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'empresa': 'Empresa Tech',
            'cargo': 'Desarrollador Junior',
            'descripcion': 'Desarrollo de aplicaciones web',
            'tipo_contrato': 'practica',
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-06-01',
            'ubicacion': 'Santiago, Chile',
            'visible': True
        }
        response = client.post('/api/portfolio/experiencias/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ExperienciaLaboral.objects.count() == 1
        assert ExperienciaLaboral.objects.first().usuario == user
    
    def test_create_habilidad_authenticated(self, client, user):
        """Prueba crear habilidad con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'nombre': 'Python',
            'nivel': 4,
            'categoria': 'tecnica',
            'visible': True
        }
        response = client.post('/api/portfolio/habilidades/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Habilidad.objects.count() == 1
        assert Habilidad.objects.first().usuario == user
    
    def test_portfolio_completo_authenticated(self, client, user):
        """Prueba obtener portfolio completo del usuario"""
        # Crear datos de prueba
        Logro.objects.create(
            usuario=user,
            titulo='Certificación Python',
            descripcion='Certificación en Python',
            tipo='certificacion',
            estado='obtenido'
        )
        Proyecto.objects.create(
            usuario=user,
            titulo='Proyecto Django',
            descripcion='Sistema web en Django',
            tecnologias=['Python', 'Django'],
            estado='completado',
            fecha_inicio='2024-01-01'
        )
        ExperienciaLaboral.objects.create(
            usuario=user,
            empresa='Empresa Tech',
            cargo='Desarrollador',
            descripcion='Desarrollo web',
            tipo_contrato='practica',
            fecha_inicio='2024-01-01'
        )
        Habilidad.objects.create(
            usuario=user,
            nombre='Python',
            nivel=4,
            categoria='tecnica'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/portfolio/completo/')
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        assert 'perfil' in data
        assert 'logros' in data
        assert 'proyectos' in data
        assert 'experiencias' in data
        assert 'habilidades' in data
        assert len(data['logros']) == 1
        assert len(data['proyectos']) == 1
        assert len(data['experiencias']) == 1
        assert len(data['habilidades']) == 1
    
    def test_portfolio_completo_unauthenticated(self, client):
        """Prueba obtener portfolio completo sin autenticación"""
        response = client.get('/api/portfolio/completo/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_logro_owner(self, client, user):
        """Prueba actualizar logro siendo el propietario"""
        logro = Logro.objects.create(
            usuario=user,
            titulo='Logro Original',
            descripcion='Descripción original',
            tipo='certificacion',
            estado='obtenido'
        )
        
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Logro Actualizado',
            'descripcion': 'Descripción actualizada'
        }
        response = client.patch(f'/api/portfolio/logros/{logro.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        
        logro.refresh_from_db()
        assert logro.titulo == 'Logro Actualizado'
        assert logro.descripcion == 'Descripción actualizada'
    
    def test_delete_logro_owner(self, client, user):
        """Prueba eliminar logro siendo el propietario"""
        logro = Logro.objects.create(
            usuario=user,
            titulo='Logro a Eliminar',
            descripcion='Este logro será eliminado',
            tipo='certificacion',
            estado='obtenido'
        )
        
        client.force_authenticate(user=user)
        response = client.delete(f'/api/portfolio/logros/{logro.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Logro.objects.count() == 0
    
    def test_portfolio_visibility_filter(self, client, user):
        """Prueba que solo se muestren elementos visibles en el portfolio"""
        # Crear logros visibles y no visibles
        Logro.objects.create(
            usuario=user,
            titulo='Logro Visible',
            descripcion='Este es visible',
            tipo='certificacion',
            estado='obtenido',
            visible=True
        )
        Logro.objects.create(
            usuario=user,
            titulo='Logro Oculto',
            descripcion='Este está oculto',
            tipo='certificacion',
            estado='obtenido',
            visible=False
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/portfolio/completo/')
        assert response.status_code == status.HTTP_200_OK
        
        logros = response.data['logros']
        assert len(logros) == 1
        assert logros[0]['titulo'] == 'Logro Visible'
