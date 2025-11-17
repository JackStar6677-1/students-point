# Guía de Despliegue PWA - StudentsPoint

## Requisitos para PWA en Producción

Según las especificaciones de Google, un PWA requiere:

### 1. HTTPS (Obligatorio)
- ✅ La aplicación DEBE estar servida sobre HTTPS
- ✅ Excepciones: localhost, 127.0.0.1, y redes locales (192.168.x.x)

### 2. Manifest.json
- ✅ Ya configurado en `/static/manifest.json`
- ✅ Incluye todos los iconos necesarios (192x192, 512x512)
- ✅ Configurado con `display: "standalone"` para experiencia tipo app

### 3. Service Worker
- ✅ Ya configurado en `/static/sw.js`
- ✅ Registrado automáticamente por `/static/js/pwa.js`
- ✅ Cache strategy configurada

### 4. Configuración Actual

**Manifest.json:**
- `start_url`: "/"
- `scope`: "/"
- `display`: "standalone"
- Iconos: ✅ Configurados (72x72 a 512x512)
- Theme color: #4A148C

**Service Worker:**
- Versión: 1.2.2
- Cache: Configurado para archivos estáticos y dinámicos
- Offline support: ✅ Habilitado

**PWA Config:**
- Producción URL: `https://StudentsPoint.duocuc.cl` (configurado en pwa-config.js)
- Desarrollo: `http://localhost:8000`

## Pasos para Despliegue

### 1. Configurar Dominio con HTTPS

```bash
# Ejemplo con Nginx + Let's Encrypt
sudo certbot --nginx -d studentspoint.duocuc.cl
```

### 2. Verificar Configuración Django

Asegurar que Django sirva el manifest.json y sw.js:

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Asegurar que manifest.json y sw.js sean accesibles
```

### 3. Verificar Headers HTTP

El servidor debe servir con headers correctos:

```
Content-Type: application/manifest+json (para manifest.json)
Content-Type: application/javascript (para sw.js)
Service-Worker-Allowed: / (para permitir scope del SW)
```

### 4. Testing PWA

Usar Chrome DevTools:
1. Abrir DevTools → Application → Manifest
2. Verificar que no haya errores
3. Verificar Service Worker → debe estar "activated"
4. Lighthouse → PWA audit (debe pasar todas las pruebas)

### 5. Verificación Post-Despliegue

```javascript
// En consola del navegador
navigator.serviceWorker.getRegistrations().then(registrations => {
  console.log('Service Workers registrados:', registrations.length);
});

// Verificar manifest
fetch('/static/manifest.json')
  .then(r => r.json())
  .then(manifest => console.log('Manifest:', manifest));
```

## Checklist Pre-Despliegue

- [ ] HTTPS configurado y funcionando
- [ ] Dominio apuntando correctamente
- [ ] manifest.json accesible en `/static/manifest.json`
- [ ] sw.js accesible en `/static/sw.js`
- [ ] Iconos presentes en `/static/images/icons/`
- [ ] Service Worker registrado correctamente
- [ ] Lighthouse PWA score > 90
- [ ] Funciona offline (modo avión)
- [ ] Instalable en móviles (Android/iOS)

## Notas Importantes

1. **HTTPS es OBLIGATORIO** - Sin HTTPS, el PWA no funcionará en producción
2. **Scope del Service Worker** - Debe coincidir con el scope del manifest
3. **Iconos** - Todos los tamaños deben estar presentes
4. **Actualización de Cache** - Cambiar versión en sw.js para forzar actualización

## Comandos Útiles

```bash
# Limpiar cache del Service Worker (desarrollo)
# En DevTools → Application → Service Workers → Unregister

# Forzar actualización del Service Worker
# Cambiar CACHE_NAME en sw.js y recargar

# Verificar PWA con Lighthouse
npm install -g lighthouse
lighthouse https://studentspoint.duocuc.cl --view
```

## Soporte de Navegadores

- ✅ Chrome/Edge (Android/Desktop)
- ✅ Firefox (Android/Desktop)
- ✅ Safari iOS 11.3+ (con limitaciones)
- ✅ Samsung Internet
- ⚠️ Safari Desktop (soporte limitado)

## Troubleshooting

**Service Worker no se registra:**
- Verificar HTTPS
- Verificar que sw.js sea accesible
- Verificar console para errores

**PWA no es instalable:**
- Verificar manifest.json válido
- Verificar iconos presentes
- Verificar HTTPS
- Verificar start_url accesible

**Cache no se actualiza:**
- Cambiar CACHE_NAME en sw.js
- Forzar actualización en DevTools

