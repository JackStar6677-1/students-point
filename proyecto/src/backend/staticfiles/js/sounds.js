// StudentsPoint - Sistema de Sonidos Simplificado
class StudentsPointSounds {
    constructor() {
        this.sounds = {};
        this.enabled = true;
        this.volume = 0.25; // Volumen más alto para sonidos más profundos
        this.audioContext = null;
        this.backgroundMusic = null;
        this.backgroundMusicEnabled = true;
        this.backgroundMusicVolume = 0.3; // Música de ambiente más audible
        this.backgroundMusicPlaying = false;
        this.init();
    }

    init() {
        // Crear sonidos suaves
        this.createSoftSounds();
        
        // Inicializar música de fondo
        this.initBackgroundMusic();
        
        // Configurar activación por interacción del usuario
        this.setupUserInteraction();
    }

    createSoftSounds() {
        // Crear contexto de audio
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Función para crear tonos suaves
        const createSoftTone = (frequency, duration, type = 'sine', effects = {}) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            const filter = this.audioContext.createBiquadFilter();
            
            // Configurar filtro para sonidos más profundos y graves
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(800, this.audioContext.currentTime); // Filtro más grave
            filter.Q.setValueAtTime(1.2, this.audioContext.currentTime); // Q más resonante
            
            // Conectar nodos
            oscillator.connect(filter);
            filter.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = type;
            
            // Configurar volumen con curva muy suave
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(this.volume * 0.3, this.audioContext.currentTime + 0.02); // Volumen muy bajo
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration);
        };

        // Sonidos muy suaves y discretos
        this.sounds = {
            // Sonido de hover más grave
            hover: () => createSoftTone(150, 0.1, 'sine'),
            
            // Sonido de click más grave
            click: () => createSoftTone(200, 0.12, 'sine'),
            
            // Sonido de éxito más grave
            success: () => createSoftTone(300, 0.22, 'sine'),
            
            // Sonido de error más grave
            error: () => createSoftTone(120, 0.18, 'sine'),
            
            // Sonido de notificación más grave
            notification: () => createSoftTone(400, 0.12, 'sine'),
            
            // Sonido de transición más profundo
            transition: () => createSoftTone(180, 0.15, 'sine'),
            
            // Sonido de login más grave
            loginSuccess: () => createSoftTone(250, 0.22, 'sine'),
            
            // Sonido de logout más profundo
            logout: () => createSoftTone(140, 0.18, 'sine'),
            
            // Sonido de navegación más grave
            navigate: () => createSoftTone(160, 0.1, 'sine'),
            
            // Sonido de formulario completado más profundo
            formComplete: () => createSoftTone(220, 0.18, 'sine'),
            
            // Sonido de mensaje enviado más grave
            messageSent: () => createSoftTone(280, 0.12, 'sine'),
            
            // Sonido de archivo subido más profundo
            fileUpload: () => createSoftTone(190, 0.15, 'sine'),
            
            // Sonido de búsqueda más grave
            search: () => createSoftTone(240, 0.1, 'sine'),
            
            // Sonido de like más profundo
            like: () => createSoftTone(320, 0.12, 'sine'),
            
            // Sonido de comentario más grave
            comment: () => createSoftTone(210, 0.1, 'sine'),
            
            // Sonido de notificación push más grave
            pushNotification: () => createSoftTone(260, 0.1, 'sine'),
            
            // Sonido de validación más profundo
            validationSuccess: () => createSoftTone(230, 0.12, 'sine'),
            
            // Sonido de carga de página más grave
            pageLoad: () => createSoftTone(170, 0.12, 'sine'),
            
            // Sonido de cierre de modal más profundo
            modalClose: () => createSoftTone(130, 0.1, 'sine'),
            
            // Sonido de scroll más grave
            scroll: () => createSoftTone(110, 0.08, 'sine'),
            
            // Sonido de drag and drop suave
            dragDrop: () => createSoftTone(700, 0.1, 'sine'),
            
            // Sonido de copia discreto
            copy: () => createSoftTone(1000, 0.06, 'sine'),
            
            // Sonido de zoom suave
            zoom: () => createSoftTone(800, 0.08, 'sine'),
            
            // Sonido de menú desplegable discreto
            dropdown: () => createSoftTone(900, 0.08, 'sine'),
            
            // Sonido de toggle suave
            toggle: () => createSoftTone(700, 0.06, 'sine'),
            
            // Sonido de slider muy discreto
            slider: () => createSoftTone(600, 0.05, 'sine'),
            
            // Sonido de calendario suave
            calendar: () => createSoftTone(800, 0.1, 'sine'),
            
            // Sonido de mapa discreto
            map: () => createSoftTone(600, 0.1, 'sine'),
            
            // Sonido de chat suave
            chat: () => createSoftTone(900, 0.08, 'sine'),
            
            // Sonido de video discreto
            video: () => createSoftTone(800, 0.1, 'sine'),
            
            // Sonido de audio suave
            audio: () => createSoftTone(700, 0.08, 'sine'),
            
            // Sonido de imagen discreto
            image: () => createSoftTone(1000, 0.08, 'sine'),
            
            // Sonido de documento suave
            document: () => createSoftTone(750, 0.1, 'sine'),
            
            // Sonido de configuración discreto
            settings: () => createSoftTone(800, 0.08, 'sine'),
            
            // Sonido de perfil suave
            profile: () => createSoftTone(700, 0.1, 'sine'),
            
            // Sonido de estadísticas discreto
            stats: () => createSoftTone(900, 0.08, 'sine'),
            
            // Sonido de reporte suave
            report: () => createSoftTone(650, 0.1, 'sine'),
            
            // Sonido de backup discreto
            backup: () => createSoftTone(800, 0.12, 'sine'),
            
            // Sonido de sincronización suave
            sync: () => createSoftTone(700, 0.1, 'sine')
        };
    }

    initBackgroundMusic() {
        // Crear elemento de audio para la música de fondo
        this.backgroundMusic = new Audio('/static/audio/Hans Zimmer - Interstellar (minimalist) [a4E95rYAe4U].mp3');
        this.backgroundMusic.loop = true;
        this.backgroundMusic.volume = this.backgroundMusicVolume;
        this.backgroundMusic.preload = 'auto';
        
        // Manejar eventos de la música de fondo
        this.backgroundMusic.addEventListener('loadstart', () => {
            console.log('StudentsPoint: Cargando música de ambiente...');
        });
        
        this.backgroundMusic.addEventListener('canplaythrough', () => {
            console.log('StudentsPoint: Música de ambiente lista');
            // No auto-reproducir hasta que el usuario interactúe
        });
        
        this.backgroundMusic.addEventListener('error', (e) => {
            console.warn('StudentsPoint: Error cargando música de ambiente:', e);
            this.backgroundMusicEnabled = false;
        });
        
        this.backgroundMusic.addEventListener('ended', () => {
            // Reiniciar automáticamente si está en loop
            if (this.backgroundMusicEnabled && this.backgroundMusicPlaying) {
                this.backgroundMusic.currentTime = 0;
                this.backgroundMusic.play().catch(e => {
                    console.log('StudentsPoint: Error reiniciando música de ambiente:', e);
                });
            }
        });
    }

    playBackgroundMusic() {
        if (!this.backgroundMusic || !this.backgroundMusicEnabled) return;
        
        this.backgroundMusic.play().then(() => {
            this.backgroundMusicPlaying = true;
            console.log('StudentsPoint: Música de ambiente iniciada');
        }).catch(e => {
            console.log('StudentsPoint: No se pudo reproducir música de ambiente:', e);
            this.backgroundMusicEnabled = false;
        });
    }

    pauseBackgroundMusic() {
        if (!this.backgroundMusic) return;
        
        this.backgroundMusic.pause();
        this.backgroundMusicPlaying = false;
        console.log('StudentsPoint: Música de ambiente pausada');
    }

    stopBackgroundMusic() {
        if (!this.backgroundMusic) return;
        
        this.backgroundMusic.pause();
        this.backgroundMusic.currentTime = 0;
        this.backgroundMusicPlaying = false;
        console.log('StudentsPoint: Música de ambiente detenida');
    }

    toggleBackgroundMusic() {
        if (this.backgroundMusicPlaying) {
            this.pauseBackgroundMusic();
        } else {
            this.playBackgroundMusic();
        }
    }

    setupUserInteraction() {
        // Configurar activación de audio después de la primera interacción del usuario
        const activateAudio = () => {
            // Activar contexto de audio
            if (this.audioContext && this.audioContext.state === 'suspended') {
                this.audioContext.resume().then(() => {
                    console.log('StudentsPoint: Audio activado por interacción del usuario');
                    // Iniciar música de fondo después de la activación
                    if (this.backgroundMusicEnabled) {
                        this.playBackgroundMusic();
                    }
                }).catch(e => {
                    console.log('StudentsPoint: Error activando audio:', e);
                });
            }
            
            // Remover listeners después de la primera activación
            document.removeEventListener('click', activateAudio);
            document.removeEventListener('keydown', activateAudio);
            document.removeEventListener('touchstart', activateAudio);
        };
        
        // Agregar listeners para diferentes tipos de interacción
        document.addEventListener('click', activateAudio, { once: true });
        document.addEventListener('keydown', activateAudio, { once: true });
        document.addEventListener('touchstart', activateAudio, { once: true });
    }

    play(soundName) {
        if (!this.enabled || !this.sounds[soundName]) return;
        
        try {
            // Verificar si el contexto de audio está suspendido
            if (this.audioContext && this.audioContext.state === 'suspended') {
                this.audioContext.resume().catch(error => {
                    console.log('No se pudo reanudar el contexto de audio:', error);
                });
            }
            
            this.sounds[soundName]();
        } catch (error) {
            console.log('Error reproduciendo sonido:', error);
        }
    }

    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }

    // Método para reproducir sonidos con delay
    playDelayed(soundName, delay = 0) {
        setTimeout(() => this.play(soundName), delay);
    }

    // Método para reproducir múltiples sonidos en secuencia
    playSequence(soundNames, delays = []) {
        soundNames.forEach((soundName, index) => {
            const delay = delays[index] || index * 200;
            this.playDelayed(soundName, delay);
        });
    }
}

// Inicializar sistema de sonidos
window.StudentsPointSounds = new StudentsPointSounds();

// Función global para reproducir sonidos
window.playSound = (soundName) => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.play(soundName);
    }
};

// Función global para reproducir sonidos con delay
window.playSoundDelayed = (soundName, delay = 0) => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.playDelayed(soundName, delay);
    }
};

// Función global para reproducir secuencias de sonidos
window.playSoundSequence = (soundNames, delays = []) => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.playSequence(soundNames, delays);
    }
};

// Funciones globales para controlar la música de fondo
window.playBackgroundMusic = () => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.playBackgroundMusic();
    }
};

window.pauseBackgroundMusic = () => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.pauseBackgroundMusic();
    }
};

window.stopBackgroundMusic = () => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.stopBackgroundMusic();
    }
};

window.toggleBackgroundMusic = () => {
    if (window.StudentsPointSounds) {
        window.StudentsPointSounds.toggleBackgroundMusic();
    }
};