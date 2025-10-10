#!/bin/bash
# Script de inicio para desarrollo Linux/Mac - StudentsPoint

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   StudentsPoint - Modo Desarrollo${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Preguntar si limpiar cache
read -p "¿Limpiar cache y sesiones? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}[INFO]${NC} Limpiando cache de Django..."
    cd proyecto/src/backend
    python manage.py clearsessions 2>/dev/null || true
    python manage.py clear_cache 2>/dev/null || true
    if [ -f db.sqlite3 ]; then
        echo -e "${YELLOW}[INFO]${NC} Eliminando base de datos de desarrollo..."
        rm db.sqlite3
    fi
    cd ../../..
fi

# Verificar Python
echo -e "${BLUE}[INFO]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python no encontrado"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Python encontrado: $(python3 --version)"
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo -e "${GREEN}[OK]${NC} Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${GREEN}[OK]${NC} Activando entorno virtual..."
    source .venv/bin/activate
fi

cd proyecto/src/backend

# Instalar dependencias
echo -e "${BLUE}[INFO]${NC} Instalando dependencias..."
pip install -r requirements.txt -q
echo -e "${GREEN}[OK]${NC} Dependencias instaladas"
echo ""

# Verificar configuración
echo -e "${BLUE}[INFO]${NC} Verificando configuración..."
export DJANGO_SETTINGS_MODULE=studentspoint.settings.dev
python manage.py check
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Problemas de configuración"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Configuración correcta"
echo ""

# Aplicar migraciones
echo -e "${BLUE}[INFO]${NC} Aplicando migraciones..."
python manage.py migrate --run-syncdb
echo -e "${GREEN}[OK]${NC} Migraciones aplicadas"
echo ""

# Recolectar archivos estáticos
echo -e "${BLUE}[INFO]${NC} Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear
echo -e "${GREEN}[OK]${NC} Archivos estáticos actualizados"
echo ""

# Crear superusuario
echo -e "${BLUE}[INFO]${NC} Creando superusuario..."
python ensure_superuser.py 2>/dev/null || true
echo -e "${GREEN}[OK]${NC} Superusuario configurado"
echo ""

# Crear directorio de logs
mkdir -p logs
echo -e "${GREEN}[OK]${NC} Directorio de logs creado"

# Limpiar logs antiguos
echo -e "${BLUE}[INFO]${NC} Limpiando logs expirados..."
find logs/ -name "*.log" -size +50M -delete 2>/dev/null || true
echo -e "${GREEN}[OK]${NC} Logs listos"
echo ""

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}   SERVIDOR LISTO${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Aplicación: http://127.0.0.1:8000"
echo "Admin: http://127.0.0.1:8000/admin/"
echo "API Docs: http://127.0.0.1:8000/api/docs/"
echo ""
echo "Credenciales: admin@studentspoint.app / admin123"
echo ""
echo -e "${BLUE}[LOGS]${NC} Sistema de logging activo en: logs/"
echo "  - general.log: Todos los eventos"
echo "  - errors.log: Solo errores"
echo "  - api.log: Peticiones API"
echo "  - auth.log: Autenticación"
echo ""

# Preguntar si iniciar monitor
read -p "¿Iniciar monitor de logs en otra terminal? (S/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    # Intentar abrir en nueva terminal según el entorno
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && python monitor_logs.py --interval 30; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd $(pwd) && python monitor_logs.py --interval 30; bash" &
    elif command -v konsole &> /dev/null; then
        konsole -e "cd $(pwd) && python monitor_logs.py --interval 30; bash" &
    else
        # Iniciar en background
        nohup python monitor_logs.py --interval 60 > /tmp/monitor_logs.out 2>&1 &
        MONITOR_PID=$!
        echo -e "${GREEN}[OK]${NC} Monitor de logs iniciado en background (PID: $MONITOR_PID)"
        echo "Ver logs del monitor: tail -f /tmp/monitor_logs.out"
    fi
fi

echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar servidor
sleep 2
python manage.py runserver 127.0.0.1:8000

