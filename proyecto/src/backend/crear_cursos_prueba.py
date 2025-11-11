"""Script para crear cursos de prueba"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
django.setup()

from studentspoint.apps.otec.models import Curso
from studentspoint.apps.accounts.models import User

def crear_cursos_prueba():
    print("=== CREANDO CURSOS DE PRUEBA ===\n")
    
    # Obtener un usuario
    usuario = User.objects.first()
    if not usuario:
        print("ERROR: No hay usuarios en la base de datos")
        return
    
    print(f"Usando usuario: {usuario.name} ({usuario.email})")
    
    # Crear cursos de ejemplo
    cursos_data = [
        {
            'titulo': 'Clases particulares de Python',
            'descripcion': 'Ofrezco clases de Python para principiantes. Incluye ejercicios practicos y proyectos.',
            'tipo': 'personal',
            'categoria': 'Programacion',
            'modalidad': 'online',
            'nivel': 'principiante',
            'duracion': '8 semanas',
            'precio': 50000,
            'email_contacto': 'profesor@example.com',
            'telefono_contacto': '+56912345678',
            'fecha_inicio': date.today(),
        },
        {
            'titulo': 'Curso Completo de React en Udemy',
            'descripcion': 'Curso gratuito de React con hooks y contexto. Ideal para principiantes.',
            'tipo': 'externo',
            'categoria': 'Desarrollo Web',
            'modalidad': 'online',
            'nivel': 'intermedio',
            'es_gratuito': True,
            'url': 'https://udemy.com/curso-react',
            'fecha_inicio': date.today(),
        },
        {
            'titulo': 'Tutorías de Cálculo y Álgebra',
            'descripcion': 'Ayudo con matematicas universitarias. Metodo practico y efectivo.',
            'tipo': 'personal',
            'categoria': 'Matematicas',
            'modalidad': 'presencial',
            'nivel': 'todos',
            'duracion': 'Flexible',
            'precio': 30000,
            'email_contacto': 'tutor.matematicas@example.com',
            'fecha_inicio': date.today(),
        },
        {
            'titulo': 'Diseño UX/UI en Coursera',
            'descripcion': 'Curso de Google sobre diseño de interfaces. Certificado profesional.',
            'tipo': 'externo',
            'categoria': 'Diseño',
            'modalidad': 'online',
            'nivel': 'principiante',
            'precio': 150000,
            'url': 'https://coursera.org/ux-design',
            'fecha_inicio': date.today(),
            'fecha_fin': date.today() + timedelta(days=90),
        },
        {
            'titulo': 'Clases de Inglés Conversacional',
            'descripcion': 'Practica tu ingles con clases dinamicas y divertidas.',
            'tipo': 'personal',
            'categoria': 'Idiomas',
            'modalidad': 'hibrido',
            'nivel': 'intermedio',
            'duracion': '12 semanas',
            'precio': 40000,
            'telefono_contacto': '+56987654321',
            'url': 'https://wa.me/56987654321',
            'fecha_inicio': date.today(),
        },
    ]
    
    creados = 0
    for curso_data in cursos_data:
        # Verificar si ya existe
        if Curso.objects.filter(titulo=curso_data['titulo']).exists():
            print(f"- Ya existe: {curso_data['titulo']}")
            continue
            
        curso = Curso.objects.create(
            autor=usuario,
            **curso_data
        )
        print(f"+ Creado: {curso.titulo}")
        creados += 1
    
    print(f"\n{creados} cursos nuevos creados")
    print(f"Total de cursos en la BD: {Curso.objects.count()}")

if __name__ == '__main__':
    crear_cursos_prueba()

