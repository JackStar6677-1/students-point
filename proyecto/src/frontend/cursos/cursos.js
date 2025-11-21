// Cursos - StudentsPoint

let cursos = [];
let cursosOriginal = [];

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    cargarEstadisticas();
    cargarCursos();
    
    // Configurar event listener para pausar videos al cerrar el modal
    const modalDetalleCurso = document.getElementById('detalleCursoModal');
    if (modalDetalleCurso) {
        modalDetalleCurso.addEventListener('hidden.bs.modal', function () {
            // Pausar todos los videos cuando se cierra el modal
            const videos = this.querySelectorAll('video.curso-video-player');
            videos.forEach(video => {
                video.pause();
                video.currentTime = 0;
            });
        });
    }
});

// Autenticacion
function initAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
}

// Cargar estadisticas
async function cargarEstadisticas() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/cursos/estadisticas/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('totalCursos').textContent = stats.total_cursos || 0;
            document.getElementById('cursosPersonales').textContent = stats.cursos_personales || 0;
            document.getElementById('cursosExternos').textContent = stats.cursos_externos || 0;
            document.getElementById('cursosGratuitos').textContent = stats.cursos_gratuitos || 0;
        } else {
            console.error('Error cargando estadisticas:', response.status);
        }
    } catch (error) {
        console.error('Error cargando estadisticas:', error);
    }
}

// Cargar cursos
async function cargarCursos() {
    try {
        const token = localStorage.getItem('access_token');
        
        // Construir URL - mostrar todos los cursos
        let url = '/api/cursos/';
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            let data = await response.json();
            console.log('Respuesta de la API:', data);
            
            // Verificar si la respuesta tiene paginación (results) o es un array directo
            if (data.results) {
                // Respuesta con paginación
                cursos = data.results;
            } else if (Array.isArray(data)) {
                // Respuesta es un array directo
                cursos = data;
            } else {
                console.error('Formato de respuesta inesperado:', data);
                mostrarError('Formato de respuesta inesperado del servidor');
                return;
            }
            
            cursosOriginal = [...cursos];
            console.log('Cursos cargados:', cursos.length);
            renderizarCursos(cursos);
        } else {
            const errorText = await response.text();
            console.error('Error del servidor:', response.status, errorText);
            mostrarError('Error al cargar los cursos: ' + response.status);
        }
    } catch (error) {
        console.error('Error cargando cursos:', error);
        mostrarError('Error de conexion al cargar cursos: ' + error.message);
    }
}

// Renderizar cursos
function renderizarCursos(cursosArray) {
    const container = document.getElementById('cursosContainer');
    
    if (cursosArray.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="fas fa-graduation-cap fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No se encontraron cursos</h4>
                <p class="text-muted">Intenta ajustar los filtros de busqueda</p>
            </div>
        `;
        return;
    }
    
    const cursosHTML = cursosArray.map(curso => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="glass p-3 h-100 course-card" style="cursor: pointer;" onclick="verDetalleCurso(${curso.id})">
                ${curso.imagen_url ? `
                    <img src="${curso.imagen_url}" class="w-100 rounded mb-3" style="height: 200px; object-fit: cover;" alt="${curso.titulo}">
                ` : `
                    <div class="w-100 rounded mb-3 d-flex align-items-center justify-content-center bg-dark" style="height: 200px;">
                        <i class="fas fa-graduation-cap fa-4x text-muted"></i>
                    </div>
                `}
                
                <div class="mb-2">
                    <span class="badge ${curso.tipo === 'personal' ? 'bg-purple' : curso.tipo === 'video' ? 'bg-success' : 'bg-primary'}">
                        ${curso.tipo_display}
                    </span>
                    <span class="badge bg-secondary">${curso.nivel_display}</span>
                    <span class="badge bg-info">${curso.modalidad_display}</span>
                </div>
                
                <h5 class="mb-2">${curso.titulo}</h5>
                <p class="text-muted small mb-2" style="height: 60px; overflow: hidden;">
                    ${curso.descripcion.substring(0, 100)}${curso.descripcion.length > 100 ? '...' : ''}
                </p>
                
                <div class="mb-2">
                    <span class="badge bg-dark">${curso.categoria}</span>
                </div>
                
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <i class="fas fa-user text-muted"></i>
                        <small class="text-muted">${curso.autor_nombre}</small>
                    </div>
                    <div>
                        <i class="fas fa-eye text-muted"></i>
                        <small class="text-muted">${curso.visualizaciones}</small>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center">
                    <h4 class="mb-0 ${curso.precio_formateado === 'Gratuito' ? 'text-success' : 'text-warning'}">
                        ${curso.precio_formateado}
                    </h4>
                    <button class="btn btn-sm btn-gradient-gold" onclick="event.stopPropagation(); verDetalleCurso(${curso.id})">
                        Ver mas
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = cursosHTML;
}

// Filtrar cursos
function filtrarCursos() {
    let cursosFiltrados = [...cursosOriginal];
    
    // Filtro por busqueda
    const search = document.getElementById('searchInput').value.toLowerCase();
    if (search) {
        cursosFiltrados = cursosFiltrados.filter(curso => 
            curso.titulo.toLowerCase().includes(search) ||
            curso.descripcion.toLowerCase().includes(search) ||
            curso.categoria.toLowerCase().includes(search)
        );
    }
    
    // Filtro por tipo
    const tipo = document.getElementById('filtroTipo').value;
    if (tipo) {
        cursosFiltrados = cursosFiltrados.filter(curso => curso.tipo === tipo);
    }
    
    // Filtro por modalidad
    const modalidad = document.getElementById('filtroModalidad').value;
    if (modalidad) {
        cursosFiltrados = cursosFiltrados.filter(curso => curso.modalidad === modalidad);
    }
    
    // Filtro por nivel
    const nivel = document.getElementById('filtroNivel').value;
    if (nivel) {
        cursosFiltrados = cursosFiltrados.filter(curso => curso.nivel === nivel);
    }
    
    // Ordenamiento
    const orden = document.getElementById('filtroOrden').value;
    cursosFiltrados.sort((a, b) => {
        if (orden === 'precio') return (a.precio || 0) - (b.precio || 0);
        if (orden === '-precio') return (b.precio || 0) - (a.precio || 0);
        if (orden === '-visualizaciones') return b.visualizaciones - a.visualizaciones;
        return 0;
    });
    
    renderizarCursos(cursosFiltrados);
}

// Ver detalle del curso
async function verDetalleCurso(id) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/cursos/${id}/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const curso = await response.json();
            mostrarDetalleCurso(curso);
        }
    } catch (error) {
        console.error('Error cargando detalle:', error);
        mostrarError('Error al cargar el detalle del curso');
    }
}

// Mostrar detalle del curso
function mostrarDetalleCurso(curso) {
    document.getElementById('detalletitulo').textContent = curso.titulo;
    
    let contactoHTML = '';
    let clasesHTML = '';
    
    if (curso.tipo === 'personal') {
        contactoHTML = `
            <div class="alert alert-info">
                <h6><i class="fas fa-address-book"></i> Informacion de Contacto</h6>
                ${curso.email_contacto ? `<p class="mb-1"><i class="fas fa-envelope"></i> ${curso.email_contacto}</p>` : ''}
                ${curso.telefono_contacto ? `<p class="mb-1"><i class="fas fa-phone"></i> ${curso.telefono_contacto}</p>` : ''}
                ${curso.url ? `<p class="mb-0"><i class="fas fa-link"></i> <a href="${curso.url}" target="_blank">Enlace de contacto</a></p>` : ''}
            </div>
        `;
    } else if (curso.tipo === 'video') {
        // Mostrar clases de video
        if (curso.clases_video && curso.clases_video.length > 0) {
            clasesHTML = `
                <div class="mb-3">
                    <h5><i class="fas fa-video"></i> Clases del Curso</h5>
                    <div class="list-group">
                        ${curso.clases_video.map((clase, index) => `
                            <div class="list-group-item">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        <h6 class="mb-1">Clase ${clase.numero_clase}: ${clase.titulo}</h6>
                                        ${clase.descripcion ? `<p class="mb-2 text-muted small">${clase.descripcion}</p>` : ''}
                                        <video controls preload="metadata" class="w-100 mt-2 curso-video-player" style="max-height: 400px;">
                                            <source src="${clase.video_url}" type="video/mp4">
                                            Tu navegador no soporta la reproduccion de videos.
                                        </video>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            clasesHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-info-circle"></i> Este curso aun no tiene clases agregadas.
                </div>
            `;
        }
        
        // Boton para gestionar clases (solo si es el autor)
        // Nota: En una implementación completa, se debería verificar desde el backend
        // Por ahora, permitimos que cualquier usuario autenticado gestione (se validará en backend)
        contactoHTML = `
            <button class="btn btn-gradient-purple w-100 mb-3" onclick="gestionarClases(${curso.id})">
                <i class="fas fa-video"></i> Gestionar Clases
            </button>
        `;
    } else {
        contactoHTML = curso.url ? `
            <a href="${curso.url}" target="_blank" class="btn btn-gradient-gold w-100 mb-3">
                <i class="fas fa-external-link-alt"></i> Ir al curso
            </a>
        ` : '';
    }
    
    const detalleHTML = `
        ${curso.imagen_url ? `
            <img src="${curso.imagen_url}" class="w-100 rounded mb-3" alt="${curso.titulo}">
        ` : ''}
        
        <div class="mb-3">
            <span class="badge ${curso.tipo === 'personal' ? 'bg-purple' : 'bg-primary'}">${curso.tipo_display}</span>
            <span class="badge bg-secondary">${curso.nivel_display}</span>
            <span class="badge bg-info">${curso.modalidad_display}</span>
            <span class="badge bg-dark">${curso.categoria}</span>
        </div>
        
        <h5 class="mb-3">Descripcion</h5>
        <p class="text-muted mb-3">${curso.descripcion}</p>
        
        <div class="row mb-3">
            <div class="col-md-6">
                <p class="mb-2"><i class="fas fa-user"></i> <strong>Autor:</strong> ${curso.autor_nombre}</p>
                <p class="mb-2"><i class="fas fa-clock"></i> <strong>Duracion:</strong> ${curso.duracion || 'No especificada'}</p>
            </div>
            <div class="col-md-6">
                <p class="mb-2"><i class="fas fa-tag"></i> <strong>Precio:</strong> <span class="${curso.precio_formateado === 'Gratuito' ? 'text-success' : 'text-warning'}">${curso.precio_formateado}</span></p>
                <p class="mb-2"><i class="fas fa-eye"></i> <strong>Visualizaciones:</strong> ${curso.visualizaciones}</p>
            </div>
        </div>
        
        ${curso.etiquetas ? `
            <div class="mb-3">
                <p class="mb-2"><strong>Etiquetas:</strong></p>
                ${curso.etiquetas.split(',').map(tag => `<span class="badge bg-secondary me-1">${tag.trim()}</span>`).join('')}
            </div>
        ` : ''}
        
        ${contactoHTML}
        ${clasesHTML}
    `;
    
    document.getElementById('detalleBody').innerHTML = detalleHTML;
    new bootstrap.Modal(document.getElementById('detalleCursoModal')).show();
}

// Gestionar clases de video
async function gestionarClases(cursoId) {
    document.getElementById('cursoIdClase').value = cursoId;
    
    // Cargar clases existentes
    await cargarClases(cursoId);
    
    // Mostrar modal
    new bootstrap.Modal(document.getElementById('gestionarClasesModal')).show();
}

// Cargar clases de un curso
async function cargarClases(cursoId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/clases-video/?curso_id=${cursoId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error del servidor:', response.status, errorText);
            mostrarError('Error al cargar las clases');
            return;
        }
        
        let data = await response.json();
        
        // Manejar diferentes formatos de respuesta
        let clases = [];
        if (Array.isArray(data)) {
            clases = data;
        } else if (data.results && Array.isArray(data.results)) {
            clases = data.results;
        } else if (data.error) {
            mostrarError(data.error);
            return;
        }
        
        const container = document.getElementById('clasesContainer');
        
        if (clases.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Aun no hay clases agregadas. Agrega la primera clase abajo.
                </div>
            `;
        } else {
            container.innerHTML = `
                <h6>Clases Existentes (${clases.length})</h6>
                <div class="list-group mb-3">
                    ${clases.map(clase => `
                        <div class="list-group-item">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <h6 class="mb-1">Clase ${clase.numero_clase}: ${clase.titulo}</h6>
                                    ${clase.descripcion ? `<p class="mb-1 text-muted small">${clase.descripcion}</p>` : ''}
                                    <small class="text-muted">Orden: ${clase.orden}</small>
                                </div>
                                <button class="btn btn-sm btn-danger" onclick="eliminarClase(${clase.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error cargando clases:', error);
        mostrarError('Error de conexion al cargar clases: ' + error.message);
    }
}

// Agregar nueva clase
async function agregarClase() {
    const cursoId = document.getElementById('cursoIdClase').value;
    const numeroClase = document.getElementById('numeroClase').value;
    const titulo = document.getElementById('tituloClase').value;
    const descripcion = document.getElementById('descripcionClase').value;
    const video = document.getElementById('videoClase').files[0];
    const orden = document.getElementById('ordenClase').value || 0;
    
    if (!video) {
        mostrarError('Debes seleccionar un archivo de video');
        return;
    }
    
    if (!numeroClase || !titulo) {
        mostrarError('Debes completar el numero de clase y el titulo');
        return;
    }
    
    const formData = new FormData();
    formData.append('curso', cursoId);
    formData.append('numero_clase', numeroClase);
    formData.append('titulo', titulo);
    if (descripcion) {
        formData.append('descripcion', descripcion);
    }
    formData.append('video', video);
    formData.append('orden', orden);
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/clases-video/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
                // NO incluir Content-Type para FormData, el navegador lo hace automáticamente
            },
            body: formData
        });
        
        if (!response.ok) {
            // Intentar leer el error como JSON, si falla usar el texto
            let errorMsg = 'Error al agregar la clase';
            try {
                const errorData = await response.json();
                if (errorData.error) {
                    errorMsg = errorData.error;
                } else if (typeof errorData === 'object') {
                    errorMsg = Object.values(errorData).flat().join(', ');
                }
            } catch (e) {
                const errorText = await response.text();
                if (errorText && !errorText.startsWith('<!DOCTYPE')) {
                    errorMsg = errorText.substring(0, 200);
                }
            }
            mostrarError(errorMsg);
            return;
        }
        
        mostrarExito('Clase agregada exitosamente');
        document.getElementById('formNuevaClase').reset();
        document.getElementById('cursoIdClase').value = cursoId;
        await cargarClases(cursoId);
    } catch (error) {
        console.error('Error agregando clase:', error);
        mostrarError('Error de conexion al agregar la clase: ' + error.message);
    }
}

// Eliminar clase
async function eliminarClase(claseId) {
    if (!confirm('¿Estas seguro de eliminar esta clase?')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/clases-video/${claseId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            mostrarExito('Clase eliminada exitosamente');
            const cursoId = document.getElementById('cursoIdClase').value;
            await cargarClases(cursoId);
        } else {
            mostrarError('Error al eliminar la clase');
        }
    } catch (error) {
        console.error('Error eliminando clase:', error);
        mostrarError('Error de conexion al eliminar la clase');
    }
}

// Publicar curso
async function publicarCurso() {
    const tipo = document.getElementById('tipoCurso').value;
    const esGratuito = document.getElementById('esGratuito').checked;
    
    // Validar campos requeridos segun tipo
    if (tipo === 'externo') {
        const url = document.getElementById('urlCurso').value;
        if (!url) {
            mostrarError('Debes proporcionar la URL del curso externo');
            return;
        }
    } else if (tipo === 'personal') {
        const email = document.getElementById('emailContacto').value;
        const telefono = document.getElementById('telefonoContacto').value;
        const urlContacto = document.getElementById('urlContacto').value;
        
        if (!email && !telefono && !urlContacto) {
            mostrarError('Debes proporcionar al menos un medio de contacto');
            return;
        }
    } else if (tipo === 'video') {
        // Los cursos con videos deben ser gratuitos
        if (!esGratuito) {
            mostrarError('Los cursos con videos deben ser gratuitos');
            return;
        }
    }
    
    // Si es curso con videos, forzar que sea gratuito
    const esGratuitoFinal = tipo === 'video' ? true : esGratuito;
    
    const cursoData = {
        tipo: tipo,
        titulo: document.getElementById('tituloCurso').value,
        descripcion: document.getElementById('descripcionCurso').value,
        categoria: document.getElementById('categoriaCurso').value,
        etiquetas: document.getElementById('etiquetasCurso').value,
        modalidad: document.getElementById('modalidadCurso').value,
        nivel: document.getElementById('nivelCurso').value,
        duracion: document.getElementById('duracionCurso').value,
        es_gratuito: esGratuitoFinal,
        precio: esGratuitoFinal ? null : document.getElementById('precioCurso').value || null,
        url: tipo === 'externo' ? document.getElementById('urlCurso').value : (tipo === 'personal' ? document.getElementById('urlContacto').value : ''),
        email_contacto: tipo === 'personal' ? document.getElementById('emailContacto').value : '',
        telefono_contacto: tipo === 'personal' ? document.getElementById('telefonoContacto').value : '',
        imagen_url: document.getElementById('imagenCurso').value
    };
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/api/cursos/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cursoData)
        });
        
        if (response.ok) {
            const cursoCreado = await response.json();
            mostrarExito('Curso publicado exitosamente');
            
            // Cerrar modal correctamente
            const modalElement = document.getElementById('nuevoCursoModal');
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modal.hide();
            }
            
            // Limpiar formulario
            document.getElementById('formNuevoCurso').reset();
            
            // Remover backdrop manualmente (fix para el problema de oscurecimiento)
            setTimeout(() => {
                document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                document.body.style.paddingRight = '';
            }, 100);
            
            // Si es curso con videos, abrir modal para gestionar clases
            if (tipo === 'video') {
                setTimeout(() => {
                    gestionarClases(cursoCreado.id);
                }, 500);
            }
            
            // Recargar datos
            cargarCursos();
            cargarEstadisticas();
        } else {
            const error = await response.json();
            const errorMsg = Object.values(error).flat().join(', ');
            mostrarError(errorMsg || 'Error al publicar el curso');
        }
    } catch (error) {
        console.error('Error publicando curso:', error);
        mostrarError('Error de conexion al publicar el curso');
    }
}

// Toggle campos segun tipo
function toggleCamposTipo() {
    const tipo = document.getElementById('tipoCurso').value;
    document.getElementById('camposExterno').style.display = tipo === 'externo' ? 'block' : 'none';
    document.getElementById('camposPersonal').style.display = tipo === 'personal' ? 'block' : 'none';
    document.getElementById('camposVideo').style.display = tipo === 'video' ? 'block' : 'none';
    
    // Si es curso con videos, forzar que sea gratuito
    if (tipo === 'video') {
        document.getElementById('esGratuito').checked = true;
        document.getElementById('campoPrecio').style.display = 'none';
        document.getElementById('precioCurso').value = '';
    }
}

// Toggle precio
function togglePrecio() {
    const esGratuito = document.getElementById('esGratuito').checked;
    document.getElementById('campoPrecio').style.display = esGratuito ? 'none' : 'block';
    if (esGratuito) {
        document.getElementById('precioCurso').value = '';
    }
}

// Mostrar mensajes
function mostrarError(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function mostrarExito(mensaje) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login.html';
}
