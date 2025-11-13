/**
 * RECORRIDOS VIRTUALES - STUDENTSPOINT
 * Sistema de navegación con diapositivas para recorridos virtuales
 */

// ========================================
// VARIABLES GLOBALES
// ========================================

let currentSlide = 0;
let totalSlides = 0;
let currentRecorrido = null;
let touchStartX = 0;
let touchEndX = 0;

// Datos de recorridos disponibles
const recorridosData = {
    'maipu': {
        nombre: 'DuocUC Sede Maipú',
        recorridos: [
            {
                id: 'biblioteca',
                titulo: 'Biblioteca',
                descripcion: 'Explora nuestra biblioteca con recursos académicos',
                icono: 'fa-book',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/biblioteca/img1biblioteca.jpeg',
                        titulo: 'Entrada a la Biblioteca',
                        descripcion: 'Vista principal de la entrada a la biblioteca DuocUC'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img2biblioteca.jpeg',
                        titulo: 'Zona de Recepción',
                        descripcion: 'Área de recepción y atención al usuario'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img3biblioteca.jpeg',
                        titulo: 'Sala de Lectura',
                        descripcion: 'Amplio espacio de estudio y lectura silenciosa'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img4biblioteca.jpeg',
                        titulo: 'Estantería de Libros',
                        descripcion: 'Colección de libros y material bibliográfico'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img5biblioteca.jpeg',
                        titulo: 'Zona de Computadores',
                        descripcion: 'Área equipada con computadores para investigación'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img6biblioteca.jpeg',
                        titulo: 'Salas de Estudio Grupal',
                        descripcion: 'Espacios para trabajo colaborativo y en equipo'
                    },
                    {
                        url: '/imagenes/mapa/biblioteca/img7biblioteca.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica de la biblioteca completa'
                    }
                ]
            },
            {
                id: 'casino',
                titulo: 'Casino',
                descripcion: 'Recorrido por el casino y espacios de alimentación',
                icono: 'fa-utensils',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/casino/img1casino.jpeg',
                        titulo: 'Entrada al Casino',
                        descripcion: 'Vista principal de la entrada al casino estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/casino/img2casino.jpeg',
                        titulo: 'Área de Servicio',
                        descripcion: 'Zona de servicio y atención del casino'
                    },
                    {
                        url: '/imagenes/mapa/casino/img3casino.jpeg',
                        titulo: 'Comedor Principal',
                        descripcion: 'Amplio espacio del comedor para estudiantes'
                    },
                    {
                        url: '/imagenes/mapa/casino/img4casino.jpeg',
                        titulo: 'Zona de Mesas',
                        descripcion: 'Área de mesas y asientos para disfrutar tus alimentos'
                    },
                    {
                        url: '/imagenes/mapa/casino/img5casino.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica del casino estudiantil'
                    }
                ]
            },
            {
                id: 'administracion',
                titulo: 'Administración',
                descripcion: 'Conoce las oficinas administrativas',
                icono: 'fa-building',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/administracion/img1administracion.jpeg',
                        titulo: 'Entrada a Administración',
                        descripcion: 'Vista principal de la entrada a las oficinas administrativas'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img2administracion.jpeg',
                        titulo: 'Recepción Administrativa',
                        descripcion: 'Área de recepción y atención al público'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img3administracion.jpeg',
                        titulo: 'Oficinas Administrativas',
                        descripcion: 'Espacios de trabajo del personal administrativo'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img4administracion.jpeg',
                        titulo: 'Sala de Reuniones',
                        descripcion: 'Espacio para reuniones y sesiones administrativas'
                    },
                    {
                        url: '/imagenes/mapa/administracion/img5administracion.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica de las oficinas administrativas'
                    }
                ]
            },
            {
                id: 'banos',
                titulo: 'Baños',
                descripcion: 'Ubicación de baños por piso',
                icono: 'fa-restroom',
                disponible: false,
                tieneSubmenu: true,
                submenu: [
                    { id: 'banos-piso1', titulo: 'Baños Primer Piso', descripcion: 'Ubicación de baños en el primer piso' },
                    { id: 'banos-piso2', titulo: 'Baños Segundo Piso', descripcion: 'Ubicación de baños en el segundo piso' },
                    { id: 'banos-piso3', titulo: 'Baños Tercer Piso', descripcion: 'Ubicación de baños en el tercer piso' },
                    { id: 'banos-piso4', titulo: 'Baños Cuarto Piso', descripcion: 'Ubicación de baños en el cuarto piso' },
                    { id: 'banos-subterraneo', titulo: 'Baños Subterráneo', descripcion: 'Ubicación de baños en el subterráneo' }
                ]
            },
            {
                id: 'punto-estudiantil',
                titulo: 'Punto Estudiantil',
                descripcion: 'Centro de atención y servicios estudiantiles',
                icono: 'fa-info-circle',
                disponible: true,
                imagenes: [
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img1puntoestudiantil.jpeg',
                        titulo: 'Entrada al Punto Estudiantil',
                        descripcion: 'Vista principal del acceso al centro de atención estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img2puntoestudiantil.jpeg',
                        titulo: 'Área de Atención',
                        descripcion: 'Zona de recepción y atención personalizada para estudiantes'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img3puntoestudiantil.jpeg',
                        titulo: 'Servicios Estudiantiles',
                        descripcion: 'Espacio de servicios y asesoría para la comunidad estudiantil'
                    },
                    {
                        url: '/imagenes/mapa/puntoestudiantil/img4puntoestudiantil.jpeg',
                        titulo: 'Vista General',
                        descripcion: 'Vista panorámica del punto de servicios estudiantiles'
                    }
                ]
            },
            {
                id: 'salas',
                titulo: 'Salas',
                descripcion: 'Recorrido por salas de clases',
                icono: 'fa-chalkboard-teacher',
                disponible: false,
                imagenes: []
            }
        ]
    }
};

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Reproducir sonido de carga si está disponible
        if (window.playSound) {
        setTimeout(() => window.playSound('pageLoad'), 500);
    }

    // Habilitar selector de sede
    const sedeSelect = document.getElementById('sede-select');
    if (sedeSelect) {
        sedeSelect.addEventListener('change', function() {
            const loadBtn = document.getElementById('load-btn');
            if (loadBtn) {
                loadBtn.disabled = !this.value;
            }
        });
    }
}

function setupEventListeners() {
    // Navegación con teclado
    document.addEventListener('keydown', handleKeyPress);

    // Touch events para swipe
    const slideContainer = document.getElementById('slideshow-container');
    if (slideContainer) {
        slideContainer.addEventListener('touchstart', handleTouchStart, { passive: true });
        slideContainer.addEventListener('touchend', handleTouchEnd, { passive: true });
    }
}

// ========================================
// NAVEGACIÓN PRINCIPAL
// ========================================

function loadRecorridos() {
    const sedeSelect = document.getElementById('sede-select');
    const sedeValue = sedeSelect.value;

    if (!sedeValue) return;

    const sedeData = recorridosData[sedeValue];
    if (!sedeData) return;

    // Actualizar título
    document.getElementById('sede-title').textContent = `Recorridos Disponibles - ${sedeData.nombre}`;

    // Renderizar cards de recorridos
    renderRecorridosCards(sedeData.recorridos);

    // Cambiar vista
    document.getElementById('sede-selector').style.display = 'none';
    document.getElementById('recorridos-container').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function renderRecorridosCards(recorridos) {
    const container = document.getElementById('recorridos-list');
    container.innerHTML = '';

    recorridos.forEach(recorrido => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        const card = document.createElement('div');
        card.className = `recorrido-card ${!recorrido.disponible ? 'disabled' : ''}`;

        if (recorrido.disponible || recorrido.tieneSubmenu) {
            card.onclick = () => {
                if (recorrido.tieneSubmenu) {
                    showBanosSubmenu(recorrido);
                } else {
                    startSlideshow(recorrido);
                }
            };
        }

        card.innerHTML = `
            <div class="recorrido-icon">
                <i class="fas ${recorrido.icono}"></i>
            </div>
            <h5>${recorrido.titulo}</h5>
            <p>${recorrido.descripcion}</p>
            ${!recorrido.disponible && !recorrido.tieneSubmenu ? '<span class="badge-proximamente">Próximamente</span>' : ''}
        `;

        col.appendChild(card);
        container.appendChild(col);
    });
}

function backToSelector() {
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('sede-selector').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

// ========================================
// SUBMENU DE BAÑOS
// ========================================

function showBanosSubmenu(recorrido) {
    const container = document.getElementById('banos-list');
    container.innerHTML = '';

    recorrido.submenu.forEach(item => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        const card = document.createElement('div');
        card.className = 'recorrido-card disabled';

        card.innerHTML = `
            <div class="recorrido-icon">
                <i class="fas fa-restroom"></i>
                </div>
            <h5>${item.titulo}</h5>
            <p>${item.descripcion}</p>
            <span class="badge-proximamente">Próximamente</span>
        `;

        col.appendChild(card);
        container.appendChild(col);
    });

    // Cambiar vista
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('banos-submenu').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function backToRecorridos() {
    document.getElementById('banos-submenu').style.display = 'none';
    document.getElementById('recorridos-container').style.display = 'block';

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

// ========================================
// VISOR DE DIAPOSITIVAS
// ========================================

function startSlideshow(recorrido) {
    if (!recorrido.disponible || !recorrido.imagenes || recorrido.imagenes.length === 0) {
        showNotification('Este recorrido aún no está disponible', 'info');
        return;
    }

    currentRecorrido = recorrido;
    totalSlides = recorrido.imagenes.length;
    currentSlide = 0;

    // Actualizar información del header
    document.getElementById('slideshow-titulo').textContent = recorrido.titulo;
    document.getElementById('slideshow-subtitulo').textContent = 'DuocUC Sede Maipú';

    // Renderizar slides
    renderSlides();

    // Renderizar dots
    renderDots();

    // Mostrar visor
    document.getElementById('recorridos-container').style.display = 'none';
    document.getElementById('slideshow-container').style.display = 'flex';

    // Actualizar navegación
    updateSlideNavigation();

    // Reproducir sonido
    if (window.playSound) window.playSound('click');

    // Precargar siguiente imagen
    preloadNextImage();
}

function renderSlides() {
    const container = document.getElementById('slide-container');
    container.innerHTML = '';

    currentRecorrido.imagenes.forEach((imagen, index) => {
        const slide = document.createElement('div');
        slide.className = `slide ${index === 0 ? 'active' : ''}`;

        const img = document.createElement('img');
        img.src = imagen.url;
        img.alt = imagen.titulo;
        img.loading = index === 0 ? 'eager' : 'lazy';

        // Agregar título y descripción overlay (opcional para mobile)
        const overlay = document.createElement('div');
        overlay.className = 'slide-overlay';
        overlay.innerHTML = `
            <div class="slide-info">
                <h3>${imagen.titulo}</h3>
                <p>${imagen.descripcion}</p>
            </div>
        `;

        slide.appendChild(img);
        // Descomentar si quieres overlay en las imágenes
        // slide.appendChild(overlay);
        
        container.appendChild(slide);
    });
}

function renderDots() {
    const container = document.getElementById('slideshow-dots');
    container.innerHTML = '';

    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.className = `dot ${i === 0 ? 'active' : ''}`;
        dot.onclick = () => goToSlide(i);
        container.appendChild(dot);
    }
}

function updateSlideNavigation() {
    // Actualizar contador
    document.getElementById('slide-counter').textContent = `${currentSlide + 1} / ${totalSlides}`;

    // Actualizar barra de progreso
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
        
        // Actualizar botones
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;

    // Actualizar dots
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });

    // Actualizar slides
    const slides = document.querySelectorAll('.slide');
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });
}

function nextSlide() {
    if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlideNavigation();
        preloadNextImage();
        if (window.playSound) window.playSound('navigate');
    }
}

function previousSlide() {
    if (currentSlide > 0) {
        currentSlide--;
        updateSlideNavigation();
        if (window.playSound) window.playSound('navigate');
    }
}

function goToSlide(index) {
    if (index >= 0 && index < totalSlides && index !== currentSlide) {
        currentSlide = index;
        updateSlideNavigation();
        preloadNextImage();
        if (window.playSound) window.playSound('click');
    }
}

function exitSlideshow() {
    document.getElementById('slideshow-container').style.display = 'none';
    
    // Volver a la vista anterior
    if (document.getElementById('banos-submenu').style.display === 'block') {
        // Ya está en submenu
    } else {
        document.getElementById('recorridos-container').style.display = 'block';
    }

    // Limpiar
    currentRecorrido = null;
    currentSlide = 0;
    totalSlides = 0;

    // Reproducir sonido
    if (window.playSound) window.playSound('click');
}

function preloadNextImage() {
    if (currentSlide < totalSlides - 1) {
        const nextImage = new Image();
        nextImage.src = currentRecorrido.imagenes[currentSlide + 1].url;
    }
}

// ========================================
// CONTROLES DE TECLADO
// ========================================

function handleKeyPress(e) {
    // Solo funciona si el visor está activo
    const slideshowContainer = document.getElementById('slideshow-container');
    if (!slideshowContainer || slideshowContainer.style.display === 'none') return;

    switch(e.key) {
        case 'ArrowRight':
        case ' ':
            e.preventDefault();
            nextSlide();
            break;
        case 'ArrowLeft':
            e.preventDefault();
            previousSlide();
            break;
        case 'Escape':
            e.preventDefault();
            exitSlideshow();
            break;
        case 'Home':
            e.preventDefault();
            goToSlide(0);
            break;
        case 'End':
            e.preventDefault();
            goToSlide(totalSlides - 1);
            break;
    }
}

// ========================================
// GESTOS TOUCH (SWIPE)
// ========================================

function handleTouchStart(e) {
    touchStartX = e.changedTouches[0].screenX;
}

function handleTouchEnd(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}

function handleSwipe() {
    const swipeThreshold = 50; // mínimo de píxeles para considerar swipe
    const difference = touchStartX - touchEndX;

    if (Math.abs(difference) < swipeThreshold) return;

    if (difference > 0) {
        // Swipe left - siguiente
        nextSlide();
    } else {
        // Swipe right - anterior
        previousSlide();
    }
}

// ========================================
// UTILIDADES
// ========================================

function showNotification(message, type = 'info') {
    // Crear notificación temporal
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '10000';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);

    // Auto-eliminar después de 3 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

function logout() {
    // Implementar lógica de logout según tu sistema
    if (confirm('¿Deseas cerrar sesión?')) {
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = '/login.html';
    }
}

// ========================================
// EXPORTAR FUNCIONES GLOBALES
// ========================================

// Hacer funciones accesibles globalmente para onclick en HTML
window.loadRecorridos = loadRecorridos;
window.backToSelector = backToSelector;
window.backToRecorridos = backToRecorridos;
window.nextSlide = nextSlide;
window.previousSlide = previousSlide;
window.goToSlide = goToSlide;
window.exitSlideshow = exitSlideshow;
window.logout = logout;

console.log('✅ Recorridos Virtuales - Sistema cargado correctamente');
