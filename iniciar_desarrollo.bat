@echo off
chcp 65001 >nul
REM Script de inicio completo para StudentsPoint - Desarrollo
REM Ejecutar con doble click para iniciar todo el proyecto

title StudentsPoint - Desarrollo
color 0A

REM Cambiar al directorio del script
cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Modo Desarrollo
echo ============================================================
echo.
echo Este script instalara todo lo necesario y iniciara el servidor
echo.

REM ============================================================
REM FASE 1: VERIFICACION DE REQUISITOS
REM ============================================================

echo [1/10] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo Instala Python 3.11+ desde python.org
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado
echo.

REM ============================================================
REM FASE 2: NAVEGAR AL BACKEND
REM ============================================================

echo [2/10] Accediendo al directorio backend...
cd proyecto\src\backend
if errorlevel 1 (
    echo [ERROR] No se encontro el directorio backend
    echo Asegurate de estar en la raiz del proyecto
    pause
    exit /b 1
)
echo [OK] Directorio backend encontrado
echo.

REM ============================================================
REM FASE 3: INSTALAR DEPENDENCIAS
REM ============================================================

echo [3/10] Instalando dependencias de Python...
echo Esto puede tomar unos minutos la primera vez...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Algunas dependencias pueden no haberse instalado
    echo Intentando instalacion detallada...
    python -m pip install -r requirements.txt
)
echo [OK] Dependencias instaladas
echo.

REM ============================================================
REM FASE 4: VERIFICAR CONFIGURACION
REM ============================================================

echo [4/10] Verificando configuracion del proyecto...
python manage.py check --deploy 2>nul
if errorlevel 1 (
    echo [WARNING] Advertencias de configuracion detectadas
    python manage.py check
) else (
    echo [OK] Configuracion correcta
)
echo.

REM ============================================================
REM FASE 5: APLICAR MIGRACIONES
REM ============================================================

echo [5/10] Aplicando migraciones de base de datos...
python manage.py makemigrations 2>nul
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo [ERROR] Error aplicando migraciones
    echo.
    pause
    exit /b 1
)
echo [OK] Migraciones aplicadas correctamente
echo.

REM ============================================================
REM FASE 6: RECOLECTAR ARCHIVOS ESTATICOS
REM ============================================================

echo [6/10] Recolectando archivos estaticos (PWA)...
python manage.py collectstatic --noinput --clear >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Error al recolectar estaticos
    echo Intentando sin cache...
    python manage.py collectstatic --noinput
) else (
    echo [OK] Archivos estaticos actualizados (PWA lista)
)
echo.

REM ============================================================
REM FASE 7: CREAR SUPERUSUARIO
REM ============================================================

echo [7/10] Configurando superusuario...
if exist ensure_superuser.py (
    python ensure_superuser.py
    if errorlevel 1 (
        echo [WARNING] No se pudo crear superusuario automaticamente
    ) else (
        echo [OK] Superusuario configurado
    )
) else (
    echo [WARNING] Script ensure_superuser.py no encontrado
)
echo.

REM ============================================================
REM FASE 8: CREAR USUARIOS DE PRUEBA
REM ============================================================

echo [8/10] Creando usuarios de prueba...
python manage.py create_demo_users 2>nul
if errorlevel 1 (
    echo [WARNING] No se pudieron crear usuarios de prueba
) else (
    echo [OK] Usuarios de prueba creados
)
echo.

REM ============================================================
REM FASE 9: CONFIGURAR DIRECTORIOS
REM ============================================================

echo [9/10] Configurando directorios necesarios...
if not exist logs mkdir logs
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles
echo [OK] Directorios configurados
echo.

REM ============================================================
REM FASE 10: DETECTAR IPS
REM ============================================================

echo [10/10] Detectando direcciones IP...

REM IP Local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "192.168"') do (
    set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP:~1!
    goto :local_found
)
:local_found

REM IP Tailscale
set TAILSCALE_IP=
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "100."') do (
    set TAILSCALE_IP=%%a
    set TAILSCALE_IP=!TAILSCALE_IP:~1!
    goto :tailscale_found
)
:tailscale_found

echo [OK] IPs detectadas
echo.

REM ============================================================
REM SERVIDOR INICIADO
REM ============================================================

echo ============================================================
echo    SERVIDOR INICIADO - StudentsPoint v5.0.0
echo ============================================================
echo.
echo URLS DE ACCESO:
echo.
echo [LOCALHOST]
echo   App:       http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin/
echo   API Docs:  http://127.0.0.1:8000/api/docs/
echo.

if defined LOCAL_IP (
    echo [RED LOCAL]
    echo   App:       http://%LOCAL_IP%:8000
    echo   Admin:     http://%LOCAL_IP%:8000/admin/
    echo.
)

if defined TAILSCALE_IP (
    echo [TAILSCALE - PWA MOVIL]
    echo   App:       http://%TAILSCALE_IP%:8000
    echo   Admin:     http://%TAILSCALE_IP%:8000/admin/
    echo.
    echo Para instalar PWA en celular:
    echo   1. Conecta tu celular a Tailscale
    echo   2. Abre Chrome en el celular
    echo   3. Navega a http://%TAILSCALE_IP%:8000
    echo   4. Menu ^(tres puntos^) -^> Agregar a pantalla de inicio
    echo.
)

echo CREDENCIALES DE ACCESO:
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo SISTEMA DE LOGS:
echo   General:   logs/general.log
echo   Errores:   logs/errors.log
echo   API:       logs/api.log
echo   Auth:      logs/auth.log
echo.
echo ============================================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo Abriendo navegador en 3 segundos...
echo.

REM Abrir navegador
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000

echo ============================================================
echo SERVIDOR DJANGO INICIANDO...
echo ============================================================
echo.

REM Iniciar servidor en todas las interfaces para Tailscale
python manage.py runserver 0.0.0.0:8000

REM Si el servidor se detiene
echo.
echo ============================================================
echo SERVIDOR DETENIDO
echo ============================================================
echo.
echo El servidor Django se ha detenido.
echo.
pause
