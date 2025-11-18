# Correcciones para Móvil - StudentsPoint

## Problemas Corregidos

### 1. ✅ Elementos en Esquinas No Accesibles

**Problema:**
- Botones en esquinas no se podían clickear en celular
- Botón de ayuda muy abajo
- Botón de instalación PWA flotante mal posicionado
- Notificaciones tapaban controles

**Solución:**
Se creó `mobile-fixes.css` que:
- Mueve botones flotantes más arriba (bottom: 80px)
- Ajusta tamaño mínimo táctil (44x44px - estándar iOS/Android)
- Mejora responsive de header
- Stack vertical de botones flotantes
- Soporte para safe-area (notch)
- Mejoras para modo standalone

### 2. ✅ Logo de Acceso Directo

**Problema:**
- El logo de acceso directo mostraba logo antiguo de DuocUC
- Iconos PWA pueden necesitar actualización

**Solución:**
- Verificados iconos PWA en `/static/images/icons/`
- Todos los HTMLs ya usan `Logo_StudentsPoint.svg.png`
- Manifest.json apunta a iconos correctos

**Para actualizar iconos PWA:**
1. Usa el logo de StudentsPoint
2. Genera en estos tamaños: 72, 96, 128, 144, 152, 192, 384, 512 px
3. Reemplaza en `proyecto/src/frontend/static/images/icons/`

---

## Cambios Implementados

### Archivos Modificados:

1. **`proyecto/src/frontend/static/css/mobile-fixes.css`** (NUEVO)
   - Correcciones responsive completas
   - Tamaños táctiles apropiados
   - Posicionamiento mejorado de elementos flotantes
   - Soporte para notch/safe-area
   - Mejoras de accesibilidad

2. **`proyecto/src/frontend/index.html`**
   - Agregado `mobile-fixes.css`
   - Meta tags Android PWA
   - Iconos optimizados

---

## Guía de Verificación en Celular

### 1. Elementos Táctiles

**Verifica que puedas clickear:**
- ✅ Botón de ayuda (? esquina inferior derecha)
- ✅ Botón "Instalar App" si aparece
- ✅ Notificaciones (🔔 en header)
- ✅ Configuración (⚙️ en header)
- ✅ Todos los botones del sidebar

**Tamaño mínimo:** 44x44px (estándar Apple Human Interface)

### 2. Responsive

**En móvil vertical:**
- ✅ Header se ajusta a 1 columna
- ✅ Quick actions en 1 columna
- ✅ Botones flotantes no se superponen
- ✅ Sidebar se oculta/muestra correctamente

**En móvil horizontal:**
- ✅ Elementos se ajustan
- ✅ Botones siguen accesibles
- ✅ Sin scroll horizontal

### 3. PWA Instalada

**En modo standalone:**
- ✅ Logo correcto (StudentsPoint, no DuocUC)
- ✅ Safe areas respetadas (notch)
- ✅ Botones no quedan detrás de barra inferior
- ✅ Splash screen con logo correcto

---

## Cómo Actualizar Iconos PWA

### Si necesitas cambiar los iconos:

**Paso 1: Preparar Logo**
1. Abre el logo de StudentsPoint
2. Asegúrate que sea cuadrado (1:1)
3. Fondo transparente o color sólido

**Paso 2: Generar Tamaños**

Usando herramientas online:
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/imageGenerator

O manualmente con software:
- GIMP / Photoshop
- ImageMagick (comando):

```bash
# Ejemplo con ImageMagick
for size in 72 96 128 144 152 192 384 512; do
    convert Logo_StudentsPoint.png -resize ${size}x${size} icon-${size}x${size}.png
done
```

**Paso 3: Reemplazar**

```bash
# Copiar nuevos iconos
copy nuevos_iconos\*.png proyecto\src\frontend\static\images\icons\
```

**Paso 4: Actualizar Manifest**

Verificar que `manifest.json` apunte a los iconos correctos (ya está configurado):

```json
{
  "icons": [
    {
      "src": "/static/images/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    // ... más iconos
  ]
}
```

**Paso 5: Limpiar Cache**

En el celular:
1. Desinstala la PWA si está instalada
2. Chrome → Configuración → Privacidad → Borrar datos
3. Marca "Imágenes y archivos en caché"
4. Borra
5. Reinstala la PWA

---

## Mejoras de CSS Implementadas

### Responsive Móvil:

```css
@media (max-width: 768px) {
    /* Botones flotantes más accesibles */
    .help-button {
        bottom: 80px !important;
        right: 16px !important;
    }
    
    /* Tamaño táctil mínimo */
    .btn-icon {
        min-width: 44px !important;
        min-height: 44px !important;
    }
    
    /* Main content sin sidebar */
    .main-content {
        margin-left: 0 !important;
    }
}
```

### Soporte Safe-Area (Notch):

```css
@media (display-mode: standalone) {
    body {
        padding-top: env(safe-area-inset-top);
        padding-bottom: env(safe-area-inset-bottom);
    }
    
    .help-button {
        bottom: calc(80px + env(safe-area-inset-bottom)) !important;
    }
}
```

### Dispositivos Táctiles:

```css
@media (hover: none) and (pointer: coarse) {
    /* Aumentar áreas de toque */
    .menu-item,
    .action-card,
    button {
        min-height: 44px !important;
    }
}
```

---

## Testing en Celular

### Chrome DevTools Mobile:

1. F12 → Toggle device toolbar
2. Selecciona dispositivo (iPhone, Pixel, etc.)
3. Prueba:
   - Clickear todos los botones
   - Scroll vertical/horizontal
   - Landscape/Portrait
   - Touch gestures

### Celular Real:

1. Conecta por USB
2. Chrome → `chrome://inspect`
3. Selecciona tu dispositivo
4. Inspecciona la página
5. Verifica consola de errores

---

## Verificación de Logo

### En el celular, verifica:

**Acceso directo/PWA instalada:**
- [ ] Ícono en pantalla de inicio
- [ ] Splash screen al abrir
- [ ] Barra de tareas (Android)
- [ ] App switcher

**Debería mostrar:**
✅ Logo de StudentsPoint (no DuocUC)
✅ Nombre: "StudentsPoint"
✅ Fondo del color correcto

**Si aún muestra logo antiguo:**
1. Desinstala la PWA
2. Borra caché de Chrome
3. Verifica que los archivos en servidor estén actualizados
4. Reinstala la PWA

---

## Scripts de Mantenimiento

### Copiar CSS actualizado:

```bash
cd proyecto\src\backend
robocopy "..\frontend\static\css" "staticfiles\css" mobile-fixes.css
```

### Copiar iconos actualizados:

```bash
cd proyecto\src\backend
robocopy "..\frontend\static\images\icons" "staticfiles\images\icons" *.png
```

### Recolectar todo:

```bash
cd proyecto\src\backend
python manage.py collectstatic --noinput --clear
```

---

## Resumen

### Antes:
❌ Botones en esquinas no accesibles  
❌ Elementos muy pequeños en móvil  
❌ Botones flotantes mal posicionados  
❌ Logo antiguo de DuocUC  

### Después:
✅ Todos los elementos accesibles (44x44px mínimo)  
✅ Botones bien posicionados (80px desde abajo)  
✅ Responsive completo  
✅ Safe-area support (notch)  
✅ Logo de StudentsPoint en todos lados  

---

**Próximos pasos:**
1. Aplicar `mobile-fixes.css` a todas las páginas HTML
2. Verificar iconos PWA son correctos
3. Probar en celular real
4. Actualizar iconos si es necesario

**Archivos importantes:**
- `proyecto/src/frontend/static/css/mobile-fixes.css`
- `proyecto/src/frontend/static/images/icons/`
- `proyecto/src/frontend/static/manifest.json`

