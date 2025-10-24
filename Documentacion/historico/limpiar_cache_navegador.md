# Limpiar Cache del Navegador

## Para eliminar el cache y ver los cambios:

### Chrome/Edge:
1. Presiona `Ctrl + Shift + Delete`
2. Selecciona "Todo el tiempo"
3. Marca "Imágenes y archivos en caché"
4. Marca "Archivos de aplicaciones web"
5. Haz clic en "Borrar datos"

### Firefox:
1. Presiona `Ctrl + Shift + Delete`
2. Selecciona "Todo"
3. Marca "Caché"
4. Marca "Datos sin conexión del sitio web"
5. Haz clic en "Borrar ahora"

### Alternativa rápida:
- Presiona `Ctrl + F5` (recarga forzada)
- O presiona `F12` → Network → "Disable cache" → Recarga

## Después de limpiar cache:
1. Ve a `/forum/`
2. Verás el nuevo diseño Reddit profesional
3. Los logs ya no mostrarán N+1 Query Alert
4. Solo verás 1 query en lugar de 30

## Verificar en logs:
Busca en la consola del servidor que ya no aparezca:
```
[WARNING] N+1 Query Alert: /api/forum/foros/ ejecuto 30 queries en 0.08s
```

Debería aparecer solo:
```
[INFO] [RESPONSE] GET /api/forum/foros/ - Status: 200 - Tiempo: 0.008s
```
