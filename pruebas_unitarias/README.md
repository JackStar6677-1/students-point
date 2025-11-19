# Pruebas Unitarias - StudentsPoint

Este directorio contiene todas las pruebas unitarias del proyecto StudentsPoint.

## Estructura de Pruebas

```
pruebas_unitarias/
├── api/
│   ├── test_audit_logging.py          # Tests de auditoría y logging
│   ├── test_auth_me.py                 # Tests de autenticación /api/auth/me/
│   ├── test_campus_map.py              # Tests de mapa de campus
│   ├── test_converter_api.py           # Tests de conversión de documentos
│   ├── test_email_verification.py      # Tests de verificación de email
│   ├── test_forum_api.py               # Tests básicos del foro
│   ├── test_forum_comprehensive.py     # Tests comprehensivos del foro
│   ├── test_forum_images.py           # Tests de imágenes en foro (nuevo)
│   ├── test_health_api.py              # Tests de health checks
│   ├── test_login_api.py               # Tests de login
│   ├── test_marketplace_api.py         # Tests básicos del marketplace
│   ├── test_marketplace_comprehensive.py # Tests comprehensivos del marketplace
│   ├── test_marketplace_images.py      # Tests de imágenes en marketplace (nuevo)
│   ├── test_notifications_api.py       # Tests de notificaciones
│   ├── test_polls_api.py               # Tests de encuestas
│   ├── test_portfolio_api.py           # Tests de portafolio
│   ├── test_profile_api.py             # Tests de perfil de usuario
│   ├── test_register_api.py            # Tests de registro
│   └── test_swipe_menu.py              # Tests de integración del menú swipe (nuevo)
└── README.md                            # Este archivo
```

## Ejecutar Pruebas

### Ejecutar todas las pruebas
```bash
cd proyecto/src/backend
pytest ../../pruebas_unitarias/ -v
```

### Ejecutar pruebas específicas por módulo
```bash
# Tests del foro
pytest ../../pruebas_unitarias/api/test_forum_api.py -v

# Tests del marketplace
pytest ../../pruebas_unitarias/api/test_marketplace_api.py -v

# Tests de autenticación
pytest ../../pruebas_unitarias/api/test_login_api.py -v
```

### Ejecutar con cobertura
```bash
pytest ../../pruebas_unitarias/ --cov=studentspoint --cov-report=html
```

### Ejecutar solo tests que no están marcados como skip
```bash
pytest ../../pruebas_unitarias/ -v -m "not skip"
```

## Nuevos Tests Agregados

### 1. Tests de Imágenes en Marketplace (`test_marketplace_images.py`)
Pruebas para la nueva funcionalidad de subida de imágenes en productos:
- ✅ Crear producto con imagen
- ✅ Crear producto sin imagen
- ✅ Validación de tamaño de imagen (máx 5MB)
- ✅ Validación de tipo de archivo
- ✅ Verificación de URL absoluta para imágenes
- ✅ Soporte para múltiples formatos (JPG, PNG, WebP)
- ✅ Autenticación requerida para subir imágenes

### 2. Tests de Imágenes en Foro (`test_forum_images.py`)
Pruebas para la funcionalidad de imágenes en posts del foro:
- ✅ Crear post con imagen
- ✅ Crear post sin imagen
- ✅ Auto-aprobación de imágenes
- ✅ Validación de formatos de imagen
- ✅ Posts anónimos con imágenes
- ✅ Autenticación requerida para subir imágenes

### 3. Tests de Integración del Menú Swipe (`test_swipe_menu.py`)
Pruebas de integración para el nuevo sistema de navegación:
- ✅ Verificación de carga del script swipe-menu.js
- ✅ Presencia del sidebar en todas las páginas
- ✅ Verificación de estilos CSS de glassmorphism
- ✅ Consistencia de navegación entre módulos
- ✅ Verificación de que mobile-menu.js fue removido

## Tests Actualizados

### Converter API (`test_converter_api.py`)
- ✅ **Removido skip**: Los tests ahora están activos y completamente funcionales
- Cobertura completa de conversión de documentos (Word to PDF, PDF to Word)
- Tests de estados (pendiente, procesando, completado, error)
- Tests de validación de archivos
- Tests de OCR
- Tests de filtrado por tipo y estado

### Notifications API (`test_notifications_api.py`)
- ✅ **Removido skip**: Los tests ahora están activos
- Tests de creación y listado de notificaciones
- Tests de marcar como leída
- Tests de configuración de notificaciones
- Tests de filtrado por tipo y estado
- Tests de prioridades y datos extra

## Módulos con Cobertura Completa

### ✅ Autenticación y Usuarios
- Login/Logout
- Registro de usuarios
- Verificación de email
- Perfil de usuario
- Auditoría de actividades

### ✅ Foro
- Creación de posts y comentarios
- Sistema de votación
- Posts anónimos
- Moderación y reportes
- **Nuevo**: Subida de imágenes

### ✅ Marketplace
- CRUD de productos
- Categorías
- Filtros y búsqueda
- Favoritos
- **Nuevo**: Subida de imágenes

### ✅ Encuestas (Polls)
- Creación de encuestas
- Sistema de votación
- Encuestas anónimas
- Resultados y estadísticas

### ✅ Portafolio
- Logros y certificaciones
- Proyectos
- Experiencia laboral
- Habilidades

### ✅ Campus
- Listado de sedes
- Recorridos virtuales
- Mapas interactivos

### ✅ Notificaciones
- Creación y envío
- Configuración de preferencias
- Filtrado por tipo
- Sistema de prioridades

### ✅ Converter
- Conversión de documentos
- Soporte de OCR
- Estados de conversión
- Historial de conversiones

### ✅ Health Checks
- Liveness checks
- Readiness checks
- API info endpoint

## Configuración de Fixtures

Todos los tests utilizan fixtures de pytest para:
- Crear usuarios de prueba
- Configurar clientes API autenticados
- Crear datos de prueba (productos, posts, encuestas, etc.)
- Limpiar la base de datos entre tests (`pytestmark = pytest.mark.django_db`)

## Mejores Prácticas

1. **Aislamiento**: Cada test es independiente y no depende de otros
2. **Limpieza**: La base de datos se limpia automáticamente entre tests
3. **Nombres descriptivos**: Los nombres de los tests describen claramente qué se está probando
4. **Fixtures**: Se reutilizan fixtures para evitar duplicación de código
5. **Assertions claras**: Cada test verifica comportamientos específicos
6. **Documentación**: Cada test tiene un docstring explicativo

## Notas Importantes

### Tests con @pytest.mark.skip
Algunos tests están marcados con `skip` por las siguientes razones válidas:

1. **Endpoints no implementados**: Tests para endpoints que están planificados pero no implementados
2. **Implementación variable**: Tests que dependen de configuraciones específicas
3. **No críticos**: Tests de características opcionales

### Tests Removidos del Skip
- ✅ `TestDocumentConverterAPI`: Ahora completamente funcional
- ✅ `TestNotificationsAPI`: Ahora completamente funcional

## Próximos Pasos

### Tests Pendientes de Implementar
- [ ] Tests E2E con Selenium/Playwright
- [ ] Tests de performance con locust
- [ ] Tests de seguridad (SQL injection, XSS, etc.)
- [ ] Tests de carga para endpoints críticos
- [ ] Tests de integración con servicios externos

### Mejoras Sugeridas
- [ ] Aumentar cobertura de código al 90%+
- [ ] Agregar tests para casos edge
- [ ] Implementar tests de regresión visual
- [ ] Agregar tests de accesibilidad
- [ ] Crear suite de tests de humo para CI/CD

## Ejecución en CI/CD

Para integrar con GitHub Actions u otro sistema CI/CD:

```yaml
# .github/workflows/tests.yml
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
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd proyecto/src/backend
          pytest ../../pruebas_unitarias/ -v --cov=studentspoint
```

## Contacto y Soporte

Para preguntas o problemas con las pruebas, contacta al equipo de desarrollo o crea un issue en el repositorio.

---

**Última actualización**: Noviembre 2024
**Versión de pytest**: 7.x
**Framework de testing**: pytest + pytest-django
