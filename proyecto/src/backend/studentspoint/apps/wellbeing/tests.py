"""Tests para la API de bienestar."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import BienestarItem

User = get_user_model()


class BienestarAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="b@duocuc.cl", password="pass", name="B", career="c")

    def test_listar_por_carrera(self):
        BienestarItem.objects.create(
            carrera="Informatica",
            tipo=BienestarItem.Tipos.KINE,
            titulo="Estiramientos",
            contenido_md="**Mover**",
        )
        self.client.force_authenticate(self.user)
        url = reverse("bienestar")
        resp = self.client.get(url, {"carrera": "Informatica"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["count"], 1)
