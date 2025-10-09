/**
 * PWA (Progressive Web App) - StudentsPoint
 * Script para registrar Service Worker y manejar instalación
 */

class StudentsPointPWA {
  constructor() {
    this.deferredPrompt = null;
    this.isInstalled = false;
    this.isOnline = navigator.onLine;
    
    this.init();
  }
  
  init() {
    this.registerServiceWorker();
    this.setupInstallPrompt();
    this.setupOnlineOfflineHandlers();
    this.setupUpdateHandlers();
    this.checkInstallationStatus();
  }
  
  /**
   * Registrar Service Worker
   */
  async registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      // Usar configuración PWA
      const pwaInfo = window.PWAConfig ? window.PWAConfig.canPWAWork() : null;
      
      if (pwaInfo && !pwaInfo.canWork) {
        console.warn('PWA: Service Worker no puede funcionar en este entorno');
        console.warn('PWA: Razones:', {
          isSecureContext: pwaInfo.isSecureContext,
          hasServiceWorker: pwaInfo.hasServiceWorker
        });
        return;
      }
      
      console.log('PWA: Contexto seguro:', pwaInfo ? pwaInfo.isSecureContext : 'Verificando...');
      console.log('PWA: Hostname:', window.location.hostname);
      console.log('PWA: Protocol:', window.location.protocol);
      
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/'
        });
        console.log('PWA: Service Worker registrado exitosamente:', registration);
        
        // Verificar actualizaciones
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.showUpdateNotification();
            }
          });
        });
        
      } catch (error) {
        console.error('PWA: Error registrando Service Worker:', error);
        console.log('PWA: Continuando sin Service Worker');
      }
    } else {
      console.warn('PWA: Service Worker no soportado en este navegador');
    }
  }
  
  /**
   * Configurar prompt de instalación
   */
  setupInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e) => {
      console.log('PWA: Prompt de instalación disponible');
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton();
    });
    
    window.addEventListener('appinstalled', () => {
      console.log('PWA: App instalada exitosamente');
      this.isInstalled = true;
      this.hideInstallButton();
      this.deferredPrompt = null;
      this.showInstallationSuccess();
    });
  }
  
  /**
   * Mostrar botón de instalación
   */
  showInstallButton() {
    const installButton = document.getElementById('install-button');
    if (installButton) {
      installButton.style.display = 'block';
      installButton.addEventListener('click', () => {
        this.installApp();
      });
    }
  }
  
  /**
   * Ocultar botón de instalación
   */
  hideInstallButton() {
    const installButton = document.getElementById('install-button');
    if (installButton) {
      installButton.style.display = 'none';
    }
  }
  
  /**
   * Instalar app
   */
  async installApp() {
    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      console.log('PWA: Resultado de instalación:', outcome);
      this.deferredPrompt = null;
    }
  }
  
  /**
   * Verificar estado de instalación
   */
  checkInstallationStatus() {
    if (window.matchMedia('(display-mode: standalone)').matches) {
      this.isInstalled = true;
      console.log('PWA: App ejecutándose en modo standalone');
    }
  }
  
  /**
   * Configurar handlers de conexión
   */
  setupOnlineOfflineHandlers() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.showOnlineStatus();
      this.syncOfflineData();
    });
    
    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.showOfflineStatus();
    });
  }
  
  /**
   * Mostrar estado online
   */
  showOnlineStatus() {
    this.showNotification('Conexión restaurada', 'success');
  }
  
  /**
   * Mostrar estado offline
   */
  showOfflineStatus() {
    this.showNotification('Sin conexión - Modo offline', 'warning');
  }
  
  /**
   * Sincronizar datos offline
   */
  async syncOfflineData() {
    if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
      try {
        const registration = await navigator.serviceWorker.ready;
        await registration.sync.register('background-sync');
        console.log('PWA: Sincronización en segundo plano registrada');
      } catch (error) {
        console.error('PWA: Error en sincronización:', error);
      }
    }
  }
  
  /**
   * Configurar handlers de actualización
   */
  setupUpdateHandlers() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
      });
    }
  }
  
  /**
   * Mostrar notificación de actualización
   */
  showUpdateNotification() {
    const updateNotification = document.createElement('div');
    updateNotification.className = 'update-notification';
    updateNotification.innerHTML = `
      <div class="alert alert-info alert-dismissible fade show" role="alert">
        <i class="fas fa-sync-alt"></i>
        Nueva versión disponible. 
        <button type="button" class="btn btn-sm btn-primary ms-2" onclick="window.location.reload()">
          Actualizar
        </button>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;
    
    document.body.insertBefore(updateNotification, document.body.firstChild);
  }
  
  /**
   * Mostrar notificación de instalación exitosa
   */
  showInstallationSuccess() {
    this.showNotification('¡StudentsPoint instalado exitosamente!', 'success');
  }
  
  /**
   * Mostrar notificación
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }
  
  /**
   * Limpiar cache
   */
  async clearCache() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.ready;
        const messageChannel = new MessageChannel();
        
        messageChannel.port1.onmessage = (event) => {
          if (event.data.success) {
            this.showNotification('Cache limpiado exitosamente', 'success');
          }
        };
        
        navigator.serviceWorker.controller.postMessage(
          { type: 'CLEAN_CACHE' },
          [messageChannel.port2]
        );
      } catch (error) {
        console.error('PWA: Error limpiando cache:', error);
      }
    }
  }
  
  /**
   * Obtener versión del Service Worker
   */
  async getVersion() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.ready;
        const messageChannel = new MessageChannel();
        
        messageChannel.port1.onmessage = (event) => {
          console.log('PWA: Versión actual:', event.data.version);
        };
        
        navigator.serviceWorker.controller.postMessage(
          { type: 'GET_VERSION' },
          [messageChannel.port2]
        );
      } catch (error) {
        console.error('PWA: Error obteniendo versión:', error);
      }
    }
  }
}

// Inicializar PWA cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  window.StudentsPointPWA = new StudentsPointPWA();
});

// Exportar para uso global
window.StudentsPointPWA = StudentsPointPWA;
