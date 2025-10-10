#  Cómo Se Ve el Sistema - StudentsPoint

##  Al Ejecutar `iniciar_desarrollo.bat` (Windows)

### Ventana 1: Servidor Django (Negro/Verde)
```
============================================================
   StudentsPoint - Modo Desarrollo
============================================================

Verificando Python...
[OK] Python encontrado

Instalando dependencias...
[OK] Dependencias instaladas

Verificando configuración...
[OK] Configuración correcta

Aplicando migraciones...
[OK] Migraciones aplicadas

Recolectando archivos estáticos (forzado)...
[OK] Archivos estáticos actualizados

Creando superusuario...
[OK] Superusuario configurado

[OK] Logs listos

============================================================
   SERVIDOR LISTO
============================================================

Aplicacion: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin/
API Docs: http://127.0.0.1:8000/api/docs/

Credenciales: admin@studentspoint.app / admin123

[LOGS] Sistema de logging activo en: logs/
  - general.log: Todos los eventos
  - errors.log: Solo errores
  - api.log: Peticiones API
  - auth.log: Autenticacion

Presiona Ctrl+C para detener el servidor

Iniciando monitor de logs...
Iniciando servidor...

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 09, 2025 - 16:30:00
Django version 5.2.6, using settings 'studentspoint.settings.dev'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

[09/Oct/2025 16:30:05] "GET / HTTP/1.1" 302 0
[09/Oct/2025 16:30:05] "GET /index.html HTTP/1.1" 200 19696
[09/Oct/2025 16:30:06] "GET /static/css/theme-dark.css HTTP/1.1" 200 12345
...
```

### Ventana 2: Monitor de Logs (Amarillo)
```
StudentsPoint - Monitor de Logs

 Iniciando monitoreo continuo (intervalo: 30s)
 Presiona Ctrl+C para detener

============================================================
 Resumen de Logs - 2025-10-09 16:30:00
============================================================

 General         - Errores: 0 Warnings: 2 Críticos: 0
 Errores         - Errores: 0 Warnings: 0 Críticos: 0
 API             - Errores: 0 Warnings: 1 Críticos: 0
 Autenticación   - Errores: 0 Warnings: 0 Críticos: 0

============================================================

[Actualiza cada 30 segundos...]

============================================================
 Resumen de Logs - 2025-10-09 16:30:30
============================================================

 General         - Errores: 0 Warnings: 2 Críticos: 0
 API             - Errores: 3 Warnings: 2 Críticos: 0
    3 nuevos errores detectados!
    Problemas críticos: Database
 Autenticación   - Errores: 0 Warnings: 0 Críticos: 0

============================================================
```

### Navegador: Aplicación
```
http://127.0.0.1:8000

[Se abre automáticamente mostrando la página principal]
```

---

##  Al Ejecutar `ver_logs.bat`

### Menu Principal
```
============================================================
   Ver Logs - StudentsPoint
============================================================

Selecciona el log que deseas ver:

  1) General (todos los eventos)
  2) Errores (solo errores)
  3) API (peticiones y respuestas)
  4) Autenticacion (login, registro, etc)
  5) Monitor en Tiempo Real
  6) Analisis Completo
  7) Volver

Opcion (1-7): _
```

### Si Seleccionas Opción 1 (General)
```
============================================================
   Log General - Presiona Ctrl+C para volver
============================================================

[INFO] 2025-10-09 16:30:15 django.server basehttp run - "GET /api/auth/me/ HTTP/1.1" 200 1234
[INFO] 2025-10-09 16:30:16 studentspoint.apps.accounts views login - Usuario admin@studentspoint.app autenticado exitosamente
[INFO] 2025-10-09 16:30:17 studentspoint middleware process_request -  GET /api/forum/posts/ - Usuario: admin@studentspoint.app
[INFO] 2025-10-09 16:30:17 studentspoint middleware process_response -  GET /api/forum/posts/ - Status: 200 - Tiempo: 0.123s
[INFO] 2025-10-09 16:30:20 django.server basehttp run - "POST /api/forum/posts/ HTTP/1.1" 201 567

[Se actualiza en tiempo real...]
[Presiona Ctrl+C para volver al menú]
```

### Si Seleccionas Opción 2 (Errores)
```
============================================================
   Log de Errores - Presiona Ctrl+C para volver
============================================================

[ERROR] 2025-10-09 16:31:22 django.request views handle_error - Internal Server Error: /api/forum/posts/
[ERROR] 2025-10-09 16:31:23 studentspoint.apps.forum views create_post - Validation error: {'titulo': ['Este campo es requerido']}
[WARNING] 2025-10-09 16:31:25 studentspoint middleware process_response -  N+1 Query Alert: /api/forum/posts/ ejecutó 25 queries

[Si no hay errores:]
[INFO] No hay errores registrados aun
[INFO] Esto es bueno - significa que no hay errores!
```

### Si Seleccionas Opción 6 (Análisis)
```
============================================================
   Analisis de Logs
============================================================

Horas a analizar (default 24): 24

============================================================
 REPORTE DE ANÁLISIS DE LOGS - Últimas 24 horas
============================================================

 RESUMEN GENERAL
   Total de errores: 12
   Período: 2025-10-08 16:30 - 2025-10-09 16:30

 ERRORES POR CATEGORÍA:
   api            :  (8)
   auth           :  (3)
   database       :  (1)

⏰ DISTRIBUCIÓN POR HORA:
   2025-10-09 15:00:  (4)
   2025-10-09 16:00:  (8)

 TOP 10 ERRORES MÁS FRECUENTES:
   1. [5x] forum.views.create_post: Validation error...
   2. [3x] accounts.views.login: Invalid credentials...

 RECOMENDACIONES:
     Alto número de errores de API - revisar validaciones

============================================================

[Presiona Enter para continuar...]
[Vuelve al menú]
```

---

##  Al Ejecutar `./iniciar_produccion.sh` (Linux)

### Pantalla Inicial
```
============================================================
   StudentsPoint - Modo Producción
============================================================

[OK] Cargando variables de entorno...
¿Actualizar código desde Git? (s/N): n

[OK] Activando entorno virtual...
[INFO] Instalando dependencias...
[INFO] Verificando configuración...
System check identified no issues (0 silenced).

[INFO] Aplicando migraciones...
Operations to perform:
  Apply all migrations: accounts, admin, auth, campuses, ...
Running migrations:
  No migrations to apply.

[INFO] Recolectando archivos estáticos...
223 static files copied to '/home/user/staticfiles'.

[OK] Directorio de logs creado/verificado
[INFO] Limpiando logs antiguos...
[OK] Logs listos

============================================================
   SERVIDOR LISTO PARA PRODUCCIÓN
============================================================

Aplicación: http://192.168.1.100:8000
Admin: http://192.168.1.100:8000/admin/
API Docs: http://192.168.1.100:8000/api/docs/

[LOGS] Sistema de logging activo en: logs/
  - general.log: Todos los eventos
  - errors.log: Solo errores
  - api.log: Peticiones API
  - auth.log: Autenticación

Opciones de inicio:
  1) Gunicorn (Producción - recomendado)
  2) Django runserver (Solo desarrollo)
  3) Con monitor de logs en segundo plano

Selecciona opción (1-3): 1

[OK] Iniciando con Gunicorn...
[INFO] Iniciando monitor de logs en segundo plano...
[OK] Monitor de logs iniciado (PID: 12345)
[OK] Sistema de alertas iniciado (PID: 12346)

Iniciando Gunicorn...
Presiona Ctrl+C para detener el servidor

[2025-10-09 16:30:00 +0000] [12347] [INFO] Starting gunicorn 20.1.0
[2025-10-09 16:30:00 +0000] [12347] [INFO] Listening at: http://0.0.0.0:8000
[2025-10-09 16:30:00 +0000] [12347] [INFO] Using worker: sync
[2025-10-09 16:30:00 +0000] [12350] [INFO] Booting worker with pid: 12350
[2025-10-09 16:30:00 +0000] [12351] [INFO] Booting worker with pid: 12351
[2025-10-09 16:30:00 +0000] [12352] [INFO] Booting worker with pid: 12352
[2025-10-09 16:30:00 +0000] [12353] [INFO] Booting worker with pid: 12353
```

### En Background (No Visible)
```
Monitor de logs:
  - PID: 12345
  - Output: /tmp/monitor_logs.out
  - Actualiza cada 60s
  - Loggea problemas

Sistema de alertas:
  - PID: 12346
  - Output: /tmp/alert_system.out
  - Verifica cada 5 min
  - Envía emails si hay problemas
```

---

##  Frontend en Navegador

### Con Performance Debug (?debug=performance)
```
Consola del Navegador (F12):

 Performance Metrics
⏱ Total Page Load: 1234ms
   DNS: 45ms
   TCP: 78ms
   Request: 123ms
   Response: 234ms
   DOM Processing: 456ms
   DOM Complete: 289ms
   Load Event: 9ms

 Performance Report
Page Load: 1234ms
API Calls: 5 (avg: 123ms)
Slow APIs: 0

 Datos servidos desde caché: /api/forum/posts/
 Datos guardados en caché: /api/auth/me/
```

---

##  Colores y Símbolos

### En Monitor de Logs
```
 = Todo OK (sin errores)
 = Warnings detectados (atención)
 = Errores críticos (revisar)
 = Nuevos errores detectados
 = Problemas críticos serios
```

### En Consola del Servidor
```
[INFO]     = Verde claro (información)
[WARNING]  = Amarillo (advertencia)
[ERROR]    = Rojo (error)
[CRITICAL] = Rojo brillante (crítico)
```

### En Scripts de Análisis
```
 = Resumen
 = Por categoría
⏰ = Por hora
 = Top errores
 = Recomendaciones
```

---

##  Vista de Archivos de Log

### general.log
```
[INFO] 2025-10-09 16:30:00 django.utils.autoreload run_with_reloader - Watching for file changes
[INFO] 2025-10-09 16:30:01 django.db.backends.base.base ensure_connection - Ensured database connection
[INFO] 2025-10-09 16:30:05 django.server basehttp run - "GET / HTTP/1.1" 302 0
[INFO] 2025-10-09 16:30:05 django.server basehttp run - "GET /index.html HTTP/1.1" 200 19696
[INFO] 2025-10-09 16:30:15 studentspoint middleware process_request -  GET /api/auth/me/ - Usuario: admin@studentspoint.app
[INFO] 2025-10-09 16:30:15 studentspoint middleware process_response -  GET /api/auth/me/ - Status: 200 - Tiempo: 0.045s
```

### errors.log
```
[ERROR] 2025-10-09 16:31:22 django.request views handle_error - Internal Server Error: /api/forum/posts/
Traceback (most recent call last):
  File "/path/studentspoint/apps/forum/views.py", line 145, in perform_create
    serializer.save(usuario=self.request.user)
  File "/path/rest_framework/serializers.py", line 230, in save
    self.instance = self.create(validated_data)
ValidationError: {'titulo': ['Este campo es requerido']}

[WARNING] 2025-10-09 16:32:10 studentspoint middleware process_response -  N+1 Query Alert: /api/forum/posts/ ejecutó 25 queries en 0.45s
```

### api.log
```
[DEBUG] 2025-10-09 16:30:15 studentspoint.apps.forum views get_queryset - Cargando posts del foro 1
[INFO] 2025-10-09 16:30:15 studentspoint middleware process_request -  GET /api/forum/posts/?foro_id=1 - Usuario: test@example.com
[INFO] 2025-10-09 16:30:15 studentspoint middleware process_response -  GET /api/forum/posts/ - Status: 200 - Tiempo: 0.123s
[DEBUG] 2025-10-09 16:30:20 studentspoint.apps.forum views perform_create - Creando nuevo post en foro 1
[INFO] 2025-10-09 16:30:20 studentspoint middleware process_request -  POST /api/forum/posts/ - Usuario: test@example.com
[INFO] 2025-10-09 16:30:20 studentspoint middleware process_response -  POST /api/forum/posts/ - Status: 201 - Tiempo: 0.234s
```

### auth.log
```
[INFO] 2025-10-09 16:28:45 studentspoint.apps.accounts views register - Nuevo usuario registrado: test@example.com
[DEBUG] 2025-10-09 16:28:46 studentspoint.apps.accounts views verificar_email - Código de verificación enviado a test@example.com
[INFO] 2025-10-09 16:29:10 studentspoint.apps.accounts views verificar_email - Email verificado: test@example.com
[INFO] 2025-10-09 16:30:00 studentspoint.apps.accounts views login - Usuario admin@studentspoint.app autenticado exitosamente
[WARNING] 2025-10-09 16:31:15 studentspoint.apps.accounts views login - Intento de login fallido: wrong@example.com
```

---

##  Layout de Pantalla Ideal (Desarrollo)

```
+----------------------------------+----------------------------------+
|                                  |                                  |
|  Ventana 1: Servidor Django      |  Ventana 2: Monitor de Logs      |
|  (Negro/Verde)                   |  (Amarillo)                      |
|                                  |                                  |
|  Django version 5.2.6            |   Resumen de Logs              |
|  Starting server at :8000        |                                  |
|                                  |   General - OK                 |
|  [09/Oct/2025 16:30:05]          |   Errores - OK                 |
|  "GET / HTTP/1.1" 302 0          |   API - 3 errores              |
|  [09/Oct/2025 16:30:05]          |   Auth - OK                    |
|  "GET /index.html" 200           |                                  |
|  [09/Oct/2025 16:30:06]          |  [Actualiza cada 30s]            |
|  "GET /static/css..." 200        |                                  |
|                                  |                                  |
+----------------------------------+----------------------------------+
|                                  |
|  Navegador: http://127.0.0.1:8000                                  |
|  (Se abre automáticamente)                                         |
|                                                                     |
+---------------------------------------------------------------------+
```

---

##  En tu Editor de Código

### VS Code / Cursor

```
Panel Inferior → Terminal

Terminal 1: Servidor (iniciar_desarrollo.bat)
Terminal 2: Logs (ver_logs.bat)
Terminal 3: Tests (python run_pytest.py)

[Sidebar]
- INDICE-MAESTRO.md     ← Start here
- logs/
  - general.log         ← Click para ver
  - errors.log          ← Click para ver errores
```

---

##  Workflow Visual

```
[Double click: iniciar_desarrollo.bat]
          ↓
    [Espera 10-15s]
          ↓
    
     Se abren 3  
       ventanas  
    
          ↓
    
     1. Servidor (negro)     
     2. Monitor (amarillo)   
     3. Navegador (web)      
    
          ↓
    [Desarrollas]
          ↓
    
     Monitor muestra:        
     - Estado de logs        
     - Nuevos errores        
     - Estadísticas          
    
          ↓
    [Si hay problema]
          ↓
    
     ver_logs.bat            
     → Opción 2 (Errores)    
     → Lees el error         
     → Arreglas              
    
          ↓
    [Ctrl+C para detener]
```

---

##  Headers HTTP Visibles

En las respuestas HTTP (ver con DevTools):

```
HTTP/1.1 200 OK
Content-Type: application/json
X-DB-Query-Count: 15          ← Queries ejecutadas
X-DB-Query-Time: 0.123s       ← Tiempo de queries
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
...
```

**Si ves:**
- `X-DB-Query-Count: 50+` →  Problema N+1
- `X-DB-Query-Time: >1s` →  Queries lentas

---

##  Experiencia Visual Completa

### Inicio
1.  Doble click en .bat
2.  Ventana negra con progreso
3.  Ventana amarilla aparece
4.  Navegador abre
5.  Todo en 15 segundos

### Durante Desarrollo
1.  Ves código en editor
2.  Ves logs en ventana amarilla
3.  Ves app en navegador
4.  Monitor alerta si hay errores

### Al Detectar Error
1.  Ventana amarilla muestra alerta
2.  Abres `ver_logs.bat`
3.  Seleccionas opción 2 (Errores)
4.  Lees el error detallado
5.  Arreglas el problema

---

##  Resumen Visual

**Antes:**
```
[ Terminal con logs mezclados ]
  ↓
[ Difícil de leer ]
  ↓
[ Se pierde info ]
```

**Ahora:**
```
[ Ventana 1: Servidor limpio ]
[ Ventana 2: Monitor organizado ]
[ Navegador: App funcionando ]
  ↓
[ Logs en archivos separados ]
  ↓
[ Análisis con un comando ]
  ↓
[ TODO VISIBLE Y ORGANIZADO ]
```

---

**¡Ahora sabes exactamente qué esperar al iniciar el proyecto!** 

