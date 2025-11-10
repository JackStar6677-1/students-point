@echo off
title StudentsPoint - Produccion
color 0E

echo ============================================================
echo    StudentsPoint - Modo Produccion
echo ============================================================
echo.

echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.11+ desde python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo [2/8] Verificando directorio del proyecto...
cd proyecto\src\backend
if errorlevel 1 (
    echo [ERROR] No se pudo acceder al directorio backend
    pause
    exit /b 1
)

echo [OK] Directorio backend encontrado
echo.

echo [3/8] Instalando dependencias de produccion...
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
if errorlevel 1 (
    echo [ERROR] Error instalando dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

echo [4/8] Configurando variables de entorno...
if not exist ".env" (
    echo Copiando configuracion de produccion...
    copy "..\..\env.production.example" ".env"
    echo.
    echo [IMPORTANTE] Archivo .env creado. Edita las siguientes variables:
    echo - SECRET_KEY: Cambia por una clave segura
    echo - ALLOWED_HOSTS: Configura tu dominio
    echo - DATABASE_URL: Verifica la configuracion de PostgreSQL
    echo - GOOGLE_OAUTH_CLIENT_ID: Configura si usas credenciales diferentes
    echo - GOOGLE_OAUTH_CLIENT_SECRET: Configura si usas credenciales diferentes
    echo.
    pause
)

echo [OK] Variables de entorno configuradas
echo.

echo [5/8] Verificando conexion a PostgreSQL...
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, user='postgres', password='214526867', database='postgres'); print('Conexion exitosa a PostgreSQL'); conn.close()" 2>nul
if errorlevel 1 (
    echo [WARNING] No se puede conectar a PostgreSQL
    echo Verifica que PostgreSQL este ejecutandose en puerto 5432
    echo Usuario: postgres, Password: 214526867
    echo.
    echo Continuando con SQLite para desarrollo...
    echo.
)

echo [OK] Base de datos verificada
echo.

echo [6/8] Aplicando migraciones...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo [ERROR] Error aplicando migraciones
    pause
    exit /b 1
)

echo [OK] Migraciones aplicadas
echo.

echo [7/8] Recolectando archivos estaticos...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo [WARNING] Error recolectando archivos estaticos (continuando...)
)

echo [OK] Archivos estaticos recolectados
echo.

echo [8/8] Creando superusuario...
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
echo URIs de redireccion autorizadas:
echo - http://localhost:8000/api/auth/google/callback/web/
echo - http://127.0.0.1:8000/api/auth/google/callback/web/
echo - https://tu-dominio.com/api/auth/google/callback/web/
echo - https://studentspoint.app/api/auth/google/callback/web/
echo.
echo ============================================================
echo    PRODUCCION LISTA
echo ============================================================
echo.
echo URLs de acceso:
echo - Aplicacion: http://127.0.0.1:8000
echo - Admin: http://127.0.0.1:8000/admin/
echo - API Docs: http://127.0.0.1:8000/api/docs/
echo.
echo Credenciales de administrador:
echo - Email: admin@studentspoint.app
echo - Password: admin123
echo.
echo Base de datos: PostgreSQL (puerto 5432) o SQLite (desarrollo)
echo Archivos estaticos: staticfiles/
echo.
echo Para iniciar el servidor de produccion:
echo gunicorn --config gunicorn.conf.py studentspoint.wsgi:application
echo.
echo Para iniciar con Django (desarrollo):
echo python manage.py runserver 0.0.0.0:8000
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

echo Iniciando servidor de produccion...
python manage.py runserver 0.0.0.0:8000