# Base de Datos - Resumen Tecnico

## Tecnologia

**Desarrollo:** SQLite  
**Produccion:** PostgreSQL  
**ORM:** Django ORM

**Ubicacion:** `proyecto/src/backend/db.sqlite3`

---

## Tablas Principales (Modelos)

### 1. Usuarios y Autenticacion

#### `accounts_customuser` (Usuario Personalizado)
```sql
CREATE TABLE accounts_customuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,        -- Login principal
    password VARCHAR(128) NOT NULL,            -- Hash bcrypt
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    carrera VARCHAR(100),
    campus_id INTEGER,                         -- FK a campuses_campus
    rol VARCHAR(20),                           -- estudiante/profesor/admin
    avatar VARCHAR(100),                       -- Ruta a imagen
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    google_id VARCHAR(255),                    -- ID de Google OAuth
    FOREIGN KEY (campus_id) REFERENCES campuses_campus(id)
);
```

**Indices:**
- `email` (UNIQUE)
- `campus_id`
- `carrera`

**Relaciones:**
- 1:N con Posts (Foro)
- 1:N con Productos (Marketplace)
- 1:1 con Portafolio
- N:N con Encuestas (via RespuestaEncuesta)
- 1:N con Reportes

---

### 2. Foro

#### `forum_categoria` (Categorias de Foro)
```sql
CREATE TABLE forum_categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,              -- Informatica, Administracion, etc.
    descripcion TEXT,
    slug VARCHAR(100) UNIQUE,
    icono VARCHAR(50),
    color VARCHAR(7),                          -- Hex color
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Datos iniciales:**
- Informatica
- Administracion
- Salud
- Ingenieria
- Construccion
- Turismo
- General

#### `forum_post` (Posts del Foro)
```sql
CREATE TABLE forum_post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor_id INTEGER NOT NULL,                 -- FK a CustomUser
    categoria_id INTEGER NOT NULL,             -- FK a Categoria
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME,
    likes INTEGER DEFAULT 0,
    estado_moderacion VARCHAR(20) DEFAULT 'publicado',  -- pendiente/publicado/rechazado
    es_anonimo BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (autor_id) REFERENCES accounts_customuser(id),
    FOREIGN KEY (categoria_id) REFERENCES forum_categoria(id)
);
```

**Indices:**
- `autor_id`
- `categoria_id`
- `fecha_creacion` (DESC)
- `estado_moderacion`

#### `forum_imagenpost` (Imagenes de Posts)
```sql
CREATE TABLE forum_imagenpost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,                  -- FK a Post
    imagen VARCHAR(100) NOT NULL,              -- Ruta a imagen
    orden INTEGER DEFAULT 0,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES forum_post(id) ON DELETE CASCADE
);
```

#### `forum_comentario` (Comentarios)
```sql
CREATE TABLE forum_comentario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,                  -- FK a Post
    autor_id INTEGER NOT NULL,                 -- FK a CustomUser
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    padre_id INTEGER,                          -- FK a Comentario (para respuestas)
    FOREIGN KEY (post_id) REFERENCES forum_post(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES accounts_customuser(id),
    FOREIGN KEY (padre_id) REFERENCES forum_comentario(id) ON DELETE CASCADE
);
```

#### `forum_postreporte` (Reportes de Posts)
```sql
CREATE TABLE forum_postreporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    reportante_id INTEGER NOT NULL,
    motivo VARCHAR(20) NOT NULL,               -- spam/ofensivo/inapropiado
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',     -- pendiente/revisado/rechazado
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES forum_post(id) ON DELETE CASCADE,
    FOREIGN KEY (reportante_id) REFERENCES accounts_customuser(id)
);
```

---

### 3. Marketplace

#### `market_categoriaproducto` (Categorias de Productos)
```sql
CREATE TABLE market_categoriaproducto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    slug VARCHAR(100) UNIQUE,
    icono VARCHAR(50),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Categorias iniciales:**
- Libros
- Tecnologia
- Ropa
- Accesorios
- Deportes
- Hogar
- Otros

#### `market_producto` (Productos)
```sql
CREATE TABLE market_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendedor_id INTEGER NOT NULL,              -- FK a CustomUser
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INTEGER NOT NULL,             -- FK a CategoriaProducto
    estado VARCHAR(20) DEFAULT 'disponible',    -- disponible/vendido/reservado
    campus_id INTEGER,                         -- FK a Campus
    condicion VARCHAR(20),                     -- nuevo/usado/como_nuevo
    ubicacion VARCHAR(200),
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_vendido DATETIME,
    comprador_id INTEGER,                      -- FK a CustomUser (cuando se vende)
    FOREIGN KEY (vendedor_id) REFERENCES accounts_customuser(id),
    FOREIGN KEY (categoria_id) REFERENCES market_categoriaproducto(id),
    FOREIGN KEY (campus_id) REFERENCES campuses_campus(id),
    FOREIGN KEY (comprador_id) REFERENCES accounts_customuser(id)
);
```

**Indices:**
- `vendedor_id`
- `categoria_id`
- `campus_id`
- `estado`
- `precio`
- `fecha_publicacion` (DESC)

#### `market_imagenproducto` (Imagenes de Productos)
```sql
CREATE TABLE market_imagenproducto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,              -- FK a Producto
    imagen VARCHAR(100) NOT NULL,
    orden INTEGER DEFAULT 0,
    es_principal BOOLEAN DEFAULT FALSE,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES market_producto(id) ON DELETE CASCADE
);
```

---

### 4. Portafolios

#### `portfolio_portafolio` (Portafolio del Usuario)
```sql
CREATE TABLE portfolio_portafolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER UNIQUE NOT NULL,         -- FK a CustomUser (1:1)
    biografia TEXT,
    telefono VARCHAR(20),
    linkedin VARCHAR(200),
    github VARCHAR(200),
    sitio_web VARCHAR(200),
    habilidades TEXT,                          -- JSON string
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME,
    es_publico BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE
);
```

#### `portfolio_proyecto` (Proyectos del Portafolio)
```sql
CREATE TABLE portfolio_proyecto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portafolio_id INTEGER NOT NULL,            -- FK a Portafolio
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    tecnologias VARCHAR(300),
    imagen VARCHAR(100),
    url_demo VARCHAR(200),
    url_repositorio VARCHAR(200),
    fecha_inicio DATE,
    fecha_fin DATE,
    orden INTEGER DEFAULT 0,
    FOREIGN KEY (portafolio_id) REFERENCES portfolio_portafolio(id) ON DELETE CASCADE
);
```

#### `portfolio_certificacion` (Certificaciones)
```sql
CREATE TABLE portfolio_certificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portafolio_id INTEGER NOT NULL,            -- FK a Portafolio
    nombre VARCHAR(200) NOT NULL,
    institucion VARCHAR(200),
    fecha_obtencion DATE,
    url_verificacion VARCHAR(200),
    imagen VARCHAR(100),
    descripcion TEXT,
    FOREIGN KEY (portafolio_id) REFERENCES portfolio_portafolio(id) ON DELETE CASCADE
);
```

---

### 5. Encuestas

#### `polls_encuesta` (Encuestas)
```sql
CREATE TABLE polls_encuesta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    creador_id INTEGER NOT NULL,               -- FK a CustomUser
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    es_anonima BOOLEAN DEFAULT FALSE,
    es_activa BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creador_id) REFERENCES accounts_customuser(id)
);
```

#### `polls_pregunta` (Preguntas de Encuesta)
```sql
CREATE TABLE polls_pregunta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encuesta_id INTEGER NOT NULL,              -- FK a Encuesta
    texto TEXT NOT NULL,
    tipo VARCHAR(20) NOT NULL,                 -- seleccion_unica/seleccion_multiple/texto
    orden INTEGER DEFAULT 0,
    es_obligatoria BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (encuesta_id) REFERENCES polls_encuesta(id) ON DELETE CASCADE
);
```

#### `polls_opcion` (Opciones de Pregunta)
```sql
CREATE TABLE polls_opcion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pregunta_id INTEGER NOT NULL,              -- FK a Pregunta
    texto VARCHAR(200) NOT NULL,
    orden INTEGER DEFAULT 0,
    FOREIGN KEY (pregunta_id) REFERENCES polls_pregunta(id) ON DELETE CASCADE
);
```

#### `polls_respuestaencuesta` (Respuestas de Usuario)
```sql
CREATE TABLE polls_respuestaencuesta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encuesta_id INTEGER NOT NULL,              -- FK a Encuesta
    usuario_id INTEGER,                        -- FK a CustomUser (NULL si es anonima)
    fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (encuesta_id) REFERENCES polls_encuesta(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES accounts_customuser(id),
    UNIQUE(encuesta_id, usuario_id)           -- Un usuario solo responde una vez
);
```

#### `polls_respuestapregunta` (Respuestas a Preguntas)
```sql
CREATE TABLE polls_respuestapregunta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    respuesta_encuesta_id INTEGER NOT NULL,    -- FK a RespuestaEncuesta
    pregunta_id INTEGER NOT NULL,              -- FK a Pregunta
    opcion_id INTEGER,                         -- FK a Opcion (para seleccion)
    texto_respuesta TEXT,                      -- Para preguntas de texto
    FOREIGN KEY (respuesta_encuesta_id) REFERENCES polls_respuestaencuesta(id) ON DELETE CASCADE,
    FOREIGN KEY (pregunta_id) REFERENCES polls_pregunta(id),
    FOREIGN KEY (opcion_id) REFERENCES polls_opcion(id)
);
```

---

### 6. Reportes

#### `reports_reporte` (Reportes de Incidencias)
```sql
CREATE TABLE reports_reporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reportante_id INTEGER NOT NULL,            -- FK a CustomUser
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,            -- infraestructura/limpieza/seguridad/etc
    ubicacion VARCHAR(200),
    prioridad VARCHAR(20) DEFAULT 'media',     -- baja/media/alta/urgente
    estado VARCHAR(20) DEFAULT 'pendiente',     -- pendiente/en_revision/en_proceso/resuelto
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    asignado_a_id INTEGER,                     -- FK a CustomUser (staff)
    campus_id INTEGER,                         -- FK a Campus
    FOREIGN KEY (reportante_id) REFERENCES accounts_customuser(id),
    FOREIGN KEY (asignado_a_id) REFERENCES accounts_customuser(id),
    FOREIGN KEY (campus_id) REFERENCES campuses_campus(id)
);
```

**Indices:**
- `reportante_id`
- `estado`
- `prioridad`
- `fecha_reporte` (DESC)
- `campus_id`

#### `reports_imagenreporte` (Imagenes de Reportes)
```sql
CREATE TABLE reports_imagenreporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporte_id INTEGER NOT NULL,               -- FK a Reporte
    imagen VARCHAR(100) NOT NULL,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reporte_id) REFERENCES reports_reporte(id) ON DELETE CASCADE
);
```

---

### 7. Cursos OTEC

#### `otec_curso` (Cursos)
```sql
CREATE TABLE otec_curso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    instructor VARCHAR(200),
    duracion_horas INTEGER,
    precio DECIMAL(10, 2) DEFAULT 0,
    nivel VARCHAR(20),                         -- basico/intermedio/avanzado
    tipo VARCHAR(20),                          -- presencial/online/hibrido
    fecha_inicio DATE,
    fecha_fin DATE,
    cupos_disponibles INTEGER DEFAULT 0,
    imagen VARCHAR(100),
    es_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `otec_clasevideo` (Videos de Clases)
```sql
CREATE TABLE otec_clasevideo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id INTEGER NOT NULL,                 -- FK a Curso
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    url_video VARCHAR(500),                    -- YouTube, Vimeo, etc.
    duracion_minutos INTEGER,
    orden INTEGER DEFAULT 0,
    FOREIGN KEY (curso_id) REFERENCES otec_curso(id) ON DELETE CASCADE
);
```

#### `otec_inscripcion` (Inscripciones a Cursos)
```sql
CREATE TABLE otec_inscripcion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id INTEGER NOT NULL,                 -- FK a Curso
    estudiante_id INTEGER NOT NULL,            -- FK a CustomUser
    fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo',        -- activo/completado/abandonado
    progreso INTEGER DEFAULT 0,                -- 0-100%
    fecha_completado DATETIME,
    FOREIGN KEY (curso_id) REFERENCES otec_curso(id),
    FOREIGN KEY (estudiante_id) REFERENCES accounts_customuser(id),
    UNIQUE(curso_id, estudiante_id)           -- No inscribirse dos veces
);
```

---

### 8. Bienestar

#### `wellbeing_rutina` (Rutinas de Ejercicio)
```sql
CREATE TABLE wellbeing_rutina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),                     -- estiramiento/fuerza/cardio/etc
    duracion_minutos INTEGER,
    nivel_dificultad VARCHAR(20),              -- facil/medio/dificil
    imagen VARCHAR(100),
    video_url VARCHAR(500),
    instrucciones TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### 9. Campus y Mapas

#### `campuses_campus` (Campus)
```sql
CREATE TABLE campuses_campus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    direccion VARCHAR(300),
    ciudad VARCHAR(100),
    region VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    latitud DECIMAL(10, 7),
    longitud DECIMAL(10, 7),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### 10. Notificaciones

#### `notifications_notificacion` (Notificaciones)
```sql
CREATE TABLE notifications_notificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,               -- FK a CustomUser
    tipo VARCHAR(50) NOT NULL,                 -- nuevo_comentario/nuevo_mensaje/etc
    titulo VARCHAR(200),
    mensaje TEXT NOT NULL,
    url VARCHAR(500),                          -- Link a la accion
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE
);
```

**Indices:**
- `usuario_id`
- `leida`
- `fecha_creacion` (DESC)

---

## Consultas SQL Utiles

### Ver todos los posts de una categoria
```sql
SELECT p.id, p.titulo, u.nombre, u.apellido, p.fecha_creacion, p.likes
FROM forum_post p
INNER JOIN accounts_customuser u ON p.autor_id = u.id
INNER JOIN forum_categoria c ON p.categoria_id = c.id
WHERE c.slug = 'informatica'
ORDER BY p.fecha_creacion DESC;
```

### Productos mas caros por categoria
```sql
SELECT c.nombre AS categoria, p.nombre, p.precio, u.nombre AS vendedor
FROM market_producto p
INNER JOIN market_categoriaproducto c ON p.categoria_id = c.id
INNER JOIN accounts_customuser u ON p.vendedor_id = u.id
WHERE p.estado = 'disponible'
ORDER BY c.nombre, p.precio DESC;
```

### Encuestas activas con numero de respuestas
```sql
SELECT e.id, e.titulo, e.fecha_inicio, e.fecha_fin, COUNT(r.id) AS total_respuestas
FROM polls_encuesta e
LEFT JOIN polls_respuestaencuesta r ON e.id = r.encuesta_id
WHERE e.es_activa = 1 AND e.fecha_fin > datetime('now')
GROUP BY e.id
ORDER BY e.fecha_inicio DESC;
```

### Reportes pendientes por prioridad
```sql
SELECT r.id, r.titulo, u.nombre, r.prioridad, r.fecha_reporte
FROM reports_reporte r
INNER JOIN accounts_customuser u ON r.reportante_id = u.id
WHERE r.estado = 'pendiente'
ORDER BY 
    CASE r.prioridad
        WHEN 'urgente' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baja' THEN 4
    END,
    r.fecha_reporte ASC;
```

### Usuarios mas activos en el foro
```sql
SELECT u.nombre, u.apellido, COUNT(p.id) AS total_posts
FROM accounts_customuser u
INNER JOIN forum_post p ON u.id = p.autor_id
WHERE p.estado_moderacion = 'publicado'
GROUP BY u.id
ORDER BY total_posts DESC
LIMIT 10;
```

---

## Migracion a PostgreSQL (Produccion)

**Django maneja automaticamente la migracion:**

```bash
# 1. Configurar PostgreSQL en settings/prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'studentspoint_db',
        'USER': 'studentspoint_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 2. Crear base de datos
sudo -u postgres psql
CREATE DATABASE studentspoint_db;
CREATE USER studentspoint_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE studentspoint_db TO studentspoint_user;

# 3. Migrar
python manage.py migrate

# 4. Cargar datos (opcional)
python manage.py loaddata initial_data.json
```

---

## Backup y Restore

### SQLite (Desarrollo)
```bash
# Backup
cp proyecto/src/backend/db.sqlite3 backups/db_backup_$(date +%Y%m%d).sqlite3

# Restore
cp backups/db_backup_20251120.sqlite3 proyecto/src/backend/db.sqlite3
```

### PostgreSQL (Produccion)
```bash
# Backup
pg_dump -U studentspoint_user studentspoint_db > backup.sql

# Restore
psql -U studentspoint_user studentspoint_db < backup.sql
```

---

## Estadisticas Actuales

**Tablas totales:** 47  
**Relaciones principales:** 25  
**Indices:** 35+  
**Constraints:** 50+ (FK, UNIQUE, CHECK)

**Optimizaciones:**
- Indices en campos de busqueda frecuente
- Cascade DELETE para imagenes y comentarios
- UNIQUE constraints para prevenir duplicados
- DEFAULT values para facilitar inserciones

---

Ver diagrama visual completo: `docs/modelo-datos/MODELO-DE-DATOS.md`

