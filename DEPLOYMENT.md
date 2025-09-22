# 🚀 Guía de Despliegue - StudentsPoint

Esta guía te ayudará a desplegar StudentsPoint en diferentes entornos, desde desarrollo local hasta producción en servidores AMP.

## 📋 Tabla de Contenidos

- [Desarrollo Local](#desarrollo-local)
- [Despliegue en Servidor AMP](#despliegue-en-servidor-amp)
- [Configuración de Base de Datos](#configuración-de-base-de-datos)
- [Configuración de Servicios Externos](#configuración-de-servicios-externos)
- [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
- [Solución de Problemas](#solución-de-problemas)

## 🏠 Desarrollo Local

### Prerrequisitos
- Python 3.11+
- Git
- SQLite (incluido con Python)

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/JackStar6677-1/students-point.git
cd students-point

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
cd proyecto/src/backend
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 5. Iniciar servidor
python manage.py runserver
```

### Acceso
- **Aplicación**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/

## 🌐 Despliegue en Servidor AMP

### Opción 1: Despliegue Manual

#### 1. Preparar Servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server nginx git -y

# Crear usuario para la aplicación
sudo adduser studentspoint
sudo usermod -aG sudo studentspoint
```

#### 2. Configurar Base de Datos PostgreSQL
```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE studentspoint_prod;
CREATE USER studentspoint WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE studentspoint_prod TO studentspoint;
ALTER USER studentspoint CREATEDB;
\q

# Configurar PostgreSQL
sudo nano /etc/postgresql/14/main/postgresql.conf
# Buscar y descomentar: listen_addresses = 'localhost'

sudo nano /etc/postgresql/14/main/pg_hba.conf
# Agregar: local   studentspoint_prod   studentspoint   md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

#### 3. Desplegar Aplicación
```bash
# Cambiar a usuario de la aplicación
sudo su - studentspoint

# Clonar repositorio
git clone https://github.com/JackStar6677-1/students-point.git
cd students-point

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
cd proyecto/src/backend
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar variables de entorno
cp env.production.example .env
nano .env
```

#### 4. Configurar Variables de Entorno (.env)
```env
# Configuración básica
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro-aqui
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip-servidor

# Base de datos
DATABASE_URL=postgresql://studentspoint:tu_password_seguro@localhost:5432/studentspoint_prod

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Google OAuth (opcional)
GOOGLE_OAUTH_CLIENT_ID=tu_client_id
GOOGLE_OAUTH_CLIENT_SECRET=tu_client_secret

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
EMAIL_USE_TLS=True

# Redis
REDIS_URL=redis://localhost:6379/0

# SSL (recomendado)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

#### 5. Configurar Aplicación
```bash
# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser

# Crear archivo de configuración Gunicorn
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
max_requests = 1000
max_requests_jitter = 100
preload_app = True
worker_class = "sync"
worker_connections = 1000
keepalive = 2
EOF
```

#### 6. Configurar Systemd Service
```bash
# Crear servicio
sudo nano /etc/systemd/system/studentspoint.service
```

```ini
[Unit]
Description=StudentsPoint Django App
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=studentspoint
Group=studentspoint
WorkingDirectory=/home/studentspoint/students-point/proyecto/src/backend
Environment="PATH=/home/studentspoint/students-point/venv/bin"
ExecStart=/home/studentspoint/students-point/venv/bin/gunicorn --config gunicorn.conf.py studentspoint.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### 7. Configurar Nginx
```bash
# Crear configuración de sitio
sudo nano /etc/nginx/sites-available/studentspoint
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # Certificados SSL (usar Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Headers de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Archivos estáticos
    location /static/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Archivos multimedia
    location /media/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Aplicación principal
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/studentspoint /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 8. Iniciar Servicios
```bash
# Iniciar servicios
sudo systemctl daemon-reload
sudo systemctl enable studentspoint
sudo systemctl start studentspoint
sudo systemctl enable redis
sudo systemctl start redis

# Verificar estado
sudo systemctl status studentspoint
sudo systemctl status redis
sudo systemctl status nginx
```

### Opción 2: Despliegue con Docker

#### 1. Crear Dockerfile de Producción
```dockerfile
# Dockerfile.prod
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copiar código de la aplicación
COPY . .

# Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "studentspoint.wsgi:application"]
```

#### 2. Crear docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: studentspoint_prod
      POSTGRES_USER: studentspoint
      POSTGRES_PASSWORD: tu_password_seguro
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=postgresql://studentspoint:tu_password_seguro@db:5432/studentspoint_prod
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn --bind 0.0.0.0:8000 --workers 3 studentspoint.wsgi:application"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### 3. Desplegar con Docker
```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ejecutar comandos de Django
docker-compose exec web python manage.py createsuperuser
```

## 🔧 Configuración de Servicios Externos

### Google OAuth 2.0

#### 1. Crear Proyecto en Google Cloud Console
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar Google+ API
4. Ir a "Credenciales" → "Crear credenciales" → "ID de cliente OAuth 2.0"

#### 2. Configurar URIs de Redirección
```
http://localhost:8000/api/auth/google/callback/web/
http://127.0.0.1:8000/api/auth/google/callback/web/
https://tu-dominio.com/api/auth/google/callback/web/
```

#### 3. Configurar Variables de Entorno
```env
GOOGLE_OAUTH_CLIENT_ID=tu_client_id_aqui
GOOGLE_OAUTH_CLIENT_SECRET=tu_client_secret_aqui
```

### Notificaciones Push (Opcional)

#### 1. Generar VAPID Keys
```bash
python -c "from pywebpush import webpush; print(webpush.generate_vapid_keys())"
```

#### 2. Configurar Variables de Entorno
```env
VAPID_PUBLIC_KEY=tu_public_key_aqui
VAPID_PRIVATE_KEY=tu_private_key_aqui
VAPID_CLAIMS={"sub": "mailto:admin@tu-dominio.com"}
```

### Email (Opcional)

#### Configuración Gmail
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
EMAIL_USE_TLS=True
```

**Nota**: Usar App Password de Gmail, no la contraseña normal.

## 📊 Monitoreo y Mantenimiento

### Logs del Sistema
```bash
# Logs de la aplicación
sudo journalctl -u studentspoint -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Comandos de Mantenimiento
```bash
# Reiniciar aplicación
sudo systemctl restart studentspoint

# Actualizar código
cd /home/studentspoint/students-point
git pull origin main
sudo systemctl restart studentspoint

# Backup de base de datos
pg_dump -h localhost -U studentspoint studentspoint_prod > backup_$(date +%Y%m%d).sql

# Limpiar logs antiguos
sudo journalctl --vacuum-time=7d
```

### Monitoreo de Recursos
```bash
# Uso de CPU y memoria
htop

# Espacio en disco
df -h

# Conexiones de red
netstat -tulpn

# Procesos de Python
ps aux | grep python
```

## 🔍 Solución de Problemas

### Problemas Comunes

#### 1. Error de Base de Datos
```bash
# Verificar conexión
psql -h localhost -U studentspoint -d studentspoint_prod

# Verificar logs
sudo journalctl -u studentspoint | grep -i error
```

#### 2. Error de Archivos Estáticos
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R studentspoint:studentspoint /home/studentspoint/students-point/proyecto/src/backend/staticfiles/
```

#### 3. Error de CORS
```bash
# Verificar configuración CORS
grep -r "CORS" /home/studentspoint/students-point/proyecto/src/backend/studentspoint/settings/
```

#### 4. Error de SSL
```bash
# Verificar certificados
sudo certbot certificates

# Renovar certificados
sudo certbot renew
```

### Comandos de Diagnóstico
```bash
# Verificar estado de servicios
sudo systemctl status studentspoint nginx postgresql redis

# Verificar puertos
sudo netstat -tulpn | grep -E ':(80|443|8000|5432|6379)'

# Verificar logs de error
sudo journalctl -u studentspoint --since "1 hour ago" | grep -i error
```

## 📞 Soporte

### Recursos de Ayuda
- **Documentación**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/JackStar6677-1/students-point/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JackStar6677-1/students-point/discussions)
- **Email**: admin@studentspoint.app

### Información para Reportar Problemas
Al reportar un problema, incluye:
- Versión de Python
- Sistema operativo
- Logs de error completos
- Pasos para reproducir
- Configuración de variables de entorno (sin credenciales)

---

**🎓 StudentsPoint** - *Despliegue exitoso garantizado*

*Última actualización: Septiembre 2024*
