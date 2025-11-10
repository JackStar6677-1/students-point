# Scripts de Utilidades - StudentsPoint

Esta carpeta contiene scripts de utilidades para el mantenimiento, despliegue y monitoreo del proyecto StudentsPoint.

## Scripts de Inicio

### Producción

#### `iniciar_produccion.bat` (Windows)
Script para iniciar el proyecto en modo producción en Windows.

**Funciones**:
- Verifica Python y dependencias
- Configura variables de entorno de producción
- Aplica migraciones
- Recolecta archivos estáticos
- Inicia el servidor (Django o Gunicorn)

**Uso**:
```batch
cd ruta\al\proyecto
scripts\iniciar_produccion.bat
```

#### `iniciar_produccion.sh` (Linux/Mac)
Script para iniciar el proyecto en modo producción en Linux/Mac.

**Funciones**:
- Configuración automática de entorno
- Opción de actualización desde Git
- Inicio con Gunicorn (recomendado)
- Monitor de logs integrado
- Sistema de alertas en segundo plano

**Uso**:
```bash
chmod +x scripts/iniciar_produccion.sh
./scripts/iniciar_produccion.sh
```

**Opciones disponibles**:
1. Gunicorn (Producción - recomendado)
2. Django runserver (Solo desarrollo)
3. Con monitor de logs en consola

## Scripts de Monitoreo

### `ver_logs.bat` / `ver_logs.sh`
Scripts para visualizar logs del sistema en tiempo real.

**Funciones**:
- Muestra logs de aplicación
- Filtra por tipo (general, errores, api, auth)
- Actualización en tiempo real

**Uso Windows**:
```batch
scripts\ver_logs.bat
```

**Uso Linux/Mac**:
```bash
chmod +x scripts/ver_logs.sh
./scripts/ver_logs.sh
```

### `ver_logs_tests.bat` / `ver_logs_tests.sh`
Scripts para visualizar logs de pruebas y tests.

**Funciones**:
- Muestra resultados de tests
- Logs de pruebas unitarias
- Reportes de cobertura

**Uso Windows**:
```batch
scripts\ver_logs_tests.bat
```

**Uso Linux/Mac**:
```bash
chmod +x scripts/ver_logs_tests.sh
./scripts/ver_logs_tests.sh
```

## Scripts de Despliegue

### `deploy_linux.sh`
Script completo de despliegue para servidores Linux.

**Funciones**:
- Configuración de servidor Linux
- Instalación de dependencias del sistema
- Configuración de Nginx
- Configuración de Gunicorn
- Setup de servicios systemd
- Configuración de SSL/HTTPS (opcional)

**Uso**:
```bash
chmod +x scripts/deploy_linux.sh
sudo ./scripts/deploy_linux.sh
```

**Requisitos**:
- Ubuntu 20.04+ o Debian 11+
- Permisos de root o sudo
- Conexión a internet

## Scripts de Instalación

### `instalar_postgresql.bat`
Instalador automatizado de PostgreSQL para Windows.

**Funciones**:
- Descarga PostgreSQL (si no está instalado)
- Configura usuario y contraseña por defecto
- Crea base de datos del proyecto
- Configura variables de entorno

**Uso**:
```batch
scripts\instalar_postgresql.bat
```

**Credenciales por defecto**:
- Usuario: `postgres`
- Contraseña: `214526867` (configurable en el script)
- Base de datos: `studentspoint_db`

## Scripts de Control

### `detener_servicios.sh` (Linux/Mac)
Detiene todos los servicios de StudentsPoint.

**Funciones**:
- Detiene Gunicorn
- Detiene monitor de logs
- Detiene sistema de alertas
- Limpia procesos huérfanos

**Uso**:
```bash
chmod +x scripts/detener_servicios.sh
./scripts/detener_servicios.sh
```

### `detener_monitor.bat` (Windows)
Detiene el monitor de logs en Windows.

**Funciones**:
- Detiene procesos de monitoreo
- Limpia recursos

**Uso**:
```batch
scripts\detener_monitor.bat
```

## Permisos en Linux/Mac

Después de clonar el repositorio, dar permisos de ejecución a los scripts:

```bash
chmod +x scripts/*.sh
```

## Notas Importantes

1. **Scripts de Desarrollo**: Los scripts `iniciar_desarrollo.bat` y `iniciar_desarrollo.sh` están en la raíz del proyecto, no en esta carpeta.

2. **Variables de Entorno**: Asegúrate de configurar correctamente las variables de entorno en los archivos `.env` antes de ejecutar scripts de producción.

3. **PostgreSQL**: Para producción, se recomienda usar PostgreSQL. El script `instalar_postgresql.bat` facilita la instalación en Windows.

4. **Logs**: Todos los logs se guardan en `proyecto/src/backend/logs/`.

5. **Gunicorn**: Solo disponible en Linux/Mac. Windows usa el servidor de desarrollo de Django.

## Troubleshooting

### Error: "Permission denied"
**Solución Linux/Mac**:
```bash
chmod +x scripts/nombre_script.sh
```

### Error: "Python no encontrado"
**Solución**:
- Instala Python 3.11+ desde [python.org](https://www.python.org)
- Asegúrate de que Python esté en el PATH del sistema

### Error de conexión a PostgreSQL
**Solución**:
1. Verifica que PostgreSQL esté ejecutándose
2. Revisa las credenciales en el archivo `.env`
3. Confirma que el puerto 5432 esté disponible

### Scripts no funcionan en Windows
**Solución**:
- Ejecuta los scripts `.bat` desde PowerShell o CMD
- No uses Git Bash para scripts `.bat`
- Verifica que tienes permisos de administrador si es necesario

## Soporte

Para más información, consulta:
- [`docs/GUIA-COMPLETA.md`](../docs/GUIA-COMPLETA.md) - Guía completa del proyecto
- [`docs/guias/DEPLOYMENT-PRODUCTION.md`](../docs/guias/DEPLOYMENT-PRODUCTION.md) - Despliegue en producción
- [`docs/guias/SISTEMA-LOGGING.md`](../docs/guias/SISTEMA-LOGGING.md) - Sistema de logs

---

**StudentsPoint Team** - Noviembre 2025

