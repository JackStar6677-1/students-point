# StudentsPoint - Guia de Presentacion

## Informacion General

**Nombre:** StudentsPoint - Plataforma Integral Estudiantil  
**Version:** 5.0.0 Production-Ready  
**Tipo:** Progressive Web App (PWA)  
**Periodo:** Agosto - Diciembre 2025  
**Proyecto:** Capstone - Ingenieria en Informatica, Duoc UC  

---

## Resumen Ejecutivo

StudentsPoint es una **plataforma web progresiva (PWA)** que centraliza herramientas y servicios estudiantiles en un solo ecosistema. La plataforma puede ser implementada por cualquier institucion educativa para reemplazar multiples sistemas dispersos.

### Problema que Resuelve

**Antes:** Estudiantes deben usar multiples aplicaciones:
- Foro en un sitio
- Marketplace en otro
- Portafolio en otro
- Cada uno con su propio login, interfaz diferente, sin integracion

**Despues:** Una sola plataforma centralizada con:
- Login unico
- Interfaz consistente
- Datos integrados
- Accesible desde cualquier dispositivo

---

## Stack Tecnologico

### Backend
- **Framework:** Django 5.2
- **API:** Django REST Framework
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (produccion)
- **Autenticacion:** JWT + OAuth2 (Google)
- **Tareas Asincronas:** Celery + Redis

### Frontend
- **Tecnologia:** Vanilla JavaScript (ES6+)
- **CSS:** CSS3 con variables personalizadas
- **PWA:** Service Workers + Web App Manifest
- **Iconos:** SVG + PNG multiplesresoluciones

### Infraestructura
- **Servidor Web:** Gunicorn (produccion)
- **Proxy Inverso:** Nginx
- **Monitoreo:** Sistema de logs personalizado
- **Testing:** pytest + Selenium

---

## Arquitectura del Sistema

### Modelo MVC (Model-View-Controller)

```
Cliente (Navegador/PWA)
    ↓
Django URLs (Router)
    ↓
Views (Controlador)
    ↓
Serializers (Transformacion de Datos)
    ↓
Models (Base de Datos)
```

### Estructura de Apps Django

```
studentspoint/
├── accounts/       - Gestion de usuarios y autenticacion
├── forum/          - Sistema de foros por carrera
├── market/         - Marketplace estudiantil
├── portfolio/      - Portafolios academicos
├── polls/          - Sistema de encuestas
├── reports/        - Reportes de incidencias
├── wellbeing/      - Bienestar y salud
├── otec/           - Cursos y capacitaciones
├── notifications/  - Sistema de notificaciones
├── campuses/       - Gestion de campus
├── document_converter/ - Conversor de documentos
└── campus_map/     - Mapas y recorridos virtuales
```

Cada app es **independiente** y **modular**, siguiendo el principio de **Separation of Concerns**.

---

## Base de Datos

### Diagrama de Relaciones Principales

```
Usuario (CustomUser)
    ├── tiene muchos → Posts (Foro)
    ├── tiene muchos → Productos (Marketplace)
    ├── tiene uno → Portafolio
    ├── responde → Encuestas
    ├── crea → Reportes
    ├── se inscribe en → Cursos
    └── pertenece a → Campus
```

### Modelos Principales

**1. CustomUser** (Usuario Personalizado)
```python
- email (EmailField) - Login principal
- nombre (CharField)
- apellido (CharField)
- carrera (CharField)
- campus (ForeignKey)
- rol (CharField) - estudiante/profesor/admin
- avatar (ImageField)
- fecha_registro (DateTimeField)
```

**2. Post** (Foro)
```python
- autor (ForeignKey → User)
- categoria (ForeignKey → Categoria)
- titulo (CharField)
- contenido (TextField)
- imagenes (ManyToManyField → ImagenPost)
- fecha_creacion (DateTimeField)
- likes (IntegerField)
- estado_moderacion (CharField)
```

**3. Producto** (Marketplace)
```python
- vendedor (ForeignKey → User)
- nombre (CharField)
- descripcion (TextField)
- precio (DecimalField)
- categoria (ForeignKey → CategoriaProducto)
- imagenes (ManyToManyField → ImagenProducto)
- estado (CharField) - disponible/vendido/reservado
- campus (ForeignKey → Campus)
```

**4. Portafolio**
```python
- usuario (OneToOneField → User)
- biografia (TextField)
- proyectos (ManyToManyField → Proyecto)
- certificaciones (ManyToManyField → Certificacion)
- habilidades (JSONField)
```

**5. Encuesta** (Polls)
```python
- titulo (CharField)
- descripcion (TextField)
- creador (ForeignKey → User)
- preguntas (ManyToManyField → Pregunta)
- fecha_inicio (DateTimeField)
- fecha_fin (DateTimeField)
- es_anonima (BooleanField)
```

**6. Reporte** (Incidencias)
```python
- reportante (ForeignKey → User)
- titulo (CharField)
- descripcion (TextField)
- categoria (CharField)
- ubicacion (CharField)
- prioridad (CharField)
- estado (CharField) - pendiente/en_revision/resuelto
- imagenes (ManyToManyField)
```

Ver diagrama completo en: `docs/modelo-datos/MODELO-DE-DATOS.md`

---

## Modulos Funcionales

### 1. Sistema de Foros
**Descripcion:** Discusion academica organizada por carreras

**Caracteristicas:**
- Categorias por carrera (Informatica, Administracion, etc.)
- Posts con imagenes multiples
- Sistema de likes
- Comentarios anidados
- Moderacion automatica con IA
- Busqueda avanzada

**Flujo:**
```
Usuario crea post → Moderacion automatica → Publicacion → Otros comentan/like
```

### 2. Marketplace
**Descripcion:** Compra/venta entre estudiantes

**Caracteristicas:**
- Categorias de productos (Libros, Tecnologia, Ropa, etc.)
- Imagenes multiples por producto
- Sistema de estado (disponible/vendido/reservado)
- Filtrado por campus
- Chat directo con vendedor
- Valoraciones

**Flujo:**
```
Vendedor publica producto → Comprador busca → Contacto → Transaccion
```

### 3. Portafolios Academicos
**Descripcion:** CV digital para estudiantes

**Caracteristicas:**
- Proyectos con imagenes y descripcion
- Certificaciones
- Habilidades tecnicas
- Enlaces a GitHub/LinkedIn
- Exportar a PDF
- Compartir enlace publico

### 4. Encuestas
**Descripcion:** Participacion estudiantil

**Caracteristicas:**
- Preguntas de seleccion multiple
- Preguntas abiertas
- Encuestas anonimas opcionales
- Resultados en tiempo real
- Graficos de visualizacion

### 5. Sistema de Reportes
**Descripcion:** Reporte de incidencias en el campus

**Caracteristicas:**
- Categorias (Infraestructura, Limpieza, Seguridad, etc.)
- Ubicacion especifica
- Prioridad (Baja, Media, Alta, Urgente)
- Seguimiento de estado
- Panel administrativo

### 6. Bienestar y Salud
**Descripcion:** Rutinas de kinesiologia y salud estudiantil

**Caracteristicas:**
- Rutinas de ejercicios
- Videos instructivos
- Seguimiento de progreso
- Consejos de salud

### 7. Cursos OTEC
**Descripcion:** Capacitaciones y certificaciones

**Caracteristicas:**
- Catalogo de cursos
- Inscripcion en linea
- Videos de clases
- Certificados digitales
- Seguimiento de progreso

### 8. Recorridos Virtuales
**Descripcion:** Google Street View del campus

**Caracteristicas:**
- Navegacion interactiva 360°
- Puntos de interes
- Informacion de edificios
- Orientacion para nuevos estudiantes

### 9. Conversor de Documentos
**Descripcion:** Herramienta de productividad

**Caracteristicas:**
- Convierte DOCX → PDF
- Procesa archivos en servidor
- Descarga automatica
- Historial de conversiones

---

## API REST

### Endpoints Principales

**Autenticacion:**
```
POST /api/auth/register/          - Registro de usuario
POST /api/auth/login/             - Login (obtiene JWT token)
POST /api/auth/logout/            - Logout
POST /api/auth/refresh/           - Refresh token
POST /api/auth/google/            - Login con Google OAuth
```

**Foro:**
```
GET    /api/forum/posts/          - Listar posts
POST   /api/forum/posts/          - Crear post
GET    /api/forum/posts/{id}/     - Detalle de post
PUT    /api/forum/posts/{id}/     - Actualizar post
DELETE /api/forum/posts/{id}/     - Eliminar post
POST   /api/forum/posts/{id}/like/ - Dar like
GET    /api/forum/categorias/     - Listar categorias
```

**Marketplace:**
```
GET    /api/market/productos/              - Listar productos
POST   /api/market/productos/              - Crear producto
GET    /api/market/productos/{id}/         - Detalle
PUT    /api/market/productos/{id}/         - Actualizar
DELETE /api/market/productos/{id}/         - Eliminar
GET    /api/market/productos/{id}/favorito/ - Agregar a favoritos
GET    /api/market/categorias/             - Listar categorias
```

**Portafolio:**
```
GET    /api/portfolio/portafolio/          - Obtener portafolio
PUT    /api/portfolio/portafolio/          - Actualizar
POST   /api/portfolio/proyectos/           - Agregar proyecto
POST   /api/portfolio/certificaciones/     - Agregar certificacion
```

**Encuestas:**
```
GET    /api/polls/encuestas/               - Listar encuestas activas
POST   /api/polls/encuestas/{id}/responder/ - Responder encuesta
GET    /api/polls/encuestas/{id}/resultados/ - Ver resultados
```

**Reportes:**
```
GET    /api/reports/reportes/              - Listar reportes
POST   /api/reports/reportes/              - Crear reporte
GET    /api/reports/reportes/{id}/         - Detalle
PUT    /api/reports/reportes/{id}/         - Actualizar estado
```

Documentacion completa: `http://localhost:8000/api/docs/` (Swagger UI)

---

## Progressive Web App (PWA)

### Que es una PWA?

Una PWA combina lo mejor de las aplicaciones web y las aplicaciones nativas:

**Ventajas sobre web tradicional:**
- ✅ Se instala como app nativa
- ✅ Funciona offline
- ✅ Notificaciones push
- ✅ Acceso rapido desde pantalla de inicio
- ✅ Sin bordes del navegador

**Ventajas sobre app nativa:**
- ✅ Sin necesidad de tiendas (Play Store/App Store)
- ✅ Actualizaciones instantaneas
- ✅ Un solo codigo para todas las plataformas
- ✅ Menor tamaño de descarga

### Componentes de nuestra PWA

**1. Service Worker** (`sw.js`)
```javascript
// Cache de archivos estaticos
// Estrategia: Cache First, Network Fallback
// Funciona offline
```

**2. Web App Manifest** (`manifest.json`)
```json
{
  "name": "StudentsPoint",
  "short_name": "StudentsPoint",
  "start_url": "/",
  "display": "standalone",  // Sin bordes del navegador
  "theme_color": "#2c3e50",
  "icons": [
    // Multiples resoluciones para diferentes dispositivos
  ]
}
```

**3. Iconos Adaptables**
- 192x192, 512x512 (Android)
- 180x180 (iOS)
- Favicon.svg (Navegadores)

### Como Instalar la PWA

**En Android (Chrome):**
1. Abre StudentsPoint en Chrome
2. Menu → "Agregar a pantalla de inicio"
3. Confirmar

**En iOS (Safari):**
1. Abre StudentsPoint en Safari
2. Compartir → "Agregar a pantalla de inicio"
3. Confirmar

**En Desktop (Chrome/Edge):**
1. Icono de instalacion en barra de direcciones
2. Click → "Instalar"

---

## Seguridad

### Autenticacion y Autorizacion

**1. JWT (JSON Web Tokens)**
- Token de acceso: 5 minutos
- Token de refresh: 7 dias
- Se guarda en localStorage (frontend)

**2. OAuth 2.0 (Google)**
- Login con cuenta institucional
- No se almacena contraseña
- Token validado en backend

**3. Permisos por Rol**
```python
- Estudiante: Crear posts, comprar/vender, portafolio
- Profesor: Todo lo anterior + moderar, crear encuestas
- Admin: Todo + gestion de usuarios, reportes
```

### Proteccion de Datos

**1. CSRF Protection**
- Django CSRF tokens
- Validacion en cada request POST/PUT/DELETE

**2. XSS Prevention**
- Escape de HTML en templates
- Content Security Policy headers

**3. SQL Injection Prevention**
- Django ORM (parametrized queries)
- Validacion de inputs con serializers

**4. Passwords**
- Hash con bcrypt (Django default)
- Minimo 8 caracteres, complejidad
- Reset via email seguro

---

## Testing

### Pruebas Unitarias (pytest)

```bash
# Ejecutar todas las pruebas
pytest pruebas_unitarias/

# Ver cobertura
pytest --cov=proyecto/src/backend/studentspoint
```

**Pruebas implementadas:**
- API endpoints (19 tests)
- Models (validators, métodos custom)
- Serializers (validacion de datos)
- Views (logica de negocio)

**Ubicacion:** `pruebas_unitarias/`

### Pruebas E2E (Selenium)

```bash
# Ejecutar pruebas automatizadas
python pruebas_automatizadas/test_homepage.py
python pruebas_automatizadas/test_login.py
python pruebas_automatizadas/test_forum_e2e.py
```

**Pruebas implementadas:**
- Login flow
- Registro de usuario
- Crear post en foro
- Navegacion general

**Ubicacion:** `pruebas_automatizadas/`

---

## Deployment

### Desarrollo (Local)

```bash
# Opcion 1: Launcher universal
iniciar_studentspoint.bat

# Opcion 2: Script directo
scripts\iniciar_desarrollo.bat
```

**URLs:**
- App: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/
- API Docs: http://127.0.0.1:8000/api/docs/

### Produccion (Linux Server)

```bash
# Despliegue automatico
chmod +x scripts/deploy_linux.sh
sudo ./scripts/deploy_linux.sh
```

**Incluye:**
- Nginx como proxy inverso
- Gunicorn como servidor WSGI
- PostgreSQL como base de datos
- Systemd services para auto-inicio
- SSL/HTTPS con Let's Encrypt

**Documentacion:** `docs/guias/DEPLOYMENT-PRODUCTION.md`

---

## Monitoreo y Logs

### Sistema de Logs

```
proyecto/src/backend/logs/
├── general.log     - Logs generales
├── errors.log      - Solo errores
├── api.log         - Peticiones API
└── auth.log        - Autenticacion
```

**Ver logs en tiempo real:**
```bash
scripts\ver_logs.bat
```

### Metricas

- Peticiones por endpoint
- Tiempo de respuesta
- Errores 4xx/5xx
- Usuarios activos
- Recursos mas usados

---

## Escalabilidad

### Arquitectura Preparada Para Crecer

**Actual (Desarrollo):**
```
Django (0.0.0.0:8000)
    ├── SQLite
    └── Archivos estaticos locales
```

**Produccion (Escalable):**
```
Nginx (Puerto 80/443)
    ↓
Gunicorn (Multiple workers)
    ↓
Django Apps
    ├── PostgreSQL (Base de datos)
    ├── Redis (Cache + Celery broker)
    ├── Celery Workers (Tareas asincronas)
    └── S3/CloudStorage (Archivos media)
```

### Optimizaciones Implementadas

**Backend:**
- Query optimization (select_related, prefetch_related)
- Database indexing en campos frecuentes
- API pagination (limit/offset)
- Cache de queries frecuentes

**Frontend:**
- Lazy loading de imagenes
- Minificacion de CSS/JS
- Service Worker cache
- Compresion de imagenes

---

## Metricas del Proyecto

### Codigo

```
Backend (Python/Django):
- Lineas de codigo: ~15,000
- Modelos: 47
- APIs: 120+ endpoints
- Tests: 50+

Frontend (JavaScript/CSS):
- Lineas de codigo: ~8,000
- Paginas: 15
- Componentes JS: 25

Total: ~23,000 lineas de codigo
```

### Archivos

```
- Archivos Python: 216
- Archivos JavaScript: 34
- Archivos CSS: 20
- Archivos HTML: 18
- Tests: 19
- Documentacion: 96 MD files
```

### Funcionalidades

```
- 9 modulos principales
- 12 apps Django
- 120+ endpoints API
- 15+ vistas frontend
- PWA completa
- Sistema de logs
- Testing automatizado
```

---

## Demostracion en Vivo

### Flujo para la Presentacion

**1. Inicio (2 min)**
- Mostrar launcher universal
- Iniciar servidor
- Abrir en navegador

**2. Homepage (1 min)**
- Navegacion principal
- Diseño responsive

**3. Login/Registro (2 min)**
- Crear usuario demo
- Login con Google (opcional)

**4. Foros (3 min)**
- Crear post con imagenes
- Comentar
- Dar likes
- Mostrar moderacion

**5. Marketplace (3 min)**
- Publicar producto
- Buscar productos
- Filtros por categoria

**6. Portafolio (2 min)**
- Agregar proyecto
- Agregar certificacion
- Vista publica

**7. PWA (3 min)**
- Instalar en celular
- Mostrar funcionamiento offline
- Notificaciones

**8. Panel Admin (2 min)**
- Dashboard
- Gestion de usuarios
- Moderacion de reportes

**Total: ~18-20 minutos**

---

## Recursos para la Presentacion

### Diapositivas Sugeridas

1. **Portada** - Logo + Nombre del proyecto
2. **Problema** - Fragmentacion de servicios estudiantiles
3. **Solucion** - Plataforma centralizada
4. **Stack Tecnologico** - Django + PWA
5. **Arquitectura** - Diagrama de componentes
6. **Base de Datos** - Diagrama ERD
7. **Modulos** - Grid con iconos de cada modulo
8. **PWA** - Comparacion web vs app nativa
9. **Demo** - Video o demo en vivo
10. **Metricas** - Lineas de codigo, funcionalidades
11. **Testing** - Cobertura de tests
12. **Escalabilidad** - Arquitectura futura
13. **Conclusiones** - Logros y aprendizajes
14. **Q&A** - Preguntas

### Documentos de Apoyo

- `docs/arquitectura/ARQUITECTURA-PRESENTACION.md`
- `docs/modelo-datos/MODELO-DE-DATOS-PRESENTACION.md`
- `docs/tecnologias/TECNOLOGIAS-PRESENTACION.md`
- `docs/academico/DEFENSA-PWA-CAPSTONE.md`

---

## Preguntas Frecuentes (Anticipadas)

**P: Por que Django y no Node.js?**
R: Django ofrece admin panel, ORM robusto, seguridad built-in, y es ideal para proyectos academicos por su claridad y documentacion.

**P: Por que PWA y no app nativa?**
R: PWA permite despliegue instantaneo, sin tiendas de apps, un solo codigo para todas las plataformas, y actualizaciones inmediatas.

**P: Como manejan la escalabilidad?**
R: Arquitectura modular con Django apps independientes, preparado para microservicios, cache con Redis, y CDN para estaticos.

**P: Seguridad de datos sensibles?**
R: JWT con expiracion corta, CSRF protection, XSS prevention, passwords hasheadas con bcrypt, y HTTPS en produccion.

**P: Cuanto tardo el desarrollo?**
R: 4 meses (Agosto-Diciembre 2025), con ~15,000 lineas de backend y ~8,000 de frontend.

**P: Puede adaptarse a otras instituciones?**
R: Si, es completamente modular y configurable por campus, carreras y roles.

---

## Contacto y Recursos

**Repositorio:** https://github.com/JackStar6677-1/students-point  
**Documentacion:** `docs/`  
**Demo Video:** (Grabar con OBS o similar)  

**Equipo:**
- Desarrollo Full Stack
- Testing y QA
- Documentacion

**Agradecimientos:**
- Duoc UC
- Profesores guia
- Compañeros de proyecto

---

**Fecha de ultima actualizacion:** Noviembre 2025  
**Version de este documento:** 1.0

