"""URLs mejoradas para la API completa de encuestas."""

from django.urls import path

from .views import (
    PollListCreateView,
    PollDetailView,
    PollVoteView,
    PollExportView,
    PollAnalyticsView,
    PollCloseView,
    MyPollsView,
    PollsDashboardView,
)

urlpatterns = [
    # CRUD básico de encuestas
    path("polls/", PollListCreateView.as_view(), name="poll-list-create"),
    path("polls/<int:pk>/", PollDetailView.as_view(), name="poll-detail"),
    
    # Acciones específicas
    path("polls/<int:pk>/votar/", PollVoteView.as_view(), name="poll-vote"),
    path("polls/<int:pk>/cerrar/", PollCloseView.as_view(), name="poll-close"),
    path("polls/<int:pk>/export/", PollExportView.as_view(), name="poll-export"),
    path("polls/<int:pk>/analytics/", PollAnalyticsView.as_view(), name="poll-analytics"),
    
    # Vistas especiales
    path("polls/mis-encuestas/", MyPollsView.as_view(), name="my-polls"),
    path("polls/dashboard/", PollsDashboardView.as_view(), name="polls-dashboard"),
]