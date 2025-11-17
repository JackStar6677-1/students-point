# Arquitectura de Software - StudentsPoint

## Resumen Ejecutivo

StudentsPoint es una **aplicación web progresiva (PWA)** que implementa una arquitectura **cliente-servidor** con separación clara entre frontend y backend. El sistema utiliza una **arquitectura de API REST** donde el frontend se comunica con el backend mediante endpoints HTTP/JSON, siguiendo el patrón **SPA (Single Page Application)**.

---

## 1. Tipo de Arquitectura

### 1.1 Arquitectura General
- **Tipo**: Cliente-Servidor con API REST
- **Patrón Frontend**: Single Page Application (SPA)
- **Patrón Backend**: Modelo-Vista-Controlador (MVC) con Django REST Framework
- **Comunicación**: HTTP/HTTPS con JSON
- **Autenticación**: JWT (JSON Web Tokens)

### 1.2 Capas de la Aplicación

```
┌─────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN            │
│  (Frontend - HTML, CSS, JavaScript)     │
│  - PWA con Service Worker                │
│  - API Services centralizados           │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON + JWT
┌──────────────▼──────────────────────────┐
│         CAPA DE APLICACIÓN              │
│  (Django REST Framework)                │
│  - Views/ViewSets                       │
│  - Serializers                          │
│  - Permissions                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         CAPA DE SERVICIOS               │
│  (Business Logic)                       │
│  - Services (forum, accounts, market)   │
│  - Utils (validaciones, helpers)       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         CAPA DE DATOS                  │
│  (Django ORM + Base de Datos)           │
│  - Models                                │
│  - PostgreSQL (prod) / SQLite (dev)     │
└─────────────────────────────────────────┘
```

---

## 2. Arquitectura del Backend

### 2.1 Framework y Tecnologías
- **Framework Principal**: Django 5.2
- **API Framework**: Django REST Framework (DRF)
- **Base de Datos**: 
  - Desarrollo: SQLite
  - Producción: PostgreSQL
- **Cache y Mensajería**: Redis
- **Tareas Asíncronas**: Celery
- **Autenticación**: JWT (Simple JWT)

### 2.2 Estructura Modular (Apps Django)

El backend está organizado en **aplicaciones Django modulares**, cada una con responsabilidades específicas:

```
studentspoint/
├── apps/
│   ├── accounts/          # Autenticación y gestión de usuarios
│   ├── forum/             # Sistema de foros
│   ├── market/            # Marketplace estudiantil
│   ├── polls/             # Sistema de encuestas
│   ├── notifications/     # Notificaciones push
│   ├── portfolio/         # Portafolio profesional
│   ├── document_converter/# Conversor de documentos
│   ├── wellbeing/         # Bienestar estudiantil
│   ├── otec/              # Cursos OTEC
│   ├── reports/           # Reportes de infraestructura
│   ├── campuses/          # Gestión de sedes y campus
│   └── health/            # Health checks
├── settings/              # Configuraciones por entorno
│   ├── base.py           # Configuración base
│   ├── dev.py            # Desarrollo
│   ├── prod.py           # Producción
│   └── test.py           # Testing
└── middleware.py         # Middlewares personalizados
```

### 2.3 Patrones de Diseño Implementados

#### 2.3.1 Service Layer Pattern
Cada módulo tiene una capa de servicios que encapsula la lógica de negocio:

- `ForumPermissionService`: Gestiona permisos del foro
- `TokenService`: Manejo de tokens JWT
- `EmailService`: Envío de emails
- `MarketService`: Lógica del marketplace
- `DocumentConverterService`: Procesamiento de documentos

**Ejemplo**:
```python
# studentspoint/apps/forum/services.py
class ForumPermissionService:
    @classmethod
    def puede_postear_en_foro(cls, usuario, foro) -> bool:
        # Lógica de permisos centralizada
        ...
```

#### 2.3.2 Repository Pattern (implícito con Django ORM)
Los modelos Django actúan como repositorios, proporcionando abstracción sobre la base de datos.

#### 2.3.3 Serializer Pattern (DRF)
Los serializers validan y transforman datos entre el modelo y la API:

```python
# Serializers validan y transforman datos
class PostSerializer(serializers.ModelSerializer):
    # Validaciones y transformaciones
    ...
```

#### 2.3.4 ViewSet Pattern (DRF)
Los ViewSets agrupan operaciones CRUD relacionadas:

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
```

### 2.4 Middleware Personalizado

El sistema incluye middleware personalizado para:
- **QueryCountDebugMiddleware**: Detecta consultas N+1
- **RequestLoggingMiddleware**: Registra todas las peticiones
- **DisableCSRFMiddleware**: Deshabilita CSRF para APIs (seguro con JWT)

### 2.5 Sistema de Autenticación

- **JWT Tokens**: Access token (corto) + Refresh token (largo)
- **OAuth 2.0**: Integración con Google
- **Verificación de Email**: Códigos temporales con expiración
- **Auditoría**: Logs de login, registro y actividad

---

## 3. Arquitectura del Frontend

### 3.1 Tecnologías
- **HTML5, CSS3, JavaScript ES6+**
- **Bootstrap 5**: Framework CSS
- **PWA**: Service Worker para funcionalidad offline
- **API Services**: Clases centralizadas para comunicación con backend

### 3.2 Estructura del Frontend

```
frontend/
├── static/
│   ├── js/
│   │   ├── auth-api.js        # Servicio de autenticación
│   │   ├── forum-api.js        # Servicio de foros
│   │   ├── market-api.js       # Servicio de marketplace
│   │   ├── portfolio-api.js    # Servicio de portafolio
│   │   ├── polls-api.js        # Servicio de encuestas
│   │   ├── courses-api.js      # Servicio de cursos
│   │   ├── wellbeing-api.js    # Servicio de bienestar
│   │   ├── main.js             # Utilidades generales
│   │   ├── auth.js             # Lógica de autenticación
│   │   └── pwa.js              # Configuración PWA
│   ├── css/
│   │   ├── styles.css          # Estilos principales
│   │   ├── students-theme.css  # Tema personalizado
│   │   └── components.css      # Componentes reutilizables
│   └── sw.js                   # Service Worker
├── index.html                  # Página principal
├── login.html                  # Login
├── register.html               # Registro
└── [módulos]/                  # Páginas por módulo
```

### 3.3 Patrón de API Services

Cada módulo tiene una clase de servicio que centraliza las llamadas HTTP:

```javascript
// Ejemplo: auth-api.js
class AuthAPI {
    constructor() {
        this.baseURL = '/api/auth';
    }
    
    async login(email, password) {
        const response = await fetch(`${this.baseURL}/login/`, {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ email, password })
        });
        return this.handleResponse(response);
    }
}
```

**Ventajas**:
- Abstracción de la comunicación HTTP
- Manejo centralizado de errores
- Reutilización de código
- Fácil mantenimiento

### 3.4 Progressive Web App (PWA)

- **Service Worker**: Cache de recursos estáticos
- **Manifest**: Configuración de instalación
- **Offline Support**: Funcionalidad básica sin conexión
- **Push Notifications**: Notificaciones en tiempo real

**Estrategias de Cache**:
- **Cache First**: Para recursos estáticos (CSS, JS, imágenes)
- **Network First**: Para APIs (datos dinámicos)
- **Stale While Revalidate**: Para HTML principal

---

## 4. Comunicación Frontend-Backend

### 4.1 Flujo de Comunicación

```
Frontend (JavaScript)
    ↓
API Service Class (auth-api.js, forum-api.js, etc.)
    ↓
fetch() con headers JWT
    ↓
Backend Django (URLs → Views → Serializers)
    ↓
Services (Lógica de negocio)
    ↓
Models (Base de datos)
    ↓
Response JSON
    ↓
Frontend (Actualización de UI)
```

### 4.2 Autenticación en Requests

```javascript
// Headers automáticos con JWT
headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
}
```

### 4.3 Manejo de Errores

- **401 Unauthorized**: Redirige a login
- **403 Forbidden**: Muestra mensaje de permisos
- **400 Bad Request**: Muestra errores de validación
- **500 Server Error**: Muestra mensaje genérico

---

## 5. Base de Datos

### 5.1 Modelo de Datos Principal

#### Entidades Principales:
- **User**: Usuarios del sistema
- **Foro**: Foros por carrera
- **Post**: Publicaciones en foros
- **Comment**: Comentarios en posts
- **Producto**: Productos del marketplace
- **Poll**: Encuestas
- **Portfolio**: Portafolios profesionales
- **Sede**: Sedes/campus de la institución

### 5.2 Relaciones Clave

```
User
  ├──→ Posts (1:N)
  ├──→ Comments (1:N)
  ├──→ Productos (1:N)
  ├──→ Encuestas (1:N)
  └──→ Portfolio (1:1)

Foro
  └──→ Posts (1:N)

Post
  ├──→ Comments (1:N)
  └──→ Votes (N:M)

Producto
  └──→ CategoriaProducto (N:1)
```

### 5.3 Migraciones

Django maneja el esquema de base de datos mediante migraciones:
- Desarrollo: SQLite (archivo local)
- Producción: PostgreSQL (servidor dedicado)

---

## 6. Tareas Asíncronas (Celery)

### 6.1 Configuración
- **Broker**: Redis
- **Result Backend**: Redis
- **Workers**: Procesan tareas en background

### 6.2 Tareas Asíncronas Implementadas
- Procesamiento de documentos (Word ↔ PDF)
- Envío de emails masivos
- Scraping de OpenGraph metadata
- Limpieza de archivos temporales

---

## 7. Seguridad

### 7.1 Medidas Implementadas

1. **Autenticación JWT**
   - Tokens con expiración
   - Refresh tokens para renovación

2. **Validación de Email**
   - Códigos temporales (15-30 min)
   - Verificación obligatoria

3. **Protección de Contraseñas**
   - Hashing PBKDF2-SHA256
   - No almacenamiento en texto plano

4. **CORS Configurado**
   - Orígenes permitidos específicos
   - Credenciales habilitadas

5. **Rate Limiting**
   - Throttling en APIs
   - Protección contra abuso

6. **Validaciones Backend**
   - Permisos por rol
   - Validación de datos en serializers

7. **Censura Automática**
   - Filtrado de palabras ofensivas
   - Moderación automática

---

## 8. Sistema de Logs y Monitoreo

### 8.1 Archivos de Log
- `general.log`: Eventos generales
- `errors.log`: Solo errores
- `api.log`: Peticiones API
- `auth.log`: Login/registro

### 8.2 Características
- **Rotación automática**: 10MB por archivo
- **Niveles de log**: DEBUG, INFO, ERROR
- **Auditoría completa**: IP, user agent, timestamps
- **Detección N+1**: Queries ineficientes

---

## 9. Testing

### 9.1 Tipos de Tests
- **Unitarios**: Modelos, serializers, servicios
- **Integración**: Flujos completos de API
- **E2E**: Interfaz con Selenium

### 9.2 Cobertura
- >80% del código backend
- Tests automatizados con pytest

---

## 10. Despliegue

### 10.1 Entornos
- **Desarrollo**: SQLite, DEBUG=True
- **Producción**: PostgreSQL, DEBUG=False
- **Configuración**: Variables de entorno (.env)

### 10.2 Servicios
- **Django**: Servidor WSGI
- **Redis**: Cache y broker
- **Celery**: Workers de tareas
- **PostgreSQL**: Base de datos

---

## 11. Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Frontend (PWA)                                       │  │
│  │  - HTML/CSS/JS                                        │  │
│  │  - Service Worker                                     │  │
│  │  - API Services                                       │  │
│  └──────────────┬───────────────────────────────────────┘  │
└─────────────────┼──────────────────────────────────────────┘
                  │ HTTP/HTTPS + JWT
┌─────────────────▼──────────────────────────────────────────┐
│                    SERVIDOR                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Django REST Framework                                │  │
│  │  - Views/ViewSets                                     │  │
│  │  - Serializers                                        │  │
│  │  - Permissions                                        │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │  Services Layer                                      │  │
│  │  - Business Logic                                    │  │
│  │  - Validations                                       │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │  Django ORM                                         │  │
│  │  - Models                                           │  │
│  │  - Migrations                                       │  │
│  └──────────────┬──────────────────────────────────────┘  │
└─────────────────┼──────────────────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────────────────┐
│              BASE DE DATOS                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL (Producción) / SQLite (Desarrollo)      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              SERVICIOS AUXILIARES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Redis     │  │   Celery    │  │     SMTP     │      │
│  │  (Cache/     │  │  (Tareas    │  │   (Emails)   │      │
│  │   Broker)    │  │  Async)     │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Principios de Diseño Aplicados

### 12.1 SOLID
- **Single Responsibility**: Cada app tiene una responsabilidad específica
- **Open/Closed**: Extensible mediante herencia y composición
- **Dependency Inversion**: Servicios abstraen dependencias

### 12.2 DRY (Don't Repeat Yourself)
- Servicios centralizados
- Utilidades reutilizables
- Componentes compartidos

### 12.3 Separation of Concerns
- Frontend: Presentación
- Backend: Lógica de negocio
- Base de datos: Persistencia

### 12.4 Modularidad
- Apps Django independientes
- Servicios desacoplados
- API Services modulares

---

## 13. Escalabilidad

### 13.1 Horizontal
- Múltiples instancias de Django (load balancer)
- Workers Celery distribuidos
- Redis cluster para cache

### 13.2 Vertical
- Optimización de queries (select_related, prefetch_related)
- Cache de consultas frecuentes
- Compresión de respuestas

---

## 14. Conclusión

StudentsPoint implementa una **arquitectura moderna y escalable** que separa claramente las responsabilidades entre frontend y backend. El uso de **API REST**, **PWA**, **servicios centralizados** y **patrones de diseño** bien establecidos, garantiza:

- **Mantenibilidad**: Código organizado y modular
- **Escalabilidad**: Preparado para crecimiento
- **Seguridad**: Múltiples capas de protección
- **Performance**: Optimizaciones en queries y cache
- **Experiencia de Usuario**: PWA con funcionalidad offline

Esta arquitectura permite el desarrollo continuo, la integración de nuevas funcionalidades y el mantenimiento a largo plazo del sistema.

