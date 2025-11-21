# 🚀 Stack Tecnológico Completo - StudentsPoint

## 📋 Resumen Ejecutivo

StudentsPoint utiliza un stack tecnológico moderno y robusto compuesto por:

- **Backend**: Django 5.2 + Django REST Framework
- **Servidor WSGI**: Gunicorn (producción)
- **Reverse Proxy**: Nginx (producción)
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Cache/Broker**: Redis
- **Tareas Asíncronas**: Celery
- **Frontend**: HTML5 + CSS3 + JavaScript (PWA)

---

## 🎯 Stack Completo por Capa

### 1. Frontend (Cliente)

```
┌─────────────────────────────────────────┐
│          NAVEGADOR (Cliente)            │
│  ┌───────────────────────────────────┐  │
│  │  HTML5 + CSS3 + JavaScript ES6+   │  │
│  │  - Bootstrap 5.3.2                │  │
│  │  - Font Awesome 6.5.1             │  │
│  │  - Service Worker (PWA)           │  │
│  │  - API Services (fetch)           │  │
│  │  - JWT Authentication             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓ HTTP/HTTPS + JSON
```

**Tecnologías Frontend:**
- HTML5, CSS3, JavaScript ES6+
- Bootstrap 5.3.2 (UI Framework)
- Font Awesome 6.5.1 (Iconos)
- PWA (Progressive Web App)
- Service Worker (offline support)
- Retell AI (Bot conversacional)

---

### 2. Servidor Web (Reverse Proxy)

```
┌─────────────────────────────────────────┐
│               NGINX                     │
│  - Reverse Proxy                        │
│  - Static Files Server                  │
│  - SSL/TLS Termination                  │
│  - Load Balancing                       │
│  - Compression (gzip)                   │
│  - Rate Limiting                        │
└─────────────────────────────────────────┘
              ↓ Unix Socket / TCP
```

**Nginx Version:** Latest stable
**Puerto:** 80 (HTTP) / 443 (HTTPS)
**Función Principal:** Reverse proxy hacia Gunicorn

---

### 3. Servidor de Aplicación (WSGI)

```
┌─────────────────────────────────────────┐
│             GUNICORN                    │
│  - WSGI HTTP Server                     │
│  - Workers: 4 (sync)                    │
│  - Timeout: 60s                         │
│  - Binding: Unix Socket                 │
│  - Graceful Restart                     │
└─────────────────────────────────────────┘
              ↓
```

**Gunicorn Version:** 21.2+
**Workers:** 4 procesos síncronos
**Worker Class:** sync
**Conexión:** Unix socket (más rápido que TCP)

---

### 4. Aplicación Backend

```
┌─────────────────────────────────────────┐
│         DJANGO 5.2                      │
│  ┌───────────────────────────────────┐  │
│  │  Django REST Framework 3.15+      │  │
│  │  - ViewSets & Serializers         │  │
│  │  - JWT Authentication             │  │
│  │  - Permissions & Throttling       │  │
│  │  - API Documentation (drf-spec)   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Backend Frameworks:**
- Django 5.2
- Django REST Framework 3.15+
- djangorestframework-simplejwt 5.3+
- django-cors-headers 4.4+
- drf-spectacular 0.27+ (docs API)

---

### 5. Base de Datos

```
┌─────────────────────────────────────────┐
│        DESARROLLO: SQLite               │
│        PRODUCCIÓN: PostgreSQL 15+       │
│  - ORM: Django ORM                      │
│  - Migraciones automáticas              │
│  - Índices optimizados                  │
└─────────────────────────────────────────┘
```

**Base de Datos:**
- **Desarrollo**: SQLite (archivo local)
- **Producción**: PostgreSQL 15+
- **Driver**: psycopg2-binary 2.9+

---

### 6. Cache y Message Broker

```
┌─────────────────────────────────────────┐
│              REDIS 5.0+                 │
│  - Cache de sesiones                    │
│  - Broker para Celery                   │
│  - Result backend                       │
│  - Pub/Sub (futuro)                     │
└─────────────────────────────────────────┘
```

**Redis:**
- Version: 5.0+
- django-redis: 5.4+
- redis-py: 5.0+

---

### 7. Tareas Asíncronas

```
┌─────────────────────────────────────────┐
│            CELERY 5.4+                  │
│  - Worker processes                     │
│  - Beat scheduler                       │
│  - Task queue                           │
│  - Result backend (Redis)               │
└─────────────────────────────────────────┘
```

**Celery:**
- Celery: 5.4+
- django-celery-beat: 2.5+
- django-celery-results: 2.5+

---

## 🔧 Arquitectura Gunicorn + Nginx

### ¿Cómo Funciona?

```
┌────────────────────────────────────────────────────────────┐
│                    FLUJO DE REQUEST                        │
└────────────────────────────────────────────────────────────┘

1. Cliente/Navegador
        ↓ HTTP/HTTPS Request
        
2. NGINX (Puerto 80/443)
   ├─→ Archivos estáticos (/static/) → Servidos directamente
   ├─→ Archivos media (/media/) → Servidos directamente
   └─→ Requests dinámicos → Proxy Pass
        ↓ Unix Socket
        
3. GUNICORN (Unix Socket)
   └─→ 4 Workers (procesos Python)
        ↓ WSGI Protocol
        
4. DJANGO Application
   └─→ Views → Services → Models → Database
        ↓ Response
        
5. Respuesta JSON → Gunicorn → Nginx → Cliente
```

---

## ⚙️ Configuración de Producción

### 1. Configuración de Nginx

**Archivo**: `/etc/nginx/sites-available/studentspoint`

```nginx
upstream studentspoint {
    # Conexión a Gunicorn via Unix Socket
    server unix:/home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name studentspoint.app www.studentspoint.app;

    # Tamaño máximo de upload
    client_max_body_size 20M;
    
    # Logs
    access_log /var/log/nginx/studentspoint_access.log;
    error_log /var/log/nginx/studentspoint_error.log;

    # Archivos estáticos (CSS, JS, imágenes)
    location /static/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Archivos media (uploads de usuarios)
    location /media/ {
        alias /home/studentspoint/students-point/proyecto/src/backend/media/;
        expires 7d;
    }

    # Proxy a Django/Gunicorn
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

    # Headers de seguridad
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

**¿Por qué Nginx?**
- ✅ Sirve archivos estáticos eficientemente (sin pasar por Django)
- ✅ Maneja SSL/TLS (HTTPS)
- ✅ Compresión gzip automática
- ✅ Rate limiting y protección DDoS
- ✅ Load balancing (múltiples instancias Gunicorn)
- ✅ Más rápido que servir directamente con Gunicorn

---

### 2. Configuración de Gunicorn

**Servicio Systemd**: `/etc/systemd/system/studentspoint-gunicorn.service`

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

**Socket Systemd**: `/etc/systemd/system/studentspoint-gunicorn.socket`

```ini
[Unit]
Description=StudentsPoint Gunicorn socket

[Socket]
ListenStream=/home/studentspoint/students-point/proyecto/src/backend/gunicorn.sock
SocketUser=www-data

[Install]
WantedBy=sockets.target
```

**Parámetros de Gunicorn Explicados:**

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `--workers` | 4 | Número de procesos worker (CPU cores * 2 + 1) |
| `--worker-class` | sync | Tipo de worker (sync, async, gevent) |
| `--bind` | unix:socket | Escucha en Unix socket (más rápido) |
| `--timeout` | 60 | Tiempo máximo de respuesta (segundos) |
| `--log-level` | info | Nivel de logging (debug, info, warning, error) |

**¿Por qué Gunicorn?**
- ✅ WSGI server estándar de Python
- ✅ Pre-fork worker model (múltiples procesos)
- ✅ Graceful restarts (sin downtime)
- ✅ Integración perfecta con Django
- ✅ Producción-ready y battle-tested
- ✅ Compatible con systemd (gestión de servicios)

---

### 3. Script de Inicio en Desarrollo/Producción

**Producción (Linux)**: `scripts/iniciar_produccion.sh`

```bash
#!/bin/bash

# Cargar entorno virtual
source venv/bin/activate

# Variables de entorno
export DJANGO_SETTINGS_MODULE=studentspoint.settings.prod

# Migrar base de datos
python manage.py migrate

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar con Gunicorn
gunicorn studentspoint.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 60 \
    --access-logfile logs/gunicorn_access.log \
    --error-logfile logs/gunicorn_error.log \
    --log-level info \
    --capture-output
```

**Producción (Windows)**: `scripts/iniciar_produccion.bat`

```batch
@echo off
call venv\Scripts\activate
set DJANGO_SETTINGS_MODULE=studentspoint.settings.prod

python manage.py migrate
python manage.py collectstatic --noinput

waitress-serve --port=8000 studentspoint.wsgi:application
```

> **Nota**: En Windows se usa `waitress` en lugar de Gunicorn (no soportado en Windows)

---

## 🔐 SSL/TLS (HTTPS)

### Certificado Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado automáticamente
sudo certbot --nginx -d studentspoint.app -d www.studentspoint.app

# Renovación automática (cron)
sudo certbot renew --dry-run
```

**Nginx con SSL:**

```nginx
server {
    listen 443 ssl http2;
    server_name studentspoint.app www.studentspoint.app;

    # Certificados SSL
    ssl_certificate /etc/letsencrypt/live/studentspoint.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/studentspoint.app/privkey.pem;
    
    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... resto de configuración
}

# Redirect HTTP → HTTPS
server {
    listen 80;
    server_name studentspoint.app www.studentspoint.app;
    return 301 https://$server_name$request_uri;
}
```

---

## 📦 Dependencias Completas

### Backend (Python)

```txt
# Core Framework
Django>=5.0,<6.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
drf-spectacular>=0.27

# Database
psycopg2-binary>=2.9  # PostgreSQL

# Server
gunicorn>=21.2  # WSGI Server (Linux/Mac)
waitress>=2.1   # WSGI Server (Windows)

# Cache & Queue
redis>=5.0
django-redis>=5.4
celery>=5.4
django-celery-beat>=2.5
django-celery-results>=2.5

# Security & Auth
python-dotenv>=1.0
django-cors-headers>=4.4

# File Processing
Pillow>=10.0
PyPDF2>=3.0
reportlab>=4.0
python-docx>=1.1.0

# Web Scraping & Requests
beautifulsoup4>=4.12
requests>=2.31

# Google OAuth
google-auth>=2.40
google-auth-oauthlib>=1.2

# Push Notifications
pywebpush>=1.14

# Testing
pytest>=8.0
pytest-django>=4.8

# Utilities
pytz>=2024.1
markdown>=3.4
```

### Frontend (CDN)

```html
<!-- Bootstrap 5.3.2 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Font Awesome 6.5.1 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- Retell AI Bot -->
<script src="https://dashboard.retellai.com/retell-widget.js" type="module"></script>
```

---

## 🚀 Proceso de Despliegue

### Workflow de Producción

```
┌─────────────────────────────────────────┐
│  1. Desarrollo Local                    │
│     - Django runserver                  │
│     - SQLite                            │
│     - DEBUG=True                        │
└──────────────┬──────────────────────────┘
               │ git push
┌──────────────▼──────────────────────────┐
│  2. Repositorio Git                     │
│     - GitHub/GitLab                     │
└──────────────┬──────────────────────────┘
               │ git pull (servidor)
┌──────────────▼──────────────────────────┐
│  3. Servidor Producción                 │
│     ├─→ Activar venv                    │
│     ├─→ pip install -r requirements.txt │
│     ├─→ python manage.py migrate        │
│     ├─→ python manage.py collectstatic  │
│     ├─→ sudo systemctl restart gunicorn │
│     └─→ sudo systemctl restart nginx    │
└─────────────────────────────────────────┘
```

### Comandos de Despliegue

```bash
# 1. En el servidor
cd /home/studentspoint/students-point
git pull origin main

# 2. Activar entorno
cd proyecto/src/backend
source venv/bin/activate

# 3. Actualizar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
export DJANGO_SETTINGS_MODULE=studentspoint.settings.prod
python manage.py migrate

# 5. Colectar estáticos
python manage.py collectstatic --noinput

# 6. Reiniciar servicios
sudo systemctl restart studentspoint-gunicorn
sudo systemctl restart nginx

# 7. Verificar estado
sudo systemctl status studentspoint-gunicorn
sudo tail -f logs/gunicorn_error.log
```

---

## 📊 Monitoreo y Logs

### Archivos de Log

```
logs/
├── django/
│   ├── general.log      # Logs generales de Django
│   ├── errors.log       # Solo errores
│   ├── api.log          # Requests a la API
│   └── auth.log         # Login/registro
├── gunicorn/
│   ├── access.log       # Requests a Gunicorn
│   └── error.log        # Errores de Gunicorn
└── nginx/
    ├── access.log       # Requests a Nginx
    └── error.log        # Errores de Nginx
```

### Comandos de Monitoreo

```bash
# Ver logs en tiempo real
tail -f logs/gunicorn_error.log
tail -f /var/log/nginx/error.log

# Ver logs de systemd
sudo journalctl -u studentspoint-gunicorn -f

# Ver estado de servicios
sudo systemctl status studentspoint-gunicorn
sudo systemctl status nginx
sudo systemctl status redis
sudo systemctl status postgresql

# Verificar conexiones
sudo netstat -tulpn | grep :80    # Nginx
sudo ss -lptn | grep gunicorn     # Gunicorn socket
```

---

## 🔥 Optimizaciones de Producción

### 1. Nginx

```nginx
# Compresión gzip
gzip on;
gzip_vary on;
gzip_types text/plain text/css text/xml text/javascript 
           application/json application/javascript application/xml+rss;

# Cache de archivos estáticos
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Límite de rate (anti DDoS)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

### 2. Gunicorn

```bash
# Calcular workers óptimos
# Formula: (2 x CPU cores) + 1
# Para 4 cores: (2 x 4) + 1 = 9 workers

gunicorn --workers 9 \
         --worker-class gevent \  # Para I/O intensivo
         --worker-connections 1000
```

### 3. Django Settings

```python
# settings/prod.py

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Sessions en Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Static files CDN (futuro)
# STATIC_URL = 'https://cdn.studentspoint.app/static/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 🐳 Docker (Alternativa)

También se puede desplegar con Docker:

```dockerfile
# Dockerfile.prod
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", 
     "--workers", "3", 
     "studentspoint.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn studentspoint.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./static:/app/static
      - ./media:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/static
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: studentspoint_prod
      POSTGRES_USER: studentspoint_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## 📈 Resumen del Stack

| Componente | Tecnología | Función |
|------------|------------|---------|
| **Frontend** | HTML/CSS/JS + Bootstrap | Interfaz de usuario |
| **PWA** | Service Worker | Funcionalidad offline |
| **Reverse Proxy** | Nginx | Servidor web, SSL, static files |
| **App Server** | Gunicorn | WSGI server para Django |
| **Backend** | Django 5.2 | Framework principal |
| **API** | Django REST Framework | Endpoints REST |
| **Auth** | JWT (Simple JWT) | Autenticación sin estado |
| **Database** | PostgreSQL | Base de datos relacional |
| **Cache** | Redis | Cache y message broker |
| **Queue** | Celery | Tareas asíncronas |
| **SSL** | Let's Encrypt | Certificados HTTPS |
| **Deploy** | Systemd + Git | Gestión de servicios |

---

## ✅ Checklist de Producción

- [x] Gunicorn instalado y configurado
- [x] Nginx como reverse proxy
- [x] PostgreSQL como base de datos
- [x] Redis para cache y Celery
- [x] SSL/TLS con Let's Encrypt
- [x] Systemd services configurados
- [x] Logs rotados automáticamente
- [x] DEBUG=False en producción
- [x] ALLOWED_HOSTS configurados
- [x] SECRET_KEY seguro (no en código)
- [x] Archivos estáticos en /static/
- [x] Media files en /media/
- [x] Backup automático de BD
- [ ] CDN para archivos estáticos (futuro)
- [ ] Monitoring con Prometheus (futuro)

---

**Última actualización**: Noviembre 2025  
**Stack Version**: Django 5.2 + Gunicorn 21.2 + Nginx Latest  
**Estado**: ✅ Producción activa

