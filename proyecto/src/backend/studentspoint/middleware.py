"""
Middleware personalizado para StudentsPoint
"""
import logging
import time
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('studentspoint')


class QueryCountDebugMiddleware(MiddlewareMixin):
    """
    Middleware que detecta queries N+1 y reporta queries excesivas
    Solo activo en DEBUG=True
    """
    
    def process_request(self, request):
        if settings.DEBUG:
            # Guardar el número inicial de queries
            request._query_count_start = len(connection.queries)
            request._query_time_start = time.time()
    
    def process_response(self, request, response):
        if settings.DEBUG and hasattr(request, '_query_count_start'):
            # Calcular queries ejecutadas
            query_count = len(connection.queries) - request._query_count_start
            query_time = time.time() - request._query_time_start
            
            # Umbral de advertencia
            if query_count > 20:
                logger.warning(
                    f"N+1 Query Alert: {request.path} ejecuto {query_count} queries "
                    f"en {query_time:.2f}s"
                )
                
                # Loggear las queries para debugging
                if query_count > 50:
                    logger.error(
                        f"CRITICO: {request.path} ejecuto {query_count} queries! "
                        f"Revisar select_related/prefetch_related"
                    )
            
            # Agregar header con info de queries (útil para desarrollo)
            response['X-DB-Query-Count'] = str(query_count)
            response['X-DB-Query-Time'] = f"{query_time:.3f}s"
        
        return response


class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware para deshabilitar CSRF en endpoints API específicos
    Solo para desarrollo
    """
    
    def process_request(self, request):
        # Deshabilitar CSRF para todas las peticiones API
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para loggear todas las peticiones
    """
    
    def process_request(self, request):
        # Guardar tiempo de inicio
        request._request_start_time = time.time()
        
        # Loggear petición entrante
        if request.path.startswith('/api/'):
            logger.info(
                f"[REQUEST] {request.method} {request.path} - "
                f"Usuario: {request.user.email if request.user.is_authenticated else 'Anonimo'}"
            )
    
    def process_response(self, request, response):
        if hasattr(request, '_request_start_time'):
            # Calcular tiempo de procesamiento
            duration = time.time() - request._request_start_time
            
            # Loggear respuesta
            if request.path.startswith('/api/'):
                level = logging.INFO if response.status_code < 400 else logging.WARNING
                logger.log(
                    level,
                    f"[RESPONSE] {request.method} {request.path} - "
                    f"Status: {response.status_code} - "
                    f"Tiempo: {duration:.3f}s"
                )
                
                # Advertir sobre respuestas lentas
                if duration > 1.0:
                    logger.warning(
                        f"[SLOW] Respuesta lenta: {request.path} tomo {duration:.3f}s"
                    )
        
        return response
    
    def process_exception(self, request, exception):
        # Loggear excepciones
        logger.error(
            f"[EXCEPTION] en {request.method} {request.path}: {str(exception)}",
            exc_info=True
        )
