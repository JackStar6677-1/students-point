# Implementacion del Modulo de Cursos Ampliado

**Fecha**: 11 de Noviembre, 2025  
**Objetivo**: Permitir a los usuarios publicar anuncios de clases privadas y compartir enlaces a cursos externos

## Resumen de Implementacion

Se amplio el modulo de cursos existente (app `otec`) para soportar dos tipos de publicaciones:

1. **Anuncios Personales**: Usuarios que ofrecen clases privadas o tutorias
2. **Enlaces Externos**: Compartir cursos de otras plataformas (Coursera, Udemy, etc.)

## Cambios en el Backend

### 1. Modelo Ampliado (`models.py`)

Se agregaron los siguientes campos al modelo `Curso`:

#### Campos Nuevos

- **Tipo de curso**:
  - `tipo`: personal (clases privadas) o externo (enlace a curso)
  - `categoria`: Programacion, Matematicas, Diseño, etc.

- **Detalles**:
  - `modalidad`: presencial, online, hibrido
  - `nivel`: principiante, intermedio, avanzado, todos
  - `duracion`: texto libre (ej: "40 horas", "3 meses")

- **Precio**:
  - `precio`: DecimalField (pesos chilenos)
  - `es_gratuito`: Boolean

- **Contacto** (para anuncios personales):
  - `email_contacto`: Email de contacto
  - `telefono_contacto`: Telefono
  - `url`: URL de contacto o plataforma

- **Metadata**:
  - `imagen_url`: URL de imagen del curso
  - `visualizaciones`: Contador de vistas
  - `created_at`, `updated_at`: Timestamps

#### Metodos Utiles

```python
def esta_vigente() -> bool
def precio_formateado() -> str  # Retorna "$150.000" o "Gratuito"
```

### 2. Serializers Actualizados (`serializers.py`)

#### CursoSerializer (Completo)
- Todos los campos del modelo
- Campos calculados: `vigente`, `precio_formateado`, `autor_nombre`
- Validaciones personalizadas:
  - Anuncios personales requieren al menos un contacto
  - Enlaces externos requieren URL
  - Validacion de fechas

#### CursoListSerializer (Simplificado)
- Version reducida para listados
- Optimizado para performance

### 3. Views Mejoradas (`views.py`)

#### CursoViewSet

**Filtros disponibles** (query parameters):
- `tipo`: personal | externo
- `categoria`: texto
- `modalidad`: presencial | online | hibrido
- `nivel`: principiante | intermedio | avanzado
- `gratuito`: true
- `vigente`: true
- `search`: busqueda en titulo/descripcion/categoria
- `ordering`: created_at, fecha_inicio, precio, visualizaciones, titulo

**Endpoints personalizados**:
- `GET /api/otec/cursos/mis_cursos/` - Cursos del usuario actual
- `GET /api/otec/cursos/categorias/` - Lista de categorias unicas
- `GET /api/otec/cursos/estadisticas/` - Estadisticas generales

**Funcionalidades**:
- Incrementa visualizaciones al ver detalle
- Solo muestra cursos visibles en GET
- Optimizado con `select_related('autor')`

## Cambios en el Frontend

### 1. HTML Modernizado (`cursos.html`)

#### Estructura
- Diseño responsive con Bootstrap 5
- Sistema de grid moderno
- Sidebar de navegacion integrado

#### Secciones Principales

1. **Header con accion**:
   - Boton "Publicar Curso/Clase"
   - Estadisticas visuales

2. **Filtros avanzados**:
   - Busqueda por texto
   - Filtros por tipo, modalidad, nivel
   - Ordenamiento multiple

3. **Grid de cursos**:
   - Cards responsive
   - Imagenes de preview
   - Badges informativos
   - Precio destacado

4. **Modal de publicacion**:
   - Formulario dinamico segun tipo
   - Validacion de campos
   - Campos opcionales claramente marcados

5. **Modal de detalle**:
   - Informacion completa del curso
   - Datos de contacto (para anuncios)
   - Link al curso externo (para enlaces)

### 2. JavaScript Completo (`cursos.js`)

#### Funciones Principales

```javascript
// Carga de datos
cargarEstadisticas()    // Estadisticas generales
cargarCursos()          // Lista de cursos
verDetalleCurso(id)     // Detalle con visualizacion

// Filtrado
filtrarCursos()         // Aplica todos los filtros

// Publicacion
publicarCurso()         // Crea nuevo curso/anuncio
toggleCamposTipo()      // Muestra/oculta campos segun tipo
togglePrecio()          // Maneja campo precio/gratuito
```

#### Validaciones Cliente

- Campos requeridos segun tipo de curso
- Al menos un contacto para anuncios personales
- URL obligatoria para cursos externos
- Fechas validas

## Endpoints de API

### Base URL: `/api/otec/cursos/`

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/` | Lista todos los cursos (con filtros) |
| POST | `/` | Crear nuevo curso |
| GET | `/{id}/` | Detalle de curso (incrementa vistas) |
| PUT | `/{id}/` | Actualizar curso |
| DELETE | `/{id}/` | Eliminar curso |
| GET | `/mis_cursos/` | Cursos del usuario actual |
| GET | `/categorias/` | Categorias disponibles |
| GET | `/estadisticas/` | Estadisticas generales |

### Ejemplos de Uso

#### Crear anuncio de clases personales

```json
POST /api/otec/cursos/
{
    "tipo": "personal",
    "titulo": "Clases de Python para principiantes",
    "descripcion": "Aprende Python desde cero...",
    "categoria": "Programacion",
    "modalidad": "online",
    "nivel": "principiante",
    "duracion": "8 semanas",
    "precio": 50000,
    "email_contacto": "profesor@email.com",
    "telefono_contacto": "+56912345678",
    "fecha_inicio": "2025-12-01"
}
```

#### Compartir curso externo

```json
POST /api/otec/cursos/
{
    "tipo": "externo",
    "titulo": "Curso completo de React en Udemy",
    "descripcion": "Curso gratuito de React...",
    "categoria": "Desarrollo Web",
    "modalidad": "online",
    "nivel": "intermedio",
    "es_gratuito": true,
    "url": "https://udemy.com/curso-react",
    "fecha_inicio": "2025-11-15"
}
```

#### Filtrar cursos

```
GET /api/otec/cursos/?tipo=personal&categoria=Programacion&modalidad=online&ordering=-created_at
```

## Caracteristicas Implementadas

### Backend
- ✅ Modelo extensible con multiples campos
- ✅ Validaciones robustas
- ✅ Filtros multiples
- ✅ Busqueda por texto
- ✅ Ordenamiento flexible
- ✅ Estadisticas en tiempo real
- ✅ Contador de visualizaciones
- ✅ Indices de base de datos optimizados

### Frontend
- ✅ Diseño moderno y responsive
- ✅ Filtros en tiempo real
- ✅ Formulario dinamico segun tipo
- ✅ Validaciones del lado del cliente
- ✅ Mensajes de exito/error
- ✅ Cards con imagenes
- ✅ Badges informativos
- ✅ Modal de detalle completo

## Como Usar

### Para Publicar Clases Privadas

1. Click en "Publicar Curso/Clase"
2. Seleccionar "Clases Privadas / Tutorias"
3. Completar informacion:
   - Titulo y descripcion
   - Categoria y nivel
   - Modalidad (presencial/online/hibrido)
   - Precio o marcar como gratuito
   - **Al menos un medio de contacto**
4. Publicar

### Para Compartir Curso Externo

1. Click en "Publicar Curso/Clase"
2. Seleccionar "Curso Externo"
3. Completar informacion:
   - Titulo y descripcion
   - **URL del curso**
   - Categoria y nivel
   - Precio (si aplica)
4. Publicar

### Para Buscar Cursos

1. Usar barra de busqueda para texto
2. Aplicar filtros:
   - Tipo (personal/externo)
   - Modalidad
   - Nivel
   - Ordenamiento
3. Click en curso para ver detalle

## Migracion Aplicada

```bash
python manage.py makemigrations otec
python manage.py migrate otec
```

**Archivos generados**:
- `0002_alter_curso_options_curso_categoria_curso_created_at_and_more.py`

## Archivos Modificados

```
proyecto/src/backend/studentspoint/apps/otec/
├── models.py           (ampliado)
├── serializers.py      (reescrito)
├── views.py            (mejorado)
└── migrations/
    └── 0002_*.py       (nuevo)

proyecto/src/frontend/cursos/
├── cursos.html         (reescrito)
└── cursos.js           (reescrito)

docs/historico/
└── IMPLEMENTACION-MODULO-CURSOS.md (nuevo)
```

## Proximas Mejoras Sugeridas

1. **Sistema de valoraciones**: Permitir calificar cursos/profesores
2. **Sistema de mensajeria**: Chat directo entre interesados y profesores
3. **Imagenes subidas**: Permitir subir imagenes en lugar de solo URLs
4. **Reservas/Inscripciones**: Sistema de cupos y reservas
5. **Calendario**: Vista de calendario con fechas de inicio
6. **Notificaciones**: Alertas de nuevos cursos por categoria
7. **Favoritos**: Marcar cursos como favoritos
8. **Reportes**: Sistema de reportes para contenido inapropiado

## Notas Tecnicas

- El modelo usa `timezone.now` en lugar de `auto_now_add` para evitar problemas con migraciones
- Los indices estan optimizados para las consultas mas frecuentes
- El contador de visualizaciones se incrementa solo al ver el detalle completo
- Las validaciones estan tanto en backend como frontend para mejor UX
- Los serializers diferentes (List vs Detail) optimizan el performance

## Testing

Para probar el modulo:

1. Iniciar servidor: `python manage.py runserver`
2. Navegar a: `http://localhost:8000/cursos/`
3. Login con usuario valido
4. Probar:
   - Crear anuncio personal
   - Crear enlace externo
   - Filtrar por categorias
   - Ver detalles
   - Verificar estadisticas

## Conclusion

El modulo de cursos ahora es una plataforma completa que permite tanto a profesores ofrecer sus servicios como a estudiantes compartir recursos educativos externos. La implementacion es escalable, con filtros potentes y una interfaz moderna.

