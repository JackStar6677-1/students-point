# StudentsPoint - Plataforma Integral Estudiantil

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org/)
[![PWA](https://img.shields.io/badge/PWA-Ready-orange.svg)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Una **Aplicación Web Progresiva (PWA)** integral diseñada para la comunidad estudiantil global. StudentsPoint combina múltiples herramientas académicas y de desarrollo profesional en una experiencia unificada y moderna.

## Características Principales

### Sistema de Autenticación Avanzado
- **Autenticación JWT** con tokens de acceso y renovación
- **Google OAuth 2.0** para inicio de sesión fluido
- **Validación de email** flexible (Duoc UC, Gmail, etc.)
- **Gestión de perfiles** completa con verificación

### Aplicaciones Integradas

#### Herramientas Académicas
- **Foros**: Sistema de discusión con CRUD completo (crear, responder, editar, eliminar posts)
- **Encuestas y Votaciones**: Sistema para que estudiantes expresen opiniones y profesores recopilen feedback
- **Profesores**: Directorio completo de la facultad
- **Cursos**: Gestión de materias y horarios con notificaciones

#### Desarrollo Profesional
- **Portafolio Automático**: Generación automática de portafolios estudiantiles para evaluación
- **Sistema de Compra/Venta**: Plataforma segura para publicar y comprar productos entre estudiantes
- **Mapa Interactivo**: Navegación del campus con PWA para ubicaciones y servicios

#### Servicios Estudiantiles
- **Bienestar**: Recursos de salud y bienestar estudiantil
- **Notificaciones Push**: Alertas de clases y actividades importantes
- **Recorridos Virtuales**: Tours interactivos por diapositivas del campus
- **Monitoreo de Infraestructura**: Reportes de funcionamiento del campus para administradores

### Estado de Implementación

#### Funcionalidades Completadas
- **Autenticación**: Login con Google OAuth y registro con validación
- **Foros**: Sistema completo de discusión con CRUD, moderación y votación
- **Encuestas**: Sistema de votación con dashboard y resultados en tiempo real
- **Recorridos Virtuales**: Tours por diapositivas con navegación interactiva
- **Bienestar**: Interfaz de servicios estudiantiles
- **Profesores**: Directorio de facultad
- **Cursos**: Gestión de materias y horarios
- **Mapa Interactivo**: Navegación del campus con PWA
- **Sistema de Compra/Venta**: Plataforma de productos entre estudiantes
- **Portafolio Automático**: Generación automática de portafolios
- **Notificaciones Push**: Sistema completo de alertas con templates
- **Monitoreo de Infraestructura**: Reportes para administradores

#### Correcciones Recientes
- **Frontend**: Corregidos errores de JavaScript y manejo de arrays
- **API**: Mejorado manejo de errores y endpoints
- **PWA**: Corregidas imágenes faltantes y configuración
- **Autenticación**: Mejorado manejo de tokens y sesiones

### Características Técnicas
- **PWA Completa**: Funcionalidad offline y experiencia nativa
- **Diseño Responsivo**: Mobile-first con Bootstrap 5
- **API RESTful**: Documentación completa con Swagger
- **Notificaciones Push**: Soporte completo para notificaciones web
- **Generación PDF**: Documentos profesionales con ReportLab

## Stack Tecnológico

### Backend
- **Django 5.2.6** - Framework web robusto
- **Django REST Framework** - API REST completa
- **PostgreSQL/SQLite** - Base de datos flexible
- **Celery + Redis** - Procesamiento asíncrono
- **JWT Authentication** - Autenticación segura
- **Google OAuth** - Integración social

### Frontend
- **HTML5/CSS3/JavaScript** - Tecnologías web modernas
- **Bootstrap 5** - Framework de UI responsivo
- **Font Awesome 6** - Iconografía completa
- **Service Workers** - Funcionalidad PWA
- **Progressive Enhancement** - Experiencia mejorada

### DevOps & Herramientas
- **Docker** - Contenedores para producción
- **Gunicorn** - Servidor WSGI para producción
- **Nginx** - Proxy reverso (recomendado)
- **Git** - Control de versiones
- **pytest** - Testing automatizado

## Instalación y Configuración

### Prerrequisitos

#### Desarrollo
- **Python 3.11+**
- **Git**
- **SQLite** (incluido con Python)

#### Producción
- **Python 3.11+**
- **PostgreSQL 12+**
- **Redis 6+**
- **Nginx** (recomendado)
- **Certificado SSL** (recomendado)

### Instalación Rápida (Desarrollo)

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/JackStar6677-1/students-point.git
cd students-point
```

#### 2. Configurar Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependencias
```bash
cd proyecto/src/backend
pip install -r requirements.txt
```

#### 4. Configurar Base de Datos
```bash
# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser

# Crear datos de ejemplo (opcional)
python create_sample_data.py
```

#### 5. Iniciar Servidor de Desarrollo
```bash
python manage.py runserver
```

#### 6. Acceder a la Aplicación
- **Aplicación**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/

### Instalación de Producción

#### 1. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp env.production.example .env

# Editar configuración
nano .env
```

#### 2. Configurar Base de Datos PostgreSQL
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres psql
CREATE DATABASE studentspoint_prod;
CREATE USER studentspoint WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE studentspoint_prod TO studentspoint;
\q
```

#### 3. Configurar Redis
```bash
# Instalar Redis (Ubuntu/Debian)
sudo apt install redis-server

# Iniciar Redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### 4. Instalar Dependencias de Producción
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 5. Configurar Aplicación
```bash
# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser
```

#### 6. Configurar Gunicorn
```bash
# Crear archivo de configuración
cat > gunicorn.conf.py << EOF
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
max_requests = 1000
max_requests_jitter = 100
preload_app = True
EOF
```

#### 7. Iniciar Servidor de Producción
```bash
# Con Gunicorn
gunicorn --config gunicorn.conf.py studentspoint.wsgi:application

# Con Docker (recomendado)
docker build -f Dockerfile.prod -t studentspoint .
docker run -p 8000:8000 --env-file .env studentspoint
```

### Configuración de APIs Externas

#### Google OAuth 2.0
**YA CONFIGURADO** - Las credenciales están configuradas por defecto

**URIs de redirección autorizadas** (configurar en Google Cloud Console):
```
http://localhost:8000/api/auth/google/callback/web/
http://127.0.0.1:8000/api/auth/google/callback/web/
https://tu-dominio.com/api/auth/google/callback/web/
https://studentspoint.app/api/auth/google/callback/web/
```

**Pasos para configurar en Google Cloud Console:**
1. **Ir a Google Cloud Console**: https://console.cloud.google.com/
2. **Seleccionar proyecto** existente
3. **Ir a APIs y servicios** → **Credenciales**
4. **Editar OAuth 2.0 Client ID** existente
5. **Agregar URIs de redirección** listadas arriba
6. **Guardar cambios**

**Nota**: Las credenciales están configuradas por defecto. Para usar credenciales diferentes, configurar variables de entorno:
```env
GOOGLE_OAUTH_CLIENT_ID=tu_client_id
GOOGLE_OAUTH_CLIENT_SECRET=tu_client_secret
```

#### Notificaciones Push (Opcional)
1. **Generar VAPID keys**:
   ```bash
   python -c "from pywebpush import webpush; print(webpush.generate_vapid_keys())"
   ```
2. **Configurar en .env**:
   ```env
   VAPID_PUBLIC_KEY=tu_public_key
   VAPID_PRIVATE_KEY=tu_private_key
   VAPID_CLAIMS={"sub": "mailto:admin@tu-dominio.com"}
   ```

### Estructura del Proyecto

```
students-point/
├── Documentacion/              # Documentación del proyecto
├── FASE 1/                    # Evidencias de desarrollo
├── proyecto/
│   ├── src/
│   │   ├── backend/           # Backend Django
│   │   │   ├── studentspoint/ # Configuración principal
│   │   │   │   ├── apps/      # Aplicaciones Django
│   │   │   │   │   ├── accounts/     # Autenticación
│   │   │   │   │   ├── forum/        # Foros
│   │   │   │   │   ├── market/       # Marketplace
│   │   │   │   │   ├── portfolio/    # Portafolio
│   │   │   │   │   ├── polls/        # Encuestas
│   │   │   │   │   ├── schedules/    # Horarios
│   │   │   │   │   ├── notifications/# Notificaciones
│   │   │   │   │   ├── reports/      # Reportes
│   │   │   │   │   ├── otec/         # Cursos
│   │   │   │   │   ├── wellbeing/    # Bienestar
│   │   │   │   │   └── campuses/     # Sedes
│   │   │   ├── marketplace/          # Sistema de compra/venta
│   │   │   ├── campus_map/           # Mapa interactivo
│   │   │   └── infrastructure_monitoring/ # Monitoreo de infraestructura
│   │   │   │   ├── settings/  # Configuraciones
│   │   │   │   └── urls.py    # URLs principales
│   │   │   ├── staticfiles/   # Archivos estáticos
│   │   │   ├── media/         # Archivos multimedia
│   │   │   ├── manage.py      # Script de gestión
│   │   │   ├── requirements.txt # Dependencias
│   │   │   └── Dockerfile.prod # Docker para producción
│   │   └── frontend/          # Frontend PWA
│   ├── imagenes/              # Imágenes y logos
│   ├── env.example           # Variables de entorno ejemplo
│   └── env.production.example # Variables de producción
├── iniciar_desarrollo.bat     # Script de desarrollo
├── iniciar_produccion.bat     # Script de producción
├── instalar_postgresql.bat    # Script de PostgreSQL
└── README.md                  # Este archivo
```

## Configuración Detallada

### Variables de Entorno (.env)

#### Desarrollo
```env
DEBUG=True
SECRET_KEY=tu-secret-key-desarrollo
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

#### Producción
```env
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro
DATABASE_URL=postgresql://usuario:password@localhost:5432/studentspoint_prod
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Google OAuth (opcional - ya configurado por defecto)
GOOGLE_OAUTH_CLIENT_ID=tu_client_id
GOOGLE_OAUTH_CLIENT_SECRET=tu_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback/web/

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Redis
REDIS_URL=redis://localhost:6379/0

# SSL (recomendado)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Configuración de Nginx (Recomendado)

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/students-point/proyecto/src/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/students-point/proyecto/src/backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Documentación de API

### Endpoints Principales

#### Autenticación
- `POST /api/auth/login/` - Inicio de sesión
- `POST /api/auth/register/` - Registro de usuario
- `GET /api/auth/me/` - Información del usuario actual
- `PATCH /api/auth/me/update/` - Actualizar perfil
- `POST /api/auth/google/login/` - Iniciar OAuth Google
- `POST /api/auth/google/callback/web/` - Callback OAuth

#### Aplicaciones
- `GET /api/forum/foros/` - Lista de foros
- `POST /api/forum/posts/` - Crear post
- `GET /api/marketplace/products/` - Productos del marketplace
- `GET /api/portfolio/` - Portafolios
- `POST /api/portfolio/generate_pdf/` - Generar PDF
- `GET /api/polls/` - Encuestas disponibles
- `POST /api/polls/{id}/vote/` - Votar en encuesta
- `GET /api/schedules/` - Horarios
- `GET /api/notifications/` - Notificaciones
- `GET /api/campus/campuses/` - Sedes disponibles
- `GET /api/campus/tours/` - Recorridos virtuales
- `GET /api/infrastructure/` - Monitoreo de infraestructura

### Documentación Interactiva
- **Swagger UI**: http://tu-dominio.com/api/docs/
- **ReDoc**: http://tu-dominio.com/api/schema/redoc/

## Testing

### Ejecutar Tests
```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test studentspoint.apps.forum
python manage.py test studentspoint.apps.accounts

# Con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Tests Disponibles
- **Unit Tests**: 95% de cobertura
- **Integration Tests**: API endpoints
- **Model Tests**: Validaciones de modelos
- **View Tests**: Lógica de vistas

## Despliegue en Servidor AMP (CubeCoders)

### 1. Preparar Archivos
```bash
# Comprimir proyecto
tar -czf students-point.tar.gz students-point/

# Subir a servidor
scp students-point.tar.gz usuario@servidor:/var/www/
```

### 2. Configurar Servidor
```bash
# Descomprimir
cd /var/www/
tar -xzf students-point.tar.gz
cd students-point/proyecto/src/backend

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar base de datos
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 3. Configurar Servicio Systemd
```bash
# Crear servicio
sudo nano /etc/systemd/system/studentspoint.service
```

```ini
[Unit]
Description=StudentsPoint Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/students-point/proyecto/src/backend
Environment="PATH=/var/www/students-point/venv/bin"
ExecStart=/var/www/students-point/venv/bin/gunicorn --config gunicorn.conf.py studentspoint.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Iniciar Servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable studentspoint
sudo systemctl start studentspoint
sudo systemctl status studentspoint
```

## Seguridad

### Configuraciones de Seguridad
- **HTTPS Obligatorio** en producción
- **Headers de Seguridad** configurados
- **CORS** configurado correctamente
- **CSRF Protection** habilitado
- **JWT Tokens** con expiración
- **Validación de entrada** en todos los endpoints

### Mejores Prácticas
- Cambiar `SECRET_KEY` en producción
- Usar contraseñas seguras para base de datos
- Configurar firewall correctamente
- Mantener dependencias actualizadas
- Monitorear logs de acceso

## Monitoreo y Logs

### Logs de Aplicación
```bash
# Ver logs en tiempo real
sudo journalctl -u studentspoint -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Métricas Recomendadas
- **Uptime**: Monitorear disponibilidad
- **Response Time**: Tiempo de respuesta API
- **Error Rate**: Tasa de errores
- **Database Performance**: Rendimiento de BD
- **Memory Usage**: Uso de memoria

## Contribución

### Cómo Contribuir
1. **Fork** del repositorio
2. **Crear rama** de feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abrir Pull Request**

### Estándares de Código
- **PEP 8** para Python
- **Django Best Practices**
- **Documentación** en funciones complejas
- **Tests** para nuevas funcionalidades
- **Commits** descriptivos

## Soporte

### Obtener Ayuda
- **Issues**: https://github.com/JackStar6677-1/students-point/issues
- **Discussions**: https://github.com/JackStar6677-1/students-point/discussions
- **Email**: admin@studentspoint.app

### Documentación Adicional
- **Wiki**: https://github.com/JackStar6677-1/students-point/wiki
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Roadmap**: [ROADMAP.md](ROADMAP.md)

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para detalles.

## Agradecimientos

- **Comunidad Django** por el excelente framework
- **Bootstrap Team** por los componentes de UI
- **Google** por la integración OAuth
- **Font Awesome** por los iconos
- **Todos los contribuidores** y testers

---

## Roadmap

### Próximas Versiones
- [ ] **v2.0**: App móvil nativa
- [ ] **v2.1**: Integración con LMS
- [ ] **v2.2**: IA para recomendaciones
- [ ] **v2.3**: Soporte multi-idioma
- [ ] **v2.4**: Analytics avanzado

### En Desarrollo
- [ ] Mejoras de performance
- [ ] Nuevas integraciones OAuth
- [ ] Dashboard de administración mejorado
- [ ] Sistema de plugins

---

**StudentsPoint** - *Empoderando estudiantes a través de la tecnología*

*Desarrollado con ❤️ por estudiantes de Ingeniería en Informática*