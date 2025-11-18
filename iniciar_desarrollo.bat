@echo off
REM Script de inicio automático para StudentsPoint - Desarrollo
REM Ejecutar con doble click para iniciar todo el proyecto

title StudentsPoint - Desarrollo
color 0A

REM Cambiar al directorio del script para rutas relativas
cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Modo Desarrollo
echo ============================================================
echo.
echo IMPORTANTE: Si esta ventana se cierra inesperadamente,
echo ejecuta este script desde una ventana de CMD para ver los errores.
echo.

REM Verificar Python
echo [1/8] Verificando Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python no encontrado. Instala Python 3.11+ desde python.org
    echo.
    echo Presiona cualquier tecla para salir...
    pause >nul
    exit /b 1
)
echo [OK] Python encontrado
echo.

REM Navegar al directorio backend
echo [2/8] Cambiando al directorio backend...
cd proyecto\src\backend
if errorlevel 1 (
    echo [ERROR] No se pudo acceder al directorio backend
    echo Asegurate de estar en la raiz del proyecto
    pause
    exit /b 1
)
echo [OK] Directorio backend encontrado
echo.

REM Instalar dependencias
echo [3/8] Instalando dependencias...
python -m pip install --no-cache-dir -r requirements.txt -q
if errorlevel 1 (
    echo [WARNING] Algunas dependencias pueden no haberse instalado correctamente
    echo Intentando instalacion sin cache...
    python -m pip install --no-cache-dir -r requirements.txt
)
echo [OK] Dependencias instaladas
echo.

REM Verificar configuración
echo [4/8] Verificando configuración...
python manage.py check
if errorlevel 1 (
    echo [WARNING] Hay advertencias en la configuración, continuando...
) else (
    echo [OK] Configuración correcta
)
echo.

REM Aplicar migraciones
echo [5/8] Aplicando migraciones...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo [ERROR] Error en migraciones. Revisa los mensajes anteriores.
    echo.
    echo Presiona cualquier tecla para salir...
    pause >nul
    exit /b 1
) else (
    echo [OK] Migraciones aplicadas
)
echo.

REM Recolectar archivos estáticos
echo [6/8] Recolectando archivos estáticos...
python manage.py collectstatic --noinput >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Error recolectando estáticos, continuando...
) else (
    echo [OK] Archivos estáticos actualizados
)
echo.

REM Crear superusuario
echo [7/8] Verificando superusuario...
python ensure_superuser.py
if errorlevel 1 (
    echo [WARNING] Error creando superusuario, continuando...
) else (
    echo [OK] Superusuario configurado
)
echo.

REM Crear usuarios de prueba
echo Creando usuarios de prueba...
python manage.py create_demo_users
if errorlevel 1 (
    echo [WARNING] Error creando usuarios de prueba, continuando...
) else (
    echo [OK] Usuarios de prueba listos
)
echo.

REM Crear directorio de logs si no existe
if not exist logs mkdir logs >nul 2>&1

REM Limpiar logs expirados (silenciosamente)
python -c "from pathlib import Path; ; logs_dir = Path('logs'); [os.remove(logs_dir / f) for f in os.listdir(logs_dir) if f.endswith('.log') and (logs_dir / f).stat().st_size > 50*1024*1024]" 2>nul

echo [8/8] Preparacion completada
echo.

REM Detectar IP de Tailscale
echo Detectando IP de Tailscale...
for /f "tokens=*" %%i in ('powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '100.*'} | Select-Object -ExpandProperty IPAddress -First 1"') do set TAILSCALE_IP=%%i

echo ============================================================
echo    SERVIDOR LISTO
echo ============================================================
echo.
echo URLs LOCALES:
echo   Aplicacion: http://127.0.0.1:8000
echo   Admin: http://127.0.0.1:8000/admin/
echo   API Docs: http://127.0.0.1:8000/api/docs/
echo.
if defined TAILSCALE_IP (
    echo URLs TAILSCALE (PWA):
    echo   Aplicacion: http://%TAILSCALE_IP%:8000
    echo   Admin: http://%TAILSCALE_IP%:8000/admin/
    echo   API Docs: http://%TAILSCALE_IP%:8000/api/docs/
    echo.
)
echo Credenciales: admin@studentspoint.app / admin123
echo.
echo [LOGS] Sistema de logging activo en: logs/
echo   - general.log: Todos los eventos
echo   - errors.log: Solo errores
echo   - api.log: Peticiones API
echo   - auth.log: Autenticacion
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Abrir navegador automáticamente después de 3 segundos
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000

echo Iniciando servidor Django...
echo Servidor accesible desde todas las interfaces (0.0.0.0:8000)
echo.

REM Intentar iniciar el servidor en 0.0.0.0 para acceso desde Tailscale
python manage.py runserver 0.0.0.0:8000
if errorlevel 1 (
    echo.
    echo [ERROR] El servidor no pudo iniciarse correctamente.
    echo Revisa los mensajes de error anteriores.
    echo.
    echo Presiona cualquier tecla para salir...
    pause >nul
    exit /b 1
)