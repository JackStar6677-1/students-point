# Modelo de Datos

Esta carpeta contiene toda la documentación relacionada con el modelo de datos y base de datos de StudentsPoint.

## Archivos Disponibles

### 📘 MODELO-DE-DATOS.md
**Documento técnico completo** con:
- Sistema de gestión de base de datos
- Todas las entidades principales (User, Foro, Post, Producto, Poll, etc.)
- Relaciones entre entidades
- Diagramas de relaciones
- Características del diseño (normalización, índices, constraints)
- Optimizaciones
- Código de ejemplo
- Estadísticas del modelo

**Úsalo cuando necesites**: Información técnica detallada sobre el modelo de datos.

---

### 📊 MODELO-DE-DATOS-PRESENTACION.md
**Versión para presentación PPT** con:
- Resumen de entidades principales
- Relaciones principales
- Características del diseño
- Diagramas simplificados
- Ventajas del diseño
- Puntos clave por slide

**Úsalo cuando necesites**: Crear slides para presentación sobre el modelo de datos.

---

## Entidades Principales

- **User**: Usuarios del sistema
- **Foro**: Foros por carrera
- **Post**: Publicaciones en foros
- **Comentario**: Comentarios en posts
- **Producto**: Productos del marketplace
- **Poll**: Encuestas
- **Portafolio**: Logros, proyectos, experiencias, habilidades
- **Sede**: Sedes físicas de la institución

**Total**: ~30+ modelos principales en 12+ apps Django modulares

---

## Características del Diseño

- ✅ Normalización (1NF, 2NF, 3NF)
- ✅ Índices optimizados
- ✅ Constraints (unique, foreign keys)
- ✅ Campos JSON flexibles
- ✅ Integridad referencial
- ✅ Auditoría completa

---

## Recomendación de Uso

1. **Para estudiar el modelo**: Lee `MODELO-DE-DATOS.md`
2. **Para crear slides**: Usa `MODELO-DE-DATOS-PRESENTACION.md`

