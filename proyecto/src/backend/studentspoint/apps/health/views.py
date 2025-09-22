"""
Health check views para StudentsPoint
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import redis
import psutil
import time
from datetime import datetime


def health_check(request):
    """
    Endpoint de health check para verificar el estado del sistema
    """
    start_time = time.time()
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {}
    }
    
    # Verificar base de datos
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['services']['database'] = {
            'status': 'healthy',
            'response_time': round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        health_status['services']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # Verificar cache (Redis)
    try:
        cache_start = time.time()
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        health_status['services']['cache'] = {
            'status': 'healthy',
            'response_time': round((time.time() - cache_start) * 1000, 2)
        }
    except Exception as e:
        health_status['services']['cache'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # Verificar Redis directamente
    try:
        redis_start = time.time()
        r = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        health_status['services']['redis'] = {
            'status': 'healthy',
            'response_time': round((time.time() - redis_start) * 1000, 2)
        }
    except Exception as e:
        health_status['services']['redis'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # Verificar sistema
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status['services']['system'] = {
            'status': 'healthy',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'memory_available': memory.available,
            'disk_free': disk.free
        }
        
        # Marcar como unhealthy si el uso de recursos es muy alto
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_status['services']['system']['status'] = 'warning'
            if health_status['status'] == 'healthy':
                health_status['status'] = 'warning'
                
    except Exception as e:
        health_status['services']['system'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'
    
    # Verificar configuración
    health_status['services']['configuration'] = {
        'status': 'healthy',
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'cache_backend': settings.CACHES['default']['BACKEND']
    }
    
    # Tiempo total de respuesta
    health_status['total_response_time'] = round((time.time() - start_time) * 1000, 2)
    
    # Determinar código de estado HTTP
    if health_status['status'] == 'healthy':
        status_code = 200
    elif health_status['status'] == 'warning':
        status_code = 200
    else:
        status_code = 503
    
    return JsonResponse(health_status, status=status_code)


def readiness_check(request):
    """
    Endpoint de readiness check para Kubernetes
    """
    try:
        # Verificar que la base de datos esté lista
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Verificar que el cache esté listo
        cache.set('readiness_check', 'ok', 10)
        cache.get('readiness_check')
        
        return JsonResponse({'status': 'ready'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'not ready', 'error': str(e)}, status=503)


def liveness_check(request):
    """
    Endpoint de liveness check para Kubernetes
    """
    return JsonResponse({'status': 'alive'}, status=200)


def api_info(request):
    """
    Endpoint público con información de la API
    """
    return JsonResponse({
        'name': 'StudentsPoint API',
        'version': '1.0.0',
        'description': 'API para la plataforma StudentsPoint - PWA estudiantil',
        'endpoints': {
            'auth': '/api/auth/',
            'forum': '/api/forum/',
            'marketplace': '/api/marketplace/',
            'campus': '/api/campus/',
            'infrastructure': '/api/infrastructure/',
            'health': '/health/',
            'docs': '/api/docs/'
        },
        'status': 'active'
    }, status=200)