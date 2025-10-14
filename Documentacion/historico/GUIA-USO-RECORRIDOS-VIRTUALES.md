# Guía de Uso - Recorridos Virtuales

## Inicio Rápido

### Windows
```bash
probar_recorridos_virtuales.bat
```

### Manual
```bash
cd proyecto/src/backend
python manage.py runserver
```

Luego abre: http://127.0.0.1:8000/streetview/

---

## Flujo de Navegación

### 1. Pantalla de Selección de Sede

Al acceder a `/streetview/`, verás:

**Elementos visibles:**
- 🏛️ Icono grande de universidad (dorado)
- Título: "Recorridos Virtuales DuocUC"
- Descripción: "Explora nuestras sedes con recorridos interactivos en 360°"
- Card central con:
  - Título: "Selecciona una Sede"
  - Dropdown selector con opciones:
    - ✅ DuocUC Sede Maipú (disponible)
    - 🔒 DuocUC Sede Central (próximamente)
    - 🔒 DuocUC Sede San Carlos (próximamente)
    - 🔒 DuocUC Sede Viña del Mar (próximamente)
    - 🔒 DuocUC Sede Valparaíso (próximamente)
  - Botón: "Explorar Recorridos" (inicialmente deshabilitado)

**Acción:** 
1. Selecciona "DuocUC Sede Maipú" en el dropdown
2. El botón "Explorar Recorridos" se habilita
3. Haz clic en el botón

---

### 2. Pantalla de Recorridos Disponibles

Después de seleccionar la sede, verás:

**Elementos visibles:**
- Botón "← Cambiar Sede" (arriba)
- Título: "Recorridos Disponibles - DuocUC Sede Maipú"
- Grid de 7 cards con iconos:

#### Card 1: Biblioteca 📚
- **Estado:** Próximamente
- **Icono:** Libro (color cyan)
- **Descripción:** "Explora nuestra biblioteca con recursos académicos"
- **Badge:** "Próximamente" (gris)
- **Interacción:** No clickeable

#### Card 2: Casino 🍽️
- **Estado:** ✅ DISPONIBLE
- **Icono:** Cubiertos (color cyan)
- **Descripción:** "Recorrido por el casino y espacios de alimentación"
- **Interacción:** ✅ Clickeable - Abre el visor de diapositivas

#### Card 3: Administración 🏢
- **Estado:** Próximamente
- **Icono:** Edificio (color cyan)
- **Descripción:** "Conoce las oficinas administrativas"
- **Badge:** "Próximamente" (gris)
- **Interacción:** No clickeable

#### Card 4: Baños 🚻
- **Estado:** Con sub-menú
- **Icono:** Restroom (color cyan)
- **Descripción:** "Ubicación de baños por piso"
- **Interacción:** ✅ Clickeable - Abre sub-menú

#### Card 5: Punto Estudiantil ℹ️
- **Estado:** Próximamente
- **Icono:** Info circle (color cyan)
- **Descripción:** "Centro de atención y servicios estudiantiles"
- **Badge:** "Próximamente" (gris)
- **Interacción:** No clickeable

#### Card 6: Salas 👨‍🏫
- **Estado:** Próximamente
- **Icono:** Pizarra (color cyan)
- **Descripción:** "Recorrido por salas de clases"
- **Badge:** "Próximamente" (gris)
- **Interacción:** No clickeable

**Efectos visuales:**
- Al hacer hover sobre las cards disponibles:
  - Se elevan 8px
  - Aparece un borde cyan brillante
  - Sombra con glow cyan
  - Línea dorada en la parte superior se expande

---

### 3. Sub-menú de Baños (Al hacer clic en "Baños")

**Elementos visibles:**
- Botón "← Volver a Recorridos" (arriba)
- Título: "Baños - DuocUC Sede Maipú"
- Grid de 5 cards:

1. **Baños Primer Piso** 🚻
   - Estado: Próximamente
   - Descripción: "Ubicación de baños en el primer piso"

2. **Baños Segundo Piso** 🚻
   - Estado: Próximamente
   - Descripción: "Ubicación de baños en el segundo piso"

3. **Baños Tercer Piso** 🚻
   - Estado: Próximamente
   - Descripción: "Ubicación de baños en el tercer piso"

4. **Baños Cuarto Piso** 🚻
   - Estado: Próximamente
   - Descripción: "Ubicación de baños en el cuarto piso"

5. **Baños Subterráneo** 🚻
   - Estado: Próximamente
   - Descripción: "Ubicación de baños en el subterráneo"

**Acción:** Haz clic en "← Volver a Recorridos" para regresar

---

### 4. Visor de Diapositivas (Al hacer clic en "Casino")

El visor se abre en pantalla completa con fondo negro.

#### Header (arriba)
**Elementos:**
- **Izquierda:**
  - Título: "Casino" (color dorado)
  - Subtítulo: "DuocUC Sede Maipú" (gris)
- **Derecha:**
  - Contador: "1 / 5" (en badge redondeado)
  - Botón: "✕ Salir" (blanco)

#### Área Principal (centro)
**Elementos:**
- Imagen actual en grande (máximo 100% de pantalla)
- Cada imagen tiene:
  - **Título:** Superpuesto (opcional, puedes activar el overlay)
  - **Descripción:** Superpuesta (opcional)

**Las 5 imágenes disponibles:**
1. **Entrada al Casino**
   - "Vista principal de la entrada al casino estudiantil"
   
2. **Área de Servicio**
   - "Zona de servicio y atención del casino"
   
3. **Comedor Principal**
   - "Amplio espacio del comedor para estudiantes"
   
4. **Zona de Mesas**
   - "Área de mesas y asientos para disfrutar tus alimentos"
   
5. **Vista General**
   - "Vista panorámica del casino estudiantil"

#### Controles de Navegación (flotantes)
**Elementos:**
- **Flecha Izquierda ←** (circular, lado izquierdo)
  - Deshabilitada en el primer slide
  - Al hacer hover: Se agranda y brilla en cyan
  
- **Flecha Derecha →** (circular, lado derecho)
  - Deshabilitada en el último slide
  - Al hacer hover: Se agranda y brilla en cyan

#### Indicadores (dots) - Parte inferior
**Elementos:**
- 5 puntos circulares pequeños
- El punto activo es dorado y más grande
- Los demás son blancos semi-transparentes
- Clickeable para saltar a cualquier slide
- Al hacer hover: Se agrandan

#### Barra de Progreso (muy abajo)
**Elementos:**
- Barra delgada (4px) en la parte inferior
- Color: Gradiente cyan → dorado
- Se llena progresivamente:
  - 1/5: 20%
  - 2/5: 40%
  - 3/5: 60%
  - 4/5: 80%
  - 5/5: 100%

---

## Controles de Navegación

### 🖱️ Con Mouse (Desktop)
- **Flechas flotantes:** Haz clic en las flechas izquierda/derecha
- **Dots:** Haz clic en cualquier punto para saltar a ese slide
- **Botón Salir:** Haz clic en "✕ Salir" en el header

### ⌨️ Con Teclado
- **← (Flecha izquierda):** Slide anterior
- **→ (Flecha derecha):** Siguiente slide
- **Espacio:** Siguiente slide
- **Escape:** Salir del visor
- **Home:** Ir al primer slide
- **End:** Ir al último slide

### 👆 Con Touch (Mobile/Tablet)
- **Swipe izquierda:** Siguiente slide
- **Swipe derecha:** Slide anterior
- **Tap en dots:** Saltar a ese slide
- **Tap en "Salir":** Cerrar visor

---

## Responsive Design

### 📱 Mobile (< 768px)
**Características:**
- Header en dos líneas (información arriba, controles abajo)
- Imagen ocupa toda la pantalla
- Flechas más pequeñas (45px)
- Dots más pequeños (10px)
- Contador de fuente reducida
- Gestos swipe activados
- Overlay con gradiente para texto legible

**Pantallas recomendadas:**
- iPhone 12/13/14 (390x844)
- Samsung Galaxy S21 (360x800)
- iPad (768x1024)

### 💻 Desktop (> 992px)
**Características:**
- Header en una línea
- Imagen con márgenes laterales
- Flechas grandes (60px)
- Dots grandes (12px)
- Contador de fuente normal
- Navegación por teclado optimizada

### 🖥️ Tablet (768px - 992px)
**Características:**
- Layout intermedio
- Controles medianos (50px)
- Imagen adaptada
- Funciona tanto touch como mouse

---

## Animaciones y Transiciones

### Al cambiar de slide:
- **Duración:** 300-500ms
- **Efecto:** Fade in/out
- **Suavidad:** ease-in-out

### Cards de recorridos:
- **Hover:** Elevación con sombra
- **Duración:** 300ms
- **Efecto:** translateY(-8px)

### Flechas de navegación:
- **Hover:** Scale(1.1) + glow cyan
- **Active:** Scale(0.95)
- **Duración:** 300ms

### Dots:
- **Hover:** Scale(1.2)
- **Active:** Scale especial + color dorado
- **Transición:** 300ms

---

## Rendimiento

### Optimizaciones implementadas:
- ✅ Lazy loading de imágenes (solo primera carga eager)
- ✅ Precarga de siguiente imagen al navegar
- ✅ Transiciones CSS optimizadas (GPU accelerated)
- ✅ Touch events con `passive: true`
- ✅ Debounce en eventos de teclado
- ✅ Optimización de repaint/reflow

### Peso de assets:
- HTML: ~10 KB
- CSS: ~15 KB
- JavaScript: ~12 KB
- Cada imagen: ~200-400 KB (JPEG optimizado)

### Tiempos de carga esperados:
- **Primera carga:** < 2 segundos
- **Cambio de slide:** < 300ms
- **Precarga siguiente:** < 500ms

---

## Troubleshooting

### Problema: "Las imágenes no cargan"
**Solución:**
1. Verifica que las imágenes existen en `proyecto/imagenes/mapa/casino/`
2. Verifica que Django está sirviendo la carpeta `imagenes` correctamente
3. Abre la consola (F12) y revisa errores 404

### Problema: "El visor no se abre"
**Solución:**
1. Abre la consola (F12) y busca errores JavaScript
2. Verifica que `streetview.js` se cargó correctamente
3. Verifica que la función `startSlideshow()` está definida

### Problema: "Los gestos swipe no funcionan en mobile"
**Solución:**
1. Asegúrate de estar en un dispositivo táctil o en modo responsive
2. El swipe requiere mínimo 50px de desplazamiento
3. Verifica que no hay otros event listeners interfiriendo

### Problema: "Las cards no se ven bien"
**Solución:**
1. Limpia la caché del navegador (Ctrl+Shift+R)
2. Verifica que `streetview.css` se cargó correctamente
3. Revisa que no hay conflictos con otros CSS

---

## Personalización

### Cambiar colores:
Edita las variables CSS en `streetview.css`:
```css
:root {
    --primary-color: #0dcaf0;  /* Cyan principal */
    --gold: #ffd700;            /* Dorado */
    --dark-bg: #1a1a1b;         /* Fondo oscuro */
}
```

### Cambiar velocidad de transiciones:
```css
:root {
    --transition: all 0.3s ease; /* Aumenta o reduce 0.3s */
}
```

### Agregar nuevas imágenes:
Edita `streetview.js`:
```javascript
imagenes: [
    {
        url: '/imagenes/mapa/casino/img6casino.jpeg',
        titulo: 'Nueva Imagen',
        descripcion: 'Descripción de la nueva imagen'
    }
]
```

---

## Conclusión

El sistema está completamente funcional y listo para usar. Los únicos recorridos que faltan son:
- Biblioteca
- Administración
- Punto Estudiantil
- Salas
- Baños por piso

Para agregarlos, solo necesitas:
1. Agregar las fotos en `proyecto/imagenes/mapa/[nombre]/`
2. Editar el objeto `recorridosData` en `streetview.js`
3. Cambiar `disponible: false` a `disponible: true`
4. Agregar el array de `imagenes` con las rutas

---

**¿Necesitas ayuda?** Revisa `IMPLEMENTACION-RECORRIDOS-VIRTUALES.md` para más detalles técnicos.

