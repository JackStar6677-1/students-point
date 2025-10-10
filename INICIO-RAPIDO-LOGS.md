#  Inicio Rápido - Sistema de Logs

##  Para Iniciar (Con Logs Automáticos)

### Windows
```batch
iniciar_desarrollo.bat
```

**Se abrirán automáticamente:**
-  Ventana 1: Servidor Django
-  Ventana 2: Monitor de Logs (amarillo)
-  Navegador: http://127.0.0.1:8000

### Linux/Mac
```bash
chmod +x iniciar_desarrollo.sh
./iniciar_desarrollo.sh
```

**Te preguntará:**
- ¿Limpiar cache? (s/N)
- ¿Abrir monitor de logs? (S/n)

Si dices sí, abre una nueva terminal con el monitor.

---

##  Ver Logs en Cualquier Momento

### Opción 1: Menu Interactivo (Recomendado)

#### Windows
```batch
ver_logs.bat
```

#### Linux/Mac
```bash
chmod +x ver_logs.sh
./ver_logs.sh
```

**Menu:**
```
1) General (todos los eventos)
2) Errores (solo errores)
3) API (peticiones)
4) Autenticación (login/registro)
5) Monitor en Tiempo Real
6) Análisis Completo
7) Salir
```

### Opción 2: PowerShell Manual (Windows)

```powershell
cd proyecto\src\backend

# Ver en tiempo real
Get-Content logs\general.log -Wait -Tail 50

# Solo errores
Get-Content logs\errors.log -Wait

# API
Get-Content logs\api.log -Wait -Tail 40
```

### Opción 3: Terminal (Linux/Mac)

```bash
cd proyecto/src/backend

# Ver en tiempo real
tail -f logs/general.log

# Solo errores
tail -f logs/errors.log

# Con colores
tail -f logs/errors.log | grep --color=always ERROR
```

---

##  Scripts de Análisis

### Monitor en Tiempo Real
```bash
cd proyecto/src/backend
python monitor_logs.py
```

**Muestra cada 30-60s:**
```
============================================================
 Resumen de Logs - 2025-10-09 16:30:00
============================================================

 General         - Errores: 0 Warnings: 2 Críticos: 0
 Errores         - Errores: 0 Warnings: 0 Críticos: 0
 API             - Errores: 5 Warnings: 3 Críticos: 0
 Autenticación   - Errores: 0 Warnings: 1 Críticos: 0

============================================================
```

### Análisis Detallado
```bash
cd proyecto/src/backend
python analyze_logs.py --hours 24
```

**Genera:**
```
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
   ...

 RECOMENDACIONES:
    Sistema funcionando correctamente
```

---

##  Detener

### Windows
```batch
# Cerrar ventana del servidor (Ctrl+C)
# Cerrar ventana del monitor (Ctrl+C)

# O usar:
detener_monitor.bat
```

### Linux
```bash
# Si usaste iniciar_desarrollo.sh:
Ctrl+C en el servidor

# Si usaste iniciar_produccion.sh:
./detener_servicios.sh

# O con systemd:
sudo systemctl stop studentspoint-monitor
sudo systemctl stop studentspoint-alerts
```

---

##  Ubicación de Logs

**Directorio:** `proyecto/src/backend/logs/`

**Archivos generados automáticamente:**
- `general.log` - Todo (INFO+)
- `errors.log` - Errores (ERROR+)
- `api.log` - APIs (DEBUG+)
- `auth.log` - Auth (DEBUG+)

**Se crean automáticamente al iniciar el servidor.**

---

##  Tips Rápidos

### Desarrollo con Dos Monitores
```
Monitor 1: iniciar_desarrollo.bat (servidor)
Monitor 2: ver_logs.bat (logs)
```

### Ver Solo Errores Críticos
```powershell
# Windows
Get-Content logs\errors.log | Select-String "CRITICAL"

# Linux
grep CRITICAL logs/errors.log
```

### Performance Debug
```
Agregar a URL: ?debug=performance
Ejemplo: http://127.0.0.1:8000/?debug=performance

Ver headers HTTP:
- X-DB-Query-Count
- X-DB-Query-Time
```

### Buscar en Logs
```bash
# Por usuario
grep "admin@studentspoint.app" logs/auth.log

# Por fecha
grep "2025-10-09" logs/general.log

# Por error específico
grep -i "database" logs/errors.log
```

---

##  Verificación Rápida

**¿Los logs están funcionando?**

1. Inicia el servidor: `iniciar_desarrollo.bat`
2. Abre otra terminal: `ver_logs.bat`
3. Selecciona opción 1 (General)
4. Deberías ver logs aparecer en tiempo real

**Si no ves logs:**
- Verifica que `logs/` existe
- Ejecuta: `python manage.py check`
- Revisa la consola del servidor

---

##  Problemas Comunes

### "Archivo de log no encontrado"
**Solución:** Inicia el servidor primero con `iniciar_desarrollo.bat`

### "Monitor no se cierra"
**Solución:** 
- Windows: `detener_monitor.bat`
- Linux: `./detener_servicios.sh`

### "Logs muy grandes"
**Solución:** Se limpian automáticamente al iniciar (>50MB)

### "No veo el monitor en Windows"
**Solución:** Se abre en ventana separada. Busca en la barra de tareas "StudentsPoint - Monitor de Logs"

---

##  Ayuda

```bash
# Ayuda de scripts Python
python monitor_logs.py --help
python analyze_logs.py --help
python alert_system.py --help
```

---

##  Resumen

1. **Inicia con**: `iniciar_desarrollo.bat` o `./iniciar_desarrollo.sh`
2. **Los logs se generan automáticamente**
3. **El monitor se abre solo (ventana separada)**
4. **Ver logs cuando quieras**: `ver_logs.bat` o `./ver_logs.sh`
5. **Detener todo**: Ctrl+C en el servidor

**¡No requiere configuración adicional!** 

---

Más info en:
- `README-LOGS.md` - Guía completa
- `SCRIPTS-DISPONIBLES.md` - Lista de scripts
- `Documentacion/guias/SISTEMA-LOGGING.md` - Documentación técnica

