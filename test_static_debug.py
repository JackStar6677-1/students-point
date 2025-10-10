#!/usr/bin/env python
"""Script para depurar el problema de archivos estáticos"""
import os
import sys
from pathlib import Path

# Configurar Django
sys.path.insert(0, 'proyecto/src/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')

import django
django.setup()

from django.test import Client
from django.urls import resolve, get_resolver
from django.conf import settings

print("=" * 60)
print("DEBUG: Archivos Estáticos")
print("=" * 60)

# 1. Verificar configuración
print("\n1. CONFIGURACIÓN:")
print(f"   STATIC_URL: {settings.STATIC_URL}")
print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"   DEBUG: {settings.DEBUG}")

# 2. Verificar archivo existe
css_path = Path(settings.STATIC_ROOT) / "static" / "css" / "theme-dark.css"
print(f"\n2. ARCHIVO:")
print(f"   Path: {css_path}")
print(f"   Existe: {css_path.exists()}")
if css_path.exists():
    print(f"   Tamaño: {css_path.stat().st_size} bytes")

# 3. Probar resolución de URL
print(f"\n3. RESOLUCIÓN DE URL:")
try:
    match = resolve('/static/css/theme-dark.css')
    print(f"   Vista: {match.func}")
    print(f"   Args: {match.args}")
    print(f"   Kwargs: {match.kwargs}")
except Exception as e:
    print(f"   ERROR: {e}")

# 4. Probar con cliente de test
print(f"\n4. TEST CON CLIENTE:")
client = Client()
response = client.get('/static/css/theme-dark.css')
print(f"   Status: {response.status_code}")
print(f"   Content-Type: {response.get('Content-Type', 'N/A')}")
print(f"   Content length: {len(response.content)} bytes")

if response.status_code == 404:
    print(f"   Content preview: {response.content[:200]}")

# 5. Listar patrones de URL
print(f"\n5. PATRONES DE URL (primeros 20):")
resolver = get_resolver()
for i, pattern in enumerate(resolver.url_patterns[:20]):
    print(f"   {i}: {pattern.pattern}")

print("\n" + "=" * 60)

