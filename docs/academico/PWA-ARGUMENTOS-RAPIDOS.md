# PWA: Argumentos Rápidos para Defensa

## "¿No es solo un acceso directo?"

### Respuesta de 30 Segundos

**NO.** Un acceso directo solo abre el navegador. Nuestra PWA:

1. **Tiene Service Worker activo** (sw.js v1.2.4) → Mostrar en DevTools
2. **Funciona offline** → Desconectar WiFi y sigue funcionando
3. **Se instala nativamente** → Sin barra de navegación
4. **Cachea 50+ recursos** → Mostrar Cache Storage
5. **Lighthouse PWA > 80** → Ejecutar en vivo

### Prueba en Vivo (2 minutos)

```
1. F12 → Application → Service Workers ✓
2. Cache Storage → 50+ archivos ✓
3. Network → Offline → Reload → ¡Funciona! ✓
4. Lighthouse → PWA Score ✓
```

---

## Diferencias Técnicas Clave

| Característica | Acceso Directo | StudentsPoint |
|----------------|----------------|---------------|
| Service Worker | ❌ | ✅ sw.js (433 líneas) |
| Funciona offline | ❌ | ✅ 50+ recursos cacheados |
| Caché inteligente | ❌ | ✅ Cache-First + Network-First |
| Instalación nativa | ❌ | ✅ Prompt del navegador |
| Modo standalone | ❌ | ✅ Sin barra URL |
| Actualizaciones | ❌ | ✅ Automáticas (versioning) |
| Manifest | ❌ | ✅ manifest.json completo |
| Iconos | 1 favicon | 8 resoluciones |
| Lighthouse PWA | Falla | Aprueba (80-100) |

---

## Código para Mostrar

### Service Worker (sw.js)

```javascript
// Intercepta TODAS las requests
self.addEventListener('fetch', (event) => {
    // Estrategia Cache-First para estáticos
    if (isStaticFile) {
        event.respondWith(
            caches.match(event.request) || fetch(event.request)
        );
    }
});
```

**Esto NO lo hace un acceso directo.**

---

## Pruebas Preparadas

### Prueba 1: Service Worker (15 seg)
- F12 → Application → Service Workers
- Estado: "activated and is running" ✓

### Prueba 2: Offline (30 seg)
- Navegar páginas
- Network → Offline
- Reload → Funciona ✓

### Prueba 3: Instalación (15 seg)
- Menú → Instalar app
- Mostrar sin barra URL ✓

### Prueba 4: Caché (15 seg)
- Application → Cache Storage
- Mostrar recursos cacheados ✓

### Prueba 5: Lighthouse (30 seg)
- Lighthouse → PWA
- Score > 80 ✓

---

## Si Preguntan...

**P: "¿Cuánto código es PWA?"**

R: 
- sw.js: 433 líneas
- manifest.json: 164 líneas
- pwa-config.js: 279 líneas
- +40 horas de desarrollo

**P: "¿Beneficios reales?"**

R:
- Velocidad: 0ms (caché) vs 500ms (red)
- Funciona sin internet
- Experiencia nativa
- Ahorro de datos

**P: "¿Estándares cumplidos?"**

R: Todos los de Google Lighthouse (15/15 checks)

---

## Demo en 3 Pasos

1. **Mostrar DevTools** (Service Worker + Caché)
2. **Desconectar internet** (sigue funcionando)
3. **Abrir app instalada** (modo standalone)

**Tiempo total: 2 minutos**

---

## Documentación Completa

Ver: `docs/academico/DEFENSA-PWA-CAPSTONE.md`

---

**TIP:** Tener DevTools abierto desde el inicio de la presentación.

