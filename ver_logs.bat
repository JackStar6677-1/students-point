@echo off
title Ver Logs - StudentsPoint
color 0B

:menu
cls
echo ============================================================
echo    Ver Logs - StudentsPoint
echo ============================================================
echo.
echo Selecciona el log que deseas ver:
echo.
echo   1) General (todos los eventos)
echo   2) Errores (solo errores)
echo   3) API (peticiones y respuestas)
echo   4) Autenticacion (login, registro, etc)
echo   5) Monitor en Tiempo Real
echo   6) Analisis Completo
echo   7) Volver
echo.
set /p opcion="Opcion (1-7): "

cd proyecto\src\backend

if "%opcion%"=="1" goto general
if "%opcion%"=="2" goto errores
if "%opcion%"=="3" goto api
if "%opcion%"=="4" goto auth
if "%opcion%"=="5" goto monitor
if "%opcion%"=="6" goto analisis
if "%opcion%"=="7" exit
goto menu

:general
cls
echo ============================================================
echo    Log General - Presiona Ctrl+C para volver
echo ============================================================
echo.
if exist logs\general.log (
    powershell -Command "Get-Content logs\general.log -Wait -Tail 50"
) else (
    echo [ERROR] Archivo logs\general.log no encontrado
    echo [INFO] Inicia el servidor primero con iniciar_desarrollo.bat
    pause
)
goto menu

:errores
cls
echo ============================================================
echo    Log de Errores - Presiona Ctrl+C para volver
echo ============================================================
echo.
if exist logs\errors.log (
    powershell -Command "Get-Content logs\errors.log -Wait -Tail 30 | Where-Object {$_ -match 'ERROR|CRITICAL'}"
) else (
    echo [INFO] No hay errores registrados aun
    echo [INFO] Esto es bueno - significa que no hay errores!
    pause
)
goto menu

:api
cls
echo ============================================================
echo    Log de API - Presiona Ctrl+C para volver
echo ============================================================
echo.
if exist logs\api.log (
    powershell -Command "Get-Content logs\api.log -Wait -Tail 40"
) else (
    echo [ERROR] Archivo logs\api.log no encontrado
    pause
)
goto menu

:auth
cls
echo ============================================================
echo    Log de Autenticacion - Presiona Ctrl+C para volver
echo ============================================================
echo.
if exist logs\auth.log (
    powershell -Command "Get-Content logs\auth.log -Wait -Tail 30"
) else (
    echo [ERROR] Archivo logs\auth.log no encontrado
    pause
)
goto menu

:monitor
cls
echo ============================================================
echo    Monitor de Logs en Tiempo Real
echo ============================================================
echo.
echo Presiona Ctrl+C para volver al menu
echo.
python monitor_logs.py --interval 30
goto menu

:analisis
cls
echo ============================================================
echo    Analisis de Logs
echo ============================================================
echo.
set /p horas="Horas a analizar (default 24): "
if "%horas%"=="" set horas=24

python analyze_logs.py --hours %horas%
echo.
pause
goto menu

