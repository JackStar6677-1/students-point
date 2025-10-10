#  Guía de Deployment a Producción - StudentsPoint

## Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Preparación del Servidor](#preparación-del-servidor)
3. [Configuración de Base de Datos](#configuración-de-base-de-datos)
4. [Configuración de la Aplicación](#configuración-de-la-aplicación)
5. [Configuración de Nginx](#configuración-de-nginx)
6. [Configuración de SSL](#configuración-de-ssl)
7. [Servicios del Sistema](#servicios-del-sistema)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
9. [Backup y Recuperación](#backup-y-recuperación)
10. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

### Hardware Recomendado
- **CPU:** 2+ cores
- **RAM:** 4GB mínimo, 8GB recomendado
- **Disco:** 20GB+ SSD
- **Ancho de banda:** 100 Mbps

### Software
- **SO:** Ubuntu 22.04 LTS (recomendado)
- **Python:** 3.11+
- **PostgreSQL:** 15+
- **Redis:** 7+
- **Nginx:** 1.18+

---

## Preparación del Servidor

### 1. Actualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependencias

```bash
# Dependencias del sistema
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server nginx \
    git supervisor certbot python3-certbot-nginx

# Dependencias de compilación
sudo apt install -y build-essential libpq-dev python3-dev \
    libssl-dev libffi-dev
```

### 3. Crear Usuario de Aplicación

```bash
sudo useradd -m -s /bin/bash studentspoint
sudo su - studentspoint
```

---

## Configuración de Base de Datos

### 1. Configurar PostgreSQL

```bash
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE studentspoint_prod;
CREATE USER studentspoint_user WITH PASSWORD 'contraseña-segura';
ALTER ROLE studentspoint_user SET client_encoding TO 'utf8';
ALTER ROLE studentspoint_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE studentspoint_user SET timezone TO 'America/Santiago';
GRANT ALL PRIVILEGES ON DATABASE studentspoint_prod TO studentspoint_user;
\q
```

### 2. Configurar PostgreSQL para Conexiones

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Agregar:
local   studentspoint_prod   studentspoint_user   md5
```

```bash
sudo systemctl restart postgresql
```

### 3. Habilitar Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

---

## Configuración de la Aplicación

### 1. Clonar Repositorio

```bash
cd /home/studentspoint
git clone https://github.com/tu-usuario/students-point.git
cd students-point/proyecto/src/backend
```

### 2. Crear Entorno Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 4. Configurar Variables de Entorno

```bash
cp ../../../env.production.example .env
nano .env

# Completar con valores reales:
SECRET_KEY=... # Generar con: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
DEBUG=0
ALLOWED_HOSTS=tu-dominio.com
DB_PASSWORD=tu-contraseña-db
# ... etc
```

### 5. Ejecutar Migraciones

```bash
export DJANGO_SETTINGS_MODULE=studentspoint.settings.prod
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## Configuración de Nginx

### 1. Crear Configuración

```bash
sudo nano /etc/nginx/sites-available/studentspoint
```

```nginx
upstream studentspoint {
    server unix:/home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name studentspoint.app www.studentspoint.app;

    client_max_body_size 20M;
    
    # Logs
    access_log /var/log/nginx/studentspoint_access.log;
    error_log /var/log/nginx/studentspoint_error.log;

    # Static files
    location /static/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/media/;
        expires 7d;
    }

    # Proxy to Django
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://studentspoint;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

### 2. Activar Sitio

```bash
sudo ln -s /etc/nginx/sites-available/studentspoint /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Configuración de SSL

### 1. Obtener Certificado (Let's Encrypt)

```bash
sudo certbot --nginx -d studentspoint.app -d www.studentspoint.app
```

### 2. Renovación Automática

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Servicios del Sistema

### 1. Gunicorn Service

```bash
sudo nano /etc/systemd/system/studentspoint-gunicorn.service
```

```ini
[Unit]
Description=StudentsPoint Gunicorn daemon
Requires=studentspoint-gunicorn.socket
After=network.target

[Service]
Type=notify
User=studentspoint
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/home/studentspoint/students-point/proyecto/src/backend
Environment="PATH=/home/studentspoint/students-point/proyecto/src/backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=studentspoint.settings.prod"
ExecStart=/home/studentspoint/students-point/proyecto/src/backend/venv/bin/gunicorn \
          --workers 4 \
          --worker-class sync \
          --bind unix:/home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock \
          --access-logfile /home/studentspoint/students-point/proyecto/src/backend/logs/gunicorn_access.log \
          --error-logfile /home/studentspoint/students-point/proyecto/src/backend/logs/gunicorn_error.log \
          --log-level info \
          studentspoint.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 2. Gunicorn Socket

```bash
sudo nano /etc/systemd/system/studentspoint-gunicorn.socket
```

```ini
[Unit]
Description=StudentsPoint Gunicorn socket

[Socket]
ListenStream=/home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock
SocketUser=www-data

[Install]
WantedBy=sockets.target
```

### 3. Celery Worker (Opcional)

```bash
sudo nano /etc/systemd/system/studentspoint-celery.service
```

```ini
[Unit]
Description=StudentsPoint Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=studentspoint
Group=studentspoint
WorkingDirectory=/home/studentspoint/students-point/proyecto/src/backend
Environment="PATH=/home/studentspoint/students-point/proyecto/src/backend/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=studentspoint.settings.prod"
ExecStart=/home/studentspoint/students-point/proyecto/src/backend/venv/bin/celery \
          -A studentspoint worker -l info --pidfile=/tmp/celery.pid
PIDFile=/tmp/celery.pid

[Install]
WantedBy=multi-user.target
```

### 4. Iniciar Servicios

```bash
sudo systemctl daemon-reload
sudo systemctl enable studentspoint-gunicorn.socket
sudo systemctl start studentspoint-gunicorn.socket
sudo systemctl enable studentspoint-gunicorn.service
sudo systemctl start studentspoint-gunicorn.service
```

### 5. Verificar Estado

```bash
sudo systemctl status studentspoint-gunicorn
sudo journalctl -u studentspoint-gunicorn -f
```

---

## Monitoreo y Mantenimiento

### 1. Script de Monitoreo

```bash
# Agregar a cron para monitoreo continuo
crontab -e

# Ejecutar cada 5 minutos
*/5 * * * * /home/studentspoint/students-point/proyecto/src/backend/venv/bin/python \
            /home/studentspoint/students-point/proyecto/src/backend/alert_system.py

# Análisis de logs diario
0 9 * * * /home/studentspoint/students-point/proyecto/src/backend/venv/bin/python \
          /home/studentspoint/students-point/proyecto/src/backend/analyze_logs.py \
          --export /home/studentspoint/daily_report.txt
```

### 2. Rotación de Logs

```bash
sudo nano /etc/logrotate.d/studentspoint
```

```
/home/studentspoint/students-point/proyecto/src/backend/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 studentspoint studentspoint
    sharedscripts
    postrotate
        systemctl reload studentspoint-gunicorn >/dev/null 2>&1 || true
    endscript
}
```

---

## Backup y Recuperación

### 1. Backup de Base de Datos

```bash
#!/bin/bash
# /home/studentspoint/backup_db.sh

BACKUP_DIR="/home/studentspoint/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="studentspoint_${DATE}.sql.gz"

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U studentspoint_user studentspoint_prod | gzip > "$BACKUP_DIR/$FILENAME"

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "studentspoint_*.sql.gz" -mtime +30 -delete

echo "Backup completado: $FILENAME"
```

```bash
chmod +x /home/studentspoint/backup_db.sh

# Agregar a cron (diario a las 2 AM)
0 2 * * * /home/studentspoint/backup_db.sh
```

### 2. Restaurar Backup

```bash
gunzip -c backup.sql.gz | psql -h localhost -U studentspoint_user studentspoint_prod
```

---

## Troubleshooting

### Problemas Comunes

#### 1. Error 502 Bad Gateway
```bash
# Verificar gunicorn
sudo systemctl status studentspoint-gunicorn
sudo journalctl -u studentspoint-gunicorn -n 50

# Verificar socket
ls -l /home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock
```

#### 2. Archivos Estáticos No Cargan
```bash
# Recolectar estáticos
python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R studentspoint:www-data staticfiles/
sudo chmod -R 755 staticfiles/
```

#### 3. Error de Base de Datos
```bash
# Verificar conexión
sudo -u postgres psql studentspoint_prod

# Ver logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

#### 4. Alto Uso de Memoria
```bash
# Reducir workers de gunicorn
# Editar /etc/systemd/system/studentspoint-gunicorn.service
# Cambiar --workers a 2 o 3
sudo systemctl daemon-reload
sudo systemctl restart studentspoint-gunicorn
```

### Comandos Útiles

```bash
# Reiniciar aplicación
sudo systemctl restart studentspoint-gunicorn

# Ver logs en tiempo real
sudo journalctl -u studentspoint-gunicorn -f

# Ver logs de nginx
sudo tail -f /var/log/nginx/studentspoint_error.log

# Verificar procesos
ps aux | grep gunicorn

# Verificar puertos
sudo netstat -tulpn | grep -E '80|443|8000'
```

---

## Checklist de Deployment

- [ ] Servidor preparado con todas las dependencias
- [ ] PostgreSQL configurado y funcionando
- [ ] Redis configurado y funcionando
- [ ] Variables de entorno configuradas
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Superusuario creado
- [ ] Nginx configurado y funcionando
- [ ] SSL configurado (Let's Encrypt)
- [ ] Servicios systemd configurados
- [ ] Gunicorn funcionando correctamente
- [ ] Logs configurados
- [ ] Backups automáticos configurados
- [ ] Monitoreo activo
- [ ] Alertas configuradas
- [ ] Pruebas de funcionamiento completadas

---

## Mantenimiento Regular

### Diario
- [ ] Revisar logs de errores
- [ ] Verificar alertas del sistema
- [ ] Monitorear uso de recursos

### Semanal
- [ ] Revisar backups
- [ ] Analizar métricas de rendimiento
- [ ] Actualizar dependencias de seguridad

### Mensual
- [ ] Revisar espacio en disco
- [ ] Optimizar base de datos (VACUUM, ANALYZE)
- [ ] Auditoría de seguridad
- [ ] Actualizar sistema operativo

---

**Documentación mantenida por:** Equipo StudentsPoint  
**Última actualización:** Octubre 2025

