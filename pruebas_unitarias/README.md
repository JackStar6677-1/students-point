### Pruebas unitarias/integración (pytest)

## Instalación

```bash
python -m pip install pytest pytest-django djangorestframework
```

## Ejecución rápida

**Todas las pruebas:**
```bash
python tests/run_pytest.py -q
```

**Archivo específico:**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_login_api.py -v
```

**Test específico:**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_login_api.py::test_login_ok_then_me -v
```

**Con más detalle:**
```bash
python tests/run_pytest.py -vv
```

## 🚀 PRUEBAS NUEVAS - APIs Principales

### **Ejecutar todas las pruebas nuevas:**
```bash
python tests/run_pytest.py pruebas_unitarias/api/ -v
```

### **Por módulo específico:**

**🏆 Portfolio API (CV/Curriculum):**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_portfolio_api.py -v
```

**🛒 Marketplace API (Productos):**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_marketplace_api.py -v
```

**🔔 Notifications API:**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_notifications_api.py -v
```

**📊 Polls API (Encuestas):**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_polls_api.py -v
```

**🏥 Health API (Estado del sistema):**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_health_api.py -v
```

**📄 Converter API (Conversión de documentos):**
```bash
python tests/run_pytest.py pruebas_unitarias/api/test_converter_api.py -v
```

### **Scripts automáticos (Windows):**
```bash
# Ejecutar todas las pruebas nuevas con detalles
ejecutar_pruebas_nuevas.bat

# Ejecutar todas las pruebas nuevas de forma rápida
ejecutar_pruebas_rapidas.bat
```

## Cómo funciona

### 1. Configuración del entorno

**`conftest.py`** (raíz): Agrega `proyecto/src/backend` al PYTHONPATH para que Python encuentre el módulo `studentspoint`.

**`pytest.ini`** (raíz): Define configuración de pytest:
- `DJANGO_SETTINGS_MODULE`: Usa `studentspoint.settings.base`
- `testpaths`: Busca tests en `pruebas_unitarias/`
- `python_files`: Descubre archivos `test_*.py`

**`run_pytest.py`**: Script que:
1. Prepara el entorno (PYTHONPATH + DJANGO_SETTINGS)
2. Ejecuta pytest con los argumentos que le pases

### 2. Estructura de un test

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db  # Marca que el test usa base de datos
def test_ejemplo():
    # 1. ARRANGE (preparar datos)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(email='test@duocuc.cl', password='pass123')
    
    # 2. ACT (ejecutar acción)
    client = APIClient()
    response = client.post('/api/auth/login/', {
        'email': 'test@duocuc.cl',
        'password': 'pass123'
    }, format='json')
    
    # 3. ASSERT (verificar resultado)
    assert response.status_code == 200
    assert 'access' in response.json()
```

### 3. Base de datos de prueba

pytest-django crea una **base de datos temporal en memoria** para cada test:

1. **Antes del test**: Crea BD vacía → Aplica migraciones
2. **Durante el test**: Puedes crear/leer/modificar datos
3. **Después del test**: Destruye la BD (rollback automático)

Cada test es **independiente** y empieza con BD limpia.

### 4. APIClient (Django REST Framework)

```python
from rest_framework.test import APIClient

client = APIClient()

# GET request
resp = client.get('/api/auth/me/')

# POST request con JSON
resp = client.post('/api/auth/login/', {
    'email': 'test@duocuc.cl',
    'password': 'pass123'
}, format='json')

# Agregar headers de autenticación
client.credentials(HTTP_AUTHORIZATION='Bearer token_aqui')

# Leer respuesta
data = resp.json()
status = resp.status_code
```

### 5. Marcadores (decoradores)

- `@pytest.mark.django_db`: Permite acceso a la base de datos
- `@pytest.skip("razón")`: Salta el test
- `@pytest.mark.parametrize`: Ejecuta el test con múltiples valores

## Tests existentes

### **Tests Originales:**
### `test_login_api.py`
- `test_auth_me_requires_token`: Verifica que `/api/auth/me/` rechace peticiones sin token
- `test_login_ok_then_me`: Login exitoso → obtener perfil con token

### `test_register_api.py`
- `test_register_then_login_ok`: Registra usuario → hace login

### `test_campus_map.py`
- `test_list_campuses_ok`: Lista de campus (paginada o simple)
- `test_list_tours_and_steps_smoke`: Tours por campus con pasos ordenados

### `test_auth_me.py`
- `test_auth_me_requires_token`: Verifica que `/api/auth/me/` rechace peticiones sin token

---

## 🆕 TESTS NUEVOS - APIs Principales

### **🏆 Portfolio API (`test_portfolio_api.py`) - 12 pruebas**
- ✅ Crear logros, proyectos, experiencias, habilidades
- ✅ Listar elementos del portfolio
- ✅ Actualizar y eliminar elementos
- ✅ Portfolio completo del usuario
- ✅ Filtros de visibilidad
- ✅ Autenticación requerida

### **🛒 Marketplace API (`test_marketplace_api.py`) - 12 pruebas**
- ✅ Crear y listar productos
- ✅ Gestión de categorías
- ✅ Filtros por estado y categoría
- ✅ URLs adicionales
- ✅ Permisos de propietario
- ✅ Diferentes tipos de enlaces

### **🔔 Notifications API (`test_notifications_api.py`) - 12 pruebas**
- ✅ Crear y listar notificaciones
- ✅ Marcar como leídas
- ✅ Filtros por tipo y estado
- ✅ Configuración de usuario
- ✅ Diferentes prioridades
- ✅ Datos extra y redirecciones

### **📊 Polls API (`test_polls_api.py`) - 12 pruebas**
- ✅ Crear encuestas con opciones
- ✅ Votación simple y múltiple
- ✅ Resultados en tiempo real
- ✅ Votación anónima
- ✅ Justificaciones requeridas
- ✅ Filtros por carrera

### **🏥 Health API (`test_health_api.py`) - 15 pruebas**
- ✅ Health checks básicos
- ✅ Liveness y readiness
- ✅ Información de API
- ✅ Verificación de servicios
- ✅ Manejo de errores
- ✅ Headers CORS

### **📄 Converter API (`test_converter_api.py`) - 15 pruebas**
- ✅ Conversión Word ↔ PDF
- ✅ Opción OCR
- ✅ Estados de conversión
- ✅ Manejo de errores
- ✅ Filtros por tipo y estado
- ✅ Timestamps y archivos

### **🎯 Total: 78 pruebas nuevas**

## Variables de entorno

```bash
# Windows PowerShell
$env:E2E_EMAIL="admin@duocuc.cl"
$env:E2E_PASSWORD="admin123"
python tests/run_pytest.py -v

# Linux/Mac
export E2E_EMAIL="admin@duocuc.cl"
export E2E_PASSWORD="admin123"
python tests/run_pytest.py -v
```

## Flujo de ejecución

```
1. python tests/run_pytest.py -q
   ↓
2. Prepara entorno (PYTHONPATH, DJANGO_SETTINGS)
   ↓
3. pytest descubre test_*.py en pruebas_unitarias/
   ↓
4. Por cada función test_*():
    Crea BD temporal
    Ejecuta test (arrange → act → assert)
    Destruye BD
   ↓
5. Muestra resumen: X passed, Y skipped, Z failed
```

## Mejores prácticas

1. **Nombres descriptivos**: `test_login_con_credenciales_invalidas`
2. **Un test, una cosa**: Verifica un comportamiento específico
3. **Arrange-Act-Assert**: Estructura clara en 3 partes
4. **Independencia**: Cada test debe poder ejecutarse solo
5. **BD limpia**: No asumas datos previos; crea lo necesario en el test

## Comandos útiles

```bash
# Solo tests que contengan "login" en el nombre
python tests/run_pytest.py -k login -v

# Detener en el primer fallo
python tests/run_pytest.py -x

# Mostrar prints y output
python tests/run_pytest.py -s

# Ejecutar en paralelo (requiere pytest-xdist)
python tests/run_pytest.py -n auto

# Solo las pruebas nuevas de APIs
python tests/run_pytest.py pruebas_unitarias/api/ -v

# Filtrar por módulo específico
python tests/run_pytest.py -k "portfolio or marketplace" -v
```

## Troubleshooting

**Error: No module named 'studentspoint'**
- Usa `python tests/run_pytest.py` en lugar de `pytest` directo

**Error: can't open file 'run_pytest.py'**
- El archivo está en `tests/run_pytest.py`, no en la raíz del proyecto

**Test se salta (SKIPPED)**
- Verifica que exista el usuario demo o que las credenciales en variables de entorno sean correctas

**BD locks o errores de migración**
- pytest usa BD en memoria; si usas sqlite, asegúrate de cerrar conexiones previas

**Error en pruebas de APIs nuevas**
- Verifica que el servidor Django esté ejecutándose si las pruebas requieren endpoints activos
- Algunas pruebas pueden fallar si no están configuradas las URLs correspondientes

---

## 📋 RESUMEN RÁPIDO DE COMANDOS

### **Comandos más usados:**
```bash
# Todas las pruebas (originales + nuevas)
python tests/run_pytest.py pruebas_unitarias/ -v

# Solo las pruebas nuevas de APIs
python tests/run_pytest.py pruebas_unitarias/api/ -v

# Por módulo específico
python tests/run_pytest.py pruebas_unitarias/api/test_portfolio_api.py -v
python tests/run_pytest.py pruebas_unitarias/api/test_marketplace_api.py -v
python tests/run_pytest.py pruebas_unitarias/api/test_notifications_api.py -v

# Scripts automáticos (Windows)
ejecutar_pruebas_nuevas.bat
```

### **Filtros útiles:**
```bash
# Solo pruebas de autenticación
python tests/run_pytest.py -k "auth or login" -v

# Solo pruebas de portfolio y marketplace
python tests/run_pytest.py -k "portfolio or marketplace" -v

# Solo pruebas de APIs nuevas
python tests/run_pytest.py -k "portfolio or marketplace or notifications or polls or health or converter" -v
```

### **Con más detalle:**
```bash
# Con stack trace completo
python tests/run_pytest.py pruebas_unitarias/api/ -v --tb=long

# Detener en primer fallo
python tests/run_pytest.py pruebas_unitarias/api/ -x

# Solo mostrar fallos
python tests/run_pytest.py pruebas_unitarias/api/ -v --tb=short
```


