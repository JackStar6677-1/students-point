/**
 * Configuración PWA para desarrollo local y Tailscale
 * StudentsPoint - Versión 1.2.3
 */

// Configuración para desarrollo local
const PWA_CONFIG = {
    // URLs base para diferentes entornos
    baseUrls: {
        development: 'http://localhost:8000',
        tailscaleLaptop: 'http://100.75.238.19:8000',  // Tailscale IP - jackstar6677-laptop
        tailscaleDesktop: 'http://100.113.204.115:8000', // Tailscale IP - desktop
        production: 'https://studentspoint.app'
    },
    
    // Configuración de cache
    cacheConfig: {
        version: '1.2.3',
        staticCache: 'StudentsPoint-static-v1.2.3',
        dynamicCache: 'StudentsPoint-dynamic-v1.2.3',
        maxAge: 86400000, // 24 horas
        maxEntries: 50
    },
    
    // Configuración de notificaciones
    notifications: {
        enabled: true,
        vapidPublicKey: 'BEl62iUYgUivxIkv69yViEuiBIa40HI8l8V6V1V8H3BZ7pRJvnSW4UPHW3v3T1td1K3_fSqiNI2j_lLQ6Ypy1XM',
        vapidPrivateKey: '3K1XdXz0L8Fz0aJSOdwuSeiJfZ5JWY7BdI3R2kS2aJ8',
        subject: 'mailto:admin@studentspoint.app'
    },
    
    // Configuración de sincronización
    sync: {
        enabled: true,
        backgroundSync: true,
        offlineSupport: true
    },
    
    // Configuración de instalación
    installation: {
        promptAfterInstall: false,
        showInstallButton: true,
        installButtonText: 'Instalar StudentsPoint'
    }
};

// Detectar entorno
function getEnvironment() {
    const hostname = window.location.hostname;
    
    // Detectar Tailscale específico (laptop)
    if (hostname === '100.75.238.19') {
        return 'tailscaleLaptop';
    }
    
    // Detectar Tailscale específico (desktop)
    if (hostname === '100.113.204.115') {
        return 'tailscaleDesktop';
    }
    
    // Detectar cualquier otra IP de Tailscale
    if (hostname.startsWith('100.')) {
        return 'tailscaleLaptop'; // Usar laptop como default
    }
    
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.includes('192.168.')) {
        return 'development';
    }
    
    return 'production';
}

// Obtener URL base según el entorno
function getBaseUrl() {
    const env = getEnvironment();
    const baseUrl = PWA_CONFIG.baseUrls[env];
    
    // Si no se encuentra, construir dinámicamente
    if (!baseUrl) {
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;
        const port = window.location.port || '8000';
        return `${protocol}//${hostname}:${port}`;
    }
    
    return baseUrl;
}

// Configuración de desarrollo local
const DEV_CONFIG = {
    // Permitir PWA en localhost
    allowLocalhost: true,
    
    // Configuración de desarrollo
    debug: true,
    logLevel: 'debug',
    
    // URLs de desarrollo
    apiUrl: 'http://localhost:8000/api',
    staticUrl: 'http://localhost:8000/static',
    
    // URLs de Tailscale (si está disponible)
    tailscaleApiUrl: 'http://100.75.238.19:8000/api',
    tailscaleStaticUrl: 'http://100.75.238.19:8000/static',
    
    // Configuración de cache para desarrollo
    cacheStrategy: 'networkFirst',
    cacheTimeout: 5000, // 5 segundos
    
    // Configuración de notificaciones para desarrollo
    notifications: {
        enabled: true,
        testMode: true,
        showTestNotifications: true
    }
};

// Configuración de producción
const PROD_CONFIG = {
    // Configuración de producción
    debug: false,
    logLevel: 'error',
    
    // URLs de producción
    apiUrl: 'https://StudentsPoint.duocuc.cl/api',
    staticUrl: 'https://StudentsPoint.duocuc.cl/static',
    
    // Configuración de cache para producción
    cacheStrategy: 'cacheFirst',
    cacheTimeout: 30000, // 30 segundos
    
    // Configuración de notificaciones para producción
    notifications: {
        enabled: true,
        testMode: false,
        showTestNotifications: false
    }
};

// Obtener configuración según el entorno
function getConfig() {
    const env = getEnvironment();
    return env === 'development' ? DEV_CONFIG : PROD_CONFIG;
}

// Función para verificar si el PWA puede funcionar
function canPWAWork() {
    const config = getConfig();
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    // Detectar contexto seguro
    const isLocalhost = hostname === 'localhost' || 
                       hostname === '127.0.0.1' ||
                       hostname === '0.0.0.0';
    
    const isPrivateNetwork = hostname.startsWith('192.168.') ||
                            hostname.startsWith('10.') ||
                            hostname.startsWith('172.16.') ||
                            hostname.startsWith('172.17.') ||
                            hostname.startsWith('172.18.') ||
                            hostname.startsWith('172.19.') ||
                            hostname.startsWith('172.20.') ||
                            hostname.startsWith('172.21.') ||
                            hostname.startsWith('172.22.') ||
                            hostname.startsWith('172.23.') ||
                            hostname.startsWith('172.24.') ||
                            hostname.startsWith('172.25.') ||
                            hostname.startsWith('172.26.') ||
                            hostname.startsWith('172.27.') ||
                            hostname.startsWith('172.28.') ||
                            hostname.startsWith('172.29.') ||
                            hostname.startsWith('172.30.') ||
                            hostname.startsWith('172.31.');
    
    const isTailscale = hostname.startsWith('100.');
    
    const isHttps = protocol === 'https:';
    
    // Chrome considera contextos seguros: localhost, 127.0.0.1, HTTPS
    // Para PWA en Tailscale/redes privadas, necesitamos forzar el contexto como seguro
    const isSecureContext = window.isSecureContext || 
                           isLocalhost || 
                           isPrivateNetwork ||
                           isTailscale ||
                           isHttps;
    
    // Verificar soporte de Service Worker
    const hasServiceWorker = 'serviceWorker' in navigator;
    
    // Verificar soporte de notificaciones
    const hasNotifications = 'Notification' in window;
    
    // Verificar soporte de instalación
    const hasInstallPrompt = 'onbeforeinstallprompt' in window;
    
    return {
        canWork: isSecureContext && hasServiceWorker,
        isSecureContext,
        hasServiceWorker,
        hasNotifications,
        hasInstallPrompt,
        isLocalhost,
        isPrivateNetwork,
        isTailscale,
        isHttps,
        hostname,
        protocol,
        config
    };
}

// Función para mostrar información de PWA
function showPWAInfo() {
    const pwaInfo = canPWAWork();
    const config = getConfig();
    
    console.log('=== PWA Configuration ===');
    console.log('Environment:', getEnvironment());
    console.log('Base URL:', getBaseUrl());
    console.log('Can PWA work:', pwaInfo.canWork);
    console.log('Is secure context:', pwaInfo.isSecureContext);
    console.log('Has Service Worker:', pwaInfo.hasServiceWorker);
    console.log('Has Notifications:', pwaInfo.hasNotifications);
    console.log('Has Install Prompt:', pwaInfo.hasInstallPrompt);
    console.log('Debug mode:', config.debug);
    console.log('Cache strategy:', config.cacheStrategy);
    console.log('========================');
    
    return pwaInfo;
}

// Función para configurar PWA según el entorno
function configurePWA() {
    const pwaInfo = canPWAWork();
    const config = getConfig();
    
    if (!pwaInfo.canWork) {
        console.warn('PWA no puede funcionar en este entorno');
        console.warn('Razones:', {
            isSecureContext: pwaInfo.isSecureContext,
            hasServiceWorker: pwaInfo.hasServiceWorker
        });
        return false;
    }
    
    // Configurar variables globales
    window.PWA_CONFIG = PWA_CONFIG;
    window.PWA_ENV = getEnvironment();
    window.PWA_BASE_URL = getBaseUrl();
    window.PWA_DEBUG = config.debug;
    
    console.log('PWA configurado correctamente para:', getEnvironment());
    return true;
}

// Exportar funciones
window.PWAConfig = {
    getEnvironment,
    getBaseUrl,
    getConfig,
    canPWAWork,
    showPWAInfo,
    configurePWA,
    PWA_CONFIG,
    DEV_CONFIG,
    PROD_CONFIG
};

// Auto-configurar al cargar
document.addEventListener('DOMContentLoaded', () => {
    configurePWA();
    
    if (window.PWA_DEBUG) {
        showPWAInfo();
    }
});
