// Verificar autenticación y redirigir si es necesario
function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    
    // Solo redirigir al login si estamos en una página protegida específica
    const protectedPaths = ['/forum/', '/market/', '/portfolio/', '/account.html'];
    const currentPath = window.location.pathname;
    const isProtectedPath = protectedPaths.some(path => currentPath.includes(path));
    
    if (!token && isProtectedPath) {
        window.location.href = '/login.html';
        return;
    }
    
    // Si hay token y estamos en login/register, redirigir al inicio
    if (token && (window.location.pathname.includes('login.html') || window.location.pathname.includes('register.html'))) {
        window.location.href = '/';
    }
}

// Función para limpiar sesión (solo cuando se hace logout explícito)
function clearSessionAndRedirect() {
    // Limpiar localStorage
    localStorage.clear();
    
    // Limpiar sessionStorage
    sessionStorage.clear();
    
    // Limpiar cookies
    document.cookie.split(";").forEach(function(c) { 
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
    });
    
    // Redirigir al login
    window.location.href = '/login.html';
}

// Función global para hacer logout
window.logout = function() {
    clearSessionAndRedirect();
};

// Función para verificar si el usuario está autenticado
window.isAuthenticated = function() {
    const token = localStorage.getItem('access_token');
    return !!token;
};

// Función para obtener el token de acceso
window.getAccessToken = function() {
    return localStorage.getItem('access_token');
};

// Función para hacer requests autenticados
window.authenticatedFetch = async function(url, options = {}) {
    const token = getAccessToken();
    
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    // Si el token expiró, hacer logout
    if (response.status === 401) {
        clearSessionAndRedirect();
        return;
    }
    
    return response;
};

// Ejecutar verificación de autenticación al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
});

// PWA Installation
let deferredPrompt;
const installBtn = document.getElementById('install-button');

if (installBtn) {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.style.display = 'block';
  });

  installBtn.addEventListener('click', async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log(`User response to the install prompt: ${outcome}`);
      deferredPrompt = null;
      installBtn.style.display = 'none';
    }
  });
}

// Service Worker Registration - Manejado por pwa.js

// Authentication helpers
function getAuthToken() {
  return localStorage.getItem('access_token');
}

function setAuthToken(token) {
  localStorage.setItem('access_token', token);
}

function removeAuthToken() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_email');
}

function isAuthenticated() {
  return !!getAuthToken();
}

function logout() {
  removeAuthToken();
  window.location.href = '/login.html';
}

// API helper
async function apiRequest(url, options = {}) {
  const token = getAuthToken();
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  };
  
  const finalOptions = { ...defaultOptions, ...options };
  
  try {
    const response = await fetch(url, finalOptions);
    
    if (response.status === 401) {
      // Token expirado, redirigir al login
      logout();
      return null;
    }
    
    return response;
  } catch (error) {
    console.error('Error en API request:', error);
    throw error;
  }
}

// Navigation helpers
function showLoginRequired() {
  if (!isAuthenticated()) {
    window.location.href = '/login.html';
    return true;
  }
  return false;
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
  // Check authentication status
  const currentPath = window.location.pathname;
  const protectedPaths = ['/forum/', '/market/', '/portfolio/', '/streetview/'];
  
  if (protectedPaths.some(path => currentPath.includes(path))) {
    if (showLoginRequired()) {
      return;
    }
  }
  
  // Update navigation based on auth status
  updateNavigation();
});

function updateNavigation() {
  const isLoggedIn = isAuthenticated();
  const userEmail = localStorage.getItem('user_email');
  
  // Update login/logout links
  const loginLinks = document.querySelectorAll('.login-link');
  const logoutLinks = document.querySelectorAll('.logout-link');
  const userInfo = document.querySelector('.user-info');
  
  loginLinks.forEach(link => {
    link.style.display = isLoggedIn ? 'none' : 'block';
  });
  
  logoutLinks.forEach(link => {
    link.style.display = isLoggedIn ? 'block' : 'none';
  });
  
  if (userInfo && userEmail) {
    userInfo.textContent = userEmail;
    userInfo.style.display = 'block';
  }
}
