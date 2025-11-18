@echo off
chcp 65001 >nul
title Regenerar Iconos PWA - StudentsPoint
color 0B

cd /d "%~dp0"

echo ============================================================
echo    Regenerar Iconos PWA con Logo de StudentsPoint
echo ============================================================
echo.

REM Verificar que Python este disponible
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    pause
    exit /b 1
)

echo [1/5] Verificando dependencias...
python -c "from PIL import Image" 2>nul
if errorlevel 1 (
    echo [INFO] Instalando Pillow...
    cd proyecto\src\backend
    pip install Pillow --quiet
    cd ..\..\..
)
echo [OK] Pillow disponible
echo.

echo [2/5] Verificando logo de StudentsPoint...
if not exist "proyecto\src\frontend\static\images\Logo_StudentsPoint.svg.png" (
    echo [ERROR] No se encontro el logo de StudentsPoint
    echo Ubicacion esperada: proyecto\src\frontend\static\images\Logo_StudentsPoint.svg.png
    pause
    exit /b 1
)
echo [OK] Logo encontrado
echo.

echo [3/5] Generando iconos PWA en todos los tamaños...
python -c "
from PIL import Image
from pathlib import Path

# Rutas
logo_path = Path('proyecto/src/frontend/static/images/Logo_StudentsPoint.svg.png')
icons_dir = Path('proyecto/src/frontend/static/images/icons')
icons_dir.mkdir(parents=True, exist_ok=True)

# Cargar logo
logo = Image.open(logo_path)
if logo.mode != 'RGBA':
    logo = logo.convert('RGBA')

# Generar todos los tamaños
sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
    # Redimensionar
    icon = logo.copy()
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    
    # Crear imagen cuadrada centrada
    final_icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    paste_x = (size - icon.size[0]) // 2
    paste_y = (size - icon.size[1]) // 2
    final_icon.paste(icon, (paste_x, paste_y), icon)
    
    # Guardar
    output_path = icons_dir / f'icon-{size}x{size}.png'
    final_icon.save(output_path, 'PNG', optimize=True)
    print(f'  - icon-{size}x{size}.png')

print('\\nTodos los iconos generados correctamente')
"

if errorlevel 1 (
    echo [ERROR] Fallo al generar iconos
    pause
    exit /b 1
)
echo [OK] Iconos generados
echo.

echo [4/5] Copiando iconos a staticfiles...
cd proyecto\src\backend
python manage.py collectstatic --noinput >nul 2>&1
cd ..\..\..
echo [OK] Iconos copiados a staticfiles
echo.

echo [5/5] Limpiando cache...
echo IMPORTANTE: Debes actualizar el cache del Service Worker
echo.

echo ============================================================
echo    Iconos PWA Regenerados Exitosamente
echo ============================================================
echo.
echo SIGUIENTES PASOS:
echo.
echo 1. Si el servidor esta corriendo, reinicialo
echo 2. En el navegador, presiona Ctrl+Shift+R para forzar recarga
echo 3. En el celular:
echo    a. Desinstala la PWA actual
echo    b. Cierra Chrome completamente
echo    c. Vuelve a instalar la PWA desde ngrok
echo.
echo NOTA: El nuevo icono de StudentsPoint aparecera en la instalacion
echo.
pause

