"""Tests para la app de cuentas."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestAuth(APITestCase):
    """Comprueba el flujo de login y el endpoint `/api/me`."""

    def setUp(self):
        self.User = get_user_model()

    def test_login_valido(self):
        user = self.User.objects.create_user(email="alumno@duocuc.cl", password="pass123")
        response = self.client.post("/api/auth/login", {"email": user.email, "password": "pass123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_dominio_invalido(self):
        response = self.client.post("/api/auth/login", {"email": "otro@ejemplo.com", "password": "x"})
        self.assertEqual(response.status_code, 400)

    def test_api_me(self):
        user = self.User.objects.create_user(email="test@duocuc.cl", password="pass123", name="Test")
        login = self.client.post("/api/auth/login", {"email": user.email, "password": "pass123"})
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], user.email)

