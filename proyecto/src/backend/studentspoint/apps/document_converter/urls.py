from django.urls import path
from .views import ConversionListCreateView, ConversionDetailView, ConversionDeleteView

urlpatterns = [
    path('converter/', ConversionListCreateView.as_view(), name='conversion-list-create'),
    path('converter/<int:pk>/', ConversionDetailView.as_view(), name='conversion-detail'),
    path('converter/<int:pk>/delete/', ConversionDeleteView.as_view(), name='conversion-delete'),
]

