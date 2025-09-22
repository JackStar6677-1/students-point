#!/usr/bin/env python
"""
Script para crear datos de ejemplo para las nuevas aplicaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from marketplace.models import Category, Product
from campus_map.models import Campus, Location, VirtualTour, TourStep

User = get_user_model()

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear categorías para marketplace
    categories_data = [
        {'name': 'Libros', 'description': 'Libros de texto y académicos', 'icon': 'fas fa-book'},
        {'name': 'Electrónicos', 'description': 'Dispositivos electrónicos', 'icon': 'fas fa-laptop'},
        {'name': 'Ropa', 'description': 'Ropa y accesorios', 'icon': 'fas fa-tshirt'},
        {'name': 'Hogar', 'description': 'Artículos para el hogar', 'icon': 'fas fa-home'},
        {'name': 'Deportes', 'description': 'Artículos deportivos', 'icon': 'fas fa-dumbbell'},
        {'name': 'Otros', 'description': 'Otros productos', 'icon': 'fas fa-tag'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"Creada categoría: {category.name}")
    
    # Crear campus
    campuses_data = [
        {
            'name': 'Sede San Carlos de Apoquindo',
            'slug': 'san-carlos',
            'address': 'Av. San Carlos de Apoquindo 2200, Las Condes, Santiago',
            'latitude': -33.4172,
            'longitude': -70.6067,
            'description': 'Sede principal de Duoc UC en Las Condes'
        },
        {
            'name': 'Sede Maipú',
            'slug': 'maipu',
            'address': 'Av. Américo Vespucio 1501, Maipú, Santiago',
            'latitude': -33.5119,
            'longitude': -70.7500,
            'description': 'Sede de Duoc UC en Maipú'
        },
        {
            'name': 'Sede San Joaquín',
            'slug': 'san-joaquin',
            'address': 'Av. Vicuña Mackenna 4910, San Joaquín, Santiago',
            'latitude': -33.4989,
            'longitude': -70.6150,
            'description': 'Sede de Duoc UC en San Joaquín'
        }
    ]
    
    for campus_data in campuses_data:
        campus, created = Campus.objects.get_or_create(
            slug=campus_data['slug'],
            defaults=campus_data
        )
        if created:
            print(f"Creado campus: {campus.name}")
            
            # Crear ubicaciones para cada campus
            locations_data = [
                {
                    'name': 'Entrada Principal',
                    'location_type': 'building',
                    'description': 'Entrada principal del campus',
                    'latitude': campus.latitude + 0.0001,
                    'longitude': campus.longitude + 0.0001,
                    'floor': 1
                },
                {
                    'name': 'Biblioteca',
                    'location_type': 'library',
                    'description': 'Biblioteca central del campus',
                    'latitude': campus.latitude + 0.0002,
                    'longitude': campus.longitude + 0.0002,
                    'floor': 2
                },
                {
                    'name': 'Cafetería',
                    'location_type': 'cafeteria',
                    'description': 'Cafetería y comedor estudiantil',
                    'latitude': campus.latitude + 0.0003,
                    'longitude': campus.longitude + 0.0003,
                    'floor': 1
                },
                {
                    'name': 'Laboratorio de Computación',
                    'location_type': 'lab',
                    'description': 'Laboratorio de computación e informática',
                    'latitude': campus.latitude + 0.0004,
                    'longitude': campus.longitude + 0.0004,
                    'floor': 3,
                    'room_number': 'LAB-301'
                },
                {
                    'name': 'Auditorio Principal',
                    'location_type': 'auditorium',
                    'description': 'Auditorio principal para eventos',
                    'latitude': campus.latitude + 0.0005,
                    'longitude': campus.longitude + 0.0005,
                    'floor': 1,
                    'room_number': 'AUD-101'
                }
            ]
            
            for loc_data in locations_data:
                location, created = Location.objects.get_or_create(
                    campus=campus,
                    name=loc_data['name'],
                    defaults=loc_data
                )
                if created:
                    print(f"  Creada ubicación: {location.name}")
            
            # Crear recorrido virtual para cada campus
            tour, created = VirtualTour.objects.get_or_create(
                campus=campus,
                title=f'Recorrido Principal - {campus.name}',
                defaults={
                    'description': f'Recorrido virtual completo por {campus.name}',
                    'is_active': True
                }
            )
            
            if created:
                print(f"  Creado recorrido virtual: {tour.title}")
                
                # Crear pasos del recorrido
                campus_locations = Location.objects.filter(campus=campus)
                for i, location in enumerate(campus_locations, 1):
                    step, created = TourStep.objects.get_or_create(
                        tour=tour,
                        order=i,
                        defaults={
                            'location': location,
                            'title': f'Paso {i}: {location.name}',
                            'description': f'Visita a {location.name}. {location.description}'
                        }
                    )
                    if created:
                        print(f"    Creado paso: {step.title}")
    
    print("Datos de ejemplo creados exitosamente!")

if __name__ == '__main__':
    create_sample_data()
