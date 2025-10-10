/**
 * Cache Manager para StudentsPoint
 * Maneja el almacenamiento en caché de datos de API
 */

class CacheManager {
    constructor() {
        this.cachePrefix = 'sp_cache_';
        this.cacheExpiry = 5 * 60 * 1000; // 5 minutos por defecto
    }

    /**
     * Guarda datos en el caché con expiración
     */
    set(key, data, expiry = this.cacheExpiry) {
        const item = {
            data: data,
            timestamp: Date.now(),
            expiry: expiry
        };
        
        try {
            localStorage.setItem(
                this.cachePrefix + key,
                JSON.stringify(item)
            );
        } catch (e) {
            console.warn('Error guardando en caché:', e);
            // Limpiar caché si está lleno
            this.clearExpired();
        }
    }

    /**
     * Obtiene datos del caché si no han expirado
     */
    get(key) {
        try {
            const item = localStorage.getItem(this.cachePrefix + key);
            if (!item) return null;

            const parsed = JSON.parse(item);
            const now = Date.now();

            // Verificar si expiró
            if (now - parsed.timestamp > parsed.expiry) {
                this.delete(key);
                return null;
            }

            return parsed.data;
        } catch (e) {
            console.warn('Error leyendo caché:', e);
            return null;
        }
    }

    /**
     * Elimina un item del caché
     */
    delete(key) {
        localStorage.removeItem(this.cachePrefix + key);
    }

    /**
     * Limpia items expirados del caché
     */
    clearExpired() {
        const now = Date.now();
        const keysToDelete = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                try {
                    const item = JSON.parse(localStorage.getItem(key));
                    if (now - item.timestamp > item.expiry) {
                        keysToDelete.push(key);
                    }
                } catch (e) {
                    keysToDelete.push(key);
                }
            }
        }

        keysToDelete.forEach(key => localStorage.removeItem(key));
        console.log(`Limpiados ${keysToDelete.length} items expirados del caché`);
    }

    /**
     * Limpia todo el caché de la aplicación
     */
    clearAll() {
        const keysToDelete = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.cachePrefix)) {
                keysToDelete.push(key);
            }
        }
        keysToDelete.forEach(key => localStorage.removeItem(key));
        console.log('Caché limpiado completamente');
    }

    /**
     * Fetch con caché automático
     */
    async cachedFetch(url, options = {}, cacheExpiry = this.cacheExpiry) {
        const cacheKey = `fetch_${url}_${JSON.stringify(options)}`;

        // Intentar obtener del caché
        const cached = this.get(cacheKey);
        if (cached) {
            console.log(` Datos servidos desde caché: ${url}`);
            return cached;
        }

        // Si no está en caché, hacer fetch
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            
            // Guardar en caché
            this.set(cacheKey, data, cacheExpiry);
            console.log(` Datos guardados en caché: ${url}`);
            
            return data;
        } catch (error) {
            console.error('Error en fetch:', error);
            throw error;
        }
    }
}

// Instancia global
const cacheManager = new CacheManager();

// Limpiar caché expirado al cargar
document.addEventListener('DOMContentLoaded', () => {
    cacheManager.clearExpired();
});

