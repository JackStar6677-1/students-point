/**
 * Script de diagnóstico PWA
 * Ejecutar en la consola del navegador para verificar el estado de la PWA
 */

(function() {
    console.log('=== DIAGNÓSTICO PWA ===');
    
    // 1. Verificar Service Worker
    if ('serviceWorker' in navigator) {
        console.log('✅ Service Worker soportado');
        navigator.serviceWorker.getRegistrations().then(registrations => {
            if (registrations.length > 0) {
                console.log('✅ Service Worker registrado:', registrations.length);
                registrations.forEach((reg, i) => {
                    console.log(`  SW ${i + 1}:`, {
                        scope: reg.scope,
                        active: reg.active ? 'Activo' : 'Inactivo',
                        installing: reg.installing ? 'Instalando' : 'No',
                        waiting: reg.waiting ? 'Esperando' : 'No'
                    });
                });
            } else {
                console.error('❌ No hay Service Workers registrados');
            }
        });
    } else {
        console.error('❌ Service Worker NO soportado');
    }
    
    // 2. Verificar Manifest
    const manifestLink = document.querySelector('link[rel="manifest"]');
    if (manifestLink) {
        console.log('✅ Manifest link encontrado:', manifestLink.href);
        fetch(manifestLink.href)
            .then(r => r.json())
            .then(manifest => {
                console.log('✅ Manifest válido:', {
                    name: manifest.name,
                    short_name: manifest.short_name,
                    start_url: manifest.start_url,
                    display: manifest.display,
                    icons: manifest.icons ? manifest.icons.length : 0
                });
                
                // Verificar iconos
                if (manifest.icons && manifest.icons.length > 0) {
                    manifest.icons.forEach(icon => {
                        fetch(icon.src)
                            .then(r => {
                                if (r.ok) {
                                    console.log(`✅ Icono encontrado: ${icon.src}`);
                                } else {
                                    console.error(`❌ Icono no encontrado: ${icon.src}`);
                                }
                            })
                            .catch(e => console.error(`❌ Error cargando icono ${icon.src}:`, e));
                    });
                }
            })
            .catch(e => console.error('❌ Error cargando manifest:', e));
    } else {
        console.error('❌ No se encontró link al manifest');
    }
    
    // 3. Verificar contexto seguro
    if (window.isSecureContext) {
        console.log('✅ Contexto seguro (HTTPS/localhost)');
    } else {
        console.error('❌ NO es contexto seguro');
    }
    
    // 4. Verificar instalación
    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('✅ PWA instalada (modo standalone)');
    } else {
        console.log('ℹ️ PWA no instalada (modo navegador)');
    }
    
    // 5. Verificar beforeinstallprompt
    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('✅ beforeinstallprompt disponible - PWA es instalable');
    });
    
    console.log('=== FIN DIAGNÓSTICO ===');
    console.log('Para más información, abre DevTools → Application → Manifest');
})();

