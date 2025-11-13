/**
 * Mobile Menu Handler
 * Maneja la funcionalidad del menú lateral en dispositivos móviles
 */

(function() {
    'use strict';
    
    // Variables globales
    let sidebar = null;
    let overlay = null;
    let menuToggle = null;
    let isMobile = false;
    
    /**
     * Detecta si estamos en mobile
     */
    function checkIfMobile() {
        return window.innerWidth <= 768;
    }
    
    /**
     * Inicializa el menú móvil
     */
    function initMobileMenu() {
        // Obtener elementos
        sidebar = document.querySelector('.sidebar');
        
        if (!sidebar) {
            console.warn('Sidebar no encontrado');
            return;
        }
        
        // Crear overlay si no existe
        if (!document.querySelector('.sidebar-overlay')) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);
        } else {
            overlay = document.querySelector('.sidebar-overlay');
        }
        
        // Crear botón hamburguesa si no existe
        if (!document.querySelector('.mobile-menu-toggle')) {
            menuToggle = document.createElement('button');
            menuToggle.className = 'mobile-menu-toggle';
            menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
            menuToggle.setAttribute('aria-label', 'Abrir menú');
            menuToggle.setAttribute('aria-expanded', 'false');
            document.body.appendChild(menuToggle);
        } else {
            menuToggle = document.querySelector('.mobile-menu-toggle');
        }
        
        // Event listeners
        setupEventListeners();
        
        // Verificar si es mobile
        isMobile = checkIfMobile();
        
        // Ocultar/mostrar botón según tamaño de pantalla
        updateMenuVisibility();
    }
    
    /**
     * Configura los event listeners
     */
    function setupEventListeners() {
        // Toggle menu al hacer click en el botón
        if (menuToggle) {
            menuToggle.addEventListener('click', toggleMenu);
        }
        
        // Cerrar menu al hacer click en el overlay
        if (overlay) {
            overlay.addEventListener('click', closeMenu);
        }
        
        // Cerrar menu al hacer click en un link (excepto los que tienen data-section)
        const menuItems = sidebar.querySelectorAll('.menu-item');
        menuItems.forEach(item => {
            if (!item.dataset.section && item.getAttribute('href') !== '#') {
                item.addEventListener('click', () => {
                    if (isMobile) {
                        closeMenu();
                    }
                });
            }
        });
        
        // Detectar cambios de tamaño de ventana
        window.addEventListener('resize', debounce(handleResize, 250));
        
        // Detectar swipe para cerrar
        let touchStartX = 0;
        let touchEndX = 0;
        
        sidebar.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        sidebar.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
        
        function handleSwipe() {
            // Swipe hacia la izquierda para cerrar
            if (touchStartX - touchEndX > 50) {
                closeMenu();
            }
        }
        
        // Cerrar con tecla Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('active')) {
                closeMenu();
            }
        });
    }
    
    /**
     * Abre el menú
     */
    function openMenu() {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        menuToggle.innerHTML = '<i class="fas fa-times"></i>';
        menuToggle.setAttribute('aria-expanded', 'true');
        
        // Prevenir scroll del body
        document.body.style.overflow = 'hidden';
        
        // Focus en el primer elemento del menú
        const firstMenuItem = sidebar.querySelector('.menu-item');
        if (firstMenuItem) {
            setTimeout(() => firstMenuItem.focus(), 300);
        }
    }
    
    /**
     * Cierra el menú
     */
    function closeMenu() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        menuToggle.setAttribute('aria-expanded', 'false');
        
        // Restaurar scroll del body
        document.body.style.overflow = '';
    }
    
    /**
     * Toggle del menú
     */
    function toggleMenu() {
        if (sidebar.classList.contains('active')) {
            closeMenu();
        } else {
            openMenu();
        }
    }
    
    /**
     * Maneja el resize de la ventana
     */
    function handleResize() {
        const wasMobile = isMobile;
        isMobile = checkIfMobile();
        
        // Si cambió de mobile a desktop
        if (wasMobile && !isMobile) {
            closeMenu();
        }
        
        updateMenuVisibility();
    }
    
    /**
     * Actualiza la visibilidad del botón según el tamaño de pantalla
     */
    function updateMenuVisibility() {
        if (menuToggle) {
            if (isMobile) {
                menuToggle.style.display = 'flex';
            } else {
                menuToggle.style.display = 'none';
                // Asegurarse de que el sidebar esté visible en desktop
                sidebar.classList.remove('active');
                if (overlay) {
                    overlay.classList.remove('active');
                }
                document.body.style.overflow = '';
            }
        }
    }
    
    /**
     * Debounce utility
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }
    
    // Exportar funciones para uso global si es necesario
    window.mobileMenu = {
        open: openMenu,
        close: closeMenu,
        toggle: toggleMenu
    };
    
})();

