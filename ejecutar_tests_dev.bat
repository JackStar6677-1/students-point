@echo off
REM ====================================================
REM Script de Testing Rápido para Desarrollo
REM ====================================================

echo.
echo ========================================
echo   PRUEBAS AUTOMATICAS - StudentsPoint
echo ========================================
echo.

cd proyecto\src\backend

echo [1/4] Verificando entorno...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias de testing...
pip install pytest pytest-django pytest-cov selenium requests -q

echo.
echo [3/4] Aplicando migraciones...
python manage.py migrate --noinput

echo.
echo [4/4] Ejecutando pruebas unitarias...
pytest ..\..\..\..\pruebas_unitarias\ -v --tb=short

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   ALGUNAS PRUEBAS FALLARON
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   TODAS LAS PRUEBAS PASARON!
echo ========================================
echo.

cd ..\..\..

pause
