from pathlib import Path
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
    "studentspoint.apps.schedules",
    "studentspoint.apps.wellbeing",
    "marketplace",
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
# Configurar archivos estáticos del frontend
STATICFILES_DIRS = [BASE_DIR.parent / "frontend/static"]

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
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@studentspoint.app')