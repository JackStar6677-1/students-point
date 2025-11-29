/**
 * Servicio API para el módulo de encuestas/polls.
 * Centraliza todas las llamadas HTTP al backend relacionadas con encuestas.
 * Basado en el patrón de MarketAPI
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
        if (window.authAPI && typeof window.authAPI.getAuthToken === 'function') {
            return window.authAPI.getAuthToken();
        }
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
            if (window.authAPI && typeof window.authAPI.logout === 'function') {
                window.authAPI.logout();
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            }
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
     * Lista todas las encuestas según filtros.
     * @param {Object} filters - Filtros opcionales (estado, categoria, search)
     * @returns {Promise<Array>} Lista de encuestas
     */
    async getPolls(filters = {}) {
        try {
            const params = new URLSearchParams();
            Object.keys(filters).forEach(key => {
                if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
                    params.append(key, filters[key]);
                }
            });

            const url = `${this.baseURL}/polls/${params.toString() ? '?' + params : ''}`;
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
            const response = await fetch(`${this.baseURL}/polls/${id}/`, {
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
            const response = await fetch(`${this.baseURL}/polls/`, {
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
            const response = await fetch(`${this.baseURL}/polls/${id}/`, {
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
            const response = await fetch(`${this.baseURL}/polls/${id}/`, {
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
     * @param {Object} payload - Payload con opciones
     * @returns {Promise<Object>} Resultado de la votación
     */
    async votePoll(id, payload) {
        try {
            // El payload puede venir como { opciones: [...] } o { respuestas: [...] }
            // Normalizamos a { opciones: [...] } que es lo que espera el backend
            const body = payload.opciones ? payload : { opciones: payload.respuestas || payload.opciones || [] };
            
            const response = await fetch(`${this.baseURL}/polls/${id}/votar/`, {
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
     * Reporta una encuesta.
     * @param {number} pollId - ID de la encuesta
     * @param {Object} reportData - Datos del reporte (tipo, descripcion)
     * @returns {Promise<Object>} Reporte creado
     */
    async reportarPoll(pollId, reportData) {
        try {
            const response = await fetch(`${this.baseURL}/polls/${pollId}/reportar/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(reportData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error reportando encuesta:', error);
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
            const response = await fetch(`${this.baseURL}/polls/${id}/respuestas/`, {
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
            const response = await fetch(`${this.baseURL}/polls/mis-encuestas/`, {
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
            const response = await fetch(`${this.baseURL}/polls/${id}/cerrar/`, {
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
            const response = await fetch(`${this.baseURL}/polls/${id}/analytics/`, {
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
            const response = await fetch(`${this.baseURL}/polls/${id}/export/?format=${format}`, {
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
            const response = await fetch(`${this.baseURL}/polls/dashboard/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo dashboard:', error);
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
}

// Exportar instancia global del servicio API
window.pollsAPI = new PollsAPI();
