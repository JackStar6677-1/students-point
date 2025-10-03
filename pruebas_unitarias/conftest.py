import os
import sys
import pathlib

# Asegurar que Django (backend) esté en PYTHONPATH
# Nota: este archivo vive en <repo>/pruebas_unitarias/conftest.py
# parents[1] → raíz del repo. Desde ahí navegamos a proyecto/src/backend
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1] / 'proyecto' / 'src' / 'backend'
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')


