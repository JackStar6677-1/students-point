// JavaScript para Cursos Abiertos

let cursos = [];
let cursosFiltrados = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarCursos();
    configurarEventos();
});

// Configurar eventos
function configurarEventos() {
    document.getElementById('btnNuevoCurso').addEventListener('click', mostrarNuevoCurso);
    document.getElementById('etiquetaSelect').addEventListener('input', filtrarCursos);
    document.getElementById('vigenciaSelect').addEventListener('change', filtrarCursos);
    document.getElementById('ordenSelect').addEventListener('change', ordenarCursos);
}

// Cargar cursos
async function cargarCursos() {
    try {
        if (!window.authAPI || !window.authAPI.isAuthenticated()) {
            mostrarError('Debes iniciar sesión para ver los cursos');
            window.location.href = '/login.html';
            return;
        }

        if (!window.coursesAPI) {
            throw new Error('Servicio API de cursos no disponible');
        }

        cursos = await window.coursesAPI.getCourses();
        cursosFiltrados = [...cursos];
        mostrarCursos();
    } catch (error) {
        console.error('Error:', error);
        const errorMsg = error.message || 'Error al cargar los cursos';
        mostrarError(errorMsg);
    }
}

// Filtrar cursos
function filtrarCursos() {
    const etiqueta = document.getElementById('etiquetaSelect').value.toLowerCase();
    const vigencia = document.getElementById('vigenciaSelect').value;

    cursosFiltrados = cursos.filter(curso => {
        const cumpleEtiqueta = !etiqueta || 
            curso.etiquetas.toLowerCase().includes(etiqueta) ||
            curso.titulo.toLowerCase().includes(etiqueta);
        
        let cumpleVigencia = true;
        if (vigencia) {
            const hoy = new Date();
            const inicio = new Date(curso.fecha_inicio);
            const fin = new Date(curso.fecha_fin);
            
            switch (vigencia) {
                case 'vigentes':
                    cumpleVigencia = inicio <= hoy && hoy <= fin;
                    break;
                case 'proximos':
                    cumpleVigencia = inicio > hoy;
                    break;
                case 'finalizados':
                    cumpleVigencia = fin < hoy;
                    break;
            }
        }
        
        return cumpleEtiqueta && cumpleVigencia;
    });

    ordenarCursos();
}

// Ordenar cursos
function ordenarCursos() {
    const orden = document.getElementById('ordenSelect').value;
    
    cursosFiltrados.sort((a, b) => {
        switch (orden) {
            case 'fecha_desc':
                return new Date(b.fecha_inicio) - new Date(a.fecha_inicio);
            case 'fecha_asc':
                return new Date(a.fecha_inicio) - new Date(b.fecha_inicio);
            case 'titulo':
                return a.titulo.localeCompare(b.titulo);
            default:
                return 0;
        }
    });

    mostrarCursos();
}

// Mostrar cursos
function mostrarCursos() {
    const container = document.getElementById('listaCursos');
    
    if (cursosFiltrados.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="bi bi-book"></i>
                    <h3>No hay cursos</h3>
                    <p>No se encontraron cursos para los filtros seleccionados.</p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = cursosFiltrados.map(curso => {
        const vigencia = obtenerVigencia(curso);
        const etiquetas = curso.etiquetas.split(',').map(tag => tag.trim()).filter(tag => tag);
        
        return `
            <div class="col-md-6 col-lg-4">
                <div class="curso-card">
                    <div class="curso-card-header">
                        <h5>${curso.titulo}</h5>
                    </div>
                    <div class="curso-card-body">
                        <div class="curso-etiquetas">
                            ${etiquetas.map(tag => `<span class="curso-etiqueta">${tag}</span>`).join('')}
                        </div>
                        <p class="curso-descripcion">
                            ${curso.descripcion.length > 120 ? 
                                curso.descripcion.substring(0, 120) + '...' : 
                                curso.descripcion}
                        </p>
                        <div class="curso-meta">
                            <div class="curso-fechas">
                                <span><strong>Inicio:</strong> ${new Date(curso.fecha_inicio).toLocaleDateString()}</span>
                                <span><strong>Fin:</strong> ${new Date(curso.fecha_fin).toLocaleDateString()}</span>
                            </div>
                            <span class="curso-vigencia ${vigencia.clase}">${vigencia.texto}</span>
                        </div>
                        <div class="curso-actions">
                            <button class="btn btn-ver-curso" onclick="verCurso(${curso.id})">
                                <i class="bi bi-eye"></i> Ver Detalles
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Obtener estado de vigencia
function obtenerVigencia(curso) {
    const hoy = new Date();
    const inicio = new Date(curso.fecha_inicio);
    const fin = new Date(curso.fecha_fin);
    
    if (inicio > hoy) {
        return { texto: 'Próximo', clase: 'proximo' };
    } else if (fin < hoy) {
        return { texto: 'Finalizado', clase: 'finalizado' };
    } else {
        return { texto: 'Vigente', clase: 'vigente' };
    }
}

// Mostrar modal de nuevo curso
function mostrarNuevoCurso() {
    const modal = new bootstrap.Modal(document.getElementById('nuevoCursoModal'));
    modal.show();
    
    // Establecer fecha mínima como hoy
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('fechaInicioCurso').min = hoy;
    document.getElementById('fechaFinCurso').min = hoy;
}

// Enviar nuevo curso
async function enviarCurso() {
    try {
        if (!window.authAPI || !window.authAPI.isAuthenticated()) {
            mostrarError('Debes iniciar sesión para publicar cursos');
            window.location.href = '/login.html';
            return;
        }

        if (!window.coursesAPI) {
            throw new Error('Servicio API de cursos no disponible');
        }

        const cursoData = {
            titulo: document.getElementById('tituloCurso').value,
            descripcion: document.getElementById('descripcionCurso').value,
            etiquetas: document.getElementById('etiquetasCurso').value,
            url: document.getElementById('urlCurso').value,
            fecha_inicio: document.getElementById('fechaInicioCurso').value,
            fecha_fin: document.getElementById('fechaFinCurso').value,
            visible: true
        };

        await window.coursesAPI.createCourse(cursoData);

        // Cerrar modal y recargar cursos
        const modal = bootstrap.Modal.getInstance(document.getElementById('nuevoCursoModal'));
        modal.hide();
        
        // Limpiar formulario
        document.getElementById('formNuevoCurso').reset();
        
        // Recargar cursos
        await cargarCursos();
        
        // Mostrar mensaje de éxito
        mostrarExito('Curso publicado exitosamente');
    } catch (error) {
        console.error('Error:', error);
        const errorMsg = error.message || 'Error al publicar el curso';
        mostrarError(errorMsg);
    }
}

// Ver curso completo
async function verCurso(id) {
    try {
        if (!window.coursesAPI) {
            throw new Error('Servicio API de cursos no disponible');
        }

        const curso = await window.coursesAPI.getCourse(id);
        const vigencia = obtenerVigencia(curso);
        const etiquetas = curso.etiquetas.split(',').map(tag => tag.trim()).filter(tag => tag);
        
        // Mostrar en modal
        document.getElementById('modalTituloCurso').textContent = curso.titulo;
        const modalContenido = document.getElementById('modalContenidoCurso');
        if (modalContenido) {
            modalContenido.innerHTML = `
            <div class="mb-3">
                <span class="curso-vigencia ${vigencia.clase}">${vigencia.texto}</span>
            </div>
            <div class="mb-3">
                <h6>Etiquetas:</h6>
                <div class="curso-etiquetas">
                    ${etiquetas.map(tag => `<span class="curso-etiqueta">${tag}</span>`).join('')}
                </div>
            </div>
            <div class="mb-3">
                <h6>Descripción:</h6>
                <p>${curso.descripcion}</p>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <h6>Fechas:</h6>
                    <p><strong>Inicio:</strong> ${new Date(curso.fecha_inicio).toLocaleDateString()}</p>
                    <p><strong>Fin:</strong> ${new Date(curso.fecha_fin).toLocaleDateString()}</p>
                </div>
                <div class="col-md-6">
                    <h6>Información:</h6>
                    <p><strong>Publicado por:</strong> ${curso.autor_nombre || 'Usuario'}</p>
                    <p><strong>Fecha de publicación:</strong> ${new Date(curso.created_at).toLocaleDateString()}</p>
                </div>
            </div>
            <div class="mt-3">
                <h6>URL del Curso:</h6>
                <p class="curso-url">${curso.url}</p>
            </div>
        `;
        }

        // Configurar botón de acceso
        const btnAcceder = document.getElementById('btnAccederCurso');
        btnAcceder.href = curso.url;
        btnAcceder.textContent = vigencia.clase === 'finalizado' ? 'Ver Curso (Finalizado)' : 'Acceder al Curso';

        const modal = new bootstrap.Modal(document.getElementById('verCursoModal'));
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        const errorMsg = error.message || 'Error al cargar el curso';
        mostrarError(errorMsg);
    }
}

// Mostrar error
function mostrarError(mensaje) {
    const container = document.getElementById('listaCursos');
    container.innerHTML = `
        <div class="col-12">
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                ${mensaje}
            </div>
        </div>
    `;
}

// Mostrar éxito
function mostrarExito(mensaje) {
    // Crear toast de éxito
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-success border-0';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-check-circle"></i> ${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover del DOM después de que se oculte
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}
