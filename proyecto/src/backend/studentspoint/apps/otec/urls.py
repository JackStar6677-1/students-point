from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CursoViewSet, ClaseVideoViewSet

router = DefaultRouter()
router.register(r"cursos", CursoViewSet, basename="curso")
router.register(r"clases-video", ClaseVideoViewSet, basename="clase-video")

urlpatterns = router.urls
