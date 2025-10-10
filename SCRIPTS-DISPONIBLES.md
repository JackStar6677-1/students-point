#  Scripts Disponibles - StudentsPoint

Todos los scripts de inicio, monitoreo y utilidades del proyecto.

##  Scripts de Inicio

### Windows (Desarrollo)

#### `iniciar_desarrollo.bat`  PRINCIPAL
Inicia el proyecto completo en modo desarrollo.

**Qué hace:**
-  Instala dependencias automáticamente
-  Aplica migraciones
-  Recolecta archivos estáticos
-  Crea superusuario
-  **Crea directorio de logs**
-  **Limpia logs antiguos**
-  **Inicia monitor de logs en ventana separada** (automático)
-  Inicia el servidor Django
-  Abre navegador automáticamente

**Uso:**
```batch
iniciar_desarrollo.bat
```

**Resultado:**
- Ventana 1: Servidor Django corriendo
- Ventana 2: Monitor de logs en tiempo real (actualiza cada 30s)
- Navegador: Abre automáticamente http://127.0.0.1:8000

---

### Linux/Mac (Desarrollo)

#### `iniciar_desarrollo.sh`  PRINCIPAL
Equivalente al .bat para sistemas Unix.

**Qué hace:**
-  Todas las funciones del .bat de Windows
-  Detecta terminal disponible (gnome-terminal, xterm, konsole)
-  Abre monitor en nueva terminal automáticamente
-  Fallback a background si no hay terminal gráfica

**Uso:**
```bash
chmod +x iniciar_desarrollo.sh
./iniciar_desarrollo.sh
```

---

### Linux (Producción)

#### `iniciar_produccion.sh`  PRODUCCIÓN
Inicia el proyecto en modo producción con Gunicorn.

**Opciones interactivas:**
1. **Gunicorn** - Recomendado (workers múltiples)
2. **Django runserver** - Solo desarrollo
3. **Con monitor** - Gunicorn + monitor en primer plano

**Servicios que inicia automáticamente:**
-  Servidor Gunicorn (4 workers)
-  Monitor de logs (actualiza cada 60s)
-  Sistema de alertas (verifica cada 5 min)

**Uso:**
```bash
chmod +x iniciar_produccion.sh
./iniciar_produccion.sh
```

**Para producción real, usar systemd:**
```bash
# Copiar servicios
sudo cp config/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Iniciar servicios
sudo systemctl start studentspoint-gunicorn
sudo systemctl start studentspoint-monitor
sudo systemctl start studentspoint-alerts

# Habilitar inicio automático
sudo systemctl enable studentspoint-gunicorn
sudo systemctl enable studentspoint-monitor
sudo systemctl enable studentspoint-alerts
```

---

##  Scripts de Monitoreo

### Ver Logs

#### `ver_logs.bat` (Windows)
Menu interactivo para ver logs.

**Opciones:**
1. Log general
2. Solo errores
3. Log de API
4. Log de autenticación
5. Monitor en tiempo real
6. Análisis completo

**Uso:**
```batch
ver_logs.bat
```

#### `ver_logs.sh` (Linux/Mac)
Equivalente para Unix con colores.

**Uso:**
```bash
chmod +x ver_logs.sh
./ver_logs.sh
```

---

### Python Scripts

#### `monitor_logs.py`
Monitor de logs en tiempo real con resumen visual.

**Uso:**
```bash
cd proyecto/src/backend

# Monitor continuo (actualiza cada 60s)
python monitor_logs.py

# Con intervalo personalizado
python monitor_logs.py --interval 30

# Una sola vez
python monitor_logs.py --once

# Ver últimos N errores
python monitor_logs.py --recent 10
```

**Muestra:**
-  Estado de cada archivo de log
-  Contadores de errores, warnings, críticos
-  Alertas de nuevos errores
-  Problemas críticos

---

#### `analyze_logs.py`
Análisis detallado de logs con reportes.

**Uso:**
```bash
cd proyecto/src/backend

# Análisis de últimas 24 horas
python analyze_logs.py

# Personalizar período
python analyze_logs.py --hours 12

# Exportar reporte
python analyze_logs.py --export reporte.txt
```

**Genera:**
-  Resumen general
-  Errores por categoría
- ⏰ Distribución por hora
-  Top 10 errores
-  Recomendaciones

---

#### `alert_system.py`
Sistema de alertas automático.

**Uso:**
```bash
cd proyecto/src/backend
python alert_system.py
```

**Verifica:**
- Tasa de errores
- Salud de BD
- Espacio en disco
- Envía email si hay problemas

---

##  Scripts de Detención

### `detener_monitor.bat` (Windows)
Detiene el monitor de logs.

```batch
detener_monitor.bat
```

### `detener_servicios.sh` (Linux)
Detiene todos los servicios.

```bash
chmod +x detener_servicios.sh
./detener_servicios.sh
```

Detiene:
- Monitor de logs
- Sistema de alertas
- Gunicorn
- Cualquier proceso restante

---

##  Otros Scripts

### `deploy_linux.sh`
Despliegue automático (pull, migrate, collectstatic).

```bash
./deploy_linux.sh
```

### `instalar_postgresql.bat`
Instala PostgreSQL en Windows (opcional).

```batch
instalar_postgresql.bat
```

---

##  Flujo de Trabajo Recomendado

### Desarrollo Diario (Windows)
```batch
1. iniciar_desarrollo.bat          # Inicia todo automáticamente
   - Se abre servidor
   - Se abre monitor de logs (ventana separada)
   - Se abre navegador

2. [Desarrollar...]

3. ver_logs.bat                     # Si necesitas revisar logs
   - Menu interactivo
   
4. Ctrl+C en ventana del servidor   # Para detener

5. detener_monitor.bat              # Si el monitor sigue abierto
```

### Desarrollo Diario (Linux/Mac)
```bash
1. ./iniciar_desarrollo.sh          # Inicia todo
   - Pregunta si abrir monitor en nueva terminal
   
2. [Desarrollar...]

3. ./ver_logs.sh                    # Ver logs (opcional)
   
4. Ctrl+C                           # Detener servidor
```

### Producción (Linux)
```bash
1. ./iniciar_produccion.sh          # Primera vez
   - Selecciona opción 1 (Gunicorn)
   
2. Para servicios permanentes:
   sudo cp config/systemd/*.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable studentspoint-*
   sudo systemctl start studentspoint-*

3. Ver estado:
   sudo systemctl status studentspoint-gunicorn
   
4. Detener:
   ./detener_servicios.sh
   # O con systemd:
   sudo systemctl stop studentspoint-*
```

---

##  Características Automáticas

### Al Iniciar Desarrollo
 Crea directorio `logs/` si no existe  
 Limpia logs >50MB automáticamente  
 Inicia monitor en ventana/terminal separada  
 Los logs se generan en tiempo real  
 No requiere configuración manual  

### Al Iniciar Producción
 Verifica configuración de deployment  
 Inicia monitor de logs en background  
 Inicia sistema de alertas automático  
 Usa Gunicorn con workers múltiples  
 Logs rotan automáticamente  

---

##  Tips

1. **Dos monitores**: Pon el servidor en uno y `ver_logs.bat` en otro
2. **Performance**: El monitor se actualiza cada 30-60s para no consumir recursos
3. **Alertas**: En producción, recibirás emails automáticamente si hay problemas
4. **Scripts .sh**: En Windows con Git Bash también funcionan

---

##  Ayuda Rápida

```bash
# Ver ayuda de un script
python monitor_logs.py --help
python analyze_logs.py --help
python alert_system.py --help
```

---

**¡Todo está automatizado! Solo ejecuta `iniciar_desarrollo.bat` o `iniciar_desarrollo.sh` y el sistema de logs inicia automáticamente.** 

