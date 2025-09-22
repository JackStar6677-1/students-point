from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Campus(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='campus/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campus"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Location(models.Model):
    LOCATION_TYPES = [
        ('building', 'Edificio'),
        ('room', 'Sala'),
        ('lab', 'Laboratorio'),
        ('library', 'Biblioteca'),
        ('cafeteria', 'Cafetería'),
        ('office', 'Oficina'),
        ('parking', 'Estacionamiento'),
        ('gym', 'Gimnasio'),
        ('auditorium', 'Auditorio'),
        ('other', 'Otro'),
    ]
    
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='other')
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    floor = models.IntegerField(null=True, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='campus/locations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.campus.name}"

class VirtualTour(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='virtual_tours')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Recorrido Virtual"
        verbose_name_plural = "Recorridos Virtuales"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.campus.name}"

class TourStep(models.Model):
    tour = models.ForeignKey(VirtualTour, on_delete=models.CASCADE, related_name='steps')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tour_steps')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='campus/tour_steps/', blank=True, null=True)
    audio_url = models.URLField(blank=True, help_text="URL del archivo de audio (opcional)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Paso del Recorrido"
        verbose_name_plural = "Pasos del Recorrido"
        ordering = ['order']
        unique_together = ['tour', 'order']
    
    def __str__(self):
        return f"{self.tour.title} - Paso {self.order}: {self.title}"

class MapMarker(models.Model):
    MARKER_TYPES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('success', 'Éxito'),
        ('danger', 'Peligro'),
        ('primary', 'Primario'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='markers')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    marker_type = models.CharField(max_length=20, choices=MARKER_TYPES, default='info')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Marcador del Mapa"
        verbose_name_plural = "Marcadores del Mapa"
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} - {self.location.name}"