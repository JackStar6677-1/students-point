from django.urls import path
from .views import (
    ConversionListCreateView, 
    ConversionDetailView, 
    ConversionDeleteView,
    ConversionDownloadView
)

urlpatterns = [
    path('converter/', ConversionListCreateView.as_view(), name='conversion-list-create'),
    path('converter/<int:pk>/', ConversionDetailView.as_view(), name='conversion-detail'),
    path('converter/<int:pk>/delete/', ConversionDeleteView.as_view(), name='conversion-delete'),
    path('converter/<int:pk>/download/', ConversionDownloadView.as_view(), name='conversion-download'),
]

