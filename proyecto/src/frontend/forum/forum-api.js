/**
 * Servicio API para el módulo de foros.
 * Centraliza todas las llamadas HTTP al backend relacionadas con foros.
 */

class ForumAPI {
    constructor() {
        this.baseURL = '/api/forum';
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
                throw new Error(data.detail || data.message || 'Error en la petición');
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
     * Lista todos los foros disponibles.
     * @param {Object} filters - Filtros opcionales (sede, carrera)
     * @returns {Promise<Array>} Lista de foros
     */
    async getForums(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.sede) params.append('sede', filters.sede);
            if (filters.carrera) params.append('carrera', filters.carrera);

            const url = `${this.baseURL}/foros/${params.toString() ? '?' + params : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(false) // Los foros pueden ser públicos
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo foros:', error);
            throw error;
        }
    }

    /**
     * Lista posts según filtros.
     * @param {Object} filters - Filtros (foro_id, orden, estado, limit)
     * @returns {Promise<Array>} Lista de posts
     */
    async getPosts(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.foro_id) params.append('foro_id', filters.foro_id);
            if (filters.orden) params.append('orden', filters.orden);
            if (filters.estado) params.append('estado', filters.estado);
            if (filters.limit) params.append('limit', filters.limit);

            const url = `${this.baseURL}/posts/${params.toString() ? '?' + params : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(false) // Los posts pueden ser públicos
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo posts:', error);
            throw error;
        }
    }

    /**
     * Crea un nuevo post.
     * @param {Object} postData - Datos del post (foro, titulo, cuerpo, tipo, anonimo, imagen, archivo, enlace_url)
     * @returns {Promise<Object>} Post creado
     */
    async createPost(postData) {
        try {
            const isFormData = postData.imagen || postData.archivo;
            let body;

            if (isFormData) {
                body = new FormData();
                Object.keys(postData).forEach(key => {
                    if (postData[key] !== null && postData[key] !== undefined) {
                        if (key === 'imagen' || key === 'archivo') {
                            body.append(key, postData[key]);
                        } else {
                            body.append(key, postData[key]);
                        }
                    }
                });
            } else {
                body = JSON.stringify(postData);
            }

            const response = await fetch(`${this.baseURL}/posts/`, {
                method: 'POST',
                headers: this.getHeaders(true, isFormData),
                body: body
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando post:', error);
            throw error;
        }
    }

    /**
     * Obtiene los comentarios de un post.
     * @param {number} postId - ID del post
     * @returns {Promise<Array>} Lista de comentarios
     */
    async getComments(postId) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/comentarios/`, {
                headers: this.getHeaders(false)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo comentarios:', error);
            throw error;
        }
    }

    /**
     * Crea un comentario en un post.
     * @param {number} postId - ID del post
     * @param {Object} commentData - Datos del comentario (cuerpo, anonimo)
     * @returns {Promise<Object>} Comentario creado
     */
    async createComment(postId, commentData) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/comentarios/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(commentData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error creando comentario:', error);
            throw error;
        }
    }

    /**
     * Vota un post.
     * @param {number} postId - ID del post
     * @param {number} valor - Valor del voto (-1, 0, 1)
     * @returns {Promise<Object>} Score actualizado
     */
    async votePost(postId, valor) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/votar/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify({ valor })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error votando post:', error);
            throw error;
        }
    }

    /**
     * Reporta un post.
     * @param {number} postId - ID del post
     * @param {Object} reportData - Datos del reporte (tipo, descripcion)
     * @returns {Promise<Object>} Reporte creado
     */
    async reportPost(postId, reportData) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/reportar/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(reportData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error reportando post:', error);
            throw error;
        }
    }

    /**
     * Obtiene las opciones de una encuesta.
     * @param {number} postId - ID del post (debe ser tipo encuesta)
     * @returns {Promise<Array>} Lista de opciones de encuesta
     */
    async getPollOptions(postId) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/encuesta/opciones/`, {
                headers: this.getHeaders(false)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo opciones de encuesta:', error);
            throw error;
        }
    }

    /**
     * Vota por una opción de encuesta.
     * @param {number} postId - ID del post
     * @param {number} opcionId - ID de la opción
     * @returns {Promise<Object>} Resultados de la encuesta
     */
    async votePoll(postId, opcionId) {
        try {
            const response = await fetch(
                `${this.baseURL}/posts/${postId}/encuesta/opciones/${opcionId}/votar/`,
                {
                    method: 'POST',
                    headers: this.getHeaders(true)
                }
            );

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error votando en encuesta:', error);
            throw error;
        }
    }

    /**
     * Modera un post (solo moderadores).
     * @param {number} postId - ID del post
     * @param {Object} moderationData - Datos de moderación (accion, razon)
     * @returns {Promise<Object>} Resultado de la moderación
     */
    async moderatePost(postId, moderationData) {
        try {
            const response = await fetch(`${this.baseURL}/posts/${postId}/moderar/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify(moderationData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error moderando post:', error);
            throw error;
        }
    }

    /**
     * Obtiene posts en moderación (solo moderadores).
     * @param {Object} filters - Filtros opcionales
     * @returns {Promise<Array>} Lista de posts en moderación
     */
    async getModerationQueue(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.foro_id) params.append('foro_id', filters.foro_id);
            if (filters.usuario_id) params.append('usuario_id', filters.usuario_id);

            const url = `${this.baseURL}/moderacion${params.toString() ? '?' + params : ''}`;
            const response = await fetch(url, {
                headers: this.getHeaders(true)
            });

            const data = await this.handleResponse(response);
            return Array.isArray(data) ? data : (data?.results || []);
        } catch (error) {
            console.error('Error obteniendo cola de moderación:', error);
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
window.forumAPI = new ForumAPI();

