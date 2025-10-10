#  Sistema de Logs Automatizado - Resumen

##  Objetivo Completado

El sistema de logs ahora se **inicia automáticamente** al ejecutar los scripts de inicio, tanto en desarrollo como en producción.

---

##  Archivos Modificados/Creados

### Scripts de Inicio Actualizados

####  `iniciar_desarrollo.bat` (Windows)
**Modificaciones:**
- Crea directorio `logs/` si no existe
- Limpia logs antiguos >50MB automáticamente
- **Inicia monitor de logs en ventana separada** usando `START`
- Muestra información de archivos de log disponibles
- Todo funciona en paralelo (servidor + monitor)

**Uso:**
```batch
iniciar_desarrollo.bat
```

**Resultado:**
- Ventana 1: Servidor Django
- Ventana 2: Monitor de logs (color amarillo, actualiza cada 30s)

####  `iniciar_desarrollo.sh` (Linux/Mac) - NUEVO
**Características:**
- Equivalente al .bat para Unix
- Detecta automáticamente terminal disponible (gnome-terminal, xterm, konsole)
- Abre monitor en nueva terminal
- Fallback a background si no hay terminal gráfica
- Colores y formato amigable

**Uso:**
```bash
chmod +x iniciar_desarrollo.sh
./iniciar_desarrollo.sh
```

####  `iniciar_produccion.sh` - MEJORADO
**Nuevas características:**
- 3 modos de inicio con menu interactivo
- **Modo 1 - Gunicorn**: Inicia automáticamente:
  - Servidor Gunicorn (4 workers)
  - Monitor de logs en background
  - Sistema de alertas (cada 5 min)
- **Modo 2 - Development**: Solo runserver
- **Modo 3 - Con Monitor**: Gunicorn + monitor en primer plano

**Servicios que corre automáticamente:**
```bash
- Gunicorn (PID guardado en /tmp/studentspoint_gunicorn.pid)
- Monitor de logs (PID en /tmp/studentspoint_monitor.pid)
- Sistema de alertas (PID en /tmp/studentspoint_alerts.pid)
```

**Trap para limpieza:** Al presionar Ctrl+C, detiene todos los servicios automáticamente.

---

### Scripts de Visualización (NUEVOS)

####  `ver_logs.bat` (Windows)
Menu interactivo con 6 opciones:
1. Ver log general en tiempo real
2. Ver solo errores con filtro
3. Ver log de API
4. Ver log de autenticación
5. Monitor en tiempo real
6. Análisis completo

**Características:**
- Usa PowerShell para `Get-Content -Wait`
- Filtra contenido automáticamente
- Vuelve al menú después de Ctrl+C

####  `ver_logs.sh` (Linux/Mac)
Equivalente con colores para terminal Unix:
- Colores distintos por tipo de log
- Grep con highlighting automático
- Detecta terminal disponible
- Menu completo igual que Windows

---

### Scripts de Detención (NUEVOS)

####  `detener_monitor.bat` (Windows)
Busca y cierra procesos de `monitor_logs.py`.

####  `detener_servicios.sh` (Linux)
Detiene todos los servicios de StudentsPoint:
- Monitor de logs
- Sistema de alertas
- Gunicorn
- Cualquier proceso restante

Lee PIDs de archivos temporales y hace cleanup.

---

### Configuración Systemd (NUEVO)

####  `config/systemd/studentspoint-monitor.service`
Servicio systemd para monitor de logs en producción.

####  `config/systemd/studentspoint-alerts.service`
Servicio systemd para sistema de alertas.

####  `config/systemd/README.md`
Documentación de instalación y uso de servicios.

**Instalación:**
```bash
sudo cp config/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable studentspoint-monitor
sudo systemctl start studentspoint-monitor
```

---

##  Flujo Automático

### Windows - Desarrollo

```
[Usuario ejecuta iniciar_desarrollo.bat]
    ↓
[Script crea logs/ y limpia antiguos]
    ↓
[Instala deps, migra, collectstatic]
    ↓
[START - Abre nueva ventana CMD]
    ↓
[Ventana nueva: python monitor_logs.py --interval 30]
    ↓
[Ventana principal: python manage.py runserver]
    ↓
[Navegador abre http://127.0.0.1:8000]
    ↓
[LOGS SE GENERAN AUTOMÁTICAMENTE]
    ↓
[Monitor muestra estadísticas cada 30s]
```

### Linux - Producción

```
[Usuario ejecuta ./iniciar_produccion.sh]
    ↓
[Selecciona opción 1: Gunicorn]
    ↓
[Script inicia en background:]
  - Gunicorn (puerto 8000)
  - Monitor de logs (cada 60s)
  - Sistema de alertas (cada 5 min)
    ↓
[Servidor corriendo con PIDs guardados]
    ↓
[LOGS SE GENERAN Y MONITOREAN AUTOMÁTICAMENTE]
    ↓
[Alertas por email si hay problemas]
    ↓
[Ctrl+C o ./detener_servicios.sh para detener]
```

---

##  Archivos de Log Generados

Cuando inicias el servidor, se crean automáticamente:

```
proyecto/src/backend/logs/
 general.log          # Todos los eventos
 errors.log           # Solo errores
 api.log             # Peticiones API
 auth.log            # Autenticación
 README.md           # Documentación
```

**Características:**
-  Rotación automática a 10MB
-  Backups de 3-5 archivos
-  Formato detallado con timestamps
-  Separados por categoría
-  No requiere configuración manual

---

##  Comandos Disponibles

### Ver Logs
```batch
# Windows
ver_logs.bat              # Menu interactivo

# Linux/Mac
./ver_logs.sh             # Menu interactivo con colores
```

### Monitoreo
```bash
cd proyecto/src/backend

# Monitor continuo
python monitor_logs.py

# Análisis
python analyze_logs.py --hours 24

# Alertas
python alert_system.py
```

### Detener
```batch
# Windows
detener_monitor.bat

# Linux
./detener_servicios.sh
```

---

##  Lo Que Se Loggea Automáticamente

### General (INFO+)
- Inicio del servidor
- Carga de aplicaciones
- Configuración de middleware
- Eventos del sistema

### Errores (ERROR+)
- Excepciones no manejadas
- Errores de base de datos
- Errores de validación
- Problemas críticos

### API (DEBUG+)
-  Peticiones entrantes: `[INFO] GET /api/forum/posts/ - Usuario: admin@...`
-  Respuestas: `[INFO] GET /api/forum/posts/ - Status: 200 - Tiempo: 0.123s`
-  Queries N+1: `[WARNING] N+1 Query Alert: /api/forum/posts/ ejecutó 35 queries`
-  APIs lentas: `[WARNING] Respuesta lenta: /api/... tomó 1.5s`

### Auth (DEBUG+)
- Login exitoso/fallido
- Registro de usuarios
- Verificación de email
- OAuth operations
- Cambios de contraseña

---

##  Ejemplos de Logs

### Log General
```
[INFO] 2025-10-09 16:30:15 django.server basehttp run - "GET /api/auth/me/ HTTP/1.1" 200 1234
[INFO] 2025-10-09 16:30:16 studentspoint.apps.accounts views login - Usuario admin@studentspoint.app autenticado exitosamente
```

### Log de Errores
```
[ERROR] 2025-10-09 16:31:22 django.request views handle_error - Internal Server Error: /api/forum/posts/
Traceback (most recent call last):
  File "/path/to/views.py", line 123, in create_post
    ...
```

### Log de API con Query Alert
```
[INFO] 2025-10-09 16:32:10 studentspoint middleware process_request -  GET /api/forum/posts/ - Usuario: test@example.com
[WARNING] 2025-10-09 16:32:11 studentspoint middleware process_response -  N+1 Query Alert: /api/forum/posts/ ejecutó 25 queries en 0.45s
[INFO] 2025-10-09 16:32:11 studentspoint middleware process_response -  GET /api/forum/posts/ - Status: 200 - Tiempo: 0.456s
```

---

##  Ventajas de la Automatización

### Antes
-  Logs se perdían en consola
-  Difícil de revisar problemas pasados
-  Sin alertas automáticas
-  Monitoreo manual
-  Queries N+1 sin detectar

### Ahora
-  Logs persistentes en archivos
-  Historial completo con timestamps
-  Alertas automáticas por email
-  Monitor en ventana separada
-  Detección automática de N+1
-  Headers HTTP con métricas
-  Análisis con un comando
-  **TODO AUTOMÁTICO AL INICIAR**

---

##  Para Empezar

**Solo necesitas:**

1. Ejecutar el script de inicio apropiado
2. ¡Listo! Los logs se generan automáticamente

**Para ver logs:**

- Windows: Ejecuta `ver_logs.bat`
- Linux: Ejecuta `./ver_logs.sh`
- O revisa directamente: `proyecto/src/backend/logs/`

**Para análisis:**

```bash
cd proyecto/src/backend
python analyze_logs.py
```

---

##  Documentación Relacionada

- `README-LOGS.md` - Guía rápida de logs
- `SCRIPTS-DISPONIBLES.md` - Todos los scripts disponibles
- `Documentacion/guias/SISTEMA-LOGGING.md` - Documentación completa
- `QUICK-START.md` - Comandos rápidos

---

**¡Todo está automatizado! Simplemente inicia el servidor y los logs funcionan automáticamente.** 

