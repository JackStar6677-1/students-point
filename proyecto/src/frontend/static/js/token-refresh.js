/**
 * Servicio de renovación automática de tokens JWT
 * Renueva el access_token automáticamente antes de que expire
 */

(function() {
    'use strict';

    class TokenRefreshService {
        constructor() {
            this.refreshInterval = null;
            // Renovar token cada 50 minutos (antes de que expire a los 60 minutos)
            this.refreshIntervalMs = 50 * 60 * 1000; // 50 minutos
            this.isRefreshing = false;
        }

        /**
         * Inicia el servicio de renovación automática
         */
        start() {
            if (this.refreshInterval) {
                console.log('Token refresh service ya está activo');
                return;
            }

            console.log('Iniciando servicio de renovación automática de tokens');
            
            // Renovar inmediatamente si el token está próximo a expirar
            this.checkAndRefreshToken();
            
            // Configurar intervalo de renovación
            this.refreshInterval = setInterval(() => {
                this.checkAndRefreshToken();
            }, this.refreshIntervalMs);
        }

        /**
         * Detiene el servicio de renovación automática
         */
        stop() {
            if (this.refreshInterval) {
                console.log('Deteniendo servicio de renovación de tokens');
                clearInterval(this.refreshInterval);
                this.refreshInterval = null;
            }
        }

        /**
         * Verifica y renueva el token si es necesario
         */
        async checkAndRefreshToken() {
            // Evitar múltiples renovaciones simultáneas
            if (this.isRefreshing) {
                console.log('Ya hay una renovación de token en progreso');
                return;
            }

            const refreshToken = localStorage.getItem('refresh_token');
            
            if (!refreshToken) {
                console.warn('No hay refresh token disponible');
                this.stop();
                return;
            }

            try {
                this.isRefreshing = true;
                console.log('Renovando access token...');
                
                const response = await fetch('/api/auth/token/refresh/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        refresh: refreshToken
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // Guardar nuevo access token
                    localStorage.setItem('access_token', data.access);
                    
                    // Si el servidor devuelve un nuevo refresh token (rotación activada)
                    if (data.refresh) {
                        localStorage.setItem('refresh_token', data.refresh);
                    }
                    
                    console.log('✓ Access token renovado exitosamente');
                    
                    // Disparar evento personalizado para que otras partes de la app se actualicen
                    window.dispatchEvent(new CustomEvent('tokenRefreshed', {
                        detail: { accessToken: data.access }
                    }));
                } else {
                    console.error('Error al renovar token:', response.status);
                    
                    if (response.status === 401) {
                        console.warn('Refresh token inválido o expirado');
                        this.handleInvalidRefreshToken();
                    }
                }
            } catch (error) {
                console.error('Error en renovación de token:', error);
            } finally {
                this.isRefreshing = false;
            }
        }

        /**
         * Maneja el caso de refresh token inválido
         */
        handleInvalidRefreshToken() {
            console.warn('Refresh token inválido - cerrando sesión');
            
            // Limpiar tokens
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            
            // Detener servicio
            this.stop();
            
            // Disparar evento de logout
            window.dispatchEvent(new Event('tokenExpired'));
            
            // Redirigir a login después de un breve delay
            setTimeout(() => {
                if (window.location.pathname !== '/login.html') {
                    window.location.href = '/login.html?session_expired=true';
                }
            }, 1000);
        }

        /**
         * Renueva el token manualmente (para usar al hacer login)
         */
        async refreshNow() {
            return await this.checkAndRefreshToken();
        }
    }

    // Crear instancia global
    window.tokenRefreshService = new TokenRefreshService();

    // Auto-iniciar si hay tokens almacenados
    document.addEventListener('DOMContentLoaded', () => {
        const accessToken = localStorage.getItem('access_token');
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (accessToken && refreshToken) {
            console.log('Detectados tokens - iniciando servicio de renovación');
            window.tokenRefreshService.start();
        }
    });

    // Escuchar eventos de login para iniciar el servicio
    window.addEventListener('userLoggedIn', () => {
        console.log('Usuario autenticado - iniciando servicio de renovación');
        window.tokenRefreshService.start();
    });

    // Escuchar eventos de logout para detener el servicio
    window.addEventListener('userLoggedOut', () => {
        console.log('Usuario desautenticado - deteniendo servicio de renovación');
        window.tokenRefreshService.stop();
    });

})();

