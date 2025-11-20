# 📚 Guía de Ejecución de Tests - Students Point

Esta guía te ayudará a ejecutar las pruebas unitarias del proyecto Students Point de manera efectiva.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Inicial](#configuración-inicial)
3. [Ejecutar Todos los Tests](#ejecutar-todos-los-tests)
4. [Ejecutar Tests Específicos](#ejecutar-tests-específicos)
5. [Ejecutar Tests por Categoría](#ejecutar-tests-por-categoría)
6. [Ver Logs y Resultados](#ver-logs-y-resultados)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

Antes de ejecutar los tests, asegúrate de tener:

- ✅ Python 3.9 o superior instalado
- ✅ Entorno virtual activado
- ✅ Todas las dependencias instaladas
- ✅ Base de datos configurada (se usa SQLite en memoria para tests)

### Instalación de Dependencias

```bash
cd proyecto/src/backend
pip install -r requirements.txt
```

---

## ⚙️ Configuración Inicial

### 1. Configurar Variables de Entorno

Los tests usan la configuración de `studentspoint.settings.test` que:
- Usa SQLite en memoria (no afecta tu BD de desarrollo)
- Deshabilita migraciones para mayor velocidad
- Configura logging específico para tests

### 2. Verificar PYTHONPATH

Asegúrate de que el directorio del proyecto esté en el PYTHONPATH:

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "C:\Users\10100\Documents\GitHub\students-point\proyecto\src\backend"
```

**Windows (CMD):**
```cmd
set PYTHONPATH=C:\Users\10100\Documents\GitHub\students-point\proyecto\src\backend
```

**Linux/Mac:**
```bash
export PYTHONPATH=/path/to/students-point/proyecto/src/backend
```

---

## 🚀 Ejecutar Todos los Tests

### Opción 1: Usando pytest directamente

```bash
# Desde la raíz del proyecto
cd proyecto/src/backend
pytest ../../pruebas_unitarias/ -v
```

### Opción 2: Usando el script de ejecución

```bash
# Desde la raíz del proyecto
cd tests
python run_pytest.py
```

### Opción 3: Usando Django test runner

```bash
cd proyecto/src/backend
python manage.py test pruebas_unitarias --settings=studentspoint.settings.test
```

---

## 🎯 Ejecutar Tests Específicos

### Ejecutar un archivo de test específico

```bash
# Test de autenticación
pytest pruebas_unitarias/api/test_auth.py -v

# Test de foros
pytest pruebas_unitarias/api/test_forum_api.py -v

# Test de marketplace
pytest pruebas_unitarias/api/test_marketplace_api.py -v
```

### Ejecutar una clase de test específica

```bash
pytest pruebas_unitarias/api/test_auth.py::TestAuth -v
```

### Ejecutar un método de test específico

```bash
pytest pruebas_unitarias/api/test_auth.py::TestAuth::test_login_valido -v
```

---

## 📂 Ejecutar Tests por Categoría

### Tests de API

```bash
pytest pruebas_unitarias/api/ -v
```

### Tests de Autenticación

```bash
pytest pruebas_unitarias/api/test_auth.py -v
```

### Tests de Campus y Sedes

```bash
pytest pruebas_unitarias/api/test_campuses_api.py -v
pytest pruebas_unitarias/api/test_campus_map.py -v
```

### Tests de Foros

```bash
pytest pruebas_unitarias/api/test_forum_api.py -v
```

### Tests de Marketplace

```bash
pytest pruebas_unitarias/api/test_marketplace_api.py -v
```

### Tests de Notificaciones Push

```bash
pytest pruebas_unitarias/api/test_notifications_api.py -v
```

### Tests de Cursos OTEC

```bash
pytest pruebas_unitarias/api/test_otec_api.py -v
```

### Tests de Encuestas

```bash
pytest pruebas_unitarias/api/test_polls_api.py -v
```

### Tests de Portfolio

```bash
pytest pruebas_unitarias/api/test_portfolio_api.py -v
```

### Tests de Reportes

```bash
pytest pruebas_unitarias/api/test_reports_api.py -v
```

### Tests de Bienestar

```bash
pytest pruebas_unitarias/api/test_wellbeing_api.py -v
```

---

## 📊 Opciones Útiles de pytest

### Mostrar salida detallada

```bash
pytest pruebas_unitarias/ -v --tb=short
```

### Ejecutar tests en paralelo (más rápido)

```bash
pytest pruebas_unitarias/ -n auto
```

### Ver prints y logs durante la ejecución

```bash
pytest pruebas_unitarias/ -v -s
```

### Ejecutar solo tests que fallaron la última vez

```bash
pytest pruebas_unitarias/ --lf
```

### Detener en el primer fallo

```bash
pytest pruebas_unitarias/ -x
```

### Generar reporte HTML

```bash
pytest pruebas_unitarias/ --html=report.html --self-contained-html
```

### Generar reporte de cobertura

```bash
pytest pruebas_unitarias/ --cov=studentspoint --cov-report=html
```

---

## 📝 Ver Logs y Resultados

### Ubicación de Logs

Los logs de los tests se guardan en:

```
logs_tests/
├── pytest_YYYYMMDD_HHMMSS.log  # Log completo de ejecución
├── pytest_errors_latest.log     # Solo errores
└── pytest_summary_latest.log    # Resumen de resultados
```

### Ver logs en tiempo real

**Windows:**
```cmd
scripts\ver_logs_tests.bat
```

**Linux/Mac:**
```bash
./scripts/ver_logs_tests.sh
```

### Leer logs manualmente

```bash
# Ver último log completo
cat logs_tests/pytest_errors_latest.log

# Ver resumen
cat logs_tests/pytest_summary_latest.log

# Ver logs en tiempo real (Linux/Mac)
tail -f logs_tests/pytest_*.log
```

---

## 🔍 Scripts Auxiliares de Testing

### Script de test de API de productos

```bash
cd proyecto/src/backend
python ../../pruebas_unitarias/test_api.py
```

### Script de test de cursos

```bash
cd proyecto/src/backend
python ../../pruebas_unitarias/test_cursos_api.py
```

### Test interactivo de verificación de email

```bash
cd proyecto/src/backend
python manage.py test_email_verification --email=test@duocuc.cl --create-user
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'studentspoint'"

**Solución:** Configura el PYTHONPATH correctamente:

```bash
# Windows
set PYTHONPATH=C:\Users\10100\Documents\GitHub\students-point\proyecto\src\backend

# Linux/Mac
export PYTHONPATH=/path/to/proyecto/src/backend
```

### Error: "django.core.exceptions.ImproperlyConfigured"

**Solución:** Asegúrate de usar la configuración de tests:

```bash
python manage.py test --settings=studentspoint.settings.test
```

### Error: "No such file or directory: conftest.py"

**Solución:** Ejecuta pytest desde el directorio correcto:

```bash
cd proyecto/src/backend
pytest ../../pruebas_unitarias/ -v
```

### Tests muy lentos

**Solución 1:** Usa la configuración de tests que deshabilita migraciones:

```bash
pytest --ds=studentspoint.settings.test
```

**Solución 2:** Ejecuta tests en paralelo:

```bash
pytest -n auto
```

### Error: "Database is locked"

**Solución:** Los tests usan SQLite en memoria, reinicia el proceso de tests:

```bash
# Limpiar cache de pytest
pytest --cache-clear

# Ejecutar tests nuevamente
pytest pruebas_unitarias/ -v
```

### Error de imports en los tests

**Solución:** Verifica que el archivo `conftest.py` existe y está configurado correctamente:

```python
# pruebas_unitarias/conftest.py debe contener:
import sys
import os
import django

# Configurar el path al proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'proyecto', 'src', 'backend'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.test')
django.setup()
```

---

## 📈 Mejores Prácticas

### 1. Ejecutar tests antes de commit

```bash
# Ejecutar suite completa
pytest pruebas_unitarias/ -v

# Si pasa, hacer commit
git add .
git commit -m "feat: nueva funcionalidad con tests"
```

### 2. Ejecutar tests relacionados después de cambios

```bash
# Si modificaste el módulo de autenticación
pytest pruebas_unitarias/api/test_auth.py -v

# Si modificaste foros
pytest pruebas_unitarias/api/test_forum_api.py -v
```

### 3. Generar reporte de cobertura periódicamente

```bash
pytest pruebas_unitarias/ --cov=studentspoint --cov-report=html --cov-report=term
```

### 4. Usar markers para categorizar tests

```bash
# Ejecutar solo tests rápidos
pytest -m "not slow" pruebas_unitarias/

# Ejecutar solo tests de integración
pytest -m "integration" pruebas_unitarias/
```

---

## 🎓 Comandos Rápidos de Referencia

```bash
# Ejecutar todos los tests
pytest pruebas_unitarias/ -v

# Ejecutar tests de API
pytest pruebas_unitarias/api/ -v

# Ejecutar un archivo específico
pytest pruebas_unitarias/api/test_auth.py -v

# Ejecutar con cobertura
pytest pruebas_unitarias/ --cov=studentspoint

# Ejecutar en paralelo
pytest pruebas_unitarias/ -n auto

# Detener en primer fallo
pytest pruebas_unitarias/ -x

# Solo tests que fallaron
pytest pruebas_unitarias/ --lf

# Ver prints durante ejecución
pytest pruebas_unitarias/ -v -s

# Generar reporte HTML
pytest pruebas_unitarias/ --html=report.html
```

---

## 📞 Soporte

Si encuentras problemas que no están cubiertos en esta guía:

1. Revisa los logs en `logs_tests/`
2. Consulta la documentación de pytest: https://docs.pytest.org
3. Revisa el archivo `EJECUTAR_TESTS.md` para más detalles
4. Consulta el README principal del proyecto

---

## 📄 Estructura de Tests

```
pruebas_unitarias/
├── api/                          # Tests de endpoints API
│   ├── test_auth.py             # Autenticación y login
│   ├── test_campuses_api.py     # Sedes y campus
│   ├── test_forum_api.py        # Foros y posts
│   ├── test_marketplace_api.py  # Marketplace
│   ├── test_notifications_api.py # Notificaciones push
│   ├── test_otec_api.py         # Cursos OTEC
│   ├── test_polls_api.py        # Encuestas
│   ├── test_portfolio_api.py    # Portfolio
│   ├── test_reports_api.py      # Reportes
│   ├── test_wellbeing_api.py    # Bienestar
│   ├── test_campus_map.py       # Mapa de campus
│   └── test_infrastructure_monitoring.py # Monitoreo
├── management/                   # Comandos de management
│   └── commands/
│       └── test_email_verification.py
├── settings/                     # Configuración de tests
│   └── test.py
├── test_api.py                  # Script de test de productos
├── test_cursos_api.py           # Script de test de cursos
├── conftest.py                  # Configuración de pytest
├── GUIA_EJECUCION_TESTS.md     # Esta guía
├── EJECUTAR_TESTS.md           # Documentación adicional
└── README.md                    # Información general
```

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar los tests, verifica:

- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] PYTHONPATH configurado
- [ ] En el directorio correcto
- [ ] Base de datos de desarrollo no se verá afectada (tests usan SQLite en memoria)

---

**Última actualización:** Noviembre 2025  
**Versión:** 5.1.0  
**Proyecto:** Students Point - Duoc UC

