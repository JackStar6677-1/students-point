# Logs de Tests - StudentsPoint

Este directorio contiene los logs generados durante la ejecucion de tests.

## Archivos Generados

### tests_execution.log
Contiene todos los logs de la ejecucion de tests (DEBUG y superior).
Este archivo se va agregando con cada ejecucion.

### tests_errors.log
Contiene solo los errores ocurridos durante los tests.
Se sobrescribe en cada ejecucion para mantener solo los errores mas recientes.

### pytest_[timestamp].log
Logs generados por pytest con timestamp especifico.
Uno por cada ejecucion de pytest.

### pytest_errors_latest.log
Ultimo log de errores de pytest.

### pytest_summary_latest.log
Resumen de la ultima ejecucion de tests.

---

## Uso

Los logs se generan automaticamente al ejecutar tests:

```bash
# Ejecutar tests (logs se generan automaticamente)
python run_pytest.py

# Ver logs mas recientes
Get-Content logs_tests\pytest_errors_latest.log      # Windows
tail -f logs_tests/pytest_errors_latest.log          # Linux

# Ver resumen
cat logs_tests/pytest_summary_latest.log
```

---

## Formato de Logs

### Log General
```
[INFO] 2025-10-09 16:30:00 - Test session started
[DEBUG] 2025-10-09 16:30:01 [tests] test_login - Iniciando test de login
[INFO] 2025-10-09 16:30:02 [studentspoint.apps.accounts] login - Usuario autenticado
```

### Log Detallado
```
[DEBUG] 2025-10-09 16:30:01 [tests.test_auth].test_login_success:45 - Creando usuario de prueba
[INFO] 2025-10-09 16:30:02 [studentspoint.apps.accounts].login:123 - Login exitoso para test@example.com
[DEBUG] 2025-10-09 16:30:02 [tests.test_auth].test_login_success:52 - Verificando token JWT
```

### Log de Errores
```
[ERROR] 2025-10-09 16:30:05 [tests.test_forum].test_create_post:78 - Error creando post
Traceback (most recent call last):
  File "test_forum.py", line 78, in test_create_post
    ...
AssertionError: 400 != 201
```

---

## Informacion en Logs

Cada test loggea:
- INICIANDO TEST: Nombre del test
- Operaciones realizadas (creacion usuarios, peticiones API, etc)
- Resultados de validaciones
- [PASSED] / [FAILED] / [SKIPPED]
- Errores detallados con traceback
- Tiempo de ejecucion

---

## Analisis de Logs

### Buscar errores de un test especifico
```bash
# Windows
Get-Content logs_tests\pytest_errors_latest.log | Select-String "test_login"

# Linux
grep "test_login" logs_tests/pytest_errors_latest.log
```

### Ver solo tests fallidos
```bash
grep "\[FAILED\]" logs_tests/tests_execution.log
```

### Contar errores
```bash
grep -c "ERROR" logs_tests/tests_errors.log
```

---

## Limpieza

Los logs se acumulan en el tiempo. Limpiar periodicamente:

```bash
# Windows
del logs_tests\pytest_*.log

# Linux  
rm logs_tests/pytest_*.log

# Mantener solo ultimos 10
ls -t logs_tests/pytest_*.log | tail -n +11 | xargs rm
```

---

## Integracion con CI/CD

Los logs pueden ser archivados como artefactos en CI/CD:

```yaml
# GitHub Actions
- name: Upload test logs
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-logs
    path: logs_tests/
```

---

Fecha: Octubre 2025
Mantenido por: Equipo de Testing

