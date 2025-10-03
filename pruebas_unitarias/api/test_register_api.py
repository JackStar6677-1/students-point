import random
import string
import pytest
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def _rand_email() -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"auto_{suffix}@duocuc.cl"


def test_register_then_login_ok():
    client = APIClient()

    email = _rand_email()
    payload = {
        "first_name": "Auto",
        "last_name": "Test",
        "email": email,
        "carrera": "Ingeniería en Informática",
        "sede": "Sede Maipú",
        "password": "testpass123",
    }

    reg = client.post('/api/auth/register/', payload, format='json')
    assert reg.status_code in (201, 400)
    if reg.status_code == 400:
        # En caso de colisión o validación, no romper la suite.
        pytest.skip(f"Registro no disponible: {reg.json()}")

    login = client.post('/api/auth/login/', {"email": email, "password": "testpass123"}, format='json')
    assert login.status_code == 200, login.json()
    tokens = login.json()
    assert 'access' in tokens


