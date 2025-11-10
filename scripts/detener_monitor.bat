@echo off
title Detener Monitor - StudentsPoint
color 0C

echo ============================================================
echo    Deteniendo Monitor de Logs - StudentsPoint
echo ============================================================
echo.

echo Buscando procesos de monitor_logs.py...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /v ^| findstr "monitor_logs"') do (
    echo Deteniendo proceso %%a...
    taskkill /PID %%a /F
)

echo.
echo [OK] Monitor de logs detenido
echo.
pause

