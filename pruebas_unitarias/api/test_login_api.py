import os
import pytest
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def test_auth_me_requires_token():
    client = APIClient()
    resp = client.get('/api/auth/me/')
    assert resp.status_code in (401, 403)


def test_login_ok_then_me():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Crear usuario de prueba
    email = 'admin@duocuc.cl'
    password = 'admin123'
    user = User.objects.create_user(
        email=email,
        password=password,
        name='Admin Test',
        career='Administración',
        role='admin_global'
    )

    client = APIClient()
    login = client.post('/api/auth/login/', {'email': email, 'password': password}, format='json')

    assert login.status_code == 200, f"Login falló: {login.json()}"
    data = login.json()
    assert 'access' in data

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {data["access"]}')
    me = client.get('/api/auth/me/')
    assert me.status_code == 200
    me_data = me.json()
    assert 'email' in me_data
    assert me_data['email'] == email


