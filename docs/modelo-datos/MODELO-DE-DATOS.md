# Modelo de Datos - StudentsPoint

## Resumen Ejecutivo

StudentsPoint utiliza un **modelo de datos relacional** implementado con Django ORM. La base de datos está diseñada para soportar múltiples módulos funcionales, manteniendo relaciones bien definidas y normalización adecuada. En desarrollo se usa **SQLite** y en producción **PostgreSQL**.

---

## 1. Sistema de Gestión de Base de Datos

### 1.1 Entornos
- **Desarrollo**: SQLite (archivo local `db.sqlite3`)
- **Producción**: PostgreSQL (servidor dedicado)

### 1.2 Características
- **ORM**: Django ORM para abstracción de base de datos
- **Migraciones**: Versionadas y automáticas con Django
- **Índices**: Optimizados para consultas frecuentes
- **Relaciones**: Foreign Keys, Many-to-Many, One-to-One

---

## 2. Entidades Principales

### 2.1 Usuarios y Autenticación

#### User (accounts_user)
Modelo principal de usuario que extiende `AbstractBaseUser`.

**Campos principales**:
- `email` (EmailField, unique): Identificador único del usuario
- `name` (CharField): Nombre del usuario
- `campus` (ForeignKey → Sede): Sede a la que pertenece
- `career` (CharField): Carrera del estudiante
- `role` (CharField): Rol del usuario (student, moderator, director_carrera, admin_global)
- `semestre` (PositiveIntegerField): Semestre actual
- `picture_file` (ImageField): Foto de perfil
- `email_verification_code` (CharField): Código de verificación
- `is_email_verified` (BooleanField): Estado de verificación
- `password_reset_code` (CharField): Código de recuperación
- `google_id` (CharField): ID de Google OAuth
- `date_joined` (DateTimeField): Fecha de registro

**Relaciones**:
- 1:N con Posts
- 1:N con Comentarios
- 1:N con Productos
- 1:N con Encuestas
- 1:1 con PortafolioConfig

#### CambioCarrera (accounts_cambiocarrera)
Registra el historial de cambios de carrera.

**Campos**:
- `usuario` (ForeignKey → User)
- `carrera_anterior` (CharField)
- `carrera_nueva` (CharField)
- `razon` (TextField)
- `fecha_cambio` (DateTimeField)

#### Modelos de Auditoría
- `LoginLog`: Registra intentos de login
- `RegistrationLog`: Registra registros
- `UserActivityLog`: Registra actividad del usuario

---

### 2.2 Foros

#### Foro (forum_foro)
Espacio de discusión por carrera.

**Campos**:
- `sede` (ForeignKey → Sede)
- `carrera` (CharField)
- `titulo` (CharField)
- `slug` (SlugField, unique)
- `es_privado` (BooleanField)
- `descripcion` (TextField)
- `created_at` (DateTimeField)

**Relaciones**:
- 1:N con Posts

#### Post (forum_post)
Publicación en un foro.

**Campos principales**:
- `foro` (ForeignKey → Foro)
- `usuario` (ForeignKey → User)
- `titulo` (CharField)
- `cuerpo` (TextField)
- `tipo` (CharField): comentario, encuesta, imagen, enlace, archivo, otro
- `imagen` (ImageField): Imagen adjunta
- `imagen_aprobada` (BooleanField)
- `archivo` (FileField): Archivo adjunto
- `score` (IntegerField): Puntuación del post
- `estado` (CharField): publicado, revision, oculto, rechazado
- `enlace_url` (URLField): URL asociada
- `total_reportes` (PositiveIntegerField)
- `created_at`, `updated_at` (DateTimeField)

**Relaciones**:
- 1:N con Comentarios
- 1:N con VotosPost
- 1:N con PostReporte
- 1:N con OpcionEncuesta

#### Comentario (forum_comentario)
Comentario en un post.

**Campos**:
- `post` (ForeignKey → Post)
- `usuario` (ForeignKey → User)
- `cuerpo` (TextField)
- `anonimo` (BooleanField)
- `score` (IntegerField)
- `created_at` (DateTimeField)

**Relaciones**:
- 1:N con VotosComentario

#### VotoPost (forum_votopost)
Votos de usuarios sobre posts.

**Campos**:
- `post` (ForeignKey → Post)
- `usuario` (ForeignKey → User)
- `valor` (IntegerField): -1, 0, 1

**Constraints**: `unique_together = ("post", "usuario")`

#### VotoComentario (forum_votocomentario)
Votos sobre comentarios.

**Campos**:
- `comentario` (ForeignKey → Comentario)
- `usuario` (ForeignKey → User)
- `valor` (IntegerField)

**Constraints**: `unique_together = ("comentario", "usuario")`

#### PostReporte (forum_postreporte)
Reportes de posts inapropiados.

**Campos**:
- `post` (ForeignKey → Post)
- `usuario` (ForeignKey → User)
- `tipo` (CharField): spam, contenido_inapropiado, acoso, etc.
- `descripcion` (TextField)
- `estado` (CharField): pendiente, resuelto, descartado
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ("post", "usuario")`

#### OpcionEncuesta (forum_opcionencuesta)
Opciones para posts de tipo encuesta.

**Campos**:
- `post` (ForeignKey → Post)
- `texto` (CharField)
- `votos` (PositiveIntegerField)
- `orden` (PositiveIntegerField)

#### VotoEncuesta (forum_votoencuesta)
Votos en encuestas.

**Campos**:
- `opcion` (ForeignKey → OpcionEncuesta)
- `usuario` (ForeignKey → User)
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ('opcion', 'usuario')`

#### ModeracionEvent (forum_moderacionevent)
Historial de acciones de moderación.

**Campos**:
- `objeto_tipo` (CharField)
- `objeto_id` (PositiveIntegerField)
- `accion` (CharField)
- `razones_json` (JSONField)
- `created_at` (DateTimeField)

---

### 2.3 Marketplace

#### CategoriaProducto (market_categoriaproducto)
Categorías de productos.

**Campos**:
- `nombre` (CharField, unique)
- `descripcion` (TextField)
- `icono` (CharField)
- `activa` (BooleanField)
- `created_at` (DateTimeField)

**Relaciones**:
- 1:N con Productos

#### Producto (market_producto)
Producto del marketplace.

**Campos principales**:
- `vendedor` (ForeignKey → User)
- `titulo` (CharField)
- `descripcion` (TextField)
- `categoria` (ForeignKey → CategoriaProducto)
- `url_principal` (URLField): Enlace obligatorio
- `tipo_enlace` (CharField): facebook, yapo, mercadolibre, otro
- `urls_adicionales` (JSONField): URLs adicionales
- `acepta_terminos` (BooleanField)
- `acepta_responsabilidad` (BooleanField)
- `fecha_aceptacion_terminos` (DateTimeField)
- `ip_aceptacion` (GenericIPAddressField)
- `og_title`, `og_description`, `og_image`, `og_site_name` (CharField/TextField/URLField): Metadatos OpenGraph
- `estado` (CharField): borrador, publicado, vendido, oculto
- `precio` (DecimalField): Precio en CLP
- `precio_student_point` (DecimalField): Precio preferente
- `moneda` (CharField): CLP
- `campus` (ForeignKey → Sede)
- `carrera` (CharField)
- `visualizaciones` (PositiveIntegerField)
- `clicks_enlace` (PositiveIntegerField)
- `created_at`, `updated_at`, `publicado_at`, `vendido_at` (DateTimeField)

**Índices**:
- `['estado', 'publicado_at']`
- `['categoria', 'estado']`
- `['campus', 'carrera']`

**Relaciones**:
- 1:N con ProductoFavorito
- 1:N con ProductoReporte
- 1:1 con ProductoAnalytics

#### ProductoFavorito (market_productofavorito)
Productos marcados como favoritos.

**Campos**:
- `usuario` (ForeignKey → User)
- `producto` (ForeignKey → Producto)
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ['usuario', 'producto']`

#### ProductoReporte (market_productoreporte)
Reportes de productos.

**Campos**:
- `producto` (ForeignKey → Producto)
- `reportador` (ForeignKey → User)
- `tipo` (CharField): fraude, inapropiado, spam, otro
- `descripcion` (TextField)
- `resuelto` (BooleanField)
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ['producto', 'reportador']`

#### ProductoAnalytics (market_productoanalytics)
Analytics de productos.

**Campos**:
- `producto` (OneToOneField → Producto)
- `total_visualizaciones` (PositiveIntegerField)
- `total_clicks` (PositiveIntegerField)
- `total_favoritos` (PositiveIntegerField)
- `total_reportes` (PositiveIntegerField)
- `visualizaciones_por_campus` (JSONField)
- `visualizaciones_por_carrera` (JSONField)
- `ultima_actualizacion` (DateTimeField)

---

### 2.4 Encuestas

#### Poll (polls_poll)
Encuesta independiente.

**Campos principales**:
- `titulo` (CharField)
- `descripcion` (TextField)
- `creador` (ForeignKey → User)
- `multi` (BooleanField): Permite múltiples opciones
- `anonima` (BooleanField)
- `requiere_justificacion` (BooleanField)
- `sedes` (ManyToManyField → Sede)
- `carreras` (JSONField): Lista de carreras
- `mostrar_resultados` (CharField): tiempo_real, al_cierre, solo_moderador
- `estado` (CharField): borrador, activa, cerrada, archivada
- `inicia_at`, `cierra_at` (DateTimeField)
- `post` (OneToOneField → Post, opcional)

**Índices**:
- `['estado', 'inicia_at']`
- `['creador', 'created_at']`

**Relaciones**:
- 1:N con PollOpcion
- 1:N con PollVoto
- 1:1 con PollAnalytics

#### PollOpcion (polls_pollopcion)
Opción de una encuesta.

**Campos**:
- `poll` (ForeignKey → Poll)
- `texto` (CharField)
- `descripcion` (TextField)
- `orden` (PositiveIntegerField)
- `color` (CharField): Color hexadecimal

**Constraints**: `unique_together = ("poll", "texto")`

#### PollVoto (polls_pollvoto)
Voto en una encuesta.

**Campos**:
- `poll` (ForeignKey → Poll)
- `opcion` (ForeignKey → PollOpcion)
- `usuario` (ForeignKey → User)
- `justificacion` (TextField)
- `ip_address` (GenericIPAddressField)
- `user_agent` (TextField)
- `sede_voto` (ForeignKey → Sede)
- `carrera_voto` (CharField)
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ("poll", "usuario", "opcion")`

**Índices**:
- `['poll', 'created_at']`
- `['usuario', 'created_at']`

#### PollAnalytics (polls_pollanalytics)
Analytics de encuestas.

**Campos**:
- `poll` (OneToOneField → Poll)
- `total_visualizaciones` (PositiveIntegerField)
- `total_participantes` (PositiveIntegerField)
- `tasa_participacion` (FloatField)
- `distribucion_sedes` (JSONField)
- `distribucion_carreras` (JSONField)
- `ultima_actualizacion` (DateTimeField)

---

### 2.5 Portafolio

#### Logro (portfolio_logro)
Logros y certificaciones.

**Campos**:
- `usuario` (ForeignKey → User)
- `titulo` (CharField)
- `descripcion` (TextField)
- `tipo` (CharField): academico, profesional, voluntariado, deportivo, cultural, otro
- `fecha_obtencion` (DateField)
- `institucion` (CharField)
- `certificado_url` (URLField)
- `visible` (BooleanField)
- `created_at` (DateTimeField)

#### Proyecto (portfolio_proyecto)
Proyectos del usuario.

**Campos**:
- `usuario` (ForeignKey → User)
- `titulo` (CharField)
- `descripcion` (TextField)
- `tecnologias` (JSONField): Lista de tecnologías
- `estado` (CharField): en_desarrollo, completado, en_pausa, cancelado
- `fecha_inicio`, `fecha_fin` (DateField)
- `url_repositorio`, `url_demo` (URLField)
- `imagenes` (JSONField): URLs de imágenes
- `visible` (BooleanField)
- `created_at` (DateTimeField)

#### ExperienciaLaboral (portfolio_experiencialaboral)
Experiencia laboral.

**Campos**:
- `usuario` (ForeignKey → User)
- `empresa` (CharField)
- `cargo` (CharField)
- `descripcion` (TextField)
- `tipo_contrato` (CharField): practica, part_time, full_time, freelance, voluntariado
- `fecha_inicio`, `fecha_fin` (DateField)
- `actual` (BooleanField)
- `ubicacion` (CharField)
- `visible` (BooleanField)
- `created_at` (DateTimeField)

#### Habilidad (portfolio_habilidad)
Habilidades del usuario.

**Campos**:
- `usuario` (ForeignKey → User)
- `nombre` (CharField)
- `categoria` (CharField): tecnica, blanda, idioma, herramienta
- `nivel` (PositiveIntegerField): 1-5
- `descripcion` (TextField)
- `visible` (BooleanField)
- `created_at` (DateTimeField)

**Constraints**: `unique_together = ['usuario', 'nombre']`

#### PortafolioConfig (portfolio_portafolioconfig)
Configuración del portafolio.

**Campos**:
- `usuario` (OneToOneField → User)
- `titulo_profesional` (CharField)
- `resumen_profesional` (TextField)
- `telefono` (CharField)
- `linkedin_url`, `github_url`, `portfolio_url` (URLField)
- `mostrar_contacto`, `mostrar_redes_sociales`, etc. (BooleanField): Configuración de visualización
- `tema_color` (CharField): Color hexadecimal
- `incluir_foto` (BooleanField)
- `foto_url` (URLField)
- `ultima_generacion` (DateTimeField)
- `version_pdf` (PositiveIntegerField)
- `created_at`, `updated_at` (DateTimeField)

#### PortafolioAnalytics (portfolio_portafolioanalytics)
Analytics del portafolio.

**Campos**:
- `usuario` (OneToOneField → User)
- `completitud_perfil` (FloatField)
- `total_logros`, `total_proyectos`, `total_experiencias`, `total_habilidades` (PositiveIntegerField)
- `visualizaciones_pdf`, `descargas_pdf` (PositiveIntegerField)
- `ultima_visualizacion` (DateTimeField)
- `ultima_actualizacion` (DateTimeField)

---

### 2.6 Sedes y Campus

#### Sede (campuses_sede)
Sede física de la institución.

**Campos**:
- `slug` (SlugField, unique)
- `nombre` (CharField)
- `direccion` (CharField)
- `lat`, `lng` (FloatField): Coordenadas geográficas

**Relaciones**:
- 1:N con Users
- 1:N con Foros
- 1:N con Recorridos
- 1:N con Productos

#### Recorrido (campuses_recorrido)
Tour por una sede.

**Campos**:
- `sede` (ForeignKey → Sede)
- `titulo` (CharField)

**Relaciones**:
- 1:N con RecorridoPaso

#### RecorridoPaso (campuses_recorridopaso)
Paso individual de un recorrido.

**Campos**:
- `recorrido` (ForeignKey → Recorrido)
- `orden` (PositiveIntegerField)
- `titulo` (CharField)
- `descripcion` (TextField)
- `imagen_url` (URLField)
- `lat`, `lng` (FloatField): Coordenadas opcionales
- `usar_streetview` (BooleanField)
- `streetview_heading`, `streetview_pitch`, `streetview_fov` (FloatField)
- `imagen_360_url`, `imagen_360_thumbnail` (URLField)

---

### 2.7 Otros Módulos

#### Curso (otec_curso)
Cursos OTEC.

**Campos principales**:
- `autor` (ForeignKey → User)
- `titulo` (CharField)
- `descripcion` (TextField)
- `tipo` (CharField): personal, externo
- `categoria` (CharField)
- `modalidad` (CharField): presencial, online, hibrido
- `nivel` (CharField): principiante, intermedio, avanzado, todos
- Y más campos...

#### InfraestructuraItem (infrastructure_monitoring_infraestructuraitem)
Reportes de infraestructura.

**Campos principales**:
- `usuario` (ForeignKey → User)
- `tipo` (CharField)
- `descripcion` (TextField)
- `ubicacion` (CharField)
- `estado` (CharField)
- Y más campos...

---

## 3. Diagrama de Relaciones Principales

```
User
  ├──→ Posts (1:N)
  ├──→ Comentarios (1:N)
  ├──→ Productos (1:N)
  ├──→ Encuestas (1:N)
  ├──→ Logros (1:N)
  ├──→ Proyectos (1:N)
  ├──→ ExperienciasLaborales (1:N)
  ├──→ Habilidades (1:N)
  ├──→ PortafolioConfig (1:1)
  └──→ PortafolioAnalytics (1:1)

Sede
  ├──→ Users (1:N)
  ├──→ Foros (1:N)
  ├──→ Recorridos (1:N)
  └──→ Productos (1:N)

Foro
  └──→ Posts (1:N)

Post
  ├──→ Comentarios (1:N)
  ├──→ VotosPost (1:N)
  ├──→ PostReporte (1:N)
  ├──→ OpcionEncuesta (1:N)
  └──→ Poll (1:1, opcional)

Poll
  ├──→ PollOpcion (1:N)
  ├──→ PollVoto (1:N)
  └──→ PollAnalytics (1:1)

Producto
  ├──→ ProductoFavorito (1:N)
  ├──→ ProductoReporte (1:N)
  └──→ ProductoAnalytics (1:1)

CategoriaProducto
  └──→ Productos (1:N)
```

---

## 4. Características del Diseño

### 4.1 Normalización
- **Primera Forma Normal (1NF)**: Todos los campos son atómicos
- **Segunda Forma Normal (2NF)**: Sin dependencias parciales
- **Tercera Forma Normal (3NF)**: Sin dependencias transitivas

### 4.2 Índices
Índices creados para optimizar consultas frecuentes:
- `Post`: `['estado', 'created_at']`
- `Producto`: `['estado', 'publicado_at']`, `['categoria', 'estado']`, `['campus', 'carrera']`
- `Poll`: `['estado', 'inicia_at']`, `['creador', 'created_at']`
- `PollVoto`: `['poll', 'created_at']`, `['usuario', 'created_at']`

### 4.3 Constraints
- **Unique Together**: Evita duplicados (ej: un usuario no puede votar dos veces el mismo post)
- **Foreign Keys**: Mantiene integridad referencial
- **Validators**: Validación a nivel de campo (ej: email, URL)

### 4.4 Campos JSON
Uso de JSONField para datos flexibles:
- `Producto.urls_adicionales`: Lista de URLs
- `Proyecto.tecnologias`: Lista de tecnologías
- `Proyecto.imagenes`: Lista de URLs de imágenes
- `Poll.carreras`: Lista de carreras
- `ProductoAnalytics.visualizaciones_por_campus`: Diccionario
- `PollAnalytics.distribucion_sedes`: Diccionario

---

## 5. Migraciones

### 5.1 Sistema de Migraciones
Django genera automáticamente migraciones cuando se modifican modelos:
- Archivos en `*/migrations/0001_initial.py`, `0002_*.py`, etc.
- Versionadas y reversibles
- Aplicadas con `python manage.py migrate`

### 5.2 Migraciones Principales
- `accounts`: Usuario personalizado, verificación de email, OAuth
- `forum`: Foros, posts, comentarios, votos, reportes
- `market`: Productos, categorías, favoritos, analytics
- `polls`: Encuestas, opciones, votos, analytics
- `portfolio`: Logros, proyectos, experiencias, habilidades
- `campuses`: Sedes, recorridos, pasos

---

## 6. Optimizaciones

### 6.1 Select Related
Uso de `select_related()` para evitar consultas N+1:
```python
Post.objects.select_related('usuario', 'foro')
```

### 6.2 Prefetch Related
Uso de `prefetch_related()` para relaciones Many-to-Many:
```python
Poll.objects.prefetch_related('sedes', 'opciones')
```

### 6.3 Query Optimization
- Índices en campos frecuentemente consultados
- Uso de `only()` y `defer()` para limitar campos
- Agregaciones con `annotate()` y `aggregate()`

---

## 7. Resumen

### 7.1 Estadísticas
- **Total de modelos**: ~30+ modelos principales
- **Apps Django**: 12+ aplicaciones modulares
- **Relaciones**: Múltiples Foreign Keys, Many-to-Many, One-to-One
- **Índices**: Optimizados para consultas frecuentes
- **Constraints**: Unique together, Foreign Keys, Validators

### 7.2 Principios Aplicados
- ✅ Normalización adecuada
- ✅ Integridad referencial
- ✅ Índices optimizados
- ✅ Campos flexibles con JSON
- ✅ Auditoría y logs
- ✅ Soft deletes donde aplica (estados en lugar de eliminación física)

---

## 8. Código de Ejemplo

### 8.1 Definición de Modelo
```python
class Post(models.Model):
    foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estado', 'created_at']),
        ]
```

### 8.2 Consultas Optimizadas
```python
# Con select_related
posts = Post.objects.select_related('usuario', 'foro').filter(estado='publicado')

# Con prefetch_related
polls = Poll.objects.prefetch_related('opciones', 'votos').filter(estado='activa')

# Con agregaciones
from django.db.models import Count
foros = Foro.objects.annotate(total_posts=Count('posts'))
```

---

Este modelo de datos está diseñado para ser **escalable**, **mantenible** y **eficiente**, siguiendo las mejores prácticas de diseño de bases de datos relacionales.

