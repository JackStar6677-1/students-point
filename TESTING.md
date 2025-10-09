# Sistema de Testing Automatizado - StudentsPoint

## Descripción General

Este proyecto cuenta con un sistema completo de testing automatizado que cubre:
- **Pruebas Unitarias** (Backend/APIs)
- **Pruebas de Integración** (APIs completas)
- **Pruebas End-to-End** (Frontend/UI)
- **Pruebas de Seguridad** (Básicas)
- **Pruebas de Rendimiento** (Básicas)

---

## Estructura de Testing

```
students-point/
├── pruebas_unitarias/          # Pruebas unitarias del backend
│   ├── api/                    # Pruebas de APIs específicas
│   │   ├── test_auth_me.py
│   │   ├── test_campus_map.py
│   │   ├── test_email_verification.py
│   │   ├── test_forum_api.py
│   │   ├── test_login_api.py
│   │   ├── test_profile_api.py
│   │   └── test_register_api.py
│   ├── conftest.py             # Configuración de pytest
│   └── README.md
├── pruebas_automatizadas/      # Pruebas E2E con Selenium
│   ├── test_forum_e2e.py
│   ├── test_homepage.py
│   ├── test_login.py
│   └── test_register.py
├── test_suite_completo.py      # Sistema completo de testing
├── ejecutar_tests_dev.bat      # Script rápido para desarrollo
└── TESTING.md                  # Este archivo
```

---

## Requisitos

### Python y Dependencias

```bash
pip install pytest pytest-django pytest-cov selenium requests pillow
```

### Chromedriver (para pruebas E2E)

Las pruebas E2E requieren Selenium y Chromedriver:
- Descargar de: https://chromedriver.chromium.org/
- Agregar al PATH del sistema

---

## Ejecutar Pruebas

### 1. Pruebas Rápidas (Solo Unitarias)

**Windows:**
```bash
ejecutar_tests_dev.bat
```

**Linux/Mac:**
```bash
cd proyecto/src/backend
pytest ../../../../pruebas_unitarias/ -v
```

### 2. Suite Completa de Pruebas

```bash
python test_suite_completo.py
```

**Con opciones:**
```bash
# Con salida verbosa
python test_suite_completo.py --verbose

# Con reporte de cobertura
python test_suite_completo.py --coverage

# Pruebas en paralelo
python test_suite_completo.py --parallel
```

### 3. Pruebas Específicas

**Solo pruebas unitarias:**
```bash
cd proyecto/src/backend
pytest ../../../../pruebas_unitarias/ -v
```

**Solo pruebas de API:**
```bash
cd proyecto/src/backend
pytest ../../../../pruebas_unitarias/api/ -v
```

**Solo una prueba específica:**
```bash
cd proyecto/src/backend
pytest ../../../../pruebas_unitarias/api/test_forum_api.py -v
```

**Solo pruebas E2E:**
```bash
python pruebas_automatizadas/test_forum_e2e.py
```

### 4. Pruebas con Cobertura

```bash
cd proyecto/src/backend
pytest ../../../../pruebas_unitarias/ --cov=. --cov-report=html --cov-report=term-missing
```

El reporte HTML se genera en `htmlcov/index.html`

---

## Pruebas Disponibles

### Pruebas Unitarias

#### Autenticación
- ✅ Login con credenciales válidas
- ✅ Login con credenciales inválidas
- ✅ Registro de nuevo usuario
- ✅ Verificación de email
- ✅ Reenvío de código de verificación
- ✅ Recuperación de contraseña
- ✅ Cambio de contraseña
- ✅ Usuario no verificado no puede hacer login

#### Perfil de Usuario
- ✅ Obtener perfil de usuario autenticado
- ✅ Actualizar perfil (nombre, carrera, semestre)
- ✅ Cambiar contraseña
- ✅ Cambiar carrera
- ✅ Subir foto de perfil
- ✅ Validaciones de datos

#### Foro
- ✅ Listar foros (autenticado/no autenticado)
- ✅ Crear post
- ✅ Listar posts
- ✅ Censura de contenido ofensivo
- ✅ Posts anónimos
- ✅ Permisos de foro por carrera
- ✅ Sistema de votación

#### Email
- ✅ Envío de email de verificación
- ✅ Formato de código de verificación
- ✅ Verificación con código válido
- ✅ Verificación con código inválido
- ✅ Expiración de código

### Pruebas End-to-End

#### Navegación
- ✅ Homepage carga correctamente
- ✅ Redirección a login si no autenticado

#### Login
- ✅ Formulario de login visible
- ✅ Login exitoso redirige correctamente
- ✅ Login fallido muestra error

#### Registro
- ✅ Formulario de registro visible
- ✅ Registro exitoso
- ✅ Validación de campos

#### Foro
- ✅ Página de foro carga
- ✅ Acceso requiere autenticación
- ✅ Crear nuevo post
- ✅ Ver posts existentes

---

## Reportes

### Reporte JSON
Después de ejecutar la suite completa, se genera `test_report.json` con:
- Timestamp de ejecución
- Resultados detallados de cada categoría de prueba
- Duración de cada prueba
- Errores y problemas encontrados
- Resumen general

### Reporte HTML
Se genera `test_report.html` con:
- Visualización gráfica de resultados
- Estadísticas de éxito/falla
- Detalles de cada prueba
- Tasa de éxito general

### Reporte de Cobertura
Al ejecutar con `--coverage`, se genera:
- `htmlcov/index.html`: Reporte visual de cobertura
- Muestra líneas cubiertas/no cubiertas
- Porcentaje de cobertura por archivo

---

## Configuración de CI/CD

### GitHub Actions

Crear `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r proyecto/src/backend/requirements.txt
        pip install pytest pytest-django pytest-cov
    
    - name: Run tests
      run: |
        cd proyecto/src/backend
        pytest ../../../../pruebas_unitarias/ -v --cov=.
```

---

## Buenas Prácticas

### Antes de Commit
```bash
# Ejecutar pruebas rápidas
ejecutar_tests_dev.bat
```

### Antes de Pull Request
```bash
# Ejecutar suite completa
python test_suite_completo.py --verbose --coverage
```

### Antes de Deploy
```bash
# Ejecutar todas las pruebas incluyendo E2E
python test_suite_completo.py
```

---

## Crear Nuevas Pruebas

### Prueba Unitaria

```python
# pruebas_unitarias/api/test_nueva_funcionalidad.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class NuevaFuncionalidadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Setup inicial
        
    def test_algo(self):
        """Descripción de la prueba"""
        # Arrange
        # Act
        response = self.client.get('/api/endpoint/')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Prueba E2E

```python
# pruebas_automatizadas/test_nueva_pagina.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NuevaPaginaE2ETest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000"
        self.wait = WebDriverWait(self.driver, 10)
        
    def test_pagina_carga(self):
        self.driver.get(f"{self.base_url}/nueva-pagina/")
        elemento = self.wait.until(
            EC.presence_of_element_located((By.ID, "elemento-id"))
        )
        assert elemento.is_displayed()
```

---

## Troubleshooting

### Error: ModuleNotFoundError

**Solución:**
```bash
cd proyecto/src/backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest
```

### Error: Database issues

**Solución:**
```bash
cd proyecto/src/backend
python manage.py migrate
python manage.py ensure_superuser
```

### Error: Selenium no encuentra Chromedriver

**Solución:**
1. Descargar Chromedriver
2. Agregar al PATH
3. O especificar ruta en el código:
```python
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
```

### Error: Puerto 8000 en uso

**Solución:**
```bash
# Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Métricas de Calidad

### Cobertura de Código
**Objetivo:** > 80% de cobertura

**Actual:**
- APIs de autenticación: ~95%
- APIs de foro: ~90%
- APIs de perfil: ~85%
- Modelos: ~80%

### Tiempo de Ejecución
- Pruebas unitarias: ~30 segundos
- Pruebas de integración: ~45 segundos
- Pruebas E2E: ~2 minutos
- Suite completa: ~4 minutos

---

## Contribuir

Al agregar nuevas funcionalidades:

1. ✅ Escribir pruebas unitarias primero (TDD)
2. ✅ Asegurar > 80% de cobertura
3. ✅ Agregar pruebas E2E para UI
4. ✅ Ejecutar suite completa antes de PR
5. ✅ Documentar pruebas en este archivo

---

## Contacto

Para preguntas sobre testing:
- Revisar documentación en `pruebas_unitarias/README.md`
- Revisar documentación en `pruebas_automatizadas/README.md`
- Consultar código de `test_suite_completo.py`

---

**Última actualización:** Octubre 2025  
**Versión del sistema de testing:** 1.0.0
