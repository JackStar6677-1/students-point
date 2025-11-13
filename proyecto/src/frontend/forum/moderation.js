// Moderation Panel JavaScript
class ModerationManager {
    constructor() {
        this.currentUser = null;
        this.currentPostId = null;
        this.forums = [];
        this.posts = [];
        this.stats = {
            revision: 0,
            reported: 0,
            hidden: 0,
            approved: 0
        };
        this.init();
    }

    async init() {
        try {
            await this.loadUser();
            await this.verifyModeratorPermissions();
            await this.loadForums();
            await this.loadPosts();
            this.setupEventListeners();
        } catch (error) {
            console.error('Error inicializando panel de moderación:', error);
        }
    }

    async loadUser() {
        try {
            if (!window.authAPI || !window.authAPI.isAuthenticated()) {
                window.location.href = '/login.html';
                throw new Error('Usuario no autenticado');
            }

            this.currentUser = await window.authAPI.getCurrentUser();
            if (this.currentUser) {
                this.updateUserInterface();
            }
        } catch (error) {
            console.error('Error cargando usuario:', error);
            if (window.authAPI) {
                window.authAPI.logout();
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            }
            window.location.href = '/login.html';
            throw error;
        }
    }

    async verifyModeratorPermissions() {
        if (!this.currentUser || !this.canModerate()) {
            this.showAlert('No tienes permisos para acceder a esta página', 'danger');
            setTimeout(() => {
                window.location.href = '/index.html';
            }, 2000);
            throw new Error('Permisos insuficientes');
        }
    }

    async loadForums() {
        try {
            if (!window.forumAPI) {
                throw new Error('Servicio de foros no disponible');
            }
            this.forums = await window.forumAPI.getForums();
            this.populateForumSelect();
        } catch (error) {
            console.error('Error loading forums:', error);
            if (!this.forums.length) {
                this.forums = this.getSampleForums();
                this.populateForumSelect();
            }
        }
    }

    async loadPosts() {
        try {
            this.showLoading(true);

            if (!window.forumAPI) {
                throw new Error('Servicio de foros no disponible');
            }

            const forumFilterElement = document.getElementById('forumFilter');
            const statusFilterElement = document.getElementById('statusFilter');
            const reportsFilterElement = document.getElementById('reportsFilter');
            const dateFilterElement = document.getElementById('dateFilter');

            const filters = {};
            if (forumFilterElement && forumFilterElement.value) {
                filters.foro_id = forumFilterElement.value;
            }
            if (statusFilterElement && statusFilterElement.value) {
                filters.estado = statusFilterElement.value;
            }

            let queue = await window.forumAPI.getModerationQueue(filters);

            if (!Array.isArray(queue)) {
                queue = queue?.results || [];
            }

            let filteredPosts = [...queue];

            if (reportsFilterElement && reportsFilterElement.value) {
                if (reportsFilterElement.value === 'reported') {
                    filteredPosts = filteredPosts.filter(post => (post.total_reportes || 0) > 0);
                } else if (reportsFilterElement.value === 'no-reports') {
                    filteredPosts = filteredPosts.filter(post => (post.total_reportes || 0) === 0);
                }
            }

            if (dateFilterElement && dateFilterElement.value) {
                const selectedDate = new Date(dateFilterElement.value);
                filteredPosts = filteredPosts.filter(post => {
                    const postDate = new Date(post.created_at);
                    return postDate.toDateString() === selectedDate.toDateString();
                });
            }

            this.calculateStats(queue);
            this.posts = filteredPosts;
            this.renderPosts();
            this.updateStatsDisplay();
        } catch (error) {
            console.error('Error loading posts:', error);
            this.showAlert(error.message || 'Error al cargar los posts en moderación', 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    calculateStats(sourcePosts = null) {
        const posts = Array.isArray(sourcePosts) ? sourcePosts : this.posts;
        this.stats = {
            revision: posts.filter(p => p.estado === 'revision').length,
            reported: posts.filter(p => (p.total_reportes || 0) > 0).length,
            hidden: posts.filter(p => p.estado === 'oculto').length,
            approved: posts.filter(p => p.estado === 'publicado' && this.isToday(p.created_at)).length
        };
    }

    updateStatsDisplay() {
        document.getElementById('revisionCount').textContent = this.stats.revision;
        document.getElementById('reportedCount').textContent = this.stats.reported;
        document.getElementById('hiddenCount').textContent = this.stats.hidden;
        document.getElementById('approvedCount').textContent = this.stats.approved;
        document.getElementById('pendingCount').textContent = this.stats.revision;
    }

    populateForumSelect() {
        const forumFilter = document.getElementById('forumFilter');
        forumFilter.innerHTML = '<option value="">Todos los foros</option>';

        this.forums.forEach(forum => {
            const option = new Option(forum.titulo, forum.id);
            forumFilter.add(option);
        });
    }

    renderPosts() {
        const container = document.getElementById('postsContainer');
        
        if (this.posts.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-shield-alt fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No hay posts para moderar</h4>
                    <p class="text-muted">Todos los posts están bajo control</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.posts.map(post => this.renderPost(post)).join('');
    }

    renderPost(post) {
        const statusClass = post.estado.toLowerCase();
        const statusText = this.getStatusText(post.estado);
        const isAnonymous = post.anonimo;
        const userName = isAnonymous ? 'Usuario Anónimo' : (post.usuario_name || 'Usuario');
        const priorityClass = this.getPriorityClass(post);
        
        return `
            <div class="card post-card ${statusClass} ${priorityClass} mb-3" data-post-id="${post.id}">
                <div class="card-body">
                    <div class="post-header">
                        <div>
                            <h5 class="card-title mb-1">${this.escapeHtml(post.titulo)}</h5>
                            <div class="post-meta">
                                <span class="anonymous-user">${userName}</span> • 
                                <span>${this.formatDate(post.created_at)}</span>
                                ${post.updated_at !== post.created_at ? `• <span class="text-muted">Editado</span>` : ''}
                            </div>
                        </div>
                        <div class="score-display ${this.getScoreClass(post.score)}">
                            <i class="fas fa-arrow-up"></i>
                            <span>${post.score}</span>
                        </div>
                    </div>
                    
                    <div class="card-text">
                        ${this.escapeHtml(post.cuerpo).replace(/\n/g, '<br>')}
                    </div>
                    
                    <div class="post-actions">
                        <button class="btn btn-success btn-sm" onclick="moderationManager.moderatePost(${post.id}, 'aprobar')">
                            <i class="fas fa-check"></i> Aprobar
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="moderationManager.moderatePost(${post.id}, 'rechazar')">
                            <i class="fas fa-times"></i> Rechazar
                        </button>
                        <button class="btn btn-warning btn-sm" onclick="moderationManager.moderatePost(${post.id}, 'ocultar')">
                            <i class="fas fa-eye-slash"></i> Ocultar
                        </button>
                        <button class="btn btn-info btn-sm" onclick="moderationManager.showReports(${post.id})">
                            <i class="fas fa-flag"></i> Reportes (${post.total_reportes || 0})
                        </button>
                        <button class="btn btn-secondary btn-sm" onclick="moderationManager.showFullModeration(${post.id})">
                            <i class="fas fa-cog"></i> Moderar
                        </button>
                    </div>
                    
                    <div class="mt-2">
                        <span class="badge bg-${this.getStatusColor(post.estado)} status-badge">
                            ${statusText}
                        </span>
                        ${post.total_reportes > 0 ? `
                            <span class="badge bg-danger status-badge">
                                ${post.total_reportes} reporte${post.total_reportes > 1 ? 's' : ''}
                            </span>
                        ` : ''}
                        ${this.getPriorityBadge(post)}
                    </div>
                    
                    ${post.razon_moderacion ? `
                        <div class="moderation-panel">
                            <h6><i class="fas fa-shield-alt me-2"></i>Moderación Anterior</h6>
                            <p class="mb-0">${this.escapeHtml(post.razon_moderacion)}</p>
                            <small class="text-muted">
                                Moderado por ${post.moderado_por?.name || 'Sistema'} 
                                ${post.moderado_at ? `el ${this.formatDate(post.moderado_at)}` : ''}
                            </small>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    getPriorityClass(post) {
        if (post.total_reportes >= 3) return 'priority-high';
        if (post.total_reportes >= 1) return 'priority-medium';
        if (post.estado === 'revision') return 'priority-low';
        return '';
    }

    getPriorityBadge(post) {
        if (post.total_reportes >= 3) {
            return '<span class="badge bg-danger status-badge">ALTA PRIORIDAD</span>';
        }
        if (post.total_reportes >= 1) {
            return '<span class="badge bg-warning text-dark status-badge">PRIORIDAD MEDIA</span>';
        }
        if (post.estado === 'revision') {
            return '<span class="badge bg-info status-badge">PENDIENTE</span>';
        }
        return '';
    }

    async moderatePost(postId, action) {
        try {
            const reason = prompt(`Razón para ${action} el post:`);
            
            if (reason === null) return; // User cancelled

            await window.forumAPI.moderatePost(postId, {
                accion: action,
                razon: reason || ''
            });

            this.showAlert(`Post ${action}do exitosamente`, 'success');
            await this.loadPosts(); // Reload to show updated status
        } catch (error) {
            console.error('Error moderating post:', error);
            this.showAlert(error.message || 'Error al moderar el post', 'danger');
        }
    }

    async showFullModeration(postId) {
        this.currentPostId = postId;
        
        // Load post details for preview
        const post = this.posts.find(p => p.id === postId);
        if (post) {
            const postPreview = document.getElementById('postPreview');
            if (postPreview) {
                postPreview.innerHTML = this.renderPostPreview(post);
            }
        }
        
        const modal = new bootstrap.Modal(document.getElementById('moderationModal'));
        modal.show();
    }

    renderPostPreview(post) {
        const isAnonymous = post.anonimo;
        const userName = isAnonymous ? 'Usuario Anónimo' : (post.usuario_name || 'Usuario');
        
        return `
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">${this.escapeHtml(post.titulo)}</h6>
                    <p class="card-text text-muted mb-2">
                        Por ${userName} • ${this.formatDate(post.created_at)}
                    </p>
                    <p class="card-text">${this.escapeHtml(post.cuerpo).replace(/\n/g, '<br>')}</p>
                    <div class="d-flex gap-2">
                        <span class="badge bg-${this.getStatusColor(post.estado)}">${this.getStatusText(post.estado)}</span>
                        ${post.total_reportes > 0 ? `<span class="badge bg-danger">${post.total_reportes} reportes</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    async showReports(postId) {
        this.currentPostId = postId;
        
        try {
            if (!window.forumAPI) {
                throw new Error('Servicio de foros no disponible');
            }

            const reports = await window.forumAPI.getPostReports(postId);
            const reportsList = document.getElementById('reportsList');
            if (reportsList) {
                reportsList.innerHTML = this.renderReports(reports);
            }
        } catch (error) {
            console.error('Error loading reports:', error);
            const reportsList = document.getElementById('reportsList');
            if (reportsList) {
                reportsList.innerHTML = `<p class="text-muted">Error al cargar los reportes: ${error.message || ''}</p>`;
            }
        }
        
        const modal = new bootstrap.Modal(document.getElementById('reportsModal'));
        modal.show();
    }

    renderReports(reports) {
        if (reports.length === 0) {
            return '<p class="text-muted text-center">No hay reportes para este post</p>';
        }

        return reports.map(report => `
            <div class="card mb-2">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="card-title mb-1">${this.getReportTypeText(report.tipo)}</h6>
                            <p class="card-text text-muted mb-1">
                                Reportado por ${report.usuario_name || 'Usuario'} • ${this.formatDate(report.created_at)}
                            </p>
                            ${report.descripcion ? `<p class="card-text">${this.escapeHtml(report.descripcion)}</p>` : ''}
                        </div>
                        <span class="badge bg-danger">${this.getReportTypeText(report.tipo)}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async submitModeration() {
        try {
            const action = document.getElementById('moderationAction').value;
            const reason = document.getElementById('moderationReason').value;

            if (!action) {
                this.showAlert('Por favor selecciona una acción', 'warning');
                return;
            }

            await window.forumAPI.moderatePost(this.currentPostId, {
                accion: action,
                razon: reason
            });

            this.showAlert(`Post ${action}do exitosamente`, 'success');
            bootstrap.Modal.getInstance(document.getElementById('moderationModal')).hide();
            await this.loadPosts(); // Reload to show updated status
        } catch (error) {
            console.error('Error moderating post:', error);
            this.showAlert(error.message || 'Error al moderar el post', 'danger');
        }
    }

    setupEventListeners() {
        // Filter changes
        document.getElementById('forumFilter').addEventListener('change', () => this.loadPosts());
        document.getElementById('statusFilter').addEventListener('change', () => this.loadPosts());
        document.getElementById('reportsFilter').addEventListener('change', () => this.loadPosts());
        document.getElementById('dateFilter').addEventListener('change', () => this.loadPosts());

        // Modal form resets
        document.getElementById('moderationModal').addEventListener('hidden.bs.modal', () => {
            document.getElementById('moderationForm').reset();
        });
    }

    canModerate() {
        if (!this.currentUser) {
            return false;
        }

        const role = this.currentUser.role;
        return Boolean(
            this.currentUser.is_staff ||
            this.currentUser.is_superuser ||
            ['moderator', 'director_carrera', 'admin_global'].includes(role)
        );
    }

    updateUserInterface() {
        if (window) {
            window.dispatchEvent(new Event('authChange'));
        }
        const userDropdown = document.querySelector('.navbar-nav .dropdown-toggle');
        if (userDropdown && this.currentUser) {
            userDropdown.innerHTML = `<i class="fas fa-user me-1"></i>${this.currentUser.name}`;
        }
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.style.display = show ? 'block' : 'none';
        }
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    getStatusText(status) {
        const statusMap = {
            'publicado': 'Publicado',
            'revision': 'En revisión',
            'oculto': 'Oculto',
            'rechazado': 'Rechazado'
        };
        return statusMap[status] || status;
    }

    getStatusColor(status) {
        const colorMap = {
            'publicado': 'success',
            'revision': 'warning',
            'oculto': 'danger',
            'rechazado': 'secondary'
        };
        return colorMap[status] || 'secondary';
    }

    getReportTypeText(type) {
        const typeMap = {
            'spam': 'Spam',
            'contenido_inapropiado': 'Contenido Inapropiado',
            'acoso': 'Acoso',
            'desinformacion': 'Desinformación',
            'violencia': 'Violencia',
            'otro': 'Otro'
        };
        return typeMap[type] || type;
    }

    getScoreClass(score) {
        if (score > 0) return 'score-positive';
        if (score < 0) return 'score-negative';
        return 'score-neutral';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    isToday(dateString) {
        const date = new Date(dateString);
        const today = new Date();
        return date.toDateString() === today.toDateString();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for onclick handlers
function submitModeration() {
    moderationManager.submitModeration();
}

function logout() {
    if (window.authAPI) {
        window.authAPI.logout();
    } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
    window.location.href = '/login.html';
}

// Initialize moderation manager
let moderationManager;
document.addEventListener('DOMContentLoaded', () => {
    moderationManager = new ModerationManager();
});
