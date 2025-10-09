### Recorridos Virtuales - StudentsPoint

Esta documentación describe la arquitectura, flujo y pautas de desarrollo del módulo de Recorridos Virtuales. Sirve como base para continuar su evolución (nuevos recorridos, integración con API y mejoras UX/PWA).

### Objetivo

- Mostrar recorridos guiados por sede a través de una experiencia por pasos (diapositivas), con soporte desktop y mobile, y compatible con PWA.

### Ubicación de archivos clave

- Página servida en producción: `proyecto/src/backend/staticfiles/streetview/index.html`
- Imágenes del recorrido de Casino (Maipú): `proyecto/imagenes/mapa/casino/` (`img1casino.jpeg` … `img5casino.jpeg`)
- Endpoints backend disponibles (cuando se use API dinámica):
  - `api/campus/campuses/` (lista de campus)
  - `api/campus/tours/?campus=<ID>` (lista de recorridos por campus)
  - `api/campus/tours/<id>/steps/` (pasos de un recorrido)

### Flujo de usuario

1. Selector de sede (precargado con las mismas sedes del registro: Central, Maipú, San Carlos, Valparaíso, Viña del Mar).
2. Cards de recorridos por sede: Casino, Biblioteca, Administración y Salas.
3. Al pulsar “Iniciar Recorrido” se abre un visor de diapositivas con controles:
   - Botones flotantes izquierda/derecha (siempre visibles, sin necesidad de scroll)
   - Puntos (dots) para saltar a cualquier paso
   - Gestos swipe en móvil (derecha/izquierda)

### Estado actual (oct-2025)

- Implementado y operativo: Casino en Sede Maipú (5 imágenes locales).
- Otros recorridos (Biblioteca, Administración, Salas): marcados como “Próximamente” en la UI.
- El selector de sedes es local (lista estática sincronizada con registro). Puede cambiarse a API más adelante.

### Diseño y UX

- Desktop:
  - Diseño de dos columnas: texto a la izquierda e imagen grande a la derecha.
  - Animación de transición lateral entre pasos.
- Mobile:
  - Imagen tipo “hero” (ocupa casi toda la pantalla) con overlay de título y descripción.
  - Gradiente para garantizar legibilidad del texto.
  - Swipe para avanzar/retroceder.

### PWA y desempeño

- La página carga recursos estáticos (`/static/*`) y las imágenes del recorrido desde `/imagenes/...` (servidas por Django en `studentspoint/urls.py`).
- Recomendación: añadir patrón de runtime caching para `/imagenes/mapa/**` en el Service Worker si se desea mayor resiliencia offline.

### Añadir un nuevo recorrido (vía imágenes locales)

1. Crear carpeta de imágenes: `proyecto/imagenes/mapa/<slug_recorrido>/` y añadir archivos con nombres consistentes (por ejemplo, `img1*.jpeg`, `img2*.jpeg`, ...). Resolución sugerida: 1920x1080 o 1600x900 (peso < 400 KB c/u).
2. En `index.html`, mapear temporalmente esas imágenes en el arreglo correspondiente para la sede objetivo, igual que el caso “Casino”.
3. Verificar que las rutas se sirvan correctamente en `http(s)://<host>/imagenes/mapa/<slug_recorrido>/...`.

### Integración con API dinámica (opcional/futuro)

Cuando se disponga de tours en base de datos, usar los endpoints del módulo `campus_map`:

- Lista de campus: `GET /api/campus/campuses/`
- Tours por campus: `GET /api/campus/tours/?campus=<ID>`
- Pasos de un tour: `GET /api/campus/tours/<id>/steps/`

Sugerencia de mapeo en el frontend:

```json
// Respuesta esperada de tours (ejemplo resumido)
[
  {
    "id": 10,
    "title": "Recorrido al Casino",
    "campus": { "id": 2, "name": "Sede Maipú", "slug": "maipu" },
    "steps": [
      { "id": 1, "order": 1, "title": "Entrada", "description": "...", "image": "/imagenes/.../img1.jpeg" },
      { "id": 2, "order": 2, "title": "Hall", "description": "...", "image": "/imagenes/.../img2.jpeg" }
    ]
  }
]
```

Si el endpoint no está disponible, mantener el “fallback” con imágenes locales (como se hace con Casino).

### Importadores (management commands) disponibles

Existen comandos para poblar tours a partir de imágenes locales. Revisión de ejemplos en:

- `proyecto/src/backend/campus_map/management/commands/import_casino_tour.py`
- `proyecto/src/backend/studentspoint/management/commands/import_casino_tour.py`

Uso típico (ajustar a tu app/entorno):

```bash
python manage.py import_casino_tour --campus-slug maipu
```

Esto busca imágenes en `proyecto/imagenes/mapa/casino/` y genera pasos ordenados.

### Convenciones de contenido

- Archivos: usar nombres predecibles (`img1`, `img2`, ...). Evitar espacios.
- Peso: optimizar (TinyPNG/Sharp) para < 400 KB y formato `jpeg`/`webp`.
- Proporción: 16:9 recomendado; mantener encuadres similares para fluidez visual.
- Texto: títulos breves (≤ 40 caracteres) y descripciones concisas (≤ 140 caracteres).

### Accesibilidad (a11y)

- Proveer `alt` descriptivo para las imágenes (si se migra a API, incluir campo `alt`).
- Soporte de teclado (flechas y ESC) se puede reintroducir si se requiere; actualmente móvil usa swipe y desktop usa FABs/dots.

### Roadmap sugerido

- Conectar Biblioteca y Administración a API de tours y definir pasos iniciales.
- Agregar “Salas” con guía ramificada por edificio/piso (menú previo al visor).
- Añadir parallax suave y transición “fade+scale” opcional entre pasos.
- Caching dedicado en SW para `/imagenes/mapa/**` y preload del siguiente paso.
- Panel de administración para crear/ordenar pasos (arrastrar/soltar) y subir imágenes.

### QA/checklist antes de publicar

- [ ] Móvil: overlay legible (contraste AA) y swipe fluido
- [ ] Desktop: botones flotantes visibles y sin saltos de scroll
- [ ] Imágenes optimizadas y rutas válidas `/imagenes/...`
- [ ] PWA: primera carga y navegación offline básica
- [ ] Enlaces de “Próximamente” deshabilitados correctamente


