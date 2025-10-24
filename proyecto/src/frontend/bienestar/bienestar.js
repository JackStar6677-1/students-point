// JavaScript para Bienestar Estudiantil

let contenidoBienestar = [];
let contenidoFiltrado = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarContenidoBienestar();
    configurarEventos();
});

// Configurar eventos
function configurarEventos() {
    document.getElementById('carreraSelect').addEventListener('change', filtrarContenido);
    document.getElementById('tipoSelect').addEventListener('change', filtrarContenido);
}

// Cargar contenido de bienestar
async function cargarContenidoBienestar() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            mostrarError('Debes iniciar sesión para acceder al contenido de bienestar');
            return;
        }

        const response = await fetch('/api/bienestar/bienestar', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error al cargar contenido de bienestar');
        }

        const data = await response.json();
        contenidoBienestar = data.results || data;
        contenidoFiltrado = [...contenidoBienestar];
        mostrarContenido();
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al cargar el contenido de bienestar');
    }
}

// Filtrar contenido
function filtrarContenido() {
    const carrera = document.getElementById('carreraSelect').value;
    const tipo = document.getElementById('tipoSelect').value;

    contenidoFiltrado = contenidoBienestar.filter(item => {
        const cumpleCarrera = !carrera || item.carrera.toLowerCase().includes(carrera.toLowerCase());
        const cumpleTipo = !tipo || item.tipo === tipo;
        return cumpleCarrera && cumpleTipo;
    });

    mostrarContenido();
}

// Mostrar contenido
function mostrarContenido() {
    const container = document.getElementById('contenidoBienestar');
    
    if (contenidoFiltrado.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="bi bi-heart-pulse"></i>
                    <h3>No hay contenido disponible</h3>
                    <p>No se encontró contenido de bienestar para los filtros seleccionados.</p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = contenidoFiltrado.map(item => `
        <div class="col-md-6 col-lg-4">
            <div class="bienestar-card">
                <div class="bienestar-card-header">
                    <h5>${item.titulo}</h5>
                </div>
                <div class="bienestar-card-body">
                    <span class="bienestar-tipo ${item.tipo}">
                        ${item.tipo === 'kine' ? 'Kinesiología' : 'Psicología'}
                    </span>
                    <p class="bienestar-descripcion">
                        ${item.descripcion || 'Contenido de bienestar para estudiantes.'}
                    </p>
                    <div class="bienestar-actions">
                        <button class="btn btn-ver-contenido" onclick="verContenido(${item.id})">
                            <i class="bi bi-eye"></i> Ver Contenido
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Ver contenido completo
async function verContenido(id) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/bienestar/bienestar/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Error al cargar el contenido');
        }

        const item = await response.json();
        
        // Mostrar en modal
        document.getElementById('modalTitulo').textContent = item.titulo;
        const modalContenido = document.getElementById('modalContenido');
        if (modalContenido) {
            modalContenido.innerHTML = `
            <div class="mb-3">
                <span class="bienestar-tipo ${item.tipo}">
                    ${item.tipo === 'kine' ? 'Kinesiología' : 'Psicología'}
                </span>
            </div>
            <div class="contenido-completo">
                ${item.contenido_html || item.contenido_md || 'Contenido no disponible'}
            </div>
            ${item.media_url ? `
                <div class="mt-3">
                    <h6>Recurso Multimedia:</h6>
                    <a href="${item.media_url}" target="_blank" class="btn btn-outline-primary">
                        <i class="bi bi-play-circle"></i> Ver Recurso
                    </a>
                </div>
            ` : ''}
        `;
        }

        const modal = new bootstrap.Modal(document.getElementById('contenidoModal'));
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error al cargar el contenido');
    }
}

// Mostrar error
function mostrarError(mensaje) {
    const container = document.getElementById('contenidoBienestar');
    container.innerHTML = `
        <div class="col-12">
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                ${mensaje}
            </div>
        </div>
    `;
}

// Mostrar loading
function mostrarLoading() {
    const container = document.getElementById('contenidoBienestar');
    container.innerHTML = `
        <div class="col-12">
            <div class="loading-spinner">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando contenido de bienestar...</p>
            </div>
        </div>
    `;
}
