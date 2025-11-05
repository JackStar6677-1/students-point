/**
 * Script común para verificar sesión y mostrar perfil/login en el header
 * Debe incluirse en todas las páginas HTML que requieren autenticación
 */

(function() {
    'use strict';

    let currentUser = null;

    /**
     * Inicializa la verificación de sesión y actualiza el header
     */
    async function initAuthHeader() {
        try {
            // Verificar si authAPI está disponible
            if (!window.authAPI) {
                console.warn('authAPI no disponible, usando fallback');
                await loadUserWithFallback();
                return;
            }

            // Verificar autenticación
            if (!window.authAPI.isAuthenticated()) {
                showLoginButtons();
                return;
            }

            // Cargar datos del usuario
            currentUser = await window.authAPI.getCurrentUser();
            showUserProfile();
            
        } catch (error) {
            console.error('Error inicializando auth header:', error);
            showLoginButtons();
        }
    }

    /**
     * Carga el usuario usando método fallback
     */
    async function loadUserWithFallback() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            showLoginButtons();
            return;
        }

        try {
            const response = await fetch('/api/auth/me/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                currentUser = await response.json();
                showUserProfile();
            } else {
                showLoginButtons();
            }
        } catch (error) {
            console.error('Error cargando usuario:', error);
            showLoginButtons();
        }
    }

    /**
     * Muestra los botones de login en el header
     */
    function showLoginButtons() {
        // Buscar contenedor de auth buttons
        const authContainers = document.querySelectorAll('.auth-buttons, .header-right, [id*="auth"], [class*="auth"]');
        
        authContainers.forEach(container => {
            if (!container) return;
            
            // Limpiar contenido
            container.innerHTML = '';
            
            // Crear botones de login
            const loginBtn = document.createElement('a');
            loginBtn.href = '/login.html';
            loginBtn.className = 'btn btn-primary btn-sm';
            loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Iniciar Sesión';
            
            const registerBtn = document.createElement('a');
            registerBtn.href = '/register.html';
            registerBtn.className = 'btn btn-outline-primary btn-sm ms-2';
            registerBtn.innerHTML = '<i class="fas fa-user-plus"></i> Registrarse';
            
            container.appendChild(loginBtn);
            container.appendChild(registerBtn);
        });

        // También actualizar sidebar si existe
        updateSidebarUser(null);
    }

    /**
     * Muestra el perfil del usuario en el header
     */
    function showUserProfile() {
        if (!currentUser) return;

        // Buscar contenedor de auth buttons
        const authContainers = document.querySelectorAll('.auth-buttons, .header-right, [id*="auth"], [class*="auth"]');
        
        authContainers.forEach(container => {
            if (!container) return;
            
            // Limpiar contenido
            container.innerHTML = '';
            
            // Crear dropdown de usuario
            const userDropdown = document.createElement('div');
            userDropdown.className = 'dropdown';
            userDropdown.innerHTML = `
                <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-user-circle me-1"></i>
                    ${escapeHtml(currentUser.name || currentUser.email || 'Usuario')}
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                    <li><a class="dropdown-item" href="/account.html"><i class="fas fa-user me-2"></i>Mi Perfil</a></li>
                    <li><a class="dropdown-item" href="/"><i class="fas fa-home me-2"></i>Inicio</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout(); return false;"><i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión</a></li>
                </ul>
            `;
            
            container.appendChild(userDropdown);
        });

        // Actualizar sidebar si existe
        updateSidebarUser(currentUser);
    }

    /**
     * Actualiza la información del usuario en el sidebar
     */
    function updateSidebarUser(user) {
        const userNameElements = document.querySelectorAll('#sidebarUserName, #userName, .user-name');
        const userRoleElements = document.querySelectorAll('#sidebarUserRole, #userRole, .user-role');
        
        userNameElements.forEach(el => {
            if (el && user) {
                el.textContent = user.name || user.email || 'Usuario';
            } else if (el) {
                el.textContent = 'Invitado';
            }
        });

        userRoleElements.forEach(el => {
            if (el && user) {
                el.textContent = user.career || 'Estudiante';
            } else if (el) {
                el.textContent = 'No autenticado';
            }
        });
    }

    /**
     * Escapa HTML para prevenir XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAuthHeader);
    } else {
        initAuthHeader();
    }

    // Exportar función para re-inicializar si es necesario
    window.initAuthHeader = initAuthHeader;
})();

