"""
Runner para descubrir y ejecutar pruebas E2E en ./pruebas_automatizadas.

Uso:
  python run_pruebas.py

Variables de entorno útiles:
- E2E_HEADLESS=1       -> Ejecuta en modo headless
- E2E_KEEP_OPEN=1      -> No cierra el navegador al terminar
- E2E_CLOSE_DELAY=10   -> Espera N segundos antes de cerrar
"""

import unittest


def main() -> None:
    test_suite = unittest.defaultTestLoader.discover(
        start_dir="pruebas_automatizadas",
        pattern="test_*.py",
        top_level_dir=None,
    )
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()


