#!/bin/bash

# StudentsPoint - Instalación PWA v1.2.3

echo "============================================"
echo "  StudentsPoint - Instalación PWA v1.2.3"
echo "============================================"
echo ""

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "[1/5] Activando entorno virtual..."
cd "$PROJECT_ROOT/proyecto/src/backend"
source "$PROJECT_ROOT/venv/bin/activate" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar el entorno virtual"
    echo "Asegúrate de tener el venv creado en la raíz del proyecto"
    exit 1
fi
echo "OK - Entorno virtual activado"
echo ""

echo "[2/5] Configurando variables de entorno..."
export DJANGO_SETTINGS_MODULE=studentspoint.settings.dev
export PYTHONPATH="$PROJECT_ROOT/proyecto/src/backend"
echo "OK - Variables configuradas"
echo ""

echo "[3/5] Ejecutando collectstatic..."
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "ERROR: Falló collectstatic"
    exit 1
fi
echo "OK - Archivos estáticos recolectados"
echo ""

echo "[4/5] Verificando archivos PWA críticos..."

STATICFILES_DIR="$PROJECT_ROOT/proyecto/src/backend/staticfiles"

if [ ! -f "$STATICFILES_DIR/sw.js" ]; then
    echo "ERROR: No se encontró sw.js en staticfiles"
    exit 1
fi
echo "OK - sw.js encontrado"

if [ ! -f "$STATICFILES_DIR/manifest.json" ]; then
    echo "ERROR: No se encontró manifest.json en staticfiles"
    exit 1
fi
echo "OK - manifest.json encontrado"

if [ ! -f "$STATICFILES_DIR/pwa-config.js" ]; then
    echo "ERROR: No se encontró pwa-config.js en staticfiles"
    exit 1
fi
echo "OK - pwa-config.js encontrado"

if [ ! -f "$STATICFILES_DIR/js/pwa.js" ]; then
    echo "ERROR: No se encontró js/pwa.js en staticfiles"
    exit 1
fi
echo "OK - pwa.js encontrado"

echo ""
echo "[5/5] Verificando iconos PWA..."

ICONS_DIR="$STATICFILES_DIR/images/icons"

for size in 72 96 128 144 152 192 384 512; do
    icon_file="$ICONS_DIR/icon-${size}x${size}.png"
    if [ ! -f "$icon_file" ]; then
        echo "ADVERTENCIA: No se encontró icon-${size}x${size}.png"
    else
        echo "OK - icon-${size}x${size}.png"
    fi
done

echo ""
echo "============================================"
echo "  Instalación PWA Completada"
echo "============================================"
echo ""
echo "La PWA está lista para usarse."
echo ""
echo "Para acceder:"
echo "  - Localhost: http://localhost:8000"
echo "  - Tailscale Laptop: http://100.75.238.19:8000"
echo "  - Tailscale Desktop: http://100.113.204.115:8000"
echo ""
echo "Una vez en la página, busca el botón 'Instalar App'"
echo "o el icono de instalación en la barra de direcciones."
echo ""
echo "Consulta docs/guias/INSTALACION-PWA.md para más información."
echo ""

