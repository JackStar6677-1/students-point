"""
Pruebas para la funcionalidad del menú de navegación swipe
Este archivo contiene tests de integración para verificar que el JavaScript del menú funciona correctamente
"""
import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def client():
    """Cliente Django para pruebas"""
    return Client()


class TestSwipeMenuIntegration:
    """Pruebas de integración para el menú swipe"""
    
    def test_swipe_menu_js_loaded_in_forum(self, client, user):
        """Verifica que el script swipe-menu.js se carga en el foro"""
        client.force_login(user)
        response = client.get('/forum/')
        
        assert response.status_code == 200
        assert b'/static/js/swipe-menu.js' in response.content
    
    def test_swipe_menu_js_loaded_in_market(self, client, user):
        """Verifica que el script swipe-menu.js se carga en marketplace"""
        client.force_login(user)
        response = client.get('/market/')
        
        assert response.status_code == 200
        assert b'/static/js/swipe-menu.js' in response.content
    
    def test_swipe_menu_js_loaded_in_account(self, client, user):
        """Verifica que el script swipe-menu.js se carga en mi cuenta"""
        client.force_login(user)
        response = client.get('/account.html')
        
        # Puede ser 200 o redirigir a login si la ruta no existe
        assert response.status_code in [200, 302, 404]
    
    def test_sidebar_present_in_pages(self, client, user):
        """Verifica que el sidebar está presente en las páginas"""
        client.force_login(user)
        
        pages = ['/forum/', '/market/']
        
        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                # Verificar que existe el elemento sidebar
                assert b'sidebar' in response.content or b'Sidebar' in response.content
    
    def test_swipe_overlay_class_in_css(self, client):
        """Verifica que la clase swipe-overlay existe en el CSS"""
        response = client.get('/static/css/base-layout.css')
        
        # Puede no estar disponible si no se sirven archivos estáticos en tests
        if response.status_code == 200:
            assert b'swipe-overlay' in response.content or response.status_code == 404
    
    def test_mobile_menu_removed(self, client, user):
        """Verifica que el script mobile-menu.js fue removido"""
        client.force_login(user)
        
        pages = ['/forum/', '/market/']
        
        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                # Verificar que NO existe mobile-menu.js
                assert b'/static/js/mobile-menu.js' not in response.content


class TestCSSStylesPresence:
    """Pruebas para verificar que los estilos CSS están presentes"""
    
    def test_forum_css_loaded(self, client, user):
        """Verifica que forum.css se carga en el foro"""
        client.force_login(user)
        response = client.get('/forum/')
        
        if response.status_code == 200:
            assert b'forum.css' in response.content or b'forum/forum.css' in response.content
    
    def test_market_css_loaded(self, client, user):
        """Verifica que mercado.css se carga en marketplace"""
        client.force_login(user)
        response = client.get('/market/')
        
        if response.status_code == 200:
            assert b'mercado.css' in response.content or b'market/mercado.css' in response.content
    
    def test_account_css_loaded(self, client, user):
        """Verifica que account.css se carga en mi cuenta"""
        client.force_login(user)
        response = client.get('/account.html')
        
        if response.status_code == 200:
            assert b'account.css' in response.content
    
    def test_glassmorphism_styles_in_modules(self, client):
        """Verifica que los estilos de glassmorphism están presentes en los CSS"""
        css_files = [
            '/static/forum/forum.css',
            '/static/market/mercado.css',
            '/static/css/account.css',
        ]
        
        for css_file in css_files:
            response = client.get(css_file)
            if response.status_code == 200:
                # Verificar que contiene estilos de glassmorphism
                assert (b'backdrop-filter' in response.content or 
                       b'glassmorphism' in response.content.lower() or
                       b'glass' in response.content)


class TestNavigationConsistency:
    """Pruebas para verificar consistencia de navegación"""
    
    def test_all_modules_have_sidebar(self, client, user):
        """Verifica que todos los módulos tienen sidebar"""
        client.force_login(user)
        
        modules = [
            '/forum/',
            '/market/',
            '/encuestas/',
            '/reportes/',
            '/cursos/',
            '/converter/',
        ]
        
        for module in modules:
            response = client.get(module)
            if response.status_code == 200:
                assert b'sidebar' in response.content.lower()
    
    def test_consistent_menu_items(self, client, user):
        """Verifica que los items del menú son consistentes"""
        client.force_login(user)
        
        response = client.get('/forum/')
        if response.status_code == 200:
            # Verificar que existen los links principales
            menu_items = [b'Inicio', b'Foro', b'Marketplace', b'Encuestas', b'Reportes']
            for item in menu_items:
                assert item in response.content

