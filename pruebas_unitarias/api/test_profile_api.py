"""
Pruebas unitarias para la API de perfil de usuario
"""
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from studentspoint.apps.accounts.models import User

class ProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            career='Ingeniería en Informática',
            semestre=3,
            is_email_verified=True
        )
        self.client.force_authenticate(user=self.user)
        
    def test_get_user_profile(self):
        """Prueba obtener perfil de usuario"""
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)
        self.assertEqual(response.data['career'], self.user.career)
        
    def test_update_user_profile(self):
        """Prueba actualizar perfil de usuario"""
        update_data = {
            'name': 'Updated Name',
            'career': 'Ingeniería Civil',
            'semestre': 5
        }
        
        response = self.client.patch('/api/auth/me/update/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.career, 'Ingeniería Civil')
        self.assertEqual(self.user.semestre, 5)
        
    def test_update_profile_invalid_semestre(self):
        """Prueba actualizar perfil con semestre inválido"""
        update_data = {
            'semestre': 15  # Semestre inválido (fuera de rango)
        }
        
        response = self.client.patch('/api/auth/me/update/', update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_change_password(self):
        """Prueba cambiar contraseña"""
        change_password_data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456'
        }
        
        response = self.client.post('/api/auth/cambiar-password/', change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la contraseña cambió
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))
        
    def test_change_password_wrong_old_password(self):
        """Prueba cambiar contraseña con contraseña antigua incorrecta"""
        change_password_data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass456'
        }
        
        response = self.client.post('/api/auth/cambiar-password/', change_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_change_career(self):
        """Prueba cambiar carrera"""
        change_career_data = {
            'nueva_carrera': 'Ingeniería en Conectividad y Redes'
        }
        
        response = self.client.post('/api/auth/cambiar-carrera/', change_career_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.career, 'Ingeniería en Conectividad y Redes')
        
    def test_change_career_invalid(self):
        """Prueba cambiar a carrera no válida"""
        change_career_data = {
            'nueva_carrera': 'Carrera que no existe'
        }
        
        response = self.client.post('/api/auth/cambiar-carrera/', change_career_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_available_careers(self):
        """Prueba obtener lista de carreras disponibles"""
        response = self.client.get('/api/carreras/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        
    def test_unauthenticated_cannot_access_profile(self):
        """Prueba que usuario no autenticado no puede acceder al perfil"""
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_profile_picture_upload(self):
        """Prueba subir foto de perfil"""
        # Crear archivo de imagen falso
        from io import BytesIO
        from PIL import Image
        
        image = Image.new('RGB', (100, 100), color='red')
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        image_file.name = 'test.jpg'
        
        update_data = {
            'picture_file': image_file
        }
        
        response = self.client.patch('/api/auth/me/update/', update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.picture_file)
