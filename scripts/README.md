# Scripts de Utilidades - StudentsPoint

Esta carpeta contiene scripts de utilidades para el mantenimiento, despliegue y monitoreo del proyecto StudentsPoint.

## Scripts de Inicio

### Desarrollo

#### `iniciar_desarrollo.bat` (Windows)
Script rapido para iniciar el proyecto en modo desarrollo.

**Funciones**:
- Verifica Python y dependencias
- Aplica migraciones automaticamente
- Recolecta archivos estaticos
- Crea superusuario si no existe
- Inicia Django en 0.0.0.0:8000
- Detecta IPs (local y Tailscale)

**Uso**:
```batch
scripts\iniciar_desarrollo.bat
```

#### `iniciar_desarrollo.sh` (Linux/Mac)
Script rapido para iniciar el proyecto en modo desarrollo.

**Funciones**:
- Configuracion automatica de entorno
- Instalacion de dependencias
- Migraciones y estaticos
- Inicia Django en 0.0.0.0:8000

**Uso**:
```bash
chmod +x scripts/iniciar_desarrollo.sh
./scripts/iniciar_desarrollo.sh
```

#### `iniciar_simple.bat` (Windows)
Version minimalista del script de inicio sin detecciones extras.

**Funciones**:
- Instalacion basica de dependencias
- Migraciones minimas
- Inicio rapido en 0.0.0.0:8000

**Uso**:
```batch
scripts\iniciar_simple.bat
```

### Tuneles Publicos

#### `iniciar_con_ngrok.bat` (Windows)
Inicia Django y ngrok para obtener un tunel HTTPS publico.

**Funciones**:
- Inicia Django en ventana separada
- Inicia ngrok automaticamente
- Da URL HTTPS publica
- Perfecto para PWA en celular

**Uso**:
```batch
scripts\iniciar_con_ngrok.bat
```

**Requisitos**:
- ngrok instalado: https://ngrok.com/download
- Authtoken configurado: `ngrok authtoken TU_TOKEN`

**Documentacion**: Ver `docs/guias/USAR-NGROK.md`

#### `iniciar_solo_ngrok.bat` (Windows)
Solo inicia ngrok (asume que Django ya esta corriendo).

**Funciones**:
- Verifica que Django este en puerto 8000
- Inicia solo el tunel ngrok
- Util si Django ya esta corriendo

**Uso**:
```batch
scripts\iniciar_solo_ngrok.bat
```

#### `iniciar_playit_https.bat` (Windows)
Inicia Django con HTTPS usando playit.gg como tunel publico.

**Funciones**:
- Instala django-sslserver
- Genera certificados SSL self-signed
- Inicia Django en puerto 8443 con HTTPS
- Inicia agente de playit.gg
- Tunel publico con dominio permanente

**Uso**:
```batch
scripts\iniciar_playit_https.bat
```

**Requisitos**:
- playit.gg instalado: https://playit.gg/download
- OpenSSL instalado (el script puede instalarlo)
- Tunel configurado para puerto 8443

**Documentacion**: Ver `docs/guias/USAR-PLAYIT.md`

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

## Scripts de PWA

### `instalar_pwa.bat` / `instalar_pwa.sh`
Instala y configura los archivos PWA del proyecto.

**Funciones**:
- Copia archivos PWA al directorio estatico
- Configura manifest.json
- Verifica service worker
- Recolecta archivos estaticos

**Uso Windows**:
```batch
scripts\instalar_pwa.bat
```

**Uso Linux/Mac**:
```bash
chmod +x scripts/instalar_pwa.sh
./scripts/instalar_pwa.sh
```

### `verificar_pwa.bat`
Verifica que la PWA este correctamente configurada.

**Funciones**:
- Verifica manifest.json
- Verifica service worker
- Verifica iconos
- Muestra reporte de estado

**Uso**:
```batch
scripts\verificar_pwa.bat
```

### `regenerar_iconos_pwa.bat`
Regenera todos los iconos de la PWA con el logo de StudentsPoint.

**Funciones**:
- Genera iconos de multiples tamaños
- Actualiza manifest.json
- Crea favicon.svg

**Requisitos**:
- ImageMagick o Pillow (Python)

**Uso**:
```batch
scripts\regenerar_iconos_pwa.bat
```

## Scripts de Configuracion

### `configurar_https.bat`
Configura HTTPS local con certificados self-signed.

**Funciones**:
- Instala django-sslserver
- Genera certificados SSL con OpenSSL
- Detecta IP de Tailscale
- Crea script de inicio HTTPS

**Uso**:
```batch
scripts\configurar_https.bat
```

**Requisitos**:
- OpenSSL instalado

## Scripts de Diagnostico

### `diagnostico.bat`
Ejecuta un diagnostico completo del sistema.

**Funciones**:
- Verifica Python y dependencias
- Verifica base de datos
- Verifica archivos estaticos
- Verifica configuraciones
- Muestra reporte detallado

**Uso**:
```batch
scripts\diagnostico.bat
```

### `aplicar_correcciones_movil.bat`
Aplica correcciones de diseño responsive para dispositivos moviles.

**Funciones**:
- Actualiza CSS responsive
- Corrige problemas de viewport
- Optimiza para diferentes tamaños de pantalla
- Recolecta estaticos

**Uso**:
```batch
scripts\aplicar_correcciones_movil.bat
```

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

1. **Launcher Universal**: En la raiz del proyecto hay un script maestro `iniciar_studentspoint.bat` que permite elegir entre todas las opciones de inicio con un menu interactivo. Ver `docs/guias/LAUNCHER.md`.

2. **Variables de Entorno**: Asegurate de configurar correctamente las variables de entorno en los archivos `.env` antes de ejecutar scripts de produccion.

3. **PostgreSQL**: Para produccion, se recomienda usar PostgreSQL. El script `instalar_postgresql.bat` facilita la instalacion en Windows.

4. **Logs**: Todos los logs se guardan en `proyecto/src/backend/logs/`.

5. **Gunicorn**: Solo disponible en Linux/Mac. Windows usa el servidor de desarrollo de Django.

6. **Tuneles Publicos**: Para acceso desde internet usa ngrok (HTTPS automatico) o playit.gg (dominio permanente). Ver documentacion en `docs/guias/`.

7. **PWA**: Para probar PWA en celular se recomienda usar ngrok que da HTTPS automaticamente sin advertencias de seguridad.

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

