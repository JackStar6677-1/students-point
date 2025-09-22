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
        await this.loadCategorias();
        await this.loadCampus();
        this.loadProductos();
    }
    
    // === AUTENTICACIÓN ===
    async checkAuth() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            this.redirectToLogin();
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/me/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                this.currentUser = await response.json();
                this.updateUIForUser();
            } else {
                this.redirectToLogin();
            }
        } catch (error) {
            console.error('Error verificando autenticación:', error);
            this.redirectToLogin();
        }
    }
    
    redirectToLogin() {
        window.location.href = '/login.html';
    }
    
    updateUIForUser() {
        // Mostrar/ocultar botones según el usuario
        const btnCrear = document.getElementById('btnCrearProducto');
        if (btnCrear) {
            btnCrear.style.display = this.currentUser ? 'block' : 'none';
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
    
    // === CARGA DE DATOS ===
    async loadCategorias() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/market/categorias/`);
            if (response.ok) {
                this.categorias = await response.json();
                this.populateCategorias();
            }
        } catch (error) {
            console.error('Error cargando categorías:', error);
        }
    }
    
    async loadCampus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/sedes/`);
            if (response.ok) {
                this.campus = await response.json();
                this.populateCampus();
            }
        } catch (error) {
            console.error('Error cargando campus:', error);
        }
    }
    
    async loadProductos() {
        this.showLoading(true);
        
        try {
            const params = new URLSearchParams(this.filtros);
            const response = await fetch(`${this.apiBaseUrl}/market/productos/?${params}`);
            
            if (response.ok) {
                this.productos = await response.json();
                this.renderProductos();
            } else {
                this.showError('Error cargando productos');
            }
        } catch (error) {
            console.error('Error cargando productos:', error);
            this.showError('Error de conexión');
        } finally {
            this.showLoading(false);
        }
    }
    
    // === RENDERIZADO ===
    populateCategorias() {
        const select = document.getElementById('filtroCategoria');
        const selectCrear = document.getElementById('inputCategoria');
        
        if (select) {
            select.innerHTML = '<option value="">Todas</option>';
            this.categorias.forEach(cat => {
                select.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
            });
        }
        
        if (selectCrear) {
            selectCrear.innerHTML = '<option value="">Seleccionar categoría</option>';
            this.categorias.forEach(cat => {
                selectCrear.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
            });
        }
    }
    
    populateCampus() {
        const select = document.getElementById('filtroCampus');
        
        if (select) {
            select.innerHTML = '<option value="">Todos</option>';
            this.campus.forEach(campus => {
                select.innerHTML += `<option value="${campus.slug}">${campus.nombre}</option>`;
            });
        }
    }
    
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
                    ${producto.og_image ? 
                        `<img src="${producto.og_image}" alt="${producto.titulo}" loading="lazy">` :
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
                        ${producto.precio ? 
                            `<span class="producto-precio">$${this.formatPrice(producto.precio)} ${producto.moneda}</span>` :
                            '<span class="producto-precio">Precio a consultar</span>'
                        }
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
    }
    
    showMisProductos() {
        this.filtros = { mis_productos: true };
        this.loadProductos();
    }
    
    showFavoritos() {
        this.filtros = { favoritos: true };
        this.loadProductos();
    }
    
    async verProducto(id) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/market/productos/${id}/`);
            if (response.ok) {
                this.productoActual = await response.json();
                this.renderProductoModal();
                document.getElementById('modalVerProducto').style.display = 'block';
            }
        } catch (error) {
            console.error('Error cargando producto:', error);
            this.showError('Error cargando producto');
        }
    }
    
    renderProductoModal() {
        const producto = this.productoActual;
        
        document.getElementById('modalTitulo').textContent = producto.titulo;
        
        const detalle = document.getElementById('productoDetalle');
        detalle.innerHTML = `
            <div class="producto-modal-imagen">
                ${producto.og_image ? 
                    `<img src="${producto.og_image}" alt="${producto.titulo}">` :
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
                
                ${producto.precio ? `
                    <div class="producto-precio-modal">
                        <h4>Precio</h4>
                        <span class="precio">$${this.formatPrice(producto.precio)} ${producto.moneda}</span>
                    </div>
                ` : ''}
                
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
        
        const formData = {
            titulo: document.getElementById('inputTitulo').value,
            descripcion: document.getElementById('inputDescripcion').value,
            categoria: document.getElementById('inputCategoria').value,
            tipo_enlace: document.getElementById('inputTipoEnlace').value,
            url_principal: document.getElementById('inputUrlPrincipal').value,
            precio: document.getElementById('inputPrecio').value || null,
            moneda: document.getElementById('inputMoneda').value
        };
        
        // Procesar URLs adicionales
        const urlsAdicionales = document.getElementById('inputUrlsAdicionales').value
            .split('\n')
            .map(url => url.trim())
            .filter(url => url);
        
        if (urlsAdicionales.length > 0) {
            formData.urls_adicionales = urlsAdicionales;
        }
        
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`${this.apiBaseUrl}/market/productos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                this.showSuccess('Producto publicado exitosamente');
                this.closeModal();
                document.getElementById('formCrearProducto').reset();
                this.loadProductos();
            } else {
                const error = await response.json();
                this.showError(error.detail || 'Error publicando producto');
            }
        } catch (error) {
            console.error('Error creando producto:', error);
            this.showError('Error de conexión');
        }
    }
    
    async toggleFavorito(id) {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`${this.apiBaseUrl}/market/productos/${id}/toggle_favorito/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.showSuccess(data.es_favorito ? 'Agregado a favoritos' : 'Removido de favoritos');
                this.loadProductos(); // Recargar para actualizar UI
            }
        } catch (error) {
            console.error('Error toggle favorito:', error);
            this.showError('Error actualizando favoritos');
        }
    }
    
    async registrarClick(id) {
        try {
            const token = localStorage.getItem('access_token');
            await fetch(`${this.apiBaseUrl}/market/productos/${id}/registrar_click/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
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
            const token = localStorage.getItem('access_token');
            const response = await fetch(`${this.apiBaseUrl}/market/reportes/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                this.showSuccess('Reporte enviado exitosamente');
                this.closeModal();
                document.getElementById('formReportar').reset();
            } else {
                const error = await response.json();
                this.showError(error.detail || 'Error enviando reporte');
            }
        } catch (error) {
            console.error('Error reportando producto:', error);
            this.showError('Error de conexión');
        }
    }
    
    // === UTILIDADES ===
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    formatPrice(price) {
        return new Intl.NumberFormat('es-CL').format(price);
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
