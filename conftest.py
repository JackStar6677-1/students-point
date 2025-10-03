import os
import sys
from pathlib import Path

# Asegurar que el paquete Django (studentspoint) sea importable
BACKEND_ROOT = Path(__file__).resolve().parent / 'proyecto' / 'src' / 'backend'
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')


