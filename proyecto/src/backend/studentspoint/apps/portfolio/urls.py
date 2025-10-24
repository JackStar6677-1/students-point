"""URLs para el sistema de portafolio."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LogroViewSet, ProyectoViewSet, ExperienciaLaboralViewSet,
    HabilidadViewSet, PortafolioConfigViewSet, PortafolioSugerenciaViewSet,
    PortafolioAnalyticsViewSet, PortafolioCompletoViewSet
)

router = DefaultRouter()
router.register(r'logros', LogroViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'experiencias', ExperienciaLaboralViewSet)
router.register(r'habilidades', HabilidadViewSet)
router.register(r'config', PortafolioConfigViewSet)
router.register(r'sugerencias', PortafolioSugerenciaViewSet)
router.register(r'analytics', PortafolioAnalyticsViewSet)
router.register(r'completo', PortafolioCompletoViewSet)

urlpatterns = [
    path('portfolio/', include(router.urls)),
]