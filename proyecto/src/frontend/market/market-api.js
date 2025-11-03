/**
 * Servicio API para el módulo de marketplace.
 * Centraliza todas las llamadas HTTP al backend relacionadas con productos.
 */

class MarketAPI {
    constructor() {
        this.baseURL = '/api/marketplace';
    }

    /**
     * Obtiene el token de autenticación del localStorage.
     * @returns {string|null} Token de acceso o null si no existe
     */
    getAuthToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Construye los headers para una petición HTTP.
     * @param {boolean} includeAuth - Si incluir el token de autenticación
     * @param {boolean} isFormData - Si es FormData, no incluir Content-Type
     * @returns {Object} Objeto con los headers
     */
    getHeaders(includeAuth = true, isFormData = false) {
        const headers = {};
        
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }
        
        if (includeAuth) {
            const token = this.getAuthToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }
        
        return headers;
    }

    /**
     * Maneja errores de respuesta HTTP.
     * @param {Response} response - Respuesta de fetch
     * @returns {Promise} Promise que resuelve con los datos o lanza error
     */
    async handleResponse(response) {
        if (response.status === 401) {
            // Token expirado, redirigir al login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login.html';
            return null;
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || data.message || data.error || 'Error en la petición');
            }
            return data;
        }

        const text = await response.text();
        if (!response.ok) {
            throw new Error(text || 'Error en la petición');
        }
        return text;
    }

    /**
     * Lista todas las categorías de productos.
     * @returns {Promise<Array>} Lista de categorías
     */
    async getCategorias() {
        try {
            const response = await fetch(`${this.baseURL}/categories/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo categorías:', error);
            throw error;
        }
    }

    /**
     * Lista productos según filtros.
     * @param {Object} filters - Filtros (estado, categoria, campus, carrera, search)
     * @returns {Promise<Array>} Lista de productos
     */
    async getProductos(filters = {}) {
        try {
            const params = new URLSearchParams();
            Object.keys(filters).forEach(key => {
                if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
                    params.append(key, filters[key]);
                }
            });

            const url = `${this.baseURL}/products/${params.toString() ? '?' + params : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo productos:', error);
            throw error;
        }
    }

    /**
     * Obtiene un producto por ID.
     * @param {number} productoId - ID del producto
     * @returns {Promise<Object>} Producto
     */
    async getProducto(productoId) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo producto:', error);
            throw error;
        }
    }

    /**
     * Crea un nuevo producto (con extracción automática de OpenGraph).
     * @param {Object} productoData - Datos del producto
     * @returns {Promise<Object>} Producto creado
     */
    async createProducto(productoData) {
        try {
            const response = await fetch(`${this.baseURL}/products/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(productoData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando producto:', error);
            throw error;
        }
    }

    /**
     * Actualiza un producto existente.
     * @param {number} productoId - ID del producto
     * @param {Object} productoData - Datos actualizados
     * @returns {Promise<Object>} Producto actualizado
     */
    async updateProducto(productoId, productoData) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(productoData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando producto:', error);
            throw error;
        }
    }

    /**
     * Elimina un producto.
     * @param {number} productoId - ID del producto
     * @returns {Promise<void>}
     */
    async deleteProducto(productoId) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando producto:', error);
            throw error;
        }
    }

    /**
     * Marca o desmarca un producto como favorito.
     * @param {number} productoId - ID del producto
     * @returns {Promise<Object>} Estado del favorito
     */
    async toggleFavorito(productoId) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/toggle_favorito/`, {
                method: 'POST',
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error toggle favorito:', error);
            throw error;
        }
    }

    /**
     * Registra un click en el enlace de un producto.
     * @param {number} productoId - ID del producto
     * @returns {Promise<Object>} Clicks totales
     */
    async registrarClick(productoId) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/registrar_click/`, {
                method: 'POST',
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error registrando click:', error);
            throw error;
        }
    }

    /**
     * Obtiene los productos favoritos del usuario actual.
     * @returns {Promise<Array>} Lista de productos favoritos
     */
    async getMisFavoritos() {
        try {
            const response = await fetch(`${this.baseURL}/products/mis_favoritos/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo favoritos:', error);
            throw error;
        }
    }

    /**
     * Obtiene los productos del usuario actual.
     * @returns {Promise<Array>} Lista de productos del usuario
     */
    async getMisProductos() {
        try {
            const response = await fetch(`${this.baseURL}/products/mis_productos/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo mis productos:', error);
            throw error;
        }
    }

    /**
     * Obtiene analytics de un producto.
     * @param {number} productoId - ID del producto
     * @returns {Promise<Object>} Analytics del producto
     */
    async getAnalytics(productoId) {
        try {
            const response = await fetch(`${this.baseURL}/products/${productoId}/analytics/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo analytics:', error);
            throw error;
        }
    }

    /**
     * Reporta un producto.
     * @param {Object} reportData - Datos del reporte (producto, tipo, descripcion)
     * @returns {Promise<Object>} Reporte creado
     */
    async reportarProducto(reportData) {
        try {
            const response = await fetch(`${this.baseURL}/reports/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(reportData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error reportando producto:', error);
            throw error;
        }
    }

    /**
     * Obtiene información del usuario actual.
     * @returns {Promise<Object>} Datos del usuario
     */
    async getCurrentUser() {
        try {
            const response = await fetch('/api/auth/me/', {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo usuario:', error);
            throw error;
        }
    }

    /**
     * Previsualiza metadatos OpenGraph de una URL (para mostrar preview antes de crear producto).
     * @param {string} url - URL a previsualizar
     * @returns {Promise<Object>} Metadatos OpenGraph
     */
    async previewURL(url) {
        try {
            // Nota: Esto podría requerir un endpoint específico en el backend
            // Por ahora, devolvemos null y se obtendrá automáticamente al crear
            return null;
        } catch (error) {
            console.error('Error previsualizando URL:', error);
            return null;
        }
    }
}

// Exportar instancia global del servicio API
window.marketAPI = new MarketAPI();

