from .base import *

DEBUG = True

# Permitir todos los hosts en desarrollo (incluye ngrok)
ALLOWED_HOSTS = ["*"]

# Para producción, usar lista específica:
# ALLOWED_HOSTS = [
#     "localhost",
#     "127.0.0.1",
#     "0.0.0.0",
#     "192.168.100.2",
#     "192.168.100.6",
#     "192.168.100.59",
#     "100.75.238.19",  # Tailscale IP - jackstar6677-laptop
#     "100.113.204.115",  # Tailscale - desktop
#     "*.ngrok.io",  # Dominios de ngrok
#     "*.ngrok-free.app",  # Nuevos dominios de ngrok
# ]

# SSL Server para HTTPS en desarrollo (PWA en Android)
INSTALLED_APPS = INSTALLED_APPS + ['sslserver'] if 'sslserver' not in INSTALLED_APPS else INSTALLED_APPS

# CSRF - En desarrollo, confiar en todos los orígenes (incluye ngrok)
# IMPORTANTE: En producción, usar lista específica
CSRF_TRUSTED_ORIGINS = [
    # HTTP
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://192.168.100.2:8000",
    "http://192.168.100.1:8000",
    "http://192.168.1.1:8000",
    "http://192.168.0.1:8000",
    "http://192.168.100.6:8000",
    "http://192.168.100.59:8000",
    "http://100.75.238.19:8000",  # Tailscale - laptop
    "http://100.113.204.115:8000",  # Tailscale - desktop
    # HTTPS (para PWA en Android)
    "https://localhost:8000",
    "https://localhost:8443",
    "https://127.0.0.1:8000",
    "https://127.0.0.1:8443",
    "https://100.75.238.19:8000",
    "https://100.75.238.19:8443",  # HTTPS Tailscale - laptop
    "https://100.113.204.115:8000",
    "https://100.113.204.115:8443",  # HTTPS Tailscale - desktop
]

# Permitir dominios de ngrok dinámicamente
import os
if os.getenv('DJANGO_SETTINGS_MODULE', '').endswith('.dev'):
    # En desarrollo, agregar patrones de ngrok
    ngrok_patterns = [
        "https://*.ngrok.io",
        "https://*.ngrok-free.app",
        "http://*.ngrok.io",
        "http://*.ngrok-free.app",
    ]
    # Nota: Django no soporta wildcards en CSRF_TRUSTED_ORIGINS directamente
    # pero ALLOWED_HOSTS = ["*"] permitirá el acceso

# Deshabilitar CSRF para APIs REST
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Permitir CORS para desarrollo
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# (única definición) CSRF_TRUSTED_ORIGINS definida arriba

# (única definición) ALLOWED_HOSTS definida arriba

# Configuración para servir archivos estáticos en desarrollo
# (STATICFILES_DIRS se define en base.py - no sobrescribir aquí)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuracion de Email - SMTP Real para desarrollo
# Usa credenciales reales para enviar emails de verificacion
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pablo.elias.miranda.292003@gmail.com'
EMAIL_HOST_PASSWORD = 'dpak rpok esau zxdl'  # App Password de Gmail
DEFAULT_FROM_EMAIL = 'StudentsPoint <pablo.elias.miranda.292003@gmail.com>'

# Google OAuth - Credenciales de desarrollo
GOOGLE_CLIENT_ID = '307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/api/auth/google/callback/web/'
FRONTEND_URL = 'http://localhost:8000'