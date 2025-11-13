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
}

let reportesManager;
document.addEventListener('DOMContentLoaded', () => {
    reportesManager = new ReportesManager();
});