@echo off
chcp 65001 >nul
title StudentsPoint - Instalador PostgreSQL

echo ============================================================
echo    StudentsPoint - Instalador PostgreSQL
echo    Versión 1.2.0
echo ============================================================
echo.

echo [INFO] Este script te ayudará a instalar PostgreSQL para StudentsPoint
echo [INFO] Asegúrate de tener permisos de administrador
echo.

echo [INFO] Verificando si PostgreSQL ya está instalado...
psql --version >nul 2>&1
if not errorlevel 1 (
    echo [INFO] PostgreSQL ya está instalado
    psql --version
    echo.
    echo [INFO] ¿Deseas continuar con la configuración? (S/N)
    set /p continue=
    if /i not "%continue%"=="S" (
        echo [INFO] Instalación cancelada
        pause
        exit /b 0
    )
) else (
    echo [INFO] PostgreSQL no está instalado
    echo.
    echo [INFO] Descargando PostgreSQL...
    echo [INFO] Por favor descarga PostgreSQL desde: https://www.postgresql.org/download/windows/
    echo [INFO] O usa el instalador automático con Chocolatey
    echo.
    echo [INFO] ¿Tienes Chocolatey instalado? (S/N)
    set /p has_choco=
    if /i "%has_choco%"=="S" (
        echo [INFO] Instalando PostgreSQL con Chocolatey...
        choco install postgresql --yes
    ) else (
        echo [INFO] Instalación manual requerida
        echo [INFO] 1. Ve a https://www.postgresql.org/download/windows/
        echo [INFO] 2. Descarga el instalador oficial
        echo [INFO] 3. Ejecuta el instalador con las siguientes opciones:
        echo [INFO]    - Puerto: 5432 (por defecto)
        echo [INFO]    - Contraseña: recuérdala para configurar StudentsPoint
        echo [INFO]    - Locale: Spanish, Chile
        echo.
        echo [INFO] Presiona Enter cuando hayas completado la instalación...
        pause
    )
)

echo.
echo [INFO] Verificando instalación de PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL no se pudo instalar correctamente
    echo [INFO] Por favor instala PostgreSQL manualmente
    pause
    exit /b 1
)

echo [INFO] PostgreSQL instalado correctamente
psql --version

echo.
echo [INFO] Configurando base de datos para StudentsPoint...
echo [INFO] Ingresa la contraseña del usuario postgres:
echo [INFO] (Esta será la contraseña que configuraste durante la instalación)

REM Crear base de datos
echo [INFO] Creando base de datos 'studentspoint_prod'...
psql -U postgres -c "CREATE DATABASE studentspoint_prod;" 2>nul
if errorlevel 1 (
    echo [WARNING] No se pudo crear la base de datos automáticamente
    echo [INFO] Por favor crea la base de datos manualmente:
    echo [INFO] 1. Abre pgAdmin o psql
    echo [INFO] 2. Ejecuta: CREATE DATABASE studentspoint_prod;
) else (
    echo [INFO] Base de datos 'studentspoint_prod' creada exitosamente
)

echo.
echo [INFO] Verificando conexión a la base de datos...
psql -U postgres -d studentspoint_prod -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo conectar a la base de datos
    echo [INFO] Verifica la configuración de PostgreSQL
) else (
    echo [INFO] Conexión a la base de datos exitosa
)

echo.
echo ============================================================
echo [INFO] Instalación de PostgreSQL completada
echo.
echo 📋 PRÓXIMOS PASOS:
echo    1. Copia env.production.example como .env
echo    2. Configura las variables de base de datos en .env
echo    3. Ejecuta iniciar_produccion.bat
echo.
echo 🔧 CONFIGURACIÓN RECOMENDADA:
echo    - DB_NAME=studentspoint_prod
echo    - DB_USER=postgres
echo    - DB_PASSWORD=[tu_contraseña]
echo    - DB_HOST=localhost
echo    - DB_PORT=5432
echo.
echo 📚 DOCUMENTACIÓN:
echo    - PostgreSQL: https://www.postgresql.org/docs/
echo    - StudentsPoint: README.md
echo ============================================================

pause
