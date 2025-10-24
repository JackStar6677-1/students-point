// StudentsPoint - Sistema de Autenticación Global
// Maneja la autenticación y navegación en todas las páginas

// Verificar si el usuario está autenticado
function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
}

// Obtener información del usuario
function getUserInfo() {
    try {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    } catch (error) {
        console.error('Error parsing user data:', error);
        return null;
    }
}

// Actualizar navegación basada en estado de autenticación
function updateNavigation() {
    const isLoggedIn = isAuthenticated();
    const userInfo = getUserInfo();
    
    // Actualizar botones de login/logout
    const loginButtons = document.querySelectorAll('.login-button, .login-link');
    const logoutButtons = document.querySelectorAll('.logout-button, .logout-link');
    const userMenus = document.querySelectorAll('.user-menu, .user-info');
    
    // Mostrar/ocultar botones de login
    loginButtons.forEach(button => {
        if (button) {
            button.style.display = isLoggedIn ? 'none' : 'inline-block';
        }
    });
    
    // Mostrar/ocultar botones de logout
    logoutButtons.forEach(button => {
        if (button) {
            button.style.display = isLoggedIn ? 'inline-block' : 'none';
        }
    });
    
    // Actualizar información del usuario
    userMenus.forEach(menu => {
        if (menu && userInfo) {
            const nameElement = menu.querySelector('.user-name');
            const emailElement = menu.querySelector('.user-email');
            
            if (nameElement) {
                nameElement.textContent = userInfo.name || userInfo.email;
            }
            if (emailElement) {
                emailElement.textContent = userInfo.email;
            }
            
            menu.style.display = isLoggedIn ? 'block' : 'none';
        }
    });
    
    // Actualizar enlaces de navegación
    const protectedLinks = document.querySelectorAll('.protected-link');
    protectedLinks.forEach(link => {
        if (link) {
            if (isLoggedIn) {
                link.style.display = 'block';
                link.style.pointerEvents = 'auto';
                link.style.opacity = '1';
            } else {
                link.style.display = 'block';
                link.style.pointerEvents = 'none';
                link.style.opacity = '0.5';
                link.title = 'Debes iniciar sesión para acceder';
            }
        }
    });
}

// Función para hacer logout
function logout() {
    // Limpiar localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    localStorage.removeItem('user_email');
    
    // Limpiar sessionStorage
    sessionStorage.clear();
    
    // Limpiar cookies
    document.cookie.split(";").forEach(function(c) { 
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
    });
    
    // Actualizar navegación
    updateNavigation();
    
    // Redirigir al login
    window.location.href = '/login.html';
}

// Función para hacer requests autenticados
async function authenticatedFetch(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        window.location.href = '/login.html';
        return null;
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        // Si el token expiró, hacer logout
        if (response.status === 401) {
            logout();
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('Error en request autenticado:', error);
        throw error;
    }
}

// Verificar autenticación y redirigir si es necesario
function checkAuthentication() {
    const protectedPaths = ['/forum/', '/market/', '/portfolio/', '/streetview/', '/account.html'];
    const currentPath = window.location.pathname;
    const isProtectedPath = protectedPaths.some(path => currentPath.includes(path));
    
    // Si no hay token y estamos en una página protegida, redirigir al login
    if (!isAuthenticated() && isProtectedPath) {
        window.location.href = '/login.html';
        return false;
    }
    
    // Si hay token y estamos en login/register, redirigir al inicio
    if (isAuthenticated() && (currentPath.includes('login.html') || currentPath.includes('register.html'))) {
        window.location.href = '/index.html';
        return false;
    }
    
    return true;
}

// Inicializar autenticación
function initAuth() {
    // Verificar autenticación
    if (!checkAuthentication()) {
        return;
    }
    
    // Actualizar navegación
    updateNavigation();
    
    // Configurar event listeners para logout
    const logoutButtons = document.querySelectorAll('.logout-button, .logout-link');
    logoutButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                logout();
            });
        }
    });
    
    // Configurar event listeners para links protegidos
    const protectedLinks = document.querySelectorAll('.protected-link');
    protectedLinks.forEach(link => {
        if (link) {
            link.addEventListener('click', function(e) {
                if (!isAuthenticated()) {
                    e.preventDefault();
                    window.location.href = '/login.html';
                }
            });
        }
    });
}

// Hacer funciones globales
window.isAuthenticated = isAuthenticated;
window.getUserInfo = getUserInfo;
window.updateNavigation = updateNavigation;
window.logout = logout;
window.authenticatedFetch = authenticatedFetch;
window.initAuth = initAuth;

// Ejecutar inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initAuth();
});

// También ejecutar en window.load por si acaso
window.addEventListener('load', function() {
    updateNavigation();
});

