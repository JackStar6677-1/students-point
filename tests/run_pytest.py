"""
Runner de pytest que prepara el entorno de Django antes de invocar pytest.

Uso:
  python run_pytest.py -q
"""

import os
import sys
from pathlib import Path
import pytest
import django


def main() -> int:
    # Ubicar raíz del repo y backend
    tests_dir = Path(__file__).resolve().parent
    repo_root = tests_dir.parent
    backend_root = repo_root / 'proyecto' / 'src' / 'backend'
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')
    # Inicializar Django para evitar AppRegistryNotReady
    django.setup()

    args = sys.argv[1:] or []
    return pytest.main(args)


if __name__ == '__main__':
    raise SystemExit(main())


