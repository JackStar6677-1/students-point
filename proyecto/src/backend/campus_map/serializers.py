from rest_framework import serializers
from .models import Campus, Location, VirtualTour, TourStep, MapMarker

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'slug', 'address', 'latitude', 'longitude', 'description', 'image', 'is_active', 'created_at', 'updated_at']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'location_type', 'description', 'latitude', 'longitude', 'floor', 'room_number', 'image', 'is_active', 'created_at', 'updated_at']

class LocationListSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'location_type', 'description', 'latitude', 'longitude', 'floor', 'room_number', 'image', 'campus', 'is_active']

class TourStepSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = TourStep
        fields = ['id', 'order', 'title', 'description', 'image', 'audio_url', 'location', 'created_at']

class VirtualTourSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    steps = TourStepSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = VirtualTour
        fields = ['id', 'title', 'description', 'campus', 'steps', 'created_by', 'is_active', 'created_at', 'updated_at']

class VirtualTourListSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    steps_count = serializers.SerializerMethodField()
    
    class Meta:
        model = VirtualTour
        fields = ['id', 'title', 'description', 'campus', 'steps_count', 'is_active', 'created_at']
    
    def get_steps_count(self, obj):
        return obj.steps.count()

class MapMarkerSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = MapMarker
        fields = ['id', 'title', 'description', 'marker_type', 'location', 'is_active', 'created_at']

class CampusWithLocationsSerializer(serializers.ModelSerializer):
    locations = LocationListSerializer(many=True, read_only=True)
    virtual_tours = VirtualTourListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Campus
        fields = ['id', 'name', 'slug', 'address', 'latitude', 'longitude', 'description', 'image', 'locations', 'virtual_tours', 'is_active']
