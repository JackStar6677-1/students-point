# StudentsPoint - Plataforma Integral Estudiantil

![Version](https://img.shields.io/badge/version-5.0.0--production--ready-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Django](https://img.shields.io/badge/django-5.2-green)
![License](https://img.shields.io/badge/license-Open%20Source-blue)
![Status](https://img.shields.io/badge/status-production--ready-success)

>  ** INICIO RÁPIDO:** Lee [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md) - Solo doble click en `iniciar_desarrollo_full.bat`

>  **NUEVO USUARIO:** Lee [`docs/GUIA-COMPLETA.md`](docs/GUIA-COMPLETA.md) para guía completa de instalación.

>  ** DOCUMENTACIÓN:** Ver carpeta [`docs/`](docs/) para documentación organizada por categorías.

>  ** PWA/MÓVIL:** Ver [`docs/guias/GUIA-RAPIDA-MOVIL.md`](docs/guias/GUIA-RAPIDA-MOVIL.md) para ejecutar en celular.

>  ** RELEASES:** Ver [`docs/releases/`](docs/releases/) para notas de versión.

## Descripcion

StudentsPoint es una plataforma web progresiva (PWA) de codigo abierto diseñada para centralizar herramientas y servicios estudiantiles. Desarrollada como proyecto de Capstone, la plataforma puede ser implementada por cualquier institucion educativa.

**Proyecto de Capstone** - Ingenieria en Informatica, Duoc UC  
**Periodo**: Agosto - Diciembre 2025  
**Estado**:  Production-Ready - Masterizado - Sistema de Logs Automático

## Filosofía del Proyecto

StudentsPoint nace de la necesidad de **centralizar y unificar** todas las herramientas que los estudiantes necesitan en un solo lugar accesible. En lugar de tener múltiples aplicaciones dispersas (foros en un sitio, marketplace en otro, portafolio en otro), esta plataforma integra una **suite completa de herramientas estudiantiles** bajo un mismo ecosistema.

### ¿Por qué tantas funciones diferentes?

La diversidad de módulos en StudentsPoint responde a una estrategia de **centralización estudiantil**:

- **Foros**: Comunicación y discusión académica por carrera
- **Marketplace**: Compra/venta entre estudiantes de la misma institución
- **Portafolio**: Gestión profesional de logros y certificaciones
- **Reportes**: Sistema de incidencias para mantener el campus en óptimas condiciones
- **Encuestas**: Participación estudiantil y feedback institucional
- **Cursos OTEC**: Capacitación continua y certificaciones
- **Bienestar**: Rutinas de kinesiología y salud estudiantil
- **Recorridos Virtuales**: Orientación y navegación del campus
- **Conversor de Documentos**: Herramientas de productividad académica

### Adopción Institucional

**Cualquier institución educativa** puede adoptar StudentsPoint como su plataforma de centralización estudiantil. El proyecto está diseñado para ser:

-  **Modular**: Cada herramienta funciona de forma independiente
-  **Escalable**: Se adapta a instituciones pequeñas y grandes
-  **Personalizable**: Configurable por campus, carreras y roles
-  **Open Source**: Libre para adaptar a necesidades específicas
-  **PWA**: Funciona como aplicación nativa en móviles y escritorio

Esta arquitectura permite que las instituciones **reemplacen múltiples sistemas dispersos** con una única plataforma integrada, mejorando la experiencia del estudiante y reduciendo la fragmentación de servicios.

##  Inicio Rápido

### Launcher Universal (Recomendado)
```batch
iniciar_studentspoint.bat
```

Este script maestro te permite elegir el modo de inicio:
1. Local - Solo esta PC
2. Red Local - WiFi
3. Tailscale - VPN privada
4. ngrok - HTTPS publico (perfecto para PWA)
5. playit.gg - Tunel HTTP permanente
6. playit.gg HTTPS - Con certificados SSL
7. Produccion - Modo produccion
8. Instalar Dependencias - Instala todo automaticamente

**Documentacion completa:** Ver [`docs/guias/LAUNCHER.md`](docs/guias/LAUNCHER.md)

### Alternativas en carpeta scripts/

**Windows:**
```batch
scripts\iniciar_desarrollo.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/iniciar_desarrollo.sh
./scripts/iniciar_desarrollo.sh
```

### Otros Modos de Inicio

Usa el launcher universal `iniciar_studentspoint.bat` y selecciona:
- **Opcion [4]** - ngrok con HTTPS (perfecto para PWA)
- **Opcion [5]** - playit.gg tunel permanente
- **Opcion [6]** - playit.gg con HTTPS

**Guias completas:**
- [`docs/guias/USAR-NGROK.md`](docs/guias/USAR-NGROK.md) - Configuracion de ngrok
- [`docs/guias/USAR-PLAYIT.md`](docs/guias/USAR-PLAYIT.md) - Configuracion de playit.gg

**¡Eso es todo!** El servidor se inicia automáticamente.

### Scripts de Inicio Disponibles

**En la raíz del proyecto:**
- `iniciar_studentspoint.bat` - **Launcher Universal** - Menu interactivo con todas las opciones

**En la carpeta `scripts/`:**
- `iniciar_desarrollo.bat/.sh` - Inicio rápido en desarrollo
- `iniciar_con_ngrok.bat` - Inicio con HTTPS (ngrok) para PWA móvil
- `iniciar_playit_https.bat` - Inicio con playit.gg y HTTPS
- `iniciar_produccion.bat/.sh` - Iniciar en modo producción
- `iniciar_simple.bat` - Inicio minimalista sin extras
- `iniciar_solo_ngrok.bat` - Solo tunel ngrok (Django debe estar corriendo)
- `configurar_https.bat` - Configurar HTTPS local con certificado self-signed
- `regenerar_iconos_pwa.bat` - Regenerar iconos PWA con logo StudentsPoint
- `ver_logs.bat/.sh` - Ver logs en tiempo real
- `ver_logs_tests.bat/.sh` - Ver logs de pruebas
- `deploy_linux.sh` - Despliegue en Linux
- `instalar_postgresql.bat` - Instalador de PostgreSQL
- `instalar_pwa.bat/.sh` - Instalar archivos PWA
- `detener_servicios.sh` - Detener servicios en Linux
- `detener_monitor.bat` - Detener monitor en Windows
- `aplicar_correcciones_movil.bat` - Aplicar correcciones de responsive móvil
- `diagnostico.bat` - Diagnóstico del sistema
- `verificar_pwa.bat` - Verificar instalación PWA
- `iniciar_simple.bat` - Inicio simple alternativo
- `iniciar_solo_ngrok.bat` - Iniciar solo ngrok (Django debe estar corriendo)
- `verificar_pwa.bat` - Verificar archivos PWA

### Cobertura de módulos recientes

- **Foros**: Comentarios, reportes y moderación con permisos y auditoría reforzada. Ahora solo permite mensajes de texto/imagen (las encuestas tienen su propio módulo).
- **Marketplace**: Visualización del `precio_student_point`, validaciones de términos y analytics automáticos.
- **Reportes**: Sistema completo para reportar incidencias en salas de clases y espacios del campus (computadores rotos, baches, infraestructura dañada, etc.) con subida de fotos, filtros dinámicos, KPIs y exportaciones CSV/PDF.
- **Encuestas**: Módulo independiente con integración completa de roles (`moderator`, `director_carrera`), votación, resultados y creación avanzada. Frontend mejorado con mejor visibilidad del selector de sedes y controles de fecha.
- **Entorno de pruebas**: Suites de API actualizadas y migraciones aplicadas para evitar discrepancias de base de datos.

>  **Documentacion completa**: Ver carpeta [`docs/`](docs/) para toda la documentacion disponible.

>  **Sistema de Logs**: Ver [`docs/guias/SISTEMA-LOGGING.md`](docs/guias/SISTEMA-LOGGING.md) para guia de monitoreo y logs.

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

### PWA (Progressive Web App)
- Service Worker con cache inteligente
- Instalacion como app nativa (Android/iOS)
- Funcionamiento offline
- Actualizaciones automaticas
- Iconos optimizados para todas las resoluciones
- Soporte HTTPS con ngrok para testing rapido
- Responsive design optimizado para moviles
- Safe-area-inset para notches y barras inferiores

### Otras Funcionalidades
- Portafolio profesional con generacion de PDF
- Recorridos virtuales 360° del campus
- Sistema de bienestar estudiantil
- Gestion de horarios de clases
- Cursos OTEC
- **Sistema de encuestas** - Módulo independiente para votaciones institucionales (no confundir con el foro)
- Notificaciones push
- Sistema de reportes de incidencias en salas de clases y espacios del campus (con subida de fotos)

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
- **Pruebas PWA**: 21 tests para verificar funcionamiento completo
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

**Testing PWA en Celular:**

Ver [`docs/guias/PRUEBAS-PWA.md`](docs/guias/PRUEBAS-PWA.md) para:
- 21 tests de verificacion PWA
- Testing en Android/iOS
- Verificacion de Service Worker
- Pruebas de instalacion
- Testing con ngrok (HTTPS)

Para mas detalles, ver la documentacion en `docs/`

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



## Uso del Sistema de Foros

### Como Estudiante

**Crear una Publicacion**
- Solo puedes crear posts en el foro de tu carrera
- Tipos disponibles: mensaje (texto) y mensaje con imagen
- El sistema censura automaticamente palabras ofensivas
- Las imagenes requieren aprobacion de administradores
- **Nota**: Las encuestas tienen su propio módulo separado (`/encuestas/`)

**Comentar en Posts**
- Puedes comentar en posts de cualquier foro
- Sin restricciones de carrera para comentarios

**Votar y Participar**
- Vota posts (upvote/downvote)
- Reporta contenido inapropiado
- Para encuestas institucionales, usa el módulo de Encuestas (`/encuestas/`)

### Como Administrador

**Panel de Administracion**
- Aprobar/rechazar imagenes masivamente
- Moderar posts en revision
- Gestionar foros publicos y privados
- Ver historial de cambios de carrera
- Gestionar usuarios y roles

## Sistema de Reportes de Incidencias

### Como Estudiante

**Crear un Reporte**
- Reporta problemas en salas de clases y espacios del campus (computadores rotos, baches, baños dañados, etc.)
- Adjunta fotos del problema para documentarlo visualmente
- Selecciona la sede/campus donde ocurrió el problema
- Indica la ubicación exacta con coordenadas (se puede usar la ubicación del dispositivo)
- Categoriza el problema (ej: "Computador roto", "Bache", "Baño dañado")
- Describe el problema en detalle

**Visualizar Reportes**
- Filtra reportes por fecha, categoría, campus y estado
- Ve KPIs en tiempo real: totales, en revisión, resueltos, pendientes
- Exporta reportes a CSV o PDF para análisis

### Como Moderador/Administrador

**Gestionar Reportes**
- Cambia el estado de reportes (Abierto → En revisión → Resuelto)
- Asigna prioridad a los reportes
- Visualiza todas las fotos adjuntas
- Filtra y analiza reportes por múltiples criterios
- Exporta datos para reportes administrativos

## Configuracion de Produccion

Ver [`docs/guias/DEPLOYMENT-PRODUCTION.md`](docs/guias/DEPLOYMENT-PRODUCTION.md) para instrucciones detalladas de despliegue en produccion.

## Estructura del Proyecto

```
students-point/
├── docs/                       # Documentacion completa
│   ├── academico/             # Documentos academicos del Capstone
│   ├── arquitectura/          # Arquitectura del sistema
│   ├── config-avanzada/       # Configuracion tecnica detallada
│   ├── especificaciones/      # Especificaciones de requisitos
│   ├── guias/                 # Guias (PWA, ngrok, deployment, etc.)
│   ├── historico/             # Resumenes y estados previos
│   ├── modelo-datos/          # Modelos de datos
│   ├── modulos/               # Documentacion de modulos
│   ├── releases/              # Notas de versiones
│   └── tecnologias/           # Stack tecnologico
│
├── scripts/                    # Scripts de utilidades organizados
│   ├── iniciar_produccion.*   # Scripts de produccion
│   ├── configurar_https.bat   # Configurar HTTPS local
│   ├── instalar_pwa.*         # Instalacion PWA
│   ├── ver_logs.*             # Scripts de visualizacion de logs
│   ├── deploy_linux.sh        # Despliegue en Linux
│   ├── diagnostico.bat        # Diagnostico del sistema
│   ├── verificar_pwa.bat      # Verificacion PWA
│   └── ...                    # Otros scripts de utilidad
│
├── FASE 1/                     # Evidencias academicas Fase 1
├── FASE 2/                     # Evidencias academicas Fase 2
├── FASE 3/                     # Evidencias academicas Fase 3
│
├── proyecto/                   # Codigo fuente principal
│   └── src/
│       ├── backend/           # Backend Django
│       │   ├── studentspoint/ # Proyecto Django principal
│       │   │   ├── apps/      # Aplicaciones Django
│       │   │   └── settings/  # Configuraciones (dev, prod, test)
│       │   └── manage.py
│       └── frontend/          # Frontend (HTML, CSS, JS)
│           ├── static/        # Archivos estaticos centralizados
│           │   ├── js/        # JavaScript centralizado
│           │   ├── css/       # CSS centralizado (con mobile-fixes.css)
│           │   ├── sw.js      # Service Worker PWA
│           │   ├── manifest.json  # Web App Manifest
│           │   └── pwa-config.js  # Configuracion PWA
│           └── *.html         # Paginas HTML
│
├── pruebas_unitarias/          # Tests unitarios (pytest)
├── pruebas_automatizadas/      # Tests E2E
├── tests/                      # Suite de tests completa
│
├── config/                     # Configuraciones del sistema
│   └── systemd/               # Servicios systemd para Linux
│
├── logs_tests/                 # Logs de pruebas automatizadas
│
├── iniciar_desarrollo.*        # Scripts de inicio rapido (raiz)
├── iniciar_con_ngrok.bat       # Inicio con HTTPS/ngrok para PWA
├── USAR-NGROK.md               # Guia rapida de ngrok
├── README.md                   # Este archivo
├── pyrightconfig.json          # Configuracion de linter
└── .gitignore                  # Archivos ignorados por Git
```

## Documentacion

La documentacion esta organizada en carpetas tematicas. Ver:
- **[docs/GUIA-COMPLETA.md](docs/GUIA-COMPLETA.md)** - Guia de inicio completa
- **Carpeta [`docs/`](docs/)** - Toda la documentacion del proyecto

### Documentacion Tecnica
 `docs/config-avanzada/`
- `descripcion-proyecto.txt` - Descripcion completa
- `estructura-proyecto.txt` - Estructura detallada
- `herramientas-utilizadas.txt` - Stack tecnologico
- `desarrollo-desde-cero.txt` - Desarrollo original

### Especificaciones de Requisitos
 `docs/especificaciones/`
- `foro detallado.txt` - Requisitos del sistema de foros
- `login-profile-register detallado.txt` - Requisitos de autenticacion

### Guias de Configuracion y Uso
 `docs/guias/`
- `CONFIGURACION-GOOGLE-EMAIL.md` - OAuth y Email SMTP
- `DEPLOYMENT-PRODUCTION.md` - Despliegue en produccion
- `SISTEMA-LOGGING.md` - Sistema de logs y monitoreo
- `docs/guias/LAUNCHER.md` - Guia completa del launcher universal con todas las opciones
- `docs/guias/USAR-NGROK.md` - Guia rapida para usar ngrok con HTTPS
- `docs/guias/USAR-PLAYIT.md` - Guia rapida para usar playit.gg con tunel publico
- `PWA-CELULAR.md` - Guia rapida de instalacion PWA en celular
- `INSTALACION-PWA.md` - Instalacion completa de PWA
- `PRUEBAS-PWA.md` - 21 tests para verificar PWA
- `ACTUALIZAR-ICONOS-PWA.md` - Actualizar iconos PWA con logo StudentsPoint
- `Recorridos_Virtuales.md` - Sistema de recorridos

### Documentos Academicos (Fases del Proyecto)
 `FASE 1/`, `FASE 2/`, `FASE 3/` - Evidencias academicas del Capstone
 `docs/academico/` - Cronogramas, presentaciones, instructivos

### Historico y Resumenes
 `docs/historico/`
- Resumenes de sesiones de trabajo
- Historiales de implementacion
- Estados previos del proyecto

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

Ver la carpeta `docs/` para ver todas las versiones y cambios detallados del proyecto.

## Changelog

Ver `docs/historico/` para ver el historial de cambios detallado.

## Contacto

- **Repositorio**: https://github.com/JackStar6677-1/students-point
- **Issues**: https://github.com/JackStar6677-1/students-point/issues

---

**Construyendo el futuro de la educacion digital** - StudentsPoint Team 2025

