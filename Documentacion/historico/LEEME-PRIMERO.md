#  ¡LEE ESTO PRIMERO!

##  Inicio Super Rápido

### Para Iniciar el Proyecto
```batch
# Windows
iniciar_desarrollo.bat

# Linux/Mac
./iniciar_desarrollo.sh
```

**Eso es TODO lo que necesitas hacer.** 

---

##  ¿Qué Pasará?

Cuando ejecutes el script de inicio:

### 1⃣ Preparación Automática (15 segundos)
-  Instala dependencias
-  Configura base de datos
-  Prepara archivos estáticos
-  Crea directorio de logs
-  Limpia logs antiguos

### 2⃣ Se Abren Automáticamente

**Windows:**
-  **Ventana 1 (Negro/Verde)**: Servidor Django corriendo
-  **Ventana 2 (Amarillo)**: Monitor de logs actualizándose cada 30s
-  **Navegador**: Tu aplicación lista en http://127.0.0.1:8000

**Linux:**
-  **Terminal 1**: Servidor Django
-  **Terminal 2**: Monitor de logs (si aceptas)
-  **Navegador**: http://127.0.0.1:8000 (abre manualmente)

### 3⃣ Los Logs Se Generan Solos
```
proyecto/src/backend/logs/
 general.log       Todos los eventos
 errors.log        Solo errores
 api.log           Peticiones API
 auth.log          Login/registro
```

---

##  ¿Qué Hace el Monitor de Logs?

La **ventana amarilla** muestra cada 30 segundos:

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

**Interpretación:**
-  = Todo bien
-  = Hay warnings o errores (revisar)
-  = Problemas críticos (urgente)

---

##  ¿Cómo Ver los Logs?

### Opción 1: Menu Interactivo (Más Fácil)
```batch
# Windows
ver_logs.bat

# Linux
./ver_logs.sh
```

**Menu con 6 opciones:**
1. Ver todo (general)
2. Solo errores
3. Solo API
4. Solo autenticación
5. Monitor en tiempo real
6. Análisis completo

### Opción 2: Manual
```powershell
# Windows
cd proyecto\src\backend
Get-Content logs\errors.log -Wait

# Linux
cd proyecto/src/backend
tail -f logs/errors.log
```

---

##  ¿Cómo Detener?

### Servidor
```
Presiona Ctrl+C en la ventana del servidor
```

### Monitor (si sigue abierto)
```batch
# Windows
detener_monitor.bat

# O cierra la ventana amarilla manualmente

# Linux
./detener_servicios.sh
```

---

##  Si Algo Sale Mal

### 1. Revisa los Errores
```batch
ver_logs.bat
# Selecciona opción 2 (Errores)
```

### 2. Análisis Completo
```bash
cd proyecto/src/backend
python analyze_logs.py
```

### 3. Verificar Sistema
```bash
cd proyecto/src/backend
python manage.py check
```

---

##  ¿Dónde Buscar Ayuda?

### Documentos Clave (en orden de importancia)

1. **`INDICE-MAESTRO.md`** 
   - Índice de TODA la documentación
   - Busca por tema o tarea
   - Encuentra cualquier documento

2. **`INICIO-RAPIDO-LOGS.md`** 
   - Cómo usar el sistema de logs
   - Comandos más comunes
   - Ejemplos prácticos

3. **`QUICK-START.md`** 
   - Comandos del día a día
   - Troubleshooting rápido
   - Tips y tricks

4. **`README.md`** 
   - Información del proyecto
   - Características
   - Arquitectura

---

##  Tips Importantes

###  Hacer
1. **Inicia con el script**: `iniciar_desarrollo.bat` (no manualmente)
2. **Deja el monitor abierto**: Te avisa de problemas
3. **Revisa logs regularmente**: `ver_logs.bat`
4. **Usa el índice**: `INDICE-MAESTRO.md` para encontrar docs

###  No Hacer
1.  No ignores la ventana amarilla del monitor
2.  No cierres los logs sin revisar errores
3.  No inicies el servidor con `python manage.py runserver` directamente
4.  No borres la carpeta `logs/` (se limpia sola)

---

##  Tu Primer Día con StudentsPoint

### Paso 1: Iniciar (1 minuto)
```batch
1. Doble click: iniciar_desarrollo.bat
2. Espera 15 segundos
3. Se abren 2 ventanas + navegador
```

### Paso 2: Explorar (5 minutos)
```
1. Navega en http://127.0.0.1:8000
2. Login: admin@studentspoint.app / admin123
3. Explora las secciones
```

### Paso 3: Desarrollar
```
1. Edita código
2. Guarda
3. Refresca navegador (Ctrl+R)
4. Mira la ventana amarilla para ver logs
```

### Paso 4: Si Hay Error
```
1. Mira ventana amarilla (monitor)
2. O ejecuta: ver_logs.bat → opción 2
3. Lee el error
4. Arregla
5. Guarda
6. Refresca
```

### Paso 5: Detener
```
1. Ctrl+C en ventana del servidor
2. Cierra ventana amarilla (o detener_monitor.bat)
3. ¡Listo!
```

---

##  Preguntas Frecuentes

### ¿Por qué se abren 2 ventanas?
- Ventana 1 = Servidor (para ver requests)
- Ventana 2 = Monitor (para ver errores y estadísticas)

### ¿Puedo cerrar la ventana amarilla?
- Sí, pero no verás alertas en tiempo real
- Los logs se siguen guardando igual

### ¿Dónde se guardan los logs?
- `proyecto/src/backend/logs/`
- Se crean automáticamente

### ¿Qué pasa si borro la carpeta logs/?
- Se crea automáticamente al iniciar
- Los logs antiguos se pierden (pero hay backups)

### ¿Funciona en producción?
- Sí! Usa `./iniciar_produccion.sh`
- Incluye Gunicorn + monitor + alertas

### ¿Necesito configurar algo?
- **NO** para desarrollo
- **SÍ** para producción (ver `env.production.example`)

---

##  Bonus: Comandos Útiles

```bash
# Ver logs en tiempo real
ver_logs.bat                        # Menu interactivo

# Análisis rápido
cd proyecto/src/backend
python analyze_logs.py

# Ejecutar tests
python run_pytest.py

# Ver documentación
# Abre INDICE-MAESTRO.md en tu editor
```

---

##  Características Destacadas

```
 Inicio en 1 click
 Monitor automático
 Alertas inteligentes
 Detección de N+1
 Cache automático
 Lazy loading
 Performance monitoring
 15+ guías
 Production-ready
```

---

##  TL;DR (Muy Corto)

```batch
# 1. Inicia
iniciar_desarrollo.bat

# 2. Desarrolla
[Edita código, guarda, refresca]

# 3. Si hay error
ver_logs.bat → opción 2

# 4. Detén
Ctrl+C
```

**¡Así de simple!** 

---

##  Siguiente Paso

 Lee [`INDICE-MAESTRO.md`](INDICE-MAESTRO.md) para ver toda la documentación disponible.

 O ve directo a [`INICIO-RAPIDO-LOGS.md`](INICIO-RAPIDO-LOGS.md) para detalles del sistema de logs.

---

**¡Bienvenido a StudentsPoint!** 

Todo está automatizado. Solo ejecuta el script de inicio y comienza a desarrollar.

**No necesitas configurar nada más.** Los logs, el monitoreo y las alertas funcionan solos.

---

**Estado:**  Production-Ready  
**Automatización:** 100%  
**Documentación:** Completa  
**Listo para:** Desarrollo y Producción

