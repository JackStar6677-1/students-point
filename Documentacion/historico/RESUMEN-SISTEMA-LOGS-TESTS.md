# Sistema de Logging para Tests - Implementado

## Resumen

Se ha implementado un sistema completo de logging para tests que genera archivos detallados automaticamente en cada ejecucion.

---

## Archivos Creados

### Configuracion
1. **conftest.py** (raiz) - Configuracion global de logging
2. **pruebas_unitarias/conftest.py** - Hooks de pytest para logging detallado
3. **settings/test.py** - Configuracion Django especifica para tests

### Scripts de Visualizacion
4. **ver_logs_tests.bat** - Menu interactivo Windows
5. **ver_logs_tests.sh** - Menu interactivo Linux

### Documentacion
6. **logs_tests/README.md** - Documentacion del directorio
7. **logs_tests/.gitignore** - Ignorar logs pero mantener estructura
8. **GUIA-LOGS-TESTS.md** - Guia completa de uso

---

## Logs Generados Automaticamente

Al ejecutar `python run_pytest.py`, se generan:

### Archivos por Ejecucion (con timestamp)
```
logs_tests/
├── pytest_20251009_215112.log           - Log general de pytest
├── test_run_20251009_215112.log         - Log basico
└── test_detailed_20251009_215112.log    - Log detallado con lineas
```

### Archivos Permanentes (ultimos)
```
logs_tests/
├── pytest_errors_latest.log      - Ultimos errores
├── pytest_summary_latest.log     - Resumen de ejecucion
├── tests_execution.log           - Acumulativo general
└── tests_errors.log              - Acumulativo errores
```

---

## Informacion en los Logs

### Inicio de Sesion
```
======================================================================
CONFIGURACION DE LOGS PARA TESTS
======================================================================
Directorio: C:\...\logs_tests
Log general: pytest_20251009_215112.log
Log errores: pytest_errors_latest.log
======================================================================
```

### Por Cada Test
```
[INFO] ============================================================
[INFO] INICIANDO TEST: test_auth_me.py::test_auth_me_requires_token
[INFO] ============================================================
[DEBUG] Operaciones del test...
[INFO] [PASSED] test_auth_me.py::test_auth_me_requires_token
```

### Cuando Falla
```
[ERROR] [FAILED] test_forum_api.py::test_create_post
[ERROR] Error: AssertionError: 400 != 201
[ERROR] Traceback completo...
```

---

## Como Usar

### Ejecutar Tests
```bash
python run_pytest.py
```

Los logs se generan automaticamente en `logs_tests/`

### Ver Logs

#### Windows
```batch
ver_logs_tests.bat
```

Menu con opciones:
1. Resumen de ultima ejecucion
2. Errores de tests
3. Log completo
4. Log detallado
5. Listar todos los logs
6. Limpiar logs antiguos

#### Linux/Mac
```bash
chmod +x ver_logs_tests.sh
./ver_logs_tests.sh
```

#### Manual
```powershell
# Windows
Get-Content logs_tests\pytest_errors_latest.log

# Linux
cat logs_tests/pytest_errors_latest.log
```

---

## Formato de Logs

### Log General
```
[INFO] 2025-10-09 21:51:12 [tests] - Test iniciado
[DEBUG] 2025-10-09 21:51:13 [tests.test_auth] - Creando usuario
```

### Log Detallado
```
[DEBUG] 2025-10-09 21:51:13 [tests.test_auth].test_login:45 - Creando usuario
[INFO] 2025-10-09 21:51:14 [studentspoint.apps.accounts].login:123 - Login OK
```

### Log de Errores
```
[ERROR] [FAILED] test_forum_api.py::test_create_post
[ERROR] Error: AssertionError: 400 != 201
```

---

## Ventajas

1. **Historial completo** - Cada ejecucion genera su log con timestamp
2. **Debugging facil** - Logs detallados con lineas de codigo
3. **Acceso rapido** - Scripts interactivos
4. **Sin emojis** - Formato profesional
5. **Resumen automatico** - Estadisticas al finalizar
6. **Separacion de errores** - Archivo especifico para errores
7. **Formato consistente** - Mismo formato que logs de desarrollo

---

## Ejecucion de Tests con Logs

```
C:\...\students-point> python run_pytest.py

======================================================================
CONFIGURACION DE LOGS PARA TESTS
======================================================================
Directorio: C:\...\logs_tests
Log general: pytest_20251009_215112.log
Log errores: pytest_errors_latest.log
======================================================================

[Ejecucion de tests...]

33 tests ejecutados
24 passed
9 failed

Logs guardados en: logs_tests/
```

---

## Estado Actual de Tests

**Ejecucion:** 9 de Octubre 2025, 21:51

**Resultados:**
- Total: 33 tests
- Passed: 24
- Failed: 9

**Tests fallidos:**
- test_email_verification (2 tests)
- test_forum_api (7 tests)
- test_profile_api (1 test con cambio de carrera)

**Todos los errores estan loggeados en:** `logs_tests/pytest_errors_latest.log`

---

## Próximos Pasos

Los logs estan listos para que el equipo de testing:

1. Ejecute tests con `python run_pytest.py`
2. Revise logs con `ver_logs_tests.bat`
3. Identifique problemas especificos en logs detallados
4. Corrija tests fallidos
5. Re-ejecute y compare logs

Los logs se generan automaticamente - no requiere configuracion adicional.

---

Fecha: 9 de Octubre 2025
Version: 1.0.0
Estado: Funcional
Commit: ba2d971 (pusheado a main)

