"""Tests para el endpoint de portafolio."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class PortfolioTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="p@duocuc.cl", password="pass", name="P", career="Ing")

    def test_descarga_pdf(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get(reverse("portfolio"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.content.startswith(b"%PDF"))
