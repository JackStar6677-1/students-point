/**
 * Servicio API para autenticación y gestión de usuarios.
 * Centraliza todas las llamadas HTTP relacionadas con autenticación.
 */

class AuthAPI {
    constructor() {
        this.baseURL = '/api/auth';
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
     * @param {boolean} autoLogoutOn401 - Si debe hacer logout automático en 401 (default: false)
     * @returns {Promise} Promise que resuelve con los datos o lanza error
     */
    async handleResponse(response, autoLogoutOn401 = false) {
        // Si es 401 y se solicita logout automático, cerrar sesión inmediatamente
        if (response.status === 401 && autoLogoutOn401) {
            console.warn('Token expirado o inválido. Cerrando sesión...');
            this.logout(true);
            return null; // No continuar procesando
        }
        
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (!response.ok) {
                const errorMsg = data.detail || data.error || data.message || 'Error en la petición';
                
                // Si es 401 y no se pidió logout automático, incluir en el mensaje
                if (response.status === 401) {
                    throw new Error(`401: ${errorMsg}`);
                }
                
                throw new Error(errorMsg);
            }
            return data;
        }

        const text = await response.text();
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error(`401: ${text || 'No autenticado'}`);
            }
            throw new Error(text || 'Error en la petición');
        }
        return text;
    }

    /**
     * Inicia sesión con email y contraseña.
     * @param {string} email - Email del usuario
     * @param {string} password - Contraseña del usuario
     * @returns {Promise<Object>} Tokens y datos del usuario
     */
    async login(email, password) {
        try {
            const response = await fetch(`${this.baseURL}/login/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email, password })
            });

            const data = await this.handleResponse(response);
            
            // Guardar tokens en localStorage
            if (data.access && data.refresh) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
            }
            
            // Guardar datos del usuario
            if (data.user) {
                localStorage.setItem('user_data', JSON.stringify(data.user));
            }
            
            // Disparar evento de login exitoso para iniciar servicio de renovación de tokens
            window.dispatchEvent(new Event('userLoggedIn'));
            
            return data;
        } catch (error) {
            console.error('Error en login:', error);
            throw error;
        }
    }

    /**
     * Registra un nuevo usuario.
     * @param {Object} userData - Datos del usuario (email, password, name, career, etc.)
     * @returns {Promise<Object>} Tokens y datos del usuario
     */
    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/register/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify(userData)
            });

            const data = await this.handleResponse(response);
            
            // Guardar tokens en localStorage
            if (data.access && data.refresh) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
            }
            
            // Guardar datos del usuario
            if (data.user) {
                localStorage.setItem('user_data', JSON.stringify(data.user));
            }
            
            return data;
        } catch (error) {
            console.error('Error en registro:', error);
            throw error;
        }
    }

    /**
     * Obtiene información del usuario actual.
     * @returns {Promise<Object>} Datos del usuario
     */
    async getCurrentUser() {
        try {
            const response = await fetch(`${this.baseURL}/me/`, {
                headers: this.getHeaders(true)
            });

            // Pasar true para logout automático en 401
            const data = await this.handleResponse(response, true);
            
            // Si data es null, ya se hizo logout
            if (!data) {
                return null;
            }
            
            // Actualizar datos en localStorage
            localStorage.setItem('user_data', JSON.stringify(data));
            
            return data;
        } catch (error) {
            console.error('Error obteniendo usuario:', error);
            
            // Si es 401, limpiar tokens y redirigir inmediatamente
            if (error.message.includes('401') || error.message.includes('autenticado') || error.message.includes('Unauthorized')) {
                this.logout(true);
                return null;
            }
            
            throw error;
        }
    }

    /**
     * Actualiza el perfil del usuario.
     * @param {Object} userData - Datos a actualizar
     * @returns {Promise<Object>} Usuario actualizado
     */
    async updateProfile(userData) {
        try {
            const response = await fetch(`${this.baseURL}/me/update/`, {
                method: 'PATCH',
                headers: this.getHeaders(true, userData instanceof FormData),
                body: userData instanceof FormData ? userData : JSON.stringify(userData)
            });

            const data = await this.handleResponse(response);
            
            // Actualizar datos en localStorage
            if (data) {
                localStorage.setItem('user_data', JSON.stringify(data));
            }
            
            return data;
        } catch (error) {
            console.error('Error actualizando perfil:', error);
            throw error;
        }
    }

    /**
     * Verifica si un email está permitido.
     * @param {string} email - Email a verificar
     * @returns {Promise<Object>} Resultado de la verificación
     */
    async checkEmail(email) {
        try {
            const response = await fetch(`${this.baseURL}/check-email/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error verificando email:', error);
            throw error;
        }
    }

    /**
     * Verifica el email con código.
     * @param {string} email - Email del usuario
     * @param {string} codigo - Código de verificación
     * @returns {Promise<Object>} Tokens y datos del usuario
     */
    async verifyEmail(email, codigo) {
        try {
            const response = await fetch(`${this.baseURL}/verificar-email/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email, codigo })
            });

            const data = await this.handleResponse(response);
            
            // Si se generaron tokens, guardarlos
            if (data.access && data.refresh) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
            }
            
            if (data.user) {
                localStorage.setItem('user_data', JSON.stringify(data.user));
            }
            
            return data;
        } catch (error) {
            console.error('Error verificando email:', error);
            throw error;
        }
    }

    /**
     * Reenvía el código de verificación.
     * @param {string} email - Email del usuario
     * @returns {Promise<Object>} Resultado del reenvío
     */
    async resendVerificationCode(email) {
        try {
            const response = await fetch(`${this.baseURL}/reenviar-codigo/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error reenviando código:', error);
            throw error;
        }
    }

    /**
     * Solicita recuperación de contraseña.
     * @param {string} email - Email del usuario
     * @returns {Promise<Object>} Resultado de la solicitud
     */
    async requestPasswordRecovery(email) {
        try {
            const response = await fetch(`${this.baseURL}/recuperar-password/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error solicitando recuperación:', error);
            throw error;
        }
    }

    /**
     * Verifica el código de recuperación.
     * @param {string} email - Email del usuario
     * @param {string} codigo - Código de recuperación
     * @returns {Promise<Object>} Resultado de la verificación
     */
    async verifyRecoveryCode(email, codigo) {
        try {
            const response = await fetch(`${this.baseURL}/verificar-codigo-recuperacion/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ email, codigo })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error verificando código:', error);
            throw error;
        }
    }

    /**
     * Resetea la contraseña con código.
     * @param {string} email - Email del usuario
     * @param {string} codigo - Código de recuperación
     * @param {string} nuevaPassword - Nueva contraseña
     * @param {string} confirmarPassword - Confirmación de contraseña
     * @returns {Promise<Object>} Resultado del reset
     */
    async resetPassword(email, codigo, nuevaPassword, confirmarPassword) {
        try {
            const response = await fetch(`${this.baseURL}/resetear-password/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({
                    email,
                    codigo,
                    nueva_password: nuevaPassword,
                    confirmar_password: confirmarPassword
                })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error reseteando contraseña:', error);
            throw error;
        }
    }

    /**
     * Cambia la contraseña (usuario autenticado).
     * @param {string} passwordActual - Contraseña actual
     * @param {string} nuevaPassword - Nueva contraseña
     * @param {string} confirmarPassword - Confirmación de contraseña
     * @returns {Promise<Object>} Resultado del cambio
     */
    async changePassword(passwordActual, nuevaPassword, confirmarPassword) {
        try {
            const response = await fetch(`${this.baseURL}/cambiar-password/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify({
                    password_actual: passwordActual,
                    nueva_password: nuevaPassword,
                    confirmar_password: confirmarPassword
                })
            });

            return await this.handleResponse(response);
        } catch (error) {
            console.error('Error cambiando contraseña:', error);
            throw error;
        }
    }

    /**
     * Cambia la carrera del usuario.
     * @param {string} nuevaCarrera - Nueva carrera
     * @param {string} razon - Razón del cambio (opcional)
     * @returns {Promise<Object>} Usuario actualizado
     */
    async changeCareer(nuevaCarrera, razon = '') {
        try {
            const response = await fetch(`${this.baseURL}/cambiar-carrera/`, {
                method: 'POST',
                headers: this.getHeaders(true),
                body: JSON.stringify({
                    nueva_carrera: nuevaCarrera,
                    razon: razon
                })
            });

            const data = await this.handleResponse(response);
            
            // Actualizar datos en localStorage
            if (data.user) {
                localStorage.setItem('user_data', JSON.stringify(data.user));
            }
            
            return data;
        } catch (error) {
            console.error('Error cambiando carrera:', error);
            throw error;
        }
    }

    /**
     * Obtiene lista de carreras disponibles.
     * @returns {Promise<Array>} Lista de carreras
     */
    async getCarreras() {
        try {
            const response = await fetch('/api/carreras/', {
                headers: this.getHeaders(false)
            });

            const data = await this.handleResponse(response);
            return data.carreras || [];
        } catch (error) {
            console.error('Error obteniendo carreras:', error);
            throw error;
        }
    }

    /**
     * Cierra sesión, limpia los tokens y redirige al login.
     * @param {boolean} redirect - Si debe redirigir al login (default: true)
     */
    logout(redirect = true) {
        // Limpiar todos los datos del localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        localStorage.removeItem('remember_me');
        localStorage.removeItem('saved_email');
        
        // Disparar evento de logout para detener servicio de renovación de tokens
        window.dispatchEvent(new Event('userLoggedOut'));
        
        // Redirigir al login si se solicita
        if (redirect) {
            // Usar replace para evitar que vuelvan con el botón atrás
            window.location.replace('/login.html');
        }
    }

    /**
     * Verifica si el usuario está autenticado.
     * @returns {boolean} True si hay token válido
     */
    isAuthenticated() {
        return !!this.getAuthToken();
    }

    /**
     * Obtiene los datos del usuario guardados localmente.
     * @returns {Object|null} Datos del usuario o null
     */
    getLocalUserData() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }
}

// Exportar instancia global del servicio API
window.authAPI = new AuthAPI();

