"""Tests para la API de cursos OTEC."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Curso

User = get_user_model()


class CursoAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u@duocuc.cl", password="pass", name="U", career="c")

    def test_crear_y_listar_vigentes(self):
        self.client.force_authenticate(self.user)
        url = reverse("curso-list")
        today = date.today()
        resp = self.client.post(
            url,
            {
                "titulo": "Curso 1",
                "descripcion": "Desc",
                "etiquetas": "python",
                "url": "http://curso.test",
                "fecha_inicio": today.isoformat(),
                "fecha_fin": (today + timedelta(days=1)).isoformat(),
                "visible": True,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)

        # crear curso expirado
        Curso.objects.create(
            autor=self.user,
            titulo="C2",
            descripcion="d",
            etiquetas="",
            url="http://x",
            fecha_inicio=today - timedelta(days=10),
            fecha_fin=today - timedelta(days=5),
            visible=True,
        )

        resp = self.client.get(url)
        self.assertEqual(resp.data["count"], 1)
