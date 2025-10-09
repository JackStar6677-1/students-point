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
from pathlib import Path
from rest_framework_simplejwt.views import TokenRefreshView


def spa_serve(request, path=""):
    # Servir desde staticfiles en lugar de frontend
    base = Path(settings.STATIC_ROOT)
    target = base / path
    
    # Si es un directorio, servir index.html
    if target.is_dir():
        path = f"{path.rstrip('/')}/index.html"
        target = base / path
    
    # Si el archivo no existe, intentar servir index.html para rutas SPA
    if not target.exists():
        # Para rutas como /forum/, /market/, etc., servir su index.html
        if path and not path.endswith('.html') and not path.endswith('.ico') and not path.endswith('.css') and not path.endswith('.js'):
            spa_path = f"{path.rstrip('/')}/index.html"
            spa_target = base / spa_path
            if spa_target.exists():
                return serve(request, spa_path, document_root=base)
        
        # Si no existe, servir index.html principal
        if (base / "index.html").exists():
            return serve(request, "index.html", document_root=base)
    
    return serve(request, path, document_root=base)

urlpatterns = [
    path('', RedirectView.as_view(url='/index.html', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('studentspoint.apps.accounts.urls')),
    path('api/', include('studentspoint.apps.campuses.urls')),
    path('api/', include('studentspoint.apps.forum.urls')),
    path('api/', include('studentspoint.apps.market.urls')),
    path('api/', include('studentspoint.apps.polls.urls')),
    path('api/', include('studentspoint.apps.schedules.urls')),
    path('api/', include('studentspoint.apps.notifications.urls')),
    path('api/', include('studentspoint.apps.reports.urls')),
    path('api/', include('studentspoint.apps.otec.urls')),
    path('api/', include('studentspoint.apps.wellbeing.urls')),
    path('api/', include('studentspoint.apps.portfolio.urls')),
    path('api/marketplace/', include('marketplace.urls')),
    path('api/campus/', include('campus_map.urls')),
    path('api/infrastructure/', include('infrastructure_monitoring.urls')),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('', include('studentspoint.apps.health.urls')),
    # Servir Service Worker desde la raíz
    re_path(r'^sw\.js$', serve, {'document_root': Path(settings.STATIC_ROOT), 'path': 'sw.js'}),
    # Servir favicon específicamente
    re_path(r'^favicon\.ico$', serve, {'document_root': Path(settings.STATIC_ROOT), 'path': 'favicon.ico'}),
    # Servir imágenes desde staticfiles
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': Path(settings.STATIC_ROOT) / "images"}),
    # Servir imágenes desde la carpeta imagenes (legacy)
    re_path(r'^imagenes/(?P<path>.*)$', serve, {'document_root': Path(settings.BASE_DIR).parent.parent / "imagenes"}),
    re_path(r'^(?P<path>.*)$', spa_serve),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Servir imágenes desde staticfiles
    urlpatterns += static('/images/', document_root=Path(settings.STATIC_ROOT) / "images")
