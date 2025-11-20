#!/bin/bash
# Script de inicio automático para StudentsPoint - Desarrollo
# Ejecutar con: ./iniciar_desarrollo.sh o doble click (si está configurado)

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Cambiar al directorio del script
cd "$(dirname "$0")"

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   StudentsPoint - Modo Desarrollo${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Verificar Python
echo -e "${BLUE}[1/8]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Python no encontrado. Instala Python 3.11+"
        echo "Presiona Enter para salir..."
        read
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi
echo -e "${GREEN}[OK]${NC} Python encontrado: $($PYTHON_CMD --version)"
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo -e "${GREEN}[INFO]${NC} Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${GREEN}[INFO]${NC} Activando entorno virtual..."
    source .venv/bin/activate
fi

# Navegar al directorio backend
echo -e "${BLUE}[2/8]${NC} Cambiando al directorio backend..."
cd proyecto/src/backend
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} No se pudo acceder al directorio backend"
    echo "Asegurate de estar en la raiz del proyecto"
    read
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Directorio backend encontrado"
echo ""

# Instalar dependencias
echo -e "${BLUE}[3/8]${NC} Instalando dependencias..."
pip install -r requirements.txt -q 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Algunas dependencias pueden no haberse instalado correctamente"
else
    echo -e "${GREEN}[OK]${NC} Dependencias instaladas"
fi
echo ""

# Verificar configuración
echo -e "${BLUE}[4/8]${NC} Verificando configuración..."
export DJANGO_SETTINGS_MODULE=studentspoint.settings.dev
$PYTHON_CMD manage.py check >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Hay advertencias en la configuración, continuando..."
else
    echo -e "${GREEN}[OK]${NC} Configuración correcta"
fi
echo ""

# Aplicar migraciones
echo -e "${BLUE}[5/8]${NC} Aplicando migraciones..."
$PYTHON_CMD manage.py migrate --run-syncdb >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Error en migraciones, continuando..."
else
    echo -e "${GREEN}[OK]${NC} Migraciones aplicadas"
fi
echo ""

# Recolectar archivos estáticos
echo -e "${BLUE}[6/8]${NC} Recolectando archivos estáticos..."
$PYTHON_CMD manage.py collectstatic --noinput >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Error recolectando estáticos, continuando..."
else
    echo -e "${GREEN}[OK]${NC} Archivos estáticos actualizados"
fi
echo ""

# Crear superusuario
echo -e "${BLUE}[7/8]${NC} Verificando superusuario..."
$PYTHON_CMD ensure_superuser.py >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Error creando superusuario, continuando..."
else
    echo -e "${GREEN}[OK]${NC} Superusuario configurado"
fi
echo ""

# Crear usuarios de prueba
echo "Creando usuarios de prueba..."
$PYTHON_CMD manage.py create_demo_users >/dev/null 2>&1
echo -e "${GREEN}[OK]${NC} Usuarios de prueba listos"
echo ""

# Crear directorio de logs
mkdir -p logs

# Limpiar logs expirados
find logs/ -name "*.log" -size +50M -delete 2>/dev/null || true

echo -e "${BLUE}[8/8]${NC} Preparación completada"
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
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Intentar abrir navegador automáticamente
sleep 3
if command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:8000 >/dev/null 2>&1 &
elif command -v open &> /dev/null; then
    open http://127.0.0.1:8000 >/dev/null 2>&1 &
fi

echo "Iniciando servidor Django..."
echo ""
$PYTHON_CMD manage.py runserver 127.0.0.1:8000

