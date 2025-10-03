import pytest
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def _unwrap_list(data):
    """Soporta respuestas paginadas (DRF) o listas simples."""
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    return data


def test_list_campuses_ok():
    client = APIClient()
    resp = client.get('/api/campus/campuses/')
    assert resp.status_code == 200
    campuses = _unwrap_list(resp.json())
    assert isinstance(campuses, list)


def test_list_tours_and_steps_smoke():
    client = APIClient()
    # Si existen campus en base (populate), probar con id=1
    tours_resp = client.get('/api/campus/tours/', {'campus': 1})
    if tours_resp.status_code != 200:
        return
    tours = _unwrap_list(tours_resp.json())
    if not tours:
        return
    tour_id = tours[0]['id']
    steps_resp = client.get(f'/api/campus/tours/{tour_id}/steps/')
    assert steps_resp.status_code == 200
    steps = _unwrap_list(steps_resp.json())
    if steps:
        orders = [s.get('order', s.get('orden', 0)) for s in steps]
        assert orders == sorted(orders)


