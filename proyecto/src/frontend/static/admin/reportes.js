// Reportes del Foro - Admin

let reportes = [];
let reportesOriginal = [];

// Emails de admin permitidos (compartida con admin-menu.js)
// Definir en window si no existe (para evitar conflictos de declaración)
if (typeof window.ADMIN_EMAILS === 'undefined') {
    window.ADMIN_EMAILS = [
        'admin@studentspoint.app',
        'pablo.elias.miranda.292003@gmail.com'
    ];
}

// Función para obtener emails de admin
function getAdminEmails() {
    return window.ADMIN_EMAILS || [];
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    verificarAdmin();
});

// Autenticacion
function initAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
    
    // Cargar info del usuario
    cargarInfoUsuario();
}

// Verificar si es admin
async function verificarAdmin() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auth/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            const userEmail = user.email ? user.email.toLowerCase() : '';
            
            // Verificar si es admin por email o por rol
            const adminEmails = getAdminEmails();
            const esAdminPorEmail = adminEmails.some(adminEmail => 
                userEmail === adminEmail.toLowerCase()
            );
            
            const esAdmin = esAdminPorEmail || 
                          user.role === 'admin_global' || 
                          user.is_staff || 
                          user.is_superuser;
            
            if (!esAdmin) {
                mostrarError('No tienes permisos para acceder a esta sección');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
                return;
            }
            
            // Si es admin, cargar reportes
            cargarReportes();
        } else {
            window.location.href = '/login.html';
        }
    } catch (error) {
        console.error('Error verificando admin:', error);
        mostrarError('Error al verificar permisos');
    }
}

// Cargar info del usuario
async function cargarInfoUsuario() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auth/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            document.getElementById('sidebarUserName').textContent = user.name || user.email;
            document.getElementById('sidebarUserRole').textContent = 'Admin';
        }
    } catch (error) {
        console.error('Error cargando info usuario:', error);
    }
}

// Cargar reportes
async function cargarReportes() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/forum/reportes/todos/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            if (response.status === 403) {
                mostrarError('No tienes permisos para ver los reportes');
                return;
            }
            const errorText = await response.text();
            console.error('Error del servidor:', response.status, errorText);
            mostrarError('Error al cargar los reportes');
            return;
        }
        
        let data = await response.json();
        
        // Manejar diferentes formatos de respuesta
        if (Array.isArray(data)) {
            reportes = data;
        } else if (data.results && Array.isArray(data.results)) {
            reportes = data.results;
        } else {
            reportes = [];
        }
        
        reportesOriginal = [...reportes];
        renderizarReportes(reportes);
    } catch (error) {
        console.error('Error cargando reportes:', error);
        mostrarError('Error de conexion al cargar reportes: ' + error.message);
    }
}

// Renderizar reportes
function renderizarReportes(reportesArray) {
    const container = document.getElementById('reportesContainer');
    
    if (reportesArray.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="fas fa-flag fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No se encontraron reportes</h4>
                <p class="text-muted">No hay reportes que coincidan con los filtros seleccionados</p>
            </div>
        `;
        return;
    }
    
    const reportesHTML = reportesArray.map(reporte => {
        // Badge de tipo (sin mostrar pendiente)
        const tipoColors = {
            'spam': 'bg-danger',
            'contenido_inapropiado': 'bg-warning',
            'acoso': 'bg-danger',
            'desinformacion': 'bg-info',
            'violencia': 'bg-danger',
            'otro': 'bg-secondary'
        };
        const tipoColor = tipoColors[reporte.tipo] || 'bg-secondary';
        
        // Badge de estado si el post fue eliminado
        let badgeEstadoEliminado = '';
        if (reporte.estado === 'post_eliminado') {
            badgeEstadoEliminado = '<span class="badge bg-dark badge-estado ms-2"><i class="fas fa-trash"></i> Post Eliminado</span>';
        }
        
        return `
            <div class="col-12 mb-3">
                <div class="glass p-4 reporte-card">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div class="flex-grow-1">
                            <div class="mb-2">
                                <span class="badge ${tipoColor} badge-estado">${reporte.tipo_display || reporte.tipo}</span>
                                ${badgeEstadoEliminado}
                            </div>
                            <h5 class="mb-2">Post Reportado</h5>
                            <p class="mb-1"><strong>Título:</strong> ${reporte.post_titulo || 'Sin título'}</p>
                            <p class="mb-1 text-muted small"><strong>Foro:</strong> ${reporte.post_foro || 'N/A'}</p>
                            <p class="mb-1 text-muted small"><strong>Autor del Post:</strong> ${reporte.post_usuario || 'N/A'}</p>
                            <p class="mb-2 text-muted small"><strong>Contenido:</strong> ${(reporte.post_cuerpo || '').substring(0, 150)}${(reporte.post_cuerpo || '').length > 150 ? '...' : ''}</p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <p class="mb-1"><strong><i class="fas fa-user"></i> Reportado por:</strong></p>
                            <p class="mb-2 text-muted">${reporte.usuario_name || 'N/A'} (${reporte.usuario_email || 'N/A'})</p>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-1"><strong><i class="fas fa-calendar"></i> Fecha:</strong></p>
                            <p class="mb-2 text-muted">${new Date(reporte.created_at).toLocaleString('es-CL')}</p>
                        </div>
                    </div>
                    
                    ${reporte.descripcion ? `
                        <div class="mt-3">
                            <p class="mb-1"><strong><i class="fas fa-comment"></i> Descripción del reporte:</strong></p>
                            <p class="text-muted">${reporte.descripcion}</p>
                        </div>
                    ` : ''}
                    
                    <div class="mt-3 d-flex gap-2">
                        <button class="btn btn-danger btn-sm" onclick="eliminarPost(${reporte.post}, ${reporte.id})" title="Eliminar post y actualizar reportes">
                            <i class="fas fa-trash"></i> Eliminar Post
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = `<div class="row">${reportesHTML}</div>`;
}

// Filtrar reportes
function filtrarReportes() {
    let reportesFiltrados = [...reportesOriginal];
    
    // Filtro por estado
    const estado = document.getElementById('filtroEstado').value;
    if (estado) {
        reportesFiltrados = reportesFiltrados.filter(r => r.estado === estado);
    }
    
    // Filtro por tipo
    const tipo = document.getElementById('filtroTipo').value;
    if (tipo) {
        reportesFiltrados = reportesFiltrados.filter(r => r.tipo === tipo);
    }
    
    // Busqueda
    const busqueda = document.getElementById('busquedaInput').value.toLowerCase();
    if (busqueda) {
        reportesFiltrados = reportesFiltrados.filter(r => 
            (r.post_titulo || '').toLowerCase().includes(busqueda) ||
            (r.post_cuerpo || '').toLowerCase().includes(busqueda) ||
            (r.usuario_name || '').toLowerCase().includes(busqueda) ||
            (r.descripcion || '').toLowerCase().includes(busqueda) ||
            (r.tipo_display || '').toLowerCase().includes(busqueda)
        );
    }
    
    renderizarReportes(reportesFiltrados);
}

// Mostrar mensajes
function mostrarError(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function mostrarExito(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

// Eliminar post
async function eliminarPost(postId, reporteId = null) {
    if (!confirm('¿Estás seguro de que deseas eliminar este post? Esta acción no se puede deshacer y actualizará todos los reportes relacionados.')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/forum/posts/${postId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok || response.status === 204) {
            mostrarExito('Post eliminado correctamente. Los reportes han sido actualizados.');
            // Recargar reportes después de un momento
            setTimeout(() => {
                cargarReportes();
            }, 1000);
        } else {
            const errorData = await response.json().catch(() => ({ error: 'Error al eliminar el post' }));
            mostrarError(errorData.error || errorData.detail || 'Error al eliminar el post');
        }
    } catch (error) {
        console.error('Error eliminando post:', error);
        mostrarError('Error de conexión al eliminar el post');
    }
}

// Actualizar estado del reporte
async function actualizarEstadoReporte(reporteId, nuevoEstado) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/forum/reportes/${reporteId}/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: nuevoEstado })
        });
        
        if (response.ok) {
            mostrarExito('Estado del reporte actualizado');
            cargarReportes();
        } else {
            const errorData = await response.json().catch(() => ({ error: 'Error al actualizar el estado' }));
            mostrarError(errorData.error || errorData.detail || 'Error al actualizar el estado');
        }
    } catch (error) {
        console.error('Error actualizando estado:', error);
        mostrarError('Error de conexión al actualizar el estado');
    }
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login.html';
}

