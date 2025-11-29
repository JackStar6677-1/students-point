// Admin - Reportes (Foro, Marketplace, Encuestas)

let reportesForo = [];
let reportesMarketplace = [];
let reportesEncuestas = [];
let reportesOriginal = [];
let tipoContenidoActual = 'todos'; // 'todos', 'foro', 'marketplace', 'encuestas'

// Emails de admin permitidos (compartida con admin-menu.js)
if (typeof window.ADMIN_EMAILS === 'undefined') {
    window.ADMIN_EMAILS = [
        'admin@studentspoint.app',
        'pablo.elias.miranda.292003@gmail.com'
    ];
}

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
    cargarInfoUsuario();
}

// Verificar si es admin
async function verificarAdmin() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/auth/me/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const user = await response.json();
            const userEmail = user.email ? user.email.toLowerCase() : '';
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
                setTimeout(() => window.location.href = '/', 2000);
                return;
            }
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
            headers: { 'Authorization': `Bearer ${token}` }
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

// Cargar todos los reportes
async function cargarReportes() {
    try {
        const token = localStorage.getItem('access_token');
        
        // Cargar reportes de los 3 tipos en paralelo
        const [foroRes, marketRes, pollsRes] = await Promise.all([
            fetch('/api/forum/reportes/todos/', {
                headers: { 'Authorization': `Bearer ${token}` }
            }),
            fetch('/api/market/reportes/todos/', {
                headers: { 'Authorization': `Bearer ${token}` }
            }),
            fetch('/api/polls/reportes/todos/', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
        ]);
        
        // Procesar reportes del foro
        if (foroRes.ok) {
            const data = await foroRes.json();
            reportesForo = Array.isArray(data) ? data : (data.results || []);
            reportesForo = reportesForo.map(r => ({ ...r, tipo_contenido: 'foro' }));
        }
        
        // Procesar reportes de marketplace
        if (marketRes.ok) {
            const data = await marketRes.json();
            reportesMarketplace = Array.isArray(data) ? data : (data.results || []);
            reportesMarketplace = reportesMarketplace.map(r => ({ ...r, tipo_contenido: 'marketplace' }));
        }
        
        // Procesar reportes de encuestas
        if (pollsRes.ok) {
            const data = await pollsRes.json();
            reportesEncuestas = Array.isArray(data) ? data : (data.results || []);
            reportesEncuestas = reportesEncuestas.map(r => ({ ...r, tipo_contenido: 'encuestas' }));
        }
        
        // Combinar todos los reportes
        reportesOriginal = [...reportesForo, ...reportesMarketplace, ...reportesEncuestas];
        
        // Ordenar por fecha (más recientes primero)
        reportesOriginal.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
        filtrarReportes();
    } catch (error) {
        console.error('Error cargando reportes:', error);
        mostrarError('Error de conexión al cargar reportes: ' + error.message);
    }
}

// Cambiar tipo de contenido
function cambiarTipoContenido() {
    tipoContenidoActual = document.getElementById('filtroTipoContenido').value;
    filtrarReportes();
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
        const tipoContenido = reporte.tipo_contenido || 'foro';
        
        // Badge de tipo de contenido
        const tipoContenidoBadges = {
            'foro': '<span class="badge bg-primary badge-estado me-2"><i class="fas fa-comments"></i> Foro</span>',
            'marketplace': '<span class="badge bg-success badge-estado me-2"><i class="fas fa-store"></i> Marketplace</span>',
            'encuestas': '<span class="badge bg-purple badge-estado me-2"><i class="fas fa-poll"></i> Encuesta</span>'
        };
        
        // Badge de tipo de reporte
        const tipoColors = {
            'spam': 'bg-danger',
            'contenido_inapropiado': 'bg-warning',
            'acoso': 'bg-danger',
            'desinformacion': 'bg-info',
            'violencia': 'bg-danger',
            'fraude': 'bg-danger',
            'inapropiado': 'bg-warning',
            'otro': 'bg-secondary'
        };
        const tipoColor = tipoColors[reporte.tipo] || 'bg-secondary';
        
        // Badge de estado eliminado
        let badgeEstadoEliminado = '';
        if (reporte.estado === 'post_eliminado' || reporte.estado === 'producto_eliminado' || reporte.estado === 'poll_eliminado') {
            const textoEliminado = tipoContenido === 'foro' ? 'Post Eliminado' : 
                                   tipoContenido === 'marketplace' ? 'Producto Eliminado' : 
                                   'Encuesta Eliminada';
            badgeEstadoEliminado = `<span class="badge bg-dark badge-estado ms-2"><i class="fas fa-trash"></i> ${textoEliminado}</span>`;
        }
        
        // Información específica según el tipo de contenido
        let tituloContenido = '';
        let infoContenido = '';
        let botonEliminar = '';
        
        if (tipoContenido === 'foro') {
            tituloContenido = 'Post Reportado';
            infoContenido = `
                <p class="mb-1"><strong>Título:</strong> ${reporte.post_titulo || 'Sin título'}</p>
                <p class="mb-1 text-muted small"><strong>Foro:</strong> ${reporte.post_foro || 'N/A'}</p>
                <p class="mb-1 text-muted small"><strong>Autor del Post:</strong> ${reporte.post_usuario || 'N/A'}</p>
                <p class="mb-2 text-muted small"><strong>Contenido:</strong> ${(reporte.post_cuerpo || '').substring(0, 150)}${(reporte.post_cuerpo || '').length > 150 ? '...' : ''}</p>
            `;
            botonEliminar = `<button class="btn btn-danger btn-sm" onclick="eliminarPost(${reporte.post}, ${reporte.id})" title="Eliminar post y actualizar reportes">
                <i class="fas fa-trash"></i> Eliminar Post
            </button>`;
        } else if (tipoContenido === 'marketplace') {
            tituloContenido = 'Producto Reportado';
            infoContenido = `
                <p class="mb-1"><strong>Título:</strong> ${reporte.producto_titulo || 'Sin título'}</p>
                <p class="mb-1 text-muted small"><strong>Vendedor:</strong> ${reporte.producto_vendedor || 'N/A'}</p>
                <p class="mb-2 text-muted small"><strong>Descripción:</strong> ${(reporte.producto_descripcion || '').substring(0, 150)}${(reporte.producto_descripcion || '').length > 150 ? '...' : ''}</p>
            `;
            botonEliminar = `<button class="btn btn-danger btn-sm" onclick="eliminarProducto(${reporte.producto}, ${reporte.id})" title="Eliminar producto y actualizar reportes">
                <i class="fas fa-trash"></i> Eliminar Producto
            </button>`;
        } else if (tipoContenido === 'encuestas') {
            tituloContenido = 'Encuesta Reportada';
            infoContenido = `
                <p class="mb-1"><strong>Título:</strong> ${reporte.poll_titulo || 'Sin título'}</p>
                <p class="mb-1 text-muted small"><strong>Creador:</strong> ${reporte.poll_creador || 'N/A'}</p>
                <p class="mb-2 text-muted small"><strong>Descripción:</strong> ${(reporte.poll_descripcion || '').substring(0, 150)}${(reporte.poll_descripcion || '').length > 150 ? '...' : ''}</p>
            `;
            botonEliminar = `<button class="btn btn-danger btn-sm" onclick="eliminarPoll(${reporte.poll}, ${reporte.id})" title="Eliminar encuesta y actualizar reportes">
                <i class="fas fa-trash"></i> Eliminar Encuesta
            </button>`;
        }
        
        // Usuario que reportó
        const usuarioNombre = tipoContenido === 'marketplace' ? 
            (reporte.reportador_name || 'N/A') : 
            (reporte.usuario_name || 'N/A');
        const usuarioEmail = tipoContenido === 'marketplace' ? 
            (reporte.reportador_email || 'N/A') : 
            (reporte.usuario_email || 'N/A');
        
        return `
            <div class="col-12 mb-3">
                <div class="glass p-4 reporte-card">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div class="flex-grow-1">
                            <div class="mb-2">
                                ${tipoContenidoBadges[tipoContenido] || ''}
                                <span class="badge ${tipoColor} badge-estado">${reporte.tipo_display || reporte.tipo}</span>
                                ${badgeEstadoEliminado}
                            </div>
                            <h5 class="mb-2">${tituloContenido}</h5>
                            ${infoContenido}
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <p class="mb-1"><strong><i class="fas fa-user"></i> Reportado por:</strong></p>
                            <p class="mb-2 text-muted">${usuarioNombre} (${usuarioEmail})</p>
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
                        ${botonEliminar}
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
    
    // Filtro por tipo de contenido
    if (tipoContenidoActual !== 'todos') {
        reportesFiltrados = reportesFiltrados.filter(r => r.tipo_contenido === tipoContenidoActual);
    }
    
    // Filtro por tipo
    const tipo = document.getElementById('filtroTipo').value;
    if (tipo) {
        reportesFiltrados = reportesFiltrados.filter(r => r.tipo === tipo);
    }
    
    // Búsqueda
    const busqueda = document.getElementById('busquedaInput').value.toLowerCase();
    if (busqueda) {
        reportesFiltrados = reportesFiltrados.filter(r => {
            const texto = (
                (r.post_titulo || r.producto_titulo || r.poll_titulo || '') +
                (r.post_cuerpo || r.producto_descripcion || r.poll_descripcion || '') +
                (r.usuario_name || r.reportador_name || '') +
                (r.descripcion || '') +
                (r.tipo_display || '')
            ).toLowerCase();
            return texto.includes(busqueda);
        });
    }
    
    renderizarReportes(reportesFiltrados);
}

// Mostrar mensajes
function mostrarError(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `${mensaje}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function mostrarExito(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `${mensaje}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
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
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok || response.status === 204) {
            mostrarExito('Post eliminado correctamente. Los reportes han sido actualizados.');
            setTimeout(() => cargarReportes(), 1000);
        } else {
            const errorData = await response.json().catch(() => ({ error: 'Error al eliminar el post' }));
            mostrarError(errorData.error || errorData.detail || 'Error al eliminar el post');
        }
    } catch (error) {
        console.error('Error eliminando post:', error);
        mostrarError('Error de conexión al eliminar el post');
    }
}

// Eliminar producto
async function eliminarProducto(productoId, reporteId = null) {
    if (!confirm('¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer y actualizará todos los reportes relacionados.')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/market/productos/${productoId}/`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok || response.status === 204) {
            mostrarExito('Producto eliminado correctamente. Los reportes han sido actualizados.');
            setTimeout(() => cargarReportes(), 1000);
        } else {
            const errorData = await response.json().catch(() => ({ error: 'Error al eliminar el producto' }));
            mostrarError(errorData.error || errorData.detail || 'Error al eliminar el producto');
        }
    } catch (error) {
        console.error('Error eliminando producto:', error);
        mostrarError('Error de conexión al eliminar el producto');
    }
}

// Eliminar encuesta
async function eliminarPoll(pollId, reporteId = null) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta encuesta? Esta acción no se puede deshacer y actualizará todos los reportes relacionados.')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/polls/${pollId}/`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok || response.status === 204) {
            mostrarExito('Encuesta eliminada correctamente. Los reportes han sido actualizados.');
            setTimeout(() => cargarReportes(), 1000);
        } else {
            const errorData = await response.json().catch(() => ({ error: 'Error al eliminar la encuesta' }));
            mostrarError(errorData.error || errorData.detail || 'Error al eliminar la encuesta');
        }
    } catch (error) {
        console.error('Error eliminando encuesta:', error);
        mostrarError('Error de conexión al eliminar la encuesta');
    }
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login.html';
}
