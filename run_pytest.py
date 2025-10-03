"""
Runner de pytest que prepara el entorno de Django antes de invocar pytest.

Uso:
  python run_pytest.py -q
"""

import os
import sys
from pathlib import Path
import pytest


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    backend_root = repo_root / 'proyecto' / 'src' / 'backend'
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')

    args = sys.argv[1:] or []
    return pytest.main(args)


if __name__ == '__main__':
    raise SystemExit(main())


