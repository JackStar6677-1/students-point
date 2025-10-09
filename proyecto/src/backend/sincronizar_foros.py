#!/usr/bin/env python
"""Script para sincronizar foros con carreras disponibles."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings')
django.setup()

from studentspoint.apps.forum.models import Foro
from studentspoint.apps.campuses.models import Sede
from studentspoint.apps.accounts.models import CARRERAS_DISPONIBLES
from django.utils.text import slugify

def sincronizar_foros():
    """Crea foros para todas las carreras disponibles."""
    
    # Obtener o crear sede por defecto
    sede, created = Sede.objects.get_or_create(
        slug="sede-central",
        defaults={
            "nombre": "Sede Central",
            "lat": -33.4489,
            "lng": -70.6693
        }
    )
    
    if created:
        print(f"✅ Sede creada: {sede.nombre}")
    
    foros_creados = 0
    foros_existentes = 0
    
    for carrera in CARRERAS_DISPONIBLES:
        slug = f"{sede.slug}-{slugify(carrera)}"
        
        foro, created = Foro.objects.get_or_create(
            sede=sede,
            carrera=carrera,
            defaults={
                "titulo": f"{carrera} - {sede.nombre}",
                "slug": slug,
                "es_privado": False,
                "descripcion": f"Foro para estudiantes de {carrera}"
            }
        )
        
        if created:
            print(f"✅ Foro creado: {foro.titulo}")
            foros_creados += 1
        else:
            foros_existentes += 1
    
    print(f"\n📊 Resumen:")
    print(f"   Foros creados: {foros_creados}")
    print(f"   Foros existentes: {foros_existentes}")
    print(f"   Total de foros: {Foro.objects.count()}")
    
    print(f"\n📋 Foros disponibles:")
    for foro in Foro.objects.all().order_by('carrera'):
        print(f"   - {foro.titulo} (Carrera: {foro.carrera})")

if __name__ == "__main__":
    print("🔄 Sincronizando foros con carreras disponibles...\n")
    sincronizar_foros()
    print("\n✅ Sincronización completada!")

