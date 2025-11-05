/**
 * Servicio API para el módulo de portafolio.
 * Centraliza todas las llamadas HTTP al backend relacionadas con portafolio.
 */

class PortfolioAPI {
    constructor() {
        this.baseURL = '/api/portfolio';
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
     * Obtiene el portafolio completo del usuario actual.
     * @returns {Promise<Object>} Datos completos del portafolio
     */
    async getPortfolioCompleto() {
        try {
            const response = await fetch(`${this.baseURL}/completo/`, {
                headers: this.getHeaders(true)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error obteniendo portafolio completo:', error);
            throw error;
        }
    }

    /**
     * Guarda el portafolio completo del usuario actual.
     * @param {Object} portfolioData - Datos del portafolio a guardar
     * @returns {Promise<Object>} Portafolio guardado
     */
    async savePortfolioCompleto(portfolioData) {
        try {
            const response = await fetch(`${this.baseURL}/completo/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(portfolioData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error guardando portafolio:', error);
            throw error;
        }
    }

    /**
     * Obtiene todos los logros del usuario.
     * @returns {Promise<Array>} Lista de logros
     */
    async getLogros() {
        try {
            const response = await fetch(`${this.baseURL}/logros/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo logros:', error);
            throw error;
        }
    }

    /**
     * Crea un nuevo logro.
     * @param {Object} logroData - Datos del logro
     * @returns {Promise<Object>} Logro creado
     */
    async createLogro(logroData) {
        try {
            const response = await fetch(`${this.baseURL}/logros/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(logroData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando logro:', error);
            throw error;
        }
    }

    /**
     * Actualiza un logro existente.
     * @param {number} id - ID del logro
     * @param {Object} logroData - Datos actualizados
     * @returns {Promise<Object>} Logro actualizado
     */
    async updateLogro(id, logroData) {
        try {
            const response = await fetch(`${this.baseURL}/logros/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(logroData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando logro:', error);
            throw error;
        }
    }

    /**
     * Elimina un logro.
     * @param {number} id - ID del logro
     * @returns {Promise<void>}
     */
    async deleteLogro(id) {
        try {
            const response = await fetch(`${this.baseURL}/logros/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando logro:', error);
            throw error;
        }
    }

    /**
     * Obtiene todos los proyectos del usuario.
     * @returns {Promise<Array>} Lista de proyectos
     */
    async getProyectos() {
        try {
            const response = await fetch(`${this.baseURL}/proyectos/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo proyectos:', error);
            throw error;
        }
    }

    /**
     * Crea un nuevo proyecto.
     * @param {Object} proyectoData - Datos del proyecto
     * @returns {Promise<Object>} Proyecto creado
     */
    async createProyecto(proyectoData) {
        try {
            const response = await fetch(`${this.baseURL}/proyectos/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(proyectoData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando proyecto:', error);
            throw error;
        }
    }

    /**
     * Actualiza un proyecto existente.
     * @param {number} id - ID del proyecto
     * @param {Object} proyectoData - Datos actualizados
     * @returns {Promise<Object>} Proyecto actualizado
     */
    async updateProyecto(id, proyectoData) {
        try {
            const response = await fetch(`${this.baseURL}/proyectos/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(proyectoData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando proyecto:', error);
            throw error;
        }
    }

    /**
     * Elimina un proyecto.
     * @param {number} id - ID del proyecto
     * @returns {Promise<void>}
     */
    async deleteProyecto(id) {
        try {
            const response = await fetch(`${this.baseURL}/proyectos/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando proyecto:', error);
            throw error;
        }
    }

    /**
     * Obtiene todas las experiencias laborales del usuario.
     * @returns {Promise<Array>} Lista de experiencias
     */
    async getExperiencias() {
        try {
            const response = await fetch(`${this.baseURL}/experiencias/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo experiencias:', error);
            throw error;
        }
    }

    /**
     * Crea una nueva experiencia laboral.
     * @param {Object} experienciaData - Datos de la experiencia
     * @returns {Promise<Object>} Experiencia creada
     */
    async createExperiencia(experienciaData) {
        try {
            const response = await fetch(`${this.baseURL}/experiencias/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(experienciaData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando experiencia:', error);
            throw error;
        }
    }

    /**
     * Actualiza una experiencia existente.
     * @param {number} id - ID de la experiencia
     * @param {Object} experienciaData - Datos actualizados
     * @returns {Promise<Object>} Experiencia actualizada
     */
    async updateExperiencia(id, experienciaData) {
        try {
            const response = await fetch(`${this.baseURL}/experiencias/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(experienciaData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando experiencia:', error);
            throw error;
        }
    }

    /**
     * Elimina una experiencia.
     * @param {number} id - ID de la experiencia
     * @returns {Promise<void>}
     */
    async deleteExperiencia(id) {
        try {
            const response = await fetch(`${this.baseURL}/experiencias/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando experiencia:', error);
            throw error;
        }
    }

    /**
     * Obtiene todas las habilidades del usuario.
     * @returns {Promise<Array>} Lista de habilidades
     */
    async getHabilidades() {
        try {
            const response = await fetch(`${this.baseURL}/habilidades/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo habilidades:', error);
            throw error;
        }
    }

    /**
     * Crea una nueva habilidad.
     * @param {Object} habilidadData - Datos de la habilidad
     * @returns {Promise<Object>} Habilidad creada
     */
    async createHabilidad(habilidadData) {
        try {
            const response = await fetch(`${this.baseURL}/habilidades/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(habilidadData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando habilidad:', error);
            throw error;
        }
    }

    /**
     * Actualiza una habilidad existente.
     * @param {number} id - ID de la habilidad
     * @param {Object} habilidadData - Datos actualizados
     * @returns {Promise<Object>} Habilidad actualizada
     */
    async updateHabilidad(id, habilidadData) {
        try {
            const response = await fetch(`${this.baseURL}/habilidades/${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(true),
                body: JSON.stringify(habilidadData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando habilidad:', error);
            throw error;
        }
    }

    /**
     * Elimina una habilidad.
     * @param {number} id - ID de la habilidad
     * @returns {Promise<void>}
     */
    async deleteHabilidad(id) {
        try {
            const response = await fetch(`${this.baseURL}/habilidades/${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(true)
            });

            if (!response.ok && response.status !== 204) {
                await this.handleResponse(response);
            }
        } catch (error) {
            console.error('Error eliminando habilidad:', error);
            throw error;
        }
    }

    /**
     * Obtiene la configuración del portafolio del usuario.
     * @returns {Promise<Object>} Configuración del portafolio
     */
    async getConfiguracion() {
        try {
            const response = await fetch(`${this.baseURL}/config/`, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data[0] : (data?.results?.[0] || data);
        } catch (error) {
            console.error('Error obteniendo configuración:', error);
            throw error;
        }
    }

    /**
     * Actualiza la configuración del portafolio.
     * @param {Object} configData - Datos de configuración
     * @returns {Promise<Object>} Configuración actualizada
     */
    async updateConfiguracion(configData) {
        try {
            const response = await fetch(`${this.baseURL}/config/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(configData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error actualizando configuración:', error);
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
window.portfolioAPI = new PortfolioAPI();

