from django.urls import path
from . import views

app_name = 'campus_map'

urlpatterns = [
    # Campus
    path('campuses/', views.CampusListAPIView.as_view(), name='campus-list'),
    path('campuses/<slug:slug>/', views.CampusDetailAPIView.as_view(), name='campus-detail'),
    path('campuses/<slug:campus_slug>/locations/', views.campus_locations, name='campus-locations'),
    path('campuses/<slug:campus_slug>/tours/', views.campus_tours, name='campus-tours'),
    
    # Ubicaciones
    path('locations/', views.LocationListAPIView.as_view(), name='location-list'),
    path('locations/<int:pk>/', views.LocationDetailAPIView.as_view(), name='location-detail'),
    path('locations/search/', views.search_locations, name='location-search'),
    path('locations/nearby/', views.nearby_locations, name='nearby-locations'),
    
    # Recorridos Virtuales
    path('tours/', views.VirtualTourListAPIView.as_view(), name='tour-list'),
    path('tours/<int:pk>/', views.VirtualTourDetailAPIView.as_view(), name='tour-detail'),
    path('tours/<int:tour_id>/steps/', views.tour_steps, name='tour-steps'),
    
    # Marcadores del Mapa
    path('markers/', views.MapMarkerListAPIView.as_view(), name='marker-list'),
]
