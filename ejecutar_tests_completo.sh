#!/bin/bash
# ====================================================
# Script de Testing Completo para Linux/Mac
# ====================================================

echo ""
echo "========================================"
echo "  PRUEBAS AUTOMATICAS - StudentsPoint"
echo "========================================"
echo ""

cd proyecto/src/backend

echo "[1/5] Verificando entorno..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no está instalado"
    exit 1
fi

echo ""
echo "[2/5] Instalando dependencias de testing..."
pip3 install pytest pytest-django pytest-cov selenium requests pillow -q

echo ""
echo "[3/5] Aplicando migraciones..."
python3 manage.py migrate --noinput

echo ""
echo "[4/5] Creando superusuario de testing..."
python3 manage.py ensure_superuser

echo ""
echo "[5/5] Ejecutando pruebas..."
pytest ../../../../pruebas_unitarias/ -v --tb=short --cov=. --cov-report=term-missing

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  ALGUNAS PRUEBAS FALLARON"
    echo "========================================"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "  TODAS LAS PRUEBAS PASARON!"
echo "========================================"
echo ""

cd ../../..

