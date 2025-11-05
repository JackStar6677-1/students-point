/**
 * Servicio API para el módulo de cursos.
 * Centraliza todas las llamadas HTTP al backend relacionadas con cursos.
 */

class CoursesAPI {
    constructor() {
        this.baseURL = '/api/otec/cursos';
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
     * Lista todos los cursos según filtros.
     * @param {Object} filters - Filtros opcionales (etiqueta, vigencia, search)
     * @returns {Promise<Array>} Lista de cursos
     */
    async getCourses(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.etiqueta) params.append('etiqueta', filters.etiqueta);
            if (filters.vigencia) params.append('vigencia', filters.vigencia);
            if (filters.search) params.append('search', filters.search);

            const url = `${this.baseURL}${params.toString() ? '?' + params : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo cursos:', error);
            throw error;
        }
    }

    /**
     * Obtiene los detalles de un curso específico.
     * @param {number} id - ID del curso
     * @returns {Promise<Object>} Datos del curso
     */
    async getCourse(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo curso:', error);
            throw error;
        }
    }

    /**
     * Crea un nuevo curso.
     * @param {Object} courseData - Datos del curso
     * @returns {Promise<Object>} Curso creado
     */
    async createCourse(courseData) {
        try {
            const response = await fetch(this.baseURL, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(courseData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando curso:', error);
            throw error;
        }
    }

    /**
     * Actualiza un curso existente.
     * @param {number} id - ID del curso
     * @param {Object} courseData - Datos actualizados
     * @returns {Promise<Object>} Curso actualizado
     */
    async updateCourse(id, courseData) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(courseData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando curso:', error);
            throw error;
        }
    }

    /**
     * Elimina un curso.
     * @param {number} id - ID del curso
     * @returns {Promise<void>}
     */
    async deleteCourse(id) {
        try {
            const response = await fetch(`${this.baseURL}/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando curso:', error);
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
window.coursesAPI = new CoursesAPI();

