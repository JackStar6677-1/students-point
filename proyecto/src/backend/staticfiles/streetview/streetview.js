/**
 * Tour Manager - StudentsPoint
 * Sistema de recorridos virtuales estilo diapositivas
 */

class TourManager {
    constructor() {
        this.currentTour = null;
        this.currentSlide = 0;
        this.tours = {
            'campus-general': {
                title: 'Campus General',
                slides: [
                    {
                        title: 'Entrada Principal',
                        description: 'Bienvenido al campus principal. Aquí encontrarás la recepción y información general.',
                        points: ['Recepción principal', 'Información estudiantil', 'Mapa del campus', 'Servicios de atención']
                    },
                    {
                        title: 'Patio Central',
                        description: 'El corazón del campus, un espacio de encuentro y descanso para estudiantes.',
                        points: ['Área de descanso', 'Espacios verdes', 'Zona de encuentros', 'Acceso a todas las áreas']
                    },
                    {
                        title: 'Aulas de Clases',
                        description: 'Las aulas están equipadas con tecnología moderna para el aprendizaje.',
                        points: ['Pizarras digitales', 'Sistemas de audio', 'Aire acondicionado', 'Capacidad para 30-40 estudiantes']
                    }
                ]
            },
            'biblioteca': {
                title: 'Biblioteca',
                slides: [
                    {
                        title: 'Recepción de Biblioteca',
                        description: 'La biblioteca es el centro de recursos académicos del campus.',
                        points: ['Préstamo de libros', 'Consulta de catálogo', 'Asistencia bibliotecaria', 'Registro de usuarios']
                    },
                    {
                        title: 'Sala de Lectura',
                        description: 'Ambiente silencioso y cómodo para la lectura y estudio.',
                        points: ['Mesas individuales', 'Iluminación adecuada', 'Ambiente climatizado', 'Política de silencio']
                    }
                ]
            },
            'casino': {
                title: 'Casino',
                slides: [
                    {
                        title: 'Ingreso al recorrido',
                        description: 'Inicio del recorrido hacia el casino del campus.',
                        points: ['Sigue la señalética', 'Mantén tu derecha', 'Respeta las zonas de tránsito']
                    },
                    {
                        title: 'Paso 1',
                        description: 'Primer punto de referencia hacia el casino.',
                        points: ['Referencia visual 1', 'Dirección recta', 'Zona iluminada']
                    },
                    {
                        title: 'Paso 2',
                        description: 'Continúa por el pasillo siguiendo la señalética.',
                        points: ['Referencia visual 2', 'Gira a la derecha al final', 'Mantén el paso peatonal']
                    },
                    {
                        title: 'Paso 3',
                        description: 'Cruza el hall y continúa hacia el sector de alimentación.',
                        points: ['Referencia visual 3', 'Cruce seguro', 'Señal de “Alimentación”']
                    },
                    {
                        title: 'Paso 4',
                        description: 'Último tramo antes de llegar al casino.',
                        points: ['Referencia visual 4', 'Área de mesas a la vista', 'Entrada próxima']
                    }
                ]
            }
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('tourModal').classList.contains('show')) {
                if (e.key === 'ArrowLeft') this.previousSlide();
                else if (e.key === 'ArrowRight') this.nextSlide();
                else if (e.key === 'Escape') this.closeTour();
            }
        });
    }

    startTour(tourId) {
        if (!this.tours[tourId]) {
            this.showError('Recorrido no disponible');
            return;
        }

        this.currentTour = this.tours[tourId];
        this.currentSlide = 0;
        
        const modal = new bootstrap.Modal(document.getElementById('tourModal'));
        document.getElementById('tourModalTitle').textContent = this.currentTour.title;
        
        this.renderSlide();
        this.updateNavigation();
        modal.show();
    }

    renderSlide() {
        if (!this.currentTour) return;

        const slide = this.currentTour.slides[this.currentSlide];
        const content = document.getElementById('tourContent');
        
        // Si el tour es "casino", mostrar la imagen real correspondiente
        const isCasino = (this.currentTour && this.currentTour.title === 'Casino');
        const casinoImages = [
            '/imagenes/mapa/casino/img1casino.jpeg',
            '/imagenes/mapa/casino/img2casino.jpeg',
            '/imagenes/mapa/casino/img3casino.jpeg',
            '/imagenes/mapa/casino/img4casino.jpeg',
            '/imagenes/mapa/casino/img5casino.jpeg',
        ];
        const casinoImgSrc = isCasino ? casinoImages[this.currentSlide] : null;

        content.innerHTML = `
            <div class="slide-container">
                <div class="slide-image">
                    ${isCasino ? `
                        <img src="${casinoImgSrc}" alt="${slide.title}" class="img-fluid rounded w-100"/>
                    ` : `
                        <div class="image-placeholder">
                            <i class="fas fa-image fa-5x"></i>
                            <p>Imagen: ${slide.title}</p>
                        </div>
                    `}
                </div>
                <div class="slide-content">
                    <h3>${slide.title}</h3>
                    <p class="slide-description">${slide.description}</p>
                    <div class="slide-points">
                        <h5>Características:</h5>
                        <ul>
                            ${slide.points.map(point => `<li>${point}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    nextSlide() {
        if (!this.currentTour) return;
        if (this.currentSlide < this.currentTour.slides.length - 1) {
            this.currentSlide++;
            this.renderSlide();
            this.updateNavigation();
        }
    }

    previousSlide() {
        if (!this.currentTour) return;
        if (this.currentSlide > 0) {
            this.currentSlide--;
            this.renderSlide();
            this.updateNavigation();
        }
    }

    updateNavigation() {
        if (!this.currentTour) return;

        const totalSlides = this.currentTour.slides.length;
        const progress = ((this.currentSlide + 1) / totalSlides) * 100;
        
        document.getElementById('slideCounter').textContent = `${this.currentSlide + 1} / ${totalSlides}`;
        document.getElementById('tourProgressBar').style.width = `${progress}%`;
        
        document.getElementById('prevSlide').disabled = this.currentSlide === 0;
        document.getElementById('nextSlide').disabled = this.currentSlide === totalSlides - 1;
    }

    restartTour() {
        if (!this.currentTour) return;
        this.currentSlide = 0;
        this.renderSlide();
        this.updateNavigation();
    }

    closeTour() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('tourModal'));
        if (modal) modal.hide();
    }

    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => {
            if (alertDiv.parentNode) alertDiv.remove();
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        if (window.playSound) window.playSound('pageLoad');
    }, 500);
    window.tourManager = new TourManager();
});