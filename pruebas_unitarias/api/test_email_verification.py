"""
Pruebas unitarias para verificación de email
"""
import pytest
from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class EmailVerificationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'career': 'Ingeniería en Informática',
            'semestre': 3
        }
        
    def test_registration_sends_verification_email(self):
        """Prueba que el registro envía email de verificación"""
        # Limpiar bandeja de salida
        mail.outbox = []
        
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se envió un email
        self.assertEqual(len(mail.outbox), 1)
        
        # Verificar contenido del email
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user_data['email']])
        self.assertIn('verificación', email.subject.lower())
        
    def test_email_verification_code_format(self):
        """Prueba que el código de verificación tiene el formato correcto"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user.email_verification_code)
        self.assertEqual(len(user.email_verification_code), 6)
        self.assertTrue(user.email_verification_code.isdigit())
        
    def test_verify_email_with_valid_code(self):
        """Prueba verificar email con código válido"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        
        verification_data = {
            'email': user.email,
            'code': user.email_verification_code
        }
        
        response = self.client.post('/api/auth/verificar-email/', verification_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user.refresh_from_db()
        self.assertTrue(user.is_email_verified)
        
    def test_verify_email_with_invalid_code(self):
        """Prueba verificar email con código inválido"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        
        verification_data = {
            'email': user.email,
            'code': '000000'  # Código inválido
        }
        
        response = self.client.post('/api/auth/verificar-email/', verification_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        user.refresh_from_db()
        self.assertFalse(user.is_email_verified)
        
    def test_resend_verification_code(self):
        """Prueba reenviar código de verificación"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        
        # Limpiar bandeja de salida
        mail.outbox = []
        
        resend_data = {'email': user.email}
        response = self.client.post('/api/auth/reenviar-codigo/', resend_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se envió un nuevo email
        self.assertEqual(len(mail.outbox), 1)
        
    def test_verification_code_expiration(self):
        """Prueba expiración del código de verificación"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        
        # Simular código expirado (más de 24 horas)
        from datetime import datetime, timedelta
        user.email_verification_sent_at = datetime.now() - timedelta(hours=25)
        user.save()
        
        verification_data = {
            'email': user.email,
            'code': user.email_verification_code
        }
        
        response = self.client.post('/api/auth/verificar-email/', verification_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_unverified_user_cannot_login(self):
        """Prueba que usuario no verificado no puede hacer login"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.assertFalse(user.is_email_verified)
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('verificar', response.data.get('error', '').lower())
        
    def test_verified_user_can_login(self):
        """Prueba que usuario verificado puede hacer login"""
        response = self.client.post('/api/auth/register/', self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        
        # Verificar email
        user.is_email_verified = True
        user.save()
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
