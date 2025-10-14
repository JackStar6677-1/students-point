@echo off
title StudentsPoint - Desarrollo
color 0A

echo ============================================================
echo    StudentsPoint - Modo Desarrollo
echo ============================================================
echo.

REM Desactivar borrado de cache/DB para evitar pérdidas accidentales
REM (Si necesitas limpiar, hazlo manualmente con comandos dedicados)

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

echo Recolectando archivos estáticos...
python manage.py collectstatic --noinput
echo [OK] Archivos estáticos actualizados
echo.

echo Creando superusuario...
python ensure_superuser.py
echo [OK] Superusuario configurado
echo.

echo Creando usuarios de prueba...
python manage.py create_demo_users >nul 2>&1
echo [OK] Usuarios de prueba listos
echo.

REM Crear directorio de logs si no existe
if not exist logs mkdir logs

echo Limpiando logs expirados...
python -c "from pathlib import Path; import os; logs_dir = Path('logs'); [os.remove(logs_dir / f) for f in os.listdir(logs_dir) if f.endswith('.log') and (logs_dir / f).stat().st_size > 50*1024*1024]" 2>nul
echo [OK] Logs listos
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
echo [LOGS] Sistema de logging activo en: logs/
echo   - general.log: Todos los eventos
echo   - errors.log: Solo errores
echo   - api.log: Peticiones API
echo   - auth.log: Autenticacion
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Monitor de logs deshabilitado por defecto
REM Para habilitar, descomenta la siguiente linea:
REM start "StudentsPoint - Monitor de Logs" cmd /k "color 0E && python monitor_logs.py --interval 30"

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

echo Iniciando servidor...
python manage.py runserver 127.0.0.1:8000

pause