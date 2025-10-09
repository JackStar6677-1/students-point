# StudentsPoint - Plataforma Integral Estudiantil

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Django](https://img.shields.io/badge/django-5.2-green)
![License](https://img.shields.io/badge/license-Open%20Source-blue)

## Descripcion

StudentsPoint es una plataforma web progresiva (PWA) de codigo abierto diseñada para centralizar herramientas y servicios estudiantiles. Desarrollada como proyecto de Capstone, la plataforma puede ser implementada por cualquier institucion educativa.

**Proyecto de Capstone** - Ingenieria en Informatica, Duoc UC  
**Periodo**: Agosto - Diciembre 2025

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
- Registro con email y contraseña (verificacion por correo)
- Login seguro con JWT y hashing de contraseñas
- Google OAuth 2.0 como alternativa
- Recuperacion de contraseña por email
- Perfil personalizable (foto, datos academicos)
- Cambio de carrera cada semestre con historial
- Sistema de roles: admin, moderador, director de carrera, estudiante
- Multiples areas de estudio disponibles

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

La documentacion esta organizada en carpetas tematicas. Ver **[INDICE COMPLETO](Documentacion/INDICE-DOCUMENTACION.md)**

### Documentacion Tecnica
📁 `Documentacion/config-avanzada/`
- `descripcion-proyecto.txt` - Descripcion completa
- `estructura-proyecto.txt` - Estructura detallada
- `herramientas-utilizadas.txt` - Stack tecnologico
- `desarrollo-desde-cero.txt` - Desarrollo original
- `instrucciones-ia.txt` - Guia para herramientas automatizadas

### Implementaciones Completas
📁 `Documentacion/implementaciones/`
- `autenticacion-implementacion-completa.txt` - Sistema de autenticacion
- `foro-implementacion-completa.txt` - Sistema de foros

### Especificaciones de Requisitos
📁 `Documentacion/especificaciones/`
- `foro detallado.txt` - Requisitos del sistema de foros
- `login-profile-register detallado.txt` - Requisitos de autenticacion

### Guias de Configuracion y Uso
📁 `Documentacion/guias/`
- `CONFIGURACION-GOOGLE-EMAIL.md` - OAuth y Email SMTP
- `PRUEBAS-Y-ESTADO-PROYECTO.md` - Estado actual y tests
- `config_email_desarrollo.txt` - Configuracion de email
- `Recorridos_Virtuales.md` - Sistema de recorridos

### Documentos Academicos
📁 `Documentacion/academico/`
- `FASE 1/` - Evidencias de Fase 1
- Cronogramas, presentaciones, instructivos

### Informes y Estados
📄 `Documentacion/`
- `INDICE-DOCUMENTACION.md` - Indice completo organizado
- `INFORME-TESTS.md` - Estado y resultados de testing
- `README.md` - Guia de la documentacion

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
- `POST /api/auth/register/` - Registro de usuario (envia codigo de verificacion)
- `POST /api/auth/login/` - Login con email/password
- `GET /api/auth/me/` - Informacion del usuario actual
- `PATCH /api/auth/me/update/` - Actualizar perfil
- `POST /api/auth/refresh/` - Renovar token
- `GET /api/auth/google/login/web/` - Login con Google OAuth

### Verificacion de Email
- `POST /api/auth/verificar-email/` - Verificar email con codigo
- `POST /api/auth/reenviar-codigo/` - Reenviar codigo de verificacion

### Recuperacion de Contraseña
- `POST /api/auth/recuperar-password/` - Solicitar codigo de recuperacion
- `POST /api/auth/verificar-codigo-recuperacion/` - Verificar codigo
- `POST /api/auth/resetear-password/` - Cambiar contraseña con codigo
- `POST /api/auth/cambiar-password/` - Cambiar contraseña (autenticado)

### Gestion de Carrera
- `POST /api/auth/cambiar-carrera/` - Cambiar area de estudio
- `GET /api/carreras/` - Lista de carreras disponibles

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
- OAuth 2.0 con Google como alternativa
- Hashing seguro de contraseñas (PBKDF2-SHA256)
- Verificacion de email con codigos temporales (anti-bots)
- Codigos de verificacion con expiracion (15-30 minutos)
- Recuperacion de contraseña segura por email
- Censura automatica de contenido ofensivo en foros
- Moderacion automatica de posts con palabras prohibidas
- Revision manual de imagenes por administradores
- Validaciones de permisos en backend
- CORS configurado correctamente
- Proteccion contra CSRF, XSS, SQL Injection
- Rate limiting en API (throttling)

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

