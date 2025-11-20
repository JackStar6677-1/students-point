"""Script de prueba rapida para la API de cursos"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
django.setup()

from studentspoint.apps.otec.models import Curso
from studentspoint.apps.accounts.models import User

def test_cursos():
    print("=== TEST DE CURSOS ===\n")
    
    # Contar cursos
    total = Curso.objects.count()
    print(f"Total de cursos en la BD: {total}")
    
    # Mostrar cursos
    cursos = Curso.objects.all()[:5]
    print(f"\nPrimeros 5 cursos:")
    for curso in cursos:
        print(f"  - {curso.titulo} ({curso.tipo}) - {curso.autor.name}")
    
    # Estadisticas
    personales = Curso.objects.filter(tipo='personal').count()
    externos = Curso.objects.filter(tipo='externo').count()
    gratuitos = Curso.objects.filter(es_gratuito=True).count()
    
    print(f"\nEstadisticas:")
    print(f"  Clases privadas: {personales}")
    print(f"  Cursos externos: {externos}")
    print(f"  Gratuitos: {gratuitos}")
    
    # Verificar usuarios
    print(f"\nTotal de usuarios: {User.objects.count()}")
    
if __name__ == '__main__':
    test_cursos()

