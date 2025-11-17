# Arquitectura de Software - StudentsPoint
## Documento para Presentación PPT

---

## 1. TIPO DE ARQUITECTURA

### Arquitectura Cliente-Servidor con API REST

- **Frontend**: Single Page Application (SPA) - PWA
- **Backend**: Django REST Framework (API REST)
- **Comunicación**: HTTP/HTTPS con JSON
- **Autenticación**: JWT (JSON Web Tokens)

**Ventajas**:
- Separación clara de responsabilidades
- Escalabilidad independiente
- Reutilización de API para múltiples clientes
- Mantenimiento simplificado

---

## 2. CAPAS DE LA ARQUITECTURA

```
┌─────────────────────────────────────┐
│   CAPA DE PRESENTACIÓN              │
│   Frontend (HTML, CSS, JavaScript)   │
│   - PWA con Service Worker          │
│   - API Services centralizados     │
└──────────────┬──────────────────────┘
               │ HTTP/JSON + JWT
┌──────────────▼──────────────────────┐
│   CAPA DE APLICACIÓN                │
│   Django REST Framework             │
│   - Views/ViewSets                  │
│   - Serializers                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   CAPA DE SERVICIOS                 │
│   Business Logic                    │
│   - Services (forum, accounts)      │
│   - Utils (validaciones)            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   CAPA DE DATOS                     │
│   Django ORM + Base de Datos         │
│   - Models                          │
│   - PostgreSQL / SQLite             │
└─────────────────────────────────────┘
```

---

## 3. ESTRUCTURA DEL BACKEND

### Framework y Tecnologías
- **Django 5.2**: Framework web principal
- **Django REST Framework**: API REST
- **PostgreSQL**: Base de datos (producción)
- **Redis**: Cache y mensajería
- **Celery**: Tareas asíncronas
- **JWT**: Autenticación

### Organización Modular (Apps Django)

```
studentspoint/
├── accounts/          # Autenticación y usuarios
├── forum/             # Sistema de foros
├── market/            # Marketplace
├── polls/             # Encuestas
├── notifications/     # Notificaciones
├── portfolio/         # Portafolio profesional
├── document_converter/ # Conversor documentos
├── wellbeing/         # Bienestar estudiantil
├── otec/              # Cursos OTEC
└── reports/           # Reportes
```

**Cada app es independiente y reutilizable**

---

## 4. PATRONES DE DISEÑO IMPLEMENTADOS

### 4.1 Service Layer Pattern
Encapsula la lógica de negocio en servicios reutilizables:

- `ForumPermissionService`: Permisos del foro
- `TokenService`: Manejo de tokens JWT
- `EmailService`: Envío de emails
- `MarketService`: Lógica del marketplace

**Beneficio**: Separación de lógica de negocio de las vistas

### 4.2 ViewSet Pattern (DRF)
Agrupa operaciones CRUD relacionadas:

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

**Beneficio**: Código más limpio y organizado

### 4.3 Serializer Pattern
Valida y transforma datos entre modelo y API:

**Beneficio**: Validación centralizada y consistente

---

## 5. ESTRUCTURA DEL FRONTEND

### Tecnologías
- HTML5, CSS3, JavaScript ES6+
- Bootstrap 5
- PWA (Service Worker)
- API Services centralizados

### Organización

```
frontend/
├── static/js/
│   ├── auth-api.js      # Servicio autenticación
│   ├── forum-api.js     # Servicio foros
│   ├── market-api.js    # Servicio marketplace
│   └── ...
├── static/css/          # Estilos
└── *.html               # Páginas
```

**Cada módulo tiene su API Service para comunicación con backend**

---

## 6. COMUNICACIÓN FRONTEND-BACKEND

### Flujo de Petición

```
1. Usuario interactúa con UI
   ↓
2. JavaScript llama a API Service
   ↓
3. API Service hace fetch() con JWT
   ↓
4. Backend valida y procesa
   ↓
5. Response JSON
   ↓
6. Frontend actualiza UI
```

### Autenticación
- **JWT Tokens**: Access token (corto) + Refresh token (largo)
- **Headers automáticos**: `Authorization: Bearer <token>`
- **Renovación automática**: Refresh token cuando expira

---

## 7. BASE DE DATOS

### Modelo de Datos

**Entidades Principales**:
- User (Usuarios)
- Foro (Foros por carrera)
- Post (Publicaciones)
- Producto (Marketplace)
- Poll (Encuestas)
- Portfolio (Portafolios)

### Relaciones

```
User
  ├──→ Posts (1:N)
  ├──→ Comments (1:N)
  ├──→ Productos (1:N)
  └──→ Portfolio (1:1)

Foro → Posts (1:N)
Post → Comments (1:N)
```

### Base de Datos
- **Desarrollo**: SQLite (archivo local)
- **Producción**: PostgreSQL (servidor dedicado)

---

## 8. PROGRESSIVE WEB APP (PWA)

### Características
- **Service Worker**: Cache de recursos
- **Offline Support**: Funcionalidad sin conexión
- **Instalable**: Se puede instalar como app nativa
- **Push Notifications**: Notificaciones en tiempo real

### Estrategias de Cache
- **Cache First**: Recursos estáticos (CSS, JS, imágenes)
- **Network First**: APIs (datos dinámicos)
- **Stale While Revalidate**: HTML principal

---

## 9. SEGURIDAD

### Medidas Implementadas

1. **Autenticación JWT**
   - Tokens con expiración
   - Refresh tokens

2. **Validación de Email**
   - Códigos temporales (15-30 min)
   - Verificación obligatoria

3. **Protección de Contraseñas**
   - Hashing PBKDF2-SHA256
   - No almacenamiento en texto plano

4. **Rate Limiting**
   - Throttling en APIs
   - Protección contra abuso

5. **Validaciones Backend**
   - Permisos por rol
   - Validación en serializers

6. **Censura Automática**
   - Filtrado de palabras ofensivas
   - Moderación automática

---

## 10. TAREAS ASÍNCRONAS (Celery)

### Configuración
- **Broker**: Redis
- **Workers**: Procesan tareas en background

### Tareas Implementadas
- Procesamiento de documentos (Word ↔ PDF)
- Envío de emails masivos
- Scraping de OpenGraph metadata
- Limpieza de archivos temporales

**Beneficio**: No bloquea la respuesta al usuario

---

## 11. SISTEMA DE LOGS Y MONITOREO

### Archivos de Log
- `general.log`: Eventos generales
- `errors.log`: Solo errores
- `api.log`: Peticiones API
- `auth.log`: Login/registro

### Características
- Rotación automática (10MB por archivo)
- Auditoría completa (IP, user agent, timestamps)
- Detección de queries N+1
- Monitoreo en tiempo real

---

## 12. DIAGRAMA DE ARQUITECTURA GENERAL

```
┌──────────────────────────────────────────────┐
│              CLIENTE (Browser)                │
│  ┌────────────────────────────────────────┐  │
│  │  Frontend PWA                          │  │
│  │  - HTML/CSS/JS                         │  │
│  │  - Service Worker                      │  │
│  │  - API Services                        │  │
│  └──────────────┬─────────────────────────┘  │
└─────────────────┼────────────────────────────┘
                  │ HTTP/HTTPS + JWT
┌─────────────────▼────────────────────────────┐
│              SERVIDOR                          │
│  ┌────────────────────────────────────────┐  │
│  │  Django REST Framework                 │  │
│  │  - Views/ViewSets                     │  │
│  │  - Serializers                        │  │
│  │  - Services                           │  │
│  └──────────────┬─────────────────────────┘  │
│                 │                             │
│  ┌──────────────▼─────────────────────────┐  │
│  │  Django ORM                            │  │
│  │  - Models                             │  │
│  └──────────────┬─────────────────────────┘  │
└─────────────────┼────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────┐
│         BASE DE DATOS                         │
│  PostgreSQL (prod) / SQLite (dev)            │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│         SERVICIOS AUXILIARES                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Redis   │  │  Celery  │  │   SMTP   │  │
│  │ (Cache)  │  │ (Async)  │  │ (Emails) │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└──────────────────────────────────────────────┘
```

---

## 13. PRINCIPIOS DE DISEÑO

### SOLID
- **Single Responsibility**: Cada app tiene una responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Dependency Inversion**: Servicios abstraen dependencias

### DRY (Don't Repeat Yourself)
- Servicios centralizados
- Utilidades reutilizables
- Componentes compartidos

### Separation of Concerns
- Frontend: Presentación
- Backend: Lógica de negocio
- Base de datos: Persistencia

---

## 14. ESCALABILIDAD

### Horizontal
- Múltiples instancias de Django (load balancer)
- Workers Celery distribuidos
- Redis cluster

### Vertical
- Optimización de queries
- Cache de consultas frecuentes
- Compresión de respuestas

---

## 15. VENTAJAS DE LA ARQUITECTURA

✅ **Mantenibilidad**: Código organizado y modular
✅ **Escalabilidad**: Preparado para crecimiento
✅ **Seguridad**: Múltiples capas de protección
✅ **Performance**: Optimizaciones en queries y cache
✅ **Experiencia de Usuario**: PWA con funcionalidad offline
✅ **Reutilización**: API puede servir múltiples clientes
✅ **Testing**: Fácil de testear (separación de capas)

---

## 16. RESUMEN PARA PPT

### Slide 1: Tipo de Arquitectura
- Cliente-Servidor con API REST
- SPA (Single Page Application)
- PWA (Progressive Web App)

### Slide 2: Capas
- Presentación (Frontend)
- Aplicación (Django REST)
- Servicios (Business Logic)
- Datos (Base de datos)

### Slide 3: Backend
- Django 5.2 + DRF
- Apps modulares
- Patrones: Service Layer, ViewSet, Serializer

### Slide 4: Frontend
- HTML/CSS/JS
- API Services centralizados
- PWA con Service Worker

### Slide 5: Seguridad
- JWT Authentication
- Validación de email
- Rate limiting
- Censura automática

### Slide 6: Tecnologías
- Backend: Django, PostgreSQL, Redis, Celery
- Frontend: HTML5, CSS3, JavaScript, Bootstrap
- PWA: Service Worker, Manifest

### Slide 7: Ventajas
- Mantenible, Escalable, Seguro, Performante

---

## PUNTOS CLAVE PARA LA PRESENTACIÓN

1. **Arquitectura moderna**: API REST con separación clara de responsabilidades
2. **Modularidad**: Apps Django independientes y reutilizables
3. **Seguridad**: Múltiples capas (JWT, validaciones, rate limiting)
4. **PWA**: Funcionalidad offline e instalable
5. **Escalabilidad**: Preparado para crecimiento horizontal y vertical
6. **Mantenibilidad**: Código organizado siguiendo principios SOLID
7. **Performance**: Optimizaciones en queries, cache y tareas asíncronas

