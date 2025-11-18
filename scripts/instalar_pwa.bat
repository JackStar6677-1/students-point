@echo off
chcp 65001 >nul
title StudentsPoint - Instalación PWA

echo ============================================
echo   StudentsPoint - Instalación PWA v1.2.3
echo ============================================
echo.

echo [1/5] Activando entorno virtual...
cd /d "%~dp0..\proyecto\src\backend"
call ..\..\..\..\venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegurate de tener el venv creado en la raiz del proyecto
    pause
    exit /b 1
)
echo OK - Entorno virtual activado
echo.

echo [2/5] Configurando variables de entorno...
set DJANGO_SETTINGS_MODULE=studentspoint.settings.dev
set PYTHONPATH=%~dp0..\proyecto\src\backend
echo OK - Variables configuradas
echo.

echo [3/5] Ejecutando collectstatic...
python manage.py collectstatic --noinput --clear
if errorlevel 1 (
    echo ERROR: Falló collectstatic
    pause
    exit /b 1
)
echo OK - Archivos estáticos recolectados
echo.

echo [4/5] Verificando archivos PWA críticos...

set STATICFILES_DIR=%~dp0..\proyecto\src\backend\staticfiles

if not exist "%STATICFILES_DIR%\sw.js" (
    echo ERROR: No se encontró sw.js en staticfiles
    pause
    exit /b 1
)
echo OK - sw.js encontrado

if not exist "%STATICFILES_DIR%\manifest.json" (
    echo ERROR: No se encontró manifest.json en staticfiles
    pause
    exit /b 1
)
echo OK - manifest.json encontrado

if not exist "%STATICFILES_DIR%\pwa-config.js" (
    echo ERROR: No se encontró pwa-config.js en staticfiles
    pause
    exit /b 1
)
echo OK - pwa-config.js encontrado

if not exist "%STATICFILES_DIR%\js\pwa.js" (
    echo ERROR: No se encontró js/pwa.js en staticfiles
    pause
    exit /b 1
)
echo OK - pwa.js encontrado

echo.
echo [5/5] Verificando iconos PWA...

set ICONS_DIR=%STATICFILES_DIR%\images\icons

for %%i in (72 96 128 144 152 192 384 512) do (
    if not exist "%ICONS_DIR%\icon-%%ix%%i.png" (
        echo ADVERTENCIA: No se encontró icon-%%ix%%i.png
    ) else (
        echo OK - icon-%%ix%%i.png
    )
)

echo.
echo ============================================
echo   Instalación PWA Completada
echo ============================================
echo.
echo La PWA está lista para usarse.
echo.
echo Para acceder:
echo   - Localhost: http://localhost:8000
echo   - Tailscale Laptop: http://100.75.238.19:8000
echo   - Tailscale Desktop: http://100.113.204.115:8000
echo.
echo Una vez en la página, busca el botón "Instalar App"
echo o el icono de instalación en la barra de direcciones.
echo.
echo Consulta docs\guias\INSTALACION-PWA.md para más información.
echo.
pause

