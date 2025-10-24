import pytest
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def test_auth_me_requires_token():
    """Verifica que el endpoint /api/auth/me/ rechace peticiones sin token."""
    client = APIClient()
    resp = client.get('/api/auth/me/')
    assert resp.status_code in (401, 403)


