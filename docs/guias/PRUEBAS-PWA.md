# Guía de Pruebas PWA - StudentsPoint

## Checklist de Pruebas v1.2.3

Esta guía contiene todos los tests necesarios para verificar que la PWA funciona correctamente en Chrome navegador y móvil con Tailscale.

---

## Preparación del Entorno

### 1. Ejecutar Script de Instalación

**Windows:**
```bash
cd scripts
instalar_pwa.bat
```

**Linux/Mac:**
```bash
cd scripts
chmod +x instalar_pwa.sh
./instalar_pwa.sh
```

### 2. Iniciar Servidor de Desarrollo

**Windows:**
```bash
iniciar_desarrollo.bat
```

**Linux/Mac:**
```bash
./iniciar_desarrollo.sh
```

### 3. Verificar Servidor Activo

- Abre `http://localhost:8000` en Chrome
- Verifica que la página cargue correctamente
- No debería haber errores en la consola

---

## Pruebas en Chrome Navegador (Escritorio)

### Test 1: Verificar Contexto Seguro

**Objetivo:** Asegurar que Chrome reconoce el contexto como seguro

**Pasos:**
1. Abre Chrome DevTools (F12)
2. Ve a la pestaña Console
3. Ejecuta: `window.isSecureContext`
4. Ejecuta: `window.PWAConfig.showPWAInfo()`

**Resultado Esperado:**
- `window.isSecureContext` debe ser `true`
- La función debe mostrar:
  ```
  Can PWA work: true
  Is secure context: true
  Has Service Worker: true
  ```

**Estado:** ☐ Pass ☐ Fail

---

### Test 2: Registro del Service Worker

**Objetivo:** Verificar que el Service Worker se registra correctamente

**Pasos:**
1. Abre Chrome DevTools (F12)
2. Ve a Application → Service Workers
3. Verifica que aparezca un Service Worker con scope "/"
4. Verifica que el estado sea "activated and is running"

**Resultado Esperado:**
- Service Worker registrado
- Estado: Activo
- Scope: "/"
- Script: `/sw.js` o `/static/sw.js`

**Estado:** ☐ Pass ☐ Fail

---

### Test 3: Carga del Manifest

**Objetivo:** Verificar que el manifest.json se carga correctamente

**Pasos:**
1. Abre Chrome DevTools (F12)
2. Ve a Application → Manifest
3. Verifica que se muestre el manifest con:
   - Name: "StudentsPoint - Plataforma Integral Estudiantil"
   - Short name: "StudentsPoint"
   - Start URL: "/?source=pwa"
   - Theme color: "#4A148C"

**Resultado Esperado:**
- Manifest cargado sin errores
- Todos los iconos marcados como disponibles
- No debe haber advertencias

**Estado:** ☐ Pass ☐ Fail

---

### Test 4: Caché de Archivos Estáticos

**Objetivo:** Verificar que los archivos se cachean correctamente

**Pasos:**
1. Navega por la aplicación (Inicio, Foro, Marketplace)
2. Abre DevTools → Application → Cache Storage
3. Verifica que existan los caches:
   - StudentsPoint-static-v1.2.3
   - StudentsPoint-dynamic-v1.2.3

**Resultado Esperado:**
- Al menos 2 caches creados
- Cache estático con ~30-50 archivos
- Cache dinámico con páginas visitadas

**Estado:** ☐ Pass ☐ Fail

---

### Test 5: Botón de Instalación

**Objetivo:** Verificar que aparece el botón de instalación

**Pasos:**
1. Busca el botón "Instalar StudentsPoint" en la página
2. O busca el ícono de instalación en la barra de direcciones
3. Haz clic en el botón/ícono

**Resultado Esperado:**
- Aparece diálogo de instalación
- Diálogo muestra nombre e ícono de la app
- Se puede confirmar la instalación

**Estado:** ☐ Pass ☐ Fail

---

### Test 6: Instalación de la PWA

**Objetivo:** Instalar la PWA y verificar que funciona

**Pasos:**
1. Instala la PWA desde el botón o barra de direcciones
2. La app debería abrirse en una nueva ventana
3. Verifica que la ventana no tenga barra de direcciones
4. Verifica que el título sea "StudentsPoint"

**Resultado Esperado:**
- App instalada exitosamente
- Se abre en ventana standalone
- No hay barra de direcciones
- Ícono correcto en la barra de tareas

**Estado:** ☐ Pass ☐ Fail

---

### Test 7: Funcionamiento Offline

**Objetivo:** Verificar que la app funciona sin conexión

**Pasos:**
1. Con la PWA instalada y abierta
2. Navega a varias páginas (Inicio, Foro, Marketplace)
3. Abre DevTools → Network
4. Marca "Offline"
5. Navega nuevamente a las páginas visitadas

**Resultado Esperado:**
- Las páginas ya visitadas cargan desde cache
- Aparece mensaje de "Sin conexión" al intentar cargar datos nuevos
- No hay errores críticos

**Estado:** ☐ Pass ☐ Fail

---

### Test 8: Actualización del Service Worker

**Objetivo:** Verificar que las actualizaciones se manejan correctamente

**Pasos:**
1. Cambia la versión en `sw.js` (por ejemplo, a 1.2.4)
2. Recarga la página
3. Debería aparecer notificación de actualización

**Resultado Esperado:**
- Aparece banner de "Nueva versión disponible"
- Al hacer clic en "Actualizar", la página se recarga
- Service Worker se actualiza a la nueva versión

**Estado:** ☐ Pass ☐ Fail

---

## Pruebas con Tailscale (Laptop y Desktop)

### Test 9: Conexión desde Tailscale Laptop

**Objetivo:** Verificar PWA desde Tailscale Laptop

**IP:** `100.75.238.19:8000`

**Pasos:**
1. Abre Chrome en tu laptop conectado a Tailscale
2. Navega a `http://100.75.238.19:8000`
3. Ejecuta: `window.PWAConfig.showPWAInfo()`
4. Verifica el entorno detectado

**Resultado Esperado:**
```
Environment: tailscaleLaptop
Base URL: http://100.75.238.19:8000
Can PWA work: true
Is secure context: true
Has Service Worker: true
isTailscale: true
```

**Estado:** ☐ Pass ☐ Fail

---

### Test 10: Instalación desde Tailscale

**Objetivo:** Instalar PWA desde Tailscale

**Pasos:**
1. Desde `http://100.75.238.19:8000`
2. Haz clic en "Instalar StudentsPoint"
3. Confirma la instalación
4. Verifica que funciona en modo standalone

**Resultado Esperado:**
- Instalación exitosa desde IP Tailscale
- App funciona correctamente
- Service Worker activo
- Cache funcionando

**Estado:** ☐ Pass ☐ Fail

---

### Test 11: Conexión desde Tailscale Desktop

**Objetivo:** Verificar PWA desde otra IP Tailscale

**IP:** `100.113.204.115:8000`

**Pasos:**
1. Desde tu desktop conectado a Tailscale
2. Navega a `http://100.113.204.115:8000`
3. Ejecuta: `window.PWAConfig.showPWAInfo()`

**Resultado Esperado:**
```
Environment: tailscaleDesktop
Base URL: http://100.113.204.115:8000
Can PWA work: true
isTailscale: true
```

**Estado:** ☐ Pass ☐ Fail

---

## Pruebas en Chrome Móvil (Android)

### Test 12: Acceso desde Chrome Android

**Objetivo:** Verificar acceso desde móvil

**Pasos:**
1. Abre Chrome en Android
2. Navega a `http://100.75.238.19:8000` (Tailscale)
3. Verifica que la página carga correctamente
4. Verifica responsive design

**Resultado Esperado:**
- Página carga sin errores
- Diseño responsive funciona
- Sidebar adaptado a móvil
- Touch funciona correctamente

**Estado:** ☐ Pass ☐ Fail

---

### Test 13: Instalación en Android

**Objetivo:** Instalar PWA en Android

**Pasos:**
1. Desde Chrome Android, abre el menú (⋮)
2. Selecciona "Agregar a pantalla de inicio"
3. Confirma la instalación
4. Busca el ícono en la pantalla de inicio
5. Abre la app desde el ícono

**Resultado Esperado:**
- Aparece opción de instalación
- Se agrega ícono a pantalla de inicio
- App abre en modo standalone
- No se ve barra de Chrome

**Estado:** ☐ Pass ☐ Fail

---

### Test 14: Notificaciones en Android

**Objetivo:** Verificar soporte de notificaciones push

**Pasos:**
1. Con la PWA instalada en Android
2. Acepta permisos de notificaciones
3. Envía una notificación de prueba desde el backend

**Resultado Esperado:**
- Aparece solicitud de permisos
- Notificación se recibe correctamente
- Al tocar la notificación, abre la app

**Estado:** ☐ Pass ☐ Fail

---

### Test 15: Funcionamiento en Background (Android)

**Objetivo:** Verificar que la PWA funciona en segundo plano

**Pasos:**
1. Abre la PWA instalada
2. Presiona el botón Home (no cerrar)
3. Espera 5 minutos
4. Abre la PWA nuevamente

**Resultado Esperado:**
- App retoma donde se quedó
- Service Worker sigue activo
- Cache actualizado si había conexión

**Estado:** ☐ Pass ☐ Fail

---

## Pruebas de Rendimiento

### Test 16: Tiempo de Carga Inicial

**Objetivo:** Medir tiempo de primera carga

**Pasos:**
1. Limpia cache completamente
2. Abre DevTools → Network
3. Marca "Disable cache"
4. Recarga la página
5. Revisa el tiempo total de carga

**Resultado Esperado:**
- Tiempo < 3 segundos en conexión buena
- Tiempo < 5 segundos en conexión regular
- DOMContentLoaded < 1 segundo

**Estado:** ☐ Pass ☐ Fail

---

### Test 17: Tiempo de Carga con Cache

**Objetivo:** Medir tiempo de carga desde cache

**Pasos:**
1. Con cache poblado
2. Abre DevTools → Network
3. Recarga la página
4. Revisa tiempo total

**Resultado Esperado:**
- Tiempo < 500ms
- Mayoría de recursos desde cache
- DOMContentLoaded < 200ms

**Estado:** ☐ Pass ☐ Fail

---

## Pruebas de Seguridad

### Test 18: Verificar HTTPS/Contexto Seguro

**Objetivo:** Asegurar que solo funciona en contextos seguros

**Pasos:**
1. Ejecuta: `window.isSecureContext`
2. Verifica protocolos permitidos
3. Intenta acceder desde HTTP no-local (debería fallar)

**Resultado Esperado:**
- Localhost: Seguro ✓
- Tailscale: Seguro ✓
- HTTP externo: No seguro ✗

**Estado:** ☐ Pass ☐ Fail

---

### Test 19: CORS y CSRF

**Objetivo:** Verificar configuración de seguridad

**Pasos:**
1. Abre DevTools → Network
2. Realiza una petición API
3. Verifica headers de respuesta

**Resultado Esperado:**
- CORS permitido para orígenes configurados
- CSRF token presente en peticiones POST
- No hay errores de CORS

**Estado:** ☐ Pass ☐ Fail

---

## Pruebas de Compatibilidad

### Test 20: Chrome Versiones Antiguas

**Objetivo:** Verificar compatibilidad con Chrome 90+

**Resultado Esperado:**
- Chrome 90-100: Funcional ✓
- Chrome 100+: Funcional ✓
- Chrome < 90: Mensaje de actualización

**Estado:** ☐ Pass ☐ Fail

---

### Test 21: Diferentes Resoluciones

**Objetivo:** Verificar responsive design

**Pasos:**
1. Prueba en:
   - 1920x1080 (Desktop)
   - 1366x768 (Laptop)
   - 768x1024 (Tablet)
   - 375x667 (Móvil)

**Resultado Esperado:**
- Layout se adapta correctamente
- Sidebar colapsable en móvil
- Botones accesibles
- Texto legible

**Estado:** ☐ Pass ☐ Fail

---

## Resumen de Resultados

### Estadísticas

- **Total de Tests:** 21
- **Tests Pasados:** ___
- **Tests Fallados:** ___
- **Porcentaje de Éxito:** ___%

### Tests Críticos (Deben pasar)

- ☐ Test 1: Contexto Seguro
- ☐ Test 2: Service Worker
- ☐ Test 3: Manifest
- ☐ Test 6: Instalación PWA
- ☐ Test 9: Tailscale Laptop
- ☐ Test 13: Instalación Android

### Problemas Encontrados

1. _____________________________________
2. _____________________________________
3. _____________________________________

### Soluciones Aplicadas

1. _____________________________________
2. _____________________________________
3. _____________________________________

---

## Comandos de Diagnóstico

### Limpiar Cache Completamente

```javascript
// En la consola del navegador
caches.keys().then(keys => {
    keys.forEach(key => caches.delete(key));
    console.log('Cache limpiado');
});
```

### Desregistrar Service Workers

```javascript
// En la consola del navegador
navigator.serviceWorker.getRegistrations().then(registrations => {
    registrations.forEach(reg => reg.unregister());
    console.log('Service Workers desregistrados');
});
```

### Ver Estado de PWA

```javascript
// En la consola del navegador
window.PWAConfig.showPWAInfo();
```

### Ver Caché Actual

```javascript
// En la consola del navegador
caches.keys().then(keys => {
    console.log('Caches activos:', keys);
    keys.forEach(key => {
        caches.open(key).then(cache => {
            cache.keys().then(requests => {
                console.log(`${key}: ${requests.length} archivos`);
            });
        });
    });
});
```

---

**Fecha de Prueba:** __________________
**Tester:** __________________________
**Versión PWA:** 1.2.3
**Chrome Version:** __________________

---

**Última actualización:** 18 de Noviembre de 2025
**Autor:** StudentsPoint Team

