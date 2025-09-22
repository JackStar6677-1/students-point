"""Rutas de la aplicación de foros."""

from django.urls import path

from .views import (
    CommentCreateView,
    ForoListView,
    ModeracionListView,
    PostHideView,
    PostListCreateView,
    PostModeracionView,
    PostReporteView,
    PostReportesListView,
    PostVoteView,
)

urlpatterns = [
    path("forum/foros/", ForoListView.as_view(), name="foro-list"),
    path("forum/posts/", PostListCreateView.as_view(), name="post-list"),
    path("forum/posts/<int:pk>/comentarios", CommentCreateView.as_view(), name="post-comments"),
    path("forum/posts/<int:pk>/votar", PostVoteView.as_view(), name="post-vote"),
    path("forum/posts/<int:pk>/reportar", PostReporteView.as_view(), name="post-report"),
    path("forum/posts/<int:pk>/moderar", PostModeracionView.as_view(), name="post-moderate"),
    path("forum/posts/<int:pk>/ocultar", PostHideView.as_view(), name="post-hide"),
    path("forum/posts/<int:pk>/reportes", PostReportesListView.as_view(), name="post-reports"),
    path("forum/moderacion", ModeracionListView.as_view(), name="moderation-list"),
]
