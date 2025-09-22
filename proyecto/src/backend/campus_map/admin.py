from django.contrib import admin
from .models import Campus, Location, VirtualTour, TourStep, MapMarker

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'address', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'campus', 'location_type', 'floor', 'room_number', 'is_active', 'created_at']
    list_filter = ['campus', 'location_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'room_number']
    raw_id_fields = ['campus']

@admin.register(VirtualTour)
class VirtualTourAdmin(admin.ModelAdmin):
    list_display = ['title', 'campus', 'created_by', 'is_active', 'created_at']
    list_filter = ['campus', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['campus', 'created_by']

@admin.register(TourStep)
class TourStepAdmin(admin.ModelAdmin):
    list_display = ['tour', 'order', 'title', 'location', 'created_at']
    list_filter = ['tour', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['tour', 'location']
    ordering = ['tour', 'order']

@admin.register(MapMarker)
class MapMarkerAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'marker_type', 'is_active', 'created_at']
    list_filter = ['marker_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['location']