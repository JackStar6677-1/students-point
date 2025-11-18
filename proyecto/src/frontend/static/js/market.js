/**
 * Sistema de Market StudentsPoint
 * Interfaz completa para compra/venta segura
 */

class MarketApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentUser = null;
        this.productos = [];
        this.categorias = [];
        this.campus = [];
        this.filtros = {};
        this.productoActual = null;
        
        this.init();
    }
    
    async init() {
        await this.checkAuth();
        this.setupEventListeners();
        this.loadProductos();
    }
    
    // === AUTENTICACIÓN ===
    async checkAuth() {
        try {
            if (!window.authAPI || !window.authAPI.isAuthenticated()) {
                this.redirectToLogin();
                return;
            }

            this.currentUser = await window.authAPI.getCurrentUser();
            if (!this.currentUser) {
                this.redirectToLogin();
                return;
            }

            if (window) {
                window.dispatchEvent(new Event('authChange'));
            }
            this.updateUIForUser();
        } catch (error) {
            console.error('Error verificando autenticación:', error);
            this.redirectToLogin();
        }
    }
    
    redirectToLogin() {
        if (window.authAPI && typeof window.authAPI.logout === 'function') {
            window.authAPI.logout();
        }
        window.location.href = '/login.html';
    }
    
    updateUIForUser() {
        const btnCrear = document.getElementById('btnCrearProducto');
        if (btnCrear) {
            btnCrear.style.display = this.currentUser ? 'block' : 'none';
        }

        const sidebarName = document.getElementById('sidebarUserName');
        const sidebarRole = document.getElementById('sidebarUserRole');
        if (sidebarName && this.currentUser) {
            sidebarName.textContent = this.currentUser.name || this.currentUser.email;
        }
        if (sidebarRole && this.currentUser) {
            sidebarRole.textContent = this.currentUser.career || 'Estudiante';
        }
    }
    
    // === EVENT LISTENERS ===
    setupEventListeners() {
        // Botones principales
        document.getElementById('btnCrearProducto')?.addEventListener('click', () => this.showCrearProducto());
        document.getElementById('btnMisProductos')?.addEventListener('click', () => this.showMisProductos());
        document.getElementById('btnFavoritos')?.addEventListener('click', () => this.showFavoritos());
        
        // Filtros
        document.getElementById('btnFiltrar')?.addEventListener('click', () => this.aplicarFiltros());
        document.getElementById('btnLimpiarFiltros')?.addEventListener('click', () => this.limpiarFiltros());
        
        // Formularios
        document.getElementById('formCrearProducto')?.addEventListener('submit', (e) => this.crearProducto(e));
        document.getElementById('formReportar')?.addEventListener('submit', (e) => this.reportarProducto(e));
        
        
        // Modales
        this.setupModalListeners();
    }
    
    setupModalListeners() {
        // Cerrar modales
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });
        
        // Cerrar al hacer click fuera del modal
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        });
    }
    
    
    async loadProductos() {
        this.showLoading(true);
        
        try {
            this.productos = await window.marketAPI.getProductos(this.filtros);
            this.renderProductos();
        } catch (error) {
            console.error('Error cargando productos:', error);
            this.showError(error.message || 'Error cargando productos');
        } finally {
            this.showLoading(false);
        }
    }
    
    // === RENDERIZADO ===
    renderProductos() {
        const container = document.getElementById('productosList');
        const noResults = document.getElementById('noResults');
        
        if (!container) return;
        
        if (this.productos.length === 0) {
            container.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }
        
        noResults.style.display = 'none';
        
        container.innerHTML = this.productos.map(producto => `
            <div class="producto-card" data-id="${producto.id}">
                <div class="producto-imagen">
                    ${producto.imagen_url ? 
                        `<img src="${producto.imagen_url}" alt="${producto.titulo}" loading="lazy">` :
                        `<div class="no-image"><i class="bi bi-image"></i></div>`
                    }
                    <div class="producto-favorito ${producto.es_favorito ? 'activo' : ''}">
                        <i class="bi bi-heart${producto.es_favorito ? '-fill' : ''}"></i>
                    </div>
                </div>
                
                <div class="producto-info">
                    <h3 class="producto-titulo">${producto.titulo}</h3>
                    <p class="producto-descripcion">${this.truncateText(producto.descripcion, 100)}</p>
                    
                    <div class="producto-meta">
                        <span class="producto-categoria">
                            <i class="bi bi-${producto.categoria_icono || 'tag'}"></i>
                            ${producto.categoria_nombre}
                        </span>
                        <span class="producto-vendedor">
                            <i class="bi bi-person"></i>
                            ${producto.vendedor_nombre}
                        </span>
                    </div>
                    
                    <div class="producto-footer">
                        <div class="producto-precios">
                            ${this.renderCardPrice(producto)}
                        </div>
                        <button class="btn btn-sm btn-outline ver-producto" data-id="${producto.id}">
                            Ver Detalles
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Event listeners para las tarjetas
        container.querySelectorAll('.ver-producto').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.dataset.id;
                this.verProducto(id);
            });
        });
        
        container.querySelectorAll('.producto-favorito').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const card = e.target.closest('.producto-card');
                const id = card.dataset.id;
                this.toggleFavorito(id);
            });
        });
    }
    
    // === FILTROS ===
    aplicarFiltros() {
        this.filtros = {};
        
        const categoria = document.getElementById('filtroCategoria')?.value;
        const campus = document.getElementById('filtroCampus')?.value;
        const precio = document.getElementById('filtroPrecio')?.value;
        const busqueda = document.getElementById('busqueda')?.value;
        
        if (categoria) this.filtros.categoria = categoria;
        if (campus) this.filtros.campus = campus;
        if (precio) this.filtros.precio_max = precio;
        if (busqueda) this.filtros.search = busqueda;
        
        this.loadProductos();
    }
    
    limpiarFiltros() {
        document.getElementById('filtroCategoria').value = '';
        document.getElementById('filtroCampus').value = '';
        document.getElementById('filtroPrecio').value = '';
        document.getElementById('busqueda').value = '';
        
        this.filtros = {};
        this.loadProductos();
    }
    
    // === MODALES ===
    showCrearProducto() {
        document.getElementById('modalCrearProducto').style.display = 'block';
        document.getElementById('formCrearProducto').reset();
    }
    
    async showMisProductos() {
        try {
            this.productos = await window.marketAPI.getMisProductos();
            this.renderProductos();
        } catch (error) {
            console.error('Error cargando mis productos:', error);
            this.showError(error.message || 'Error cargando productos');
        }
    }
    
    async showFavoritos() {
        try {
            const favoritos = await window.marketAPI.getMisFavoritos();
            this.productos = favoritos.map(f => f.producto);
            this.renderProductos();
        } catch (error) {
            console.error('Error cargando favoritos:', error);
            this.showError(error.message || 'Error cargando favoritos');
        }
    }
    
    async verProducto(id) {
        try {
            this.productoActual = await window.marketAPI.getProducto(id);
            this.renderProductoModal();
            document.getElementById('modalVerProducto').style.display = 'block';
        } catch (error) {
            console.error('Error cargando producto:', error);
            this.showError(error.message || 'Error cargando producto');
        }
    }
    
    renderProductoModal() {
        const producto = this.productoActual;
        
        document.getElementById('modalTitulo').textContent = producto.titulo;
        
        const detalle = document.getElementById('productoDetalle');
        detalle.innerHTML = `
            <div class="producto-modal-imagen">
                ${producto.imagen_url ? 
                    `<img src="${producto.imagen_url}" alt="${producto.titulo}">` :
                    `<div class="no-image-large"><i class="bi bi-image"></i></div>`
                }
            </div>
            
            <div class="producto-modal-info">
                <div class="producto-meta-modal">
                    <span class="categoria">
                        <i class="bi bi-${producto.categoria_icono || 'tag'}"></i>
                        ${producto.categoria_nombre}
                    </span>
                    <span class="vendedor">
                        <i class="bi bi-person"></i>
                        ${producto.vendedor_nombre}
                    </span>
                    <span class="campus">
                        <i class="bi bi-geo-alt"></i>
                        ${producto.campus_nombre || 'No especificado'}
                    </span>
                </div>
                
                <div class="producto-descripcion-modal">
                    <h4>Descripción</h4>
                    <p>${producto.descripcion}</p>
                </div>
                
                <div class="producto-precio-modal">
                    <h4>Precio</h4>
                    ${this.renderModalPrice(producto)}
                </div>
                
                <div class="producto-enlaces">
                    <h4>Enlaces</h4>
                    <a href="${producto.url_principal}" target="_blank" class="enlace-principal">
                        <i class="bi bi-box-arrow-up-right"></i>
                        Ver en ${producto.tipo_enlace}
                    </a>
                    
                    ${producto.urls_adicionales && producto.urls_adicionales.length > 0 ? `
                        <div class="enlaces-adicionales">
                            <h5>Enlaces adicionales:</h5>
                            ${producto.urls_adicionales.map(url => `
                                <a href="${url}" target="_blank" class="enlace-adicional">
                                    <i class="bi bi-link"></i> ${url}
                                </a>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        // Actualizar botón de favorito
        const favoritoTexto = document.getElementById('favoritoTexto');
        if (favoritoTexto) {
            favoritoTexto.textContent = producto.es_favorito ? 'Quitar de Favoritos' : 'Agregar a Favoritos';
        }
        
        // Event listeners para botones
        document.getElementById('btnVerEnlace')?.addEventListener('click', () => {
            window.open(producto.url_principal, '_blank');
            this.registrarClick(producto.id);
        });
        
        document.getElementById('btnToggleFavorito')?.addEventListener('click', () => {
            this.toggleFavorito(producto.id);
        });
        
        document.getElementById('btnReportar')?.addEventListener('click', () => {
            this.showReportarModal();
        });
    }
    
    showReportarModal() {
        document.getElementById('modalVerProducto').style.display = 'none';
        document.getElementById('modalReportar').style.display = 'block';
    }
    
    closeModal() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }
    
    // === ACCIONES ===
    async crearProducto(e) {
        e.preventDefault();
        
        // Obtener valores
        const descripcion = document.getElementById('inputDescripcion').value.trim();
        const urlPrincipal = document.getElementById('inputUrlPrincipal').value.trim();
        const precio = document.getElementById('inputPrecio').value;
        const precioStudentPoint = document.getElementById('inputPrecioStudentPoint').value;
        
        // Validar
        if (!descripcion) {
            this.showError('El mensaje es obligatorio');
            return;
        }
        
        if (!urlPrincipal) {
            this.showError('El link es obligatorio');
            return;
        }
        
        const btnSubmit = document.getElementById('btnSubmitProducto');
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Publicando...';
        
        try {
            const data = {
                titulo: descripcion.substring(0, 50), // Primera parte como título
                descripcion: descripcion,
                url_principal: urlPrincipal
            };
            
            if (precio) data.precio = precio;
            if (precioStudentPoint) data.precio_student_point = precioStudentPoint;
            
            console.log('Enviando:', data);
            
            const response = await fetch(`${this.apiBaseUrl}/market/productos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${window.authAPI.getAuthToken()}`
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                console.error('Error:', error);
                throw new Error(JSON.stringify(error));
            }
            
            const producto = await response.json();
            console.log('Creado:', producto);
            
            this.showSuccess('¡Publicado!');
            this.closeModal();
            document.getElementById('formCrearProducto').reset();
            
            // Recargar
            this.loadProductos();
            
        } catch (error) {
            console.error(error);
            this.showError('Error al publicar. Revisa la consola (F12)');
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Publicar';
        }
    }
    
    async toggleFavorito(id) {
        try {
            const data = await window.marketAPI.toggleFavorito(id);
            this.showSuccess(data.es_favorito ? 'Agregado a favoritos' : 'Removido de favoritos');
            this.loadProductos(); // Recargar para actualizar UI
        } catch (error) {
            console.error('Error toggle favorito:', error);
            this.showError(error.message || 'Error actualizando favoritos');
        }
    }
    
    async registrarClick(id) {
        try {
            await window.marketAPI.registrarClick(id);
        } catch (error) {
            console.error('Error registrando click:', error);
        }
    }
    
    async reportarProducto(e) {
        e.preventDefault();
        
        const formData = {
            producto: this.productoActual.id,
            tipo: document.getElementById('inputTipoReporte').value,
            descripcion: document.getElementById('inputDescripcionReporte').value
        };
        
        try {
            await window.marketAPI.reportarProducto(formData);
            this.showSuccess('Reporte enviado exitosamente');
            this.closeModal();
            document.getElementById('formReportar').reset();
        } catch (error) {
            console.error('Error reportando producto:', error);
            this.showError(error.message || 'Error enviando reporte');
        }
    }
    
    // === UTILIDADES ===
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    formatPrice(price) {
        const value = Number(price);
        if (Number.isNaN(value)) {
            return price ?? '';
        }
        return new Intl.NumberFormat('es-CL').format(value);
    }
    
    normalizePrice(value) {
        if (value === null || value === undefined || value === '') {
            return null;
        }
        const number = Number(value);
        return Number.isNaN(number) ? null : number;
    }
    
    getPriceInfo(producto) {
        const moneda = producto.moneda || 'CLP';
        const studentValue = this.normalizePrice(producto.precio_student_point);
        const originalValue = this.normalizePrice(producto.precio);
        const format = (value) => `$${this.formatPrice(value)} ${moneda}`;
        
        return {
            student: studentValue !== null ? { value: studentValue, formatted: format(studentValue) } : null,
            original: originalValue !== null ? { value: originalValue, formatted: format(originalValue) } : null,
            moneda
        };
    }
    
    renderCardPrice(producto) {
        const info = this.getPriceInfo(producto);
        const parts = [];
        
        if (info.student) {
            parts.push(
                `<span class="producto-precio-sp">${info.student.formatted}<span class="producto-precio-chip">StudentsPoint</span></span>`
            );
        }
        
        if (info.original) {
            const className = info.student ? 'producto-precio-original' : 'producto-precio';
            const extraLabel = info.student ? ' <small class="precio-etiqueta">Precio externo</small>' : '';
            parts.push(
                `<span class="${className}">${info.original.formatted}${extraLabel}</span>`
            );
        }
        
        if (!parts.length) {
            parts.push('<span class="producto-precio producto-precio-placeholder">Precio a consultar</span>');
        }
        
        return parts.join('');
    }
    
    renderModalPrice(producto) {
        const info = this.getPriceInfo(producto);
        if (!info.student && !info.original) {
            return '<p class="text-muted mb-0">Coordina el precio directamente con el vendedor.</p>';
        }
        
        const sections = [];
        
        if (info.student) {
            sections.push(
                `<div class="precio-line precio-line-sp">
                    <span class="precio-label">Precio StudentsPoint</span>
                    <span class="precio-valor">${info.student.formatted}</span>
                </div>`
            );
        }
        
        if (info.original) {
            sections.push(
                `<div class="precio-line ${info.student ? 'precio-line-original' : 'precio-line-standard'}">
                    <span class="precio-label">${info.student ? 'Precio externo' : 'Precio'}</span>
                    <span class="precio-valor ${info.student ? 'precio-valor-tachado' : ''}">${info.original.formatted}</span>
                </div>`
            );
        }
        
        return sections.join('');
    }
    
    showLoading(show) {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.style.display = show ? 'block' : 'none';
        }
    }
    
    showSuccess(message) {
        this.showToast(message, 'success');
    }
    
    showError(message) {
        this.showToast(message, 'error');
    }
    
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const messageEl = document.getElementById('toastMessage');
        
        if (toast && messageEl) {
            messageEl.textContent = message;
            toast.className = `toast toast-${type}`;
            toast.style.display = 'block';
            
            setTimeout(() => {
                toast.style.display = 'none';
            }, 3000);
        }
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    new MarketApp();
});
