@echo off
chcp 65001 >nul
title StudentsPoint - Aplicar Correcciones Móvil
color 0B

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Correcciones para Móvil
echo ============================================================
echo.
echo Este script aplicara las correcciones de responsive
echo y elementos en esquinas para celular.
echo.

echo [1/3] Copiando CSS de correcciones móvil...
echo.

REM Copiar mobile-fixes.css a staticfiles
cd proyecto\src\backend

robocopy "..\..\src\frontend\static\css" "staticfiles\css" mobile-fixes.css /NFL /NDL

if exist "staticfiles\css\mobile-fixes.css" (
    echo [OK] mobile-fixes.css copiado
) else (
    echo [ERROR] No se pudo copiar mobile-fixes.css
    pause
    exit /b 1
)

echo.
echo [2/3] Actualizando archivos estaticos...
echo.

python manage.py collectstatic --noinput >nul 2>&1

if errorlevel 1 (
    echo [WARNING] Advertencias al recolectar estaticos
) else (
    echo [OK] Archivos estaticos actualizados
)

echo.
echo [3/3] Verificando iconos PWA...
echo.

cd ..\..\..

set icon_count=0
for %%s in (72 96 128 144 152 192 384 512) do (
    if exist "proyecto\src\frontend\static\images\icons\icon-%%sx%%s.png" (
        set /a icon_count+=1
    )
)

echo Iconos PWA encontrados: %icon_count%/8

if %icon_count% LSS 8 (
    echo.
    echo [WARNING] Faltan algunos iconos PWA
    echo Genera los iconos faltantes con:
    echo   - https://realfavicongenerator.net/
    echo   - https://www.pwabuilder.com/imageGenerator
    echo.
) else (
    echo [OK] Todos los iconos PWA presentes
)

echo.
echo ============================================================
echo    Correcciones Aplicadas
echo ============================================================
echo.
echo Cambios implementados:
echo   [x] mobile-fixes.css agregado
echo   [x] Botones flotantes reposicionados
echo   [x] Tamaños tactiles minimos (44x44px)
echo   [x] Soporte para safe-area (notch)
echo   [x] Responsive mejorado
echo.
echo Para verificar en celular:
echo   1. Inicia el servidor: iniciar_desarrollo.bat
echo   2. Abre en celular: http://100.75.238.19:8000
echo   3. Verifica que todos los botones sean clickeables
echo   4. Verifica que el logo sea de StudentsPoint
echo.
echo Si el logo muestra DuocUC antiguo:
echo   - Desinstala la PWA
echo   - Borra cache de Chrome
echo   - Reinstala la PWA
echo.
echo Documentacion: CORRECIONES-MOVIL.md
echo.
pause

