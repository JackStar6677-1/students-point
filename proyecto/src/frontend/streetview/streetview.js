/**
 * Navegación Virtual - StudentsPoint
 * Sistema de navegación paso a paso por el campus
 */

class VirtualNavigation {
    constructor() {
        this.currentIndex = 0;
        this.points = [
            {
                id: 1,
                title: "Entrada Principal",
                description: "Bienvenido al campus StudentsPoint Maipú. Aquí comienza tu recorrido virtual por nuestras instalaciones.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Entrada Principal",
                detailDescription: "La entrada principal del campus StudentsPoint Maipú es el punto de acceso principal para estudiantes, profesores y visitantes.",
                features: [
                    "Recepción y atención al público",
                    "Información general del campus",
                    "Acceso a todas las instalaciones",
                    "Estacionamiento para visitantes"
                ],
                location: "Entrada Principal",
                hours: "Lunes a Viernes: 8:00 - 20:00",
                services: "Recepción, Información"
            },
            {
                id: 2,
                title: "Biblioteca",
                description: "Centro de recursos académicos con amplia colección de libros, computadores y espacios de estudio.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Biblioteca Central",
                detailDescription: "La biblioteca del campus cuenta con una amplia colección de recursos académicos y espacios de estudio.",
                features: [
                    "Más de 10,000 libros físicos",
                    "Acceso a bases de datos académicas",
                    "Espacios de estudio individual y grupal",
                    "Computadores con internet"
                ],
                location: "Edificio Principal - 2do Piso",
                hours: "Lunes a Viernes: 8:00 - 21:00",
                services: "Préstamo de libros, Consultas, Estudio"
            },
            {
                id: 3,
                title: "Laboratorio de Computación",
                description: "Laboratorios equipados con tecnología de última generación para el aprendizaje práctico.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Laboratorios de Computación",
                detailDescription: "Nuestros laboratorios están equipados con computadores de última generación y software especializado.",
                features: [
                    "Computadores de última generación",
                    "Software especializado por carrera",
                    "Conexión de alta velocidad",
                    "Proyectores y pantallas interactivas"
                ],
                location: "Edificio Tecnológico - 1er y 2do Piso",
                hours: "Lunes a Viernes: 8:00 - 22:00",
                services: "Clases prácticas, Proyectos, Consultas técnicas"
            },
            {
                id: 4,
                title: "Aula Magna",
                description: "Espacio principal para eventos, conferencias y presentaciones importantes del campus.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Aula Magna",
                detailDescription: "El Aula Magna es nuestro espacio principal para eventos académicos y conferencias.",
                features: [
                    "Capacidad para 200 personas",
                    "Sistema de audio profesional",
                    "Proyección HD y 4K",
                    "Iluminación profesional"
                ],
                location: "Edificio Principal - 3er Piso",
                hours: "Según programación de eventos",
                services: "Eventos, Conferencias, Presentaciones"
            },
            {
                id: 5,
                title: "Cafetería",
                description: "Espacio de encuentro estudiantil con variedad de alimentos y bebidas a precios accesibles.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Cafetería Estudiantil",
                detailDescription: "La cafetería es el corazón social del campus, donde los estudiantes se reúnen para comer y socializar.",
                features: [
                    "Variedad de comidas saludables",
                    "Precios accesibles para estudiantes",
                    "Espacios de descanso y socialización",
                    "WiFi gratuito"
                ],
                location: "Edificio Principal - Planta Baja",
                hours: "Lunes a Viernes: 7:30 - 19:00",
                services: "Alimentación, Descanso, Socialización"
            },
            {
                id: 6,
                title: "Laboratorio de Ciencias",
                description: "Laboratorios especializados para prácticas de ciencias básicas y experimentos.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Laboratorios de Ciencias",
                detailDescription: "Laboratorios especializados para las carreras que requieren prácticas de ciencias básicas.",
                features: [
                    "Instrumentos de laboratorio especializados",
                    "Materiales para experimentos",
                    "Medidas de seguridad completas",
                    "Supervisión de técnicos especializados"
                ],
                location: "Edificio de Ciencias - 1er Piso",
                hours: "Lunes a Viernes: 8:00 - 18:00",
                services: "Prácticas de laboratorio, Experimentos, Investigación"
            },
            {
                id: 7,
                title: "Área de Estudio",
                description: "Espacios tranquilos y cómodos para el estudio individual y grupal de los estudiantes.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Áreas de Estudio",
                detailDescription: "Espacios diseñados específicamente para el estudio, con mobiliario cómodo y ambiente tranquilo.",
                features: [
                    "Mobiliario cómodo y ergonómico",
                    "Iluminación natural y artificial",
                    "Ambiente silencioso",
                    "Enchufes para dispositivos"
                ],
                location: "Edificio Principal - 2do y 3er Piso",
                hours: "Lunes a Domingo: 7:00 - 23:00",
                services: "Estudio individual, Estudio grupal, Consultas"
            },
            {
                id: 8,
                title: "Patio Central",
                description: "Espacio al aire libre para el descanso, actividades recreativas y eventos al aire libre.",
                image: "/static/images/placeholder-campus.jpg",
                detailTitle: "Patio Central",
                detailDescription: "El patio central es un espacio al aire libre que sirve como punto de encuentro para estudiantes.",
                features: [
                    "Espacio al aire libre amplio",
                    "Áreas verdes y jardines",
                    "Mobiliario para descanso",
                    "Área para eventos al aire libre"
                ],
                location: "Centro del Campus",
                hours: "Acceso 24/7",
                services: "Descanso, Recreación, Eventos, Socialización"
            }
        ];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.renderPointsList();
        this.updateDisplay();
        this.updateProgress();
        
        // Reproducir sonido de carga
        if (window.playSound) {
            window.playSound('pageLoad');
        }
    }
    
    setupEventListeners() {
        // Botones de navegación
        document.getElementById('btnPrev').addEventListener('click', () => this.previousPoint());
        document.getElementById('btnNext').addEventListener('click', () => this.nextPoint());
        
        // Navegación por teclado
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                this.previousPoint();
            } else if (e.key === 'ArrowRight') {
                this.nextPoint();
            }
        });
        
        // Botones del header
        document.getElementById('btnFullscreen').addEventListener('click', () => this.toggleFullscreen());
        document.getElementById('btnInfo').addEventListener('click', () => this.showInfo());
        
        // Navegación por lista
        document.getElementById('points-list').addEventListener('click', (e) => {
            const pointItem = e.target.closest('.list-group-item');
            if (pointItem) {
                const index = parseInt(pointItem.dataset.index);
                this.goToPoint(index);
            }
        });
    }
    
    renderPointsList() {
        const pointsList = document.getElementById('points-list');
        pointsList.innerHTML = '';
        
        this.points.forEach((point, index) => {
            const listItem = document.createElement('div');
            listItem.className = `list-group-item ${index === this.currentIndex ? 'active' : ''}`;
            listItem.dataset.index = index;
            
            listItem.innerHTML = `
                <span class="point-number">${point.id}</span>
                <div>
                    <strong>${point.title}</strong>
                    <br>
                    <small>${point.description}</small>
                </div>
            `;
            
            pointsList.appendChild(listItem);
        });
    }
    
    updateDisplay() {
        const point = this.points[this.currentIndex];
        
        // Actualizar imagen
        const image = document.getElementById('current-image');
        image.src = point.image;
        image.alt = point.title;
        
        // Actualizar información del overlay
        document.getElementById('point-title').textContent = point.title;
        document.getElementById('point-description').textContent = point.description;
        
        // Actualizar detalles
        document.getElementById('detail-title').textContent = point.detailTitle;
        document.getElementById('detail-description').textContent = point.detailDescription;
        
        // Actualizar características
        const featuresList = document.getElementById('detail-features');
        featuresList.innerHTML = '';
        point.features.forEach(feature => {
            const li = document.createElement('li');
            li.textContent = feature;
            featuresList.appendChild(li);
        });
        
        // Actualizar meta información
        document.getElementById('meta-location').textContent = point.location;
        document.getElementById('meta-hours').textContent = point.hours;
        document.getElementById('meta-services').textContent = point.services;
        
        // Actualizar indicador de posición
        document.getElementById('current-position').textContent = this.currentIndex + 1;
        document.getElementById('total-positions').textContent = this.points.length;
        
        // Actualizar botones
        document.getElementById('btnPrev').disabled = this.currentIndex === 0;
        document.getElementById('btnNext').disabled = this.currentIndex === this.points.length - 1;
        
        // Actualizar lista
        this.renderPointsList();
        
        // Reproducir sonido de navegación
        if (window.playSound) {
            window.playSound('navigate');
        }
    }
    
    updateProgress() {
        const progress = ((this.currentIndex + 1) / this.points.length) * 100;
        document.getElementById('route-progress').style.width = `${progress}%`;
    }
    
    nextPoint() {
        if (this.currentIndex < this.points.length - 1) {
            this.currentIndex++;
            this.updateDisplay();
            this.updateProgress();
        }
    }
    
    previousPoint() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateDisplay();
            this.updateProgress();
        }
    }
    
    goToPoint(index) {
        if (index >= 0 && index < this.points.length) {
            this.currentIndex = index;
            this.updateDisplay();
            this.updateProgress();
        }
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('Error al entrar en pantalla completa:', err);
            });
        } else {
            document.exitFullscreen();
        }
        
        // Reproducir sonido
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    showInfo() {
        const modal = new bootstrap.Modal(document.getElementById('modalInfo'));
        modal.show();
        
        // Reproducir sonido
        if (window.playSound) {
            window.playSound('click');
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.virtualNavigation = new VirtualNavigation();
    
    // Agregar efectos hover con sonido
    const interactiveElements = document.querySelectorAll('.btn, .list-group-item');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            if (window.playSound) {
                window.playSound('hover');
            }
        });
    });
    
    // Animación de entrada
    const elements = document.querySelectorAll('.students-card, .streetview-container');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
});

// Exportar para uso global
window.VirtualNavigation = VirtualNavigation;
