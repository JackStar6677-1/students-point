"""
Pruebas unitarias para la API del foro
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from studentspoint.apps.forum.models import Foro, Post, Comentario
from studentspoint.apps.accounts.models import User
from studentspoint.apps.campuses.models import Sede

User = get_user_model()

class ForumAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            career='Ingeniería en Informática'
        )
        
        # Crear sede para los foros
        self.sede = Sede.objects.create(
            nombre='Sede de Prueba',
            slug='sede-prueba',
            direccion='Dirección de prueba 123',
            lat=-33.4489,
            lng=-70.6693
        )
        
        # Crear foro
        self.foro = Foro.objects.create(
            sede=self.sede,
            carrera='Ingeniería en Informática',
            titulo='Foro de Prueba',
            descripcion='Foro para pruebas',
            slug='foro-prueba'
        )
        
    def test_list_foros_authenticated(self):
        """Prueba listar foros con usuario autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/forum/foros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
    def test_list_foros_unauthenticated(self):
        """Prueba listar foros sin autenticación"""
        response = self.client.get('/api/forum/foros/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_post_authenticated(self):
        """Prueba crear post con usuario autenticado"""
        self.client.force_authenticate(user=self.user)
        data = {
            'foro': self.foro.id,
            'titulo': 'Post de prueba',
            'cuerpo': 'Contenido del post de prueba',
            'tipo': 'texto'
        }
        response = self.client.post('/api/forum/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        
    def test_create_post_unauthenticated(self):
        """Prueba crear post sin autenticación"""
        data = {
            'foro': self.foro.id,
            'titulo': 'Post de prueba',
            'cuerpo': 'Contenido del post de prueba',
            'tipo': 'texto'
        }
        response = self.client.post('/api/forum/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_posts(self):
        """Prueba listar posts"""
        # Crear algunos posts
        post1 = Post.objects.create(
            foro=self.foro,
            usuario=self.user,
            titulo='Post 1',
            cuerpo='Contenido 1',
            tipo='texto'
        )
        post2 = Post.objects.create(
            foro=self.foro,
            usuario=self.user,
            titulo='Post 2',
            cuerpo='Contenido 2',
            tipo='texto'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/forum/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_post_content_censorship(self):
        """Prueba censura de contenido ofensivo"""
        self.client.force_authenticate(user=self.user)
        data = {
            'foro': self.foro.id,
            'titulo': 'Post con palabra ofensiva',
            'cuerpo': 'Este es un contenido con la palabra estúpido que debería ser censurada',
            'tipo': 'texto'
        }
        response = self.client.post('/api/forum/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el contenido fue censurado
        post = Post.objects.get(id=response.data['id'])
        self.assertIn('***', post.cuerpo)
        
    def test_anonymous_post(self):
        """Prueba crear post anónimo"""
        self.client.force_authenticate(user=self.user)
        data = {
            'foro': self.foro.id,
            'titulo': 'Post anónimo',
            'cuerpo': 'Contenido anónimo',
            'tipo': 'texto',
            'anonimo': True
        }
        response = self.client.post('/api/forum/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        post = Post.objects.get(id=response.data['id'])
        self.assertTrue(post.anonimo)
        
    def test_forum_permissions(self):
        """Prueba permisos de foro basados en carrera"""
        # Crear foro específico para una carrera
        foro_carrera = Foro.objects.create(
            sede=self.sede,
            carrera='Ingeniería en Informática',
            titulo='Foro de Ingeniería',
            descripcion='Solo para estudiantes de ingeniería',
            slug='foro-ingenieria',
            es_privado=True
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/forum/foros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el foro aparece en la lista
        foro_titles = [f.get('titulo', f.get('nombre', '')) for f in response.data]
        self.assertIn('Foro de Ingeniería', foro_titles)
        
    def test_post_voting(self):
        """Prueba sistema de votación de posts"""
        post = Post.objects.create(
            foro=self.foro,
            usuario=self.user,
            titulo='Post para votar',
            cuerpo='Contenido',
            tipo='texto'
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Votar positivo
        response = self.client.post(f'/api/forum/posts/{post.id}/vote/', {'vote': 'up'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el score aumentó
        post.refresh_from_db()
        self.assertEqual(post.score, 1)
        
        # Votar negativo
        response = self.client.post(f'/api/forum/posts/{post.id}/vote/', {'vote': 'down'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el score cambió
        post.refresh_from_db()
        self.assertEqual(post.score, -1)
