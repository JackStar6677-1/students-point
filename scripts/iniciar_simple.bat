@echo off
chcp 65001 >nul
title StudentsPoint - Inicio Simple
color 0A

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Inicio Simple
echo ============================================================
echo.

cd proyecto\src\backend
if errorlevel 1 (
    echo ERROR: No se encontro el directorio backend
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install -r requirements.txt -q

echo Aplicando migraciones...
python manage.py migrate --run-syncdb

echo Recolectando archivos estaticos...
python manage.py collectstatic --noinput >nul 2>&1

echo.
echo ============================================================
echo SERVIDOR INICIADO
echo ============================================================
echo.
echo URLs:
echo   http://127.0.0.1:8000
echo   http://127.0.0.1:8000/admin/
echo.
echo Credenciales: admin@studentspoint.app / admin123
echo.
echo Presiona Ctrl+C para detener
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

python manage.py runserver 0.0.0.0:8000

pause

