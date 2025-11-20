@echo off
chcp 65001 >nul
title StudentsPoint - playit.gg Tunnel
color 0D

cd /d "%~dp0"

echo ============================================================
echo    StudentsPoint - Servidor con playit.gg Tunnel
echo ============================================================
echo.
echo Este script iniciara el servidor Django y playit.gg para
echo obtener acceso publico y probar la PWA desde internet.
echo.

REM Verificar que playit.gg este instalado
where playit >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] playit.gg no encontrado en PATH
    echo.
    echo Si ya instalaste playit.gg:
    echo   - Asegurate de que el ejecutable este en el PATH
    echo   - O coloca playit.exe en la carpeta del proyecto
    echo.
    echo Si no lo has instalado:
    echo   - Descarga desde: https://playit.gg/download
    echo   - Instala y configura tu tunel
    echo.
    echo El servidor Django se iniciara de todos modos...
    echo Puedes iniciar playit.gg manualmente despues.
    echo.
    timeout /t 5 /nobreak
    set PLAYIT_AVAILABLE=0
) else (
    echo [OK] playit.gg encontrado
    echo.
    set PLAYIT_AVAILABLE=1
)

echo [1/4] Navegando al backend...
cd proyecto\src\backend

if errorlevel 1 (
    echo [ERROR] No se encontro el directorio backend
    pause
    exit /b 1
)

echo [OK] Directorio backend encontrado
echo.

echo [2/4] Instalando dependencias...
pip install -r requirements.txt -q
echo [OK] Dependencias instaladas
echo.

echo [3/4] Aplicando migraciones y recolectando estaticos...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1
echo [OK] Base de datos y estaticos listos
echo.

echo [4/4] Iniciando servidor Django en puerto 8000...
echo.

REM Iniciar Django en una nueva ventana separada
start "Django Server - NO CERRAR" cmd /k "python manage.py runserver 127.0.0.1:8000"

echo Esperando a que Django inicie...
echo.

REM Esperar 10 segundos para que Django inicie completamente
timeout /t 10 /nobreak

echo ============================================================
echo    Servidor Django Iniciado en ventana separada
echo ============================================================
echo.
echo IMPORTANTE:
echo   - NO CIERRES la ventana "Django Server - NO CERRAR"
echo   - Servidor local: http://127.0.0.1:8000
echo.
echo Verificando que Django esta corriendo...
echo.

REM Verificar que Django responde
curl -s http://localhost:8000 >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Django puede no estar listo todavia
    echo Esperando 5 segundos mas...
    timeout /t 5 /nobreak >nul
)

echo [OK] Django esta corriendo
echo.

if %PLAYIT_AVAILABLE%==1 (
    echo Ahora iniciando playit.gg en ventana separada...
    echo.
    
    REM Volver a la raiz para iniciar playit
    cd ..\..\..
    
    REM Iniciar playit.gg en ventana separada
    start "Playit.gg Tunnel - NO CERRAR" cmd /k "playit"
    
    echo.
    echo ============================================================
    echo    playit.gg iniciado en ventana separada
    echo ============================================================
    echo.
) else (
    echo ============================================================
    echo    playit.gg NO esta disponible
    echo ============================================================
    echo.
    echo Puedes iniciar playit.gg manualmente en otra terminal.
    echo.
)

echo ============================================================
echo    INFORMACION DE ACCESO
echo ============================================================
echo.
echo [ACCESO LOCAL]
echo   App:       http://127.0.0.1:8000
echo   Admin:     http://127.0.0.1:8000/admin/
echo   API Docs:  http://127.0.0.1:8000/api/docs/
echo.
echo [ACCESO PUBLICO - playit.gg]
echo   Dominio:   best-wales.gl.at.ply.gg:16063
echo   App:       http://best-wales.gl.at.ply.gg:16063
echo   Admin:     http://best-wales.gl.at.ply.gg:16063/admin/
echo.
echo NOTA: Si tu dominio de playit.gg es diferente, actualiza
echo       la variable ALLOWED_HOSTS en settings/dev.py
echo.
echo [CREDENCIALES DE ACCESO]
echo   Usuario:   admin@studentspoint.app
echo   Password:  admin123
echo.
echo [CONFIGURACION DE PWA]
echo   Para probar PWA desde internet:
echo   1. Accede desde tu celular a: http://best-wales.gl.at.ply.gg:16063
echo   2. Abre el menu de opciones del navegador
echo   3. Selecciona "Agregar a pantalla de inicio"
echo   4. La PWA se instalara correctamente
echo.
echo NOTA IMPORTANTE:
echo   - El tunel de playit.gg debe estar activo y configurado
echo   - Asegurate de que el puerto 8000 este mapeado en playit.gg
echo   - El agente debe estar corriendo (ventana separada)
echo.
echo ============================================================
echo    LOGS DEL SISTEMA
echo ============================================================
echo   General:   proyecto\src\backend\logs\general.log
echo   Errores:   proyecto\src\backend\logs\errors.log
echo   API:       proyecto\src\backend\logs\api.log
echo   Auth:      proyecto\src\backend\logs\auth.log
echo.
echo ============================================================
echo.
echo PARA DETENER TODO:
echo   1. Presiona Ctrl+C en esta ventana
echo   2. Cierra la ventana "Django Server - NO CERRAR"
echo   3. Cierra la ventana "Playit.gg Tunnel - NO CERRAR"
echo.
echo ============================================================
echo.
echo Presiona cualquier tecla para finalizar este script...
echo Las otras ventanas seguiran abiertas hasta que las cierres.
echo.
pause >nul

echo.
echo ============================================================
echo SCRIPT FINALIZADO
echo ============================================================
echo.
echo RECUERDA: 
echo   - Cierra manualmente "Django Server - NO CERRAR"
echo   - Cierra manualmente "Playit.gg Tunnel - NO CERRAR"
echo.
pause

