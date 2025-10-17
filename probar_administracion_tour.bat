@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════════════
echo    PROBAR RECORRIDO DE ADMINISTRACIÓN - STUDENTSPOINT
echo ════════════════════════════════════════════════════════════
echo.
echo [1/3] Verificando archivos...
echo.

if not exist "proyecto\imagenes\mapa\administracion\img1administracion.jpeg" (
    echo ❌ ERROR: No se encuentran las imágenes de administración
    echo    Ubicación esperada: proyecto\imagenes\mapa\administracion\
    pause
    exit /b 1
)

if not exist "proyecto\src\backend\staticfiles\imagenes\mapa\administracion\img1administracion.jpeg" (
    echo ❌ ERROR: Imágenes no copiadas a staticfiles
    echo    Ejecuta: copy proyecto\imagenes\mapa\administracion\*.jpeg proyecto\src\backend\staticfiles\imagenes\mapa\administracion\
    pause
    exit /b 1
)

if not exist "proyecto\src\backend\staticfiles\streetview\streetview.js" (
    echo ❌ ERROR: Archivo JavaScript no encontrado en staticfiles
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
echo    INSTRUCCIONES DE PRUEBA - ADMINISTRACIÓN
echo ════════════════════════════════════════════════════════════
echo.
echo 1. El navegador se abrirá automáticamente
echo 2. Selecciona "DuocUC Sede Maipú" en el selector
echo 3. Haz clic en "Explorar Recorridos"
echo 4. Ahora verás DOS recorridos disponibles:
echo    - ✅ Casino (ya funcionaba)
echo    - ✅ Administración (¡NUEVO!)
echo 5. Haz clic en la card "Administración" 
echo 6. Navega por las 5 imágenes usando:
echo    - Flechas flotantes (izquierda/derecha)
echo    - Puntos (dots) en la parte inferior
echo    - Teclado: Flechas ← →, Espacio, Escape
echo.
echo ════════════════════════════════════════════════════════════
echo    IMÁGENES DE ADMINISTRACIÓN
echo ════════════════════════════════════════════════════════════
echo.
echo 1. Entrada a Administración
echo 2. Recepción Administrativa  
echo 3. Oficinas Administrativas
echo 4. Sala de Reuniones
echo 5. Vista General
echo.
echo Presiona cualquier tecla para iniciar el servidor...
pause >nul

echo.
echo Iniciando servidor Django...
echo.
python manage.py runserver
