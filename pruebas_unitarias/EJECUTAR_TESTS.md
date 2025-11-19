# Guía para Ejecutar Tests - StudentsPoint

Esta guía te ayudará a ejecutar todas las pruebas unitarias del proyecto StudentsPoint.

## Prerrequisitos

1. **Python 3.10+** instalado
2. **Entorno virtual** activado
3. **Dependencias instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración Inicial

### 1. Activar el entorno virtual

**Windows:**
```bash
cd proyecto\src\backend
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd proyecto/src/backend
source venv/bin/activate
```

### 2. Verificar instalación de pytest
```bash
pytest --version
```

Deberías ver algo como:
```
pytest 7.x.x
```

## Comandos de Ejecución

### Ejecutar TODOS los tests
```bash
cd proyecto/src/backend
pytest ../../pruebas_unitarias/ -v
```

### Ejecutar tests con más detalles
```bash
pytest ../../pruebas_unitarias/ -v -s
```
- `-v`: verbose (muestra más detalles)
- `-s`: muestra prints y outputs

### Ejecutar tests de un módulo específico

#### Tests del Foro
```bash
pytest ../../pruebas_unitarias/api/test_forum_api.py -v
pytest ../../pruebas_unitarias/api/test_forum_comprehensive.py -v
pytest ../../pruebas_unitarias/api/test_forum_images.py -v
```

#### Tests del Marketplace
```bash
pytest ../../pruebas_unitarias/api/test_marketplace_api.py -v
pytest ../../pruebas_unitarias/api/test_marketplace_comprehensive.py -v
pytest ../../pruebas_unitarias/api/test_marketplace_images.py -v
```

#### Tests de Autenticación
```bash
pytest ../../pruebas_unitarias/api/test_login_api.py -v
pytest ../../pruebas_unitarias/api/test_register_api.py -v
pytest ../../pruebas_unitarias/api/test_auth_me.py -v
pytest ../../pruebas_unitarias/api/test_email_verification.py -v
```

#### Tests de Notificaciones
```bash
pytest ../../pruebas_unitarias/api/test_notifications_api.py -v
```

#### Tests de Encuestas
```bash
pytest ../../pruebas_unitarias/api/test_polls_api.py -v
```

#### Tests de Portafolio
```bash
pytest ../../pruebas_unitarias/api/test_portfolio_api.py -v
```

#### Tests de Converter
```bash
pytest ../../pruebas_unitarias/api/test_converter_api.py -v
```

### Ejecutar un test específico
```bash
pytest ../../pruebas_unitarias/api/test_forum_api.py::ForumAPITestCase::test_create_post_authenticated -v
```

### Ejecutar tests por categoría (con marcadores)

#### Solo tests que NO están en skip
```bash
pytest ../../pruebas_unitarias/ -v -m "not skip"
```

#### Tests lentos (si están marcados)
```bash
pytest ../../pruebas_unitarias/ -v -m "slow"
```

## Análisis de Cobertura

### Generar reporte de cobertura HTML
```bash
pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador.

### Generar reporte de cobertura en terminal
```bash
pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=term
```

### Cobertura con detalles de líneas faltantes
```bash
pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=term-missing
```

## Opciones Útiles de Pytest

### Detener en el primer fallo
```bash
pytest ../../pruebas_unitarias/ -x
```

### Ejecutar solo los tests que fallaron la última vez
```bash
pytest ../../pruebas_unitarias/ --lf
```

### Ejecutar tests en paralelo (más rápido)
```bash
pip install pytest-xdist
pytest ../../pruebas_unitarias/ -n auto
```

### Mostrar los 10 tests más lentos
```bash
pytest ../../pruebas_unitarias/ --durations=10
```

### Modo watch (re-ejecutar cuando cambien archivos)
```bash
pip install pytest-watch
ptw ../../pruebas_unitarias/
```

## Filtrar Tests por Nombre

### Tests que contengan "market" en el nombre
```bash
pytest ../../pruebas_unitarias/ -k "market"
```

### Tests que contengan "image" en el nombre
```bash
pytest ../../pruebas_unitarias/ -k "image"
```

### Tests que NO contengan "comprehensive"
```bash
pytest ../../pruebas_unitarias/ -k "not comprehensive"
```

## Debugging

### Ejecutar con debugger (pdb)
```bash
pytest ../../pruebas_unitarias/ --pdb
```

### Entrar al debugger solo en fallos
```bash
pytest ../../pruebas_unitarias/ --pdb -x
```

### Modo trace (para ver cada paso)
```bash
pytest ../../pruebas_unitarias/ --trace
```

## Generar Reportes

### Reporte en formato JUnit (para CI/CD)
```bash
pytest ../../pruebas_unitarias/ --junitxml=test-results.xml
```

### Reporte HTML bonito
```bash
pip install pytest-html
pytest ../../pruebas_unitarias/ --html=report.html --self-contained-html
```

## Solución de Problemas Comunes

### Error: "No module named 'studentspoint'"
**Solución**: Asegúrate de estar en el directorio correcto y que el entorno virtual esté activado.
```bash
cd proyecto/src/backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
```

### Error: "Database is locked"
**Solución**: Usa una base de datos en memoria para tests:
```python
# En settings/test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

### Tests muy lentos
**Solución 1**: Ejecuta en paralelo
```bash
pytest ../../pruebas_unitarias/ -n auto
```

**Solución 2**: Usa base de datos en memoria

**Solución 3**: Ejecuta solo los tests necesarios
```bash
pytest ../../pruebas_unitarias/api/test_forum_api.py -v
```

### ImportError en fixtures
**Solución**: Verifica que existe `conftest.py` en el directorio raíz de pruebas.

## Estructura de un Test Completo

```python
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def client():
    """Cliente API"""
    return APIClient()


class TestMiModulo:
    """Tests para Mi Módulo"""
    
    def test_algo_funciona(self, client, user):
        """Prueba que algo funciona correctamente"""
        client.force_authenticate(user=user)
        response = client.get('/api/mi-endpoint/')
        assert response.status_code == status.HTTP_200_OK
```

## Mejores Prácticas

1. ✅ **Siempre ejecuta los tests antes de hacer commit**
   ```bash
   pytest ../../pruebas_unitarias/ -v
   ```

2. ✅ **Verifica la cobertura regularmente**
   ```bash
   pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=term
   ```

3. ✅ **Mantén los tests rápidos**
   - Usa fixtures para datos de prueba
   - Evita sleeps innecesarios
   - Usa mocks para servicios externos

4. ✅ **Escribe tests descriptivos**
   ```python
   def test_create_post_with_valid_data_returns_201():
       """Verifica que crear un post con datos válidos devuelve 201 Created"""
       pass
   ```

5. ✅ **Un test, una assertion principal**
   ```python
   # ✅ Bueno
   def test_user_creation():
       user = User.objects.create_user(...)
       assert user.email == 'test@duocuc.cl'
   
   # ❌ Evitar
   def test_everything():
       # Muchas assertions no relacionadas
       pass
   ```

## Integración con IDEs

### VSCode
Instala la extensión "Python Test Explorer" y configura:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "../../pruebas_unitarias/"
    ]
}
```

### PyCharm
1. Ve a Settings → Tools → Python Integrated Tools
2. Selecciona "pytest" como test runner
3. Haz clic derecho en el directorio de tests → "Run pytest"

## Resumen de Comandos Más Usados

```bash
# Ejecutar todos los tests
pytest ../../pruebas_unitarias/ -v

# Ejecutar con cobertura
pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=html

# Ejecutar solo un archivo
pytest ../../pruebas_unitarias/api/test_forum_api.py -v

# Ejecutar solo los que no están en skip
pytest ../../pruebas_unitarias/ -v -m "not skip"

# Ejecutar en paralelo
pytest ../../pruebas_unitarias/ -n auto

# Detener en el primer error
pytest ../../pruebas_unitarias/ -x

# Ver prints y outputs
pytest ../../pruebas_unitarias/ -s
```

## ¿Necesitas Ayuda?

- 📖 Documentación de pytest: https://docs.pytest.org/
- 📖 pytest-django: https://pytest-django.readthedocs.io/
- 📁 README de tests: `pruebas_unitarias/README.md`
- 👥 Contacta al equipo de desarrollo

---

**¡Feliz Testing!** 🧪✨

