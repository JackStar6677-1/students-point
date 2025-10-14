# Guia Completa - StudentsPoint

## Inicio Rapido

### Para Iniciar el Proyecto AHORA MISMO

#### Windows
```batch
iniciar_desarrollo.bat
```
Doble click y listo. Se abriran 2 ventanas automaticamente.

#### Linux/Mac
```bash
chmod +x iniciar_desarrollo.sh
./iniciar_desarrollo.sh
```
Todo se configura automaticamente.

---

## Que Obtienes

### Al Ejecutar el Script de Inicio

1. **Servidor Django funcionando**
   - Puerto: 8000
   - Auto-reload activado
   - Navegador abre solo

2. **Monitor de Logs (Ventana separada)**
   - Actualiza cada 30s
   - Muestra errores nuevos
   - Con colores para facil lectura

3. **Logs Automaticos**
   - 4 archivos: general, errors, api, auth
   - Se generan solos
   - Rotan automaticamente

---

## 3 Comandos Que Necesitas

### 1. Iniciar
```batch
iniciar_desarrollo.bat
```

### 2. Ver Logs
```batch
ver_logs.bat
```

### 3. Detener
```
Ctrl+C (en ventana del servidor)
```

---

## Que Pasara

Cuando ejecutes el script de inicio:

### Preparacion Automatica (15 segundos)
- Instala dependencias
- Configura base de datos
- Prepara archivos estaticos
- Crea directorio de logs
- Limpia logs antiguos

### Se Abren Automaticamente

**Windows:**
- **Ventana 1 (Negro/Verde)**: Servidor Django corriendo
- **Ventana 2 (Amarillo)**: Monitor de logs actualizandose cada 30s
- **Navegador**: Tu aplicacion lista en http://127.0.0.1:8000

**Linux:**
- **Terminal 1**: Servidor Django
- **Terminal 2**: Monitor de logs (si aceptas)
- **Navegador**: http://127.0.0.1:8000 (abre manualmente)

### Los Logs Se Generan Solos
```
proyecto/src/backend/logs/
  general.log       Todos los eventos
  errors.log        Solo errores
  api.log           Peticiones API
  auth.log          Login/registro
```

---

## Como Ver los Logs

### Opcion 1: Menu Interactivo (Mas Facil)
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
4. Solo autenticacion
5. Monitor en tiempo real
6. Analisis completo

### Opcion 2: Manual
```powershell
# Windows
cd proyecto\src\backend
Get-Content logs\errors.log -Wait

# Linux
cd proyecto/src/backend
tail -f logs/errors.log
```

---

## Como Detener

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

## Comandos Comunes

### Desarrollo
```bash
# Iniciar servidor
cd proyecto\src\backend
python manage.py runserver

# Ver logs en tiempo real
Get-Content logs\general.log -Wait -Tail 50

# Monitorear rendimiento
python monitor_logs.py

# Ejecutar tests
cd ..\..\..
python run_pytest.py
```

### Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell
```

### Archivos Estaticos
```bash
# Recolectar estaticos
python manage.py collectstatic --noinput

# Limpiar y recolectar
python manage.py collectstatic --noinput --clear
```

### Debugging
```bash
# Ver logs de errores
Get-Content logs\errors.log -Wait -Tail 20  # Windows
tail -f logs/errors.log  # Linux/Mac

# Ver logs de API
Get-Content logs\api.log -Wait  # Windows

# Ver logs de autenticacion
tail -f logs/auth.log  # Linux/Mac

# Verificar sistema
python manage.py check
python manage.py check --deploy  # Para produccion
```

---

## URLs Importantes

- **Frontend**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **Health**: http://127.0.0.1:8000/health/

**Credenciales por defecto:**
- Email: `admin@studentspoint.app`
- Password: `admin123`

---

## Si Algo Sale Mal

### 1. Revisa los Errores
```batch
ver_logs.bat
# Selecciona opcion 2 (Errores)
```

### 2. Analisis Completo
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

## Troubleshooting Rapido

### Error: Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: Database locked
```bash
# Cerrar todas las conexiones
python manage.py dbshell
.quit
```

### Error: Static files not found
```bash
python manage.py collectstatic --noinput --clear
```

### Error: Permission denied (logs)
```bash
# Windows (ejecutar PowerShell como Admin)
icacls logs /grant Users:F /T

# Linux/Mac
chmod -R 755 logs/
```

---

## Donde Buscar Ayuda

### Documentos Clave (en orden de importancia)

1. **`INDICE-MAESTRO.md`** 
   - Indice de TODA la documentacion
   - Busca por tema o tarea
   - Encuentra cualquier documento

2. **`INICIO-RAPIDO-LOGS.md`** 
   - Como usar el sistema de logs
   - Comandos mas comunes
   - Ejemplos practicos

3. **`SCRIPTS-DISPONIBLES.md`** 
   - Todos los scripts disponibles
   - Como usarlos
   - Para que sirven

4. **`README.md`** 
   - Informacion del proyecto
   - Caracteristicas
   - Arquitectura

---

## Tu Primer Dia con StudentsPoint

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
1. Edita codigo
2. Guarda
3. Refresca navegador (Ctrl+R)
4. Mira la ventana amarilla para ver logs
```

### Paso 4: Si Hay Error
```
1. Mira ventana amarilla (monitor)
2. O ejecuta: ver_logs.bat → opcion 2
3. Lee el error
4. Arregla
5. Guarda
6. Refresca
```

### Paso 5: Detener
```
1. Ctrl+C en ventana del servidor
2. Cierra ventana amarilla (o detener_monitor.bat)
3. Listo
```

---

## Preguntas Frecuentes

### Por que se abren 2 ventanas?
- Ventana 1 = Servidor (para ver requests)
- Ventana 2 = Monitor (para ver errores y estadisticas)

### Puedo cerrar la ventana amarilla?
- Si, pero no veras alertas en tiempo real
- Los logs se siguen guardando igual

### Donde se guardan los logs?
- `proyecto/src/backend/logs/`
- Se crean automaticamente

### Que pasa si borro la carpeta logs/?
- Se crea automaticamente al iniciar
- Los logs antiguos se pierden (pero hay backups)

### Funciona en produccion?
- Si! Usa `./iniciar_produccion.sh`
- Incluye Gunicorn + monitor + alertas

### Necesito configurar algo?
- **NO** para desarrollo
- **SI** para produccion (ver `env.production.example`)

---

## Tips Importantes

### Hacer
1. **Inicia con el script**: `iniciar_desarrollo.bat` (no manualmente)
2. **Deja el monitor abierto**: Te avisa de problemas
3. **Revisa logs regularmente**: `ver_logs.bat`
4. **Usa el indice**: `INDICE-MAESTRO.md` para encontrar docs

### No Hacer
1. No ignores la ventana amarilla del monitor
2. No cierres los logs sin revisar errores
3. No inicies el servidor con `python manage.py runserver` directamente
4. No borres la carpeta `logs/` (se limpia sola)

---

## Caracteristicas Principales

### Sistema de Foros Avanzado
- Foros personalizados por carrera
- Restriccion de publicacion: usuarios solo pueden postear en el foro de su carrera
- Libertad de comentarios: usuarios pueden comentar en cualquier foro
- Tipos de publicaciones: comentarios, encuestas, imagenes, otros
- Censura automatica de contenido ofensivo
- Revision manual de imagenes por administradores
- Foros publicos y privados
- Sistema de moderacion automatica y manual

### Autenticacion y Usuarios
- Registro con email y contrasena (verificacion por correo)
- Login seguro con JWT y hashing de contrasenas
- Google OAuth 2.0 como alternativa
- Recuperacion de contrasena por email
- Perfil personalizable (foto, datos academicos)
- Cambio de carrera cada semestre con historial
- Sistema de roles: admin, moderador, director de carrera, estudiante
- Multiples areas de estudio disponibles

### Sistema de Monitoreo
- **Logging completo**: 4 archivos de log separados (general, errors, api, auth)
- **Monitor en tiempo real**: Actualizacion automatica cada 30-60s
- **Sistema de alertas**: Deteccion automatica de problemas criticos
- **Analisis avanzado**: Reportes con estadisticas y recomendaciones
- **Optimizacion de queries**: Deteccion automatica de N+1
- **Performance monitoring**: Metricas de frontend en tiempo real

---

## Stack Tecnologico

### Backend
- **Django 5.2** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos (produccion)
- **SQLite** - Base de datos (desarrollo)
- **Redis** - Cache y broker de mensajes
- **Celery** - Tareas asincronas
- **JWT** - Autenticacion con tokens

### Frontend
- **HTML5, CSS3, JavaScript ES6+** - Tecnologias base
- **Bootstrap 5** - Framework CSS
- **PWA** - Service Worker para funcionalidad offline
- **Font Awesome** - Iconos

---

## Estado del Proyecto

- **Version Actual**: v2.1.0 (Release)
- **Fecha de Inicio**: Agosto 2025
- **Estado**: Sistema de Foros y Autenticacion Completos
- **Tests**: 71 pruebas automatizadas, 87% de cobertura
- **Documentacion**: Completa y organizada
- **Production-Ready**: Si

---

## Siguiente Paso

Lee [`INDICE-MAESTRO.md`](INDICE-MAESTRO.md) para ver toda la documentacion disponible.

O ve directo a [`INICIO-RAPIDO-LOGS.md`](INICIO-RAPIDO-LOGS.md) para detalles del sistema de logs.

---

**Estado:** Production-Ready  
**Automatizacion:** 100%  
**Documentacion:** Completa  
**Listo para:** Desarrollo y Produccion

---

**Bienvenido a StudentsPoint!**

Todo esta automatizado. Solo ejecuta el script de inicio y comienza a desarrollar.

No necesitas configurar nada mas. Los logs, el monitoreo y las alertas funcionan solos.

