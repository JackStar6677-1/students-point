"""
Configuracion especifica para tests
"""
from .base import *

# Deshabilitar debugging durante tests para mas velocidad
DEBUG = False

# Base de datos en memoria para tests mas rapidos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Deshabilitar migraciones para tests mas rapidos
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Logging especifico para tests
LOGS_DIR = BASE_DIR / "logs_tests"
LOGS_DIR.mkdir(exist_ok=True)

# Configurar logging para tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s [%(name)s] %(funcName)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(levelname)s] %(asctime)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_test': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'tests_execution.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
        'file_test_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'tests_errors.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
        'file_test_api': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'tests_api.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_test'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_test_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'tests': {
            'handlers': ['console', 'file_test', 'file_test_errors'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'studentspoint': {
            'handlers': ['file_test_api'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_test'],
        'level': 'INFO',
    },
}

# Password hashers mas rapidos para tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Deshabilitar middleware pesado durante tests
MIDDLEWARE = [m for m in MIDDLEWARE if 'QueryCountDebugMiddleware' not in m]

# Email backend para tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Deshabilitar throttling en tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
