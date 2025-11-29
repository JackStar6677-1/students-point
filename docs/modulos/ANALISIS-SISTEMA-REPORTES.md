# Análisis del Sistema de Reportes - Extensión a Marketplace y Encuestas

## 📋 Resumen Ejecutivo

Este documento analiza el sistema actual de reportes del foro y propone una extensión para incluir reportes de **Marketplace** y **Encuestas** en el módulo de administración de reportes.

---

## 🔍 Análisis del Sistema Actual

### 1. **Sistema de Reportes del Foro**

#### 1.1 Modelo de Datos (`PostReporte`)

**Ubicación**: `proyecto/src/backend/studentspoint/apps/forum/models.py`

```python
class PostReporte(models.Model):
    """Reportes de usuarios sobre posts inapropiados."""
    
    class TipoReporte(models.TextChoices):
        SPAM = "spam", "Spam"
        CONTENIDO_INAPROPIADO = "contenido_inapropiado", "Contenido Inapropiado"
        ACOSO = "acoso", "Acoso"
        DESINFORMACION = "desinformacion", "Desinformación"
        VIOLENCIA = "violencia", "Violencia"
        OTRO = "otro", "Otro"
    
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        RESUELTO = "resuelto", "Resuelto"
        DESCARTADO = "descartado", "Descartado"
        POST_ELIMINADO = "post_eliminado", "Post Eliminado"
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reportes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    tipo = models.CharField(max_length=30, choices=TipoReporte.choices)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Características clave**:
- ✅ Relación ForeignKey con `Post`
- ✅ Tipos de reporte estandarizados
- ✅ Estados de seguimiento
- ✅ Unique constraint: un usuario solo puede reportar un post una vez
- ✅ Campo `descripcion` opcional para detalles adicionales

#### 1.2 API Endpoints

**Ubicación**: `proyecto/src/backend/studentspoint/apps/forum/views.py`

| Endpoint | Método | Descripción | Permisos |
|----------|--------|-------------|----------|
| `/api/forum/posts/<pk>/reportar/` | POST | Crear reporte de un post | `IsAuthenticated` |
| `/api/forum/posts/<pk>/reportes/` | GET | Listar reportes de un post | `IsAuthenticated` |
| `/api/forum/reportes/<pk>/` | PATCH | Actualizar estado de reporte | `IsModerator` |
| `/api/forum/reportes/todos/` | GET | Listar TODOS los reportes (Admin) | `IsModerator` |

**Vista clave - `TodosReportesListView`**:
```python
class TodosReportesListView(generics.ListAPIView):
    """Lista TODOS los reportes del foro - Solo para administradores."""
    permission_classes = [IsModerator]
    serializer_class = PostReporteSerializer
    
    def get_queryset(self):
        qs = PostReporte.objects.select_related(
            'post', 'post__usuario', 'post__foro', 'usuario'
        ).order_by("-created_at")
        # Filtros opcionales por estado y tipo
        return qs
```

#### 1.3 Serializer

**Ubicación**: `proyecto/src/backend/studentspoint/apps/forum/serializers.py`

```python
class PostReporteSerializer(serializers.ModelSerializer):
    usuario_name = serializers.SerializerMethodField()
    usuario_email = serializers.SerializerMethodField()
    post_titulo = serializers.SerializerMethodField()
    post_cuerpo = serializers.SerializerMethodField()
    post_usuario = serializers.SerializerMethodField()
    post_foro = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
```

**Características**:
- ✅ Incluye información del post reportado
- ✅ Incluye información del usuario que reportó
- ✅ Muestra `display` fields para tipos y estados legibles

#### 1.4 Frontend - Módulo Admin

**Ubicación**: `proyecto/src/frontend/admin/reportes.html` y `proyecto/src/frontend/static/admin/reportes.js`

**Funcionalidades**:
- ✅ Carga todos los reportes desde `/api/forum/reportes/todos/`
- ✅ Renderiza cada reporte con información del post
- ✅ Filtros por estado y tipo
- ✅ Búsqueda por texto
- ✅ Botón "Eliminar Post" que:
  - Elimina el post mediante `DELETE /api/forum/posts/<pk>/`
  - Actualiza automáticamente todos los reportes relacionados a `POST_ELIMINADO`

**Función de eliminación**:
```javascript
async function eliminarPost(postId, reporteId = null) {
    const response = await fetch(`/api/forum/posts/${postId}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    // El backend actualiza automáticamente los reportes
}
```

---

### 2. **Sistema de Reportes del Marketplace**

#### 2.1 Modelo de Datos (`ProductoReporte`)

**Ubicación**: `proyecto/src/backend/studentspoint/apps/market/models.py`

```python
class ProductoReporte(models.Model):
    """Reportes de productos inapropiados o fraudulentos."""
    
    class TiposReporte(models.TextChoices):
        FRAUDE = "fraude", "Posible Fraude"
        INAPROPIADO = "inapropiado", "Contenido Inapropiado"
        SPAM = "spam", "Spam"
        OTRO = "otro", "Otro"
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="reportes")
    reportador = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    tipo = models.CharField(max_length=20, choices=TiposReporte.choices)
    descripcion = models.TextField()
    resuelto = models.BooleanField(default=False)  # ⚠️ Diferente al sistema del foro
    created_at = models.DateTimeField(auto_now_add=True)
```

**Diferencias con `PostReporte`**:
- ⚠️ Usa `resuelto` (Boolean) en lugar de `estado` (CharField con opciones)
- ⚠️ Tipos de reporte diferentes (fraude, inapropiado, spam, otro)
- ⚠️ Campo `descripcion` es **requerido** (no opcional)
- ⚠️ Nombre del campo: `reportador` vs `usuario`

#### 2.2 API Endpoints (Actual)

**Estado actual**: ❌ **NO HAY ENDPOINTS PÚBLICOS PARA REPORTES DE PRODUCTOS**

- No existe endpoint para crear reportes de productos
- No existe endpoint para listar reportes de productos
- No existe endpoint para administrar reportes de productos

**Solo existe**:
- Modelo `ProductoReporte` en la base de datos
- Serializer `ProductoReporteSerializer` (no usado en views)

#### 2.3 Eliminación de Productos

**Ubicación**: `proyecto/src/backend/studentspoint/apps/market/views.py`

**Estado actual**: El `ProductoViewSet` solo tiene `list` y `create`. **NO tiene `destroy`**.

---

### 3. **Sistema de Encuestas (Polls)**

#### 3.1 Modelo de Datos (`Poll`)

**Ubicación**: `proyecto/src/backend/studentspoint/apps/polls/models.py`

**Estado actual**: ❌ **NO EXISTE MODELO DE REPORTES PARA ENCUESTAS**

- No hay `PollReporte` o similar
- No hay sistema de reportes para encuestas
- Las encuestas pueden tener un `post` relacionado (OneToOneField opcional), pero no hay reportes directos

#### 3.2 API Endpoints

**Endpoints existentes**:
- `/api/polls/` - Listar/Crear encuestas
- `/api/polls/<pk>/` - Detalle/Actualizar/Eliminar encuesta
- `/api/polls/<pk>/votar/` - Votar en encuesta
- `/api/polls/<pk>/cerrar/` - Cerrar encuesta

**Estado**: ✅ Existe `destroy` en `PollDetailView` para eliminar encuestas.

---

## 🎯 Propuesta de Implementación

### Objetivo

Extender el módulo de reportes del admin (`/admin/reportes.html`) para mostrar:
1. ✅ Reportes del foro (ya existe)
2. ➕ Reportes del marketplace
3. ➕ Reportes de encuestas (crear sistema)

Y permitir eliminar desde el admin:
- Posts del foro (ya existe)
- Productos del marketplace
- Encuestas

---

### Arquitectura Propuesta

#### Opción 1: Vista Unificada (Recomendada)

Crear una vista que unifique todos los reportes en un solo endpoint:

```
/api/reportes/todos/  (nuevo endpoint unificado)
```

**Ventajas**:
- ✅ Un solo lugar para obtener todos los reportes
- ✅ Fácil de filtrar y ordenar
- ✅ Frontend más simple

**Estructura de respuesta**:
```json
{
  "reportes_foro": [
    {
      "id": 1,
      "tipo": "foro",
      "post": {...},
      "usuario": {...},
      "tipo_reporte": "spam",
      "estado": "pendiente",
      "created_at": "..."
    }
  ],
  "reportes_marketplace": [
    {
      "id": 1,
      "tipo": "marketplace",
      "producto": {...},
      "reportador": {...},
      "tipo_reporte": "fraude",
      "resuelto": false,
      "created_at": "..."
    }
  ],
  "reportes_encuestas": [
    {
      "id": 1,
      "tipo": "encuesta",
      "poll": {...},
      "usuario": {...},
      "tipo_reporte": "inapropiado",
      "estado": "pendiente",
      "created_at": "..."
    }
  ]
}
```

#### Opción 2: Endpoints Separados

Mantener endpoints separados y unificar en el frontend:

```
/api/forum/reportes/todos/      (ya existe)
/api/market/reportes/todos/     (nuevo)
/api/polls/reportes/todos/      (nuevo)
```

**Ventajas**:
- ✅ Mantiene separación de responsabilidades
- ✅ Más fácil de mantener por módulo

**Desventajas**:
- ⚠️ Frontend debe hacer 3 llamadas
- ⚠️ Más complejo de filtrar globalmente

---

### Plan de Implementación Detallado

#### Fase 1: Estandarizar Modelos de Reportes

**1.1 Actualizar `ProductoReporte`**:
- [ ] Cambiar `resuelto` (Boolean) → `estado` (CharField con opciones)
- [ ] Agregar estados: `PENDIENTE`, `RESUELTO`, `DESCARTADO`, `PRODUCTO_ELIMINADO`
- [ ] Hacer `descripcion` opcional (como en `PostReporte`)
- [ ] Renombrar `reportador` → `usuario` (opcional, mantener compatibilidad)

**1.2 Crear `PollReporte`**:
```python
class PollReporte(models.Model):
    """Reportes de encuestas inapropiadas."""
    
    class TipoReporte(models.TextChoices):
        SPAM = "spam", "Spam"
        CONTENIDO_INAPROPIADO = "contenido_inapropiado", "Contenido Inapropiado"
        ACOSO = "acoso", "Acoso"
        DESINFORMACION = "desinformacion", "Desinformación"
        VIOLENCIA = "violencia", "Violencia"
        OTRO = "otro", "Otro"
    
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        RESUELTO = "resuelto", "Resuelto"
        DESCARTADO = "descartado", "Descartado"
        POLL_ELIMINADO = "poll_eliminado", "Encuesta Eliminada"
    
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="reportes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    tipo = models.CharField(max_length=30, choices=TipoReporte.choices)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("poll", "usuario")
```

#### Fase 2: Crear APIs de Reportes

**2.1 Marketplace - Endpoints**:
- [ ] `POST /api/market/productos/<pk>/reportar/` - Crear reporte
- [ ] `GET /api/market/productos/<pk>/reportes/` - Listar reportes de un producto
- [ ] `GET /api/market/reportes/todos/` - Listar todos los reportes (Admin)
- [ ] `PATCH /api/market/reportes/<pk>/` - Actualizar estado de reporte
- [ ] `DELETE /api/market/productos/<pk>/` - Eliminar producto (actualizar reportes)

**2.2 Encuestas - Endpoints**:
- [ ] `POST /api/polls/<pk>/reportar/` - Crear reporte
- [ ] `GET /api/polls/<pk>/reportes/` - Listar reportes de una encuesta
- [ ] `GET /api/polls/reportes/todos/` - Listar todos los reportes (Admin)
- [ ] `PATCH /api/polls/reportes/<pk>/` - Actualizar estado de reporte
- [ ] `DELETE /api/polls/<pk>/` - Ya existe, actualizar para marcar reportes como `POLL_ELIMINADO`

#### Fase 3: Vista Unificada (Opcional)

**3.1 Crear endpoint unificado**:
- [ ] `GET /api/reportes/todos/` - Vista que unifica todos los reportes
- [ ] Parámetros de query: `?tipo=foro|marketplace|encuesta`, `?estado=pendiente`, etc.

#### Fase 4: Actualizar Frontend

**4.1 Actualizar `reportes.js`**:
- [ ] Cargar reportes de los 3 tipos
- [ ] Renderizar con badges diferenciados por tipo
- [ ] Agregar filtro por tipo de contenido (Foro/Marketplace/Encuesta)
- [ ] Botones de eliminación según el tipo:
  - Foro: `eliminarPost(postId)`
  - Marketplace: `eliminarProducto(productoId)` (nuevo)
  - Encuesta: `eliminarPoll(pollId)` (nuevo)

**4.2 Actualizar `reportes.html`**:
- [ ] Agregar opción en filtro: "Tipo de Contenido" (Foro/Marketplace/Encuesta)
- [ ] Actualizar renderizado para mostrar información específica de cada tipo

---

## 📊 Comparación de Modelos

| Característica | PostReporte | ProductoReporte (Actual) | PollReporte (Propuesto) |
|----------------|-------------|--------------------------|-------------------------|
| **Estado** | CharField (4 opciones) | Boolean (`resuelto`) | CharField (4 opciones) |
| **Tipos de Reporte** | 6 tipos | 4 tipos | 6 tipos (igual que foro) |
| **Descripción** | Opcional | Requerido | Opcional |
| **Campo Usuario** | `usuario` | `reportador` | `usuario` |
| **Unique Constraint** | `(post, usuario)` | `(producto, reportador)` | `(poll, usuario)` |
| **Estado Eliminado** | `POST_ELIMINADO` | ❌ No existe | `POLL_ELIMINADO` |

---

## 🔧 Cambios Técnicos Necesarios

### Backend

1. **Migraciones**:
   - [ ] Migración para actualizar `ProductoReporte.resuelto` → `estado`
   - [ ] Migración para crear `PollReporte`

2. **Serializers**:
   - [ ] Actualizar `ProductoReporteSerializer` para incluir campos de display
   - [ ] Crear `PollReporteSerializer` (similar a `PostReporteSerializer`)

3. **Views**:
   - [ ] Crear vistas de reportes para marketplace
   - [ ] Crear vistas de reportes para encuestas
   - [ ] Actualizar `ProductoViewSet` para agregar `destroy` y actualizar reportes
   - [ ] Actualizar `PollDetailView.destroy` para actualizar reportes

4. **URLs**:
   - [ ] Agregar rutas de reportes en `market/urls.py`
   - [ ] Agregar rutas de reportes en `polls/urls.py`

### Frontend

1. **JavaScript**:
   - [ ] Actualizar `reportes.js` para cargar múltiples tipos
   - [ ] Agregar funciones `eliminarProducto()` y `eliminarPoll()`
   - [ ] Actualizar `renderizarReportes()` para mostrar diferentes tipos

2. **HTML**:
   - [ ] Agregar filtro por tipo de contenido
   - [ ] Actualizar estructura de renderizado

---

## 🎨 Diseño de UI Propuesto

### Badges por Tipo de Contenido

- **Foro**: Badge azul con icono `fa-comments`
- **Marketplace**: Badge verde con icono `fa-store`
- **Encuesta**: Badge morado con icono `fa-poll`

### Información a Mostrar

**Para cada reporte**:
- Tipo de contenido (Foro/Marketplace/Encuesta)
- Título/Descripción del contenido reportado
- Autor del contenido
- Usuario que reportó
- Tipo de reporte (Spam, Fraude, etc.)
- Estado (Pendiente/Resuelto/Descartado/Eliminado)
- Fecha del reporte
- Descripción del reporte (si existe)
- Botón "Eliminar [Tipo]" según corresponda

---

## ✅ Checklist de Implementación

### Backend
- [ ] Crear migración para `PollReporte`
- [ ] Crear migración para actualizar `ProductoReporte`
- [ ] Crear `PollReporteSerializer`
- [ ] Actualizar `ProductoReporteSerializer`
- [ ] Crear vistas de reportes para marketplace
- [ ] Crear vistas de reportes para encuestas
- [ ] Agregar `destroy` a `ProductoViewSet`
- [ ] Actualizar `PollDetailView.destroy` para marcar reportes
- [ ] Agregar URLs de reportes

### Frontend
- [ ] Actualizar `reportes.js` para cargar múltiples tipos
- [ ] Agregar funciones de eliminación
- [ ] Actualizar renderizado
- [ ] Agregar filtros en HTML

### Testing
- [ ] Tests para crear reportes de marketplace
- [ ] Tests para crear reportes de encuestas
- [ ] Tests para listar reportes unificados
- [ ] Tests para eliminar productos/encuestas desde admin

---

## 📝 Notas Adicionales

1. **Compatibilidad**: Mantener compatibilidad con reportes existentes de `ProductoReporte` que usan `resuelto=True/False`.

2. **Permisos**: Todos los endpoints de reportes deben requerir `IsAuthenticated` para crear y `IsModerator` para administrar.

3. **Performance**: Considerar usar `select_related` y `prefetch_related` en las vistas de listado para optimizar queries.

4. **Notificaciones**: Considerar agregar notificaciones cuando se resuelve un reporte o se elimina contenido.

---

## 🚀 Próximos Pasos

1. Revisar y aprobar este análisis
2. Decidir entre Opción 1 (Vista Unificada) o Opción 2 (Endpoints Separados)
3. Crear tareas de implementación
4. Implementar Fase 1 (Estandarizar Modelos)
5. Implementar Fase 2 (Crear APIs)
6. Implementar Fase 3 (Vista Unificada si se elige)
7. Implementar Fase 4 (Frontend)
8. Testing y validación

---

**Fecha de creación**: 2025-01-XX  
**Autor**: Análisis del sistema  
**Versión**: 1.0

