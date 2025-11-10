#  Guía del Sistema de Logging - StudentsPoint

## Descripción General

StudentsPoint cuenta con un sistema completo de logging que registra todos los eventos importantes de la aplicación en archivos organizados por categoría.

##  Archivos de Log

Todos los logs se guardan en: `proyecto/src/backend/logs/`

| Archivo | Nivel | Descripción |
|---------|-------|-------------|
| `general.log` | INFO+ | Logs generales de toda la aplicación |
| `errors.log` | ERROR+ | Solo errores y críticos |
| `api.log` | DEBUG+ | Peticiones y respuestas de APIs |
| `auth.log` | DEBUG+ | Autenticación y autorización |

##  Configuración

La configuración se encuentra en `proyecto/src/backend/studentspoint/settings/base.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {funcName} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_general': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'general.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        # ... más handlers
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
        },
        # ... más loggers
    },
}
```

##  Uso en el Código

### Importar Logger

```python
import logging

logger = logging.getLogger(__name__)
```

### Niveles de Log

```python
# DEBUG - Información detallada para diagnóstico
logger.debug(f"Usuario {user_id} cargó página de perfil")

# INFO - Eventos informativos
logger.info(f"Nuevo usuario registrado: {user.email}")

# WARNING - Advertencias
logger.warning(f"Intento de acceso a recurso no existente: {resource_id}")

# ERROR - Errores que no detienen la app
logger.error(f"Error al procesar petición: {error}", exc_info=True)

# CRITICAL - Errores críticos
logger.critical(f"Error fatal en base de datos: {error}")
```

### Ejemplos Prácticos

#### En una Vista de API

```python
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger('studentspoint.apps.forum')

@api_view(['POST'])
def crear_post(request):
    try:
        logger.info(f"Usuario {request.user.id} creando nuevo post")
        
        # ... lógica de creación ...
        
        logger.info(f"Post {post.id} creado exitosamente")
        return Response({'id': post.id}, status=201)
        
    except Exception as e:
        logger.error(f"Error creando post: {str(e)}", exc_info=True)
        return Response({'error': 'Error interno'}, status=500)
```

#### En un Modelo

```python
import logging

logger = logging.getLogger('studentspoint')

class Producto(models.Model):
    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Creando nuevo producto: {self.titulo}")
        else:
            logger.debug(f"Actualizando producto: {self.id}")
        
        super().save(*args, **kwargs)
```

#### En Signals

```python
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger('studentspoint.apps.accounts')

@receiver(post_save, sender=User)
def usuario_creado(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Nuevo usuario creado: {instance.email}")
```

##  Monitoreo en Tiempo Real

### Linux/Mac
```bash
# Ver logs en tiempo real
tail -f proyecto/src/backend/logs/general.log

# Ver solo errores
tail -f proyecto/src/backend/logs/errors.log | grep ERROR

# Ver múltiples archivos
tail -f proyecto/src/backend/logs/{general,errors,api}.log
```

### Windows PowerShell
```powershell
# Ver logs en tiempo real
Get-Content proyecto\src\backend\logs\general.log -Wait -Tail 50

# Filtrar errores
Get-Content proyecto\src\backend\logs\general.log -Wait | Where-Object {$_ -match "ERROR"}
```

##  Análisis de Logs

### Buscar Errores Específicos

```bash
# Buscar errores de autenticación
grep "auth" proyecto/src/backend/logs/errors.log

# Buscar por fecha
grep "2025-10-09" proyecto/src/backend/logs/general.log

# Buscar por usuario
grep "user@example.com" proyecto/src/backend/logs/auth.log

# Contar errores
grep -c "ERROR" proyecto/src/backend/logs/general.log
```

### Scripts de Análisis

#### Contar Errores por Tipo
```bash
#!/bin/bash
echo "=== Resumen de Errores ==="
echo "Errores totales: $(grep -c "ERROR" logs/general.log)"
echo "Warnings: $(grep -c "WARNING" logs/general.log)"
echo "Críticos: $(grep -c "CRITICAL" logs/general.log)"
```

#### Errores Más Frecuentes
```bash
grep "ERROR" logs/general.log | \
  sed 's/.*- //' | \
  sort | uniq -c | sort -rn | head -10
```

##  Alertas y Notificaciones

### Script de Monitoreo (ejemplo)

```python
import time
import subprocess

def check_errors():
    result = subprocess.run(
        ['grep', '-c', 'ERROR', 'logs/errors.log'],
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())

last_count = 0
while True:
    current_count = check_errors()
    if current_count > last_count:
        new_errors = current_count - last_count
        print(f" {new_errors} nuevos errores detectados!")
        # Aquí podrías enviar notificación por email/Slack
    last_count = current_count
    time.sleep(60)  # Revisar cada minuto
```

##  Mantenimiento

### Rotación Automática

Los logs rotan automáticamente según configuración:
- Cuando un archivo alcanza 10 MB (general, errors, api) o 5 MB (auth)
- Se mantienen 3-5 archivos de respaldo
- Los archivos antiguos se numeran: `general.log.1`, `general.log.2`, etc.

### Limpieza Manual

```bash
# Eliminar logs antiguos (mantener actuales)
rm logs/*.log.*

# Comprimir logs antiguos
gzip logs/*.log.*

# Limpiar logs de más de 30 días
find logs/ -name "*.log.*" -mtime +30 -delete
```

##  Mejores Prácticas

###  Hacer

1. **Usar el nivel apropiado**
   ```python
   logger.debug("Detalles técnicos")  # Solo en desarrollo
   logger.info("Evento normal")       # Operaciones exitosas
   logger.warning("Situación inusual")  # Atención pero no error
   logger.error("Error recuperable")  # Error manejado
   logger.critical("Error fatal")     # Requiere acción inmediata
   ```

2. **Incluir contexto útil**
   ```python
   logger.info(f"Usuario {user.id} ({user.email}) inició sesión desde {request.META['REMOTE_ADDR']}")
   ```

3. **Usar `exc_info=True` para excepciones**
   ```python
   try:
       # código que puede fallar
   except Exception as e:
       logger.error("Error procesando datos", exc_info=True)
   ```

###  Evitar

1. **No loggear información sensible**
   ```python
   #  MAL
   logger.info(f"Contraseña: {password}")
   
   #  BIEN
   logger.info(f"Usuario autenticado: {username}")
   ```

2. **No hacer logging excesivo**
   ```python
   #  MAL - log en cada iteración
   for item in items:
       logger.debug(f"Procesando {item}")
   
   #  BIEN - log resumen
   logger.info(f"Procesados {len(items)} items")
   ```

3. **No incluir objetos grandes**
   ```python
   #  MAL
   logger.debug(f"Datos completos: {huge_object}")
   
   #  BIEN
   logger.debug(f"Procesando {type(huge_object).__name__} con {len(huge_object)} elementos")
   ```

##  Integración con Herramientas

### Sentry (Recomendado para Producción)

```python
# settings/prod.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
)
```

### ELK Stack (Para análisis avanzado)

Los logs en formato texto pueden ser enviados a Elasticsearch/Logstash/Kibana para análisis visual avanzado.

### Grafana + Loki

Alternativa moderna para monitoreo y visualización de logs.

##  Formato de Logs

Formato actual:
```
[LEVEL] YYYY-MM-DD HH:MM:SS logger_name module function - message
```

Ejemplo real:
```
[INFO] 2025-10-09 16:30:15 studentspoint.apps.accounts views login - Usuario admin@studentspoint.app autenticado exitosamente
[ERROR] 2025-10-09 16:31:22 django.request views handle_error - Internal Server Error: /api/forum/posts/
[WARNING] 2025-10-09 16:32:10 studentspoint.apps.forum services check_moderation - Post 123 requiere moderación manual
```

##  Solución de Problemas

### Los logs no se generan

1. Verificar que la carpeta `logs/` existe y tiene permisos
2. Verificar configuración en `settings/base.py`
3. Verificar que el servidor Django está corriendo
4. Probar manualmente:
   ```python
   import logging
   logger = logging.getLogger('studentspoint')
   logger.info("Test log")
   ```

### Los archivos son muy grandes

- Los logs rotan automáticamente
- Si necesitas reducir el tamaño, ajusta `maxBytes` en settings
- Considera aumentar nivel mínimo de INFO a WARNING en producción

### Pérdida de rendimiento

- Los logs en nivel DEBUG pueden ser costosos
- En producción, usar nivel INFO o WARNING
- Considerar logging asíncrono para alto volumen

---

##  Recursos Adicionales

- [Documentación oficial de logging en Python](https://docs.python.org/3/library/logging.html)
- [Django Logging](https://docs.djangoproject.com/en/5.0/topics/logging/)
- [Logging Best Practices](https://docs.python-guide.org/writing/logging/)

---

**Última actualización:** Octubre 2025  
**Mantenido por:** Equipo StudentsPoint

