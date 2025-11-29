"""URLs marketplace"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet,
    ProductoReporteView,
    ProductoReportesListView,
    ProductoReporteUpdateView,
    TodosProductoReportesListView,
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
    # Reportes de productos
    path('productos/<int:pk>/reportar/', ProductoReporteView.as_view(), name='producto-report'),
    path('productos/<int:pk>/reportes/', ProductoReportesListView.as_view(), name='producto-reports'),
    path('reportes/<int:pk>/', ProductoReporteUpdateView.as_view(), name='producto-report-update'),
    path('reportes/todos/', TodosProductoReportesListView.as_view(), name='todos-producto-reportes'),
]
