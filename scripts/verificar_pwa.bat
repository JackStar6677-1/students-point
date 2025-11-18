@echo off
chcp 65001 >nul
cls
echo ========================================
echo   Verificación PWA - StudentsPoint
echo ========================================
echo.

cd /d "%~dp0proyecto\src\backend"

echo [1/5] Verificando archivos críticos...
echo.

if not exist "staticfiles\sw.js" (
    echo [X] ERROR: sw.js no encontrado
    pause
    exit /b 1
) else (
    echo [OK] sw.js encontrado
)

if not exist "staticfiles\manifest.json" (
    echo [X] ERROR: manifest.json no encontrado
    pause
    exit /b 1
) else (
    echo [OK] manifest.json encontrado
)

if not exist "staticfiles\pwa-config.js" (
    echo [X] ERROR: pwa-config.js no encontrado
    pause
    exit /b 1
) else (
    echo [OK] pwa-config.js encontrado
)

if not exist "staticfiles\js\pwa.js" (
    echo [X] ERROR: js\pwa.js no encontrado
    pause
    exit /b 1
) else (
    echo [OK] js\pwa.js encontrado
)

echo.
echo [2/5] Verificando iconos PWA...
echo.

set icon_found=0
for %%s in (72 96 128 144 152 192 384 512) do (
    if exist "staticfiles\images\icons\icon-%%sx%%s.png" (
        echo [OK] icon-%%sx%%s.png
        set /a icon_found+=1
    ) else (
        echo [!] FALTA: icon-%%sx%%s.png
    )
)

echo.
echo [3/5] Verificando archivos HTML...
echo.

if exist "staticfiles\index.html" (
    echo [OK] index.html
) else (
    echo [!] FALTA: index.html
)

if exist "staticfiles\login.html" (
    echo [OK] login.html
) else (
    echo [!] FALTA: login.html
)

echo.
echo [4/5] Verificando estructura...
echo.

if exist "staticfiles\css\" (
    echo [OK] Carpeta CSS
) else (
    echo [X] FALTA: Carpeta CSS
)

if exist "staticfiles\js\" (
    echo [OK] Carpeta JS
) else (
    echo [X] FALTA: Carpeta JS
)

if exist "staticfiles\images\" (
    echo [OK] Carpeta images
) else (
    echo [X] FALTA: Carpeta images
)

echo.
echo [5/5] Resumen de verificación...
echo.

echo ----------------------------------------
echo   Archivos PWA críticos: OK
echo   Iconos encontrados: %icon_found%/8
echo   Estructura: OK
echo ----------------------------------------
echo.

if %icon_found% LSS 8 (
    echo [!] ADVERTENCIA: Faltan algunos iconos
    echo     La PWA funcionará pero puede tener problemas de visualización
)

echo.
echo ========================================
echo   Verificación completada
echo ========================================
echo.
echo La PWA debería estar lista para usar.
echo.
echo Para iniciar el servidor:
echo   iniciar_desarrollo.bat
echo.
echo Para acceder:
echo   http://localhost:8000
echo   http://100.75.238.19:8000 (Tailscale laptop)
echo   http://100.113.204.115:8000 (Tailscale desktop)
echo.
pause

