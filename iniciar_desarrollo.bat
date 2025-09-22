@echo off
title StudentsPoint - Desarrollo
color 0A

echo ============================================================
echo    StudentsPoint - Modo Desarrollo
echo ============================================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.11+ desde python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo Navegando al directorio backend...
cd proyecto\src\backend
if errorlevel 1 (
    echo [ERROR] No se pudo acceder al directorio backend
    pause
    exit /b 1
)

echo [OK] Directorio backend encontrado
echo.

echo Verificando archivo requirements.txt...
if not exist requirements.txt (
    echo [ERROR] Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

echo [OK] requirements.txt encontrado
echo.

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error instalando dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

echo Verificando configuración de Django...
python manage.py check
if errorlevel 1 (
    echo [ERROR] Problema con la configuración de Django
    pause
    exit /b 1
)

echo [OK] Configuración de Django correcta
echo.

echo Aplicando migraciones de base de datos...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo [ERROR] Error aplicando migraciones
    pause
    exit /b 1
)

echo [OK] Migraciones aplicadas
echo.

echo Recolectando archivos estáticos...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo [WARNING] Error recolectando archivos estáticos (continuando...)
)

echo [OK] Archivos estáticos recolectados
echo.

echo Creando superusuario...
python ensure_superuser.py
if errorlevel 1 (
    echo [WARNING] Error creando superusuario (continuando...)
)

echo [OK] Superusuario configurado
echo.

echo ============================================================
echo    CONFIGURACION COMPLETADA
echo ============================================================
echo.
echo Google OAuth configurado con credenciales por defecto
echo URIs de redirección autorizadas:
echo - http://localhost:8000/api/auth/google/callback/web/
echo - http://127.0.0.1:8000/api/auth/google/callback/web/
echo.
echo ============================================================
echo    SERVIDOR LISTO
echo ============================================================
echo.
echo Aplicacion: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin/
echo API Docs: http://127.0.0.1:8000/api/docs/
echo.
echo Credenciales de administrador:
echo Email: admin@studentspoint.app
echo Password: admin123
echo.
echo Funcionalidades disponibles:
echo - Autenticacion JWT + Google OAuth
echo - Foros con moderacion
echo - Marketplace con enlaces externos
echo - Portafolio con generacion PDF
echo - Encuestas y votaciones
echo - Horarios de clases
echo - Notificaciones push
echo - Recorridos virtuales
echo - Sistema de reportes
echo - Cursos OTEC
echo - Bienestar estudiantil
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000

echo Iniciando servidor de desarrollo...
python manage.py runserver 127.0.0.1:8000

echo.
echo Servidor detenido
pause