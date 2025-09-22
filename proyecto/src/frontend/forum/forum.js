// Forum JavaScript
class ForumManager {
    constructor() {
        this.currentUser = null;
        this.currentPostId = null;
        this.forums = [];
        this.posts = [];
        this.init();
    }

    getSampleForums() {
        return [
            { id: 1, nombre: 'General', descripcion: 'Discusiones generales' },
            { id: 2, nombre: 'Académico', descripcion: 'Temas académicos' },
            { id: 3, nombre: 'Social', descripcion: 'Actividades sociales' }
        ];
    }

    getSamplePosts() {
        return [
            {
                id: 1,
                titulo: 'Bienvenidos al foro',
                contenido: 'Este es un post de ejemplo para demostrar la funcionalidad del foro.',
                autor: 'Admin',
                fecha_creacion: new Date().toISOString(),
                foro: { nombre: 'General' },
                likes: 5,
                respuestas: 3
            },
            {
                id: 2,
                titulo: 'Consulta sobre horarios',
                contenido: '¿Alguien sabe dónde puedo consultar los horarios de clases?',
                autor: 'Estudiante',
                fecha_creacion: new Date(Date.now() - 86400000).toISOString(),
                foro: { nombre: 'Académico' },
                likes: 2,
                respuestas: 1
            },
            {
                id: 3,
                titulo: 'Evento social próximo',
                contenido: 'Se está organizando un evento social para el próximo fin de semana.',
                autor: 'Organizador',
                fecha_creacion: new Date(Date.now() - 172800000).toISOString(),
                foro: { nombre: 'Social' },
                likes: 8,
                respuestas: 5
            }
        ];
    }

    async init() {
        await this.loadUser();
        await this.loadForums();
        await this.loadPosts();
        this.setupEventListeners();
        this.checkModeratorPermissions();
    }

    async loadUser() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = '../index.html';
                return;
            }

            const response = await fetch('/api/auth/me/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                this.currentUser = await response.json();
                this.updateUserInterface();
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '../index.html';
            }
        } catch (error) {
            console.error('Error loading user:', error);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '../index.html';
        }
    }

    async loadForums() {
        try {
            const response = await fetch('/api/forum/');
            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    this.forums = await response.json();
                } else {
                    // Si no es JSON, usar datos de ejemplo
                    this.forums = this.getSampleForums();
                }
                this.populateForumSelects();
            } else {
                // Si falla la API, usar datos de ejemplo
                this.forums = this.getSampleForums();
                this.populateForumSelects();
            }
        } catch (error) {
            console.error('Error loading forums:', error);
            // En caso de error, usar datos de ejemplo
            this.forums = this.getSampleForums();
            this.populateForumSelects();
        }
    }

    async loadPosts() {
        try {
            this.showLoading(true);
            
            const params = new URLSearchParams();
            const forumFilterElement = document.getElementById('forumFilter');
            const sortFilterElement = document.getElementById('sortFilter');
            const statusFilterElement = document.getElementById('statusFilter');
            
            const forumFilter = forumFilterElement ? forumFilterElement.value : '';
            const sortFilter = sortFilterElement ? sortFilterElement.value : '';
            const statusFilter = statusFilterElement ? statusFilterElement.value : '';

            if (forumFilter) params.append('foro_id', forumFilter);
            if (sortFilter) params.append('orden', sortFilter);
            if (statusFilter) params.append('estado', statusFilter);

            const response = await fetch(`/api/posts/?${params}`);
            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    this.posts = await response.json();
                } else {
                    // Si no es JSON, usar datos de ejemplo
                    this.posts = this.getSamplePosts();
                }
                this.renderPosts();
            } else {
                // Si falla la API, usar datos de ejemplo
                this.posts = this.getSamplePosts();
                this.renderPosts();
            }
        } catch (error) {
            console.error('Error loading posts:', error);
            // En caso de error, usar datos de ejemplo
            this.posts = this.getSamplePosts();
            this.renderPosts();
        } finally {
            this.showLoading(false);
        }
    }

    populateForumSelects() {
        const forumFilter = document.getElementById('forumFilter');
        const postForum = document.getElementById('postForum');
        
        // Clear existing options
        forumFilter.innerHTML = '<option value="">Todos los foros</option>';
        postForum.innerHTML = '<option value="">Selecciona un foro</option>';

        this.forums.forEach(forum => {
            const option1 = new Option(forum.titulo, forum.id);
            const option2 = new Option(forum.titulo, forum.id);
            forumFilter.add(option1);
            postForum.add(option2);
        });
    }

    renderPosts() {
        const container = document.getElementById('postsContainer');
        
        if (this.posts.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-comments fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No hay posts disponibles</h4>
                    <p class="text-muted">Sé el primero en crear un post en el foro</p>
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
        
        return `
            <div class="card post-card ${statusClass} mb-3" data-post-id="${post.id}">
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
                        <button class="btn btn-outline-primary btn-sm vote-btn" 
                                onclick="forumManager.votePost(${post.id}, 1)" 
                                data-vote="1">
                            <i class="fas fa-arrow-up"></i> Me gusta
                        </button>
                        <button class="btn btn-outline-danger btn-sm vote-btn" 
                                onclick="forumManager.votePost(${post.id}, -1)" 
                                data-vote="-1">
                            <i class="fas fa-arrow-down"></i> No me gusta
                        </button>
                        <button class="btn btn-outline-secondary btn-sm" 
                                onclick="forumManager.showComments(${post.id})">
                            <i class="fas fa-comments"></i> Comentarios (${post.total_comentarios || 0})
                        </button>
                        <button class="btn btn-outline-warning btn-sm" 
                                onclick="forumManager.reportPost(${post.id})">
                            <i class="fas fa-flag"></i> Reportar
                        </button>
                        ${this.canModerate() ? `
                            <button class="btn btn-outline-info btn-sm" 
                                    onclick="forumManager.moderatePost(${post.id})">
                                <i class="fas fa-shield-alt"></i> Moderar
                            </button>
                        ` : ''}
                    </div>
                    
                    <div class="mt-2">
                        <span class="badge bg-${this.getStatusColor(post.estado)} status-badge">
                            ${statusText}
                        </span>
                        ${post.total_reportes > 0 ? `
                            <span class="badge bg-warning text-dark status-badge">
                                ${post.total_reportes} reporte${post.total_reportes > 1 ? 's' : ''}
                            </span>
                        ` : ''}
                    </div>
                    
                    ${post.razon_moderacion ? `
                        <div class="moderation-panel">
                            <h6><i class="fas fa-shield-alt me-2"></i>Moderación</h6>
                            <p class="mb-0">${this.escapeHtml(post.razon_moderacion)}</p>
                            <small class="text-muted">
                                Moderado por ${post.moderado_por?.name || 'Sistema'} 
                                ${post.moderado_at ? `el ${this.formatDate(post.moderado_at)}` : ''}
                            </small>
                        </div>
                    ` : ''}
                    
                    <div id="comments-${post.id}" class="comment-section" style="display: none;">
                        <!-- Comments will be loaded here -->
                    </div>
                </div>
            </div>
        `;
    }

    async votePost(postId, value) {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/posts/${postId}/votar/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ valor: value })
            });

            if (response.ok) {
                const result = await response.json();
                this.updatePostScore(postId, result.score);
                this.showAlert('Voto registrado correctamente', 'success');
            } else {
                this.showAlert('Error al registrar el voto', 'danger');
            }
        } catch (error) {
            console.error('Error voting:', error);
            this.showAlert('Error al registrar el voto', 'danger');
        }
    }

    updatePostScore(postId, newScore) {
        const postCard = document.querySelector(`[data-post-id="${postId}"]`);
        if (postCard) {
            const scoreDisplay = postCard.querySelector('.score-display span');
            if (scoreDisplay) {
                scoreDisplay.textContent = newScore;
                scoreDisplay.parentElement.className = `score-display ${this.getScoreClass(newScore)}`;
            }
        }
    }

    async showComments(postId) {
        const commentsContainer = document.getElementById(`comments-${postId}`);
        
        if (commentsContainer.style.display === 'none') {
            try {
                const response = await fetch(`/api/posts/${postId}/comentarios/`);
                if (response.ok) {
                    const comments = await response.json();
                    commentsContainer.innerHTML = this.renderComments(comments);
                    commentsContainer.style.display = 'block';
                }
            } catch (error) {
                console.error('Error loading comments:', error);
            }
        } else {
            commentsContainer.style.display = 'none';
        }
    }

    renderComments(comments) {
        if (comments.length === 0) {
            return '<p class="text-muted text-center">No hay comentarios aún</p>';
        }

        return comments.map(comment => `
            <div class="comment-item">
                <div class="comment-meta">
                    <strong>${comment.anonimo ? 'Usuario Anónimo' : (comment.usuario_name || 'Usuario')}</strong>
                    • ${this.formatDate(comment.created_at)}
                </div>
                <div>${this.escapeHtml(comment.cuerpo).replace(/\n/g, '<br>')}</div>
            </div>
        `).join('');
    }

    reportPost(postId) {
        this.currentPostId = postId;
        const modal = new bootstrap.Modal(document.getElementById('reportModal'));
        modal.show();
    }

    async submitReport() {
        try {
            const token = localStorage.getItem('access_token');
            const reportType = document.getElementById('reportType').value;
            const reportDescription = document.getElementById('reportDescription').value;

            if (!reportType) {
                this.showAlert('Por favor selecciona un tipo de reporte', 'warning');
                return;
            }

            const response = await fetch(`/api/posts/${this.currentPostId}/reportar/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tipo: reportType,
                    descripcion: reportDescription
                })
            });

            if (response.ok) {
                this.showAlert('Reporte enviado correctamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('reportModal')).hide();
                this.loadPosts(); // Reload to show updated report count
            } else {
                this.showAlert('Error al enviar el reporte', 'danger');
            }
        } catch (error) {
            console.error('Error submitting report:', error);
            this.showAlert('Error al enviar el reporte', 'danger');
        }
    }

    moderatePost(postId) {
        this.currentPostId = postId;
        const modal = new bootstrap.Modal(document.getElementById('moderationModal'));
        modal.show();
    }

    async submitModeration() {
        try {
            const token = localStorage.getItem('access_token');
            const action = document.getElementById('moderationAction').value;
            const reason = document.getElementById('moderationReason').value;

            if (!action) {
                this.showAlert('Por favor selecciona una acción', 'warning');
                return;
            }

            const response = await fetch(`/api/posts/${this.currentPostId}/moderar/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    accion: action,
                    razon: reason
                })
            });

            if (response.ok) {
                this.showAlert(`Post ${action}do exitosamente`, 'success');
                bootstrap.Modal.getInstance(document.getElementById('moderationModal')).hide();
                this.loadPosts(); // Reload to show updated status
            } else {
                this.showAlert('Error al moderar el post', 'danger');
            }
        } catch (error) {
            console.error('Error moderating post:', error);
            this.showAlert('Error al moderar el post', 'danger');
        }
    }

    async createPost() {
        try {
            const token = localStorage.getItem('access_token');
            const forumId = document.getElementById('postForum').value;
            const title = document.getElementById('postTitle').value;
            const content = document.getElementById('postContent').value;
            const anonymous = document.getElementById('postAnonymous').checked;

            if (!forumId || !title || !content) {
                this.showAlert('Por favor completa todos los campos requeridos', 'warning');
                return;
            }

            const response = await fetch('/api/posts/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    foro: forumId,
                    titulo: title,
                    cuerpo: content,
                    anonimo: anonymous
                })
            });

            if (response.ok) {
                this.showAlert('Post creado correctamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('newPostModal')).hide();
                document.getElementById('newPostForm').reset();
                this.loadPosts();
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Error al crear el post', 'danger');
            }
        } catch (error) {
            console.error('Error creating post:', error);
            this.showAlert('Error al crear el post', 'danger');
        }
    }

    setupEventListeners() {
        // Filter changes
        const forumFilter = document.getElementById('forumFilter');
        const sortFilter = document.getElementById('sortFilter');
        const statusFilter = document.getElementById('statusFilter');
        
        if (forumFilter) {
            forumFilter.addEventListener('change', () => this.loadPosts());
        }
        if (sortFilter) {
            sortFilter.addEventListener('change', () => this.loadPosts());
        }
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.loadPosts());
        }

        // Modal form resets
        const newPostModal = document.getElementById('newPostModal');
        if (newPostModal) {
            newPostModal.addEventListener('hidden.bs.modal', () => {
                const form = document.getElementById('newPostForm');
                if (form) form.reset();
            });
        }

        const reportModal = document.getElementById('reportModal');
        if (reportModal) {
            reportModal.addEventListener('hidden.bs.modal', () => {
                const form = document.getElementById('reportForm');
                if (form) form.reset();
            });
        }

        const moderationModal = document.getElementById('moderationModal');
        if (moderationModal) {
            moderationModal.addEventListener('hidden.bs.modal', () => {
                const form = document.getElementById('moderationForm');
                if (form) form.reset();
            });
        }
    }

    checkModeratorPermissions() {
        if (this.currentUser && this.canModerate()) {
            document.getElementById('moderationLink').style.display = 'block';
        }
    }

    canModerate() {
        return this.currentUser && ['moderator', 'director_carrera', 'admin_global'].includes(this.currentUser.role);
    }

    updateUserInterface() {
        // Update user display in navbar
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

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for onclick handlers
function createPost() {
    forumManager.createPost();
}

function submitReport() {
    forumManager.submitReport();
}

function submitModeration() {
    forumManager.submitModeration();
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '../index.html';
}

// Initialize forum manager
let forumManager;
document.addEventListener('DOMContentLoaded', () => {
    forumManager = new ForumManager();
});
