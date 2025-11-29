/**
 * Módulo de Encuestas - StudentsPoint
 * Sistema simple de encuestas con votación única
 */

class EncuestasManager {
    constructor() {
        this.currentUser = null;
        this.encuestas = [];
        this.imagenSeleccionada = null;
        this.modalCrear = null;
        this.currentEncuestaId = null;
        
        this.init();
    }
    
    async init() {
        await this.loadUser();
        this.setupEventListeners();
        await this.cargarEncuestas();
        
        // Inicializar modal
        this.modalCrear = new bootstrap.Modal(document.getElementById('modalCrearEncuesta'));
    }
    
    async loadUser() {
        try {
            if (!window.authAPI || !window.authAPI.isAuthenticated()) {
                window.location.href = '/login.html';
                return;
            }
            
            this.currentUser = await window.authAPI.getCurrentUser();
            
            // Actualizar UI
            const sidebarName = document.getElementById('sidebarUserName');
            const sidebarRole = document.getElementById('sidebarUserRole');
            if (sidebarName && this.currentUser) {
                sidebarName.textContent = this.currentUser.name || this.currentUser.email;
            }
            if (sidebarRole && this.currentUser) {
                sidebarRole.textContent = this.currentUser.career || 'Estudiante';
            }
        } catch (error) {
            console.error('Error loading user:', error);
            window.location.href = '/login.html';
        }
    }
    
    setupEventListeners() {
        // Preview de imagen
        document.getElementById('imagenEncuesta')?.addEventListener('change', (e) => {
            this.previewImagen(e.target.files[0]);
        });
        
        // Delegación de eventos para elementos dinámicos (encuestas renderizadas)
        const container = document.getElementById('encuestas-container');
        if (container && !container.hasAttribute('data-listeners-attached')) {
            container.setAttribute('data-listeners-attached', 'true');
            
            container.addEventListener('click', (e) => {
                // Botones de votar
                const btnVotar = e.target.closest('.btn-votar');
                if (btnVotar && btnVotar.id) {
                    const encuestaId = parseInt(btnVotar.id.replace('btn-votar-', ''));
                    if (!isNaN(encuestaId)) {
                        this.votar(encuestaId);
                        return;
                    }
                }
                
                // Opciones de voto
                const opcionVoto = e.target.closest('.opcion-voto');
                if (opcionVoto && !opcionVoto.classList.contains('voted') && opcionVoto.dataset.encuesta) {
                    const encuestaId = parseInt(opcionVoto.dataset.encuesta);
                    const opcionId = parseInt(opcionVoto.dataset.opcion);
                    if (!isNaN(encuestaId) && !isNaN(opcionId)) {
                        const encuesta = this.encuestas.find(e => e.id === encuestaId);
                        if (encuesta) {
                            this.seleccionarOpcion(encuestaId, opcionId, encuesta.multi || encuesta.permitirMultiple);
                        }
                        return;
                    }
                }
                
                // Botones de eliminar
                const btnEliminar = e.target.closest('[id^="btn-eliminar-"]');
                if (btnEliminar && btnEliminar.id) {
                    const encuestaId = parseInt(btnEliminar.id.replace('btn-eliminar-', ''));
                    if (!isNaN(encuestaId)) {
                        this.eliminarEncuesta(encuestaId);
                        return;
                    }
                }
            });
        }
        
        // Reproducir sonido de carga
        if (window.playSound) {
            window.playSound('pageLoad');
        }
    }
    
    // ==================== CREAR ENCUESTA ====================
    
    previewImagen(file) {
        if (!file) return;
        
        // Validar tamaño (5MB máx)
        if (file.size > 5 * 1024 * 1024) {
            alert('La imagen es muy grande. Máximo 5MB.');
            return;
        }
        
        // Validar tipo
        if (!file.type.startsWith('image/')) {
            alert('Por favor selecciona una imagen válida.');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagenSeleccionada = e.target.result;
            
            // Mostrar preview
            const preview = document.getElementById('imagenPreview');
            const placeholder = document.querySelector('.upload-placeholder');
            const removeBtn = document.querySelector('.remove-image');
            
            preview.src = this.imagenSeleccionada;
            preview.classList.remove('d-none');
            placeholder.classList.add('d-none');
            removeBtn.classList.remove('d-none');
        };
        
        reader.readAsDataURL(file);
    }
    
    agregarOpcion() {
        const container = document.getElementById('opcionesContainer');
        const opcionesActuales = container.querySelectorAll('.opcion-item');
        const numero = opcionesActuales.length + 1;
        
        const div = document.createElement('div');
        div.className = 'input-group mb-2 opcion-item';
        div.innerHTML = `
            <span class="input-group-text"><i class="fas fa-grip-vertical"></i></span>
            <input type="text" class="form-control opcion-input" placeholder="Opción ${numero}" required>
            <button class="btn btn-outline-danger" type="button" onclick="encuestasManager.eliminarOpcion(this)">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        container.appendChild(div);
        
        // Habilitar botones de eliminar si hay más de 2
        if (opcionesActuales.length >= 2) {
            container.querySelectorAll('.btn-outline-danger').forEach(btn => {
                btn.disabled = false;
            });
        }
    }
    
    eliminarOpcion(button) {
        const container = document.getElementById('opcionesContainer');
        const opcionesActuales = container.querySelectorAll('.opcion-item');
        
        if (opcionesActuales.length <= 2) {
            alert('Debe haber al menos 2 opciones');
            return;
        }
        
        button.closest('.opcion-item').remove();
        
        // Deshabilitar botones de eliminar si quedan exactamente 2
        if (container.querySelectorAll('.opcion-item').length === 2) {
            container.querySelectorAll('.btn-outline-danger').forEach(btn => {
                btn.disabled = true;
            });
        }
    }
    
    async crearEncuesta() {
        const titulo = document.getElementById('tituloEncuesta').value.trim();
        const descripcion = document.getElementById('descripcionEncuesta').value.trim();
        const permitirMultiple = document.getElementById('permitirMultiple').checked;
        const mostrarResultados = document.getElementById('mostrarResultados').checked;
        
        // Validar título
        if (!titulo) {
            this.showToast('Por favor ingresa un título para la encuesta', 'warning');
            return;
        }
        
        // Obtener opciones
        const opcionesInputs = document.querySelectorAll('.opcion-input');
        const opciones = Array.from(opcionesInputs)
            .map(input => input.value.trim())
            .filter(val => val !== '');
        
        if (opciones.length < 2) {
            this.showToast('Debes agregar al menos 2 opciones', 'warning');
            return;
        }
        
        try {
            // Intentar guardar en BD si hay API disponible
            if (window.pollsAPI) {
                try {
                    const pollData = {
                        titulo: titulo,
                        descripcion: descripcion,
                        multi: permitirMultiple,
                        mostrar_resultados: mostrarResultados ? 'tiempo_real' : 'al_cierre',
                        opciones: opciones.map((texto, index) => ({
                            texto: texto,
                            orden: index
                        }))
                    };
                    
                    await window.pollsAPI.createPoll(pollData);
                    this.showToast('Encuesta creada exitosamente en el servidor', 'success');
                } catch (error) {
                    console.warn('Error guardando en BD, usando localStorage:', error);
                    // Continuar con localStorage
                }
            }
            
            // Guardar imagen antes de limpiar
            const imagenGuardada = this.imagenSeleccionada;
            
            // Guardar también en localStorage
            const nuevaEncuesta = {
                id: Date.now(),
                titulo: titulo,
                descripcion: descripcion,
                imagen: imagenGuardada || null,
                opciones: opciones.map((texto, index) => ({
                    id: index,
                    texto: texto,
                    votos: 0
                })),
                permitirMultiple: permitirMultiple,
                mostrarResultados: mostrarResultados,
                autor: {
                    id: this.currentUser.id,
                    nombre: this.currentUser.name || this.currentUser.email
                },
                fechaCreacion: new Date().toISOString(),
                votantes: []
            };
            
            this.encuestas.push(nuevaEncuesta);
            this.guardarEncuestas();
            
            // Cerrar modal y limpiar
            this.modalCrear.hide();
            this.limpiarFormulario();
            
            // Recargar encuestas
            await this.cargarEncuestas();
            
            this.showToast('Encuesta creada exitosamente', 'success');
            
            if (window.playSound) {
                window.playSound('success');
            }
        } catch (error) {
            console.error('Error creando encuesta:', error);
            this.showToast('Error al crear la encuesta: ' + (error.message || 'Error desconocido'), 'error');
        }
    }
    
    limpiarFormulario() {
        document.getElementById('formCrearEncuesta').reset();
        this.removerImagen();
        
        // Resetear opciones
        const container = document.getElementById('opcionesContainer');
        container.innerHTML = `
            <div class="input-group mb-2 opcion-item">
                <span class="input-group-text"><i class="fas fa-grip-vertical"></i></span>
                <input type="text" class="form-control opcion-input" placeholder="Opción 1" required>
                <button class="btn btn-outline-danger" type="button" onclick="encuestasManager.eliminarOpcion(this)" disabled>
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="input-group mb-2 opcion-item">
                <span class="input-group-text"><i class="fas fa-grip-vertical"></i></span>
                <input type="text" class="form-control opcion-input" placeholder="Opción 2" required>
                <button class="btn btn-outline-danger" type="button" onclick="encuestasManager.eliminarOpcion(this)" disabled>
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    }
    
    removerImagen() {
        this.imagenSeleccionada = null;
        const preview = document.getElementById('imagenPreview');
        const placeholder = document.querySelector('.upload-placeholder');
        const removeBtn = document.querySelector('.remove-image');
        const input = document.getElementById('imagenEncuesta');
        
        if (preview) {
            preview.src = '';
            preview.classList.add('d-none');
        }
        if (placeholder) placeholder.classList.remove('d-none');
        if (removeBtn) removeBtn.classList.add('d-none');
        if (input) input.value = '';
    }
    
    // ==================== CARGAR Y MOSTRAR ENCUESTAS ====================
    
    async cargarEncuestas() {
        try {
            // Intentar cargar desde BD primero
            if (window.pollsAPI) {
                try {
                    const encuestasBD = await window.pollsAPI.getPolls();
                    if (Array.isArray(encuestasBD) && encuestasBD.length > 0) {
                        // Cargar detalles completos
                        this.encuestas = await Promise.all(
                            encuestasBD.map(async (encuesta) => {
                                try {
                                    const detalle = await window.pollsAPI.getPoll(encuesta.id);
                                    return this.adaptarEncuestaAPI(detalle);
                                } catch (error) {
                                    return this.adaptarEncuestaAPI(encuesta);
                                }
                            })
                        );
                        this.renderizarEncuestas();
                        return;
                    }
                } catch (error) {
                    console.warn('Error cargando desde BD, usando localStorage:', error);
                }
            }
            
            // Fallback a localStorage
            const encuestasGuardadas = localStorage.getItem('studentspoint_encuestas');
            this.encuestas = encuestasGuardadas ? JSON.parse(encuestasGuardadas) : [];
            this.renderizarEncuestas();
        } catch (error) {
            console.error('Error al cargar encuestas:', error);
            this.showToast('Error al cargar las encuestas', 'error');
            this.encuestas = [];
            this.renderizarEncuestas();
        }
    }
    
    adaptarEncuestaAPI(encuesta) {
        // Adaptar estructura de API a formato esperado
        const opciones = encuesta.opciones || [];
        const creadorId = encuesta.creador || (typeof encuesta.creador === 'object' && encuesta.creador ? encuesta.creador.id : null);
        const creadorNombre = encuesta.creador_nombre || 
                             (typeof encuesta.creador === 'object' && encuesta.creador ? encuesta.creador.name : null) ||
                             'Usuario';
        
        return {
            id: encuesta.id,
            titulo: encuesta.titulo || '',
            descripcion: encuesta.descripcion || '',
            opciones: opciones.map(op => ({
                id: op.id,
                texto: op.texto || '',
                votos: op.votos || 0,
                porcentaje: 0
            })),
            multi: encuesta.multi || false,
            mostrarResultados: encuesta.mostrar_resultados === 'tiempo_real' || encuesta.mostrar_resultados === true,
            total_votos: encuesta.total_votos || 0,
            puede_votar: encuesta.puede_votar !== false,
            esta_activa: encuesta.estado === 'activa' || encuesta.estado === 'ACTIVA',
            autor: {
                id: creadorId,
                nombre: creadorNombre
            },
            fechaCreacion: encuesta.created_at || new Date().toISOString(),
            yaVoto: encuesta.ya_voto || false
        };
    }
    
    guardarEncuestas() {
        localStorage.setItem('studentspoint_encuestas', JSON.stringify(this.encuestas));
    }
    
    renderizarEncuestas() {
        const container = document.getElementById('encuestas-container');
        if (!container) return;
        
        if (this.encuestas.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <i class="fas fa-poll-h fa-4x mb-3"></i>
                        <h3>No hay encuestas disponibles</h3>
                        <p>Crea la primera encuesta para comenzar</p>
                    </div>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.encuestas.map(encuesta => this.renderizarTarjetaEncuesta(encuesta)).join('');
        
        // Los event listeners se manejan con delegación de eventos en setupEventListeners
    }
    
    renderizarTarjetaEncuesta(encuesta) {
        const yaVoto = (encuesta.votantes && this.currentUser && encuesta.votantes.includes(this.currentUser.id)) || 
                      encuesta.yaVoto || 
                      (encuesta.puede_votar === false) || 
                      (encuesta.esta_activa === false);
        const totalVotos = encuesta.total_votos || encuesta.opciones.reduce((sum, op) => sum + (op.votos || 0), 0);
        const esAutor = encuesta.autor && this.currentUser && encuesta.autor.id === this.currentUser.id;
        
        // Calcular porcentajes si ya votó
        if (yaVoto && encuesta.mostrarResultados) {
            encuesta.opciones.forEach(op => {
                op.porcentaje = totalVotos > 0 ? Math.round((op.votos / totalVotos) * 100) : 0;
            });
        }
        
        return `
            <div class="col-12 col-md-6 col-lg-4">
                <div class="encuesta-card">
                    ${encuesta.imagen ? `
                        <div class="encuesta-image-container">
                            <img src="${encuesta.imagen}" alt="${this.escapeHtml(encuesta.titulo)}" class="encuesta-image">
                        </div>
                    ` : ''}
                    <div class="encuesta-card-body">
                        <h3 class="encuesta-title">${this.escapeHtml(encuesta.titulo)}</h3>
                        ${encuesta.descripcion ? `<p class="encuesta-description">${this.escapeHtml(encuesta.descripcion)}</p>` : ''}
                        
                        <div class="encuesta-meta">
                            <div class="encuesta-meta-item">
                                <i class="fas fa-user"></i>
                                <span>${this.escapeHtml(encuesta.autor ? encuesta.autor.nombre : 'Usuario')}</span>
                            </div>
                            <div class="encuesta-meta-item">
                                <i class="fas fa-calendar"></i>
                                <span>${this.formatDate(encuesta.fechaCreacion)}</span>
                            </div>
                        </div>
                        
                        <div class="votacion-opciones">
                            ${this.renderizarOpciones(encuesta, yaVoto)}
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            ${!yaVoto ? `
                                <button class="btn btn-votar" id="btn-votar-${encuesta.id}">
                                    <i class="fas fa-check-circle me-2"></i>Confirmar Voto
                                </button>
                            ` : encuesta.mostrarResultados ? `
                                <div class="total-votos">
                                    <span class="total-votos-numero">${totalVotos}</span>
                                    <span class="total-votos-texto">votos totales</span>
                                </div>
                            ` : `
                                <div class="ya-votado-badge">
                                    <i class="fas fa-check-circle"></i>
                                    <span>Ya votaste</span>
                                </div>
                            `}
                        </div>
                        
                        ${esAutor ? `
                            <button class="btn btn-danger w-100 mt-2" id="btn-eliminar-${encuesta.id}">
                                <i class="fas fa-trash me-2"></i>Eliminar Encuesta
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    renderizarOpciones(encuesta, yaVoto) {
        return encuesta.opciones.map(opcion => {
            const opcionId = opcion.id;
            
            return `
                <div class="opcion-voto ${yaVoto ? 'voted' : ''}" 
                     data-encuesta="${encuesta.id}" 
                     data-opcion="${opcionId}">
                    ${!yaVoto ? `
                        <div class="opcion-voto-content">
                            ${(encuesta.multi || encuesta.permitirMultiple) ? `
                                <div class="checkbox-custom">
                                    <i class="fas fa-check" style="display: none;"></i>
                                </div>
                            ` : `
                                <div class="radio-custom"></div>
                            `}
                            <span class="opcion-voto-texto">${this.escapeHtml(opcion.texto)}</span>
                        </div>
                    ` : `
                        <div class="opcion-voto-content">
                            <span class="opcion-voto-texto">${this.escapeHtml(opcion.texto)}</span>
                            <span class="opcion-voto-porcentaje">${opcion.porcentaje || 0}%</span>
                            <span class="opcion-voto-votos">(${opcion.votos || 0} votos)</span>
                        </div>
                        <div class="opcion-voto-barra" style="width: ${opcion.porcentaje || 0}%"></div>
                    `}
                </div>
            `;
        }).join('');
    }
    
    // ==================== VOTACIÓN ====================
    
    seleccionarOpcion(encuestaId, opcionId, permitirMultiple) {
        const encuesta = this.encuestas.find(e => e.id === encuestaId);
        if (!encuesta || encuesta.yaVoto) return;
        
        const opcionElemento = document.querySelector(
            `.opcion-voto[data-encuesta="${encuestaId}"][data-opcion="${opcionId}"]`
        );
        
        if (!opcionElemento) return;
        
        if (!permitirMultiple) {
            // Radio: deseleccionar todas las demás
            document.querySelectorAll(`.opcion-voto[data-encuesta="${encuestaId}"]`).forEach(el => {
                el.classList.remove('selected');
            });
        }
        
        // Toggle selección
        opcionElemento.classList.toggle('selected');
        
        // Mostrar/ocultar check en checkbox
        const checkIcon = opcionElemento.querySelector('.checkbox-custom i');
        if (checkIcon) {
            checkIcon.style.display = opcionElemento.classList.contains('selected') ? 'block' : 'none';
        }
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    async votar(encuestaId) {
        const encuesta = this.encuestas.find(e => e.id === encuestaId);
        if (!encuesta) return;
        
        if (encuesta.yaVoto || (encuesta.votantes && encuesta.votantes.includes(this.currentUser.id))) {
            this.showToast('Ya votaste en esta encuesta', 'warning');
            return;
        }
        
        // Obtener opciones seleccionadas
        const opcionesSeleccionadas = Array.from(
            document.querySelectorAll(`.opcion-voto[data-encuesta="${encuestaId}"].selected`)
        ).map(el => parseInt(el.dataset.opcion));
        
        if (opcionesSeleccionadas.length === 0) {
            this.showToast('Por favor selecciona al menos una opción', 'warning');
            return;
        }
        
        try {
            // Intentar votar en BD si es una encuesta del servidor
            if (window.pollsAPI && encuesta.id < 1000000) {
                try {
                    await window.pollsAPI.votePoll(encuesta.id, {
                        opciones: opcionesSeleccionadas
                    });
                    this.showToast('¡Voto registrado exitosamente!', 'success');
                    await this.cargarEncuestas();
                    return;
                } catch (error) {
                    console.warn('Error votando en BD, usando localStorage:', error);
                }
            }
            
            // Fallback a localStorage
            opcionesSeleccionadas.forEach(opcionId => {
                const opcion = encuesta.opciones.find(o => o.id === opcionId);
                if (opcion) {
                    opcion.votos = (opcion.votos || 0) + 1;
                }
            });
            
            if (!encuesta.votantes) encuesta.votantes = [];
            encuesta.votantes.push(this.currentUser.id);
            this.guardarEncuestas();
            await this.cargarEncuestas();
            this.showToast('¡Voto registrado exitosamente!', 'success');
        } catch (error) {
            console.error('Error votando:', error);
            this.showToast('Error al votar: ' + (error.message || 'Error desconocido'), 'error');
        }
    }
    
    // ==================== ELIMINAR ENCUESTA ====================
    
    async eliminarEncuesta(encuestaId) {
        if (!confirm('¿Estás seguro de que quieres eliminar esta encuesta?')) {
            return;
        }
        
        try {
            // Intentar eliminar de BD si es una encuesta del servidor
            if (window.pollsAPI && encuestaId < 1000000) {
                try {
                    await window.pollsAPI.deletePoll(encuestaId);
                } catch (error) {
                    console.warn('Error eliminando de BD:', error);
                }
            }
            
            // Eliminar de localStorage
            this.encuestas = this.encuestas.filter(e => e.id !== encuestaId);
            this.guardarEncuestas();
            await this.cargarEncuestas();
            
            this.showToast('Encuesta eliminada', 'success');
            
            if (window.playSound) {
                window.playSound('success');
            }
        } catch (error) {
            console.error('Error eliminando encuesta:', error);
            this.showToast('Error al eliminar la encuesta: ' + (error.message || 'Error desconocido'), 'error');
        }
    }
    
    // ==================== UTILIDADES ====================
    
    showToast(message, type = 'info') {
        const colors = {
            success: '#20c997',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#0dcaf0'
        };
        
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type] || colors.info};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    formatDate(dateString) {
        if (!dateString) return 'Fecha desconocida';
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (seconds < 60) return 'Hace un momento';
        if (minutes < 60) return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
        if (hours < 24) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
        if (days < 7) return `Hace ${days} día${days > 1 ? 's' : ''}`;
        
        return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Funciones globales para compatibilidad con HTML
function mostrarModalCrear() {
    const modal = new bootstrap.Modal(document.getElementById('modalCrearEncuesta'));
    modal.show();
}

function crearEncuesta(e) {
    if (e) e.preventDefault();
    if (window.encuestasManager) {
        window.encuestasManager.crearEncuesta();
    }
}

function agregarOpcion() {
    if (window.encuestasManager) {
        window.encuestasManager.agregarOpcion();
    }
}

function eliminarOpcion(button) {
    if (window.encuestasManager) {
        window.encuestasManager.eliminarOpcion(button);
    }
}

function removerImagen() {
    if (window.encuestasManager) {
        window.encuestasManager.removerImagen();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.encuestasManager = new EncuestasManager();
});
