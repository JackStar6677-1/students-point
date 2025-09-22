"""
Middleware personalizado para StudentsPoint
"""

from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware para deshabilitar CSRF en rutas de API
    """
    
    def process_request(self, request):
        # Deshabilitar CSRF para todas las rutas de API
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
            # También deshabilitar para el middleware de CSRF
            request.csrf_processing_done = True
        return None


class CustomCorsMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para CORS
    """
    
    def process_response(self, request, response):
        # Agregar headers CORS personalizados
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response