"""Rutas de la aplicación de foros."""

from django.urls import path

from .views import (
    CommentCreateView,
    EncuestaOpcionesListView,
    EncuestaVotarView,
    ForoListView,
    ModeracionListView,
    PostHideView,
    PostListCreateView,
    PostModeracionView,
    PostReporteView,
    PostReportesListView,
    PostVoteView,
    ReporteUpdateView,
    TodosReportesListView,
)

urlpatterns = [
    path("forum/foros/", ForoListView.as_view(), name="foro-list"),
    path("forum/posts/", PostListCreateView.as_view(), name="post-list"),
    # Rutas específicas primero (más específicas antes que las generales)
    path("forum/posts/<int:pk>/comentarios/", CommentCreateView.as_view(), name="post-comments"),
    path("forum/posts/<int:pk>/votar/", PostVoteView.as_view(), name="post-vote"),
    path("forum/posts/<int:pk>/reportar/", PostReporteView.as_view(), name="post-report"),
    path("forum/posts/<int:pk>/moderar/", PostModeracionView.as_view(), name="post-moderate"),
    path("forum/posts/<int:pk>/ocultar/", PostHideView.as_view(), name="post-hide"),
    path("forum/posts/<int:pk>/reportes/", PostReportesListView.as_view(), name="post-reports"),
    # Ruta general para DELETE al final
    path("forum/posts/<int:pk>/", PostListCreateView.as_view(), name="post-detail"),
    path("forum/reportes/<int:pk>/", ReporteUpdateView.as_view(), name="report-update"),
    path("forum/moderacion/", ModeracionListView.as_view(), name="moderation-list"),
    # Encuestas
    path("forum/posts/<int:pk>/encuesta/opciones/", EncuestaOpcionesListView.as_view(), name="encuesta-opciones"),
    path("forum/posts/<int:pk>/encuesta/opciones/<int:opcion_id>/votar/", EncuestaVotarView.as_view(), name="encuesta-votar"),
    # Reportes - Admin
    path("forum/reportes/todos/", TodosReportesListView.as_view(), name="todos-reportes"),
]
