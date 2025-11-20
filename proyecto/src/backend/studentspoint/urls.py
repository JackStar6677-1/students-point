"""
URL configuration for studentspoint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse, FileResponse
from pathlib import Path
from rest_framework_simplejwt.views import TokenRefreshView
from studentspoint.apps.otec.video_views import serve_video


def serve_sw(request):
    """Servir Service Worker con headers correctos para PWA"""
    # Intentar desde staticfiles primero
    sw_path = Path(settings.STATIC_ROOT) / 'sw.js'
    if not sw_path.exists():
        # Si no está en staticfiles, buscar en static
        sw_path = Path(settings.BASE_DIR).parent / 'frontend' / 'static' / 'sw.js'
    
    if sw_path.exists():
        with open(sw_path, 'rb') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/javascript')
        # Headers importantes para PWA
        response['Service-Worker-Allowed'] = '/'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return HttpResponse('Service Worker not found', status=404)

def serve_manifest(request):
    """Servir manifest.json con headers correctos para PWA"""
    # Intentar desde staticfiles primero
    manifest_path = Path(settings.STATIC_ROOT) / 'manifest.json'
    if not manifest_path.exists():
        # Si no está en staticfiles, buscar en static
        manifest_path = Path(settings.BASE_DIR).parent / 'frontend' / 'static' / 'manifest.json'
    
    if manifest_path.exists():
        with open(manifest_path, 'rb') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/manifest+json')
        response['Cache-Control'] = 'public, max-age=3600'
        return response
    return HttpResponse('Manifest not found', status=404)

def spa_serve(request, path=""):
    # Servir HTMLs y otros archivos desde staticfiles
    base = Path(settings.STATIC_ROOT)
    
    # Si la ruta está vacía, servir index.html directamente
    if not path or path == '/':
        return serve(request, "index.html", document_root=base)
    
    target = base / path
    
    # Mapeo de rutas a archivos HTML específicos
    route_map = {
        'forum': 'forum/foro.html',
        'market': 'market/mercado.html',
        'bienestar': 'bienestar/bienestar.html',
        'portfolio': 'portfolio/portafolio.html',
        'encuestas': 'encuestas/encuestas.html',
        'cursos': 'cursos/cursos.html',
        'reportes': 'reportes/reportes.html',
        'streetview': 'streetview/recorridos-virtuales.html',
        'converter': 'converter/conversor.html',
        'moderacion': 'admin/reportes.html',  # Módulo de moderación de reportes del foro
    }
    
    # Si es un directorio, buscar archivo específico o index.html
    if target.is_dir():
        route_name = path.rstrip('/').split('/')[-1]
        if route_name in route_map:
            path = route_map[route_name]
        else:
            path = f"{path.rstrip('/')}/index.html"
        target = base / path
    
    # Si el archivo no existe, intentar servir archivo específico para rutas SPA
    if not target.exists():
        # Para rutas como /forum, /market, etc., servir su archivo específico
        if path and not path.endswith('.html') and not path.endswith('.ico') and not path.endswith('.css') and not path.endswith('.js'):
            route_name = path.rstrip('/').split('/')[-1]
            
            if route_name in route_map:
                spa_path = route_map[route_name]
                spa_target = base / spa_path
                if spa_target.exists():
                    return serve(request, spa_path, document_root=base)
        
        # Si no existe, servir index.html principal
        if (base / "index.html").exists():
            return serve(request, "index.html", document_root=base)
    
    return serve(request, path, document_root=base)

urlpatterns = [
    # Ruta de moderación ANTES del admin de Django para evitar conflictos
    re_path(r'^moderacion/?$', spa_serve, {'path': 'admin/reportes.html'}),
    path('admin/', admin.site.urls),
    path('api/', include('studentspoint.apps.accounts.urls')),
    path('api/', include('studentspoint.apps.campuses.urls')),
    path('api/', include('studentspoint.apps.forum.urls')),
    path('api/', include('studentspoint.apps.polls.urls')),
    path('api/', include('studentspoint.apps.notifications.urls')),
    path('api/', include('studentspoint.apps.reports.urls')),
    path('api/', include('studentspoint.apps.otec.urls')),
    path('api/', include('studentspoint.apps.wellbeing.urls')),
    path('api/', include('studentspoint.apps.portfolio.urls')),
    path('api/', include('studentspoint.apps.document_converter.urls')),
    path('api/market/', include('studentspoint.apps.market.urls')),
    path('api/campus/', include('campus_map.urls')),
    path('api/infrastructure/', include('infrastructure_monitoring.urls')),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    # Servir Service Worker y manifest ANTES de todo (prioridad alta para PWA)
    re_path(r'^sw\.js$', serve_sw),
    re_path(r'^manifest\.json$', serve_manifest),
    path('', include('studentspoint.apps.health.urls')),
    re_path(r'^manifest\.webmanifest$', serve, {
        'document_root': Path(settings.STATIC_ROOT), 
        'path': 'manifest.webmanifest',
        'content_type': 'application/manifest+json'
    }),
    # Servir favicon específicamente
    re_path(r'^favicon\.ico$', serve, {'document_root': Path(settings.STATIC_ROOT), 'path': 'favicon.ico'}),
    # Servir archivos estaticos ANTES del catch-all (directamente desde staticfiles/)
    # Nota: sw.js y manifest.json ya se sirven arriba, pero también desde /static/ para compatibilidad
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': Path(settings.STATIC_ROOT)}),
    # Servir archivos del conversor con MIME type correcto
    re_path(r'^converter/(?P<path>.*\.js)$', serve, {
        'document_root': Path(settings.STATIC_ROOT) / 'converter',
        'content_type': 'application/javascript'
    }),
    re_path(r'^converter/(?P<path>.*\.css)$', serve, {
        'document_root': Path(settings.STATIC_ROOT) / 'converter',
        'content_type': 'text/css'
    }),
    # Servir imágenes desde staticfiles (sin /static/)
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': Path(settings.STATIC_ROOT) / "images"}),
    # Servir imágenes desde la carpeta imagenes (legacy)
    re_path(r'^imagenes/(?P<path>.*)$', serve, {'document_root': Path(settings.BASE_DIR).parent.parent / "imagenes"}),
    # Servir videos con soporte de streaming (HTTP Range Requests)
    re_path(r'^media/cursos/videos/(?P<path>.*)$', serve_video, name='serve_video'),
    # Servir otros archivos media (archivos subidos por usuarios: conversiones, fotos de perfil, etc.)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': Path(settings.MEDIA_ROOT)}),
    # Catch-all al final
    re_path(r'^(?P<path>.*)$', spa_serve),
]
