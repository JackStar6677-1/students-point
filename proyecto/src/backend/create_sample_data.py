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
from django.utils import timezone
from studentspoint.apps.market.models import CategoriaProducto as Category, Producto as Product
from campus_map.models import Campus, Location, VirtualTour, TourStep, MapMarker
from studentspoint.apps.campuses.models import Sede

User = get_user_model()

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear categorías para marketplace
    categories_data = [
        {'nombre': 'Libros', 'descripcion': 'Libros de texto y académicos', 'icono': 'fas fa-book'},
        {'nombre': 'Electrónicos', 'descripcion': 'Dispositivos electrónicos', 'icono': 'fas fa-laptop'},
        {'nombre': 'Ropa', 'descripcion': 'Ropa y accesorios', 'icono': 'fas fa-tshirt'},
        {'nombre': 'Hogar', 'descripcion': 'Artículos para el hogar', 'icono': 'fas fa-home'},
        {'nombre': 'Deportes', 'descripcion': 'Artículos deportivos', 'icono': 'fas fa-dumbbell'},
        {'nombre': 'Otros', 'descripcion': 'Otros productos', 'icono': 'fas fa-tag'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"Creada categoría: {category.nombre}")
    
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
    
    # Crear datos de ejemplo para monitoreo de infraestructura
    print(" Creando datos de ejemplo para monitoreo de infraestructura...")
    
    from infrastructure_monitoring.models import InfraestructuraItem, AlertaInfraestructura, MantenimientoProgramado, MetricasInfraestructura, ReporteInfraestructura, DashboardConfig
    from datetime import timedelta
    
    # Crear una sede si no existe
    sede, created = Sede.objects.get_or_create(
        slug='sede-principal',
        defaults={
            'nombre': 'Sede Principal',
            'direccion': 'Av. Principal 123, Santiago',
            'lat': -33.4489,
            'lng': -70.6693
        }
    )
    if created:
        print(f"Creada sede: {sede.nombre}")
    
    # Crear elementos de infraestructura
    infraestructura_items = [
        {
            'nombre': 'Aula 101',
            'tipo': 'aula',
            'ubicacion': 'Edificio A, Primer Piso',
            'descripcion': 'Aula principal con capacidad para 40 estudiantes',
            'estado_actual': 'operativo',
            'capacidad_maxima': 40,
            'campus': sede,
            'activo': True
        },
        {
            'nombre': 'Laboratorio de Computación',
            'tipo': 'laboratorio',
            'ubicacion': 'Edificio B, Segundo Piso',
            'descripcion': 'Laboratorio con 30 computadores para clases de programación',
            'estado_actual': 'operativo',
            'capacidad_maxima': 30,
            'campus': sede,
            'activo': True
        },
        {
            'nombre': 'Biblioteca Central',
            'tipo': 'biblioteca',
            'ubicacion': 'Edificio C, Planta Baja',
            'descripcion': 'Biblioteca principal con salas de estudio',
            'estado_actual': 'operativo',
            'capacidad_maxima': 100,
            'campus': sede,
            'activo': True
        },
        {
            'nombre': 'Cafetería',
            'tipo': 'cafeteria',
            'ubicacion': 'Edificio D, Planta Baja',
            'descripcion': 'Cafetería con capacidad para 80 personas',
            'estado_actual': 'operativo',
            'capacidad_maxima': 80,
            'campus': sede,
            'activo': True
        },
        {
            'nombre': 'Gimnasio',
            'tipo': 'gimnasio',
            'ubicacion': 'Edificio E, Planta Baja',
            'descripcion': 'Gimnasio con cancha de básquetbol y equipos de ejercicio',
            'estado_actual': 'operativo',
            'capacidad_maxima': 50,
            'campus': sede,
            'activo': True
        }
    ]
    
    for item_data in infraestructura_items:
        InfraestructuraItem.objects.get_or_create(
            nombre=item_data['nombre'],
            defaults=item_data
        )
    
    # Crear reportes de ejemplo
    reportes = [
        {
            'item': InfraestructuraItem.objects.filter(nombre='Aula 101').first(),
            'reportado_por': User.objects.first(),
            'tipo': 'mantenimiento',
            'titulo': 'Proyector necesita mantenimiento',
            'descripcion': 'El proyector del Aula 101 presenta problemas de calibración',
            'prioridad': 'media',
            'estado': 'abierto',
            'fecha_reporte': timezone.now()
        },
        {
            'item': InfraestructuraItem.objects.filter(nombre='Laboratorio de Computación').first(),
            'reportado_por': User.objects.first(),
            'tipo': 'problema',
            'titulo': 'Fallo en sistema de red',
            'descripcion': '5 computadores sin conexión a internet',
            'prioridad': 'alta',
            'estado': 'en_proceso',
            'fecha_reporte': timezone.now() - timedelta(hours=2)
        }
    ]
    
    for reporte_data in reportes:
        if reporte_data['item'] and reporte_data['reportado_por']:
            ReporteInfraestructura.objects.get_or_create(
                item=reporte_data['item'],
                titulo=reporte_data['titulo'],
                defaults=reporte_data
            )
    
    # Crear mantenimientos programados
    mantenimientos = [
        {
            'item': InfraestructuraItem.objects.filter(nombre='Biblioteca Central').first(),
            'tipo': 'preventivo',
            'titulo': 'Limpieza general y revisión de equipos',
            'descripcion': 'Limpieza general y revisión de equipos de la biblioteca',
            'fecha_programada': timezone.now() + timedelta(days=30),
            'duracion_estimada_horas': 4,
            'completado': False
        },
        {
            'item': InfraestructuraItem.objects.filter(nombre='Gimnasio').first(),
            'tipo': 'preventivo',
            'titulo': 'Revisión de equipos de ejercicio y cancha',
            'descripcion': 'Revisión de equipos de ejercicio y cancha del gimnasio',
            'fecha_programada': timezone.now() + timedelta(days=15),
            'duracion_estimada_horas': 6,
            'completado': False
        }
    ]
    
    for mantenimiento_data in mantenimientos:
        if mantenimiento_data['item']:
            MantenimientoProgramado.objects.get_or_create(
                item=mantenimiento_data['item'],
                titulo=mantenimiento_data['titulo'],
                defaults=mantenimiento_data
            )
    
    # Crear métricas de ejemplo
    items = InfraestructuraItem.objects.all()
    for item in items:
        MetricasInfraestructura.objects.get_or_create(
            item=item,
            fecha_medicion=timezone.now(),
            defaults={
                'ocupacion_actual': 25,
                'ocupacion_promedio': 75.0,
                'tiempo_uso_total': 480,
                'temperatura': 22.5,
                'humedad': 45.0,
                'ruido_db': 65.0,
                'velocidad_wifi': 100.0,
                'calificacion_satisfaccion': 4,
                'comentarios': f'Métricas del {item.nombre}'
            }
        )
    
    # Crear reportes de ejemplo
    reportes = [
        {
            'item': InfraestructuraItem.objects.filter(nombre='Aula 101').first(),
            'reportado_por': User.objects.first(),
            'tipo': 'problema',
            'titulo': 'Reporte Mensual de Infraestructura',
            'descripcion': 'Estado general de la infraestructura del campus',
            'prioridad': 'media',
            'estado': 'abierto'
        }
    ]
    
    for reporte_data in reportes:
        if reporte_data['item'] and reporte_data['reportado_por']:
            ReporteInfraestructura.objects.get_or_create(
                item=reporte_data['item'],
                titulo=reporte_data['titulo'],
                defaults=reporte_data
            )
    
    # Crear configuración del dashboard
    if User.objects.exists():
        DashboardConfig.objects.get_or_create(
            usuario=User.objects.first(),
            defaults={
                'mostrar_metricas_tiempo_real': True,
                'mostrar_reportes_recientes': True,
                'mostrar_mantenimientos_pendientes': True,
                'mostrar_alertas': True,
                'mostrar_graficos_ocupacion': True
            }
        )

    print(" Datos de ejemplo creados exitosamente!")
    print("\n Resumen:")
    print(f"   - Categorías: {Category.objects.count()}")
    print(f"   - Productos: {Product.objects.count()}")
    print(f"   - Sedes: {Campus.objects.count()}")
    print(f"   - Ubicaciones: {Location.objects.count()}")
    print(f"   - Tours virtuales: {VirtualTour.objects.count()}")
    print(f"   - Pasos de tours: {TourStep.objects.count()}")
    print(f"   - Marcadores: {MapMarker.objects.count()}")
    print(f"   - Elementos de infraestructura: {InfraestructuraItem.objects.count()}")
    print(f"   - Alertas: {AlertaInfraestructura.objects.count()}")
    print(f"   - Mantenimientos: {MantenimientoProgramado.objects.count()}")
    print(f"   - Métricas: {MetricasInfraestructura.objects.count()}")
    print(f"   - Reportes: {ReporteInfraestructura.objects.count()}")
    print("\n ¡El sistema está listo para usar!")

if __name__ == '__main__':
    create_sample_data()
