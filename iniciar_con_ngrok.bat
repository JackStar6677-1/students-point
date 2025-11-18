@echo off
chcp 65001 >nul
title StudentsPoint - ngrok HTTPS
color 0D

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Servidor con ngrok (HTTPS)
echo ============================================================
echo.
echo Este script iniciara el servidor Django y ngrok para
echo obtener un enlace HTTPS publico para probar la PWA.
echo.

REM Verificar que ngrok este instalado
where ngrok >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ngrok no encontrado
    echo.
    echo Asegurate de que ngrok este instalado y en el PATH
    echo Descarga: https://ngrok.com/download
    echo.
    pause
    exit /b 1
)

echo [OK] ngrok encontrado
echo.

echo [1/4] Navegando al backend...
cd proyecto\src\backend

if errorlevel 1 (
    echo [ERROR] No se encontro el directorio backend
    pause
    exit /b 1
)

echo [OK] Directorio backend encontrado
echo.

echo [2/4] Instalando dependencias...
pip install -r requirements.txt -q
echo [OK] Dependencias instaladas
echo.

echo [3/4] Aplicando migraciones y recolectando estaticos...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1
echo [OK] Base de datos y estaticos listos
echo.

echo [4/4] Iniciando servidor Django en puerto 8000...
echo.

REM Iniciar Django en segundo plano
start /B "Django Server" python manage.py runserver 0.0.0.0:8000

REM Esperar a que Django inicie
timeout /t 5 /nobreak >nul

echo ============================================================
echo    Servidor Django Iniciado
echo ============================================================
echo.
echo Servidor local: http://127.0.0.1:8000
echo.
echo Ahora iniciando ngrok...
echo.
echo IMPORTANTE:
echo   1. ngrok te dara un enlace HTTPS (ej: https://abc123.ngrok.io)
echo   2. Usa ese enlace en tu celular para probar la PWA
echo   3. La PWA se instalara correctamente con HTTPS
echo   4. El enlace cambia cada vez que reinicias ngrok
echo.
echo Presiona Ctrl+C para detener ngrok y el servidor
echo.

timeout /t 3 /nobreak >nul

REM Iniciar ngrok
cd ..\..\..
ngrok http 8000

REM Si ngrok se cierra, matar el servidor Django
taskkill /F /FI "WINDOWTITLE eq Django Server*" >nul 2>&1

echo.
echo Servidor y ngrok detenidos
echo.
pause

