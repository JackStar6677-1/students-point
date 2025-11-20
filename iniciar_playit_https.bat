@echo off
chcp 65001 >nul
title StudentsPoint - playit.gg con HTTPS
color 0D

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - playit.gg con HTTPS
echo ============================================================
echo.
echo Este script configura Django con HTTPS para usar con playit.gg
echo.

REM ============================================================
REM FASE 1: INSTALAR DJANGO-SSLSERVER
REM ============================================================

echo [1/6] Instalando django-sslserver...
cd proyecto\src\backend
pip install django-sslserver -q

if errorlevel 1 (
    echo [WARNING] Error instalando django-sslserver
    echo Intentando de nuevo...
    pip install django-sslserver
)

echo [OK] django-sslserver instalado
echo.

REM ============================================================
REM FASE 2: VERIFICAR CERTIFICADOS
REM ============================================================

echo [2/6] Verificando certificados SSL...

if not exist cert.pem (
    echo Generando certificados SSL...
    
    REM Verificar si OpenSSL esta disponible
    where openssl >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] OpenSSL no encontrado
        echo.
        echo OPCION 1: Instalar OpenSSL
        echo   winget install OpenSSL.Light
        echo   O descarga desde: https://slproweb.com/products/Win32OpenSSL.html
        echo.
        echo OPCION 2: Usar ngrok en su lugar
        echo   ngrok da HTTPS automaticamente sin necesidad de certificados
        echo   Ejecuta: iniciar_con_ngrok.bat
        echo.
        pause
        exit /b 1
    )
    
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=CL/ST=Santiago/L=Santiago/O=StudentsPoint/CN=best-wales.gl.at.ply.gg"
    
    if errorlevel 1 (
        echo [ERROR] No se pudo generar el certificado
        pause
        exit /b 1
    )
    
    echo [OK] Certificados generados
) else (
    echo [OK] Certificados ya existen
)
echo.

REM ============================================================
REM FASE 3: INSTALAR DEPENDENCIAS Y MIGRAR
REM ============================================================

echo [3/6] Instalando dependencias...
pip install -r requirements.txt -q
echo [OK] Dependencias instaladas
echo.

echo [4/6] Aplicando migraciones...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1
echo [OK] Base de datos lista
echo.

REM ============================================================
REM FASE 4: INICIAR DJANGO CON HTTPS
REM ============================================================

echo [5/6] Iniciando Django con HTTPS en puerto 8443...
echo.

REM Iniciar Django con HTTPS en ventana separada
start "Django HTTPS Server - NO CERRAR" cmd /k "python manage.py runsslserver 0.0.0.0:8443 --certificate cert.pem --key key.pem"

echo Esperando a que Django inicie...
timeout /t 10 /nobreak >nul

echo [OK] Django HTTPS iniciado
echo.

REM ============================================================
REM FASE 5: INICIAR PLAYIT.GG
REM ============================================================

echo [6/6] Verificando playit.gg...

cd ..\..\..

where playit >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] playit.gg no encontrado en PATH
    echo.
    echo El servidor Django HTTPS esta corriendo en puerto 8443
    echo.
    echo IMPORTANTE: Debes configurar tu tunel de playit.gg para el puerto 8443
    echo.
    echo Pasos:
    echo   1. Ve a https://playit.gg/account
    echo   2. Edita tu tunel "unnamed"
    echo   3. Cambia el puerto local de 8000 a 8443
    echo   4. Guarda los cambios
    echo   5. Ejecuta playit manualmente
    echo.
    echo O puedes usar ngrok que da HTTPS automaticamente:
    echo   iniciar_con_ngrok.bat
    echo.
    timeout /t 5 /nobreak
) else (
    echo [OK] playit.gg encontrado
    echo.
    echo IMPORTANTE: Asegurate de que tu tunel apunte al puerto 8443
    echo.
    echo Iniciando playit.gg...
    start "Playit.gg Tunnel - NO CERRAR" cmd /k "playit"
    echo.
)

REM ============================================================
REM INFORMACION DE ACCESO
REM ============================================================

echo.
echo ============================================================
echo    INFORMACION DE ACCESO - HTTPS
echo ============================================================
echo.
echo [ACCESO LOCAL CON HTTPS]
echo   App:       https://127.0.0.1:8443
echo   Admin:     https://127.0.0.1:8443/admin/
echo   API Docs:  https://127.0.0.1:8443/api/docs/
echo.
echo NOTA: El navegador mostrara advertencia de certificado
echo       Click en "Avanzado" -^> "Continuar" para acceder
echo.
echo [ACCESO PUBLICO - playit.gg]
echo   IMPORTANTE: Debes configurar el tunel para puerto 8443
echo.
echo   1. Ve a https://playit.gg/account
echo   2. Edita tu tunel "unnamed"
echo   3. Cambia "Local Port" de 8000 a 8443
echo   4. Guarda y reinicia playit
echo.
echo   Entonces podras acceder con:
echo   App:       https://best-wales.gl.at.ply.gg:16063
echo   Admin:     https://best-wales.gl.at.ply.gg:16063/admin/
echo.
echo [ALTERNATIVA MAS FACIL - ngrok]
echo   ngrok da HTTPS automaticamente sin configuracion:
echo   
echo   Ejecuta: iniciar_con_ngrok.bat
echo   
echo   ngrok detecta automaticamente HTTPS y no necesitas
echo   cambiar puertos ni generar certificados.
echo.
echo ============================================================
echo    CREDENCIALES DE ACCESO
echo ============================================================
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo ============================================================
echo.
echo PARA DETENER TODO:
echo   1. Cierra la ventana "Django HTTPS Server - NO CERRAR"
echo   2. Cierra la ventana "Playit.gg Tunnel - NO CERRAR"
echo.
echo Presiona cualquier tecla para finalizar este script...
echo.
pause >nul

echo.
echo RECUERDA:
echo   - Configura el tunel de playit.gg al puerto 8443
echo   - O usa ngrok para HTTPS automatico
echo.
pause

