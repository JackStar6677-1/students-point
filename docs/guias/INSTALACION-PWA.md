# Guía de Instalación PWA - StudentsPoint

## Versión 1.2.3 - Optimizada para Tailscale y Chrome

Esta guía te ayudará a instalar StudentsPoint como Progressive Web App (PWA) en Chrome navegador y Chrome móvil, incluyendo conexiones a través de Tailscale.

---

## Requisitos Previos

### Hardware y Software
- **Navegador:** Google Chrome 90+ (navegador o móvil)
- **Sistema Operativo:** Windows 10+, macOS, Linux, Android 8+, iOS 16+
- **Conexión:** Red local, Tailscale o HTTPS

### IPs Soportadas
- **Localhost:** `localhost`, `127.0.0.1`
- **Redes Locales:** `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`
- **Tailscale:** Cualquier IP `100.x.x.x` (rango CGNAT)
  - Laptop: `100.75.238.19`
  - Desktop: `100.113.204.115`

---

## Instalación en Chrome Navegador (Escritorio)

### Opción 1: Desde el Botón de Instalación

1. Abre StudentsPoint en Chrome
2. Busca el botón **"Instalar StudentsPoint"** en la esquina superior derecha
3. Haz clic en el botón
4. Confirma la instalación en el diálogo que aparece
5. La aplicación se instalará y abrirá en una ventana independiente

### Opción 2: Desde la Barra de Direcciones

1. Abre StudentsPoint en Chrome
2. Busca el ícono de instalación (⊕ o computadora con flecha) en la barra de direcciones
3. Haz clic en el ícono
4. Selecciona **"Instalar"**
5. Confirma la instalación

### Opción 3: Desde el Menú de Chrome

1. Abre StudentsPoint en Chrome
2. Haz clic en el menú de Chrome (⋮) en la esquina superior derecha
3. Selecciona **"Instalar StudentsPoint..."**
4. Confirma la instalación

---

## Instalación en Chrome Móvil (Android)

### Pasos de Instalación

1. **Abre Chrome** en tu dispositivo Android
2. **Navega** a StudentsPoint usando tu dirección:
   - Local: `http://192.168.x.x:8000`
   - Tailscale: `http://100.75.238.19:8000` (laptop) o `http://100.113.204.115:8000` (desktop)
3. **Toca el menú** (⋮) en la esquina superior derecha
4. **Selecciona** "Agregar a pantalla de inicio" o "Instalar app"
5. **Edita el nombre** si lo deseas (opcional)
6. **Toca "Agregar"** o "Instalar"
7. La aplicación aparecerá en tu pantalla de inicio

### Verificar Instalación

- Busca el ícono de StudentsPoint en tu pantalla de inicio
- Toca el ícono para abrir la app en modo standalone
- La app se abrirá sin la barra de Chrome, como una app nativa

---

## Instalación en Chrome iOS (iPhone/iPad)

**Nota:** Chrome en iOS no soporta completamente PWAs. Se recomienda usar Safari.

### Usando Safari (Recomendado)

1. Abre **Safari** en tu dispositivo iOS
2. Navega a StudentsPoint
3. Toca el botón **Compartir** (cuadrado con flecha hacia arriba)
4. Desplázate y selecciona **"Agregar a pantalla de inicio"**
5. Toca **"Agregar"**

---

## Verificación de la Instalación

### Comprobaciones Básicas

1. **Service Worker Activo**
   - Abre DevTools (F12)
   - Ve a **Application → Service Workers**
   - Verifica que haya un Service Worker activo

2. **Manifest Cargado**
   - Abre DevTools (F12)
   - Ve a **Application → Manifest**
   - Verifica que el manifest esté cargado correctamente

3. **Caché Funcionando**
   - Abre DevTools (F12)
   - Ve a **Application → Cache Storage**
   - Verifica que existan caches de StudentsPoint

### Diagnóstico de PWA

Ejecuta el script de diagnóstico en la consola del navegador:

```javascript
// Abrir DevTools (F12) y pegar en la consola
window.PWAConfig.showPWAInfo();
```

Deberías ver algo como:

```
=== PWA Configuration ===
Environment: tailscaleLaptop
Base URL: http://100.75.238.19:8000
Can PWA work: true
Is secure context: true
Has Service Worker: true
Has Notifications: true
Has Install Prompt: true
Debug mode: true
Cache strategy: networkFirst
========================
```

---

## Solución de Problemas

### Problema: No aparece el botón de instalación

**Solución:**
1. Verifica que estés usando Chrome 90+
2. Asegúrate de estar en un contexto seguro (localhost, Tailscale, HTTPS)
3. Recarga la página con Ctrl+F5 (limpiar caché)
4. Verifica la consola para errores de Service Worker

### Problema: Error al registrar Service Worker

**Solución:**
1. Abre DevTools → Application → Service Workers
2. Haz clic en **"Unregister"** en todos los Service Workers antiguos
3. Recarga la página
4. Verifica que `sw.js` esté accesible en `http://tu-ip:8000/sw.js`

### Problema: Service Worker no funciona en Tailscale

**Solución:**
1. Verifica que tu IP de Tailscale esté en la lista de ALLOWED_HOSTS en `dev.py`
2. Verifica CSRF_TRUSTED_ORIGINS en `dev.py`
3. Limpia la caché del navegador completamente
4. Desregistra Service Workers antiguos
5. Recarga la página

### Problema: PWA no funciona offline

**Solución:**
1. Verifica que el Service Worker esté activo
2. Navega primero online para cachear recursos
3. Verifica la estrategia de caché en DevTools → Application → Cache Storage
4. Prueba desconectando y navegando a páginas ya visitadas

### Problema: Iconos de la app no se ven

**Solución:**
1. Verifica que los iconos existan en `/static/images/icons/`
2. Abre el manifest.json y verifica las rutas de los iconos
3. Verifica que los iconos sean accesibles desde el navegador
4. Reinstala la PWA después de verificar

---

## Características de la PWA

### Funcionalidad Offline

- **Páginas cacheadas:** Inicio, Foro, Marketplace, Portafolio, etc.
- **Estrategia:** Network First para APIs, Cache First para estáticos
- **Caché dinámico:** Las páginas visitadas se cachean automáticamente

### Notificaciones Push

- **Soporte:** Chrome navegador y Android
- **Configuración:** Automática al instalar la PWA
- **Permisos:** Se solicitan automáticamente

### Sincronización en Background

- **Soporte:** Chrome navegador y Android
- **Funcionalidad:** Sincroniza datos cuando recuperas conexión
- **Automático:** Se ejecuta en segundo plano

---

## Configuración Avanzada

### Cambiar Estrategia de Caché

Edita `pwa-config.js`:

```javascript
const DEV_CONFIG = {
    cacheStrategy: 'networkFirst', // o 'cacheFirst' o 'staleWhileRevalidate'
    cacheTimeout: 5000,
};
```

### Limpiar Caché Manualmente

```javascript
// En la consola del navegador
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(registrations => {
        registrations.forEach(reg => reg.unregister());
    });
}
caches.keys().then(keys => {
    keys.forEach(key => caches.delete(key));
});
```

### Actualizar Service Worker

1. Incrementa la versión en `sw.js`
2. Recarga la página
3. Aparecerá una notificación de actualización disponible
4. Haz clic en "Actualizar"

---

## Especificaciones Técnicas

### Service Worker

- **Versión:** 1.2.3
- **Scope:** `/`
- **Estrategias:** Network First, Cache First, Stale While Revalidate
- **Caché estático:** ~50 archivos
- **Caché dinámico:** Sin límite (se gestiona automáticamente)

### Manifest

- **Display Mode:** Standalone
- **Orientación:** Any (portrait y landscape)
- **Theme Color:** #4A148C (púrpura)
- **Background Color:** #1a1a2e (azul oscuro)
- **Iconos:** 8 tamaños (72x72 a 512x512)

### Compatibilidad

- **Chrome:** 90+ (100%)
- **Edge:** 90+ (100%)
- **Firefox:** 90+ (Limitado)
- **Safari:** 15.4+ (Limitado)
- **Chrome Android:** 90+ (100%)
- **Safari iOS:** 15.4+ (Limitado - usar Safari en lugar de Chrome)

---

## Comandos Útiles

### Iniciar Servidor de Desarrollo

```bash
# Windows
iniciar_desarrollo.bat

# Linux/Mac
./iniciar_desarrollo.sh
```

### Verificar Service Worker

```bash
# En Chrome, navega a:
chrome://serviceworker-internals/
```

### Inspeccionar PWA

```bash
# En Chrome, abre DevTools y ve a:
Application → Manifest
Application → Service Workers
Application → Cache Storage
```

---

## Contacto y Soporte

Si tienes problemas con la instalación de la PWA:

1. Revisa la consola del navegador para errores
2. Ejecuta el diagnóstico de PWA
3. Verifica que todas las configuraciones sean correctas
4. Consulta la documentación completa en `/docs/`

---

**Última actualización:** 18 de Noviembre de 2025
**Versión:** 1.2.3
**Autor:** StudentsPoint Team

