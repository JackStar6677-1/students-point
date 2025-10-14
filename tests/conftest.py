import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Asegurar que el paquete Django (studentspoint) sea importable
BACKEND_ROOT = Path(__file__).resolve().parent / 'proyecto' / 'src' / 'backend'
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')

# Configurar directorio de logs para tests
TEST_LOGS_DIR = Path(__file__).resolve().parent / 'logs_tests'
TEST_LOGS_DIR.mkdir(exist_ok=True)

# Configurar logging para tests
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = TEST_LOGS_DIR / f'test_run_{timestamp}.log'
detailed_log = TEST_LOGS_DIR / f'test_detailed_{timestamp}.log'
errors_log = TEST_LOGS_DIR / 'test_errors_latest.log'

# Configuracion de logging para tests
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Handler adicional para logs detallados
detailed_handler = logging.FileHandler(detailed_log, mode='w', encoding='utf-8')
detailed_handler.setLevel(logging.DEBUG)
detailed_formatter = logging.Formatter(
    '[%(levelname)s] %(asctime)s %(name)s.%(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
detailed_handler.setFormatter(detailed_formatter)

# Handler para errores
error_handler = logging.FileHandler(errors_log, mode='w', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(detailed_formatter)

# Aplicar handlers al logger raiz
root_logger = logging.getLogger()
root_logger.addHandler(detailed_handler)
root_logger.addHandler(error_handler)

# Logger para tests
test_logger = logging.getLogger('tests')
test_logger.setLevel(logging.DEBUG)

print(f"\n{'='*70}")
print(f"LOGS DE TESTS - StudentsPoint")
print(f"{'='*70}")
print(f"Log general: {log_file.name}")
print(f"Log detallado: {detailed_log.name}")
print(f"Log errores: {errors_log.name}")
print(f"Directorio: {TEST_LOGS_DIR}")
print(f"{'='*70}\n")

