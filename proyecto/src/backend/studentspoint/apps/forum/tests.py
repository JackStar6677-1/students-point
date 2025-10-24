"""Pruebas para la app de foros."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from studentspoint.apps.campuses.models import Sede

from .models import Foro, Post


class ForumEndpointTests(APITestCase):
    """Verifica creación de posts, moderación y acciones de usuarios."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="user@duocuc.cl", password="pass123")
        login = self.client.post("/api/auth/login", {"email": self.user.email, "password": "pass123"})
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        sede = Sede.objects.create(
            slug="central", nombre="Sede Central", direccion="Av 1", lat=0, lng=0
        )
        self.foro = Foro.objects.create(sede=sede, carrera="Ing", titulo="General", slug="general")

    def test_crear_post_valido(self):
        response = self.client.post(
            "/api/posts",
            {"foro": self.foro.id, "titulo": "Hola", "cuerpo": "Contenido"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["estado"], "publicado")
        self.assertEqual(Post.objects.count(), 1)

    def test_post_con_palabra_prohibida(self):
        response = self.client.post(
            "/api/posts",
            {"foro": self.foro.id, "titulo": "Hola", "cuerpo": "malo contenido"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["estado"], "revision")

    def test_votar_post(self):
        post = Post.objects.create(foro=self.foro, usuario=self.user, titulo="t", cuerpo="c")
        response = self.client.post(f"/api/posts/{post.id}/votar", {"valor": 1})
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.score, 1)

    def test_comentar_post(self):
        post = Post.objects.create(foro=self.foro, usuario=self.user, titulo="t", cuerpo="c")
        response = self.client.post(
            f"/api/posts/{post.id}/comentarios", {"cuerpo": "hola"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(post.comentarios.count(), 1)
