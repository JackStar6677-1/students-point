#!/bin/bash
# Script de despliegue para servidor Linux (CubeCoders AMP)

echo "=== Despliegue StudentsPoint ==="

# Verificar que estamos en el directorio correcto
if [ ! -f "proyecto/src/backend/manage.py" ]; then
    echo "ERROR: No se encontró manage.py. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

# Actualizar código desde Git
echo "Actualizando código desde Git..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "ERROR: Error actualizando código desde Git"
    exit 1
fi

# Activar entorno virtual (ajustar ruta según configuración)
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "WARNING: No se encontró entorno virtual. Usando Python del sistema."
fi

# Navegar al directorio backend
cd proyecto/src/backend

# Instalar/actualizar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Error instalando dependencias"
    exit 1
fi

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Error aplicando migraciones"
    exit 1
fi

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "ERROR: Error recolectando archivos estáticos"
    exit 1
fi

# Limpiar cache
echo "Limpiando cache..."
python manage.py clear_cache
python manage.py clearsessions

# Verificar configuración
echo "Verificando configuración..."
python manage.py check --deploy
if [ $? -ne 0 ]; then
    echo "WARNING: Problemas de configuración detectados"
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Reiniciar servicio (descomentar y ajustar según configuración del servidor)
# echo "Reiniciando servicio..."
# sudo systemctl restart studentspoint
# sudo systemctl restart nginx

echo "=== Despliegue completado ==="
echo "Servidor: http://tu-dominio.com"
echo "Admin: http://tu-dominio.com/admin/"
echo "API Docs: http://tu-dominio.com/api/docs/"
echo ""
echo "NOTA: Asegúrate de configurar las variables de entorno:"
echo "- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT"
echo "- EMAIL_HOST_USER, EMAIL_HOST_PASSWORD"
echo "- GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET"
echo "- ALLOWED_HOSTS"
