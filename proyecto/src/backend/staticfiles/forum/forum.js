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
                titulo: 'Consulta sobre cursos',
                contenido: '¿Alguien sabe dónde puedo consultar información sobre los cursos?',
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
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    this.currentUser = await response.json();
                    this.updateUserInterface();
                } else {
                    const text = await response.text();
                    console.error('Respuesta no es JSON:', text);
                    throw new Error('Respuesta inválida del servidor');
                }
            } else {
                const errorText = await response.text();
                console.error('Error de autenticación:', errorText);
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
            const token = localStorage.getItem('access_token');
            if (!token) {
                console.log('No hay token de autenticación');
                this.forums = this.getSampleForums();
                this.populateForumSelects();
                return;
            }

            const response = await fetch('/api/forum/foros/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    this.forums = Array.isArray(data) ? data : data.results || [];
                } else {
                    // Si no es JSON, probablemente redirigió a login
                    console.log('Respuesta no es JSON, probablemente no autenticado');
                    this.forums = this.getSampleForums();
                }
            } else {
                // Si falla la API, usar datos de ejemplo
                console.log('Error en API de foros:', response.status);
                this.forums = this.getSampleForums();
            }
            this.populateForumSelects();
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

            const token = localStorage.getItem('access_token');
            const headers = {};
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
                headers['Content-Type'] = 'application/json';
            }

            const response = await fetch(`/api/forum/posts/?${params}`, { headers });
            if (response.ok) {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    this.posts = Array.isArray(data) ? data : data.results || [];
                } else {
                    // Si no es JSON, probablemente redirigió a login
                    console.log('Respuesta no es JSON, probablemente no autenticado');
                    this.posts = this.getSamplePosts();
                }
            } else {
                // Si falla la API, usar datos de ejemplo
                console.log('Error en API de posts:', response.status);
                this.posts = this.getSamplePosts();
            }
            this.renderPosts();
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
        
        // Solo proceder si los elementos existen
        if (forumFilter) {
            // Clear existing options
            forumFilter.innerHTML = '<option value="">Todos los foros</option>';
            this.forums.forEach(forum => {
                const option = new Option(forum.titulo, forum.id);
                forumFilter.add(option);
            });
        }
        
        if (postForum) {
            // Clear existing options
            postForum.innerHTML = '<option value="">Selecciona un foro</option>';
            this.forums.forEach(forum => {
                const option = new Option(forum.titulo, forum.id);
                postForum.add(option);
            });
        }
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
        const tipoClass = post.tipo || 'comentario';
        
        return `
            <div class="post-card fade-in" data-post-id="${post.id}">
                <div class="type-indicator ${tipoClass}"></div>
                <div class="vote-section">
                    <button class="vote-btn upvote" onclick="forumManager.votePost(${post.id}, 1)" title="Upvote">
                        <i class="fas fa-arrow-up"></i>
                    </button>
                    <span class="vote-count ${this.getScoreClass(post.score)}">${post.score}</span>
                    <button class="vote-btn downvote" onclick="forumManager.votePost(${post.id}, -1)" title="Downvote">
                        <i class="fas fa-arrow-down"></i>
                    </button>
                </div>
                <div class="post-content">
                    <div class="post-header">
                        ${post.foro_info ? `
                            <a href="#" class="post-foro-tag" onclick="filterByForum(${post.foro_info.id}); return false;">
                                ${post.foro_info.carrera}
                            </a>
                        ` : ''}
                        <div class="post-author">
                            <strong>${userName}</strong>
                            ${post.usuario_career ? `<span>• ${post.usuario_career}</span>` : ''}
                            <span class="post-time">• ${this.formatDate(post.created_at)}</span>
                        </div>
                        ${tipoClass !== 'comentario' ? `<span class="post-badge badge-${tipoClass}">${tipoClass}</span>` : ''}
                        ${post.estado !== 'publicado' ? `<span class="post-badge badge-${post.estado}">${statusText}</span>` : ''}
                    </div>
                    
                    <h2 class="post-title">${this.escapeHtml(post.titulo)}</h2>
                    
                    <div class="post-body-preview">
                        ${this.escapeHtml(post.cuerpo).replace(/\n/g, '<br>')}
                    </div>
                    
                    ${post.imagen_url ? `
                        <div class="post-image-container">
                            ${!post.imagen_aprobada ? `
                                <div class="image-pending-approval">
                                    <i class="fas fa-clock"></i> Imagen en revisión por moderadores
                                </div>
                            ` : `
                                <img src="${post.imagen_url}" alt="${this.escapeHtml(post.titulo)}" class="post-image" 
                                     onclick="window.open('${post.imagen_url}', '_blank')">
                            `}
                        </div>
                    ` : ''}
                    
                    <div class="post-footer">
                        <button class="post-action" onclick="forumManager.showComments(${post.id})">
                            <i class="fas fa-comment"></i>
                            ${post.total_comentarios || 0} Comentarios
                        </button>
                        <button class="post-action" onclick="forumManager.reportPost(${post.id})">
                            <i class="fas fa-flag"></i>
                            Reportar
                        </button>
                        ${this.canModerate() ? `
                            <button class="post-action" onclick="forumManager.moderatePost(${post.id})">
                                <i class="fas fa-shield-alt"></i>
                                Moderar
                            </button>
                        ` : ''}
                        ${post.total_reportes > 0 ? `
                            <span class="text-warning">
                                <i class="fas fa-exclamation-triangle"></i>
                                ${post.total_reportes} reporte${post.total_reportes > 1 ? 's' : ''}
                            </span>
                        ` : ''}
                    </div>
                    
                    ${post.razon_moderacion ? `
                        <div class="alert alert-warning mt-2">
                            <strong><i class="fas fa-shield-alt me-2"></i>Moderación:</strong>
                            ${this.escapeHtml(post.razon_moderacion)}
                            <br><small>Moderado por ${post.moderado_por?.name || 'Sistema'} 
                            ${post.moderado_at ? `el ${this.formatDate(post.moderado_at)}` : ''}</small>
                        </div>
                    ` : ''}
                    
                    <div id="comments-${post.id}" class="comments-section" style="display: none;">
                        <!-- Comments will be loaded here -->
                    </div>
                </div>
            </div>
        `;
    }

    async votePost(postId, value) {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/forum/posts/${postId}/votar/`, {
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
                const response = await fetch(`/api/forum/posts/${postId}/comentarios/`);
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
            const reportTypeElement = document.getElementById('reportType');
            const reportDescriptionElement = document.getElementById('reportDescription');
            const reportType = reportTypeElement ? reportTypeElement.value : '';
            const reportDescription = reportDescriptionElement ? reportDescriptionElement.value : '';

            if (!reportType) {
                this.showAlert('Por favor selecciona un tipo de reporte', 'warning');
                return;
            }

            const response = await fetch(`/api/forum/posts/${this.currentPostId}/reportar/`, {
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
            const actionElement = document.getElementById('moderationAction');
            const reasonElement = document.getElementById('moderationReason');
            const action = actionElement ? actionElement.value : '';
            const reason = reasonElement ? reasonElement.value : '';

            if (!action) {
                this.showAlert('Por favor selecciona una acción', 'warning');
                return;
            }

            const response = await fetch(`/api/forum/posts/${this.currentPostId}/moderar/`, {
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
            const forumIdElement = document.getElementById('postForum');
            const titleElement = document.getElementById('postTitle');
            const contentElement = document.getElementById('postContent');
            const anonymousElement = document.getElementById('postAnonymous');
            const imageElement = document.getElementById('postImage');
            
            const forumId = forumIdElement ? forumIdElement.value : '';
            const title = titleElement ? titleElement.value : '';
            const content = contentElement ? contentElement.value : '';
            const anonymous = anonymousElement ? anonymousElement.checked : false;

            if (!forumId || !title || !content) {
                this.showAlert('Por favor completa todos los campos requeridos', 'warning');
                return;
            }

            // Usar FormData para soportar subida de imágenes
            const formData = new FormData();
            formData.append('foro', forumId);
            formData.append('titulo', title);
            formData.append('cuerpo', content);
            formData.append('anonimo', anonymous);
            
            // Agregar imagen si existe
            if (imageElement && imageElement.files.length > 0) {
                formData.append('imagen', imageElement.files[0]);
            }

            const response = await fetch('/api/forum/posts/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    // NO incluir Content-Type para que el navegador lo configure con boundary
                },
                body: formData
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
            const moderationLink = document.getElementById('moderationLink');
            if (moderationLink) {
                moderationLink.style.display = 'block';
            }
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

// Image upload handling functions
function handleImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validar tamaño (máx 5MB)
    if (file.size > 5 * 1024 * 1024) {
        alert('La imagen no puede superar los 5MB');
        event.target.value = '';
        return;
    }
    
    // Validar tipo
    if (!file.type.startsWith('image/')) {
        alert('Solo se permiten archivos de imagen');
        event.target.value = '';
        return;
    }
    
    // Mostrar preview
    showImagePreview(file);
}

function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById('imagePreview');
        const container = document.getElementById('imagePreviewContainer');
        if (preview && container) {
            preview.src = e.target.result;
            container.style.display = 'block';
            
            // Ocultar área de upload
            const uploadArea = document.getElementById('imageUploadArea');
            if (uploadArea) {
                uploadArea.style.display = 'none';
            }
        }
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    const input = document.getElementById('postImage');
    const container = document.getElementById('imagePreviewContainer');
    const uploadArea = document.getElementById('imageUploadArea');
    
    if (input) input.value = '';
    if (container) container.style.display = 'none';
    if (uploadArea) uploadArea.style.display = 'block';
}

// Drag and drop handling
document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('imageUploadArea');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const input = document.getElementById('postImage');
                input.files = files;
                handleImageSelect({ target: input });
            }
        });
    }
});

// Helper function para filtrar por foro
function filterByForum(foroId) {
    const forumFilter = document.getElementById('forumFilter');
    if (forumFilter) {
        forumFilter.value = foroId;
        if (forumManager) {
            forumManager.loadPosts();
        }
    }
}

// Initialize forum manager
let forumManager;
document.addEventListener('DOMContentLoaded', () => {
    forumManager = new ForumManager();
});
