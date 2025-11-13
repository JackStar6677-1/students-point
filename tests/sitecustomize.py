"""Auto-ajustes de ruta para pytest y herramientas CLI.

Python importa automáticamente este módulo si está en sys.path.
Insertamos `proyecto/src/backend` para que el paquete Django `studentspoint`
sea importable sin configurar PYTHONPATH manualmente.
"""

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
BACKEND_ROOT = REPO_ROOT / 'proyecto' / 'src' / 'backend'

for path in (str(BACKEND_ROOT), str(REPO_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

# Evitar conflictos de nombres con management commands llamados test_*
legacy_module = sys.modules.get('test_email_verification')
if (
    legacy_module
    and hasattr(legacy_module, '__file__')
    and 'management\\commands\\test_email_verification.py' in legacy_module.__file__
):
    sys.modules.pop('test_email_verification', None)


