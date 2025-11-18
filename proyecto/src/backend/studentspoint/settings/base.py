from pathlib import Path
from datetime import timedelta
import os

# base.py está en: server/studentspoint/settings/base.py
# Queremos que BASE_DIR sea: server/
BASE_DIR = Path(__file__).resolve().parents[2]

# ---- Seguridad / debug ----
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ---- Apps ----
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # Para blacklist de tokens
    "django_filters",

    # Local apps (ajusta nombres si cambiaste rutas)
    "studentspoint.apps.accounts",
    "studentspoint.apps.campuses",
    "studentspoint.apps.forum",
    "studentspoint.apps.health",
    "studentspoint.apps.market",
    "studentspoint.apps.notifications",
    "studentspoint.apps.otec",
    "studentspoint.apps.polls",
    "studentspoint.apps.portfolio",
    "studentspoint.apps.reports",
    "studentspoint.apps.wellbeing",
    "studentspoint.apps.document_converter",
    "campus_map",
    "infrastructure_monitoring",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "studentspoint.middleware.DisableCSRFMiddleware",  # Deshabilitar CSRF para APIs
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "studentspoint.middleware.QueryCountDebugMiddleware",  # Detectar N+1 queries
    "studentspoint.middleware.RequestLoggingMiddleware",  # Loggear peticiones
]

ROOT_URLCONF = "studentspoint.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # opcional, si usas templates globales
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "studentspoint.wsgi.application"
ASGI_APPLICATION = "studentspoint.asgi.application"  # por si luego usas Channels/WebSockets

# ---- Base de datos ----
# SQLite para desarrollo, PostgreSQL para producción
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
    }
}

# Configuración específica para PostgreSQL en producción
if os.getenv("DB_ENGINE") == "django.db.backends.postgresql":
    DATABASES["default"].update({
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "CONN_MAX_AGE": 600,  # Conexiones persistentes
    })

# ---- Idioma / zona horaria ----
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ---- Archivos estáticos y media ----
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Los archivos de frontend/static/ van directamente a staticfiles/ (no a staticfiles/static/)
# Los HTMLs de frontend/ van también a staticfiles/
STATICFILES_DIRS = [
    ("", BASE_DIR.parent / "frontend" / "static"),  # CSS, JS, images, audio → staticfiles/
    ("", BASE_DIR.parent / "frontend"),  # HTMLs y otras carpetas → staticfiles/
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

# ---- DRF ----
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "1000/day", "anon": "100/day"},
}

# ---- JWT Authentication ----
SIMPLE_JWT = {
    # Tokens de acceso duran 60 minutos (1 hora)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Tokens de refresh duran 7 días
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    
    # Rotación de refresh tokens (seguridad adicional)
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    
    # Configuración del algoritmo
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    
    # Headers
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    
    # Claims personalizados
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    
    # Configuración de tokens
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    
    # Actualizar el last_login del usuario al generar token
    "UPDATE_LAST_LOGIN": True,
}

if os.getenv("DEMO_MODE") == "1":
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = []
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny"
    ]

SPECTACULAR_SETTINGS = {
    "TITLE": "StudentsPoint API",
    "DESCRIPTION": "API para la plataforma StudentsPoint - PWA estudiantil",
    "VERSION": "1.0.0",
}


# ---- CORS ----
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")


# ---- Google OAuth (DESHABILITADO) ----
# GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")


# ---- Google Maps/Street View (DESHABILITADO - USAMOS STREET VIEW PERSONALIZADO) ----
# GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")


# ---- Celery ----
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

# ---- OAuth de Google ----
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "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")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback/web/")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

# ---- Configuracion de Email ----
# Por defecto usa console (mostrar en terminal)
# dev.py y prod.py pueden sobrescribir estas configuraciones
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@studentspoint.app')

# ---- Configuración de Logging ----
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {funcName} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {asctime} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'general.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'api.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'file_auth': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'auth.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        'studentspoint': {
            'handlers': ['console', 'file_api'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'studentspoint.apps.accounts': {
            'handlers': ['console', 'file_auth'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'studentspoint.apps.forum': {
            'handlers': ['console', 'file_api'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_general'],
        'level': 'INFO',
    },
}