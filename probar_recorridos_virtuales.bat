@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════════════
echo    PROBAR RECORRIDOS VIRTUALES - STUDENTSPOINT
echo ════════════════════════════════════════════════════════════
echo.
echo [1/3] Verificando archivos...
echo.

if not exist "proyecto\imagenes\mapa\casino\img1casino.jpeg" (
    echo ❌ ERROR: No se encuentran las imágenes del casino
    echo    Ubicación esperada: proyecto\imagenes\mapa\casino\
    pause
    exit /b 1
)

if not exist "proyecto\src\backend\staticfiles\streetview\streetview.js" (
    echo ❌ ERROR: Archivo JavaScript no encontrado
    pause
    exit /b 1
)

if not exist "proyecto\src\backend\staticfiles\streetview\streetview.css" (
    echo ❌ ERROR: Archivo CSS no encontrado
    pause
    exit /b 1
)

echo ✅ Todos los archivos están en su lugar
echo.

echo [2/3] Iniciando servidor Django...
echo.

cd proyecto\src\backend

echo Iniciando en http://127.0.0.1:8000/streetview/
echo.
echo ════════════════════════════════════════════════════════════
echo    INSTRUCCIONES DE PRUEBA
echo ════════════════════════════════════════════════════════════
echo.
echo 1. El navegador se abrirá automáticamente
echo 2. Selecciona "DuocUC Sede Maipú" en el selector
echo 3. Haz clic en "Explorar Recorridos"
echo 4. Haz clic en la card "Casino" (es la única disponible)
echo 5. Navega usando:
echo    - Flechas flotantes (izquierda/derecha)
echo    - Puntos (dots) en la parte inferior
echo    - Teclado: Flechas ← →, Espacio, Escape
echo    - En mobile: Gestos swipe
echo.
echo Para probar en MOBILE:
echo 1. Presiona F12 para abrir DevTools
echo 2. Presiona Ctrl+Shift+M para modo responsive
echo 3. Selecciona un dispositivo móvil (ej: iPhone 12)
echo 4. Prueba los gestos swipe
echo.
echo [3/3] Abriendo navegador...
timeout /t 3 >nul
start http://127.0.0.1:8000/streetview/
echo.

python manage.py runserver

echo.
echo Servidor detenido.
pause

