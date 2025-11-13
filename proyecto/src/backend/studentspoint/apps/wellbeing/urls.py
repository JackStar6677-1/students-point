from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BienestarListView, BienestarViewSet

router = DefaultRouter()
router.register(r'bienestar', BienestarViewSet, basename='bienestar')

urlpatterns = [
    path("", include(router.urls)),
    # Vista heredada para compatibilidad
    path("bienestar-list/", BienestarListView.as_view(), name="bienestar-list"),
]
