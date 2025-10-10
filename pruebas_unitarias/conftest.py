import os
import sys
import pathlib
import logging
import pytest
from datetime import datetime

# Asegurar que Django (backend) esté en PYTHONPATH
# Nota: este archivo vive en <repo>/pruebas_unitarias/conftest.py
# parents[1] → raíz del repo. Desde ahí navegamos a proyecto/src/backend
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1] / 'proyecto' / 'src' / 'backend'
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.base')

# Configurar logs de tests
TEST_LOGS_DIR = pathlib.Path(__file__).resolve().parents[1] / 'logs_tests'
TEST_LOGS_DIR.mkdir(exist_ok=True)

# Hooks de pytest para logging detallado
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configurar logging antes de ejecutar tests"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Archivos de log
    log_file = TEST_LOGS_DIR / f'pytest_{timestamp}.log'
    errors_log = TEST_LOGS_DIR / 'pytest_errors_latest.log'
    summary_log = TEST_LOGS_DIR / 'pytest_summary_latest.log'
    
    # Configurar handler de archivo
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s [%(name)s] %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Handler de errores
    error_handler = logging.FileHandler(errors_log, mode='w', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Aplicar a logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Deshabilitar logs de Django admin durante tests
    logging.getLogger('django.db.backends').setLevel(logging.WARNING)
    
    # Guardar info de configuracion
    config.test_logs_dir = TEST_LOGS_DIR
    config.test_log_file = log_file
    config.test_summary_file = summary_log
    
    print(f"\n{'='*70}")
    print(f"CONFIGURACION DE LOGS PARA TESTS")
    print(f"{'='*70}")
    print(f"Directorio: {TEST_LOGS_DIR}")
    print(f"Log general: {log_file.name}")
    print(f"Log errores: {errors_log.name}")
    print(f"{'='*70}\n")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Log antes de cada test"""
    logger = logging.getLogger('tests')
    logger.info(f"{'='*60}")
    logger.info(f"INICIANDO TEST: {item.nodeid}")
    logger.info(f"{'='*60}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """Log del resultado de cada test"""
    logger = logging.getLogger('tests')
    
    if report.when == 'call':
        if report.passed:
            logger.info(f"[PASSED] {report.nodeid}")
        elif report.failed:
            logger.error(f"[FAILED] {report.nodeid}")
            if hasattr(report, 'longrepr'):
                logger.error(f"Error: {report.longrepr}")
        elif report.skipped:
            logger.warning(f"[SKIPPED] {report.nodeid}")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Generar resumen al finalizar tests"""
    if hasattr(session.config, 'test_summary_file'):
        summary_file = session.config.test_summary_file
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("RESUMEN DE EJECUCION DE TESTS - StudentsPoint\n")
            f.write("="*70 + "\n\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Directorio de logs: {session.config.test_logs_dir}\n")
            f.write(f"Exit status: {exitstatus}\n\n")
            
            # Obtener estadisticas
            if hasattr(session, 'testscollected'):
                f.write(f"Tests ejecutados: {session.testscollected}\n")
            if hasattr(session, 'testsfailed'):
                f.write(f"Tests fallidos: {session.testsfailed}\n")
            
            f.write("\nPara ver logs detallados:\n")
            f.write(f"  - Log completo: {session.config.test_log_file.name}\n")
            f.write(f"  - Solo errores: pytest_errors_latest.log\n")
            f.write(f"  - Este resumen: pytest_summary_latest.log\n")
            f.write("\n" + "="*70 + "\n")
        
        print(f"\nResumen guardado en: {summary_file}")

