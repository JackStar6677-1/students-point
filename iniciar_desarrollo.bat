@echo off
title StudentsPoint - Desarrollo
color 0A

echo ============================================================
echo    StudentsPoint - Modo Desarrollo
echo ============================================================
echo.

REM Preguntar si limpiar cache
set /p CLEAN_CACHE="¿Limpiar cache y sesiones? (S/N): "
if /i "%CLEAN_CACHE%"=="S" (
    echo [INFO] Limpiando cache de Django...
    cd proyecto\src\backend
    python manage.py clearsessions
    python manage.py clear_cache
    if exist db.sqlite3 (
        echo [INFO] Eliminando base de datos de desarrollo...
        del db.sqlite3
    )
    cd ..\..\..
)

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

cd proyecto\src\backend

echo Instalando dependencias...
pip install -r requirements.txt -q
echo [OK] Dependencias instaladas
echo.

echo Verificando configuración...
python manage.py check
echo [OK] Configuración correcta
echo.

echo Aplicando migraciones...
python manage.py migrate --run-syncdb
echo [OK] Migraciones aplicadas
echo.

echo Recolectando archivos estáticos (forzado)...
python manage.py collectstatic --noinput --clear
echo [OK] Archivos estáticos actualizados
echo.

echo Creando superusuario...
python ensure_superuser.py
echo [OK] Superusuario configurado
echo.

echo ============================================================
echo    SERVIDOR LISTO
echo ============================================================
echo.
echo Aplicacion: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin/
echo API Docs: http://127.0.0.1:8000/api/docs/
echo.
echo Credenciales: admin@studentspoint.app / admin123
echo.
echo NOTA: Si ves errores de cache, reinicia el navegador
echo con Ctrl+Shift+Delete para limpiar cache del navegador
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

echo Iniciando servidor...
python manage.py runserver 127.0.0.1:8000

pause