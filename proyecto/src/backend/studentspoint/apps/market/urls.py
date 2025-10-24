"""URLs para el sistema de compra/venta."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaProductoViewSet, ProductoViewSet, 
    ProductoReporteViewSet, ProductoAnalyticsViewSet
)

app_name = 'market'

router = DefaultRouter()
router.register(r'categories', CategoriaProductoViewSet, basename='category')
router.register(r'products', ProductoViewSet, basename='product')
router.register(r'reports', ProductoReporteViewSet, basename='report')
router.register(r'analytics', ProductoAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]