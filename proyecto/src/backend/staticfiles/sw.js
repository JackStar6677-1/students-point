/**
 * Service Worker para StudentsPoint
 * Versión: 1.0.0
 */

const CACHE_NAME = 'StudentsPoint-v1.2.0';
const STATIC_CACHE = 'StudentsPoint-static-v1.2.0';
const DYNAMIC_CACHE = 'StudentsPoint-dynamic-v1.2.0';

// Archivos estáticos para cache
const STATIC_FILES = [
  '/',
  '/index.html',
  '/login.html',
  '/register.html',
  '/account.html',
  '/teachers.html',
  '/campuses.html',
  '/static/css/styles.css',
  '/static/css/students-theme.css',
  '/static/js/main.js',
  '/static/js/pwa.js',
  '/static/js/sounds.js',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://code.jquery.com/jquery-3.7.1.min.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  '/static/images/icons/icon-192x192.png',
  '/static/images/icons/icon-512x512.png',
  '/forum/',
  '/market/',
  '/portfolio/',
  '/streetview/',
  '/bienestar/',
  '/reportes/',
  '/cursos/',
  '/encuestas/',
  '/horarios/'
];

// Archivos de API para cache dinámico
const API_PATTERNS = [
  '/api/auth/',
  '/api/forum/',
  '/api/market/',
  '/api/portfolio/',
  '/api/polls/',
  '/api/campuses/',
  '/api/bienestar/',
  '/api/reports/',
  '/api/otec/',
  '/api/notifications/',
  '/api/schedules/'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('Service Worker: Cacheando archivos estáticos');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Instalación completada');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Service Worker: Error en instalación:', error);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activando...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Service Worker: Eliminando cache antiguo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activación completada');
        return self.clients.claim();
      })
  );
});

// Interceptación de requests
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Estrategia para archivos estáticos
  if (STATIC_FILES.includes(url.pathname)) {
    event.respondWith(
      caches.match(request)
        .then((response) => {
          if (response) {
            return response;
          }
          return fetch(request)
            .then((response) => {
              if (response.status === 200) {
                const responseClone = response.clone();
                caches.open(STATIC_CACHE)
                  .then((cache) => {
                    cache.put(request, responseClone);
                  });
              }
              return response;
            });
        })
    );
  }
  
  // Estrategia para APIs
  else if (API_PATTERNS.some(pattern => url.pathname.startsWith(pattern))) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cachear respuestas exitosas de API
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE)
              .then((cache) => {
                cache.put(request, responseClone);
              });
          }
          return response;
        })
        .catch(() => {
          // Fallback a cache si no hay conexión
          return caches.match(request)
            .then((response) => {
              if (response) {
                return response;
              }
              // Respuesta offline para APIs
              return new Response(
                JSON.stringify({
                  error: 'Sin conexión',
                  message: 'No se pudo conectar al servidor. Verifica tu conexión a internet.'
                }),
                {
                  status: 503,
                  statusText: 'Service Unavailable',
                  headers: {
                    'Content-Type': 'application/json'
                  }
                }
              );
            });
        })
    );
  }
  
  // Estrategia para otros recursos
  else {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cachear recursos exitosos
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE)
              .then((cache) => {
                cache.put(request, responseClone);
              });
          }
          return response;
        })
        .catch(() => {
          // Fallback a cache
          return caches.match(request);
        })
    );
  }
});

// Manejo de notificaciones push
self.addEventListener('push', (event) => {
  console.log('Service Worker: Notificación push recibida');
  
  const options = {
    body: 'Tienes una nueva notificación de StudentsPoint',
    icon: '/static/images/icon-192x192.png',
    badge: '/static/images/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Ver notificación',
        icon: '/static/images/icon-96x96.png'
      },
      {
        action: 'close',
        title: 'Cerrar',
        icon: '/static/images/icon-96x96.png'
      }
    ]
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.data = { ...options.data, ...data };
  }
  
  event.waitUntil(
    self.registration.showNotification('StudentsPoint', options)
  );
});

// Manejo de clics en notificaciones
self.addEventListener('notificationclick', (event) => {
  console.log('Service Worker: Click en notificación');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'close') {
    // Solo cerrar la notificación
    return;
  } else {
    // Click en el cuerpo de la notificación
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Sincronización en segundo plano
self.addEventListener('sync', (event) => {
  console.log('Service Worker: Sincronización en segundo plano');
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Aquí se pueden agregar tareas de sincronización
      Promise.resolve()
    );
  }
});

// Manejo de mensajes del cliente
self.addEventListener('message', (event) => {
  console.log('Service Worker: Mensaje recibido:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({
      version: CACHE_NAME
    });
  }
});

// Limpieza de cache
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'CLEAN_CACHE') {
    event.waitUntil(
      caches.keys()
        .then((cacheNames) => {
          return Promise.all(
            cacheNames.map((cacheName) => {
              return caches.delete(cacheName);
            })
          );
        })
        .then(() => {
          event.ports[0].postMessage({
            success: true,
            message: 'Cache limpiado exitosamente'
          });
        })
    );
  }
});

console.log('Service Worker: Cargado correctamente');
