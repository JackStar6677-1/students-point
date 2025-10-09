# StudentsPoint - Plataforma Integral Estudiantil

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Django](https://img.shields.io/badge/django-5.2-green)
![License](https://img.shields.io/badge/license-Open%20Source-blue)

## Descripcion

StudentsPoint es una plataforma web progresiva (PWA) integral diseñada para centralizar y mejorar la experiencia estudiantil. Ofrece herramientas academicas, de desarrollo profesional y de bienestar en una sola aplicacion.

**Proyecto de Capstone** - Ingenieria en Informatica, Duoc UC

## Caracteristicas Principales

### Sistema de Foros Avanzado
- Foros personalizados por carrera
- Restriccion de publicacion: usuarios solo pueden postear en el foro de su carrera
- Libertad de comentarios: usuarios pueden comentar en cualquier foro
- Tipos de publicaciones: comentarios, encuestas, imagenes, otros
- Censura automatica de contenido ofensivo
- Revision manual de imagenes por administradores
- Foros publicos y privados
- Sistema de moderacion automatica y manual

### Autenticacion y Usuarios
- Autenticacion dual: JWT + Google OAuth 2.0
- Registro tradicional con validacion de correo
- Sistema de roles: admin, moderador, director de carrera, estudiante
- Gestion de cambio de carrera con historial

### Otras Funcionalidades
- Marketplace estudiantil con integracion externa
- Portafolio profesional con generacion de PDF
- Recorridos virtuales 360° del campus
- Sistema de bienestar estudiantil
- Gestion de horarios de clases
- Cursos OTEC
- Sistema de encuestas
- Notificaciones push
- Sistema de reportes de infraestructura

## Stack Tecnologico

### Backend
- **Django 5.2** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos (produccion)
- **SQLite** - Base de datos (desarrollo)
- **Redis** - Cache y broker de mensajes
- **Celery** - Tareas asincronas
- **JWT** - Autenticacion con tokens

### Frontend
- **HTML5, CSS3, JavaScript ES6+** - Tecnologias base
- **Bootstrap 5** - Framework CSS
- **PWA** - Service Worker para funcionalidad offline
- **Font Awesome** - Iconos

## Instalacion

### Requisitos Previos
- Python 3.11+
- Git
- PostgreSQL (para produccion)

### Instalacion Rapida - Desarrollo

#### Windows
```bash
# Ejecutar el script de instalacion
iniciar_desarrollo.bat
```

#### Linux/Mac
```bash
# Clonar repositorio
git clone https://github.com/JackStar6677-1/students-point.git
cd students-point

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
cd proyecto/src/backend
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estaticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### Acceso

- **Aplicacion**: http://127.0.0.1:8000
- **Panel Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/

## Estructura del Proyecto

```
students-point/
├── Documentacion/           # Documentacion completa del proyecto
│   └── config-avanzada/     # Documentacion tecnica detallada
├── proyecto/
│   └── src/
│       ├── backend/         # Backend Django
│       │   └── studentspoint/
│       │       └── apps/    # Aplicaciones Django
│       │           ├── accounts/      # Autenticacion y usuarios
│       │           ├── forum/         # Sistema de foros
│       │           ├── market/        # Marketplace
│       │           ├── portfolio/     # Portafolios
│       │           ├── campuses/      # Recorridos campus
│       │           └── ...
│       └── frontend/        # Frontend (HTML/CSS/JS)
├── pruebas_unitarias/       # Tests unitarios con pytest
└── pruebas_automatizadas/   # Tests E2E
```

## Uso del Sistema de Foros

### Como Estudiante

**Crear una Publicacion**
- Solo puedes crear posts en el foro de tu carrera
- Tipos disponibles: comentario, encuesta, imagen, otro
- El sistema censura automaticamente palabras ofensivas
- Las imagenes requieren aprobacion de administradores

**Comentar en Posts**
- Puedes comentar en posts de cualquier foro
- Sin restricciones de carrera para comentarios

**Votar y Participar**
- Vota posts (upvote/downvote)
- Participa en encuestas
- Reporta contenido inapropiado

### Como Administrador

**Panel de Administracion**
- Aprobar/rechazar imagenes masivamente
- Moderar posts en revision
- Gestionar foros publicos y privados
- Ver historial de cambios de carrera
- Gestionar usuarios y roles

## Configuracion de Produccion

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas de despliegue en produccion.

## Documentacion

La documentacion completa se encuentra en:

- `Documentacion/config-avanzada/descripcion-proyecto.txt` - Descripcion completa
- `Documentacion/config-avanzada/estructura-proyecto.txt` - Estructura detallada
- `Documentacion/config-avanzada/herramientas-utilizadas.txt` - Stack tecnologico

- `Documentacion/config-avanzada/foro-implementacion-completa.txt` - Sistema de foros

## Testing

### Tests Unitarios
```bash
cd pruebas_unitarias
pytest
```

### Tests E2E
```bash
cd pruebas_automatizadas
pytest
```

## API Endpoints

### Autenticacion
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/login/` - Login con email/password
- `GET /api/auth/me/` - Informacion del usuario actual
- `POST /api/auth/refresh/` - Renovar token
- `GET /api/auth/google/login/web/` - Login con Google OAuth

### Foros
- `GET /api/foros/` - Lista de foros accesibles
- `GET /api/posts/?foro_id=X` - Posts de un foro
- `POST /api/posts/` - Crear post (solo en foro de tu carrera)
- `POST /api/posts/{id}/comentar/` - Comentar post
- `POST /api/posts/{id}/votar/` - Votar post
- `POST /api/posts/{id}/reportar/` - Reportar post

Ver documentacion completa de API en `/api/docs/`

## Seguridad

- Autenticacion JWT con tokens de acceso y refresco
- OAuth 2.0 con Google
- Censura automatica de contenido ofensivo
- Moderacion automatica de posts con palabras prohibidas
- Revision manual de imagenes
- Validaciones de permisos en backend
- CORS configurado correctamente
- Proteccion contra CSRF, XSS, SQL Injection

## Contribuciones

Este es un proyecto academico de Capstone. Las contribuciones son bienvenidas siguiendo estas pautas:

1. Fork del repositorio
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Equipo de Desarrollo

- Pablo Avendaño
- Darosh Luco
- Isaac Paz

**Institucion**: Duoc UC  
**Carrera**: Ingenieria en Informatica  
**Asignatura**: Proyecto de Capstone (APT122)

## Licencia

Este proyecto es de codigo abierto, desarrollado como proyecto academico.

## Estado del Proyecto

- **Version Actual**: 2.0.0
- **Fecha de Inicio**: Agosto 2025
- **Fecha Actual**: Octubre 2025
- **Estado**: En Desarrollo Activo

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para ver el historial de cambios.

## Contacto

- **Repositorio**: https://github.com/JackStar6677-1/students-point
- **Issues**: https://github.com/JackStar6677-1/students-point/issues

---

**Construyendo el futuro de la educacion digital** - StudentsPoint Team 2025

