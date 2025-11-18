@echo off
chcp 65001 >nul
title ngrok HTTPS - StudentsPoint
color 0E

cd /d "%~dp0\.."

echo ============================================================
echo    ngrok HTTPS para StudentsPoint
echo ============================================================
echo.
echo Este script solo inicia ngrok.
echo ASEGURATE de que Django este corriendo en puerto 8000
echo.

REM Verificar que ngrok este instalado
where ngrok >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ngrok no encontrado
    echo.
    echo Instala ngrok desde: https://ngrok.com/download
    echo.
    pause
    exit /b 1
)

echo Verificando que Django este corriendo en puerto 8000...
echo.

REM Verificar que Django responde
curl -s http://localhost:8000 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Django NO esta corriendo en puerto 8000
    echo.
    echo Primero inicia Django con:
    echo   iniciar_desarrollo.bat
    echo.
    echo O manualmente:
    echo   cd proyecto\src\backend
    echo   python manage.py runserver 0.0.0.0:8000
    echo.
    pause
    exit /b 1
)

echo [OK] Django esta corriendo
echo.
echo Iniciando ngrok...
echo.
echo INSTRUCCIONES:
echo   1. Copia el enlace HTTPS que aparecera
echo   2. Abrelo en tu celular
echo   3. Haz clic en "Visit Site" (pagina de aviso de ngrok)
echo   4. Instala la PWA: Menu (⋮) -> "Instalar app"
echo.
echo Presiona Ctrl+C para detener ngrok
echo.

timeout /t 3 /nobreak >nul

ngrok http 8000

echo.
echo ngrok detenido
echo.
pause

