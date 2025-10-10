@echo off
title Ver Logs de Tests - StudentsPoint
color 0D

:menu
cls
echo ============================================================
echo    Ver Logs de Tests - StudentsPoint
echo ============================================================
echo.
echo Selecciona el tipo de log:
echo.
echo   1) Resumen de ultima ejecucion
echo   2) Errores de tests
echo   3) Log completo de tests
echo   4) Log detallado (con lineas de codigo)
echo   5) Ver todos los logs disponibles
echo   6) Limpiar logs antiguos
echo   7) Volver
echo.
set /p opcion="Opcion (1-7): "

if "%opcion%"=="1" goto resumen
if "%opcion%"=="2" goto errores
if "%opcion%"=="3" goto completo
if "%opcion%"=="4" goto detallado
if "%opcion%"=="5" goto listar
if "%opcion%"=="6" goto limpiar
if "%opcion%"=="7" exit
goto menu

:resumen
cls
echo ============================================================
echo    Resumen de Tests
echo ============================================================
echo.
if exist logs_tests\pytest_summary_latest.log (
    type logs_tests\pytest_summary_latest.log
) else (
    echo [INFO] No hay resumen disponible
    echo [INFO] Ejecuta primero: python run_pytest.py
)
echo.
pause
goto menu

:errores
cls
echo ============================================================
echo    Errores de Tests
echo ============================================================
echo.
if exist logs_tests\pytest_errors_latest.log (
    type logs_tests\pytest_errors_latest.log
) else (
    echo [INFO] No hay errores registrados
    echo [INFO] Esto es bueno - significa que todos los tests pasaron
)
echo.
pause
goto menu

:completo
cls
echo ============================================================
echo    Log Completo de Tests
echo ============================================================
echo.
if exist logs_tests\tests_execution.log (
    powershell -Command "Get-Content logs_tests\tests_execution.log -Tail 100"
) else (
    echo [ERROR] Archivo no encontrado
    echo [INFO] Ejecuta primero: python run_pytest.py
)
echo.
pause
goto menu

:detallado
cls
echo ============================================================
echo    Log Detallado de Tests
echo ============================================================
echo.
for /f %%f in ('dir /b /od logs_tests\test_detailed_*.log 2^>nul') do set lastfile=%%f
if defined lastfile (
    powershell -Command "Get-Content logs_tests\%lastfile% -Tail 150"
) else (
    echo [ERROR] No hay logs detallados disponibles
)
echo.
pause
goto menu

:listar
cls
echo ============================================================
echo    Logs Disponibles
echo ============================================================
echo.
if exist logs_tests (
    dir /b /o-d logs_tests\*.log
) else (
    echo [INFO] Directorio logs_tests no encontrado
)
echo.
pause
goto menu

:limpiar
cls
echo ============================================================
echo    Limpiar Logs Antiguos
echo ============================================================
echo.
set /p confirmar="¿Eliminar logs antiguos (mantener ultimos 5)? (S/N): "
if /i "%confirmar%"=="S" (
    echo Limpiando logs antiguos...
    
    REM Mantener solo ultimos 5 archivos pytest_*.log
    for /f "skip=5 tokens=*" %%f in ('dir /b /o-d logs_tests\pytest_*.log 2^>nul') do (
        echo Eliminando: %%f
        del logs_tests\%%f
    )
    
    REM Mantener solo ultimos 5 archivos test_*.log
    for /f "skip=5 tokens=*" %%f in ('dir /b /o-d logs_tests\test_*.log 2^>nul') do (
        echo Eliminando: %%f
        del logs_tests\%%f
    )
    
    echo [OK] Logs antiguos eliminados
) else (
    echo [INFO] Operacion cancelada
)
echo.
pause
goto menu

