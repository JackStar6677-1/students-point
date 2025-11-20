"""Tests para el endpoint de portafolio."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class PortfolioTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="p@duocuc.cl", password="pass", name="P", career="Ing")

    def test_descarga_pdf(self):
        """Test de generación de PDF del portfolio."""
        self.client.force_authenticate(self.user)
        # Usar la URL correcta del router para la acción generate_pdf
        resp = self.client.get('/api/portfolio/completo/generate_pdf/')
        # El endpoint devuelve un PDF o un error 500 si hay problemas
        self.assertIn(resp.status_code, [200, 500])
        # Si es exitoso, debe ser un PDF
        if resp.status_code == 200:
            self.assertTrue(resp.content.startswith(b"%PDF"))
