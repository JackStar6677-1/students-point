#!/usr/bin/env python3
"""
Script para verificar la configuración de Google OAuth
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
django.setup()

from django.conf import settings
from studentspoint.apps.accounts.oauth import GoogleOAuthService

def check_oauth_config():
    """Verificar configuración de OAuth"""
    print(" Verificando configuración de Google OAuth")
    print("=" * 50)
    
    # Verificar configuración básica
    print(f"Client ID: {getattr(settings, 'GOOGLE_CLIENT_ID', 'No configurado')}")
    print(f"Client Secret: {'*' * 20}...{getattr(settings, 'GOOGLE_CLIENT_SECRET', 'No configurado')[-4:]}")
    print(f"Redirect URI: {getattr(settings, 'GOOGLE_REDIRECT_URI', 'No configurado')}")
    print(f"Frontend URL: {getattr(settings, 'FRONTEND_URL', 'No configurado')}")
    print()
    
    # Verificar servicio OAuth
    try:
        service = GoogleOAuthService()
        print(" Servicio OAuth inicializado correctamente")
        print(f"   - Client ID: {service.client_id}")
        print(f"   - Redirect URI: {service.redirect_uri}")
        print(f"   - Scopes: {', '.join(service.scopes)}")
        print()
        
        # Generar URL de autorización
        auth_url, state = service.get_authorization_url()
        print(" URL de autorización generada correctamente")
        print(f"   - Auth URL: {auth_url[:100]}...")
        print(f"   - State: {state}")
        print()
        
    except Exception as e:
        print(f" Error inicializando servicio OAuth: {e}")
        return False
    
    # Verificar URLs que deben estar en Google Cloud Console
    print(" URLs que deben estar configuradas en Google Cloud Console:")
    print("   URIs de redirección autorizadas:")
    print("   - http://localhost:8000/api/auth/google/callback/web/")
    print("   - http://127.0.0.1:8000/api/auth/google/callback/web/")
    print("   - https://studentspoint.app/api/auth/google/callback/web/")
    print()
    
    print(" Orígenes JavaScript autorizados:")
    print("   - http://localhost:8000")
    print("   - http://127.0.0.1:8000")
    print("   - https://studentspoint.app")
    print()
    
    print(" Configuración verificada correctamente")
    return True

if __name__ == "__main__":
    try:
        check_oauth_config()
    except Exception as e:
        print(f" Error verificando configuración: {e}")
        sys.exit(1)

