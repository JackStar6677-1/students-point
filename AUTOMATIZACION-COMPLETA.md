#  AUTOMATIZACIÓN COMPLETA - StudentsPoint

##  TODO AUTOMATIZADO

El proyecto StudentsPoint ahora tiene **automatización completa** de inicio, monitoreo y gestión de logs.

---

##  Inicio Automático

### ¿Qué Sucede al Ejecutar los Scripts?

#### Windows: `iniciar_desarrollo.bat`
```
1. Verifica Python
2. Instala dependencias
3. Aplica migraciones
4. Recolecta archivos estáticos
5. Crea superusuario si no existe
6. Crea directorio logs/
7. Limpia logs >50MB
8.  ABRE VENTANA NUEVA con monitor de logs
9. Inicia servidor Django
10. Abre navegador automáticamente
```

**Resultado:**
- **Ventana 1 (Negro/Verde)**: Servidor corriendo
- **Ventana 2 (Amarillo)**: Monitor de logs actualizándose
- **Navegador**: Aplicación lista para usar

#### Linux: `iniciar_desarrollo.sh`
```
1-7. [Igual que Windows]
8.  Detecta terminal disponible (gnome-terminal, xterm, konsole)
9.  Abre monitor en nueva terminal (o background)
10. Inicia servidor Django
```

#### Linux: `iniciar_produccion.sh`
```
Menu con 3 opciones:
1. Gunicorn (Producción) 
   - Inicia Gunicorn con 4 workers
   -  Monitor de logs en background (PID guardado)
   -  Sistema de alertas cada 5 min (PID guardado)
   - PIDs en /tmp/ para control
   
2. Django runserver (Desarrollo)
   - Solo para pruebas
   
3. Gunicorn + Monitor visible
   - Gunicorn en background
   - Monitor en primer plano
   -  Sistema de alertas en background
```

---

##  Sistema de Logs Automático

### Archivos Creados Automáticamente

Al iniciar el servidor, se crean en `proyecto/src/backend/logs/`:

```
logs/
 general.log      #  Auto-creado - Todos los eventos
 errors.log       #  Auto-creado - Solo errores
 api.log          #  Auto-creado - Peticiones API
 auth.log         #  Auto-creado - Autenticación
```

**Características automáticas:**
-  Rotación a 10MB
-  5 backups automáticos
-  Limpieza de logs >50MB al iniciar
-  Formato detallado con timestamps

---

##  Monitoreo Automático

### Monitor de Logs (Ventana Separada)

**Windows:**
- Se abre automáticamente al iniciar
- Título: "StudentsPoint - Monitor de Logs"
- Color: Amarillo (fácil de identificar)
- Actualiza cada 30s

**Linux:**
- Abre en nueva terminal si está disponible
- Si no, corre en background
- PID guardado en `/tmp/studentspoint_monitor.pid`

**Qué muestra:**
```
============================================================
 Resumen de Logs - 2025-10-09 16:30:00
============================================================

 General         - Errores: 0 Warnings: 2 Críticos: 0
 Errores         - Errores: 0 Warnings: 0 Críticos: 0
 API             - Errores: 5 Warnings: 3 Críticos: 0
    3 nuevos errores detectados!
 Autenticación   - Errores: 0 Warnings: 1 Críticos: 0

============================================================
```

---

##  Sistema de Alertas Automático (Producción)

### Al iniciar con `iniciar_produccion.sh` (Opción 1 o 3):

**Se ejecuta automáticamente cada 5 minutos:**
```python
alert_system.py
```

**Verifica:**
-  Tasa de errores por hora
-  Errores críticos
-  Conexión a base de datos
-  Espacio en disco
-  Rendimiento general

**Envía email si:**
-  Más de 50 errores/hora
-  Más de 5 críticos/hora
-  Error de conexión DB
-  Espacio en disco >90%

---

##  Estructura Completa

```
students-point/
 iniciar_desarrollo.bat        #  Inicio Windows (CON LOGS)
 iniciar_desarrollo.sh          #  Inicio Linux (CON LOGS)
 iniciar_produccion.sh          #  Producción (CON LOGS + ALERTAS)

 ver_logs.bat                   #  Ver logs Windows
 ver_logs.sh                    #  Ver logs Linux

 detener_monitor.bat            #  Detener monitor Windows
 detener_servicios.sh           #  Detener todo Linux

 README-LOGS.md                 #  Guía rápida de logs
 INICIO-RAPIDO-LOGS.md         #  Esta guía
 SCRIPTS-DISPONIBLES.md         #  Lista completa de scripts
 RESUMEN-AUTOMATIZACION-LOGS.md #  Resumen técnico

 proyecto/src/backend/
    logs/                      #  Logs (auto-creado)
       general.log
       errors.log
       api.log
       auth.log
   
    monitor_logs.py            #  Monitor
    analyze_logs.py            #  Análisis
    alert_system.py            #  Alertas
   
    studentspoint/
        middleware.py          #  Middleware de logs/queries
        settings/
            base.py            #  Config LOGGING
            prod.py            #  Config producción

 config/systemd/                #  Servicios Linux
     studentspoint-monitor.service
     studentspoint-alerts.service
     README.md
```

---

##  Comandos Más Usados

### Iniciar Proyecto
```batch
# Windows
iniciar_desarrollo.bat

# Linux
./iniciar_desarrollo.sh
```

### Ver Logs
```batch
# Windows
ver_logs.bat

# Linux
./ver_logs.sh
```

### Detener Todo
```batch
# Windows
Ctrl+C en ventanas
detener_monitor.bat (si es necesario)

# Linux
./detener_servicios.sh
```

---

##  Ciclo de Desarrollo Típico

```
1. iniciar_desarrollo.bat
   ↓
2. [Se abren 2 ventanas automáticamente]
   ↓
3. [Desarrollas y ves logs en la ventana amarilla]
   ↓
4. [Si necesitas análisis: ver_logs.bat → opción 6]
   ↓
5. Ctrl+C para detener
```

---

##  Logs que Se Registran Automáticamente

### Eventos Normales
```
[INFO] Servidor iniciado en http://127.0.0.1:8000
[INFO] GET /api/auth/me/ - Usuario: admin@studentspoint.app
[INFO] POST /api/forum/posts/ - Status: 201 - Tiempo: 0.123s
```

### Warnings
```
[WARNING] N+1 Query Alert: /api/forum/posts/ ejecutó 25 queries
[WARNING] Respuesta lenta: /api/posts/ tomó 1.5s
```

### Errores
```
[ERROR] Internal Server Error: /api/forum/posts/
[ERROR] Database connection failed
[CRITICAL] Espacio en disco crítico: 95% usado
```

---

##  Características Automáticas

###  Sin Configuración Manual
- Los logs se crean solos
- El monitor se inicia solo
- Las alertas se ejecutan solas
- La rotación es automática
- La limpieza es automática

###  Inteligente
- Detecta terminal disponible (Linux)
- Abre en ventana nueva si es posible
- Fallback a background si no
- PIDs guardados para control
- Cleanup automático al salir (Ctrl+C)

###  Multiplataforma
- Scripts .bat para Windows
- Scripts .sh para Linux/Mac
- Mismo comportamiento en ambos
- Documentación unificada

---

##  Próximos Pasos

### Ya Configurado
1.  Logging automático
2.  Monitor automático
3.  Alertas automáticas (producción)
4.  Rotación automática
5.  Limpieza automática

### Opcional - Mejorar
1. ⏳ Configurar email SMTP para alertas
2. ⏳ Integrar con Sentry (producción)
3. ⏳ Dashboard web de logs (Grafana/Loki)
4. ⏳ Análisis con IA de patrones de error

---

##  Soporte

**Todo funciona automáticamente**, pero si necesitas ayuda:

1. Lee `README-LOGS.md` para guía completa
2. Ejecuta `ver_logs.bat` y ve el log de errores
3. Ejecuta `python analyze_logs.py` para análisis
4. Revisa `SCRIPTS-DISPONIBLES.md` para lista completa

---

##  Resumen Ejecutivo

**Antes:**
```
 Logs solo en consola
 Se perdían al cerrar
 Sin monitoreo
 Sin alertas
 Configuración manual
```

**Ahora:**
```
 Logs persistentes en archivos
 Monitor en ventana separada (automático)
 Alertas cada 5 min (producción)
 Análisis con un comando
 TODO SE INICIA AUTOMÁTICAMENTE
```

---

**¡Simplemente ejecuta `iniciar_desarrollo.bat` y todo funciona!** 

No más configuración manual. No más logs perdidos. Todo está automatizado.

