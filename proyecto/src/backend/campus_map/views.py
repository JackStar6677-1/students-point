from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Campus, Location, VirtualTour, TourStep, MapMarker
from .serializers import (
    CampusSerializer, LocationSerializer, LocationListSerializer,
    VirtualTourSerializer, VirtualTourListSerializer, TourStepSerializer,
    MapMarkerSerializer, CampusWithLocationsSerializer
)
from drf_spectacular.utils import extend_schema

class CampusListAPIView(generics.ListAPIView):
    queryset = Campus.objects.filter(is_active=True)
    serializer_class = CampusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CampusDetailAPIView(generics.RetrieveAPIView):
    queryset = Campus.objects.filter(is_active=True)
    serializer_class = CampusWithLocationsSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.filter(is_active=True).select_related('campus')
    serializer_class = LocationListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campus_id = self.request.query_params.get('campus')
        location_type = self.request.query_params.get('type')
        
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        
        if location_type:
            queryset = queryset.filter(location_type=location_type)
        
        return queryset

class LocationDetailAPIView(generics.RetrieveAPIView):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VirtualTourListAPIView(generics.ListAPIView):
    queryset = (
        VirtualTour.objects.filter(is_active=True)
        .select_related('campus', 'created_by')
        .prefetch_related('steps', 'steps__location')
    )
    serializer_class = VirtualTourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campus_id = self.request.query_params.get('campus')

        # Filtro explícito por query param
        if campus_id:
            return queryset.filter(campus_id=campus_id)

        # Si no viene filtro y el usuario tiene sede asignada (apps.campuses.Sede),
        # intentar mapear por slug/nombre al modelo Campus de este módulo
        user = getattr(self.request, 'user', None)
        try:
            if user and user.is_authenticated and getattr(user, 'campus', None):
                sede = user.campus  # studentspoint.apps.campuses.models.Sede
                # Intentar por slug primero
                mapped = queryset.filter(campus__slug=sede.slug)
                if mapped.exists():
                    return mapped
                # Fallback: intentar por nombre (case-insensitive)
                mapped = queryset.filter(campus__name__iexact=sede.nombre)
                if mapped.exists():
                    return mapped
        except Exception:
            # No bloquear en caso de error de mapeo; retornar sin filtrar
            pass

        return queryset

class VirtualTourDetailAPIView(generics.RetrieveAPIView):
    queryset = VirtualTour.objects.filter(is_active=True)
    serializer_class = VirtualTourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MapMarkerListAPIView(generics.ListAPIView):
    queryset = MapMarker.objects.filter(is_active=True).select_related('location')
    serializer_class = MapMarkerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        campus_id = self.request.query_params.get('campus')
        location_id = self.request.query_params.get('location')
        
        if campus_id:
            queryset = queryset.filter(location__campus_id=campus_id)
        
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def campus_locations(request, campus_slug):
    try:
        campus = Campus.objects.get(slug=campus_slug, is_active=True)
        locations = Location.objects.filter(campus=campus, is_active=True)
        serializer = LocationListSerializer(locations, many=True)
        return Response(serializer.data)
    except Campus.DoesNotExist:
        return Response({'error': 'Campus no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def campus_tours(request, campus_slug):
    try:
        campus = Campus.objects.get(slug=campus_slug, is_active=True)
        tours = VirtualTour.objects.filter(campus=campus, is_active=True)
        serializer = VirtualTourListSerializer(tours, many=True)
        return Response(serializer.data)
    except Campus.DoesNotExist:
        return Response({'error': 'Campus no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def tour_steps(request, tour_id):
    try:
        tour = VirtualTour.objects.get(id=tour_id, is_active=True)
        steps = TourStep.objects.filter(tour=tour).order_by('order')
        serializer = TourStepSerializer(steps, many=True)
        return Response(serializer.data)
    except VirtualTour.DoesNotExist:
        return Response({'error': 'Recorrido virtual no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_locations(request):
    query = request.GET.get('q', '')
    campus_id = request.GET.get('campus')
    location_type = request.GET.get('type')
    
    queryset = Location.objects.filter(is_active=True)
    
    if campus_id:
        queryset = queryset.filter(campus_id=campus_id)
    
    if location_type:
        queryset = queryset.filter(location_type=location_type)
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    serializer = LocationListSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def nearby_locations(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = float(request.GET.get('radius', 0.01))  # Radio en grados (aproximadamente 1km)
    
    if not lat or not lng:
        return Response({'error': 'Se requieren coordenadas lat y lng'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lat = float(lat)
        lng = float(lng)
        
        locations = Location.objects.filter(
            is_active=True,
            latitude__gte=lat-radius,
            latitude__lte=lat+radius,
            longitude__gte=lng-radius,
            longitude__lte=lng+radius
        ).select_related('campus')
        
        serializer = LocationListSerializer(locations, many=True)
        return Response(serializer.data)
    except ValueError:
        return Response({'error': 'Coordenadas inválidas'}, status=status.HTTP_400_BAD_REQUEST)