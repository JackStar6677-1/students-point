@echo off
chcp 65001 >nul
title StudentsPoint - Launcher
color 0B

cd /d "%~dp0"

:MENU
cls
echo.
echo ============================================================
echo    StudentsPoint - Launcher Universal
echo ============================================================
echo.
echo Selecciona el modo de inicio:
echo.
echo  [1] Local - Solo en esta PC (127.0.0.1:8000)
echo.
echo  [2] Red Local - Acceso desde dispositivos en tu red WiFi
echo.
echo  [3] Tailscale - Red privada VPN (requiere Tailscale)
echo.
echo  [4] ngrok - Tunel HTTPS publico (recomendado para PWA)
echo.
echo  [5] Produccion - Modo produccion completo
echo.
echo  [6] Instalar Dependencias - Instalar todo automaticamente
echo.
echo  [0] Salir
echo.
echo ============================================================
echo.

set /p opcion="Elige una opcion [0-6]: "

if "%opcion%"=="1" goto LOCAL
if "%opcion%"=="2" goto RED_LOCAL
if "%opcion%"=="3" goto TAILSCALE
if "%opcion%"=="4" goto NGROK
if "%opcion%"=="5" goto PRODUCCION
if "%opcion%"=="6" goto INSTALAR_DEPS
if "%opcion%"=="0" exit /b 0

echo.
echo Opcion invalida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

REM ============================================================
REM OPCION 1: LOCAL
REM ============================================================
:LOCAL
cls
echo ============================================================
echo    Modo: LOCAL - Solo esta PC
echo ============================================================
echo.
echo Iniciando servidor Django en modo local...
echo.

cd proyecto\src\backend

echo [1/4] Instalando dependencias...
pip install -r requirements.txt -q 2>nul

echo [2/4] Migraciones...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1

echo [3/4] Configurando usuarios...
python ensure_superuser.py >nul 2>&1

echo [4/4] Iniciando servidor...
echo.
echo ============================================================
echo SERVIDOR INICIADO - MODO LOCAL
echo ============================================================
echo.
echo URLs de acceso:
echo   App:       http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin/
echo   API Docs:  http://127.0.0.1:8000/api/docs/
echo.
echo Credenciales:
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo Presiona Ctrl+C para detener
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

python manage.py runserver 127.0.0.1:8000

cd ..\..\..
pause
goto MENU

REM ============================================================
REM OPCION 2: RED LOCAL
REM ============================================================
:RED_LOCAL
cls
echo ============================================================
echo    Modo: RED LOCAL - WiFi
echo ============================================================
echo.
echo Iniciando servidor accesible desde tu red local...
echo.

cd proyecto\src\backend

echo [1/5] Instalando dependencias...
pip install -r requirements.txt -q 2>nul

echo [2/5] Migraciones...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1

echo [3/5] Configurando usuarios...
python ensure_superuser.py >nul 2>&1

echo [4/5] Detectando IP local...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "192.168"') do (
    set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP:~1!
    goto :ip_local_found
)
:ip_local_found

echo [5/5] Iniciando servidor...
echo.
echo ============================================================
echo SERVIDOR INICIADO - MODO RED LOCAL
echo ============================================================
echo.
echo URLs de acceso:
echo.
echo   [ESTA PC]
echo   App:       http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin/
echo.

if defined LOCAL_IP (
    echo   [OTROS DISPOSITIVOS EN TU RED WIFI]
    echo   App:       http://%LOCAL_IP%:8000
    echo   Admin:     http://%LOCAL_IP%:8000/admin/
    echo.
    echo   Conecta tu celular/tablet a la misma red WiFi
    echo   y abre esa URL en el navegador
    echo.
)

echo Credenciales:
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo Presiona Ctrl+C para detener
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

python manage.py runserver 0.0.0.0:8000

cd ..\..\..
pause
goto MENU

REM ============================================================
REM OPCION 3: TAILSCALE
REM ============================================================
:TAILSCALE
cls
echo ============================================================
echo    Modo: TAILSCALE - Red Privada VPN
echo ============================================================
echo.

REM Verificar Tailscale
tailscale status >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Tailscale no esta instalado o no esta corriendo
    echo.
    echo Instala Tailscale desde: https://tailscale.com/download
    echo.
    echo Despues de instalar, ejecuta:
    echo   tailscale up
    echo.
    pause
    goto MENU
)

echo [OK] Tailscale detectado
echo.

cd proyecto\src\backend

echo [1/5] Instalando dependencias...
pip install -r requirements.txt -q 2>nul

echo [2/5] Migraciones...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1

echo [3/5] Configurando usuarios...
python ensure_superuser.py >nul 2>&1

echo [4/5] Detectando IP de Tailscale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr "100."') do (
    set TAILSCALE_IP=%%a
    set TAILSCALE_IP=!TAILSCALE_IP:~1!
    goto :tailscale_found
)
:tailscale_found

echo [5/5] Iniciando servidor...
echo.
echo ============================================================
echo SERVIDOR INICIADO - MODO TAILSCALE
echo ============================================================
echo.
echo URLs de acceso:
echo.
echo   [LOCAL]
echo   App:       http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin/
echo.

if defined TAILSCALE_IP (
    echo   [TAILSCALE VPN - Desde cualquier dispositivo con Tailscale]
    echo   App:       http://%TAILSCALE_IP%:8000
    echo   Admin:     http://%TAILSCALE_IP%:8000/admin/
    echo.
    echo   IMPORTANTE:
    echo   - El dispositivo debe tener Tailscale instalado y conectado
    echo   - Usa esta IP en tu celular para instalar la PWA
    echo   - La conexion es privada y segura (VPN)
    echo.
) else (
    echo [WARNING] No se detecto IP de Tailscale
)

echo Credenciales:
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo Presiona Ctrl+C para detener
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

python manage.py runserver 0.0.0.0:8000

cd ..\..\..
pause
goto MENU

REM ============================================================
REM OPCION 4: NGROK
REM ============================================================
:NGROK
cls
echo ============================================================
echo    Modo: NGROK - Tunel HTTPS Publico
echo ============================================================
echo.

REM Verificar ngrok
where ngrok >nul 2>&1
if errorlevel 1 (
    echo [INFO] ngrok no esta instalado
    echo.
    set /p instalar_ngrok="Deseas instalar ngrok automaticamente? [S/N]: "
    if /i "!instalar_ngrok!"=="S" (
        echo.
        echo Instalando ngrok con winget...
        winget install ngrok.ngrok --accept-package-agreements --accept-source-agreements
        
        if errorlevel 1 (
            echo.
            echo [ERROR] No se pudo instalar automaticamente
            echo.
            echo Instala manualmente:
            echo   1. Descarga desde: https://ngrok.com/download
            echo   2. Descomprime y agrega al PATH
            echo   3. Ejecuta: ngrok authtoken TU_TOKEN
            echo.
            pause
            goto MENU
        )
        
        echo.
        echo [OK] ngrok instalado
        echo.
        echo IMPORTANTE: Necesitas configurar tu authtoken
        echo.
        set /p authtoken="Pega tu ngrok authtoken (desde https://dashboard.ngrok.com/): "
        ngrok authtoken !authtoken!
    ) else (
        goto MENU
    )
)

echo [OK] ngrok encontrado
echo.

cd proyecto\src\backend

echo [1/4] Instalando dependencias...
pip install -r requirements.txt -q 2>nul

echo [2/4] Migraciones...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1

echo [3/4] Iniciando Django...
start "Django Server - NO CERRAR" cmd /k "python manage.py runserver 0.0.0.0:8000"

echo [4/4] Esperando Django...
timeout /t 10 /nobreak >nul

cd ..\..\..

echo.
echo ============================================================
echo SERVIDOR DJANGO INICIADO
echo ============================================================
echo.
echo [OK] Django corriendo en http://127.0.0.1:8000
echo.
echo Ahora iniciando ngrok...
echo.
echo IMPORTANTE:
echo   - ngrok te dara un enlace HTTPS publico
echo   - Usa ese enlace en tu celular para instalar la PWA
echo   - El enlace cambia cada vez que reinicias ngrok
echo.
echo Para detener:
echo   - Presiona Ctrl+C en esta ventana para detener ngrok
echo   - Cierra la ventana "Django Server - NO CERRAR"
echo.
timeout /t 3 /nobreak >nul

ngrok http 8000

echo.
echo ngrok detenido
echo.
echo RECUERDA: Cierra manualmente la ventana "Django Server - NO CERRAR"
echo.
pause
goto MENU

REM ============================================================
REM OPCION 5: PRODUCCION
REM ============================================================
:PRODUCCION
cls
echo ============================================================
echo    Modo: PRODUCCION
echo ============================================================
echo.
echo Iniciando en modo produccion...
echo.

if exist scripts\iniciar_produccion.bat (
    call scripts\iniciar_produccion.bat
) else (
    echo [ERROR] Script de produccion no encontrado
    pause
)
goto MENU

REM ============================================================
REM OPCION 6: INSTALAR DEPENDENCIAS
REM ============================================================
:INSTALAR_DEPS
cls
echo ============================================================
echo    Instalacion Automatica de Dependencias
echo ============================================================
echo.
echo Este proceso instalara todo lo necesario para StudentsPoint
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo.
    echo Instala Python 3.11+ desde:
    echo   https://www.python.org/downloads/
    echo   O ejecuta: winget install Python.Python.3.11
    echo.
    pause
    goto MENU
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo.
    echo Instala Python 3.11+ desde:
    echo   https://www.python.org/downloads/
    echo   O ejecuta: winget install Python.Python.3.11
    echo.
    pause
    goto MENU
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado
echo.

REM Instalar pip packages
echo [2/10] Actualizando pip...
python -m pip install --upgrade pip --quiet

echo [3/10] Instalando dependencias de Python...
cd proyecto\src\backend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [WARNING] Algunas dependencias fallaron, reintentando...
    pip install -r requirements.txt
)
cd ..\..\..

echo [4/10] Instalando django-sslserver (para HTTPS)...
pip install django-sslserver --quiet 2>nul

REM Verificar/Instalar ngrok
echo [5/10] Verificando ngrok...
where ngrok >nul 2>&1
if errorlevel 1 (
    echo [INFO] ngrok no encontrado. Instalando...
    winget install ngrok.ngrok --accept-package-agreements --accept-source-agreements --silent
    if errorlevel 1 (
        echo [WARNING] No se pudo instalar ngrok automaticamente
        echo Descarga manual: https://ngrok.com/download
    ) else (
        echo [OK] ngrok instalado
        echo.
        echo IMPORTANTE: Configura tu authtoken de ngrok
        echo   1. Registrate en: https://dashboard.ngrok.com/signup
        echo   2. Copia tu authtoken
        echo   3. Ejecuta: ngrok authtoken TU_TOKEN
        echo.
    )
) else (
    echo [OK] ngrok ya esta instalado
)

REM Verificar OpenSSL
echo [6/10] Verificando OpenSSL...
where openssl >nul 2>&1
if errorlevel 1 (
    echo [INFO] OpenSSL no encontrado. Instalando...
    winget install ShiningLight.OpenSSL.Light --accept-package-agreements --accept-source-agreements --silent
    if errorlevel 1 (
        echo [WARNING] No se pudo instalar OpenSSL automaticamente
        echo.
        echo Opciones de instalacion manual:
        echo   1. winget install ShiningLight.OpenSSL.Light
        echo   2. Descarga desde: https://slproweb.com/products/Win32OpenSSL.html
        echo.
    ) else (
        echo [OK] OpenSSL instalado
        echo.
        echo IMPORTANTE: Reinicia la terminal para que OpenSSL este en el PATH
        echo.
    )
) else (
    echo [OK] OpenSSL ya esta instalado
)

REM Verificar Tailscale
echo [7/10] Verificando Tailscale...
where tailscale >nul 2>&1
if errorlevel 1 (
    echo [INFO] Tailscale no encontrado
    echo Para instalar Tailscale:
    echo   Descarga desde: https://tailscale.com/download/windows
    echo   Es opcional, solo si quieres usar VPN privada
) else (
    echo [OK] Tailscale ya esta instalado
)

REM Verificar playit.gg
echo [8/10] Verificando playit.gg...
where playit >nul 2>&1
if errorlevel 1 (
    echo [INFO] playit.gg no encontrado
    echo Para instalar playit.gg:
    echo   Descarga desde: https://playit.gg/download
    echo   Es opcional, solo si quieres tunel publico permanente
) else (
    echo [OK] playit.gg ya esta instalado
)

REM Migraciones
echo [9/10] Ejecutando migraciones de base de datos...
cd proyecto\src\backend
python manage.py makemigrations >nul 2>&1
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput --clear >nul 2>&1

REM Superusuario
echo [10/10] Creando superusuario...
python ensure_superuser.py >nul 2>&1

cd ..\..\..

echo.
echo ============================================================
echo    INSTALACION COMPLETADA
echo ============================================================
echo.
echo Herramientas instaladas:
echo   [OK] Python y dependencias
echo   [OK] Django y apps
echo   [OK] Base de datos configurada
echo   [OK] Archivos estaticos recolectados
echo   [OK] Superusuario creado
echo.

where ngrok >nul 2>&1
if not errorlevel 1 echo   [OK] ngrok

where openssl >nul 2>&1
if not errorlevel 1 echo   [OK] OpenSSL

where tailscale >nul 2>&1
if not errorlevel 1 echo   [OK] Tailscale

where playit >nul 2>&1
if not errorlevel 1 echo   [OK] playit.gg

echo.
echo Credenciales creadas:
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo Ya puedes iniciar StudentsPoint desde el menu principal
echo.
pause
goto MENU

