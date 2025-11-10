# Guia de Logs para Tests - StudentsPoint

## Descripcion

El sistema genera logs automaticos y detallados cada vez que se ejecutan los tests. Estos logs ayudan a identificar problemas, debuggear tests fallidos y mantener un historial de ejecuciones.

---

## Ubicacion de Logs

**Directorio:** `logs_tests/`

Este directorio se crea automaticamente al ejecutar tests por primera vez.

---

## Archivos Generados

### Archivos por Ejecucion

#### pytest_[timestamp].log
Log general de cada ejecucion de pytest con timestamp.

**Ejemplo:** `pytest_20251009_163000.log`

**Contiene:**
- Configuracion de la sesion
- Lista de tests ejecutados
- Resultados (PASSED/FAILED/SKIPPED)
- Warnings y mensajes

#### test_run_[timestamp].log
Log basico de ejecucion con informacion general.

#### test_detailed_[timestamp].log
Log detallado con numeros de linea y funciones especificas.

**Formato:**
```
[DEBUG] 2025-10-09 16:30:01 [tests.test_auth].test_login:45 - Creando usuario de prueba
[INFO] 2025-10-09 16:30:02 [studentspoint.apps.accounts].login:123 - Login exitoso
```

### Archivos Permanentes

#### pytest_errors_latest.log
Contiene solo los errores de la ultima ejecucion de pytest.
Se sobrescribe en cada ejecucion.

#### pytest_summary_latest.log
Resumen de la ultima ejecucion con estadisticas.

**Contiene:**
- Fecha y hora
- Total de tests
- Tests fallidos
- Exit status
- Links a otros logs

#### tests_execution.log
Log acumulativo de todas las ejecuciones.
Se va agregando contenido (no se sobrescribe).

#### tests_errors.log
Log acumulativo de errores.
Se va agregando contenido.

---

## Ejecucion de Tests

### Ejecutar con Logs

```bash
# Tests completos (logs se generan automaticamente)
python run_pytest.py

# Tests especificos
pytest pruebas_unitarias/api/test_forum_api.py -v

# Tests con mas verbosidad
pytest -vv
```

### Salida en Consola

Al ejecutar tests, veras:

```
======================================================================
CONFIGURACION DE LOGS PARA TESTS
======================================================================
Directorio: C:\...\logs_tests
Log general: pytest_20251009_163000.log
Log errores: pytest_errors_latest.log
======================================================================

[Ejecucion de tests...]

Resumen guardado en: logs_tests\pytest_summary_latest.log
```

---

## Ver Logs de Tests

### Opcion 1: Scripts Interactivos (Recomendado)

#### Windows
```batch
ver_logs_tests.bat
```

#### Linux/Mac
```bash
chmod +x ver_logs_tests.sh
./ver_logs_tests.sh
```

**Menu con opciones:**
1. Resumen de ultima ejecucion
2. Errores de tests
3. Log completo
4. Log detallado
5. Ver todos los logs
6. Limpiar logs antiguos

### Opcion 2: Manual

#### Windows PowerShell
```powershell
cd logs_tests

# Ver resumen
type pytest_summary_latest.log

# Ver errores
type pytest_errors_latest.log

# Ver ultimas 50 lineas del log completo
Get-Content tests_execution.log -Tail 50

# Buscar un test especifico
Get-Content tests_execution.log | Select-String "test_login"
```

#### Linux/Mac
```bash
cd logs_tests

# Ver resumen
cat pytest_summary_latest.log

# Ver errores
cat pytest_errors_latest.log

# Ver log completo (ultimas 50 lineas)
tail -n 50 tests_execution.log

# Ver en tiempo real (si ejecutas tests en otra terminal)
tail -f tests_execution.log

# Buscar un test especifico
grep "test_login" tests_execution.log
```

---

## Informacion en los Logs

### Cada Test Loggea

1. **Inicio del test**
```
[INFO] ============================================================
[INFO] INICIANDO TEST: pruebas_unitarias/api/test_auth_me.py::test_auth_me_requires_token
[INFO] ============================================================
```

2. **Operaciones realizadas**
```
[DEBUG] Creando usuario de prueba: test@example.com
[DEBUG] Enviando peticion GET a /api/auth/me/
[INFO] Respuesta recibida: 401 Unauthorized
```

3. **Resultado**
```
[INFO] [PASSED] pruebas_unitarias/api/test_auth_me.py::test_auth_me_requires_token
```

O si falla:
```
[ERROR] [FAILED] pruebas_unitarias/api/test_login_api.py::test_login_invalid
[ERROR] Error: AssertionError: 200 != 400
```

### Logs de Errores

Cuando un test falla, se loggea:
- Nombre completo del test
- Error especifico (AssertionError, ValueError, etc)
- Traceback completo
- Valores esperados vs obtenidos
- Contexto adicional

**Ejemplo:**
```
[ERROR] [FAILED] test_forum_api.py::test_create_post
[ERROR] Error: AssertionError: 400 != 201
Expected status 201 but got 400
Response data: {'error': 'Validation failed'}

Traceback:
  File "test_forum_api.py", line 50, in test_create_post
    self.assertEqual(response.status_code, 201)
```

---

## Configuracion de Logging

### Archivo: conftest.py (raiz del proyecto)
Configura logging general para todos los tests.

### Archivo: pruebas_unitarias/conftest.py
Configura hooks de pytest para logging detallado:
- pytest_configure: Setup inicial
- pytest_runtest_setup: Antes de cada test
- pytest_runtest_logreport: Despues de cada test
- pytest_sessionfinish: Resumen final

### Archivo: settings/test.py
Configuracion especifica de Django para tests con logging optimizado.

---

## Casos de Uso

### Debuggear Test Fallido

1. Ejecutar tests:
   ```bash
   python run_pytest.py
   ```

2. Ver errores:
   ```bash
   ver_logs_tests.bat
   # Opcion 2: Errores
   ```

3. Ver contexto completo:
   ```bash
   # Buscar el test especifico en log detallado
   grep -A 20 "test_login_invalid" logs_tests/test_detailed_*.log
   ```

4. Identificar el problema en el traceback

5. Corregir y volver a ejecutar

### Revisar Ejecucion Anterior

```bash
# Ver resumen
cat logs_tests/pytest_summary_latest.log

# Ver que tests pasaron
grep "\[PASSED\]" logs_tests/tests_execution.log

# Ver que tests fallaron
grep "\[FAILED\]" logs_tests/tests_execution.log
```

### Comparar Ejecuciones

```bash
# Listar logs por fecha
ls -lt logs_tests/pytest_*.log

# Comparar dos ejecuciones
diff logs_tests/pytest_20251009_100000.log logs_tests/pytest_20251009_110000.log
```

---

## Mantenimiento

### Limpieza Automatica

Los scripts `ver_logs_tests.bat` y `ver_logs_tests.sh` incluyen opcion para limpiar logs antiguos (mantiene ultimos 5).

### Limpieza Manual

```bash
# Windows
del logs_tests\pytest_*.log
del logs_tests\test_*.log

# Linux
rm logs_tests/pytest_*.log
rm logs_tests/test_*.log

# Mantener solo ultimos 10 dias
find logs_tests/ -name "*.log" -mtime +10 -delete
```

---

## Integracion con CI/CD

### GitHub Actions

```yaml
- name: Run tests with logs
  run: python run_pytest.py

- name: Upload test logs
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-logs
    path: logs_tests/
    retention-days: 30
```

### GitLab CI

```yaml
test:
  script:
    - python run_pytest.py
  artifacts:
    when: always
    paths:
      - logs_tests/
    expire_in: 1 week
```

---

## Ejemplo de Log Completo

```
======================================================================
CONFIGURACION DE LOGS PARA TESTS
======================================================================
Directorio: C:\...\students-point\logs_tests
Log general: pytest_20251009_163000.log
Log errores: pytest_errors_latest.log
======================================================================

[INFO] 2025-10-09 16:30:00 [tests] - Sesion de tests iniciada
[INFO] 2025-10-09 16:30:00 [tests] - ============================================================
[INFO] 2025-10-09 16:30:00 [tests] - INICIANDO TEST: test_auth_me.py::test_auth_me_requires_token
[INFO] 2025-10-09 16:30:00 [tests] - ============================================================
[DEBUG] 2025-10-09 16:30:00 [django.db.backends] - Conectando a base de datos
[INFO] 2025-10-09 16:30:01 [tests] - [PASSED] test_auth_me.py::test_auth_me_requires_token
[INFO] 2025-10-09 16:30:01 [tests] - ============================================================
[INFO] 2025-10-09 16:30:01 [tests] - INICIANDO TEST: test_login_api.py::test_login_success
[INFO] 2025-10-09 16:30:01 [tests] - ============================================================
[DEBUG] 2025-10-09 16:30:01 [tests.test_login] - Creando usuario: test@example.com
[INFO] 2025-10-09 16:30:02 [studentspoint.apps.accounts] - Usuario autenticado: test@example.com
[INFO] 2025-10-09 16:30:02 [tests] - [PASSED] test_login_api.py::test_login_success
```

---

## Troubleshooting

### No se generan logs

Verificar que:
1. Directorio `logs_tests/` existe (se crea automaticamente)
2. Archivo `conftest.py` esta configurado correctamente
3. Tests se ejecutan con `python run_pytest.py`

### Logs muy grandes

```bash
# Ver tamano
du -sh logs_tests/

# Limpiar logs antiguos
./ver_logs_tests.sh
# Opcion 6: Limpiar logs antiguos
```

### No encuentro un error especifico

```bash
# Buscar en todos los logs
grep -r "error_especifico" logs_tests/

# Buscar test especifico
grep -r "test_login" logs_tests/
```

---

## Ventajas del Sistema

1. **Historial completo:** Cada ejecucion genera su propio log
2. **Debugging facil:** Logs detallados con lineas de codigo
3. **Acceso rapido:** Scripts interactivos para ver logs
4. **Formato profesional:** Sin emojis, prefijos claros
5. **Resumen automatico:** Archivo summary con estadisticas
6. **Separacion de errores:** Archivo especifico solo para errores
7. **CI/CD ready:** Facil de integrar en pipelines

---

## Comandos Rapidos

```bash
# Ejecutar tests (genera logs)
python run_pytest.py

# Ver errores
ver_logs_tests.bat                          # Windows
./ver_logs_tests.sh                         # Linux

# Ver resumen rapido
type logs_tests\pytest_summary_latest.log   # Windows
cat logs_tests/pytest_summary_latest.log    # Linux

# Buscar test especifico
grep "test_name" logs_tests/tests_execution.log
```

---

Fecha: 9 de Octubre 2025
Version: 1.0.0
Estado: Implementado

