/**
 * Script para agregar el enlace de administración de reportes en el sidebar
 * Solo visible para usuarios administradores
 */

// Emails de admin permitidos (configurar aquí)
// Usar window.ADMIN_EMAILS para que sea accesible globalmente y evitar conflictos
if (typeof window.ADMIN_EMAILS === 'undefined') {
    window.ADMIN_EMAILS = [
        'admin@studentspoint.app',
        'pablo.elias.miranda.292003@gmail.com'
    ];
}

/**
 * Verifica si el usuario actual es administrador
 */
async function esAdmin() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return false;
        }
        
        const response = await fetch('/api/auth/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            const userEmail = user.email ? user.email.toLowerCase() : '';
            
            // Verificar si es admin por email o por rol
            const adminEmails = window.ADMIN_EMAILS || [];
            const esAdminPorEmail = adminEmails.some(adminEmail => 
                userEmail === adminEmail.toLowerCase()
            );
            
            return esAdminPorEmail || 
                   user.role === 'admin_global' || 
                   user.is_staff || 
                   user.is_superuser;
        }
        return false;
    } catch (error) {
        console.error('Error verificando admin:', error);
        return false;
    }
}

/**
 * Agrega el enlace de administración al sidebar si el usuario es admin
 */
async function agregarEnlaceAdmin() {
    const esAdminUser = await esAdmin();
    
    if (!esAdminUser) {
        return; // No es admin, no agregar enlace
    }
    
    // Buscar el sidebar menu
    const sidebarMenu = document.querySelector('.sidebar-menu');
    if (!sidebarMenu) {
        return; // No hay sidebar menu
    }
    
    // Verificar si ya existe el enlace
    const enlaceExistente = sidebarMenu.querySelector('a[href="/moderacion/"]');
    if (enlaceExistente) {
        // Actualizar el enlace existente para asegurar que tenga el icono y texto correctos
        enlaceExistente.innerHTML = `
            <i class="fas fa-shield-alt"></i>
            <span>Admin</span>
        `;
        return;
    }
    
    // Buscar el enlace del foro para insertar después
    const foroLink = sidebarMenu.querySelector('a[href="/forum/"]');
    if (foroLink) {
        // Crear el nuevo enlace
        const adminLink = document.createElement('a');
        adminLink.href = '/moderacion/';
        adminLink.className = 'menu-item';
        adminLink.innerHTML = `
            <i class="fas fa-shield-alt"></i>
            <span>Admin</span>
        `;
        
        // Insertar después del enlace del foro
        foroLink.parentNode.insertBefore(adminLink, foroLink.nextSibling);
    }
}

// Ejecutar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', agregarEnlaceAdmin);
} else {
    agregarEnlaceAdmin();
}

