# Actualizar Iconos de la PWA

## Problema Detectado

Los iconos de la PWA mostraban el logo antiguo de Duoc UC en lugar del logo de StudentsPoint.

## Solución

He creado un script automatizado que regenera todos los iconos de la PWA con el logo correcto de StudentsPoint.

---

## Pasos para Actualizar los Iconos

### 1. Ejecuta el Script (EN UNA TERMINAL NUEVA)

**IMPORTANTE:** No uses la terminal donde está corriendo el servidor.

Abre una **nueva terminal** y ejecuta:

```bash
scripts\regenerar_iconos_pwa.bat
```

Este script:
- ✅ Verifica que Pillow esté instalado
- ✅ Genera 8 iconos en todos los tamaños necesarios (72x72 hasta 512x512)
- ✅ Usa el logo oficial de StudentsPoint
- ✅ Copia automáticamente los iconos a staticfiles
- ✅ Optimiza las imágenes

### 2. Reinicia el Servidor

Si el servidor Django/ngrok está corriendo:

1. **Detén el servidor** (Ctrl+C en ambas ventanas)
2. **Vuelve a iniciar:**
   ```bash
   iniciar_con_ngrok.bat
   ```

### 3. Actualiza la PWA en el Celular

Para que los nuevos iconos aparezcan en tu celular:

#### Opción A: Actualización Completa (Recomendado)

1. **Desinstala la PWA actual**
   - Mantén presionado el icono de StudentsPoint
   - Selecciona "Desinstalar" o "Eliminar"

2. **Cierra Chrome completamente**
   - Abre el administrador de apps
   - Fuerza el cierre de Chrome
   - O reinicia el celular (más seguro)

3. **Reinstala la PWA**
   - Abre Chrome
   - Ve al enlace de ngrok
   - Haz clic en "Visit Site"
   - Menú (⋮) → "Instalar app"
   - **Ahora verás el logo de StudentsPoint**

#### Opción B: Forzar Actualización de Caché

Si no quieres desinstalar:

1. Abre la PWA
2. Ve a Configuración de la app
3. Borra datos de la app
4. Reinicia la PWA

---

## Verificación

### Iconos Generados

Los iconos se crean en:
```
proyecto/src/frontend/static/images/icons/
  - icon-72x72.png    ✓
  - icon-96x96.png    ✓
  - icon-128x128.png  ✓
  - icon-144x144.png  ✓
  - icon-152x152.png  ✓
  - icon-192x192.png  ✓
  - icon-384x384.png  ✓
  - icon-512x512.png  ✓
```

### Versión Actualizada

La versión del Service Worker se actualizó a `1.2.4` para forzar la recarga del caché:

- `sw.js` → v1.2.4
- `pwa-config.js` → v1.2.4
- `manifest.json` → Sin cambios (solo los iconos)

---

## Troubleshooting

### El icono sigue siendo el antiguo

**Causa:** El caché del navegador/PWA no se actualizó

**Solución:**
1. Desinstala completamente la PWA
2. Borra los datos de Chrome en el celular:
   - Ajustes → Apps → Chrome
   - Almacenamiento → Borrar datos
3. Reinicia el celular
4. Reinstala la PWA

### Script falla al generar iconos

**Causa:** Pillow no está instalado o hay error con la imagen

**Solución:**
```bash
pip install Pillow
```

Si el error persiste, verifica que existe:
```
proyecto/src/frontend/static/images/Logo_StudentsPoint.svg.png
```

### Los iconos se ven pixelados

**Causa:** El logo original tiene baja resolución

**Solución:** El logo StudentsPoint actual es SVG renderizado a PNG de alta calidad. Si se ve pixelado, es porque la imagen original necesita mayor resolución.

---

## Archivos Modificados

### Generados/Actualizados:
- `proyecto/src/frontend/static/images/icons/icon-*.png` (8 archivos)
- `proyecto/src/backend/staticfiles/images/icons/icon-*.png` (copiados automáticamente)

### Versiones Actualizadas:
- `proyecto/src/frontend/static/sw.js` (v1.2.3 → v1.2.4)
- `proyecto/src/frontend/static/pwa-config.js` (v1.2.3 → v1.2.4)

### Scripts Nuevos:
- `regenerar_iconos_pwa.bat` (raíz del proyecto)

---

## Para Subir al Git

Cuando todo esté funcionando, sube los cambios:

```bash
git add -A
git commit -m "Iconos PWA actualizados con logo StudentsPoint - Version 1.2.4"
git push origin main
```

---

## Notas Técnicas

### Formato de Iconos

- **Formato:** PNG con canal alpha (transparencia)
- **Aspect Ratio:** 1:1 (cuadrado)
- **Fondo:** Transparente
- **Optimización:** Activada para reducir tamaño

### Compatibilidad

Los iconos generados son compatibles con:
- ✅ Android (Chrome, Edge, Samsung Internet)
- ✅ iOS (Safari)
- ✅ Desktop PWA (Windows, Mac, Linux)
- ✅ Manifest v3 estándar

### Tamaños y Propósitos

| Tamaño | Uso |
|--------|-----|
| 72x72 | Android (ldpi) |
| 96x96 | Android (mdpi), Windows |
| 128x128 | Chrome Web Store |
| 144x144 | Android (xhdpi), Windows |
| 152x152 | iOS, iPadOS |
| 192x192 | Android (xxhdpi) |
| 384x384 | Android (xxxhdpi) |
| 512x512 | Splash screens, alta resolución |

---

**Fecha de actualización:** 18 de Noviembre 2025  
**Versión PWA:** 1.2.4

