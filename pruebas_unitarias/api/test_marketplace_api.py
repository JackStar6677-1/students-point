"""
Pruebas unitarias para la API de Marketplace (Productos)
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from studentspoint.apps.market.models import CategoriaProducto, Producto

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para marketplace"""
    return User.objects.create_user(
        email='vendedor@duocuc.cl',
        password='testpass123',
        name='Vendedor Test',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def categoria():
    """Categoría de producto de prueba"""
    return CategoriaProducto.objects.create(
        nombre='Electrónicos',
        descripcion='Dispositivos electrónicos y tecnología'
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestMarketplaceAPI:
    """Pruebas para la API de Marketplace"""
    
    def test_list_categorias_authenticated(self, client, user):
        """Prueba listar categorías con usuario autenticado"""
        CategoriaProducto.objects.create(
            nombre='Electrónicos',
            descripcion='Dispositivos electrónicos'
        )
        CategoriaProducto.objects.create(
            nombre='Libros',
            descripcion='Libros y material académico'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/marketplace/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_list_categorias_unauthenticated(self, client):
        """Prueba listar categorías sin autenticación"""
        response = client.get('/api/marketplace/categories/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_producto_authenticated(self, client, user, categoria):
        """Prueba crear producto con usuario autenticado"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Laptop Dell Inspiron',
            'descripcion': 'Laptop en excelente estado, ideal para programación',
            'categoria': categoria.id,
            'url_principal': 'https://yapo.cl/123456',
            'tipo_enlace': 'yapo',
            'precio': 500000,
            'moneda': 'CLP',
            'estado': 'publicado'
        }
        response = client.post('/api/marketplace/products/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Producto.objects.count() == 1
        assert Producto.objects.first().vendedor == user
    
    def test_create_producto_unauthenticated(self, client, categoria):
        """Prueba crear producto sin autenticación"""
        data = {
            'titulo': 'Laptop Dell Inspiron',
            'descripcion': 'Laptop en excelente estado',
            'categoria': categoria.id,
            'url_principal': 'https://yapo.cl/123456',
            'tipo_enlace': 'yapo',
            'precio': 500000
        }
        response = client.post('/api/marketplace/products/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_productos_authenticated(self, client, user, categoria):
        """Prueba listar productos con usuario autenticado"""
        # Crear algunos productos
        Producto.objects.create(
            vendedor=user,
            titulo='Producto 1',
            descripcion='Descripción 1',
            categoria=categoria,
            url_principal='https://yapo.cl/1',
            tipo_enlace='yapo',
            estado='publicado'
        )
        Producto.objects.create(
            vendedor=user,
            titulo='Producto 2',
            descripcion='Descripción 2',
            categoria=categoria,
            url_principal='https://yapo.cl/2',
            tipo_enlace='yapo',
            estado='publicado'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/marketplace/products/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_list_productos_unauthenticated(self, client):
        """Prueba listar productos sin autenticación"""
        response = client.get('/api/marketplace/products/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_producto_detail_authenticated(self, client, user, categoria):
        """Prueba obtener detalle de producto con usuario autenticado"""
        producto = Producto.objects.create(
            vendedor=user,
            titulo='Laptop Dell Inspiron',
            descripcion='Laptop en excelente estado',
            categoria=categoria,
            url_principal='https://yapo.cl/123456',
            tipo_enlace='yapo',
            estado='publicado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/marketplace/products/{producto.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['titulo'] == 'Laptop Dell Inspiron'
        assert response.data['vendedor'] == user.id
    
    def test_update_producto_owner(self, client, user, categoria):
        """Prueba actualizar producto siendo el propietario"""
        producto = Producto.objects.create(
            vendedor=user,
            titulo='Producto Original',
            descripcion='Descripción original',
            categoria=categoria,
            url_principal='https://yapo.cl/123456',
            tipo_enlace='yapo',
            estado='publicado'
        )
        
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Producto Actualizado',
            'descripcion': 'Descripción actualizada',
            'precio': 600000
        }
        response = client.patch(f'/api/marketplace/products/{producto.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        
        producto.refresh_from_db()
        assert producto.titulo == 'Producto Actualizado'
        assert producto.descripcion == 'Descripción actualizada'
        assert producto.precio == 600000
    
    def test_delete_producto_owner(self, client, user, categoria):
        """Prueba eliminar producto siendo el propietario"""
        producto = Producto.objects.create(
            vendedor=user,
            titulo='Producto a Eliminar',
            descripcion='Este producto será eliminado',
            categoria=categoria,
            url_principal='https://yapo.cl/123456',
            tipo_enlace='yapo',
            estado='publicado'
        )
        
        client.force_authenticate(user=user)
        response = client.delete(f'/api/marketplace/products/{producto.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Producto.objects.count() == 0
    
    def test_producto_estados_filter(self, client, user, categoria):
        """Prueba filtrado por estados de producto"""
        Producto.objects.create(
            vendedor=user,
            titulo='Producto Publicado',
            descripcion='Este está publicado',
            categoria=categoria,
            url_principal='https://yapo.cl/1',
            tipo_enlace='yapo',
            estado='publicado'
        )
        Producto.objects.create(
            vendedor=user,
            titulo='Producto Vendido',
            descripcion='Este ya se vendió',
            categoria=categoria,
            url_principal='https://yapo.cl/2',
            tipo_enlace='yapo',
            estado='vendido'
        )
        Producto.objects.create(
            vendedor=user,
            titulo='Producto Borrador',
            descripcion='Este es borrador',
            categoria=categoria,
            url_principal='https://yapo.cl/3',
            tipo_enlace='yapo',
            estado='borrador'
        )
        
        client.force_authenticate(user=user)
        
        # Filtrar por estado publicado
        response = client.get('/api/marketplace/products/?estado=publicado')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Producto Publicado'
        
        # Filtrar por estado vendido
        response = client.get('/api/marketplace/products/?estado=vendido')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Producto Vendido'
    
    def test_producto_categoria_filter(self, client, user, categoria):
        """Prueba filtrado por categoría de producto"""
        categoria2 = CategoriaProducto.objects.create(
            nombre='Libros',
            descripcion='Libros y material académico'
        )
        
        Producto.objects.create(
            vendedor=user,
            titulo='Laptop',
            descripcion='Laptop',
            categoria=categoria,
            url_principal='https://yapo.cl/1',
            tipo_enlace='yapo',
            estado='publicado'
        )
        Producto.objects.create(
            vendedor=user,
            titulo='Libro Python',
            descripcion='Libro de Python',
            categoria=categoria2,
            url_principal='https://yapo.cl/2',
            tipo_enlace='yapo',
            estado='publicado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/marketplace/products/?categoria={categoria.id}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['titulo'] == 'Laptop'
    
    def test_producto_urls_adicionales(self, client, user, categoria):
        """Prueba crear producto con URLs adicionales"""
        client.force_authenticate(user=user)
        data = {
            'titulo': 'Laptop con Fotos',
            'descripcion': 'Laptop con múltiples fotos',
            'categoria': categoria.id,
            'url_principal': 'https://yapo.cl/123456',
            'tipo_enlace': 'yapo',
            'urls_adicionales': [
                'https://img1.com/foto1.jpg',
                'https://img2.com/foto2.jpg',
                'https://video.com/demo.mp4'
            ],
            'estado': 'publicado'
        }
        response = client.post('/api/marketplace/products/', data)
        assert response.status_code == status.HTTP_201_CREATED
        
        producto = Producto.objects.first()
        assert len(producto.urls_adicionales) == 3
        assert 'https://img1.com/foto1.jpg' in producto.urls_adicionales
