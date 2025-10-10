#  Sistema de Logs - Guía Rápida

##  Inicio Automático

### Desarrollo (Windows)
```batch
iniciar_desarrollo.bat
```

Esto automáticamente:
-  Crea el directorio `logs/` si no existe
-  Limpia logs antiguos (>50MB)
-  Inicia el servidor Django
-  Abre ventana separada con monitor de logs en tiempo real
-  Los logs se generan automáticamente en `proyecto/src/backend/logs/`

### Producción (Linux)
```bash
./iniciar_produccion.sh
```

Opciones disponibles:
1. **Gunicorn** - Producción recomendado (inicia monitor automáticamente)
2. **Django runserver** - Solo desarrollo
3. **Con monitor** - Gunicorn + monitor en primer plano

##  Archivos de Log

Los logs se guardan automáticamente en: `proyecto/src/backend/logs/`

| Archivo | Contenido |
|---------|-----------|
| `general.log` | Todos los eventos (INFO+) |
| `errors.log` | Solo errores y críticos |
| `api.log` | Peticiones y respuestas API |
| `auth.log` | Login, registro, OAuth |

##  Ver Logs

### Windows - Interfaz Amigable
```batch
ver_logs.bat
```

Menu interactivo con opciones:
1. Ver log general
2. Ver solo errores
3. Ver log de API
4. Ver log de autenticación
5. Monitor en tiempo real
6. Análisis completo

### Windows - PowerShell Manual
```powershell
# Ver log general en tiempo real
cd proyecto\src\backend
Get-Content logs\general.log -Wait -Tail 50

# Solo errores
Get-Content logs\errors.log -Wait | Where-Object {$_ -match "ERROR"}

# Últimas 100 líneas
Get-Content logs\general.log -Tail 100
```

### Linux/Mac
```bash
cd proyecto/src/backend

# Ver en tiempo real
tail -f logs/general.log

# Solo errores
tail -f logs/errors.log | grep ERROR

# Múltiples archivos
tail -f logs/{general,errors,api}.log
```

##  Monitoreo Avanzado

### Monitor en Tiempo Real
```bash
# Actualiza cada 30 segundos
cd proyecto/src/backend
python monitor_logs.py --interval 30

# Una sola vez
python monitor_logs.py --once

# Ver últimos 10 errores
python monitor_logs.py --recent 10
```

Muestra:
-  Estado de cada log
-  Conteo de errores, warnings, críticos
-  Alertas de nuevos errores
-  Problemas críticos detectados

### Análisis Detallado
```bash
# Análisis de últimas 24 horas
python analyze_logs.py --hours 24

# Exportar reporte
python analyze_logs.py --export reporte_$(date +%Y%m%d).txt

# Últimas 12 horas
python analyze_logs.py --hours 12
```

Genera:
-  Resumen general
-  Errores por categoría
- ⏰ Distribución por hora
-  Top 10 errores más frecuentes
-  Recomendaciones

##  Sistema de Alertas

Se ejecuta automáticamente cada 5 minutos cuando usas `iniciar_produccion.sh`.

Manual:
```bash
python alert_system.py
```

Verifica:
- Tasa de errores por hora
- Errores críticos
- Salud de base de datos
- Espacio en disco

Envía email si detecta problemas críticos.

##  Configuración

### Desarrollo
Los logs están configurados en `settings/base.py`:
- Nivel: DEBUG para apps, INFO para Django
- Rotación: 10MB por archivo
- Backups: 3-5 archivos

### Producción
Los logs se ajustan en `settings/prod.py`:
- Nivel: INFO para apps, WARNING para Django
- Rotación: 10MB por archivo
- Solo errores se envían a `errors.log`

##  Detener Servicios

### Windows
```batch
detener_monitor.bat
```

O cerrar la ventana del monitor manualmente.

### Linux
```bash
./detener_servicios.sh
```

O con systemd:
```bash
sudo systemctl stop studentspoint-monitor
sudo systemctl stop studentspoint-alerts
```

##  Mejores Prácticas

### Revisar Regularmente
```bash
# Cada mañana, revisar errores del día anterior
python analyze_logs.py --hours 24

# Cada semana, análisis completo
python analyze_logs.py --hours 168 --export reporte_semanal.txt
```

### Buscar Problemas Específicos
```bash
# Buscar por usuario
grep "user@example.com" logs/auth.log

# Buscar por fecha
grep "2025-10-09" logs/general.log

# Contar errores
grep -c "ERROR" logs/errors.log
```

### Limpiar Logs Antiguos
Los logs rotan automáticamente, pero puedes limpiar manualmente:

```bash
# Windows
del proyecto\src\backend\logs\*.log.*

# Linux
rm proyecto/src/backend/logs/*.log.*
```

##  Tips

1. **Dos monitores**: Usa el servidor en uno y `ver_logs.bat` en otro
2. **Filtrar por nivel**: Los logs tienen formato `[LEVEL] timestamp ...`
3. **Headers HTTP**: Revisa `X-DB-Query-Count` en respuestas para detectar N+1
4. **Performance**: Agrega `?debug=performance` a URLs para métricas

##  Soporte

Si los logs no se generan:
1. Verifica que `logs/` existe: `mkdir logs`
2. Verifica permisos de escritura
3. Revisa configuración en `settings/base.py` sección LOGGING
4. Ejecuta `python manage.py check`

---

**Los logs se inician automáticamente al ejecutar `iniciar_desarrollo.bat` o `iniciar_produccion.sh`**

No requiere configuración adicional - todo está automatizado! 

