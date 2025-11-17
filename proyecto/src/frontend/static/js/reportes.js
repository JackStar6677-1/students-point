class ReportesManager {
    constructor() {
        this.reports = [];
        this.sedes = [];
        this.categorySet = new Set();
        this.token = null;
        this.currentUser = null;
        this.init();
    }

    async init() {
        try {
            await this.ensureAuth();
            this.setupEventListeners();
            await this.loadSedes();
            await this.loadData();
        } catch (error) {
            console.error('Error inicializando reportes:', error);
            this.showToast(error.message || 'No fue posible cargar los reportes', 'error');
        }
    }

    async ensureAuth() {
        if (!window.authAPI || !window.authAPI.isAuthenticated()) {
            window.location.href = '/login.html';
            throw new Error('Usuario no autenticado');
        }

        try {
            this.currentUser = await window.authAPI.getCurrentUser();
            this.token = window.authAPI.getAuthToken();
            if (window) {
                window.dispatchEvent(new Event('authChange'));
            }
        } catch (error) {
            window.authAPI.logout();
            window.location.href = '/login.html';
            throw error;
        }
    }

    setupEventListeners() {
        document.getElementById('btnAplicarFiltros')?.addEventListener('click', () => {
            this.loadData();
        });

        document.getElementById('btnLimpiarFiltros')?.addEventListener('click', () => {
            this.resetFilters();
            this.loadData();
        });

        document.getElementById('btnExportarExcel')?.addEventListener('click', () => {
            this.exportarReporte('excel');
        });

        document.getElementById('btnExportarPDF')?.addEventListener('click', () => {
            this.exportarReporte('pdf');
        });

        // Modal de nuevo reporte
        const btnNuevoReporte = document.getElementById('btnNuevoReporte');
        const modalNuevoReporte = document.getElementById('modalNuevoReporte');
        const btnCrearReporte = document.getElementById('btnCrearReporte');
        const inputFotos = document.getElementById('reporteFotos');

        if (btnNuevoReporte && modalNuevoReporte) {
            const modal = new bootstrap.Modal(modalNuevoReporte);
            btnNuevoReporte.addEventListener('click', () => {
                this.resetFormNuevoReporte();
                this.populateSedesInForm();
                this.getCurrentLocation();
                modal.show();
            });

            if (btnCrearReporte) {
                btnCrearReporte.addEventListener('click', () => {
                    this.crearReporte();
                });
            }

            if (inputFotos) {
                inputFotos.addEventListener('change', (e) => {
                    this.previewFotos(e.target.files);
                });
            }

            // Resetear formulario al cerrar modal
            modalNuevoReporte.addEventListener('hidden.bs.modal', () => {
                this.resetFormNuevoReporte();
            });
        }
    }

    resetFilters() {
        const fechaInicio = document.getElementById('filtroFechaInicio');
        const fechaFin = document.getElementById('filtroFechaFin');
        const categoria = document.getElementById('filtroTipo');
        const campus = document.getElementById('filtroCampus');

        if (fechaInicio) fechaInicio.value = '';
        if (fechaFin) fechaFin.value = '';
        if (categoria) categoria.value = '';
        if (campus) campus.value = '';
    }

    async loadSedes() {
        try {
            const response = await fetch('/api/sedes/');
            if (!response.ok) {
                throw new Error('No se pudieron cargar las sedes');
            }
            this.sedes = await response.json();
            this.populateCampusSelect();
        } catch (error) {
            console.error('Error cargando sedes:', error);
        }
    }

    populateCampusSelect() {
        const select = document.getElementById('filtroCampus');
        if (!select) {
            return;
        }

        const currentValue = select.value;
        select.innerHTML = '<option value="">Todas las sedes</option>';

        this.sedes.forEach((sede) => {
            const option = document.createElement('option');
            option.value = sede.slug;
            option.textContent = sede.nombre;
            select.appendChild(option);
        });

        if (currentValue) {
            const exists = this.sedes.some((sede) => sede.slug === currentValue);
            select.value = exists ? currentValue : '';
        }
    }

    buildQueryParams() {
        const params = new URLSearchParams();
        const fechaInicio = document.getElementById('filtroFechaInicio')?.value;
        const fechaFin = document.getElementById('filtroFechaFin')?.value;
        const categoria = document.getElementById('filtroTipo')?.value;
        const campus = document.getElementById('filtroCampus')?.value;

        if (fechaInicio) params.append('fecha_inicio', fechaInicio);
        if (fechaFin) params.append('fecha_fin', fechaFin);
        if (categoria) params.append('categoria', categoria);
        if (campus) params.append('sede', campus);

        return params.toString();
    }

    async loadData() {
        this.showLoading(true);
        try {
            const params = this.buildQueryParams();
            const endpoint = params ? `/api/reports/?${params}` : '/api/reports/';

            const response = await fetch(endpoint, {
                headers: this.getAuthHeaders(),
            });

            if (response.status === 401) {
                window.authAPI.logout();
                window.location.href = '/login.html';
                return;
            }

            if (!response.ok) {
                throw new Error('No se pudieron cargar los reportes');
            }

            const data = await response.json();
            const reports = Array.isArray(data) ? data : data?.results || [];

            this.reports = reports;
            this.updateCategoryOptions(reports);
            this.updateKPIs(reports);
            this.updateResumen(reports);
            this.renderReports(reports);
        } catch (error) {
            console.error('Error cargando reportes:', error);
            this.showToast(error.message || 'Error cargando reportes', 'error');
            this.renderReports([]);
        } finally {
            this.showLoading(false);
        }
    }

    updateCategoryOptions(reports) {
        const select = document.getElementById('filtroTipo');
        if (!select) return;

        const selectedValue = select.value;
        reports
            .map((reporte) => reporte.categoria)
            .filter((categoria) => !!categoria)
            .forEach((categoria) => this.categorySet.add(categoria));

        const categories = Array.from(this.categorySet).sort((a, b) => a.localeCompare(b));
        select.innerHTML = '<option value="">Todas las categorías</option>';
        categories.forEach((categoria) => {
            const option = document.createElement('option');
            option.value = categoria;
            option.textContent = categoria;
            select.appendChild(option);
        });

        if (selectedValue && this.categorySet.has(selectedValue)) {
            select.value = selectedValue;
        }
    }

    updateKPIs(reports) {
        const total = reports.length;
        const enRevision = reports.filter((reporte) => reporte.estado === 'revision').length;
        const resueltos = reports.filter((reporte) => reporte.estado === 'resuelto').length;
        const abiertos = reports.filter((reporte) => reporte.estado === 'abierto').length;

        const setText = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        };

        setText('totalReportes', total);
        setText('reportesRevision', enRevision);
        setText('reportesResueltos', resueltos);
        setText('reportesPendientes', abiertos);

        const now = new Date();
        this.setTrend('totalReportesTrend', `<i class="fas fa-sync-alt"></i> Actualizado ${this.formatTime(now)}`);
        this.setTrend(
            'reportesRevisionTrend',
            enRevision > 0 ? '<i class="fas fa-hourglass-half"></i> Requieren seguimiento' : '<i class="fas fa-check"></i> Sin pendientes'
        );
        this.setTrend(
            'reportesResueltosTrend',
            resueltos > 0 ? '<i class="fas fa-thumbs-up"></i> Buen trabajo' : '<i class="fas fa-info-circle"></i> Aún sin resolver'
        );
        this.setTrend(
            'reportesPendientesTrend',
            abiertos > 0 ? '<i class="fas fa-bell"></i> Atención requerida' : '<i class="fas fa-check-circle"></i> Todo resuelto'
        );
    }

    setTrend(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = message;
        }
    }

    updateResumen(reports) {
        const resumen = document.getElementById('reportesResultadoResumen');
        if (!resumen) return;

        if (!reports.length) {
            resumen.textContent = 'No se encontraron reportes para los filtros seleccionados.';
            return;
        }

        const filtrosActivos = [];
        const fechaInicio = document.getElementById('filtroFechaInicio')?.value;
        const fechaFin = document.getElementById('filtroFechaFin')?.value;
        const categoria = document.getElementById('filtroTipo')?.value;
        const campus = document.getElementById('filtroCampus')?.value;

        if (fechaInicio) filtrosActivos.push(`desde ${this.formatDate(fechaInicio)}`);
        if (fechaFin) filtrosActivos.push(`hasta ${this.formatDate(fechaFin)}`);
        if (categoria) filtrosActivos.push(`categoría «${categoria}»`);
        if (campus) {
            const sede = this.sedes.find((item) => item.slug === campus);
            filtrosActivos.push(`sede «${sede?.nombre || campus}»`);
        }

        const filtros = filtrosActivos.length ? ` con filtros (${filtrosActivos.join(', ')})` : '';
        resumen.textContent = `Mostrando ${reports.length} reporte(s)${filtros}.`;
    }

    renderReports(reports) {
        const container = document.getElementById('reportesLista');
        const emptyState = document.getElementById('reportesVacio');

        if (!container || !emptyState) {
            return;
        }

        if (!reports.length) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        container.innerHTML = reports.map((reporte) => this.renderReportCard(reporte)).join('');
    }

    renderReportCard(reporte) {
        const estado = this.formatEstado(reporte.estado);
        const estadoClass = this.getEstadoBadgeClass(reporte.estado);
        const prioridadLabel = this.getPrioridadLabel(reporte.prioridad);
        const prioridadClass = this.getPrioridadBadgeClass(reporte.prioridad);
        const fecha = this.formatDateTime(reporte.creado_at);

        // Renderizar fotos si existen
        let fotosHtml = '';
        if (reporte.media && Array.isArray(reporte.media) && reporte.media.length > 0) {
            const fotos = reporte.media.map(m => m.url || m.imagen).filter(Boolean);
            if (fotos.length > 0) {
                fotosHtml = `
                    <div class="mt-3">
                        <small class="text-muted d-block mb-2"><i class="fas fa-images me-1"></i>Fotos adjuntas:</small>
                        <div class="d-flex flex-wrap gap-2">
                            ${fotos.map(url => `
                                <img src="${this.escapeHtml(url)}" 
                                     alt="Foto del reporte" 
                                     class="img-thumbnail" 
                                     style="max-width: 100px; max-height: 100px; cursor: pointer;"
                                     onclick="window.open('${this.escapeHtml(url)}', '_blank')"
                                     loading="lazy">
                            `).join('')}
                        </div>
                    </div>
                `;
            }
        }

        return `
            <article class="card shadow-sm mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
                        <div>
                            <h3 class="h5 mb-1">${this.escapeHtml(reporte.categoria || 'Reporte sin categoría')}</h3>
                            <p class="text-muted mb-2">${this.escapeHtml(reporte.descripcion || 'Sin descripción')}</p>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-${estadoClass} me-1">${estado}</span>
                            <span class="badge bg-${prioridadClass}">${prioridadLabel}</span>
                        </div>
                    </div>

                    ${fotosHtml}

                    <div class="d-flex flex-wrap gap-3 text-muted small mt-3">
                        <span><i class="fas fa-map-marker-alt me-1"></i>${this.escapeHtml(reporte.sede_nombre || 'Sede no informada')}</span>
                        <span><i class="fas fa-clock me-1"></i>${fecha}</span>
                        <span><i class="fas fa-user me-1"></i>ID reportante: ${reporte.usuario ?? 'N/D'}</span>
                        <span><i class="fas fa-exclamation-circle me-1"></i>Prioridad ${reporte.prioridad ?? 0}</span>
                    </div>
                </div>
            </article>
        `;
    }

    getEstadoBadgeClass(estado) {
        switch (estado) {
            case 'resuelto':
                return 'success';
            case 'revision':
                return 'warning text-dark';
            case 'abierto':
            default:
                return 'danger';
        }
    }

    getPrioridadBadgeClass(prioridad) {
        if (prioridad >= 3) return 'danger';
        if (prioridad === 2) return 'warning text-dark';
        if (prioridad === 1) return 'info text-dark';
        return 'secondary';
    }

    getPrioridadLabel(prioridad) {
        if (prioridad >= 3) return 'Alta';
        if (prioridad === 2) return 'Media';
        if (prioridad === 1) return 'Baja';
        return 'Sin prioridad';
    }

    formatEstado(estado) {
        const mapping = {
            abierto: 'Abierto',
            revision: 'En revisión',
            resuelto: 'Resuelto',
        };
        return mapping[estado] || estado;
    }

    showLoading(show) {
        const loader = document.getElementById('reportesLoading');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }

    getAuthHeaders(includeJson = true) {
        const headers = {};
        if (includeJson) {
            headers['Content-Type'] = 'application/json';
        }
        if (this.token) {
            headers.Authorization = `Bearer ${this.token}`;
        }
        return headers;
    }

    async exportarReporte(formato) {
        if (!this.reports.length) {
            this.showToast('No hay reportes para exportar.', 'warning');
            return;
        }

        if (formato === 'excel') {
            this.exportAsCSV();
        } else if (formato === 'pdf') {
            this.exportAsPDF();
        } else {
            this.showToast('Formato no soportado', 'error');
        }
    }

    exportAsCSV() {
        const headers = ['ID', 'Categoría', 'Descripción', 'Estado', 'Sede', 'Prioridad', 'Lat', 'Lng', 'Creado'];
        const rows = this.reports.map((reporte) => [
            reporte.id,
            reporte.categoria || '',
            (reporte.descripcion || '').replace(/\s+/g, ' ').trim(),
            this.formatEstado(reporte.estado),
            reporte.sede_nombre || '',
            reporte.prioridad ?? '',
            reporte.lat ?? '',
            reporte.lng ?? '',
            this.formatDateTime(reporte.creado_at),
        ]);

        const csvContent = [headers, ...rows]
            .map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(','))
            .join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `reportes_studentspoint_${this.formatFileDate(new Date())}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        this.showToast('Archivo CSV generado correctamente.', 'info');
    }

    exportAsPDF() {
        const ventana = window.open('', '_blank');
        if (!ventana) {
            this.showToast('No se pudo abrir la ventana para exportar.', 'error');
            return;
        }

        const estilos = `
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { text-align: center; margin-bottom: 20px; }
                table { width: 100%; border-collapse: collapse; font-size: 12px; }
                th, td { border: 1px solid #999; padding: 6px 8px; text-align: left; }
                th { background: #f0f0f0; }
            </style>
        `;
        const filas = this.reports
            .map(
                (reporte) => `
                <tr>
                    <td>${reporte.id}</td>
                    <td>${this.escapeHtml(reporte.categoria || '')}</td>
                    <td>${this.escapeHtml(reporte.descripcion || '').slice(0, 140)}</td>
                    <td>${this.formatEstado(reporte.estado)}</td>
                    <td>${this.escapeHtml(reporte.sede_nombre || '')}</td>
                    <td>${reporte.prioridad ?? ''}</td>
                    <td>${this.formatDateTime(reporte.creado_at)}</td>
                </tr>`
            )
            .join('');

        ventana.document.write(`
            <html>
                <head>
                    <title>Reportes StudentsPoint</title>
                    ${estilos}
                </head>
                <body>
                    <h1>Reporte de incidencias StudentsPoint</h1>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Categoría</th>
                                <th>Descripción</th>
                                <th>Estado</th>
                                <th>Sede</th>
                                <th>Prioridad</th>
                                <th>Creado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${filas}
                        </tbody>
                    </table>
                </body>
            </html>
        `);
        ventana.document.close();
        ventana.focus();
        ventana.print();
    }

    formatDateTime(value) {
        if (!value) return 'Fecha no disponible';
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return value;
        return date.toLocaleString('es-CL', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    }

    formatDate(value) {
        if (!value) return '';
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return value;
        return date.toLocaleDateString('es-CL', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    }

    formatTime(date) {
        return date.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' });
    }

    formatFileDate(date) {
        const pad = (value) => String(value).padStart(2, '0');
        return `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}_${pad(date.getHours())}${pad(
            date.getMinutes()
        )}`;
    }

    escapeHtml(text) {
        if (text === null || text === undefined) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showToast(message, type = 'info') {
        const normalizedType = ['error', 'warning', 'info'].includes(type) ? type : 'info';
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.classList.add(normalizedType);
        toast.innerHTML = `<div class="toast-content"><span>${message}</span></div>`;
        document.body.appendChild(toast);
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 3000);
    }

    // Métodos para crear nuevo reporte
    resetFormNuevoReporte() {
        const form = document.getElementById('formNuevoReporte');
        if (form) form.reset();
        const preview = document.getElementById('fotosPreview');
        if (preview) preview.innerHTML = '';
        const errorDiv = document.getElementById('reporteError');
        if (errorDiv) {
            errorDiv.classList.add('d-none');
            errorDiv.textContent = '';
        }
    }

    populateSedesInForm() {
        const select = document.getElementById('reporteSede');
        if (!select || !this.sedes.length) return;

        const currentValue = select.value;
        select.innerHTML = '<option value="">Selecciona una sede</option>';
        this.sedes.forEach((sede) => {
            const option = document.createElement('option');
            option.value = sede.id || sede.slug;
            option.textContent = sede.nombre;
            select.appendChild(option);
        });

        if (currentValue) {
            select.value = currentValue;
        }
    }

    getCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latInput = document.getElementById('reporteLat');
                    const lngInput = document.getElementById('reporteLng');
                    if (latInput) latInput.value = position.coords.latitude.toFixed(6);
                    if (lngInput) lngInput.value = position.coords.longitude.toFixed(6);
                },
                (error) => {
                    console.warn('No se pudo obtener la ubicación:', error);
                }
            );
        }
    }

    previewFotos(files) {
        const preview = document.getElementById('fotosPreview');
        if (!preview) return;

        preview.innerHTML = '';
        Array.from(files).forEach((file, index) => {
            if (!file.type.startsWith('image/')) {
                this.showToast(`El archivo ${file.name} no es una imagen`, 'warning');
                return;
            }
            if (file.size > 5 * 1024 * 1024) {
                this.showToast(`La imagen ${file.name} es muy grande (máx 5MB)`, 'warning');
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'img-thumbnail';
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                img.style.margin = '4px';
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }

    async crearReporte() {
        const sede = document.getElementById('reporteSede')?.value;
        const categoria = document.getElementById('reporteCategoria')?.value;
        const descripcion = document.getElementById('reporteDescripcion')?.value;
        const lat = document.getElementById('reporteLat')?.value;
        const lng = document.getElementById('reporteLng')?.value;
        const fotosInput = document.getElementById('reporteFotos');
        const errorDiv = document.getElementById('reporteError');
        const btnCrear = document.getElementById('btnCrearReporte');

        // Validar campos requeridos
        if (!sede || !categoria || !descripcion || !lat || !lng) {
            if (errorDiv) {
                errorDiv.textContent = 'Por favor completa todos los campos requeridos.';
                errorDiv.classList.remove('d-none');
            }
            return;
        }

        if (errorDiv) errorDiv.classList.add('d-none');

        // Crear FormData para multipart/form-data
        const formData = new FormData();
        formData.append('sede', sede);
        formData.append('categoria', categoria);
        formData.append('descripcion', descripcion);
        formData.append('lat', parseFloat(lat));
        formData.append('lng', parseFloat(lng));

        // Agregar fotos
        if (fotosInput && fotosInput.files.length > 0) {
            Array.from(fotosInput.files).forEach((file, index) => {
                if (file.type.startsWith('image/') && file.size <= 5 * 1024 * 1024) {
                    formData.append(`imagen_${index}`, file);
                }
            });
        }

        if (btnCrear) btnCrear.disabled = true;

        try {
            const response = await fetch('/api/reports/', {
                method: 'POST',
                headers: this.getAuthHeaders(false), // No incluir Content-Type para multipart
                body: formData,
            });

            if (response.status === 401) {
                window.authAPI.logout();
                window.location.href = '/login.html';
                return;
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Error al crear el reporte' }));
                throw new Error(errorData.detail || errorData.message || 'Error al crear el reporte');
            }

            this.showToast('Reporte creado exitosamente', 'success');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalNuevoReporte'));
            if (modal) modal.hide();

            // Recargar lista de reportes
            await this.loadData();
        } catch (error) {
            console.error('Error creando reporte:', error);
            if (errorDiv) {
                errorDiv.textContent = error.message || 'Error al crear el reporte';
                errorDiv.classList.remove('d-none');
            }
            this.showToast(error.message || 'Error al crear el reporte', 'error');
        } finally {
            if (btnCrear) btnCrear.disabled = false;
        }
    }
}

let reportesManager;
document.addEventListener('DOMContentLoaded', () => {
    reportesManager = new ReportesManager();
});