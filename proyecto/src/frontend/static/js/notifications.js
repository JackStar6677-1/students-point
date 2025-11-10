/**
 * Sistema de Notificaciones del Navegador - StudentsPoint
 * Gestiona permisos y envío de notificaciones push
 */

class NotificationsManager {
  constructor() {
    this.permission = Notification.permission || 'default';
    this.isSupported = 'Notification' in window;
    this.subscription = null;
    this.askOnLoad = true;
    this.askDelay = 3000; // Esperar 3 segundos antes de preguntar
    
    this.init();
  }
  
  /**
   * Inicializar sistema de notificaciones
   */
  init() {
    if (!this.isSupported) {
      console.warn('Notificaciones: No soportadas en este navegador');
      return;
    }
    
    console.log('Notificaciones: Sistema inicializado');
    console.log('Notificaciones: Permiso actual:', this.permission);
    
    // Si el permiso ya fue denegado, no preguntar
    if (this.permission === 'denied') {
      console.warn('Notificaciones: Permiso denegado previamente');
      return;
    }
    
    // Si el permiso ya fue concedido, registrar subscription
    if (this.permission === 'granted') {
      this.subscribeToPush();
      return;
    }
    
    // Si no se ha preguntado aún, esperar un momento y preguntar
    if (this.permission === 'default' && this.askOnLoad) {
      setTimeout(() => {
        this.showPermissionPrompt();
      }, this.askDelay);
    }
  }
  
  /**
   * Mostrar prompt de permisos con UI amigable
   */
  showPermissionPrompt() {
    // Verificar si ya existe el prompt
    if (document.getElementById('notification-permission-prompt')) {
      return;
    }
    
    // Crear el prompt visual
    const prompt = document.createElement('div');
    prompt.id = 'notification-permission-prompt';
    prompt.className = 'notification-prompt animate-slide-in-bottom';
    prompt.innerHTML = `
      <div class="notification-prompt-content">
        <div class="notification-prompt-icon">
          <i class="fas fa-bell"></i>
        </div>
        <div class="notification-prompt-text">
          <h5 class="mb-1">Mantente actualizado</h5>
          <p class="mb-0 small">¿Deseas recibir notificaciones sobre nuevas publicaciones y actividades?</p>
        </div>
        <div class="notification-prompt-actions">
          <button class="btn btn-sm btn-primary" id="notification-allow">
            <i class="fas fa-check me-1"></i>Permitir
          </button>
          <button class="btn btn-sm btn-outline-secondary" id="notification-deny">
            <i class="fas fa-times me-1"></i>Ahora no
          </button>
        </div>
        <button class="notification-prompt-close" id="notification-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    `;
    
    // Agregar estilos
    this.injectStyles();
    
    // Agregar al DOM
    document.body.appendChild(prompt);
    
    // Event listeners
    document.getElementById('notification-allow').addEventListener('click', () => {
      this.requestPermission();
      prompt.remove();
    });
    
    document.getElementById('notification-deny').addEventListener('click', () => {
      console.log('Notificaciones: Usuario rechazó el prompt');
      prompt.remove();
      // Recordar que el usuario rechazó (no preguntar nuevamente en esta sesión)
      sessionStorage.setItem('notification_prompt_declined', 'true');
    });
    
    document.getElementById('notification-close').addEventListener('click', () => {
      prompt.remove();
      sessionStorage.setItem('notification_prompt_closed', 'true');
    });
    
    // Auto-cerrar después de 15 segundos si no hay interacción
    setTimeout(() => {
      if (document.getElementById('notification-permission-prompt')) {
        prompt.remove();
      }
    }, 15000);
  }
  
  /**
   * Inyectar estilos CSS
   */
  injectStyles() {
    if (document.getElementById('notification-styles')) {
      return; // Ya están inyectados
    }
    
    const styles = document.createElement('style');
    styles.id = 'notification-styles';
    styles.textContent = `
      .notification-prompt {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        color: white;
        animation: slideInBottom 0.5s ease-out;
      }
      
      .notification-prompt-content {
        padding: 20px;
        position: relative;
      }
      
      .notification-prompt-icon {
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 24px;
        color: #fbbf24;
      }
      
      .notification-prompt-text {
        margin-left: 50px;
        margin-bottom: 15px;
      }
      
      .notification-prompt-text h5 {
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
      }
      
      .notification-prompt-text p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 13px;
        line-height: 1.4;
      }
      
      .notification-prompt-actions {
        display: flex;
        gap: 10px;
        margin-left: 50px;
      }
      
      .notification-prompt-actions .btn {
        flex: 1;
        font-size: 13px;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 500;
      }
      
      .notification-prompt-actions .btn-primary {
        background: #fbbf24;
        border: none;
        color: #1a1a1a;
      }
      
      .notification-prompt-actions .btn-primary:hover {
        background: #f59e0b;
      }
      
      .notification-prompt-actions .btn-outline-secondary {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
      }
      
      .notification-prompt-actions .btn-outline-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
      }
      
      .notification-prompt-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.7);
        font-size: 14px;
        cursor: pointer;
        padding: 5px;
        border-radius: 4px;
        transition: all 0.2s;
      }
      
      .notification-prompt-close:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
      }
      
      @keyframes slideInBottom {
        from {
          transform: translateY(100%);
          opacity: 0;
        }
        to {
          transform: translateY(0);
          opacity: 1;
        }
      }
      
      .animate-slide-in-bottom {
        animation: slideInBottom 0.5s ease-out;
      }
      
      @media (max-width: 480px) {
        .notification-prompt {
          bottom: 10px;
          right: 10px;
          left: 10px;
          max-width: none;
        }
        
        .notification-prompt-actions {
          flex-direction: column;
        }
      }
    `;
    
    document.head.appendChild(styles);
  }
  
  /**
   * Solicitar permiso de notificaciones
   */
  async requestPermission() {
    if (!this.isSupported) {
      console.warn('Notificaciones: No soportadas');
      return false;
    }
    
    try {
      const permission = await Notification.requestPermission();
      this.permission = permission;
      
      console.log('Notificaciones: Permiso obtenido:', permission);
      
      if (permission === 'granted') {
        this.showSuccessMessage();
        this.subscribeToPush();
        
        // Enviar notificación de prueba
        setTimeout(() => {
          this.sendTestNotification();
        }, 1000);
        
        return true;
      } else {
        this.showDeniedMessage();
        return false;
      }
    } catch (error) {
      console.error('Notificaciones: Error solicitando permiso:', error);
      return false;
    }
  }
  
  /**
   * Suscribirse a notificaciones push
   */
  async subscribeToPush() {
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
      console.warn('Notificaciones push: No soportadas');
      return;
    }
    
    try {
      const registration = await navigator.serviceWorker.ready;
      
      // Verificar si ya está suscrito
      let subscription = await registration.pushManager.getSubscription();
      
      if (subscription) {
        console.log('Notificaciones push: Ya está suscrito');
        this.subscription = subscription;
        return subscription;
      }
      
      // Obtener clave pública VAPID desde configuración
      const vapidPublicKey = window.PWA_CONFIG?.notifications?.vapidPublicKey || 
                            'BEl62iUYgUivxIkv69yViEuiBIa40HI8l8V6V1V8H3BZ7pRJvnSW4UPHW3v3T1td1K3_fSqiNI2j_lLQ6Ypy1XM';
      
      // Convertir clave VAPID a Uint8Array
      const convertedKey = this.urlBase64ToUint8Array(vapidPublicKey);
      
      // Crear nueva suscripción
      subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedKey
      });
      
      console.log('Notificaciones push: Suscripción creada');
      this.subscription = subscription;
      
      // Enviar suscripción al servidor
      await this.sendSubscriptionToServer(subscription);
      
      return subscription;
    } catch (error) {
      console.error('Notificaciones push: Error en suscripción:', error);
      return null;
    }
  }
  
  /**
   * Convertir clave VAPID de base64 a Uint8Array
   */
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');
    
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    
    return outputArray;
  }
  
  /**
   * Enviar suscripción al servidor
   */
  async sendSubscriptionToServer(subscription) {
    try {
      // Obtener token de autenticación si existe
      const token = window.authAPI?.getAuthToken() || localStorage.getItem('access_token');
      
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch('/api/notifications/subscribe/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          subscription: subscription.toJSON(),
          user_agent: navigator.userAgent,
          device_type: this.getDeviceType()
        })
      });
      
      if (response.ok) {
        console.log('Notificaciones: Suscripción enviada al servidor');
      } else {
        console.warn('Notificaciones: Error enviando suscripción al servidor');
      }
    } catch (error) {
      console.error('Notificaciones: Error enviando suscripción:', error);
    }
  }
  
  /**
   * Obtener tipo de dispositivo
   */
  getDeviceType() {
    const ua = navigator.userAgent;
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
      return 'tablet';
    }
    if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
      return 'mobile';
    }
    return 'desktop';
  }
  
  /**
   * Enviar notificación de prueba
   */
  sendTestNotification() {
    if (this.permission !== 'granted') {
      return;
    }
    
    const notification = new Notification('¡Notificaciones activadas!', {
      body: 'Ya puedes recibir actualizaciones de StudentsPoint',
      icon: '/static/images/icons/icon-192x192.png',
      badge: '/static/images/icons/icon-72x72.png',
      tag: 'welcome-notification',
      requireInteraction: false,
      silent: false,
      vibrate: [200, 100, 200]
    });
    
    notification.onclick = () => {
      window.focus();
      notification.close();
    };
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
      notification.close();
    }, 5000);
  }
  
  /**
   * Mostrar mensaje de éxito
   */
  showSuccessMessage() {
    this.showToast('Notificaciones activadas correctamente', 'success');
  }
  
  /**
   * Mostrar mensaje de denegación
   */
  showDeniedMessage() {
    this.showToast('No se activaron las notificaciones. Puedes habilitarlas desde la configuración del navegador.', 'info');
  }
  
  /**
   * Mostrar toast notification
   */
  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `notification-toast notification-toast-${type}`;
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10001;
      max-width: 350px;
      background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
      color: white;
      padding: 16px 20px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      animation: slideInRight 0.3s ease-out;
      font-size: 14px;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOutRight 0.3s ease-in';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
  
  /**
   * Desuscribirse de notificaciones
   */
  async unsubscribe() {
    try {
      if (this.subscription) {
        await this.subscription.unsubscribe();
        console.log('Notificaciones: Desuscripción exitosa');
        this.subscription = null;
        return true;
      }
    } catch (error) {
      console.error('Notificaciones: Error al desuscribirse:', error);
      return false;
    }
  }
  
  /**
   * Verificar estado de permisos
   */
  checkPermissionStatus() {
    return {
      isSupported: this.isSupported,
      permission: this.permission,
      isGranted: this.permission === 'granted',
      isDenied: this.permission === 'denied',
      isDefault: this.permission === 'default',
      subscription: this.subscription !== null
    };
  }
}

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  // Solo inicializar si no se ha rechazado en esta sesión
  const declined = sessionStorage.getItem('notification_prompt_declined');
  const closed = sessionStorage.getItem('notification_prompt_closed');
  
  if (!declined && !closed) {
    window.NotificationsManager = new NotificationsManager();
  } else {
    console.log('Notificaciones: No se preguntará en esta sesión (usuario ya respondió)');
  }
});

// Exportar para uso global
window.NotificationsManager = NotificationsManager;

