# Guía de Despliegue para Servidor Linux (CubeCoders AMP)

## Requisitos del Servidor

### Software Necesario
- Python 3.11+ 
- PostgreSQL 12+
- Git
- Nginx (opcional, para servir archivos estáticos)

### Variables de Entorno Requeridas

Crear archivo `.env` en el directorio del proyecto con:

```bash
# Base de datos PostgreSQL
DB_NAME=studentspoint_prod
DB_USER=postgres
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432

# Email SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=noreply@studentspoint.app

# Google OAuth
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret

# Dominio
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Seguridad (para producción con HTTPS)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

## Pasos de Despliegue

### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib git nginx -y

# Crear usuario para la aplicación
sudo adduser studentspoint
sudo usermod -aG sudo studentspoint
```

### 2. Configurar PostgreSQL

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE studentspoint_prod;
CREATE USER studentspoint_user WITH PASSWORD 'password_seguro';
GRANT ALL PRIVILEGES ON DATABASE studentspoint_prod TO studentspoint_user;
\q
```

### 3. Clonar y Configurar la Aplicación

```bash
# Cambiar al usuario de la aplicación
sudo su - studentspoint

# Clonar el repositorio
git clone https://github.com/tu-usuario/students-point.git
cd students-point

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r proyecto/src/backend/requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Crear archivo .env
nano .env
# Pegar las variables de entorno listadas arriba
```

### 5. Ejecutar Despliegue

```bash
# Hacer ejecutable el script
chmod +x deploy_linux.sh

# Ejecutar despliegue
./deploy_linux.sh
```

### 6. Configurar Servicio del Sistema (Opcional)

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/studentspoint.service

# Contenido del archivo:
[Unit]
Description=StudentsPoint Django App
After=network.target

[Service]
User=studentspoint
Group=studentspoint
WorkingDirectory=/home/studentspoint/students-point
Environment=PATH=/home/studentspoint/students-point/venv/bin
ExecStart=/home/studentspoint/students-point/venv/bin/python proyecto/src/backend/manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target

# Habilitar y iniciar servicio
sudo systemctl enable studentspoint
sudo systemctl start studentspoint
sudo systemctl status studentspoint
```

### 7. Configurar Nginx (Opcional)

```bash
# Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/studentspoint

# Contenido:
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location /static/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/staticfiles/;
    }

    location /media/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/studentspoint /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Comandos Útiles

### Actualizar Aplicación
```bash
cd /home/studentspoint/students-point
git pull origin main
./deploy_linux.sh
```

### Ver Logs
```bash
# Logs del servicio
sudo journalctl -u studentspoint -f

# Logs de Django
tail -f /home/studentspoint/students-point/proyecto/src/backend/logs/django.log
```

### Reiniciar Servicio
```bash
sudo systemctl restart studentspoint
sudo systemctl restart nginx
```

### Backup de Base de Datos
```bash
sudo -u postgres pg_dump studentspoint_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Solución de Problemas

### Error de Permisos
```bash
sudo chown -R studentspoint:studentspoint /home/studentspoint/students-point
```

### Error de Base de Datos
```bash
# Verificar conexión
sudo -u postgres psql -d studentspoint_prod -c "SELECT 1;"
```

### Error de Archivos Estáticos
```bash
cd /home/studentspoint/students-point/proyecto/src/backend
python manage.py collectstatic --noinput
```

## Notas Importantes

1. **Seguridad**: Cambiar todas las contraseñas por defecto
2. **HTTPS**: Configurar certificado SSL para producción
3. **Firewall**: Configurar reglas de firewall apropiadas
4. **Backups**: Implementar backups automáticos de la base de datos
5. **Monitoreo**: Configurar monitoreo del servidor y aplicación