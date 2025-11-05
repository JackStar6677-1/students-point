# StudentsPoint - Plataforma Integral Estudiantil

![Version](https://img.shields.io/badge/version-5.0.0--production--ready-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Django](https://img.shields.io/badge/django-5.2-green)
![License](https://img.shields.io/badge/license-Open%20Source-blue)
![Status](https://img.shields.io/badge/status-production--ready-success)

>  **NUEVO USUARIO:** Lee [`Documentacion/GUIA-COMPLETA.md`](Documentacion/GUIA-COMPLETA.md) para inicio super rapido.

>  **TODA LA DOCUMENTACION:** Ver [`Documentacion/INDICE-MAESTRO.md`](Documentacion/INDICE-MAESTRO.md) para indice completo.

## Descripcion

StudentsPoint es una plataforma web progresiva (PWA) de codigo abierto diseñada para centralizar herramientas y servicios estudiantiles. Desarrollada como proyecto de Capstone, la plataforma puede ser implementada por cualquier institucion educativa.

**Proyecto de Capstone** - Ingenieria en Informatica, Duoc UC  
**Periodo**: Agosto - Diciembre 2025  
**Estado**:  Production-Ready - Masterizado - Sistema de Logs Automático

##  Inicio Rápido

### Windows
```batch
iniciar_desarrollo.bat
```

### Linux/Mac
```bash
chmod +x iniciar_desarrollo.sh
./iniciar_desarrollo.sh
```

**¡Eso es todo!** El servidor y el monitor de logs se inician automáticamente.

>  **Documentacion completa**: Ver [`Documentacion/INDICE-MAESTRO.md`](Documentacion/INDICE-MAESTRO.md) para guia completa de toda la documentacion disponible.

>  **Sistema de Logs**: Ver [`Documentacion/INICIO-RAPIDO-LOGS.md`](Documentacion/INICIO-RAPIDO-LOGS.md) para guia de monitoreo y logs.

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
- Optimizacion de consultas N+1
- Abstraccion de codigo con servicios y utilidades

### Autenticacion y Usuarios
- Registro con email y contraseña (verificacion por correo)
- Login seguro con JWT y hashing de contraseñas
- Google OAuth 2.0 como alternativa
- Recuperacion de contraseña por email
- Verificacion de email con codigos HTML profesionales
- Sistema de auditoria completo (LoginLog, RegistrationLog, UserActivityLog)
- Perfil personalizable (foto, datos academicos)
- Cambio de carrera cada semestre con historial
- Sistema de roles: admin, moderador, director de carrera, estudiante
- Multiples areas de estudio disponibles
- Scripts de prueba interactivos para verificacion de email

### Marketplace Estudiantil
- Productos con enlaces externos (Facebook, Yapo, MercadoLibre)
- OpenGraph metadata scraping automatico
- Vista previa de productos externos
- Sistema de favoritos
- Reportes de productos inapropiados
- Analytics detallados por producto
- Filtrado por campus y carrera
- Abstraccion de servicios para extraccion de metadatos

### Conversor de Documentos
- Conversion Word a PDF con preservacion de formato
- Conversion PDF a Word editable
- OCR para PDFs escaneados (pytesseract)
- Validacion de archivos (tamaño, tipo, contenido vacio)
- Manejo robusto de errores
- Procesamiento asincrono
- Historial de conversiones
- Limpieza automatica de archivos temporales

### Otras Funcionalidades
- Portafolio profesional con generacion de PDF
- Recorridos virtuales 360° del campus
- Sistema de bienestar estudiantil
- Gestion de horarios de clases
- Cursos OTEC
- Sistema de encuestas
- Notificaciones push
- Sistema de reportes de infraestructura
- PWA (Progressive Web App) completamente funcional

### Sistema de Monitoreo y Auditoria
- **Logging completo**: 4 archivos de log separados (general, errors, api, auth)
- **Monitor en tiempo real**: Actualizacion automatica cada 30-60s
- **Sistema de alertas**: Deteccion automatica de problemas criticos
- **Analisis avanzado**: Reportes con estadisticas y recomendaciones
- **Optimizacion de queries**: Deteccion automatica de N+1
- **Performance monitoring**: Metricas de frontend en tiempo real
- **Auditoria de usuarios**: Registro completo de logins, registros y actividad
- **Trazabilidad**: IP, user agent y timestamps para cada accion importante

## Testing

El proyecto incluye un sistema completo de testing automatizado:

- **Pruebas Unitarias**: APIs, modelos, serializers, vistas
- **Pruebas de Integracion**: Flujos completos de APIs
- **Pruebas E2E**: Interfaz de usuario con Selenium
- **Cobertura**: >80% del codigo

**Ejecutar pruebas:**
```bash
# Windows
ejecutar_tests_dev.bat

# Linux/Mac
./ejecutar_tests_completo.sh

# Suite completa con reporte
python tests/test_suite_completo.py --verbose --coverage
```

Para mas detalles, ver [Documentacion/TESTING.md](Documentacion/TESTING.md)

## Stack Tecnologico

### Backend
- **Django 5.2** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos (produccion)
- **SQLite** - Base de datos (desarrollo)
- **Redis** - Cache y broker de mensajes
- **Celery** - Tareas asincronas
- **JWT** - Autenticacion con tokens
- **python-docx, reportlab** - Procesamiento de documentos
- **PyPDF2, pytesseract** - Conversion PDF y OCR
- **beautifulsoup4, requests** - Web scraping y OpenGraph
- **google-auth** - OAuth 2.0 con Google

### Frontend
- **HTML5, CSS3, JavaScript ES6+** - Tecnologias base
- **Bootstrap 5** - Framework CSS
- **PWA** - Service Worker para funcionalidad offline
- **Font Awesome** - Iconos
- **API Services centralizados** - Abstraccion de llamadas HTTP
- **Autenticacion centralizada** - Servicios reutilizables

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
 Documentacion/           # Documentacion completa del proyecto
    config-avanzada/     # Documentacion tecnica detallada
 proyecto/
    src/
        backend/         # Backend Django
           studentspoint/
               apps/    # Aplicaciones Django
                   accounts/      # Autenticacion, usuarios y auditoria
                   forum/         # Sistema de foros
                   market/        # Marketplace
                   portfolio/     # Portafolios profesionales
                   campuses/      # Recorridos virtuales campus
                   document_converter/  # Conversor de documentos
                   notifications/ # Sistema de notificaciones
                   polls/         # Sistema de encuestas
                   otec/          # Cursos OTEC
                   reports/       # Reportes de infraestructura
                   wellbeing/     # Bienestar estudiantil
                   health/        # Health checks
        frontend/        # Frontend (HTML/CSS/JS)
           static/       # Archivos estaticos (CSS, JS, imagenes)
           forum/        # Interfaz de foros
           market/       # Interfaz de marketplace
           portfolio/    # Interfaz de portafolios
           converter/    # Interfaz de conversor
           cursos/       # Interfaz de cursos
           encuestas/    # Interfaz de encuestas
           bienestar/    # Interfaz de bienestar
           reportes/     # Interfaz de reportes
           streetview/   # Recorridos virtuales
 pruebas_unitarias/       # Tests unitarios con pytest
 pruebas_automatizadas/   # Tests E2E
 iniciar_desarrollo.bat   # Script de inicio Windows
 iniciar_desarrollo.sh   # Script de inicio Linux/Mac
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

Ver [Documentacion/DEPLOYMENT.md](Documentacion/DEPLOYMENT.md) para instrucciones detalladas de despliegue en produccion.

## Documentacion

La documentacion esta organizada en carpetas tematicas. Ver:
- **[Documentacion/GUIA-COMPLETA.md](Documentacion/GUIA-COMPLETA.md)** - Guia de inicio completa
- **[Documentacion/INDICE-MAESTRO.md](Documentacion/INDICE-MAESTRO.md)** - Indice general de toda la documentacion
- **[Documentacion/ESTRUCTURA-DOCUMENTACION.md](Documentacion/ESTRUCTURA-DOCUMENTACION.md)** - Como esta organizada la documentacion
- **[Documentacion/INDICE-DOCUMENTACION.md](Documentacion/INDICE-DOCUMENTACION.md)** - Indice de Documentacion/ completo

### Documentacion Tecnica
 `Documentacion/config-avanzada/`
- `descripcion-proyecto.txt` - Descripcion completa
- `estructura-proyecto.txt` - Estructura detallada
- `herramientas-utilizadas.txt` - Stack tecnologico
- `desarrollo-desde-cero.txt` - Desarrollo original
- `instrucciones-ia.txt` - Guia para herramientas automatizadas

### Implementaciones Completas
 `Documentacion/implementaciones/`
- `autenticacion-implementacion-completa.txt` - Sistema de autenticacion
- `foro-implementacion-completa.txt` - Sistema de foros

### Especificaciones de Requisitos
 `Documentacion/especificaciones/`
- `foro detallado.txt` - Requisitos del sistema de foros
- `login-profile-register detallado.txt` - Requisitos de autenticacion

### Guias de Configuracion y Uso
 `Documentacion/guias/`
- `CONFIGURACION-GOOGLE-EMAIL.md` - OAuth y Email SMTP
- `PRUEBAS-Y-ESTADO-PROYECTO.md` - Estado actual y tests
- `config_email_desarrollo.txt` - Configuracion de email
- `Recorridos_Virtuales.md` - Sistema de recorridos

### Documentos Academicos
 `Documentacion/academico/`
- `FASE 1/` - Evidencias de Fase 1
- Cronogramas, presentaciones, instructivos

### Informes y Estados
 `Documentacion/`
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

- **Version Actual**: v5.0.0 (Release 5)
- **Fecha de Inicio**: Agosto 2025
- **Fecha Actual**: Noviembre 2025
- **Estado**: Production-Ready - Sistema Completo con Auditoria

### Hitos Completados (v5.0.0 - 5 de Noviembre 2025)
- Sistema de foros avanzado personalizado por carrera
- Sistema de autenticacion completo con verificacion de email HTML
- Sistema de auditoria completo (LoginLog, RegistrationLog, UserActivityLog)
- Email SMTP real configurado y funcional
- Google OAuth 2.0 configurado y funcional
- Conversor de documentos Word/PDF con OCR
- Marketplace con extraccion automatica de OpenGraph
- Abstraccion de codigo mejorada (services, utils, API services)
- PWA completamente funcional con instalacion
- Scripts de inicio automatizados (Windows y Linux)
- Scripts de prueba interactivos para verificacion de email
- Base de datos completamente migrada
- Tests unitarios completos y corregidos
- Documentacion completa y organizada
- Eliminacion de codigo duplicado y redundante
- Configuracion de linters (Pyright) para imports dinamicos

## Releases

Ver [Documentacion/RELEASES.md](Documentacion/RELEASES.md) para ver todas las versiones.

## Changelog

Ver [Documentacion/CHANGELOG.md](Documentacion/CHANGELOG.md) para ver el historial de cambios detallado.

## Contacto

- **Repositorio**: https://github.com/JackStar6677-1/students-point
- **Issues**: https://github.com/JackStar6677-1/students-point/issues

---

**Construyendo el futuro de la educacion digital** - StudentsPoint Team 2025

