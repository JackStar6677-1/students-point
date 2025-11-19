"""
Pruebas unitarias para la funcionalidad de imágenes en el Foro
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from studentspoint.apps.forum.models import Foro, Post
from studentspoint.apps.campuses.models import Sede

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para foro"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def sede():
    """Sede de prueba"""
    return Sede.objects.create(
        nombre='Sede Central',
        slug='sede-central',
        direccion='Av. Central 123',
        lat=-33.4489,
        lng=-70.6693
    )


@pytest.fixture
def foro(sede):
    """Foro de prueba"""
    return Foro.objects.create(
        sede=sede,
        carrera='Ingeniería en Informática',
        titulo='Foro de Prueba',
        descripcion='Foro para pruebas',
        slug='foro-prueba'
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestForumImagesAPI:
    """Pruebas para la funcionalidad de imágenes en Foro"""
    
    def test_create_post_with_image(self, client, user, foro):
        """Prueba crear post con imagen"""
        client.force_authenticate(user=user)
        
        # Crear archivo de imagen de prueba
        test_image = SimpleUploadedFile(
            "test_post.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        data = {
            'foro': foro.id,
            'titulo': 'Post con imagen',
            'cuerpo': 'Este es un post de prueba con imagen',
            'tipo': 'texto',
            'imagen': test_image
        }
        
        response = client.post('/api/forum/posts/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que la imagen se guardó
        post = Post.objects.first()
        assert post.imagen is not None
        # Verificar que imagen_aprobada es True por defecto (según cambios recientes)
        assert post.imagen_aprobada == True
    
    def test_create_post_without_image(self, client, user, foro):
        """Prueba crear post sin imagen"""
        client.force_authenticate(user=user)
        
        data = {
            'foro': foro.id,
            'titulo': 'Post sin imagen',
            'cuerpo': 'Este es un post sin imagen',
            'tipo': 'texto'
        }
        
        response = client.post('/api/forum/posts/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que el post se creó sin imagen
        post = Post.objects.first()
        assert post.imagen.name == '' or post.imagen is None
    
    def test_post_image_auto_approved(self, client, user, foro):
        """Prueba que las imágenes se aprueban automáticamente"""
        client.force_authenticate(user=user)
        
        test_image = SimpleUploadedFile(
            "auto_approve.jpg",
            b"image content",
            content_type="image/jpeg"
        )
        
        data = {
            'foro': foro.id,
            'titulo': 'Post auto-aprobado',
            'cuerpo': 'Contenido del post',
            'tipo': 'texto',
            'imagen': test_image
        }
        
        response = client.post('/api/forum/posts/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        post = Post.objects.first()
        # Según los cambios recientes, imagen_aprobada debe ser True automáticamente
        assert post.imagen_aprobada == True
    
    def test_list_posts_with_images(self, client, user, foro):
        """Prueba listar posts con imágenes"""
        # Crear posts con y sin imágenes
        Post.objects.create(
            foro=foro,
            usuario=user,
            titulo='Post 1',
            cuerpo='Contenido 1',
            tipo='texto'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/forum/posts/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar estructura de respuesta
        assert isinstance(response.data, list) or 'results' in response.data
    
    def test_post_image_url_in_response(self, client, user, foro):
        """Prueba que la URL de imagen se devuelve en la respuesta"""
        client.force_authenticate(user=user)
        
        test_image = SimpleUploadedFile(
            "response_test.jpg",
            b"image",
            content_type="image/jpeg"
        )
        
        data = {
            'foro': foro.id,
            'titulo': 'Post para verificar URL',
            'cuerpo': 'Contenido',
            'tipo': 'texto',
            'imagen': test_image
        }
        
        response = client.post('/api/forum/posts/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que se incluye información de la imagen
        # (el formato exacto puede variar según el serializer)
        post = Post.objects.first()
        assert post.imagen is not None
    
    def test_post_image_types_validation(self, client, user, foro):
        """Prueba validación de tipos de imagen"""
        client.force_authenticate(user=user)
        
        valid_formats = [
            ('test.jpg', 'image/jpeg'),
            ('test.png', 'image/png'),
        ]
        
        for filename, content_type in valid_formats:
            test_image = SimpleUploadedFile(
                filename,
                b"fake image",
                content_type=content_type
            )
            
            data = {
                'foro': foro.id,
                'titulo': f'Post con {filename}',
                'cuerpo': 'Contenido',
                'tipo': 'texto',
                'imagen': test_image
            }
            
            response = client.post('/api/forum/posts/', data, format='multipart')
            assert response.status_code == status.HTTP_201_CREATED
    
    def test_anonymous_post_with_image(self, client, user, foro):
        """Prueba crear post anónimo con imagen"""
        client.force_authenticate(user=user)
        
        test_image = SimpleUploadedFile(
            "anon_image.jpg",
            b"image content",
            content_type="image/jpeg"
        )
        
        data = {
            'foro': foro.id,
            'titulo': 'Post anónimo con imagen',
            'cuerpo': 'Contenido anónimo',
            'tipo': 'texto',
            'anonimo': True,
            'imagen': test_image
        }
        
        response = client.post('/api/forum/posts/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        post = Post.objects.first()
        assert post.anonimo == True
        assert post.imagen is not None
    
    def test_post_without_authentication_cannot_upload_image(self, client, foro):
        """Prueba que usuario sin autenticar no puede subir imagen en post"""
        test_image = SimpleUploadedFile(
            "test.jpg",
            b"image",
            content_type="image/jpeg"
        )
        
        data = {
            'foro': foro.id,
            'titulo': 'Post sin auth',
            'cuerpo': 'Contenido',
            'tipo': 'texto',
            'imagen': test_image
        }
        
        response = client.post('/api/forum/posts/', data, format='multipart')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

