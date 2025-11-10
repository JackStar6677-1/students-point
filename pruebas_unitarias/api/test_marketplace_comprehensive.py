"""
Pruebas completas para los endpoints del Marketplace
Incluye pruebas para productos, categorías, y gestión de listings
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestMarketplaceProducts:
    """Pruebas para la creación y gestión de productos"""
    
    def test_create_product_requires_authentication(self):
        """Verifica que crear un producto requiere autenticación"""
        client = APIClient()
        
        # Intentar crear producto sin autenticación
        response = client.post('/api/marketplace/products/', {
            'titulo': 'Test Product',
            'descripcion': 'Test Description',
            'precio': 1000,
            'categoria': 'libros'
        }, format='json')
        
        assert response.status_code in (401, 403)
    
    def test_create_product_success(self):
        """Verifica que un usuario autenticado puede crear productos"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear usuario y autenticarse
        user = User.objects.create_user(
            email='seller@duocuc.cl',
            password='testpass123',
            name='Test Seller',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'seller@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Contar productos antes
        products_before = Producto.objects.count()
        
        # Crear producto
        response = client.post('/api/marketplace/products/', {
            'titulo': 'Libro de Cálculo',
            'descripcion': 'Libro en excelente estado',
            'precio': 15000,
            'categoria': 'libros',
            'campus': 'Maipú'
        }, format='json')
        
        assert response.status_code in (200, 201)
        
        # Verificar que se creó el producto
        products_after = Producto.objects.count()
        assert products_after == products_before + 1
        
        # Verificar detalles del producto
        product = Producto.objects.latest('created_at')
        assert product.vendedor == user
        assert product.titulo == 'Libro de Cálculo'
        assert product.precio == 15000
    
    def test_list_products_public_access(self):
        """Verifica que listar productos es público"""
        client = APIClient()
        
        # Intentar listar productos sin autenticación
        response = client.get('/api/marketplace/products/')
        
        assert response.status_code == 200
    
    def test_update_own_product(self):
        """Verifica que un usuario puede actualizar sus propios productos"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear usuario y producto
        user = User.objects.create_user(
            email='owner@duocuc.cl',
            password='testpass123',
            name='Product Owner',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        product = Producto.objects.create(
            vendedor=user,
            titulo='Original Title',
            descripcion='Original Description',
            precio=10000,
            categoria='libros',
            campus='Maipú'
        )
        
        # Autenticarse
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'owner@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Actualizar producto
        response = client.patch(f'/api/marketplace/products/{product.id}/', {
            'titulo': 'Updated Title',
            'precio': 12000
        }, format='json')
        
        assert response.status_code == 200
        
        # Verificar que se actualizó
        product.refresh_from_db()
        assert product.titulo == 'Updated Title'
        assert product.precio == 12000
    
    def test_cannot_update_others_product(self):
        """Verifica que un usuario no puede actualizar productos de otros"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear dos usuarios
        owner = User.objects.create_user(
            email='productowner@duocuc.cl',
            password='testpass123',
            name='Product Owner',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        other_user = User.objects.create_user(
            email='otheruser@duocuc.cl',
            password='testpass123',
            name='Other User',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        # Crear producto del primer usuario
        product = Producto.objects.create(
            vendedor=owner,
            titulo='Original Title',
            descripcion='Original Description',
            precio=10000,
            categoria='libros',
            campus='Maipú'
        )
        
        # Autenticarse como el otro usuario
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'otheruser@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Intentar actualizar producto de otro usuario
        response = client.patch(f'/api/marketplace/products/{product.id}/', {
            'titulo': 'Hacked Title'
        }, format='json')
        
        assert response.status_code in (403, 404)
        
        # Verificar que no se actualizó
        product.refresh_from_db()
        assert product.titulo == 'Original Title'
    
    def test_delete_own_product(self):
        """Verifica que un usuario puede eliminar sus propios productos"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear usuario y producto
        user = User.objects.create_user(
            email='deleter@duocuc.cl',
            password='testpass123',
            name='Product Deleter',
            career='Ingeniería en Informática',
            semestre=1,
            is_email_verified=True
        )
        
        product = Producto.objects.create(
            vendedor=user,
            titulo='To Be Deleted',
            descripcion='Description',
            precio=10000,
            categoria='libros',
            campus='Maipú'
        )
        
        product_id = product.id
        
        # Autenticarse
        client = APIClient()
        login_response = client.post('/api/auth/login/', {
            'email': 'deleter@duocuc.cl',
            'password': 'testpass123'
        }, format='json')
        
        token = login_response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Eliminar producto
        response = client.delete(f'/api/marketplace/products/{product_id}/')
        
        assert response.status_code in (200, 204)
        
        # Verificar que se eliminó
        assert not Producto.objects.filter(id=product_id).exists()


class TestMarketplaceCategories:
    """Pruebas para filtrado por categorías"""
    
    def test_filter_products_by_category(self):
        """Verifica que se puede filtrar productos por categoría"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear usuario
        user = User.objects.create_user(
            email='categoryseller@duocuc.cl',
            password='testpass123',
            name='Category Seller',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        # Crear productos de diferentes categorías
        Producto.objects.create(
            vendedor=user,
            titulo='Libro 1',
            descripcion='Description',
            precio=10000,
            categoria='libros',
            campus='Maipú'
        )
        
        Producto.objects.create(
            vendedor=user,
            titulo='Laptop',
            descripcion='Description',
            precio=300000,
            categoria='electronica',
            campus='Maipú'
        )
        
        client = APIClient()
        
        # Filtrar por categoría libros
        response = client.get('/api/marketplace/products/?categoria=libros')
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que solo retorna productos de la categoría libros
        if isinstance(data, list):
            for product in data:
                assert product.get('categoria') == 'libros'
        elif isinstance(data, dict) and 'results' in data:
            for product in data['results']:
                assert product.get('categoria') == 'libros'


class TestMarketplaceSearch:
    """Pruebas para búsqueda de productos"""
    
    def test_search_products_by_title(self):
        """Verifica que se puede buscar productos por título"""
        from studentspoint.apps.marketplace.models import Producto
        
        # Crear usuario
        user = User.objects.create_user(
            email='searchseller@duocuc.cl',
            password='testpass123',
            name='Search Seller',
            career='Ingeniería en Informática',
            semestre=1
        )
        
        # Crear productos
        Producto.objects.create(
            vendedor=user,
            titulo='Cálculo para Ingenieros',
            descripcion='Libro excelente',
            precio=15000,
            categoria='libros',
            campus='Maipú'
        )
        
        Producto.objects.create(
            vendedor=user,
            titulo='Física Moderna',
            descripcion='Libro de física',
            precio=20000,
            categoria='libros',
            campus='Maipú'
        )
        
        client = APIClient()
        
        # Buscar por término
        response = client.get('/api/marketplace/products/?search=Cálculo')
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que retorna resultados
        if isinstance(data, list):
            assert len(data) >= 1
            assert any('Cálculo' in product.get('titulo', '') for product in data)
        elif isinstance(data, dict) and 'results' in data:
            assert len(data['results']) >= 1
            assert any('Cálculo' in product.get('titulo', '') for product in data['results'])

