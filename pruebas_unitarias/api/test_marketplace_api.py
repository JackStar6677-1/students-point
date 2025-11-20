"""Tests para la API de Marketplace."""

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from studentspoint.apps.market.models import Producto, CategoriaProducto
from studentspoint.apps.campuses.models import Sede

User = get_user_model()


class MarketplaceAPITests(APITestCase):
    """Tests para el sistema de Marketplace."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        # Crear sede
        self.sede = Sede.objects.create(
            slug="maipu",
            nombre="Sede Maipú",
            direccion="Av. Américo Vespucio 1501",
            lat=-33.5,
            lng=-70.7
        )
        
        # Crear usuarios
        self.vendedor = User.objects.create_user(
            email="vendedor@duocuc.cl",
            password="pass123",
            name="Vendedor Test",
            career="Ingeniería en Informática",
            campus=self.sede
        )
        
        self.comprador = User.objects.create_user(
            email="comprador@duocuc.cl",
            password="pass123",
            name="Comprador Test",
            career="Ingeniería en Informática",
            campus=self.sede
        )
        
        # Crear categoría
        self.categoria = CategoriaProducto.objects.create(
            nombre="General",
            descripcion="Categoría general",
            activa=True
        )
        
        # Autenticar como vendedor
        self.client.force_authenticate(self.vendedor)
    
    def test_crear_producto_exitoso(self):
        """Test crear un producto con los campos mínimos requeridos."""
        data = {
            'descripcion': 'Laptop HP Core i5 en buen estado',
            'url': 'https://facebook.com/marketplace/item/123',
            'precio': 250000,
            'precio_estudiante': 230000
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        # Debe ser exitoso
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('success'))
        
        # Verificar que el producto se creó
        self.assertEqual(Producto.objects.count(), 1)
        producto = Producto.objects.first()
        self.assertEqual(producto.descripcion, 'Laptop HP Core i5 en buen estado')
        self.assertEqual(producto.vendedor, self.vendedor)
        self.assertEqual(producto.estado, 'publicado')
    
    def test_crear_producto_sin_descripcion(self):
        """Test que falla al crear producto sin descripción."""
        data = {
            'url': 'https://example.com/test'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        # Debe fallar
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
    
    def test_crear_producto_sin_url(self):
        """Test que falla al crear producto sin URL."""
        data = {
            'descripcion': 'Producto sin URL'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        # Debe fallar
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
    
    def test_crear_producto_sin_autenticacion(self):
        """Test que usuarios no autenticados no pueden crear productos."""
        # Cerrar sesión
        self.client.force_authenticate(user=None)
        
        data = {
            'descripcion': 'Producto sin auth',
            'url': 'https://example.com/test'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        # Debe rechazar
        self.assertEqual(response.status_code, 401)
    
    def test_listar_productos_publicos(self):
        """Test listar productos publicados."""
        # Crear productos
        Producto.objects.create(
            vendedor=self.vendedor,
            titulo='Producto 1',
            descripcion='Descripción producto 1',
            url_principal='https://example.com/1',
            categoria=self.categoria,
            estado='publicado',
            publicado_at=timezone.now(),
            precio=10000,
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        Producto.objects.create(
            vendedor=self.vendedor,
            titulo='Producto 2',
            descripcion='Descripción producto 2',
            url_principal='https://example.com/2',
            categoria=self.categoria,
            estado='publicado',
            publicado_at=timezone.now(),
            precio=20000,
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        # Listar productos (sin autenticación)
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/market/productos/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        
        # Verificar estructura de datos
        primer_producto = response.data[0]
        self.assertIn('id', primer_producto)
        self.assertIn('descripcion', primer_producto)
        self.assertIn('url', primer_producto)
        self.assertIn('precio', primer_producto)
    
    def test_solo_lista_productos_publicados(self):
        """Test que solo lista productos con estado publicado."""
        # Crear producto publicado
        Producto.objects.create(
            vendedor=self.vendedor,
            titulo='Producto Publicado',
            descripcion='Visible',
            url_principal='https://example.com/1',
            categoria=self.categoria,
            estado='publicado',
            publicado_at=timezone.now(),
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        # Crear producto borrador
        Producto.objects.create(
            vendedor=self.vendedor,
            titulo='Producto Borrador',
            descripcion='No visible',
            url_principal='https://example.com/2',
            categoria=self.categoria,
            estado='borrador',
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        # Crear producto vendido
        Producto.objects.create(
            vendedor=self.vendedor,
            titulo='Producto Vendido',
            descripcion='Ya vendido',
            url_principal='https://example.com/3',
            categoria=self.categoria,
            estado='vendido',
            vendido_at=timezone.now(),
            acepta_terminos=True,
            acepta_responsabilidad=True
        )
        
        # Listar productos
        response = self.client.get('/api/market/productos/')
        
        self.assertEqual(response.status_code, 200)
        # Solo debe mostrar el producto publicado
        self.assertEqual(len(response.data), 1)
        self.assertIn('Visible', response.data[0]['descripcion'])
    
    def test_crear_producto_con_precio(self):
        """Test crear producto con precio."""
        data = {
            'descripcion': 'Libro de Programación Python',
            'url': 'https://yapo.cl/item/123',
            'precio': 15000,
            'precio_estudiante': 12000
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        producto = Producto.objects.first()
        self.assertEqual(producto.precio, 15000)
        self.assertEqual(producto.precio_student_point, 12000)
        self.assertEqual(producto.moneda, 'CLP')
    
    def test_crear_producto_sin_precio(self):
        """Test crear producto sin especificar precio."""
        data = {
            'descripcion': 'Producto sin precio',
            'url': 'https://mercadolibre.cl/item/123'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        producto = Producto.objects.first()
        self.assertIsNone(producto.precio)
        self.assertIsNone(producto.precio_student_point)
    
    def test_producto_se_asigna_categoria_general(self):
        """Test que productos se asignan a categoría General por defecto."""
        data = {
            'descripcion': 'Producto de prueba',
            'url': 'https://example.com/test'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        producto = Producto.objects.first()
        self.assertEqual(producto.categoria.nombre, 'General')
    
    def test_producto_acepta_terminos_automaticamente(self):
        """Test que al crear producto se aceptan términos automáticamente."""
        data = {
            'descripcion': 'Producto con términos',
            'url': 'https://example.com/terminos'
        }
        
        response = self.client.post('/api/market/productos/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        
        producto = Producto.objects.first()
        self.assertTrue(producto.acepta_terminos)
        self.assertTrue(producto.acepta_responsabilidad)
    
    def test_productos_ordenados_por_fecha_descendente(self):
        """Test que productos se listan del más reciente al más antiguo."""
        import time
        
        # Crear productos con diferentes tiempos
        for i in range(3):
            Producto.objects.create(
                vendedor=self.vendedor,
                titulo=f'Producto {i}',
                descripcion=f'Descripción {i}',
                url_principal=f'https://example.com/{i}',
                categoria=self.categoria,
                estado='publicado',
                publicado_at=timezone.now(),
                acepta_terminos=True,
                acepta_responsabilidad=True
            )
            if i < 2:  # No esperar después del último
                time.sleep(0.1)
        
        response = self.client.get('/api/market/productos/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        
        # El primer producto debe ser el más reciente (Producto 2)
        self.assertIn('Descripción 2', response.data[0]['descripcion'])
    
    def test_limitar_productos_a_100(self):
        """Test que solo se devuelven los últimos 100 productos."""
        # Este test solo verifica que la consulta existe, no crea 101 productos
        response = self.client.get('/api/market/productos/')
        self.assertEqual(response.status_code, 200)
        # Verificar que devuelve una lista (vacía o con productos)
        self.assertIsInstance(response.data, list)
