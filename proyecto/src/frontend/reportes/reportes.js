/**
 * Módulo de Reportes - StudentsPoint
 * Sistema simple de reportes de desperfectos
 */

class ReportesManager {
    constructor() {
        this.currentUser = null;
        this.reportes = [];
        this.reportesFiltrados = [];
        this.imagenSeleccionada = null;
        this.modalCrear = null;
        this.modalDetalle = null;
        
        this.init();
    }
    
    async init() {
        await this.loadUser();
        this.setupEventListeners();
        await this.cargarReportes();
        
        // Inicializar modales
        this.modalCrear = new bootstrap.Modal(document.getElementById('modalCrearReporte'));
        this.modalDetalle = new bootstrap.Modal(document.getElementById('modalDetalleReporte'));
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
        document.getElementById('imagenReporte')?.addEventListener('change', (e) => {
            this.previewImagen(e.target.files[0]);
        });
        
        // Reproducir sonido de carga
        if (window.playSound) {
            window.playSound('pageLoad');
        }
    }
    
    // ==================== CREAR REPORTE ====================
    
    previewImagen(file) {
        if (!file) return;
        
        // Validar tamaño (5MB máx)
        if (file.size > 5 * 1024 * 1024) {
            this.showToast('La imagen es muy grande. Máximo 5MB.', 'error');
            return;
        }
        
        // Validar tipo
        if (!file.type.startsWith('image/')) {
            this.showToast('Por favor selecciona una imagen válida.', 'error');
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
    
    removerImagen() {
        this.imagenSeleccionada = null;
        
        const preview = document.getElementById('imagenPreview');
        const placeholder = document.querySelector('.upload-placeholder');
        const removeBtn = document.querySelector('.remove-image');
        const input = document.getElementById('imagenReporte');
        
        preview.classList.add('d-none');
        placeholder.classList.remove('d-none');
        removeBtn.classList.add('d-none');
        input.value = '';
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    async crearReporte() {
        const tipo = document.getElementById('tipoProblema').value;
        const ubicacion = document.getElementById('ubicacionReporte').value.trim();
        const titulo = document.getElementById('tituloReporte').value.trim();
        const descripcion = document.getElementById('descripcionReporte').value.trim();
        
        // Validaciones
        if (!this.imagenSeleccionada) {
            this.showToast('Por favor selecciona una imagen del desperfecto', 'warning');
            return;
        }
        
        if (!tipo) {
            this.showToast('Por favor selecciona el tipo de problema', 'warning');
            return;
        }
        
        if (!ubicacion) {
            this.showToast('Por favor ingresa la ubicación', 'warning');
            return;
        }
        
        if (!titulo) {
            this.showToast('Por favor ingresa un título', 'warning');
            return;
        }
        
        if (!descripcion) {
            this.showToast('Por favor describe el problema', 'warning');
            return;
        }
        
        // Crear objeto de reporte
        const reporte = {
            id: Date.now(),
            tipo,
            ubicacion,
            titulo,
            descripcion,
            imagen: this.imagenSeleccionada,
            autor: {
                id: this.currentUser.id,
                nombre: this.currentUser.name
            },
            fechaCreacion: new Date().toISOString()
        };
        
        // Guardar en localStorage
        this.reportes.push(reporte);
        this.guardarReportes();
        
        // Cerrar modal y limpiar
        this.modalCrear.hide();
        this.limpiarFormulario();
        
        // Recargar reportes
        await this.cargarReportes();
        
        // Notificación
        this.showToast('Reporte enviado exitosamente', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    limpiarFormulario() {
        document.getElementById('formCrearReporte').reset();
        this.removerImagen();
    }
    
    // ==================== CARGAR Y MOSTRAR REPORTES ====================
    
    async cargarReportes() {
        try {
            // Cargar desde localStorage
            const reportesGuardados = localStorage.getItem('studentspoint_reportes');
            this.reportes = reportesGuardados ? JSON.parse(reportesGuardados) : [];
            
            this.reportesFiltrados = [...this.reportes];
            this.actualizarEstadisticas();
            this.renderizarReportes();
        } catch (error) {
            console.error('Error al cargar reportes:', error);
            this.showToast('Error al cargar los reportes', 'error');
        }
    }
    
    actualizarEstadisticas() {
        const total = this.reportes.length;
        document.getElementById('stat-total').textContent = total;
    }
    
    filtrarReportes() {
        const tipoFiltro = document.getElementById('filtroTipo').value;
        const busqueda = document.getElementById('buscarReporte').value.toLowerCase();
        
        this.reportesFiltrados = this.reportes.filter(reporte => {
            const matchTipo = !tipoFiltro || reporte.tipo === tipoFiltro;
            const matchBusqueda = !busqueda || 
                reporte.titulo.toLowerCase().includes(busqueda) ||
                reporte.descripcion.toLowerCase().includes(busqueda) ||
                reporte.ubicacion.toLowerCase().includes(busqueda);
            
            return matchTipo && matchBusqueda;
        });
        
        this.renderizarReportes();
    }
    
    renderizarReportes() {
        const container = document.getElementById('reportes-container');
        
        if (this.reportesFiltrados.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <i class="fas fa-clipboard-list"></i>
                        <h3>No hay reportes</h3>
                        <p>Sé el primero en reportar un problema para ayudar a mejorar la sede</p>
                        <button class="btn btn-primary mt-3" onclick="reportesManager.mostrarModalCrear()">
                            <i class="fas fa-plus-circle me-2"></i>Crear Primer Reporte
                        </button>
                    </div>
                </div>
            `;
            return;
        }
        
        // Ordenar por fecha más reciente
        const reportesOrdenados = [...this.reportesFiltrados].sort((a, b) => 
            new Date(b.fechaCreacion) - new Date(a.fechaCreacion)
        );
        
        container.innerHTML = reportesOrdenados.map(reporte => 
            this.renderizarTarjetaReporte(reporte)
        ).join('');
    }
    
    renderizarTarjetaReporte(reporte) {
        const tipoTexto = {
            'infraestructura': '🏗️ Infraestructura',
            'equipamiento': '💻 Equipamiento',
            'limpieza': '🧹 Limpieza',
            'seguridad': '🔒 Seguridad',
            'otro': '📋 Otro'
        };
        
        return `
            <div class="col-12 col-md-6 col-lg-4">
                <div class="reporte-card" onclick="reportesManager.verDetalle(${reporte.id})">
                    <img src="${reporte.imagen}" alt="${reporte.titulo}" class="reporte-card-image">
                    
                    <div class="reporte-card-body">
                        <div class="reporte-header">
                            <span class="badge-tipo">${tipoTexto[reporte.tipo]}</span>
                        </div>
                        
                        <h3 class="reporte-title">${reporte.titulo}</h3>
                        
                        <div class="reporte-ubicacion">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>${reporte.ubicacion}</span>
                        </div>
                        
                        <p class="reporte-description">${reporte.descripcion}</p>
                        
                        <div class="reporte-meta">
                            <div class="reporte-meta-item">
                                <i class="fas fa-user"></i>
                                <span>${reporte.autor.nombre}</span>
                            </div>
                            <div class="reporte-meta-item">
                                <i class="fas fa-calendar"></i>
                                <span>${this.formatearFecha(reporte.fechaCreacion)}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // ==================== VER DETALLE ====================
    
    verDetalle(reporteId) {
        const reporte = this.reportes.find(r => r.id === reporteId);
        if (!reporte) return;
        
        const tipoTexto = {
            'infraestructura': '🏗️ Infraestructura',
            'equipamiento': '💻 Equipamiento',
            'limpieza': '🧹 Limpieza',
            'seguridad': '🔒 Seguridad',
            'otro': '📋 Otro'
        };
        
        // Título del modal
        document.getElementById('detalleModalTitle').innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>${reporte.titulo}
        `;
        
        // Cuerpo del modal
        document.getElementById('detalleModalBody').innerHTML = `
            <img src="${reporte.imagen}" alt="${reporte.titulo}" class="detalle-imagen">
            
            <div class="detalle-info">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <div class="detalle-item">
                            <div class="detalle-item-label">Tipo de Problema</div>
                            <div class="detalle-item-value">${tipoTexto[reporte.tipo]}</div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="detalle-item">
                            <div class="detalle-item-label">Ubicación</div>
                            <div class="detalle-item-value">
                                <i class="fas fa-map-marker-alt me-2"></i>${reporte.ubicacion}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="detalle-item">
                            <div class="detalle-item-label">Reportado por</div>
                            <div class="detalle-item-value">
                                <i class="fas fa-user me-2"></i>${reporte.autor.nombre}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="detalle-item">
                            <div class="detalle-item-label">Fecha de Reporte</div>
                            <div class="detalle-item-value">
                                <i class="fas fa-calendar me-2"></i>${this.formatearFechaCompleta(reporte.fechaCreacion)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="detalle-descripcion">
                <strong style="color: #fbbf24; display: block; margin-bottom: 0.5rem;">
                    <i class="fas fa-align-left me-2"></i>Descripción del Problema
                </strong>
                ${reporte.descripcion}
            </div>
        `;
        
        // Footer del modal - solo mostrar botón eliminar si es el autor
        const esAutor = reporte.autor.id === this.currentUser.id;
        
        if (esAutor) {
            document.getElementById('detalleModalFooter').innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                <button type="button" class="btn btn-danger" onclick="reportesManager.eliminarReporte(${reporte.id})">
                    <i class="fas fa-trash me-2"></i>Eliminar
                </button>
            `;
        } else {
            document.getElementById('detalleModalFooter').innerHTML = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
            `;
        }
        
        this.modalDetalle.show();
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    // ==================== ELIMINAR REPORTE ====================
    
    async eliminarReporte(reporteId) {
        if (!confirm('¿Estás seguro de que quieres eliminar este reporte?')) {
            return;
        }
        
        this.reportes = this.reportes.filter(r => r.id !== reporteId);
        this.guardarReportes();
        
        this.modalDetalle.hide();
        await this.cargarReportes();
        
        this.showToast('Reporte eliminado', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    // ==================== UTILIDADES ====================
    
    guardarReportes() {
        localStorage.setItem('studentspoint_reportes', JSON.stringify(this.reportes));
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
    
    formatearFechaCompleta(fechaISO) {
        const fecha = new Date(fechaISO);
        return fecha.toLocaleDateString('es-ES', { 
            day: 'numeric', 
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    showToast(message, type = 'info') {
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
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
let reportesManager;
document.addEventListener('DOMContentLoaded', () => {
    reportesManager = new ReportesManager();
});

// Funciones globales
function mostrarModalCrear() {
    reportesManager.mostrarModalCrear();
}

function removerImagen() {
    reportesManager.removerImagen();
}

function crearReporte() {
    reportesManager.crearReporte();
}

