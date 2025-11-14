"""
Comando de management para poblar categorías iniciales del marketplace.

Uso:
    python manage.py poblar_categorias
"""

from django.core.management.base import BaseCommand
from studentspoint.apps.market.models import CategoriaProducto


class Command(BaseCommand):
    help = 'Pobla la base de datos con categorías iniciales del marketplace (al menos 10 categorías)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando categorías del marketplace...'))
        
        # Lista de categorías con descripciones e iconos
        categorias_data = [
            {
                'nombre': 'Libros y Apuntes',
                'descripcion': 'Libros de texto, apuntes, guías de estudio y material académico',
                'icono': 'fas fa-book'
            },
            {
                'nombre': 'Electrónicos',
                'descripcion': 'Laptops, tablets, smartphones, calculadoras y dispositivos electrónicos',
                'icono': 'fas fa-laptop'
            },
            {
                'nombre': 'Ropa y Accesorios',
                'descripcion': 'Ropa, zapatos, mochilas, carteras y accesorios personales',
                'icono': 'fas fa-tshirt'
            },
            {
                'nombre': 'Hogar y Decoración',
                'descripcion': 'Artículos para el hogar, decoración, muebles y electrodomésticos',
                'icono': 'fas fa-home'
            },
            {
                'nombre': 'Deportes y Fitness',
                'descripcion': 'Equipamiento deportivo, ropa deportiva, accesorios de gimnasio',
                'icono': 'fas fa-dumbbell'
            },
            {
                'nombre': 'Instrumentos Musicales',
                'descripcion': 'Guitarras, pianos, instrumentos de viento, percusión y accesorios musicales',
                'icono': 'fas fa-music'
            },
            {
                'nombre': 'Arte y Manualidades',
                'descripcion': 'Materiales de arte, pinturas, pinceles, cuadernos de dibujo',
                'icono': 'fas fa-palette'
            },
            {
                'nombre': 'Videojuegos y Consolas',
                'descripcion': 'Consolas, videojuegos, controles, accesorios gaming',
                'icono': 'fas fa-gamepad'
            },
            {
                'nombre': 'Bicicletas y Transporte',
                'descripcion': 'Bicicletas, scooters, patinetas, accesorios de transporte',
                'icono': 'fas fa-bicycle'
            },
            {
                'nombre': 'Servicios',
                'descripcion': 'Tutorías, clases particulares, servicios de diseño, programación, etc.',
                'icono': 'fas fa-handshake'
            },
            {
                'nombre': 'Material de Oficina',
                'descripcion': 'Cuadernos, lápices, calculadoras, carpetas, material de oficina',
                'icono': 'fas fa-briefcase'
            },
            {
                'nombre': 'Otros',
                'descripcion': 'Otros productos que no encajan en las categorías anteriores',
                'icono': 'fas fa-tag'
            }
        ]
        
        creadas = 0
        existentes = 0
        
        for cat_data in categorias_data:
            categoria, created = CategoriaProducto.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'descripcion': cat_data['descripcion'],
                    'icono': cat_data['icono'],
                    'activa': True
                }
            )
            
            if created:
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Creada categoria: {categoria.nombre}')
                )
            else:
                existentes += 1
                # Actualizar descripción e icono si no los tiene
                if not categoria.descripcion or not categoria.icono:
                    categoria.descripcion = cat_data['descripcion']
                    categoria.icono = cat_data['icono']
                    categoria.activa = True
                    categoria.save()
                    self.stdout.write(
                        self.style.WARNING(f'[ACTUALIZADA] Categoria: {categoria.nombre}')
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(f'[EXISTE] Categoria: {categoria.nombre}')
                    )
        
        total = CategoriaProducto.objects.filter(activa=True).count()
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'[COMPLETADO] Proceso finalizado:'))
        self.stdout.write(f'  - Categorias creadas: {creadas}')
        self.stdout.write(f'  - Categorias existentes: {existentes}')
        self.stdout.write(f'  - Total de categorias activas: {total}')
        
        if total < 10:
            self.stdout.write(
                self.style.WARNING(f'[ADVERTENCIA] Solo hay {total} categorias activas. Se recomienda al menos 10.')
            )

