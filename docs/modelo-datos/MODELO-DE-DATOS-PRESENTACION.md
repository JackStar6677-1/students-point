# Modelo de Datos - StudentsPoint
## Documento para Presentación PPT

---

## 1. SISTEMA DE BASE DE DATOS

### Gestión de Base de Datos
- **Desarrollo**: SQLite (archivo local)
- **Producción**: PostgreSQL (servidor dedicado)
- **ORM**: Django ORM para abstracción
- **Migraciones**: Automáticas y versionadas

---

## 2. ENTIDADES PRINCIPALES

### 2.1 Usuarios
- **User**: Usuario principal con email, nombre, carrera, rol
- **CambioCarrera**: Historial de cambios de carrera
- **LoginLog, RegistrationLog, UserActivityLog**: Auditoría

### 2.2 Foros
- **Foro**: Espacio de discusión por carrera
- **Post**: Publicaciones (comentario, encuesta, imagen, etc.)
- **Comentario**: Comentarios en posts
- **VotoPost, VotoComentario**: Sistema de votación
- **PostReporte**: Reportes de contenido inapropiado

### 2.3 Marketplace
- **CategoriaProducto**: Categorías de productos
- **Producto**: Productos con enlaces externos
- **ProductoFavorito**: Productos favoritos
- **ProductoAnalytics**: Estadísticas de productos

### 2.4 Encuestas
- **Poll**: Encuestas independientes
- **PollOpcion**: Opciones de encuesta
- **PollVoto**: Votos de usuarios
- **PollAnalytics**: Analytics de encuestas

### 2.5 Portafolio
- **Logro**: Logros y certificaciones
- **Proyecto**: Proyectos realizados
- **ExperienciaLaboral**: Experiencia laboral
- **Habilidad**: Habilidades técnicas y blandas
- **PortafolioConfig**: Configuración del portafolio
- **PortafolioAnalytics**: Analytics del portafolio

### 2.6 Sedes y Campus
- **Sede**: Sedes físicas de la institución
- **Recorrido**: Tours por sedes
- **RecorridoPaso**: Pasos individuales de recorridos

---

## 3. RELACIONES PRINCIPALES

```
User
  ├──→ Posts (1:N)
  ├──→ Comentarios (1:N)
  ├──→ Productos (1:N)
  ├──→ Encuestas (1:N)
  ├──→ Logros, Proyectos, Experiencias, Habilidades (1:N)
  └──→ PortafolioConfig (1:1)

Sede
  ├──→ Users (1:N)
  ├──→ Foros (1:N)
  ├──→ Recorridos (1:N)
  └──→ Productos (1:N)

Foro → Posts (1:N)
Post → Comentarios (1:N)
Post → Votos, Reportes (1:N)

Poll → PollOpcion (1:N)
Poll → PollVoto (1:N)

Producto → ProductoFavorito, ProductoReporte (1:N)
```

---

## 4. CARACTERÍSTICAS DEL DISEÑO

### 4.1 Normalización
- ✅ Primera Forma Normal (1NF)
- ✅ Segunda Forma Normal (2NF)
- ✅ Tercera Forma Normal (3NF)

### 4.2 Índices Optimizados
- Posts: `['estado', 'created_at']`
- Productos: `['estado', 'publicado_at']`, `['categoria', 'estado']`
- Encuestas: `['estado', 'inicia_at']`

### 4.3 Constraints
- **Unique Together**: Evita duplicados (ej: un usuario no puede votar dos veces)
- **Foreign Keys**: Integridad referencial
- **Validators**: Validación a nivel de campo

### 4.4 Campos JSON
- Listas flexibles: tecnologías, imágenes, URLs
- Diccionarios: analytics, distribuciones

---

## 5. ESTADÍSTICAS

- **Total de modelos**: ~30+ modelos principales
- **Apps Django**: 12+ aplicaciones modulares
- **Relaciones**: Múltiples Foreign Keys, Many-to-Many, One-to-One
- **Índices**: Optimizados para consultas frecuentes

---

## 6. DIAGRAMA SIMPLIFICADO

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     ├──→ Posts ──→ Comentarios
     ├──→ Productos ──→ Favoritos
     ├──→ Encuestas ──→ Votos
     └──→ Portafolio (Logros, Proyectos, etc.)

┌──────────┐
│   Sede   │
└────┬─────┘
     │
     ├──→ Foros ──→ Posts
     ├──→ Recorridos ──→ Pasos
     └──→ Productos
```

---

## 7. VENTAJAS DEL DISEÑO

✅ **Normalización adecuada**: Sin redundancia
✅ **Integridad referencial**: Foreign Keys garantizan consistencia
✅ **Índices optimizados**: Consultas rápidas
✅ **Campos flexibles**: JSON para datos dinámicos
✅ **Auditoría completa**: Logs de actividad
✅ **Escalabilidad**: Preparado para crecimiento

---

## PUNTOS CLAVE PARA PPT

### Slide 1: Sistema de Base de Datos
- SQLite (desarrollo) / PostgreSQL (producción)
- Django ORM
- Migraciones automáticas

### Slide 2: Entidades Principales
- User, Foro, Post, Producto, Poll, Portafolio, Sede
- ~30+ modelos en total

### Slide 3: Relaciones
- 1:N (User → Posts)
- Many-to-Many (Poll → Sedes)
- 1:1 (User → PortafolioConfig)

### Slide 4: Características
- Normalización (1NF, 2NF, 3NF)
- Índices optimizados
- Constraints (unique, foreign keys)
- Campos JSON flexibles

### Slide 5: Ventajas
- Escalable
- Mantenible
- Eficiente
- Integridad de datos

