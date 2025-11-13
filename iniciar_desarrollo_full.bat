@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ------------------------------------------------------------------
REM Script de bootstrap completo para StudentsPoint (modo desarrollo)
REM - Crea/activa entorno virtual en .venv
REM - Instala dependencias backend
REM - Copia .env de ejemplo si no existe
REM - Aplica migraciones y colecta estáticos
REM - Arranca Redis (si está instalado), Celery y Django en terminales separadas
REM ------------------------------------------------------------------

title StudentsPoint - Desarrollo Completo
color 0B

REM Ubicarse en la raíz del repositorio
cd /d "%~dp0"
set PROJECT_ROOT=%cd%
set BACKEND_DIR=%PROJECT_ROOT%\proyecto\src\backend
set VENV_DIR=%PROJECT_ROOT%\.venv

echo ============================================================
echo   StudentsPoint - Inicialización completa de desarrollo
echo ============================================================
echo/

REM 1. Verificar Python
echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.11+ no encontrado. Instala Python y vuelve a ejecutar.
    pause
    exit /b 1
)
for /f "delims=" %%P in ('python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"') do set PY_VERSION=%%P
echo [OK] Python !PY_VERSION!
echo/

REM 2. Crear/activar entorno virtual
echo [2/8] Preparando entorno virtual (.venv)...
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo    Creando nuevo entorno virtual...
    python -m venv "%VENV_DIR%"
)
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [ERROR] No se encontró el script de activación en %VENV_DIR%
    pause
    exit /b 1
)
call "%VENV_DIR%\Scripts\activate.bat"
echo [OK] Entorno virtual activo
echo/

REM 3. Actualizar pip e instalar dependencias backend
echo [3/8] Instalando dependencias del backend...
pushd "%BACKEND_DIR%"
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Se produjeron errores al instalar requirements.txt
    echo           Revisa la salida anterior por detalles.
)
popd
echo [OK] Dependencias backend listas
echo/

REM 4. Generar archivo .env si no existe
echo [4/8] Preparando archivo .env...
set ENV_FILE=%BACKEND_DIR%\.env
if not exist "%ENV_FILE%" (
    if exist "%PROJECT_ROOT%\proyecto\env.development.example" (
        copy "%PROJECT_ROOT%\proyecto\env.development.example" "%ENV_FILE%" >nul
        echo    Se copió env.development.example a src\backend\.env
        echo    Ajusta credenciales según tu entorno si es necesario.
    ) else (
        echo [WARNING] No se encontró env.development.example; crea %ENV_FILE% manualmente.
    )
) else (
    echo    Archivo .env existente respetado.
)
echo [OK] Configuración de entorno revisada
echo/

REM 5. Aplicar migraciones y recolectar estáticos
echo [5/8] Ejecutando migraciones y collectstatic...
pushd "%BACKEND_DIR%"
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Falló la ejecución de migraciones.
    popd
    pause
    exit /b 1
)
python manage.py collectstatic --noinput >nul
python ensure_superuser.py >nul
python manage.py create_demo_users >nul
popd
echo [OK] Base de datos y archivos estáticos actualizados
echo/

REM 6. Verificar/levantar Redis
echo [6/8] Verificando Redis...
where redis-server >nul 2>&1
if errorlevel 1 (
    echo [WARNING] redis-server no se encontró en PATH. Arranca Redis manualmente si es requerido.
) else (
    for /f "tokens=*" %%R in ('tasklist /FI "imagename eq redis-server.exe" ^| find /I "redis-server.exe"') do set REDIS_RUNNING=1
    if defined REDIS_RUNNING (
        echo    Redis ya se encuentra en ejecución.
    ) else (
        echo    Iniciando redis-server en nueva ventana...
        start "StudentsPoint - Redis" cmd /k "redis-server"
        timeout /t 3 >nul
    )
)
echo/

REM 7. Iniciar Celery worker (opcional pero recomendado)
echo [7/8] Iniciando Celery worker...
start "StudentsPoint - Celery" cmd /k ^
    "cd /d \"%BACKEND_DIR%\" && call \"%VENV_DIR%\Scripts\activate.bat\" && celery -A studentspoint worker -l info"
timeout /t 2 >nul
echo/

REM 8. Iniciar servidor Django
echo [8/8] Iniciando servidor Django...
start "StudentsPoint - Django" cmd /k ^
    "cd /d \"%BACKEND_DIR%\" && call \"%VENV_DIR%\Scripts\activate.bat\" && python manage.py runserver 127.0.0.1:8000"
timeout /t 2 >nul

echo ============================================================
echo   Servidor arrancando en http://127.0.0.1:8000
echo   Admin: http://127.0.0.1:8000/admin/
echo   API Docs: http://127.0.0.1:8000/api/docs/
echo ============================================================
echo/
echo Nota:
echo   - Redis y Celery se abrieron en ventanas separadas.
echo   - Presiona Ctrl+C en cada ventana para detener los procesos.
echo   - El entorno virtual .venv se reutilizará en ejecuciones futuras.
echo/

exit /b 0

