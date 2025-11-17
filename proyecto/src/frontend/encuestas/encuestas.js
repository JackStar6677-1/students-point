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
        
        if (window.playSound) {
            window.playSound('click');
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
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    removerImagen() {
        this.imagenSeleccionada = null;
        
        const preview = document.getElementById('imagenPreview');
        const placeholder = document.querySelector('.upload-placeholder');
        const removeBtn = document.querySelector('.remove-image');
        const input = document.getElementById('imagenEncuesta');
        
        preview.classList.add('d-none');
        placeholder.classList.remove('d-none');
        removeBtn.classList.add('d-none');
        input.value = '';
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    async crearEncuesta() {
        const titulo = document.getElementById('tituloEncuesta').value.trim();
        const descripcion = document.getElementById('descripcionEncuesta').value.trim();
        const permitirMultiple = document.getElementById('permitirMultiple').checked;
        const mostrarResultados = document.getElementById('mostrarResultados').checked;
        
        // Validar título
        if (!titulo) {
            alert('Por favor ingresa un título para la encuesta');
            return;
        }
        
        // Obtener opciones
        const opcionesInputs = document.querySelectorAll('.opcion-input');
        const opciones = Array.from(opcionesInputs)
            .map(input => input.value.trim())
            .filter(val => val !== '');
        
        if (opciones.length < 2) {
            alert('Debes agregar al menos 2 opciones');
            return;
        }
        
        // Crear objeto de encuesta
        const encuesta = {
            id: Date.now(),
            titulo,
            descripcion,
            imagen: this.imagenSeleccionada || '/static/images/default-poll.jpg',
            opciones: opciones.map((texto, index) => ({
                id: index,
                texto,
                votos: 0
            })),
            permitirMultiple,
            mostrarResultados,
            autor: {
                id: this.currentUser.id,
                nombre: this.currentUser.name
            },
            fechaCreacion: new Date().toISOString(),
            votantes: [] // Array de IDs de usuarios que ya votaron
        };
        
        // Guardar en localStorage (simular backend)
        this.encuestas.push(encuesta);
        this.guardarEncuestas();
        
        // Cerrar modal y limpiar
        this.modalCrear.hide();
        this.limpiarFormulario();
        
        // Recargar encuestas
        await this.cargarEncuestas();
        
        // Notificación
        this.showToast('Encuesta creada exitosamente', 'success');
        
        if (window.playSound) {
            window.playSound('success');
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
    
    // ==================== CARGAR Y MOSTRAR ENCUESTAS ====================
    
    async cargarEncuestas() {
        try {
            // Cargar desde localStorage
            const encuestasGuardadas = localStorage.getItem('studentspoint_encuestas');
            this.encuestas = encuestasGuardadas ? JSON.parse(encuestasGuardadas) : [];
            
            this.renderizarEncuestas();
        } catch (error) {
            console.error('Error al cargar encuestas:', error);
            this.showToast('Error al cargar las encuestas', 'error');
        }
    }
    
    renderizarEncuestas() {
        const container = document.getElementById('encuestas-container');
        
        if (this.encuestas.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <i class="fas fa-poll-h"></i>
                        <h3>No hay encuestas aún</h3>
                        <p>Sé el primero en crear una encuesta para la comunidad</p>
                        <button class="btn btn-primary mt-3" onclick="encuestasManager.mostrarModalCrear()">
                            <i class="fas fa-plus-circle me-2"></i>Crear Primera Encuesta
                        </button>
                    </div>
                </div>
            `;
            return;
        }
        
        // Ordenar por fecha más reciente
        const encuestasOrdenadas = [...this.encuestas].sort((a, b) => 
            new Date(b.fechaCreacion) - new Date(a.fechaCreacion)
        );
        
        container.innerHTML = encuestasOrdenadas.map(encuesta => 
            this.renderizarTarjetaEncuesta(encuesta)
        ).join('');
    }
    
    renderizarTarjetaEncuesta(encuesta) {
        const yaVoto = encuesta.votantes.includes(this.currentUser.id);
        const totalVotos = encuesta.opciones.reduce((sum, op) => sum + op.votos, 0);
        const esAutor = encuesta.autor.id === this.currentUser.id;
        
        return `
            <div class="col-12 col-md-6 col-lg-4">
                <div class="encuesta-card">
                    ${encuesta.imagen ? `
                        <img src="${encuesta.imagen}" alt="${encuesta.titulo}" class="encuesta-card-image">
                    ` : ''}
                    
                    <div class="encuesta-card-body">
                        <h3 class="encuesta-title">${encuesta.titulo}</h3>
                        
                        ${encuesta.descripcion ? `
                            <p class="encuesta-description">${encuesta.descripcion}</p>
                        ` : ''}
                        
                        <div class="encuesta-meta">
                            <div class="encuesta-meta-item">
                                <i class="fas fa-user"></i>
                                <span>${encuesta.autor.nombre}</span>
                            </div>
                            <div class="encuesta-meta-item">
                                <i class="fas fa-calendar"></i>
                                <span>${this.formatearFecha(encuesta.fechaCreacion)}</span>
                            </div>
                            <div class="encuesta-meta-item">
                                <i class="fas fa-vote-yea"></i>
                                <span>${totalVotos} voto${totalVotos !== 1 ? 's' : ''}</span>
                            </div>
                        </div>
                        
                        ${yaVoto ? `
                            <div class="ya-votado-badge">
                                <i class="fas fa-check-circle"></i>
                                <span>Ya votaste</span>
                            </div>
                        ` : ''}
                        
                        ${this.renderizarOpciones(encuesta, yaVoto)}
                        
                        ${!yaVoto ? `
                            <button class="btn btn-votar" onclick="encuestasManager.votar(${encuesta.id})" id="btn-votar-${encuesta.id}">
                                <i class="fas fa-check-circle me-2"></i>Confirmar Voto
                            </button>
                        ` : encuesta.mostrarResultados ? `
                            <div class="total-votos">
                                <span class="total-votos-numero">${totalVotos}</span>
                                <span class="total-votos-texto">votos totales</span>
                            </div>
                        ` : ''}
                        
                        ${esAutor ? `
                            <button class="btn btn-danger w-100 mt-2" onclick="encuestasManager.eliminarEncuesta(${encuesta.id})">
                                <i class="fas fa-trash me-2"></i>Eliminar Encuesta
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    renderizarOpciones(encuesta, yaVoto) {
        const totalVotos = encuesta.opciones.reduce((sum, op) => sum + op.votos, 0);
        const mostrarResultados = yaVoto && encuesta.mostrarResultados;
        
        return `
            <div class="votacion-opciones" id="opciones-${encuesta.id}">
                ${encuesta.opciones.map(opcion => {
                    const porcentaje = totalVotos > 0 ? Math.round((opcion.votos / totalVotos) * 100) : 0;
                    
                    return `
                        <div class="opcion-voto ${yaVoto ? 'voted' : ''}" 
                             data-encuesta="${encuesta.id}" 
                             data-opcion="${opcion.id}"
                             onclick="${!yaVoto ? `encuestasManager.seleccionarOpcion(${encuesta.id}, ${opcion.id}, ${encuesta.permitirMultiple})` : ''}">
                            ${mostrarResultados ? `
                                <div class="opcion-voto-barra" style="width: ${porcentaje}%"></div>
                            ` : ''}
                            
                            <div class="opcion-voto-content">
                                <div class="d-flex align-items-center">
                                    ${!yaVoto ? (encuesta.permitirMultiple ? `
                                        <div class="checkbox-custom">
                                            <i class="fas fa-check" style="display: none;"></i>
                                        </div>
                                    ` : `
                                        <div class="radio-custom"></div>
                                    `) : ''}
                                    <span class="opcion-voto-texto">${opcion.texto}</span>
                                </div>
                                
                                ${mostrarResultados ? `
                                    <div>
                                        <span class="opcion-voto-porcentaje">${porcentaje}%</span>
                                        <span class="opcion-voto-votos">(${opcion.votos})</span>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }
    
    // ==================== VOTACIÓN ====================
    
    seleccionarOpcion(encuestaId, opcionId, permitirMultiple) {
        const opcionElemento = document.querySelector(
            `.opcion-voto[data-encuesta="${encuestaId}"][data-opcion="${opcionId}"]`
        );
        
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
        
        // Verificar si ya votó
        if (encuesta.votantes.includes(this.currentUser.id)) {
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
        
        // Registrar voto
        opcionesSeleccionadas.forEach(opcionId => {
            const opcion = encuesta.opciones.find(o => o.id === opcionId);
            if (opcion) {
                opcion.votos++;
            }
        });
        
        // Marcar usuario como votante
        encuesta.votantes.push(this.currentUser.id);
        
        // Guardar cambios
        this.guardarEncuestas();
        
        // Recargar vista
        await this.cargarEncuestas();
        
        this.showToast('¡Voto registrado exitosamente!', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    // ==================== ELIMINAR ENCUESTA ====================
    
    async eliminarEncuesta(encuestaId) {
        if (!confirm('¿Estás seguro de que quieres eliminar esta encuesta?')) {
            return;
        }
        
        this.encuestas = this.encuestas.filter(e => e.id !== encuestaId);
        this.guardarEncuestas();
        await this.cargarEncuestas();
        
        this.showToast('Encuesta eliminada', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    // ==================== UTILIDADES ====================
    
    guardarEncuestas() {
        localStorage.setItem('studentspoint_encuestas', JSON.stringify(this.encuestas));
    }
    
    mostrarModalCrear() {
        this.limpiarFormulario();
        this.modalCrear.show();
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    formatearFecha(fechaISO) {
        const fecha = new Date(fechaISO);
        const ahora = new Date();
        const diff = ahora - fecha;
        
        const minutos = Math.floor(diff / 60000);
        const horas = Math.floor(diff / 3600000);
        const dias = Math.floor(diff / 86400000);
        
        if (minutos < 1) return 'Ahora';
        if (minutos < 60) return `Hace ${minutos} min`;
        if (horas < 24) return `Hace ${horas}h`;
        if (dias < 7) return `Hace ${dias}d`;
        
        return fecha.toLocaleDateString('es-ES', { 
            day: 'numeric', 
            month: 'short',
            year: fecha.getFullYear() !== ahora.getFullYear() ? 'numeric' : undefined
        });
    }
    
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
            background: ${colors[type]};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
}

// Inicializar
let encuestasManager;
document.addEventListener('DOMContentLoaded', () => {
    encuestasManager = new EncuestasManager();
});

// Funciones globales
function mostrarModalCrear() {
    encuestasManager.mostrarModalCrear();
}

function agregarOpcion() {
    encuestasManager.agregarOpcion();
}

function eliminarOpcion(button) {
    encuestasManager.eliminarOpcion(button);
}

function removerImagen() {
    encuestasManager.removerImagen();
}

function crearEncuesta() {
    encuestasManager.crearEncuesta();
}
