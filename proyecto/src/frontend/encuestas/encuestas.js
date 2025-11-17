class EncuestasManager {
    constructor() {
        this.currentUser = null;
        this.canManage = false;
        this.token = null;
        this.sedes = [];
        this.polls = [];
        this.pollCache = new Map();
        this.pollsContainer = document.getElementById('polls-container');
        this.pollModalElement = document.getElementById('pollModal');
        this.createPollModalElement = document.getElementById('createPollModal');
        this.pollModal = this.pollModalElement ? new bootstrap.Modal(this.pollModalElement) : null;
        this.createPollModal = this.createPollModalElement ? new bootstrap.Modal(this.createPollModalElement) : null;
        this.searchDebounce = this.debounce(() => this.loadPolls(), 400);
        this.init();
    }

    async init() {
        try {
            await this.ensureAuth();
            this.setupEventListeners();
            await this.loadSedes();
            this.resetCreateForm();
            await this.loadPolls();
        } catch (error) {
            console.error('Error inicializando encuestas:', error);
            this.showToast(error.message || 'No fue posible cargar las encuestas', 'error');
        }
    }

    async ensureAuth() {
        if (!window.authAPI || !window.authAPI.isAuthenticated()) {
            window.location.href = '/login.html';
            throw new Error('Usuario no autenticado');
        }

        this.currentUser = await window.authAPI.getCurrentUser();
        this.token = window.authAPI.getAuthToken();

        this.canManage = Boolean(
            this.currentUser &&
            ['moderator', 'director_carrera', 'admin_global'].includes(this.currentUser.role)
        );

        const createBtn = document.getElementById('create-btn');
        if (createBtn) {
            createBtn.style.display = this.canManage ? 'inline-block' : 'none';
        }
    }

    setupEventListeners() {
        const statusFilter = document.getElementById('filter-status');
        const campusFilter = document.getElementById('filter-campus');
        const searchInput = document.getElementById('search-polls');
        const form = document.getElementById('createPollForm');

        statusFilter?.addEventListener('change', () => this.loadPolls());
        campusFilter?.addEventListener('change', () => this.loadPolls());
        searchInput?.addEventListener('keyup', () => this.searchDebounce());

        if (form) {
            form.addEventListener('submit', (event) => {
                event.preventDefault();
                this.submitNewPoll();
            });
        }
    }

    debounce(fn, wait = 300) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => fn.apply(this, args), wait);
        };
    }

    async loadSedes() {
        try {
            const response = await fetch('/api/sedes/');
            if (!response.ok) {
                throw new Error('No se pudieron cargar las sedes');
            }
            this.sedes = await response.json();
        } catch (error) {
            console.warn('No fue posible obtener la lista de sedes:', error);
            this.sedes = [];
        } finally {
            this.populateCampusFilters();
            this.populateCreatePollCampuses();
        }
    }

    populateCampusFilters() {
        const filterSelect = document.getElementById('filter-campus');
        if (!filterSelect) {
            return;
        }

        const currentValue = filterSelect.value;
        filterSelect.innerHTML = '<option value="">Todas las sedes</option>';

        this.sedes.forEach((sede) => {
            const option = document.createElement('option');
            option.value = sede.slug;
            option.textContent = sede.nombre;
            filterSelect.appendChild(option);
        });

        if (currentValue) {
            filterSelect.value = currentValue;
        }
    }

    populateCreatePollCampuses() {
        const select = document.getElementById('poll-campuses');
        if (!select) return;

        select.innerHTML = '';
        this.sedes.forEach((sede) => {
            const option = document.createElement('option');
            option.value = sede.id;
            option.textContent = sede.nombre;
            select.appendChild(option);
        });
    }

    buildFilters() {
        const filters = {};
        const statusFilter = document.getElementById('filter-status');
        const searchInput = document.getElementById('search-polls');

        const estado = statusFilter?.value;
        const search = searchInput?.value?.trim();

        if (estado) {
            filters.estado = estado;
        }
        if (search) {
            filters.search = search;
        }

        return filters;
    }

    async loadPolls() {
        if (!this.pollsContainer) return;

        const filters = this.buildFilters();
        const campusFilter = document.getElementById('filter-campus')?.value || '';

        this.showLoading(true);

        try {
            if (!window.pollsAPI) {
                throw new Error('Servicio de encuestas no disponible');
            }

            let polls = await window.pollsAPI.getPolls(filters);
            if (!Array.isArray(polls)) {
                polls = polls?.results || [];
            }

            // Filtrar por campus si está seleccionado
            if (campusFilter) {
                const campus = this.sedes.find((sede) => sede.slug === campusFilter);
                if (campus) {
                    // Obtener detalles completos para filtrar por sedes
                    const detailedPolls = await Promise.all(
                        polls.map(async (poll) => {
                            try {
                                return await this.getPollDetail(poll.id);
                            } catch {
                                return poll; // Si falla, usar el poll básico
                            }
                        })
                    );

                    polls = detailedPolls.filter((poll) => {
                        if (!poll) return false;
                        const sedes = poll.sedes_nombres || [];
                        // Si no tiene sedes asignadas, está abierta para todos
                        if (sedes.length === 0) {
                            return true;
                        }
                        // Verificar si el campus está en la lista de sedes
                        return sedes.some((sedeNombre) => 
                            sedeNombre === campus.nombre || sedeNombre === campus.slug
                        );
                    });
                }
            }
            
            // Actualizar cache con los polls obtenidos
            polls.forEach((poll) => {
                const cached = this.pollCache.get(poll.id) || {};
                this.pollCache.set(poll.id, { ...cached, ...poll });
            });

            this.polls = polls;
            this.renderPolls();
        } catch (error) {
            console.error('Error cargando encuestas:', error);
            this.showLoading(false);
            if (this.pollsContainer) {
                this.pollsContainer.innerHTML = `
                    <div class="col-12 text-center py-5">
                        <i class="fas fa-triangle-exclamation fa-2x text-danger mb-3"></i>
                        <p class="text-danger mb-0">${this.escapeHtml(error.message || 'Error al cargar las encuestas')}</p>
                        <button class="btn btn-outline-primary mt-3" onclick="loadPolls()">
                            <i class="fas fa-redo me-2"></i>Reintentar
                        </button>
                    </div>
                `;
            }
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        if (!this.pollsContainer) return;

        if (show) {
            this.pollsContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="mt-3">Obteniendo encuestas disponibles...</p>
                </div>
            `;
        }
    }

    renderPolls() {
        if (!this.pollsContainer) return;

        if (!this.polls.length) {
            this.pollsContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-poll-h fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No encontramos encuestas</h4>
                    <p class="text-muted mb-0">Prueba ajustando los filtros o revisa más tarde.</p>
                </div>
            `;
            return;
        }

        const summary = this.buildSummary(this.polls);

        const cards = this.polls.map((poll) => this.renderPollCard(poll)).join('');

        this.pollsContainer.innerHTML = `
            <div class="col-12">
                <div class="alert alert-light border shadow-sm d-flex justify-content-between align-items-center">
                    <span>${summary}</span>
                    <span class="text-muted small">
                        Última actualización: ${this.formatDateTime(new Date().toISOString())}
                    </span>
                </div>
            </div>
            ${cards}
        `;

        this.attachCardEvents();
    }

    buildSummary(polls) {
        const total = polls.length;
        const activos = polls.filter((poll) => poll.estado === 'activa' || poll.esta_activa).length;
        const cerrados = polls.filter((poll) => poll.estado === 'cerrada').length;

        return `Se encontraron ${total} encuestas · Activas: ${activos} · Cerradas: ${cerrados}`;
    }

    renderPollCard(poll) {
        const detail = this.pollCache.get(poll.id) || poll;
        const estado = detail.estado || (detail.esta_activa ? 'activa' : 'programada');
        const estadoLabel = this.getEstadoLabel(estado);
        const estadoClass = this.getEstadoClass(estado);
        const puedeVotar = Boolean(detail.puede_votar);
        const totalVotos = detail.total_votos ?? 0;
        const inicia = detail.inicia_at ? this.formatDateTime(detail.inicia_at) : 'Inicio inmediato';
        const cierra = detail.cierra_at ? this.formatDateTime(detail.cierra_at) : 'Sin fecha de cierre';

        return `
            <div class="col-12 col-lg-6 mb-4" data-poll-id="${detail.id}">
                <div class="card h-100 shadow-sm border-0">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h5 class="card-title mb-1">${this.escapeHtml(detail.titulo || 'Encuesta sin título')}</h5>
                                <p class="card-text text-muted mb-3">${this.escapeHtml(detail.descripcion || 'Sin descripción')}</p>
                            </div>
                            <span class="badge bg-${estadoClass} text-uppercase">${estadoLabel}</span>
                        </div>

                        <ul class="list-unstyled text-muted small mb-4">
                            <li><i class="fas fa-user-edit me-2"></i>${detail.creador_nombre || 'Anónimo'}</li>
                            <li><i class="fas fa-play-circle me-2"></i>${inicia}</li>
                            <li><i class="fas fa-stopwatch me-2"></i>${cierra}</li>
                            <li><i class="fas fa-users me-2"></i>${totalVotos} voto(s)</li>
                        </ul>

                        <div class="mt-auto d-flex flex-wrap gap-2">
                            ${puedeVotar ? `
                                <button class="btn btn-primary btn-sm" data-action="vote" data-id="${detail.id}">
                                    <i class="fas fa-edit me-1"></i> Participar
                                </button>
                            ` : ''}
                            <button class="btn btn-outline-primary btn-sm" data-action="results" data-id="${detail.id}">
                                <i class="fas fa-chart-pie me-1"></i> Resultados
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" data-action="details" data-id="${detail.id}">
                                <i class="fas fa-info-circle me-1"></i> Detalles
                            </button>
                            ${this.canManage ? this.renderAdminButtons(detail) : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderAdminButtons(poll) {
        const buttons = [];
        if (poll.estado === 'activa' || poll.esta_activa) {
            buttons.push(`
                <button class="btn btn-outline-danger btn-sm" data-action="close" data-id="${poll.id}">
                    <i class="fas fa-ban me-1"></i> Cerrar
                </button>
            `);
        }
        return buttons.join('');
    }

    attachCardEvents() {
        this.pollsContainer.querySelectorAll('[data-action="vote"]').forEach((btn) => {
            btn.addEventListener('click', () => this.openPollModal(Number(btn.dataset.id), 'vote'));
        });
        this.pollsContainer.querySelectorAll('[data-action="results"]').forEach((btn) => {
            btn.addEventListener('click', () => this.openPollModal(Number(btn.dataset.id), 'results'));
        });
        this.pollsContainer.querySelectorAll('[data-action="details"]').forEach((btn) => {
            btn.addEventListener('click', () => this.openPollModal(Number(btn.dataset.id), 'details'));
        });
        this.pollsContainer.querySelectorAll('[data-action="close"]').forEach((btn) => {
            btn.addEventListener('click', () => this.closePoll(Number(btn.dataset.id)));
        });
    }

    async getPollDetail(id) {
        if (this.pollCache.has(id) && this.pollCache.get(id).opciones) {
            return this.pollCache.get(id);
        }

        if (!window.pollsAPI) {
            throw new Error('Servicio de encuestas no disponible');
        }

        const detail = await window.pollsAPI.getPoll(id);
        this.pollCache.set(id, detail);
        return detail;
    }

    async openPollModal(id, mode) {
        try {
            const poll = await this.getPollDetail(id);
            this.renderPollModal(poll, mode);
            this.pollModal?.show();
        } catch (error) {
            console.error('Error obteniendo encuesta:', error);
            this.showToast(error.message || 'No fue posible obtener la encuesta', 'error');
        }
    }

    renderPollModal(poll, mode) {
        const title = document.getElementById('pollModalTitle');
        const body = document.getElementById('pollModalBody');
        const footer = document.getElementById('pollModalFooter');

        if (!title || !body || !footer) return;

        title.textContent = poll.titulo || 'Encuesta';
        body.innerHTML = this.renderPollSummary(poll);
        footer.innerHTML = '';

        if (mode === 'vote') {
            if (!poll.puede_votar) {
                body.innerHTML += `
                    <div class="alert alert-info mt-3">
                        <i class="fas fa-info-circle me-2"></i>
                        Ya registraste tu voto o no tienes permisos para participar en esta encuesta.
                    </div>
                `;
                return;
            }
            body.innerHTML += this.renderVoteForm(poll);
            footer.innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                <button type="button" class="btn btn-primary" id="submitVoteBtn">
                    <i class="fas fa-paper-plane me-1"></i> Enviar voto
                </button>
            `;
            document.getElementById('submitVoteBtn')?.addEventListener('click', () => this.submitVote(poll));
        } else if (mode === 'results') {
            body.innerHTML += this.renderResults(poll);
            footer.innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            `;
        } else {
            body.innerHTML += this.renderResults(poll, true);
            footer.innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                ${poll.puede_votar ? `
                    <button type="button" class="btn btn-primary" id="voteFromDetailsBtn">
                        <i class="fas fa-check me-1"></i> Participar
                    </button>
                ` : ''}
            `;
            document.getElementById('voteFromDetailsBtn')?.addEventListener('click', () => {
                this.pollModal?.hide();
                this.openPollModal(poll.id, 'vote');
            });
        }
    }

    renderPollSummary(poll) {
        const estado = this.getEstadoLabel(poll.estado);
        const sedes = poll.sedes_nombres?.length ? poll.sedes_nombres.join(', ') : 'Todas las sedes';
        const carreras = poll.carreras?.length ? poll.carreras.join(', ') : 'Todas las carreras';
        const inicio = poll.inicia_at ? this.formatDateTime(poll.inicia_at) : 'Inicio inmediato';
        const cierre = poll.cierra_at ? this.formatDateTime(poll.cierra_at) : 'Sin fecha de cierre';

        return `
            <div class="mb-3">
                <h6 class="text-muted text-uppercase">Información general</h6>
                <ul class="list-unstyled small mb-0">
                    <li><strong>Estado:</strong> ${estado}</li>
                    <li><strong>Inicio:</strong> ${inicio}</li>
                    <li><strong>Cierre:</strong> ${cierre}</li>
                    <li><strong>Público objetivo:</strong> ${sedes}</li>
                    <li><strong>Carreras:</strong> ${carreras}</li>
                    <li><strong>Total de votos:</strong> ${poll.total_votos ?? 0}</li>
                </ul>
            </div>
        `;
    }

    renderVoteForm(poll) {
        const multiple = poll.multi;
        const inputType = multiple ? 'checkbox' : 'radio';

        const options = (poll.opciones || []).map((opcion) => `
            <div class="form-check mb-2">
                <input class="form-check-input" type="${inputType}" 
                    name="poll-option" id="option-${opcion.id}" value="${opcion.id}">
                <label class="form-check-label" for="option-${opcion.id}">
                    ${this.escapeHtml(opcion.texto)}
                </label>
            </div>
        `).join('');

        return `
            <div class="mt-3">
                <h6 class="text-muted text-uppercase">${multiple ? 'Selecciona una o más opciones' : 'Selecciona una opción'}</h6>
                <form id="pollVoteForm">
                    ${options}
                    ${poll.requiere_justificacion ? `
                        <div class="mt-3">
                            <label for="poll-justification" class="form-label">Justificación</label>
                            <textarea id="poll-justification" class="form-control" rows="3" placeholder="Describe brevemente tu elección"></textarea>
                        </div>
                    ` : ''}
                </form>
            </div>
        `;
    }

    renderResults(poll, compact = false) {
        if (!poll.puede_ver_resultados) {
            return `
                <div class="alert alert-warning mt-3">
                    <i class="fas fa-lock me-2"></i>
                    Los resultados estarán disponibles una vez que la encuesta finalice o si un moderador los habilita.
                </div>
            `;
        }

        const total = poll.total_votos || 0;
        if (!total) {
            return `
                <div class="alert alert-light mt-3">
                    <i class="fas fa-chart-line me-2"></i>
                    Aún no hay votos registrados en esta encuesta.
                </div>
            `;
        }

        const rows = (poll.opciones || []).map((opcion) => {
            const votos = opcion.votos ?? 0;
            const porcentaje = opcion.porcentaje ?? (total ? Math.round((votos / total) * 100) : 0);
            return `
                <div class="mb-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <strong>${this.escapeHtml(opcion.texto)}</strong>
                        <span class="text-muted">${votos} voto(s) · ${porcentaje}%</span>
                    </div>
                    <div class="progress" style="height: 8px;">
                        <div class="progress-bar bg-primary" role="progressbar" style="width: ${porcentaje}%"></div>
                    </div>
                </div>
            `;
        }).join('');

        const wrapperClass = compact ? 'mt-3' : 'mt-4';
        return `
            <div class="${wrapperClass}">
                <h6 class="text-muted text-uppercase mb-3">Resultados actuales</h6>
                ${rows}
            </div>
        `;
    }

    async submitVote(poll) {
        const form = document.getElementById('pollVoteForm');
        if (!form) return;

        const selected = Array.from(form.querySelectorAll('input[name="poll-option"]:checked')).map((input) => Number(input.value));
        if (!selected.length) {
            this.showToast('Selecciona al menos una opción para votar.', 'warning');
            return;
        }

        const payload = { opciones: selected };
        if (poll.requiere_justificacion) {
            const justification = document.getElementById('poll-justification')?.value.trim();
            if (!justification) {
                this.showToast('Debes agregar una justificación para tu voto.', 'warning');
                return;
            }
            payload.justificacion = justification;
        }

        try {
            await window.pollsAPI.votePoll(poll.id, payload);
            this.showToast('¡Tu voto fue registrado correctamente!', 'info');
            this.pollModal?.hide();
            await this.loadPolls();
        } catch (error) {
            console.error('Error enviando voto:', error);
            this.showToast(error.message || 'No fue posible registrar tu voto', 'error');
        }
    }

    async closePoll(id) {
        if (!this.canManage) {
            this.showToast('No tienes permisos para cerrar encuestas.', 'error');
            return;
        }

        const confirmed = window.confirm('¿Seguro que deseas cerrar esta encuesta? Esta acción no se puede revertir.');
        if (!confirmed) return;

        try {
            await window.pollsAPI.closePoll(id);
            this.showToast('La encuesta fue cerrada correctamente.', 'info');
            await this.loadPolls();
        } catch (error) {
            console.error('Error cerrando encuesta:', error);
            this.showToast(error.message || 'No fue posible cerrar la encuesta', 'error');
        }
    }

    showCreatePollModal() {
        if (!this.canManage) {
            this.showToast('Solo los moderadores pueden crear encuestas.', 'error');
            return;
        }
        this.resetCreateForm();
        this.createPollModal?.show();
    }

    resetCreateForm() {
        const form = document.getElementById('createPollForm');
        const optionsContainer = document.getElementById('poll-options');
        if (!form || !optionsContainer) return;

        form.reset();
        optionsContainer.innerHTML = '';
        this.addOptionField('Sí');
        this.addOptionField('No');
    }

    addOptionField(value = '') {
        const container = document.getElementById('poll-options');
        if (!container) return;

        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group mb-2';
        inputGroup.innerHTML = `
            <input type="text" class="form-control" placeholder="Opción" value="${this.escapeHtml(value)}" required>
            <button class="btn btn-outline-danger" type="button">
                <i class="fas fa-trash"></i>
            </button>
        `;

        inputGroup.querySelector('button')?.addEventListener('click', () => this.removeOptionField(inputGroup));
        container.appendChild(inputGroup);
    }

    removeOptionField(groupElement) {
        const container = document.getElementById('poll-options');
        if (!container) return;

        const inputs = container.querySelectorAll('.input-group');
        if (inputs.length <= 2) {
            this.showToast('Una encuesta necesita al menos dos opciones.', 'warning');
            return;
        }

        groupElement.remove();
    }

    async submitNewPoll() {
        if (!this.canManage) {
            this.showToast('No tienes permisos para crear encuestas.', 'error');
            return;
        }

        const titleInput = document.getElementById('poll-title');
        const descriptionInput = document.getElementById('poll-description');
        const startInput = document.getElementById('poll-start');
        const endInput = document.getElementById('poll-end');
        const multiCheckbox = document.getElementById('poll-multi');
        const anonymousCheckbox = document.getElementById('poll-anonymous');
        const justificationCheckbox = document.getElementById('poll-justification');
        const resultsCheckbox = document.getElementById('poll-results');
        const campusSelect = document.getElementById('poll-campuses');
        const optionsContainer = document.getElementById('poll-options');

        if (!titleInput || !optionsContainer) return;

        const title = titleInput.value.trim();
        if (!title) {
            this.showToast('Escribe un título para la encuesta.', 'warning');
            return;
        }

        const optionValues = Array.from(optionsContainer.querySelectorAll('input'))
            .map((input) => input.value.trim())
            .filter(Boolean);

        if (optionValues.length < 2) {
            this.showToast('Agrega al menos dos opciones de respuesta.', 'warning');
            return;
        }

        const selectedCampuses = Array.from(campusSelect?.selectedOptions || []).map((option) => Number(option.value));

        const payload = {
            titulo: title,
            descripcion: descriptionInput?.value || '',
            multi: Boolean(multiCheckbox?.checked),
            anonima: Boolean(anonymousCheckbox?.checked),
            requiere_justificacion: Boolean(justificationCheckbox?.checked),
            mostrar_resultados: resultsCheckbox?.checked ? 'tiempo_real' : 'solo_moderador',
            carreras: [],
            opciones: optionValues.map((texto, index) => ({
                texto,
                orden: index,
            })),
        };

        if (startInput?.value) {
            payload.inicia_at = startInput.value;
        }
        if (endInput?.value) {
            payload.cierra_at = endInput.value;
        }
        if (selectedCampuses.length) {
            payload.sedes_ids = selectedCampuses;
        }

        try {
            await window.pollsAPI.createPoll(payload);
            this.showToast('Encuesta creada correctamente.', 'info');
            this.createPollModal?.hide();
            await this.loadPolls();
        } catch (error) {
            console.error('Error creando encuesta:', error);
            this.showToast(error.message || 'No fue posible crear la encuesta', 'error');
        }
    }

    getEstadoLabel(estado) {
        const labels = {
            activa: 'Activa',
            cerrada: 'Cerrada',
            programada: 'Programada',
            borrador: 'Borrador',
            archivada: 'Archivada',
        };
        return labels[estado] || estado || 'Desconocido';
    }

    getEstadoClass(estado) {
        const mapping = {
            activa: 'success',
            cerrada: 'secondary',
            programada: 'info',
            borrador: 'warning',
            archivada: 'dark',
        };
        return mapping[estado] || 'primary';
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        if (Number.isNaN(date.getTime())) return 'Fecha no disponible';
        return date.toLocaleString('es-CL', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    }

    escapeHtml(text) {
        if (text === undefined || text === null) return '';
        const div = document.createElement('div');
        div.textContent = String(text);
        return div.innerHTML;
    }

    showToast(message, type = 'info') {
        const allowedTypes = ['info', 'warning', 'error'];
        const toastType = allowedTypes.includes(type) ? type : 'info';

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.classList.add(toastType);
        toast.innerHTML = `<div class="toast-content"><span>${message}</span></div>`;

        document.body.appendChild(toast);

        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 3000);
    }
}

let encuestasManager;

document.addEventListener('DOMContentLoaded', () => {
    encuestasManager = new EncuestasManager();

    window.loadPolls = () => encuestasManager.loadPolls();
    window.showCreatePoll = () => encuestasManager.showCreatePollModal();
    window.addOption = () => encuestasManager.addOptionField();
    window.removeOption = (button) => {
        if (button?.closest('.input-group')) {
            encuestasManager.removeOptionField(button.closest('.input-group'));
        }
    };
    window.createPoll = () => encuestasManager.submitNewPoll();
});
