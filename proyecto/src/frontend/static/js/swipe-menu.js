/**
 * Swipe Menu - Navegación con gestos táctiles
 * Desliza de izquierda a derecha para abrir el menú
 */

(function() {
    'use strict';
    
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    let sidebar = null;
    let overlay = null;
    let isMenuOpen = false;
    
    // Configuración
    const SWIPE_THRESHOLD = 50; // Mínimo de píxeles para considerar un swipe
    const EDGE_THRESHOLD = 30;  // Área desde el borde izquierdo para iniciar el swipe
    
    /**
     * Inicializar el menú con gestos
     */
    function init() {
        sidebar = document.querySelector('.sidebar');
        
        if (!sidebar) {
            console.warn('Sidebar no encontrado');
            return;
        }
        
        // Crear overlay
        createOverlay();
        
        // Agregar event listeners
        document.addEventListener('touchstart', handleTouchStart, { passive: true });
        document.addEventListener('touchmove', handleTouchMove, { passive: false });
        document.addEventListener('touchend', handleTouchEnd, { passive: true });
        
        console.log('Swipe menu inicializado');
    }
    
    /**
     * Crear el overlay oscuro
     */
    function createOverlay() {
        if (!document.querySelector('.swipe-overlay')) {
            overlay = document.createElement('div');
            overlay.className = 'swipe-overlay';
            overlay.addEventListener('click', closeMenu);
            document.body.appendChild(overlay);
        } else {
            overlay = document.querySelector('.swipe-overlay');
        }
    }
    
    /**
     * Manejar inicio del toque
     */
    function handleTouchStart(e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }
    
    /**
     * Manejar movimiento del toque
     */
    function handleTouchMove(e) {
        // Si el menú está cerrado y el toque no empezó desde el borde, ignorar
        if (!isMenuOpen && touchStartX > EDGE_THRESHOLD) {
            return;
        }
        
        // Si hay un swipe horizontal significativo, prevenir scroll
        const currentX = e.touches[0].clientX;
        const diffX = Math.abs(currentX - touchStartX);
        const diffY = Math.abs(e.touches[0].clientY - touchStartY);
        
        if (diffX > diffY && diffX > 10) {
            e.preventDefault();
        }
    }
    
    /**
     * Manejar fin del toque
     */
    function handleTouchEnd(e) {
        touchEndX = e.changedTouches[0].clientX;
        touchEndY = e.changedTouches[0].clientY;
        
        handleSwipe();
    }
    
    /**
     * Procesar el gesto de swipe
     */
    function handleSwipe() {
        const diffX = touchEndX - touchStartX;
        const diffY = Math.abs(touchEndY - touchStartY);
        
        // Verificar que sea un swipe horizontal (no vertical)
        if (diffY > 100) {
            return; // Probablemente es un scroll vertical
        }
        
        // Swipe de izquierda a derecha para ABRIR
        if (!isMenuOpen && diffX > SWIPE_THRESHOLD && touchStartX <= EDGE_THRESHOLD) {
            openMenu();
        }
        
        // Swipe de derecha a izquierda para CERRAR
        if (isMenuOpen && diffX < -SWIPE_THRESHOLD) {
            closeMenu();
        }
    }
    
    /**
     * Abrir el menú
     */
    function openMenu() {
        if (!sidebar || isMenuOpen) return;
        
        sidebar.classList.add('swipe-active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        isMenuOpen = true;
        
        console.log('Menú abierto');
    }
    
    /**
     * Cerrar el menú
     */
    function closeMenu() {
        if (!sidebar || !isMenuOpen) return;
        
        sidebar.classList.remove('swipe-active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        isMenuOpen = false;
        
        console.log('Menú cerrado');
    }
    
    /**
     * Agregar listener para cerrar con tecla Escape
     */
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isMenuOpen) {
            closeMenu();
        }
    });
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Exportar funciones
    window.swipeMenu = {
        open: openMenu,
        close: closeMenu,
        isOpen: () => isMenuOpen
    };
    
})();

