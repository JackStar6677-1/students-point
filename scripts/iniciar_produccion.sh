#!/bin/bash
# Script de inicio para producción Linux - StudentsPoint

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   StudentsPoint - Modo Producción${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "proyecto/src/backend/manage.py" ]; then
    echo -e "${RED}[ERROR]${NC} No se encontró manage.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Cargar variables de entorno si existe .env
if [ -f "proyecto/.env" ]; then
    echo -e "${GREEN}[OK]${NC} Cargando variables de entorno..."
    set -a
    source proyecto/.env
    set +a
else
    echo -e "${YELLOW}[WARNING]${NC} No se encontró archivo .env"
fi

# Actualizar código desde Git (opcional)
read -p "¿Actualizar código desde Git? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}[INFO]${NC} Actualizando código desde Git..."
    git pull origin main
fi

# Activar entorno virtual
if [ -d "venv" ]; then
    echo -e "${GREEN}[OK]${NC} Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${GREEN}[OK]${NC} Activando entorno virtual..."
    source .venv/bin/activate
elif [ -d "proyecto/src/backend/venv" ]; then
    echo -e "${GREEN}[OK]${NC} Activando entorno virtual..."
    source proyecto/src/backend/venv/bin/activate
else
    echo -e "${YELLOW}[WARNING]${NC} No se encontró entorno virtual. Usando Python del sistema."
fi

# Navegar al directorio backend
cd proyecto/src/backend

# Instalar/actualizar dependencias
echo -e "${BLUE}[INFO]${NC} Instalando dependencias..."
pip install -r requirements.txt -q

# Verificar configuración
echo -e "${BLUE}[INFO]${NC} Verificando configuración..."
export DJANGO_SETTINGS_MODULE=studentspoint.settings.prod
python manage.py check --deploy
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Problemas de configuración detectados"
    exit 1
fi

# Aplicar migraciones
echo -e "${BLUE}[INFO]${NC} Aplicando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo -e "${BLUE}[INFO]${NC} Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear directorio de logs si no existe
mkdir -p logs
echo -e "${GREEN}[OK]${NC} Directorio de logs creado/verificado"

# Limpiar logs antiguos (mayores a 50MB)
echo -e "${BLUE}[INFO]${NC} Limpiando logs antiguos..."
find logs/ -name "*.log" -size +50M -delete 2>/dev/null || true
find logs/ -name "*.log.*" -mtime +30 -delete 2>/dev/null || true

# Verificar que Gunicorn está instalado
if ! command -v gunicorn &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Gunicorn no encontrado. Instalando..."
    pip install gunicorn
fi

# Configurar variables de entorno para producción
export DJANGO_SETTINGS_MODULE=studentspoint.settings.prod
export PYTHONUNBUFFERED=1

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}   SERVIDOR LISTO PARA PRODUCCIÓN${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "Aplicación: http://$(hostname -I | awk '{print $1}'):8000"
echo -e "Admin: http://$(hostname -I | awk '{print $1}'):8000/admin/"
echo -e "API Docs: http://$(hostname -I | awk '{print $1}'):8000/api/docs/"
echo ""
echo -e "${BLUE}[LOGS]${NC} Sistema de logging activo en: logs/"
echo "  - general.log: Todos los eventos"
echo "  - errors.log: Solo errores"
echo "  - api.log: Peticiones API"
echo "  - auth.log: Autenticación"
echo ""

# Preguntar modo de inicio
echo "Opciones de inicio:"
echo "  1) Gunicorn (Producción - recomendado)"
echo "  2) Django runserver (Solo desarrollo)"
echo "  3) Con monitor de logs en segundo plano"
read -p "Selecciona opción (1-3): " -n 1 -r
echo ""

case $REPLY in
    1)
        echo -e "${GREEN}[OK]${NC} Iniciando con Gunicorn..."
        
        # Iniciar monitor de logs en background
        echo -e "${BLUE}[INFO]${NC} Iniciando monitor de logs en segundo plano..."
        nohup python monitor_logs.py --interval 60 > /tmp/monitor_logs.out 2>&1 &
        MONITOR_PID=$!
        echo -e "${GREEN}[OK]${NC} Monitor de logs iniciado (PID: $MONITOR_PID)"
        echo $MONITOR_PID > /tmp/studentspoint_monitor.pid
        
        # Iniciar sistema de alertas cada 5 minutos
        (while true; do
            python alert_system.py
            sleep 300
        done) > /tmp/alert_system.out 2>&1 &
        ALERT_PID=$!
        echo -e "${GREEN}[OK]${NC} Sistema de alertas iniciado (PID: $ALERT_PID)"
        echo $ALERT_PID > /tmp/studentspoint_alerts.pid
        
        echo ""
        echo -e "${GREEN}Iniciando Gunicorn...${NC}"
        echo "Presiona Ctrl+C para detener el servidor"
        echo ""
        
        # Trap para limpiar procesos al salir
        trap "echo ''; echo 'Deteniendo servicios...'; kill $MONITOR_PID $ALERT_PID 2>/dev/null; exit" INT TERM
        
        gunicorn studentspoint.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --worker-class sync \
            --timeout 60 \
            --access-logfile logs/gunicorn_access.log \
            --error-logfile logs/gunicorn_error.log \
            --log-level info \
            --capture-output
        ;;
    2)
        echo -e "${YELLOW}[WARNING]${NC} Modo desarrollo - No usar en producción"
        python manage.py runserver 0.0.0.0:8000
        ;;
    3)
        echo -e "${GREEN}[OK]${NC} Iniciando con monitor de logs en consola..."
        
        # Iniciar servidor en background
        echo -e "${BLUE}[INFO]${NC} Iniciando Gunicorn en segundo plano..."
        nohup gunicorn studentspoint.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --timeout 60 \
            --access-logfile logs/gunicorn_access.log \
            --error-logfile logs/gunicorn_error.log \
            --log-level info > /tmp/gunicorn.out 2>&1 &
        GUNICORN_PID=$!
        echo -e "${GREEN}[OK]${NC} Gunicorn iniciado (PID: $GUNICORN_PID)"
        echo $GUNICORN_PID > /tmp/studentspoint_gunicorn.pid
        
        # Iniciar sistema de alertas
        (while true; do
            python alert_system.py
            sleep 300
        done) > /tmp/alert_system.out 2>&1 &
        ALERT_PID=$!
        echo $ALERT_PID > /tmp/studentspoint_alerts.pid
        
        echo ""
        echo -e "${GREEN}Monitor de logs activo${NC}"
        echo "Presiona Ctrl+C para detener todos los servicios"
        echo ""
        
        # Trap para limpiar procesos al salir
        trap "echo ''; echo 'Deteniendo servicios...'; kill $GUNICORN_PID $ALERT_PID 2>/dev/null; exit" INT TERM
        
        # Mostrar monitor de logs en primer plano
        python monitor_logs.py --interval 30
        ;;
    *)
        echo -e "${RED}[ERROR]${NC} Opción inválida"
        exit 1
        ;;
esac

