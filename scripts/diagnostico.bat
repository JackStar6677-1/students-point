@echo off
REM Script de diagnóstico para StudentsPoint
REM Ejecuta este script para verificar la configuración del proyecto

title StudentsPoint - Diagnostico
color 0E

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Diagnostico del Sistema
echo ============================================================
echo.

echo [1] Verificando Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo.
) else (
    echo [OK] Python instalado
    echo.
)

echo [2] Verificando pip...
python -m pip --version
if errorlevel 1 (
    echo [ERROR] pip no encontrado
    echo.
) else (
    echo [OK] pip disponible
    echo.
)

echo [3] Verificando directorio del proyecto...
if exist "proyecto\src\backend\manage.py" (
    echo [OK] Directorio backend encontrado
    echo.
) else (
    echo [ERROR] No se encuentra manage.py en proyecto\src\backend\
    echo Asegurate de estar en la raiz del proyecto
    echo.
)

echo [4] Verificando archivo requirements.txt...
if exist "proyecto\src\backend\requirements.txt" (
    echo [OK] requirements.txt encontrado
    echo.
) else (
    echo [ERROR] No se encuentra requirements.txt
    echo.
)

echo [5] Verificando Django...
cd proyecto\src\backend 2>nul
if not errorlevel 1 (
    python -c "import django; print('[OK] Django', django.get_version())" 2>nul
    if errorlevel 1 (
        echo [ERROR] Django no esta instalado
        echo Ejecuta: pip install -r requirements.txt
    )
    echo.
    cd ..\..\..
) else (
    echo [ERROR] No se pudo acceder al directorio backend
    echo.
)

echo [6] Verificando archivo .env...
if exist "proyecto\src\backend\.env" (
    echo [OK] Archivo .env encontrado
    echo.
) else (
    echo [ADVERTENCIA] Archivo .env no encontrado
    echo Se usara la configuracion por defecto
    echo.
)

echo ============================================================
echo    Diagnostico completado
echo ============================================================
echo.
echo Si hay errores, corrigelos antes de ejecutar iniciar_desarrollo.bat
echo.
pause

