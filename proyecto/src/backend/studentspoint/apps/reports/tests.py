"""Pruebas para la API de reportes."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from studentspoint.apps.campuses.models import Sede
from .models import Reporte

User = get_user_model()


class ReporteAPITests(APITestCase):
    def setUp(self):
        self.sede = Sede.objects.create(slug="plaza", nombre="Plaza", direccion="dir", lat=0, lng=0)
        self.user = User.objects.create_user(email="user@duocuc.cl", password="pass", name="User", career="c")
        self.mod = User.objects.create_user(
            email="mod@duocuc.cl", password="pass", name="Mod", career="c", role=User.Roles.MODERATOR
        )

    def test_crear_listar_y_actualizar_reporte(self):
        self.client.force_authenticate(self.user)
        url = reverse("reporte-list")
        resp = self.client.post(
            url,
            {
                "sede": self.sede.id,
                "categoria": "Iluminación",
                "descripcion": "Foco quemado",
                "lat": 1.0,
                "lng": -1.0,
                "media": [{"url": "http://example.com/img.jpg"}],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        rep_id = resp.data["id"]
        self.assertEqual(Reporte.objects.count(), 1)

        # Listar filtrando por sede
        resp = self.client.get(url, {"sede": self.sede.slug})
        self.assertEqual(resp.data["count"], 1)

        # Cambiar estado como moderador
        self.client.force_authenticate(self.mod)
        detail = reverse("reporte-detail", args=[rep_id])
        resp = self.client.patch(detail, {"estado": Reporte.Estados.REVISION})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["estado"], Reporte.Estados.REVISION)
