/**
 * Servicio API para el módulo de encuestas/polls.
 * Centraliza todas las llamadas HTTP al backend relacionadas con encuestas.
 */

class PollsAPI {
    constructor() {
        this.baseURL = '/api/polls';
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
            if (window.authAPI) {
                window.authAPI.logout();
            }
            window.location.href = '/login.html';
            return null;
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                const errorMsg = data.detail || data.error || data.message || 'Error en la petición';
                throw new Error(errorMsg);
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
     * Lista todas las encuestas según filtros.
     * @param {Object} filters - Filtros opcionales (estado, categoria, search)
     * @returns {Promise<Array>} Lista de encuestas
     */
    async getPolls(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.estado) params.append('estado', filters.estado);
            if (filters.categoria) params.append('categoria', filters.categoria);
            if (filters.search) params.append('search', filters.search);

            const url = `${this.baseURL}/${params.toString() ? '?' + params.toString() : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo encuestas:', error);
            throw error;
        }
    }

    /**
     * Obtiene los detalles de una encuesta específica.
     * @param {number} id - ID de la encuesta
     * @returns {Promise<Object>} Datos de la encuesta
     */
    async getPoll(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo encuesta:', error);
            throw error;
        }
    }

    /**
     * Crea una nueva encuesta.
     * @param {Object} pollData - Datos de la encuesta
     * @returns {Promise<Object>} Encuesta creada
     */
    async createPoll(pollData) {
        try {
            const response = await fetch(`${this.baseURL}/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(pollData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando encuesta:', error);
            throw error;
        }
    }

    /**
     * Actualiza una encuesta existente.
     * @param {number} id - ID de la encuesta
     * @param {Object} pollData - Datos actualizados
     * @returns {Promise<Object>} Encuesta actualizada
     */
    async updatePoll(id, pollData) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(pollData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando encuesta:', error);
            throw error;
        }
    }

    /**
     * Elimina una encuesta.
     * @param {number} id - ID de la encuesta
     * @returns {Promise<void>}
     */
    async deletePoll(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando encuesta:', error);
            throw error;
        }
    }

    /**
     * Vota en una encuesta.
     * @param {number} id - ID de la encuesta
     * @param {Array} respuestas - Array de respuestas
     * @returns {Promise<Object>} Resultado de la votación
     */
    async votePoll(id, payload) {
        try {
            // El payload puede venir como { opciones: [...] } o { respuestas: [...] }
            // Normalizamos a { opciones: [...] } que es lo que espera el backend
            const body = payload.opciones ? payload : { opciones: payload.respuestas || payload.opciones || [] };
            
            const response = await fetch(`${this.baseURL}/${id}/votar/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(body)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error votando en encuesta:', error);
            throw error;
        }
    }

    /**
     * Obtiene las respuestas de una encuesta.
     * @param {number} id - ID de la encuesta
     * @returns {Promise<Array>} Lista de respuestas
     */
    async getPollResponses(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/respuestas/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo respuestas:', error);
            throw error;
        }
    }

    /**
     * Obtiene las encuestas del usuario actual.
     * @returns {Promise<Array>} Lista de encuestas del usuario
     */
    async getMyPolls() {
        try {
            const response = await fetch(`${this.baseURL}/mis-encuestas/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo mis encuestas:', error);
            throw error;
        }
    }

    /**
     * Cierra una encuesta.
     * @param {number} id - ID de la encuesta
     * @returns {Promise<Object>} Encuesta cerrada
     */
    async closePoll(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/cerrar/`, {
                method: 'POST',
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error cerrando encuesta:', error);
            throw error;
        }
    }

    /**
     * Obtiene analytics de una encuesta.
     * @param {number} id - ID de la encuesta
     * @returns {Promise<Object>} Datos de analytics
     */
    async getPollAnalytics(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/analytics/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo analytics:', error);
            throw error;
        }
    }

    /**
     * Exporta los resultados de una encuesta.
     * @param {number} id - ID de la encuesta
     * @param {string} format - Formato de exportación (csv, json, xlsx)
     * @returns {Promise<Blob>} Archivo exportado
     */
    async exportPoll(id, format = 'csv') {
        try {
            const response = await fetch(`${this.baseURL}/${id}/export/?format=${format}`, {
                headers: this.getHeaders(true)
            });

            if (!response.ok) {
                await this.handleResponse(response);
            }

            return await response.blob();
        } catch (error) {
            console.error('Error exportando encuesta:', error);
            throw error;
        }
    }

    /**
     * Obtiene el dashboard de encuestas.
     * @returns {Promise<Object>} Datos del dashboard
     */
    async getDashboard() {
        try {
            const response = await fetch(`${this.baseURL}/dashboard/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo dashboard:', error);
            throw error;
        }
    }

    /**
     * Obtiene el usuario actual usando el servicio de autenticación.
     * @returns {Promise<Object>} Datos del usuario
     */
    async getCurrentUser() {
        if (window.authAPI) {
            return await window.authAPI.getCurrentUser();
        }
        throw new Error('Servicio de autenticación no disponible');
    }
}

// Exportar instancia global del servicio API
window.pollsAPI = new PollsAPI();

