"""Pruebas para la app de sedes."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Recorrido, RecorridoPaso, Sede


class CampusEndpointsTests(APITestCase):
    """Verifica la consulta de sedes y recorridos."""

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email="tester@duocuc.cl", password="pass123")
        login = self.client.post("/api/auth/login", {"email": user.email, "password": "pass123"})
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.sede = Sede.objects.create(
            slug="maipu",
            nombre="Sede Maipú",
            direccion="Calle 123",
            lat=-33.0,
            lng=-70.0,
        )
        self.recorrido = Recorrido.objects.create(sede=self.sede, titulo="Tour")
        RecorridoPaso.objects.create(
            recorrido=self.recorrido,
            orden=1,
            titulo="Inicio",
            descripcion="Entrada",
            imagen_url="http://example.com/1.jpg",
            lat=-33.1,
            lng=-70.1,
        )
        RecorridoPaso.objects.create(
            recorrido=self.recorrido,
            orden=2,
            titulo="Sala",
            descripcion="Sala de clases",
            imagen_url="http://example.com/2.jpg",
        )

    def test_list_sedes(self):
        response = self.client.get("/api/sedes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["slug"], "maipu")

    def test_recorridos_por_sede(self):
        response = self.client.get("/api/recorridos", {"sede": "maipu"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["orden"], 1)
        self.assertEqual(response.data["results"][1]["orden"], 2)
