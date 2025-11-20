#!/usr/bin/env python
"""Script para probar la API de productos"""
import sys
import os

# Add the project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings')

import django
django.setup()

from studentspoint.apps.market.models import Producto

productos = Producto.objects.filter(estado='publicado').order_by('-id')[:10]

print(f"Total productos publicados: {productos.count()}")
print("\nProductos:")
for p in productos:
    print(f"  {p.id}: {p.titulo[:50]}")

