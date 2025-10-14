"""Auto-ajustes de ruta para pytest y herramientas CLI.

Python importa automáticamente este módulo si está en sys.path.
Insertamos `proyecto/src/backend` para que el paquete Django `studentspoint`
sea importable sin configurar PYTHONPATH manualmente.
"""

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent / 'proyecto' / 'src' / 'backend'
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


