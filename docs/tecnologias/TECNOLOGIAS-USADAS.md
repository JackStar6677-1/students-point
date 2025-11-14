# Tecnologías Usadas - StudentsPoint

## Resumen Ejecutivo

StudentsPoint utiliza un **stack tecnológico moderno y robusto** que combina tecnologías probadas en producción con herramientas de vanguardia. El proyecto está construido principalmente con **Python/Django** en el backend y **HTML/CSS/JavaScript** en el frontend, siguiendo estándares web modernos.

---

## 1. Backend

### 1.1 Framework Principal

#### Django 5.2
- **Versión**: 5.0 - 6.0 (actualmente 5.2)
- **Propósito**: Framework web principal
- **Características utilizadas**:
  - Sistema de modelos y ORM
  - Sistema de migraciones
  - Sistema de autenticación
  - Middleware personalizado
  - Sistema de templates
  - Sistema de administración
- **Razón de elección**: Framework maduro, robusto, con excelente documentación y comunidad

#### Django REST Framework (DRF) 3.15+
- **Versión**: >= 3.15
- **Propósito**: Construcción de API REST
- **Características utilizadas**:
  - ViewSets y Views
  - Serializers para validación
  - Permissions y Authentication
  - Paginación
  - Throttling (rate limiting)
  - Filtrado con django-filter
- **Razón de elección**: Estándar de facto para APIs REST en Django

#### drf-spectacular 0.27+
- **Versión**: >= 0.27
- **Propósito**: Documentación automática de API (OpenAPI/Swagger)
- **Características**: Genera documentación interactiva en `/api/docs/`
- **Razón de elección**: Documentación automática y actualizada

---

### 1.2 Base de Datos

#### PostgreSQL
- **Versión**: Compatible con versiones recientes
- **Propósito**: Base de datos de producción
- **Características utilizadas**:
  - Modelos relacionales
  - Transacciones ACID
  - Índices optimizados
  - JSON fields
- **Driver**: psycopg2-binary >= 2.9
- **Razón de elección**: Base de datos robusta, escalable y open source

#### SQLite
- **Versión**: Incluida en Python
- **Propósito**: Base de datos de desarrollo
- **Características**: Archivo local, sin configuración adicional
- **Razón de elección**: Simplicidad para desarrollo local

---

### 1.3 Autenticación y Seguridad

#### djangorestframework-simplejwt 5.3+
- **Versión**: >= 5.3
- **Propósito**: Autenticación con JWT (JSON Web Tokens)
- **Características utilizadas**:
  - Access tokens (cortos)
  - Refresh tokens (largos)
  - Renovación automática
- **Razón de elección**: Estándar moderno para autenticación stateless

#### django-cors-headers 4.4+
- **Versión**: >= 4.4
- **Propósito**: Configuración de CORS (Cross-Origin Resource Sharing)
- **Características**: Permite peticiones desde diferentes orígenes
- **Razón de elección**: Necesario para SPA con frontend separado

#### google-auth 2.40+
- **Versión**: >= 2.40
- **Propósito**: Integración con Google OAuth 2.0
- **Características**: Autenticación con Google
- **Razón de elección**: Autenticación social confiable

---

### 1.4 Tareas Asíncronas

#### Celery 5.4+
- **Versión**: >= 5.4
- **Propósito**: Procesamiento de tareas asíncronas
- **Características utilizadas**:
  - Workers para tareas en background
  - Tareas programadas
  - Retry automático
- **Razón de elección**: Estándar para tareas asíncronas en Python

#### Redis 5.0+
- **Versión**: >= 5.0
- **Propósito**: 
  - Broker de mensajes para Celery
  - Cache de consultas frecuentes
- **Características**: In-memory data store, alta velocidad
- **Driver**: django-redis >= 5.4
- **Razón de elección**: Rápido, confiable, ampliamente usado

#### django-celery-beat 2.5+
- **Versión**: >= 2.5
- **Propósito**: Tareas programadas (cron jobs)
- **Razón de elección**: Integración nativa con Django

#### django-celery-results 2.5+
- **Versión**: >= 2.5
- **Propósito**: Almacenamiento de resultados de tareas Celery
- **Razón de elección**: Tracking de tareas asíncronas

---

### 1.5 Procesamiento de Documentos

#### python-docx 1.1.0+
- **Versión**: >= 1.1.0
- **Propósito**: Lectura y escritura de archivos Word (.docx)
- **Características**: Conversión Word a PDF
- **Razón de elección**: Librería estándar para documentos Word

#### PyPDF2 3.0+
- **Versión**: >= 3.0
- **Propósito**: Procesamiento de archivos PDF
- **Características**: Lectura, escritura, manipulación de PDFs
- **Razón de elección**: Librería robusta para PDFs

#### reportlab 4.0+
- **Versión**: >= 4.0
- **Propósito**: Generación de PDFs desde cero
- **Características**: Generación de portafolios en PDF
- **Razón de elección**: Estándar para generación de PDFs en Python

#### pytesseract 0.3.10+
- **Versión**: >= 0.3.10
- **Propósito**: OCR (Optical Character Recognition)
- **Características**: Extracción de texto de imágenes/PDFs escaneados
- **Razón de elección**: Integración con Tesseract OCR

#### pdf2image 1.16.3+
- **Versión**: >= 1.16.3
- **Propósito**: Conversión de PDF a imágenes para OCR
- **Razón de elección**: Necesario para procesamiento OCR

#### Pillow 10.0+
- **Versión**: >= 10.0
- **Propósito**: Procesamiento de imágenes
- **Características**: Redimensionamiento, conversión de formatos
- **Razón de elección**: Librería estándar para imágenes en Python

---

### 1.6 Web Scraping y HTTP

#### beautifulsoup4 4.12+
- **Versión**: >= 4.12
- **Propósito**: Parsing de HTML
- **Características**: Extracción de metadatos OpenGraph
- **Razón de elección**: Librería estándar para scraping

#### requests 2.31+
- **Versión**: >= 2.31
- **Propósito**: Cliente HTTP
- **Características**: Peticiones HTTP para scraping
- **Razón de elección**: Librería estándar y simple

---

### 1.7 Notificaciones

#### pywebpush 1.14+
- **Versión**: >= 1.14
- **Propósito**: Notificaciones push web
- **Características**: Envío de notificaciones push a navegadores
- **Razón de elección**: Estándar para notificaciones web

---

### 1.8 Utilidades

#### python-dotenv 1.0+
- **Versión**: >= 1.0
- **Propósito**: Carga de variables de entorno desde archivos .env
- **Razón de elección**: Gestión sencilla de configuración

#### django-filter 25.1+
- **Versión**: >= 25.1
- **Propósito**: Filtrado avanzado en APIs
- **Características**: Filtros dinámicos en ViewSets
- **Razón de elección**: Integración con DRF

#### pytz 2024.1+
- **Versión**: >= 2024.1
- **Propósito**: Manejo de zonas horarias
- **Razón de elección**: Soporte completo de timezones

#### markdown 3.4+
- **Versión**: >= 3.4
- **Propósito**: Renderizado de Markdown
- **Razón de elección**: Formato estándar para texto

#### psutil 5.9+
- **Versión**: >= 5.9
- **Propósito**: Monitoreo del sistema
- **Características**: Métricas de CPU, memoria, etc.
- **Razón de elección**: Monitoreo de recursos

---

### 1.9 Testing

#### pytest 8.0+
- **Versión**: >= 8.0
- **Propósito**: Framework de testing
- **Características**: Tests unitarios, de integración, fixtures
- **Razón de elección**: Framework moderno y flexible

#### pytest-django 4.8+
- **Versión**: >= 4.8
- **Propósito**: Integración de pytest con Django
- **Razón de elección**: Testing eficiente en Django

---

### 1.10 Producción

#### gunicorn 21.2+
- **Versión**: >= 21.2
- **Propósito**: Servidor WSGI para producción
- **Características**: Múltiples workers, alta concurrencia
- **Razón de elección**: Servidor WSGI estándar para producción

#### django-storages 1.14+
- **Versión**: >= 1.14
- **Propósito**: Almacenamiento en la nube (opcional)
- **Características**: Integración con S3, Azure, etc.
- **Razón de elección**: Escalabilidad de almacenamiento

#### boto3 1.34+
- **Versión**: >= 1.34
- **Propósito**: SDK de AWS (para almacenamiento S3)
- **Razón de elección**: Integración con servicios AWS

---

## 2. Frontend

### 2.1 Tecnologías Base

#### HTML5
- **Versión**: HTML5 estándar
- **Propósito**: Estructura de páginas
- **Características utilizadas**:
  - Semantic HTML
  - Formularios HTML5
  - Offline capabilities (PWA)

#### CSS3
- **Versión**: CSS3 estándar
- **Propósito**: Estilos y diseño
- **Características utilizadas**:
  - Flexbox y Grid
  - Animaciones CSS
  - Variables CSS
  - Media queries (responsive)

#### JavaScript ES6+
- **Versión**: ES6+ (ECMAScript 2015+)
- **Propósito**: Lógica del frontend
- **Características utilizadas**:
  - Async/await
  - Arrow functions
  - Classes
  - Modules
  - Fetch API
  - LocalStorage
  - Service Workers

---

### 2.2 Frameworks y Librerías

#### Bootstrap 5.3.0
- **Versión**: 5.3.0 (CDN)
- **Propósito**: Framework CSS
- **Características utilizadas**:
  - Sistema de grid
  - Componentes (botones, cards, modals, etc.)
  - Utilidades responsive
  - Iconos (Bootstrap Icons)
- **Razón de elección**: Framework CSS maduro y completo

#### Font Awesome 6.4.0
- **Versión**: 6.4.0 (CDN)
- **Propósito**: Iconos
- **Características**: Miles de iconos vectoriales
- **Razón de elección**: Librería de iconos estándar

#### jQuery 3.7.1
- **Versión**: 3.7.1 (CDN)
- **Propósito**: Manipulación del DOM (legacy, uso limitado)
- **Razón de elección**: Compatibilidad con algunos componentes

---

### 2.3 Progressive Web App (PWA)

#### Service Worker
- **Tecnología**: Service Worker API (nativo del navegador)
- **Propósito**: Funcionalidad offline y cache
- **Características**:
  - Cache de recursos estáticos
  - Estrategias de cache (Cache First, Network First)
  - Funcionalidad offline
- **Archivo**: `static/sw.js`

#### Web App Manifest
- **Tecnología**: Web App Manifest (estándar W3C)
- **Propósito**: Configuración de instalación PWA
- **Características**:
  - Nombre, iconos, colores
  - Modo de visualización
  - Orientación
- **Archivo**: `static/manifest.json`, `static/manifest.webmanifest`

#### Push Notifications
- **Tecnología**: Web Push API (nativo del navegador)
- **Propósito**: Notificaciones push
- **Características**: Notificaciones en tiempo real

---

## 3. Herramientas de Desarrollo

### 3.1 Control de Versiones

#### Git
- **Propósito**: Control de versiones
- **Plataforma**: GitHub
- **Razón de elección**: Estándar de la industria

---

### 3.2 Linting y Formateo

#### Pyright
- **Propósito**: Type checking para Python
- **Configuración**: `pyrightconfig.json`
- **Razón de elección**: Type checking estático

---

### 3.3 Scripts de Automatización

#### Scripts Bash (.sh)
- **Propósito**: Scripts para Linux/Mac
- **Ejemplos**: `iniciar_desarrollo.sh`, `ver_logs.sh`

#### Scripts Batch (.bat)
- **Propósito**: Scripts para Windows
- **Ejemplos**: `iniciar_desarrollo.bat`, `ver_logs.bat`

---

## 4. Servicios y Infraestructura

### 4.1 Servidor Web

#### Gunicorn
- **Propósito**: Servidor WSGI en producción
- **Características**: Múltiples workers, alta concurrencia

#### Django Development Server
- **Propósito**: Servidor de desarrollo
- **Comando**: `python manage.py runserver`

---

### 4.2 Servicios de Email

#### SMTP (Gmail)
- **Propósito**: Envío de emails
- **Configuración**: Variables de entorno
- **Características**: Verificación de email, recuperación de contraseña

---

### 4.3 Almacenamiento

#### Sistema de Archivos Local
- **Propósito**: Almacenamiento de archivos en desarrollo
- **Carpetas**: `media/` para archivos subidos

#### Almacenamiento en la Nube (Opcional)
- **Servicio**: AWS S3, Azure Blob Storage
- **Librería**: django-storages + boto3
- **Propósito**: Escalabilidad en producción

---

## 5. Stack Tecnológico Completo

### 5.1 Backend Stack
```
Python 3.11+
  ├── Django 5.2
  │   ├── Django REST Framework 3.15+
  │   ├── Simple JWT 5.3+
  │   ├── drf-spectacular 0.27+
  │   ├── django-cors-headers 4.4+
  │   ├── django-filter 25.1+
  │   └── django-celery-beat 2.5+
  ├── PostgreSQL (producción) / SQLite (desarrollo)
  ├── Redis 5.0+ (cache y broker)
  ├── Celery 5.4+ (tareas async)
  ├── Procesamiento de documentos
  │   ├── python-docx 1.1.0+
  │   ├── PyPDF2 3.0+
  │   ├── reportlab 4.0+
  │   ├── pytesseract 0.3.10+
  │   └── Pillow 10.0+
  ├── Web scraping
  │   ├── beautifulsoup4 4.12+
  │   └── requests 2.31+
  ├── OAuth
  │   └── google-auth 2.40+
  ├── Notificaciones
  │   └── pywebpush 1.14+
  └── Testing
      ├── pytest 8.0+
      └── pytest-django 4.8+
```

### 5.2 Frontend Stack
```
HTML5
  ├── CSS3
  │   └── Bootstrap 5.3.0
  ├── JavaScript ES6+
  │   ├── Fetch API
  │   ├── Service Workers (PWA)
  │   └── Web Push API
  └── Librerías
      ├── Font Awesome 6.4.0
      └── jQuery 3.7.1
```

### 5.3 Infraestructura
```
Servidor
  ├── Gunicorn (producción)
  ├── Django Dev Server (desarrollo)
  └── Nginx (opcional, reverse proxy)

Base de Datos
  ├── PostgreSQL (producción)
  └── SQLite (desarrollo)

Cache y Mensajería
  └── Redis 5.0+

Almacenamiento
  ├── Sistema de archivos local (desarrollo)
  └── Cloud Storage (producción, opcional)
```

---

## 6. Versiones y Compatibilidad

### 6.1 Python
- **Versión mínima**: Python 3.11+
- **Razón**: Soporte para características modernas

### 6.2 Navegadores Soportados
- Chrome/Edge (últimas versiones)
- Firefox (últimas versiones)
- Safari (últimas versiones)
- Navegadores móviles modernos

### 6.3 PWA Support
- Chrome/Edge: Soporte completo
- Firefox: Soporte completo
- Safari: Soporte parcial (iOS 11.3+)

---

## 7. Razones de Elección de Tecnologías

### 7.1 Backend
- **Django**: Framework maduro, robusto, con excelente ecosistema
- **DRF**: Estándar para APIs REST en Django
- **PostgreSQL**: Base de datos robusta y escalable
- **Celery + Redis**: Solución probada para tareas asíncronas
- **JWT**: Autenticación stateless moderna

### 7.2 Frontend
- **HTML/CSS/JS vanilla**: Sin dependencias pesadas, fácil mantenimiento
- **Bootstrap**: Framework CSS completo y probado
- **PWA**: Mejor experiencia de usuario, funcionalidad offline

### 7.3 Procesamiento
- **python-docx, PyPDF2**: Librerías estándar para documentos
- **pytesseract**: OCR confiable y open source
- **beautifulsoup4**: Scraping simple y efectivo

---

## 8. Resumen

### 8.1 Tecnologías Principales
- **Backend**: Python 3.11+, Django 5.2, DRF 3.15+
- **Base de datos**: PostgreSQL (prod), SQLite (dev)
- **Cache/Broker**: Redis 5.0+
- **Tareas async**: Celery 5.4+
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Bootstrap 5
- **PWA**: Service Workers, Web App Manifest

### 8.2 Características
- ✅ Stack moderno y actualizado
- ✅ Tecnologías probadas en producción
- ✅ Buen rendimiento y escalabilidad
- ✅ Fácil mantenimiento
- ✅ Documentación completa
- ✅ Comunidad activa

---

Este stack tecnológico está diseñado para ser **robusto**, **escalable** y **mantenible**, utilizando tecnologías estándar de la industria con excelente soporte y documentación.

