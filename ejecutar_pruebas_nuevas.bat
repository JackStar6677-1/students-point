@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════════════
echo    EJECUTAR PRUEBAS UNITARIAS NUEVAS - STUDENTSPOINT
echo ════════════════════════════════════════════════════════════
echo.
echo [1/4] Verificando archivos de prueba...
echo.

if not exist "pruebas_unitarias\api\test_portfolio_api.py" (
    echo ❌ ERROR: test_portfolio_api.py no encontrado
    pause
    exit /b 1
)

if not exist "pruebas_unitarias\api\test_marketplace_api.py" (
    echo ❌ ERROR: test_marketplace_api.py no encontrado
    pause
    exit /b 1
)

if not exist "pruebas_unitarias\api\test_notifications_api.py" (
    echo ❌ ERROR: test_notifications_api.py no encontrado
    pause
    exit /b 1
)

if not exist "pruebas_unitarias\api\test_polls_api.py" (
    echo ❌ ERROR: test_polls_api.py no encontrado
    pause
    exit /b 1
)

if not exist "pruebas_unitarias\api\test_health_api.py" (
    echo ❌ ERROR: test_health_api.py no encontrado
    pause
    exit /b 1
)

if not exist "pruebas_unitarias\api\test_converter_api.py" (
    echo ❌ ERROR: test_converter_api.py no encontrado
    pause
    exit /b 1
)

echo ✅ Todos los archivos de prueba están en su lugar
echo.

echo [2/4] Verificando sintaxis de Python...
echo.

python -m py_compile pruebas_unitarias\api\test_portfolio_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_portfolio_api.py
    pause
    exit /b 1
)

python -m py_compile pruebas_unitarias\api\test_marketplace_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_marketplace_api.py
    pause
    exit /b 1
)

python -m py_compile pruebas_unitarias\api\test_notifications_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_notifications_api.py
    pause
    exit /b 1
)

python -m py_compile pruebas_unitarias\api\test_polls_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_polls_api.py
    pause
    exit /b 1
)

python -m py_compile pruebas_unitarias\api\test_health_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_health_api.py
    pause
    exit /b 1
)

python -m py_compile pruebas_unitarias\api\test_converter_api.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Sintaxis incorrecta en test_converter_api.py
    pause
    exit /b 1
)

echo ✅ Sintaxis correcta en todos los archivos
echo.

echo [3/4] Ejecutando pruebas unitarias nuevas...
echo.

echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE PORTFOLIO API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_portfolio_api.py -v

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE MARKETPLACE API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_marketplace_api.py -v

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE NOTIFICACIONES API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_notifications_api.py -v

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE ENCUESTAS API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_polls_api.py -v

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE HEALTH API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_health_api.py -v

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS DE CONVERTER API
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\test_converter_api.py -v

echo.
echo [4/4] Ejecutando todas las pruebas juntas...
echo.

echo ════════════════════════════════════════════════════════════
echo    RESUMEN COMPLETO DE PRUEBAS
echo ════════════════════════════════════════════════════════════
python run_pytest.py pruebas_unitarias\api\ -v --tb=short

echo.
echo ════════════════════════════════════════════════════════════
echo    PRUEBAS COMPLETADAS
echo ════════════════════════════════════════════════════════════
echo.
echo ✅ Se ejecutaron las siguientes pruebas nuevas:
echo    - Portfolio API (CV/Curriculum)
echo    - Marketplace API (Productos)
echo    - Notifications API (Notificaciones)
echo    - Polls API (Encuestas)
echo    - Health API (Estado del sistema)
echo    - Converter API (Conversión de documentos)
echo.
echo 📊 Total de pruebas nuevas: ~60+ casos de prueba
echo 🎯 Cobertura: APIs principales del sistema
echo.
pause
