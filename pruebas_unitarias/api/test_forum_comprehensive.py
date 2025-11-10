"""
Pruebas completas para los endpoints del foro
Incluye pruebas para posts, comentarios, votos, reportes y moderación
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestForumPosts:
    """Pruebas para la creación y gestión de posts"""
    
    def test_create_post_requires_authentication(self):
        """Verifica que crear un post requiere autenticación"""
        from studentspoint.apps.forum.models import Foro
        
        # Crear un foro
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test Description',
            sede_duoc='Maipú'
        )
        
        client = APIClient()
        
        # Intentar crear post sin autenticación
        response = client.post('/api/forum/posts/', {
            'foro': foro.id,
            'titulo': 'Test Post',
            'contenido': 'Test Content'
        }, format='json')
        
        assert response.status_code in (401, 403)
    
    def test_create_post_success(self):
        """Verifica que un usuario autenticado puede crear posts"""
        from studentspoint.apps.forum.models import Foro, Post
        
        # Crear usuario y autenticarse
        user = User.objects.create_user(
            email='poster@duocuc.cl',
            password='testpass123',
            name='Test Poster',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'poster@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Crear foro
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test Description',
            sede_duoc='Maipú'
        )
        
        # Contar posts antes
        posts_before = Post.objects.count()
        
        # Crear post
        response = client.post('/api/forum/posts/', {
            'foro': foro.id,
            'titulo': 'Mi Primer Post',
            'contenido': 'Este es el contenido de mi post de prueba'
        }, format='json')
        
        assert response.status_code in (200, 201)
        
        # Verificar que se creó el post
        posts_after = Post.objects.count()
        assert posts_after == posts_before + 1
        
        # Verificar detalles del post
        post = Post.objects.latest('created_at')
        assert post.autor == user
        assert post.titulo == 'Mi Primer Post'
        assert post.foro == foro
    
    def test_list_posts_public_access(self):
        """Verifica que listar posts es público"""
        client = APIClient()
        
        # Intentar listar posts sin autenticación
        response = client.get('/api/forum/posts/')
        
        assert response.status_code == 200
    
    def test_vote_post_requires_authentication(self):
        """Verifica que votar un post requiere autenticación"""
        from studentspoint.apps.forum.models import Foro, Post
        
        # Crear usuario y post
        user = User.objects.create_user(
            email='author@duocuc.cl',
            password='testpass123',
            name='Author',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test',
            sede_duoc='Maipú'
        )
        
        post = Post.objects.create(
            foro=foro,
            autor=user,
            titulo='Test Post',
            contenido='Content'
        )
        
        client = APIClient()
        
        # Intentar votar sin autenticación
        response = client.post(f'/api/forum/posts/{post.id}/vote/', {
            'vote_type': 'upvote'
        }, format='json')
        
        assert response.status_code in (401, 403)


class TestForumComments:
    """Pruebas para comentarios en posts"""
    
    def test_create_comment_requires_authentication(self):
        """Verifica que crear comentarios requiere autenticación"""
        from studentspoint.apps.forum.models import Foro, Post
        
        # Crear usuario y post
        user = User.objects.create_user(
            email='postauthor@duocuc.cl',
            password='testpass123',
            name='Post Author',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test',
            sede_duoc='Maipú'
        )
        
        post = Post.objects.create(
            foro=foro,
            autor=user,
            titulo='Test Post',
            contenido='Content'
        )
        
        client = APIClient()
        
        # Intentar comentar sin autenticación
        response = client.post(f'/api/forum/posts/{post.id}/comments/', {
            'contenido': 'Test Comment'
        }, format='json')
        
        assert response.status_code in (401, 403)
    
    def test_create_comment_success(self):
        """Verifica que un usuario autenticado puede comentar"""
        from studentspoint.apps.forum.models import Foro, Post, Comentario
        
        # Crear usuario autor del post
        author = User.objects.create_user(
            email='postauthor2@duocuc.cl',
            password='testpass123',
            name='Post Author',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        # Crear usuario comentarista
        commenter = User.objects.create_user(
            email='commenter@duocuc.cl',
            password='testpass123',
            name='Commenter',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        # Crear foro y post
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test',
            sede_duoc='Maipú'
        )
        
        post = Post.objects.create(
            foro=foro,
            autor=author,
            titulo='Test Post',
            contenido='Content'
        )
        
        # Autenticarse como comentarista
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'commenter@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Contar comentarios antes
        comments_before = Comentario.objects.count()
        
        # Crear comentario
        response = client.post(f'/api/forum/posts/{post.id}/comments/', {
            'contenido': 'Este es mi comentario de prueba'
        }, format='json')
        
        assert response.status_code in (200, 201)
        
        # Verificar que se creó el comentario
        comments_after = Comentario.objects.count()
        assert comments_after == comments_before + 1
        
        # Verificar detalles del comentario
        comment = Comentario.objects.latest('created_at')
        assert comment.autor == commenter
        assert comment.post == post
        assert 'prueba' in comment.contenido.lower()


class TestForumReports:
    """Pruebas para el sistema de reportes"""
    
    def test_report_post_requires_authentication(self):
        """Verifica que reportar contenido requiere autenticación"""
        from studentspoint.apps.forum.models import Foro, Post
        
        # Crear usuario y post
        user = User.objects.create_user(
            email='reported@duocuc.cl',
            password='testpass123',
            name='Reported User',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test',
            sede_duoc='Maipú'
        )
        
        post = Post.objects.create(
            foro=foro,
            autor=user,
            titulo='Test Post',
            contenido='Content'
        )
        
        client = APIClient()
        
        # Intentar reportar sin autenticación
        response = client.post(f'/api/forum/posts/{post.id}/report/', {
            'razon': 'spam'
        }, format='json')
        
        assert response.status_code in (401, 403)


class TestForumModeration:
    """Pruebas para funcionalidades de moderación"""
    
    def test_moderation_requires_moderator_role(self):
        """Verifica que las acciones de moderación requieren rol de moderador"""
        from studentspoint.apps.forum.models import Foro, Post
        
        # Crear usuario normal (no moderador)
        normal_user = User.objects.create_user(
            email='normal@duocuc.cl',
            password='testpass123',
            name='Normal User',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True,
            role='estudiante'
        )
        
        # Crear otro usuario y su post
        author = User.objects.create_user(
            email='author2@duocuc.cl',
            password='testpass123',
            name='Author',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        foro = Foro.objects.create(
            nombre='Test Forum',
            descripcion='Test',
            sede_duoc='Maipú'
        )
        
        post = Post.objects.create(
            foro=foro,
            autor=author,
            titulo='Test Post',
            contenido='Content'
        )
        
        # Autenticarse como usuario normal
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'normal@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Intentar eliminar post (acción de moderación)
        response = client.delete(f'/api/forum/posts/{post.id}/')
        
        # Debería ser denegado (403) o el post no debería pertenecer al usuario
        assert response.status_code in (403, 404)

