#  Índice Maestro - StudentsPoint

##  Para Empezar YA

### Solo quiero iniciar el proyecto
 **`iniciar_desarrollo.bat`** (Windows) o **`iniciar_desarrollo.sh`** (Linux)

### Quiero ver los logs
 **`ver_logs.bat`** (Windows) o **`ver_logs.sh`** (Linux)

### Necesito ayuda rápida
 **`QUICK-START.md`** - Comandos más usados

---

##  Documentación por Tema

###  Inicio y Scripts

| Documento | Descripción | Cuándo Leer |
|-----------|-------------|-------------|
| `INICIO-RAPIDO-LOGS.md` | Guía rápida de logs | **Primero** - Start here |
| `SCRIPTS-DISPONIBLES.md` | Lista completa de scripts | Referencia rápida |
| `QUICK-START.md` | Comandos más usados | Desarrollo diario |
| `AUTOMATIZACION-COMPLETA.md` | Cómo funciona la automatización | Entender el sistema |

###  Sistema de Logs

| Documento | Descripción | Cuándo Leer |
|-----------|-------------|-------------|
| `README-LOGS.md` | Guía completa de logs | Configuración y uso |
| `RESUMEN-AUTOMATIZACION-LOGS.md` | Cómo se automatizó | Detalles técnicos |
| `Documentacion/guias/SISTEMA-LOGGING.md` | Documentación técnica detallada | Desarrollo avanzado |
| `proyecto/src/backend/logs/README.md` | Info rápida de archivos de log | Referencia |

###  Deployment y Producción

| Documento | Descripción | Cuándo Leer |
|-----------|-------------|-------------|
| `Documentacion/guias/DEPLOYMENT-PRODUCTION.md` | Guía completa 70+ pasos | Deploy a producción |
| `DEPLOYMENT.md` | Info general de deployment | Introducción |
| `env.production.example` | Variables de entorno | Configuración |
| `config/systemd/README.md` | Servicios Linux | Producción Linux |

###  Información del Proyecto

| Documento | Descripción | Cuándo Leer |
|-----------|-------------|-------------|
| `PROYECTO-MASTERIZADO.md` | Resumen completo de mejoras | Ver todo lo nuevo |
| `README.md` | Documentación principal | Siempre útil |
| `CHANGELOG.md` | Historial de cambios | Ver evolución |
| `ROADMAP.md` | Planes futuros | Próximas features |

###  Testing

| Documento | Descripción | Cuándo Leer |
|-----------|-------------|-------------|
| `TESTING.md` | Guía de testing | Ejecutar tests |
| `Documentacion/INFORME-TESTS.md` | Informe de tests | Resultados |
| `pruebas_unitarias/README.md` | Tests unitarios | Tests específicos |

###  Documentación Académica

| Directorio | Descripción |
|-----------|-------------|
| `Documentacion/academico/` | Documentos académicos del capstone |
| `Documentacion/especificaciones/` | Specs detalladas de features |
| `Documentacion/guias/` | Guías técnicas |
| `Documentacion/implementaciones/` | Detalles de implementación |

---

##  Guías Rápidas por Tarea

### "Quiero iniciar el proyecto"
1. Windows: Doble click en `iniciar_desarrollo.bat`
2. Linux: `./iniciar_desarrollo.sh`
3. Listo - servidor + logs funcionando

### "Quiero ver qué está pasando en el servidor"
1. Ejecuta `ver_logs.bat` (Windows) o `./ver_logs.sh` (Linux)
2. Selecciona opción 1 (General)
3. Ves logs en tiempo real

### "Quiero ver solo los errores"
1. `ver_logs.bat` → Opción 2
2. O directamente: `Get-Content logs\errors.log -Wait`

### "Quiero análisis detallado"
1. `cd proyecto\src\backend`
2. `python analyze_logs.py`
3. Lee el reporte generado

### "Algo anda mal, ¿cómo lo reviso?"
1. `ver_logs.bat` → Opción 2 (Errores)
2. O `python analyze_logs.py` para reporte completo
3. O revisa `logs/errors.log` directamente

### "Quiero deploy a producción"
1. Lee `Documentacion/guias/DEPLOYMENT-PRODUCTION.md`
2. Configura `env.production.example` → `.env`
3. Ejecuta `./iniciar_produccion.sh`
4. Selecciona opción 1 (Gunicorn)

### "Quiero ejecutar tests"
1. `python run_pytest.py`
2. Lee resultados
3. Si falla algo, revisa logs

---

##  Documentos por Nivel

### Nivel Principiante
Empieza aquí si es tu primera vez:
1. `README.md` - Introducción
2. `INICIO-RAPIDO-LOGS.md` - Cómo iniciar
3. `QUICK-START.md` - Comandos básicos

### Nivel Intermedio
Ya conoces el proyecto:
1. `README-LOGS.md` - Sistema de logs completo
2. `SCRIPTS-DISPONIBLES.md` - Todos los scripts
3. `PROYECTO-MASTERIZADO.md` - Qué hay de nuevo

### Nivel Avanzado
Desarrollo profesional:
1. `Documentacion/guias/SISTEMA-LOGGING.md` - Logs técnico
2. `DEPLOYMENT-PRODUCTION.md` - Deploy completo
3. `studentspoint/middleware.py` - Código fuente
4. `studentspoint/settings/prod.py` - Config producción

---

##  Por Tipo de Archivo

### Archivos .bat (Windows)
```
iniciar_desarrollo.bat         Inicio principal
ver_logs.bat                   Ver logs
detener_monitor.bat            Detener monitor
ejecutar_tests_dev.bat         Tests
instalar_postgresql.bat        Instalar DB
iniciar_produccion.bat         Producción Windows
```

### Archivos .sh (Linux)
```
iniciar_desarrollo.sh          Inicio principal
iniciar_produccion.sh          Producción Linux
ver_logs.sh                    Ver logs
detener_servicios.sh           Detener todo
deploy_linux.sh                Deploy
ejecutar_tests_completo.sh     Tests
```

### Archivos .py (Utilidades)
```
monitor_logs.py                Monitor en tiempo real
analyze_logs.py                Análisis de logs
alert_system.py                Sistema de alertas
run_pytest.py                  Ejecutar tests
create_sample_data.py          Datos de prueba
```

### Archivos .md (Documentación)
```
README.md                      Principal
QUICK-START.md                 Comandos rápidos
PROYECTO-MASTERIZADO.md        Resumen de mejoras
INICIO-RAPIDO-LOGS.md          Logs quick start
README-LOGS.md                 Logs completo
SCRIPTS-DISPONIBLES.md         Scripts
AUTOMATIZACION-COMPLETA.md     Automatización
RESUMEN-AUTOMATIZACION-LOGS.md  Resumen técnico
INDICE-MAESTRO.md             Este archivo
```

---

##  Rutas Rápidas

### "No sé por dónde empezar"
 `README.md` → `INICIO-RAPIDO-LOGS.md` → `iniciar_desarrollo.bat`

### "Quiero entender el sistema de logs"
 `README-LOGS.md` → `SISTEMA-LOGGING.md`

### "Quiero ver todo lo nuevo"
 `PROYECTO-MASTERIZADO.md`

### "Voy a hacer deploy"
 `DEPLOYMENT-PRODUCTION.md`

### "Necesito comandos ahora"
 `QUICK-START.md`

### "¿Qué scripts hay disponibles?"
 `SCRIPTS-DISPONIBLES.md`

---

##  Buscar Información

### Por Palabra Clave

| Busco | Ver |
|-------|-----|
| logs, logging, monitoreo | `README-LOGS.md` |
| scripts, .bat, .sh | `SCRIPTS-DISPONIBLES.md` |
| producción, deploy | `DEPLOYMENT-PRODUCTION.md` |
| tests, testing | `TESTING.md` |
| comandos, quick | `QUICK-START.md` |
| nuevo, masterizado | `PROYECTO-MASTERIZADO.md` |
| automatización | `AUTOMATIZACION-COMPLETA.md` |

---

##  ¿Todavía Tienes Dudas?

1. **Busca en este índice** la palabra clave
2. **Lee el documento recomendado**
3. **Ejecuta el script** correspondiente
4. **Revisa los logs** si algo falla: `ver_logs.bat`

---

##  Los 3 Archivos Más Importantes

Si solo vas a leer 3 documentos, que sean estos:

1. **`README.md`** - Qué es StudentsPoint
2. **`INICIO-RAPIDO-LOGS.md`** - Cómo iniciar y ver logs
3. **`QUICK-START.md`** - Comandos del día a día

---

##  Conclusión

**Todo está automatizado y documentado.**

Solo necesitas:
1. Ejecutar `iniciar_desarrollo.bat`
2. Los logs se manejan solos
3. Ver logs cuando quieras con `ver_logs.bat`

**¡Así de simple!** 

---

**Última actualización:** Octubre 2025  
**Estado:**  Completamente Automatizado  
**Mantenido por:** Equipo StudentsPoint

