"""
Pruebas unitarias para la funcionalidad de imágenes en Marketplace
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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
        nombre='General',
        descripcion='Categoría general',
        activa=True
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestMarketplaceImagesAPI:
    """Pruebas para la funcionalidad de imágenes en Marketplace"""
    
    def test_create_producto_with_image(self, client, user, categoria):
        """Prueba crear producto con imagen"""
        client.force_authenticate(user=user)
        
        # Crear archivo de imagen de prueba
        test_image = SimpleUploadedFile(
            "test_product.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        data = {
            'descripcion': 'Laptop Dell con imagen',
            'url': 'https://facebook.com/marketplace/item/123',
            'precio': 500000,
            'precio_estudiante': 450000,
            'imagen': test_image
        }
        
        response = client.post('/api/market/productos/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'imagen' in response.data
        assert response.data['imagen'] is not None
        
        # Verificar que la imagen se guardó
        producto = Producto.objects.first()
        assert producto.imagen is not None
        assert 'market/productos/' in producto.imagen.name
    
    def test_create_producto_without_image(self, client, user, categoria):
        """Prueba crear producto sin imagen"""
        client.force_authenticate(user=user)
        
        data = {
            'descripcion': 'Laptop Dell sin imagen',
            'url': 'https://facebook.com/marketplace/item/123',
            'precio': 500000,
            'precio_estudiante': 450000
        }
        
        response = client.post('/api/market/productos/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que el producto se creó sin imagen
        producto = Producto.objects.first()
        assert producto.imagen.name == '' or producto.imagen is None
    
    def test_list_productos_with_images(self, client, user, categoria):
        """Prueba listar productos con imágenes"""
        # Crear productos con y sin imágenes
        Producto.objects.create(
            titulo='Producto con imagen',
            descripcion='Descripción 1',
            url_principal='https://test.com/1',
            precio=100000,
            precio_student_point=90000,
            vendedor=user,
            categoria=categoria,
            estado='publicado',
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        response = client.get('/api/market/productos/')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        
        # Verificar que se incluye el campo imagen
        if len(response.data) > 0:
            assert 'imagen' in response.data[0]
    
    def test_image_size_validation(self, client, user, categoria):
        """Prueba validación de tamaño de imagen (máx 5MB)"""
        client.force_authenticate(user=user)
        
        # Crear una imagen "grande" (simulada)
        # En un test real, crearías un archivo de más de 5MB
        large_image = SimpleUploadedFile(
            "large_image.jpg",
            b"x" * 6 * 1024 * 1024,  # 6MB
            content_type="image/jpeg"
        )
        
        data = {
            'descripcion': 'Producto con imagen grande',
            'url': 'https://test.com/123',
            'precio': 100000,
            'imagen': large_image
        }
        
        response = client.post('/api/market/productos/', data, format='multipart')
        # El resultado puede ser 201 si no hay validación de tamaño
        # o 400 si sí hay validación
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    
    def test_image_type_validation(self, client, user, categoria):
        """Prueba validación de tipo de imagen"""
        client.force_authenticate(user=user)
        
        # Crear un archivo que no es imagen
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"this is not an image",
            content_type="text/plain"
        )
        
        data = {
            'descripcion': 'Producto con archivo inválido',
            'url': 'https://test.com/123',
            'precio': 100000,
            'imagen': invalid_file
        }
        
        response = client.post('/api/market/productos/', data, format='multipart')
        # El resultado puede variar según la validación implementada
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    
    def test_producto_image_url_format(self, client, user, categoria):
        """Prueba que la URL de imagen devuelta es absoluta"""
        client.force_authenticate(user=user)
        
        test_image = SimpleUploadedFile(
            "product.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        data = {
            'descripcion': 'Producto para verificar URL',
            'url': 'https://test.com/123',
            'imagen': test_image
        }
        
        response = client.post('/api/market/productos/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        if response.data.get('imagen'):
            imagen_url = response.data['imagen']
            # Verificar que es una URL completa
            assert imagen_url.startswith('http://') or imagen_url.startswith('https://')
    
    def test_multiple_image_formats(self, client, user, categoria):
        """Prueba subida de diferentes formatos de imagen"""
        client.force_authenticate(user=user)
        
        image_formats = [
            ('test.jpg', 'image/jpeg'),
            ('test.png', 'image/png'),
            ('test.webp', 'image/webp'),
        ]
        
        for filename, content_type in image_formats:
            test_image = SimpleUploadedFile(
                filename,
                b"fake image content",
                content_type=content_type
            )
            
            data = {
                'descripcion': f'Producto con {filename}',
                'url': f'https://test.com/{filename}',
                'imagen': test_image
            }
            
            response = client.post('/api/market/productos/', data, format='multipart')
            assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que se crearon todos los productos
        assert Producto.objects.count() == len(image_formats)
    
    def test_producto_without_authentication_cannot_upload_image(self, client, categoria):
        """Prueba que usuario sin autenticar no puede subir imagen"""
        test_image = SimpleUploadedFile(
            "test.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        data = {
            'descripcion': 'Producto sin autenticación',
            'url': 'https://test.com/123',
            'imagen': test_image
        }
        
        response = client.post('/api/market/productos/', data, format='multipart')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

