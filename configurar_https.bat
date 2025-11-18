@echo off
chcp 65001 >nul
title StudentsPoint - Configurar HTTPS
color 0E

echo ============================================================
echo    StudentsPoint - Configuracion HTTPS para PWA Android
echo ============================================================
echo.
echo Este script configurara HTTPS para que la PWA funcione
echo correctamente en Android.
echo.
echo IMPORTANTE: Necesitas OpenSSL instalado
echo.

cd /d "%~dp0"

REM Verificar OpenSSL
where openssl >nul 2>&1
if errorlevel 1 (
    echo [ERROR] OpenSSL no encontrado
    echo.
    echo Descarga e instala OpenSSL desde:
    echo   Windows: https://slproweb.com/products/Win32OpenSSL.html
    echo   O usa: winget install OpenSSL.Light
    echo.
    pause
    exit /b 1
)

echo [OK] OpenSSL encontrado
echo.

REM Detectar IP de Tailscale
echo Detectando IP de Tailscale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "100."') do (
    set TAILSCALE_IP=%%a
    set TAILSCALE_IP=!TAILSCALE_IP:~1!
    goto :ip_found
)

echo [WARNING] No se detectó IP de Tailscale
set /p TAILSCALE_IP="Ingresa tu IP de Tailscale (100.x.x.x): "

:ip_found

echo [OK] IP Tailscale: %TAILSCALE_IP%
echo.

REM Navegar al backend
cd proyecto\src\backend
if errorlevel 1 (
    echo [ERROR] No se encontro el directorio backend
    pause
    exit /b 1
)

echo [1/4] Generando certificado SSL...
echo.

REM Generar certificado
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=CL/ST=Santiago/L=Santiago/O=StudentsPoint/CN=%TAILSCALE_IP%"

if errorlevel 1 (
    echo [ERROR] No se pudo generar el certificado
    pause
    exit /b 1
)

echo [OK] Certificado generado
echo.

echo [2/4] Instalando django-sslserver...
pip install django-sslserver -q

if errorlevel 1 (
    echo [WARNING] Error instalando django-sslserver
)

echo [OK] django-sslserver instalado
echo.

echo [3/4] Actualizando configuracion...

REM Agregar sslserver a INSTALLED_APPS si no existe
findstr /C:"sslserver" studentspoint\settings\dev.py >nul
if errorlevel 1 (
    echo Agregando sslserver a INSTALLED_APPS...
    REM Esto requeriría edición manual o un script más complejo
    echo [WARNING] Debes agregar 'sslserver' a INSTALLED_APPS manualmente
)

echo.

echo [4/4] Creando script de inicio HTTPS...

cd ..\..\..

REM Crear script de inicio HTTPS
(
echo @echo off
echo chcp 65001 ^>nul
echo title StudentsPoint - HTTPS
echo color 0A
echo.
echo cd /d "%%~dp0proyecto\src\backend"
echo.
echo echo ============================================================
echo echo    StudentsPoint - Servidor HTTPS
echo echo ============================================================
echo echo.
echo echo URLs:
echo echo   HTTPS: https://%TAILSCALE_IP%:8443
echo echo   Admin: https://%TAILSCALE_IP%:8443/admin/
echo echo.
echo echo PRIMERA VEZ en el celular:
echo echo   1. Navega a https://%TAILSCALE_IP%:8443
echo echo   2. Acepta el certificado ^(Avanzado -^> Continuar^)
echo echo   3. Instala la PWA normalmente
echo echo.
echo echo Credenciales: admin@studentspoint.app / admin123
echo echo.
echo.
echo python manage.py migrate --run-syncdb ^>nul 2^>^&1
echo python manage.py collectstatic --noinput ^>nul 2^>^&1
echo.
echo timeout /t 2 /nobreak ^>nul
echo.
echo python manage.py runsslserver 0.0.0.0:8443 --certificate cert.pem --key key.pem
echo.
echo pause
) > iniciar_https.bat

echo [OK] Script creado: iniciar_https.bat
echo.

echo ============================================================
echo    CONFIGURACION COMPLETADA
echo ============================================================
echo.
echo Archivos creados:
echo   - proyecto\src\backend\cert.pem
echo   - proyecto\src\backend\key.pem
echo   - iniciar_https.bat
echo.
echo IMPORTANTE:
echo   1. Agrega 'sslserver' a INSTALLED_APPS en dev.py
echo   2. Ejecuta: iniciar_https.bat
echo   3. En el celular, navega a: https://%TAILSCALE_IP%:8443
echo   4. Acepta el certificado self-signed
echo   5. Instala la PWA
echo.
echo Documentacion completa:
echo   docs\guias\PWA-ANDROID-HTTPS.md
echo.
pause

