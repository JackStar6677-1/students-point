/**
 * Encuestas Manager - StudentsPoint
 * Sistema completo de encuestas y votaciones
 */

class EncuestasManager {
    constructor() {
        this.currentUser = null;
        this.encuestas = [];
        this.respuestas = [];
        this.filtros = {};
        this.vistaActual = 'lista';
        this.encuestaActual = null;
        
        this.init();
    }
    
    async init() {
        await this.loadUser();
        this.setupEventListeners();
        await this.loadEncuestas();
        this.updateStats();
        this.renderEncuestas();
    }
    
    // === AUTENTICACIÓN ===
    async loadUser() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = '/login.html';
                return;
            }
            
            const response = await fetch('/api/auth/me/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                this.currentUser = await response.json();
            } else {
                window.location.href = '/login.html';
            }
        } catch (error) {
            console.error('Error loading user:', error);
            window.location.href = '/login.html';
        }
    }
    
    // === EVENT LISTENERS ===
    setupEventListeners() {
        // Filters
        document.getElementById('btnFiltrar')?.addEventListener('click', () => {
            this.aplicarFiltros();
        });
        
        document.getElementById('btnLimpiarFiltros')?.addEventListener('click', () => {
            this.limpiarFiltros();
        });
        
        // View toggle
        document.getElementById('btnVistaLista')?.addEventListener('click', () => {
            this.cambiarVista('lista');
        });
        
        document.getElementById('btnVistaGrid')?.addEventListener('click', () => {
            this.cambiarVista('grid');
        });
        
        // Create poll
        document.getElementById('btnCrearEncuesta')?.addEventListener('click', () => {
            this.showModal('modalCrearEncuesta');
        });
        
        // Modal events
        this.setupModalEvents();
    }
    
    setupModalEvents() {
        // Close modals
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });
        
        // Close on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        });
        
        // Form submissions
        document.getElementById('formCrearEncuesta')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.crearEncuesta();
        });
        
        document.getElementById('formResponderEncuesta')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.enviarRespuestas();
        });
    }
    
    // === CARGA DE DATOS ===
    async loadEncuestas() {
        try {
            this.showLoading(true);
            
            const token = localStorage.getItem('access_token');
            const params = new URLSearchParams(this.filtros);
            
            const response = await fetch(`/api/polls/?${params}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                this.encuestas = await response.json();
                this.renderEncuestas();
            } else {
                this.showError('Error cargando encuestas');
            }
        } catch (error) {
            console.error('Error loading encuestas:', error);
            this.showError('Error de conexión');
        } finally {
            this.showLoading(false);
        }
    }
    
    async loadRespuestas(encuestaId) {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/polls/${encuestaId}/respuestas/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error loading respuestas:', error);
        }
        return [];
    }
    
    // === RENDERIZADO ===
    renderEncuestas() {
        const container = document.getElementById('encuestasList');
        const noResults = document.getElementById('noResults');
        
        if (!container) return;
        
        if (this.encuestas.length === 0) {
            container.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }
        
        noResults.style.display = 'none';
        
        const viewClass = this.vistaActual === 'grid' ? 'grid-view' : '';
        container.className = `encuestas-list ${viewClass}`;
        
        container.innerHTML = this.encuestas.map(encuesta => this.renderEncuesta(encuesta)).join('');
        
        // Add event listeners
        container.querySelectorAll('.btn-responder').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.responderEncuesta(id);
            });
        });
        
        container.querySelectorAll('.btn-resultados').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.verResultados(id);
            });
        });
        
        container.querySelectorAll('.btn-editar').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.editarEncuesta(id);
            });
        });
    }
    
    renderEncuesta(encuesta) {
        const estado = this.getEstadoEncuesta(encuesta);
        const porcentajeParticipacion = this.calcularPorcentajeParticipacion(encuesta);
        const puedeResponder = this.puedeResponder(encuesta);
        const yaRespondio = this.yaRespondio(encuesta);
        
        return `
            <div class="encuesta-card">
                <div class="encuesta-header">
                    <h3 class="encuesta-titulo">${encuesta.titulo}</h3>
                    <span class="encuesta-estado ${estado}">${estado}</span>
                </div>
                
                <div class="encuesta-descripcion">
                    ${encuesta.descripcion}
                </div>
                
                <div class="encuesta-meta">
                    <span><i class="fas fa-tag"></i> ${encuesta.categoria}</span>
                    <span><i class="fas fa-calendar"></i> ${this.formatDate(encuesta.fecha_inicio)}</span>
                    <span><i class="fas fa-clock"></i> ${this.formatDate(encuesta.fecha_fin)}</span>
                    <span><i class="fas fa-users"></i> ${encuesta.total_respuestas || 0} respuestas</span>
                </div>
                
                <div class="encuesta-progress">
                    <div class="progress-label">
                        <span>Participación</span>
                        <span>${porcentajeParticipacion}%</span>
                    </div>
                    <div class="progress-bar-custom">
                        <div class="progress-fill" style="width: ${porcentajeParticipacion}%"></div>
                    </div>
                </div>
                
                <div class="encuesta-actions">
                    ${puedeResponder && !yaRespondio ? `
                        <button class="students-btn students-btn-primary btn-responder" data-id="${encuesta.id}">
                            <i class="fas fa-edit"></i> Responder
                        </button>
                    ` : ''}
                    
                    ${yaRespondio ? `
                        <button class="students-btn students-btn-success" disabled>
                            <i class="fas fa-check"></i> Ya Respondida
                        </button>
                    ` : ''}
                    
                    <button class="students-btn students-btn-outline btn-resultados" data-id="${encuesta.id}">
                        <i class="fas fa-chart-bar"></i> Ver Resultados
                    </button>
                    
                    ${this.puedeEditar(encuesta) ? `
                        <button class="students-btn students-btn-outline btn-editar" data-id="${encuesta.id}">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    // === FILTROS ===
    aplicarFiltros() {
        this.filtros = {};
        
        const estado = document.getElementById('filtroEstado')?.value;
        const categoria = document.getElementById('filtroCategoria')?.value;
        const busqueda = document.getElementById('busqueda')?.value;
        
        if (estado) this.filtros.estado = estado;
        if (categoria) this.filtros.categoria = categoria;
        if (busqueda) this.filtros.search = busqueda;
        
        this.loadEncuestas();
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    limpiarFiltros() {
        document.getElementById('filtroEstado').value = '';
        document.getElementById('filtroCategoria').value = '';
        document.getElementById('busqueda').value = '';
        
        this.filtros = {};
        this.loadEncuestas();
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    // === VISTAS ===
    cambiarVista(vista) {
        this.vistaActual = vista;
        
        document.getElementById('btnVistaLista').classList.toggle('active', vista === 'lista');
        document.getElementById('btnVistaGrid').classList.toggle('active', vista === 'grid');
        
        this.renderEncuestas();
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    // === ENCUESTAS ===
    async crearEncuesta() {
        try {
            const formData = {
                titulo: document.getElementById('inputTitulo').value,
                descripcion: document.getElementById('inputDescripcion').value,
                categoria: document.getElementById('inputCategoria').value,
                tipo: document.getElementById('inputTipo').value,
                fecha_inicio: document.getElementById('inputFechaInicio').value,
                fecha_fin: document.getElementById('inputFechaFin').value,
                preguntas: document.getElementById('inputPreguntas').value.split('\n').filter(p => p.trim()),
                anonima: document.getElementById('inputAnonima').checked,
                obligatoria: document.getElementById('inputObligatoria').checked
            };
            
            const token = localStorage.getItem('access_token');
            const response = await fetch('/api/polls/encuestas/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                this.showSuccess('Encuesta creada exitosamente');
                this.closeModal();
                document.getElementById('formCrearEncuesta').reset();
                this.loadEncuestas();
            } else {
                const error = await response.json();
                this.showError(error.detail || 'Error creando encuesta');
            }
        } catch (error) {
            console.error('Error creating encuesta:', error);
            this.showError('Error de conexión');
        }
    }
    
    async responderEncuesta(id) {
        const encuesta = this.encuestas.find(e => e.id === id);
        if (!encuesta) return;
        
        this.encuestaActual = encuesta;
        this.renderPreguntas(encuesta);
        this.showModal('modalResponderEncuesta');
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    renderPreguntas(encuesta) {
        const container = document.getElementById('encuestaPreguntas');
        document.getElementById('modalEncuestaTitulo').textContent = encuesta.titulo;
        
        container.innerHTML = encuesta.preguntas.map((pregunta, index) => `
            <div class="question-item">
                <div class="question-text">${index + 1}. ${pregunta}</div>
                <div class="question-options">
                    ${this.renderOpcionesPregunta(index)}
                </div>
            </div>
        `).join('');
    }
    
    renderOpcionesPregunta(index) {
        const opciones = [
            'Muy de acuerdo',
            'De acuerdo',
            'Neutral',
            'En desacuerdo',
            'Muy en desacuerdo'
        ];
        
        return opciones.map(opcion => `
            <div class="option-item">
                <input type="radio" name="pregunta_${index}" value="${opcion}" id="pregunta_${index}_${opcion}" required>
                <label for="pregunta_${index}_${opcion}">${opcion}</label>
            </div>
        `).join('');
    }
    
    async enviarRespuestas() {
        try {
            const formData = new FormData(document.getElementById('formResponderEncuesta'));
            const respuestas = [];
            
            for (let i = 0; i < this.encuestaActual.preguntas.length; i++) {
                const respuesta = formData.get(`pregunta_${i}`);
                if (respuesta) {
                    respuestas.push({
                        pregunta: this.encuestaActual.preguntas[i],
                        respuesta: respuesta
                    });
                }
            }
            
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/polls/${this.encuestaActual.id}/votar/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ respuestas })
            });
            
            if (response.ok) {
                this.showSuccess('Respuestas enviadas exitosamente');
                this.closeModal();
                this.loadEncuestas();
            } else {
                const error = await response.json();
                this.showError(error.detail || 'Error enviando respuestas');
            }
        } catch (error) {
            console.error('Error sending respuestas:', error);
            this.showError('Error de conexión');
        }
    }
    
    async verResultados(id) {
        const encuesta = this.encuestas.find(e => e.id === id);
        if (!encuesta) return;
        
        try {
            const respuestas = await this.loadRespuestas(id);
            this.renderResultados(encuesta, respuestas);
            this.showModal('modalVerResultados');
        } catch (error) {
            console.error('Error loading resultados:', error);
            this.showError('Error cargando resultados');
        }
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    renderResultados(encuesta, respuestas) {
        document.getElementById('modalResultadosTitulo').textContent = `Resultados: ${encuesta.titulo}`;
        
        const container = document.getElementById('encuestaResultados');
        
        if (respuestas.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-chart-bar fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No hay respuestas aún</h4>
                    <p class="text-muted">Las respuestas aparecerán aquí cuando los usuarios participen</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = encuesta.preguntas.map((pregunta, index) => {
            const respuestasPregunta = respuestas.map(r => r.respuestas[index]).filter(r => r);
            const conteo = this.contarRespuestas(respuestasPregunta);
            
            return `
                <div class="results-section">
                    <h3>${index + 1}. ${pregunta}</h3>
                    <div class="result-options">
                        ${Object.entries(conteo).map(([opcion, count]) => {
                            const porcentaje = ((count / respuestasPregunta.length) * 100).toFixed(1);
                            return `
                                <div class="result-option">
                                    <span class="result-option-text">${opcion}</span>
                                    <div>
                                        <span class="result-option-count">${count}</span>
                                        <span class="result-option-percentage">(${porcentaje}%)</span>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }).join('');
    }
    
    contarRespuestas(respuestas) {
        const conteo = {};
        respuestas.forEach(respuesta => {
            conteo[respuesta.respuesta] = (conteo[respuesta.respuesta] || 0) + 1;
        });
        return conteo;
    }
    
    // === MODALES ===
    showModal(modalId) {
        document.getElementById(modalId).classList.add('show');
    }
    
    closeModal() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
    }
    
    // === ESTADÍSTICAS ===
    updateStats() {
        const total = this.encuestas.length;
        const completadas = this.encuestas.filter(e => this.yaRespondio(e)).length;
        const pendientes = total - completadas;
        const participacion = total > 0 ? Math.round((completadas / total) * 100) : 0;
        
        document.getElementById('totalEncuestas').textContent = total;
        document.getElementById('encuestasCompletadas').textContent = completadas;
        document.getElementById('encuestasPendientes').textContent = pendientes;
        document.getElementById('porcentajeParticipacion').textContent = `${participacion}%`;
    }
    
    // === UTILIDADES ===
    getEstadoEncuesta(encuesta) {
        const ahora = new Date();
        const inicio = new Date(encuesta.fecha_inicio);
        const fin = new Date(encuesta.fecha_fin);
        
        if (ahora < inicio) return 'programada';
        if (ahora > fin) return 'cerrada';
        return 'activa';
    }
    
    calcularPorcentajeParticipacion(encuesta) {
        // Simular porcentaje basado en respuestas
        const total = 100; // Total de usuarios
        const respuestas = encuesta.total_respuestas || 0;
        return Math.round((respuestas / total) * 100);
    }
    
    puedeResponder(encuesta) {
        const estado = this.getEstadoEncuesta(encuesta);
        return estado === 'activa';
    }
    
    yaRespondio(encuesta) {
        // Simular verificación de respuesta
        return Math.random() > 0.7; // 30% de probabilidad de haber respondido
    }
    
    puedeEditar(encuesta) {
        return this.currentUser && 
               (this.currentUser.role === 'admin' || 
                this.currentUser.role === 'moderator' ||
                encuesta.creador_id === this.currentUser.id);
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
    
    showLoading(show) {
        // Implementar loading spinner si es necesario
    }
    
    showSuccess(message) {
        this.showToast(message, 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    showError(message) {
        this.showToast(message, 'error');
        
        if (window.playSound) {
            window.playSound('error');
        }
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}

// Initialize encuestas manager
let encuestasManager;
document.addEventListener('DOMContentLoaded', () => {
    encuestasManager = new EncuestasManager();
    
    // Play page load sound
    if (window.playSound) {
        window.playSound('pageLoad');
    }
});