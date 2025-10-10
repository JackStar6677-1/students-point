/**
 * Lazy Loading de Imágenes para StudentsPoint
 * Mejora el rendimiento cargando imágenes solo cuando son visibles
 */

class LazyLoader {
    constructor(options = {}) {
        this.options = {
            root: null,
            rootMargin: '50px',
            threshold: 0.01,
            ...options
        };

        this.observer = null;
        this.init();
    }

    init() {
        // Verificar soporte de IntersectionObserver
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver(
                this.handleIntersection.bind(this),
                this.options
            );

            // Observar todas las imágenes lazy
            this.observeImages();
        } else {
            // Fallback para navegadores antiguos
            this.loadAllImages();
        }
    }

    observeImages() {
        const images = document.querySelectorAll('img[data-src], img[loading="lazy"]');
        images.forEach(img => {
            if (img.dataset.src) {
                this.observer.observe(img);
            }
        });
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                this.loadImage(img);
                this.observer.unobserve(img);
            }
        });
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;

        // Agregar clase de carga
        img.classList.add('lazy-loading');

        // Crear imagen temporal para precargar
        const tempImg = new Image();
        
        tempImg.onload = () => {
            img.src = src;
            img.classList.remove('lazy-loading');
            img.classList.add('lazy-loaded');
            
            // Remover atributo data-src
            delete img.dataset.src;
        };

        tempImg.onerror = () => {
            img.classList.remove('lazy-loading');
            img.classList.add('lazy-error');
            console.error(`Error cargando imagen: ${src}`);
        };

        tempImg.src = src;
    }

    loadAllImages() {
        // Fallback: cargar todas las imágenes inmediatamente
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => this.loadImage(img));
    }

    // Agregar nuevas imágenes al observer
    observe(element) {
        if (this.observer) {
            this.observer.observe(element);
        }
    }
}

// CSS para animación de carga
const style = document.createElement('style');
style.textContent = `
    img[data-src] {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }

    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    img.lazy-loaded {
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    img.lazy-error {
        background: #ffebee;
        border: 2px dashed #f44336;
    }
`;
document.head.appendChild(style);

// Instancia global
const lazyLoader = new LazyLoader();

// Re-observar imágenes después de cambios dinámicos
document.addEventListener('DOMContentLoaded', () => {
    // Observar mutaciones para nuevas imágenes
    const mutationObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { // Element node
                    // Buscar imágenes en el nuevo nodo
                    const images = node.querySelectorAll ? node.querySelectorAll('img[data-src]') : [];
                    images.forEach(img => lazyLoader.observe(img));
                    
                    // Si el nodo mismo es una imagen
                    if (node.tagName === 'IMG' && node.dataset.src) {
                        lazyLoader.observe(node);
                    }
                }
            });
        });
    });

    mutationObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
});

