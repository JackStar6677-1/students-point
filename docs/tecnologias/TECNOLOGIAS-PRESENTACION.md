# Tecnologías Usadas - StudentsPoint
## Documento para Presentación PPT

---

## 1. BACKEND

### Framework Principal
- **Django 5.2**: Framework web principal
- **Django REST Framework 3.15+**: API REST
- **drf-spectacular 0.27+**: Documentación automática de API

### Base de Datos
- **PostgreSQL**: Producción (robusta y escalable)
- **SQLite**: Desarrollo (simple y local)
- **psycopg2-binary**: Driver de PostgreSQL

### Autenticación
- **djangorestframework-simplejwt 5.3+**: JWT tokens
- **google-auth 2.40+**: OAuth con Google
- **django-cors-headers 4.4+**: CORS

### Tareas Asíncronas
- **Celery 5.4+**: Procesamiento asíncrono
- **Redis 5.0+**: Cache y broker de mensajes
- **django-celery-beat 2.5+**: Tareas programadas

### Procesamiento de Documentos
- **python-docx 1.1.0+**: Word (.docx)
- **PyPDF2 3.0+**: PDFs
- **reportlab 4.0+**: Generación de PDFs
- **pytesseract 0.3.10+**: OCR
- **Pillow 10.0+**: Imágenes

### Web Scraping
- **beautifulsoup4 4.12+**: Parsing HTML
- **requests 2.31+**: Cliente HTTP

### Notificaciones
- **pywebpush 1.14+**: Notificaciones push web

### Testing
- **pytest 8.0+**: Framework de testing
- **pytest-django 4.8+**: Integración con Django

### Producción
- **gunicorn 21.2+**: Servidor WSGI

---

## 2. FRONTEND

### Tecnologías Base
- **HTML5**: Estructura
- **CSS3**: Estilos
- **JavaScript ES6+**: Lógica

### Frameworks y Librerías
- **Bootstrap 5.3.0**: Framework CSS
- **Font Awesome 6.4.0**: Iconos
- **jQuery 3.7.1**: Manipulación DOM (limitado)

### Progressive Web App (PWA)
- **Service Worker**: Funcionalidad offline y cache
- **Web App Manifest**: Configuración de instalación
- **Web Push API**: Notificaciones push

---

## 3. STACK COMPLETO

### Backend Stack
```
Python 3.11+
  ├── Django 5.2 + DRF 3.15+
  ├── PostgreSQL / SQLite
  ├── Redis + Celery
  ├── JWT Authentication
  ├── Document Processing
  └── Web Scraping
```

### Frontend Stack
```
HTML5 + CSS3 + JavaScript ES6+
  ├── Bootstrap 5
  ├── Font Awesome
  └── PWA (Service Worker)
```

---

## 4. RAZONES DE ELECCIÓN

### Backend
- **Django**: Framework maduro y robusto
- **DRF**: Estándar para APIs REST
- **PostgreSQL**: Base de datos escalable
- **Celery + Redis**: Solución probada para async

### Frontend
- **HTML/CSS/JS vanilla**: Sin dependencias pesadas
- **Bootstrap**: Framework CSS completo
- **PWA**: Mejor experiencia de usuario

---

## 5. VENTAJAS DEL STACK

✅ **Tecnologías probadas**: Ampliamente usadas en producción
✅ **Buen rendimiento**: Optimizado para velocidad
✅ **Escalabilidad**: Preparado para crecimiento
✅ **Mantenibilidad**: Código organizado y documentado
✅ **Comunidad activa**: Soporte y recursos disponibles

---

## PUNTOS CLAVE PARA PPT

### Slide 1: Backend
- Django 5.2 + DRF
- PostgreSQL
- Celery + Redis

### Slide 2: Frontend
- HTML5, CSS3, JavaScript ES6+
- Bootstrap 5
- PWA

### Slide 3: Funcionalidades Especiales
- Procesamiento de documentos (Word, PDF, OCR)
- Web scraping (OpenGraph)
- Notificaciones push

### Slide 4: Infraestructura
- Gunicorn (producción)
- Redis (cache)
- PostgreSQL (base de datos)

### Slide 5: Ventajas
- Moderno
- Probado
- Escalable
- Mantenible

