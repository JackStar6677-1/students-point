"""
URLs para el sistema de monitoreo de infraestructura.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.InfraestructuraItemViewSet)
router.register(r'reportes', views.ReporteInfraestructuraViewSet)
router.register(r'stats', views.DashboardStatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]
