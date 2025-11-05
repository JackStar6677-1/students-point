/**
 * Portfolio Manager - StudentsPoint
 * Sistema completo de portafolio con generación de PDF
 */

class PortfolioManager {
    constructor() {
        this.currentUser = null;
        this.portfolioData = {
            perfil: {
                nombre: '',
                email: '',
                telefono: '',
                linkedin: '',
                github: '',
                carrera: '',
                campus: '',
                tituloProfesional: '',
                resumenProfesional: ''
            },
            logros: [],
            proyectos: [],
            experiencias: [],
            habilidades: [],
            configuracion: {
                temaColor: '#2e004f',
                mostrarContacto: true,
                mostrarRedes: true,
                mostrarLogros: true,
                mostrarProyectos: true,
                mostrarExperiencia: true,
                mostrarHabilidades: true
            }
        };
        
        this.currentEditingItem = null;
        this.currentEditingType = null;
        
        this.init();
    }
    
    async init() {
        await this.loadUser();
        await this.loadPortfolioData();
        this.setupEventListeners();
        this.updateProgress();
        this.renderAllSections();
    }
    
    // === AUTENTICACIÓN ===
    async loadUser() {
        try {
            if (!window.authAPI) {
                throw new Error('Servicio de autenticación no disponible');
            }
            
            if (!window.authAPI.isAuthenticated()) {
                window.location.href = '/login.html';
                return;
            }
            
            this.currentUser = await window.authAPI.getCurrentUser();
            this.populateUserData();
        } catch (error) {
            console.error('Error loading user:', error);
            if (error.message.includes('401') || error.message.includes('autenticado')) {
                window.location.href = '/login.html';
            } else {
                this.showToast('Error al cargar el usuario', 'error');
            }
        }
    }
    
    populateUserData() {
        if (this.currentUser) {
            document.getElementById('inputNombre').value = this.currentUser.name || '';
            document.getElementById('inputEmail').value = this.currentUser.email || '';
            document.getElementById('inputCampus').value = this.currentUser.campus?.nombre || '';
            document.getElementById('inputCarrera').value = this.currentUser.career || '';
            
            this.portfolioData.perfil.nombre = this.currentUser.name || '';
            this.portfolioData.perfil.email = this.currentUser.email || '';
            this.portfolioData.perfil.campus = this.currentUser.campus?.nombre || '';
            this.portfolioData.perfil.carrera = this.currentUser.career || '';
        }
    }
    
    // === CARGA DE DATOS ===
    async loadPortfolioData() {
        try {
            if (!window.portfolioAPI) {
                throw new Error('Servicio API de portafolio no disponible');
            }
            
            const data = await window.portfolioAPI.getPortfolioCompleto();
            if (data) {
                this.portfolioData = { ...this.portfolioData, ...data };
            }
        } catch (error) {
            console.error('Error loading portfolio data:', error);
            const errorMsg = error.message || 'Error al cargar los datos del portafolio';
            this.showToast(errorMsg, 'error');
        }
    }
    
    async savePortfolioData() {
        try {
            if (!window.portfolioAPI) {
                throw new Error('Servicio API de portafolio no disponible');
            }
            
            await window.portfolioAPI.savePortfolioCompleto(this.portfolioData);
            this.showToast('Portafolio guardado exitosamente', 'success');
        } catch (error) {
            console.error('Error saving portfolio data:', error);
            const errorMsg = error.message || 'Error al guardar el portafolio';
            this.showToast(errorMsg, 'error');
        }
    }
    
    // === EVENT LISTENERS ===
    setupEventListeners() {
        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabId = e.target.dataset.tab;
                this.switchTab(tabId);
            });
        });
        
        // Form submissions
        document.getElementById('formPerfil')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.savePerfil();
        });
        
        document.getElementById('formConfiguracion')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveConfiguracion();
        });
        
        // Add buttons
        document.getElementById('btnAgregarLogro')?.addEventListener('click', () => {
            this.showModal('logro');
        });
        
        document.getElementById('btnAgregarProyecto')?.addEventListener('click', () => {
            this.showModal('proyecto');
        });
        
        document.getElementById('btnAgregarExperiencia')?.addEventListener('click', () => {
            this.showModal('experiencia');
        });
        
        document.getElementById('btnAgregarHabilidad')?.addEventListener('click', () => {
            this.showModal('habilidad');
        });
        
        // PDF Generation
        document.getElementById('btnGenerarPDF')?.addEventListener('click', () => {
            this.generatePDF();
        });
        
        // Preview
        document.getElementById('btnVistaPrevia')?.addEventListener('click', () => {
            this.showPreview();
        });
        
        // Modal events
        this.setupModalEvents();
    }
    
    setupModalEvents() {
        // Close modals
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });
        
        // Close on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        });
        
        // Form submissions
        document.getElementById('formLogro')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveItem('logro');
        });
        
        document.getElementById('formProyecto')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveItem('proyecto');
        });
        
        document.getElementById('formExperiencia')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveItem('experiencia');
        });
        
        document.getElementById('formHabilidad')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveItem('habilidad');
        });
    }
    
    // === NAVEGACIÓN ===
    switchTab(tabId) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`tab-${tabId}`).classList.add('active');
        
        // Play sound
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    // === GUARDAR DATOS ===
    savePerfil() {
        // Capturar todos los valores del formulario
        this.portfolioData.perfil = {
            nombre: document.getElementById('inputNombre')?.value || '',
            email: document.getElementById('inputEmail')?.value || '',
            telefono: document.getElementById('inputTelefono')?.value || '',
            linkedin: document.getElementById('inputLinkedin')?.value || '',
            github: document.getElementById('inputGithub')?.value || '',
            carrera: document.getElementById('inputCarrera')?.value || '',
            campus: document.getElementById('inputCampus')?.value || '',
            sitioWeb: document.getElementById('inputSitioWeb')?.value || '',
            resumenProfesional: document.getElementById('inputResumenBio')?.value || ''
        };
        
        // Debug: mostrar datos capturados
        console.log('Datos de perfil guardados:', this.portfolioData.perfil);
        
        this.savePortfolioData();
        this.updateProgress();
        this.showToast('Perfil guardado exitosamente', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    saveConfiguracion() {
        // Capturar configuración y datos adicionales del perfil
        const tituloProfesional = document.getElementById('inputTituloProfesional')?.value || '';
        const resumenProfesional = document.getElementById('inputResumenProfesional')?.value || '';
        
        this.portfolioData.configuracion = {
            tituloProfesional: tituloProfesional,
            resumenProfesional: resumenProfesional,
            temaColor: document.getElementById('inputTemaColor')?.value || '#2e004f',
            mostrarContacto: document.getElementById('inputMostrarContacto')?.checked ?? true,
            mostrarRedes: document.getElementById('inputMostrarRedes')?.checked ?? true,
            mostrarLogros: document.getElementById('inputMostrarLogros')?.checked ?? true,
            mostrarProyectos: document.getElementById('inputMostrarProyectos')?.checked ?? true,
            mostrarExperiencia: document.getElementById('inputMostrarExperiencia')?.checked ?? true,
            mostrarHabilidades: document.getElementById('inputMostrarHabilidades')?.checked ?? true
        };
        
        // Actualizar también el perfil con título y resumen
        this.portfolioData.perfil.tituloProfesional = tituloProfesional;
        this.portfolioData.perfil.resumenProfesional = resumenProfesional;
        
        // Debug: mostrar configuración guardada
        console.log('Configuración guardada:', this.portfolioData.configuracion);
        
        this.savePortfolioData();
        this.showToast('Configuración guardada exitosamente', 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    // === MODALES ===
    showModal(type, item = null) {
        this.currentEditingType = type;
        this.currentEditingItem = item;
        
        const modal = document.getElementById(`modal${type.charAt(0).toUpperCase() + type.slice(1)}`);
        const title = document.getElementById(`modal${type.charAt(0).toUpperCase() + type.slice(1)}Titulo`);
        
        if (title) {
            title.textContent = item ? 'Editar' : 'Agregar';
        }
        
        if (item) {
            this.populateModal(type, item);
        } else {
            this.clearModal(type);
        }
        
        modal.classList.add('show');
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    closeModal() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
        
        this.currentEditingItem = null;
        this.currentEditingType = null;
    }
    
    populateModal(type, item) {
        const form = document.getElementById(`form${type.charAt(0).toUpperCase() + type.slice(1)}`);
        if (!form) return;
        
        Object.keys(item).forEach(key => {
            const input = form.querySelector(`#input${type.charAt(0).toUpperCase() + type.slice(1)}${key.charAt(0).toUpperCase() + key.slice(1)}`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = item[key];
                } else {
                    input.value = item[key];
                }
            }
        });
    }
    
    clearModal(type) {
        const form = document.getElementById(`form${type.charAt(0).toUpperCase() + type.slice(1)}`);
        if (form) {
            form.reset();
        }
    }
    
    saveItem(type) {
        const form = document.getElementById(`form${type.charAt(0).toUpperCase() + type.slice(1)}`);
        const item = {};
        
        // Capturar TODOS los inputs del formulario por ID
        const prefix = `input${type.charAt(0).toUpperCase() + type.slice(1)}`;
        
        form.querySelectorAll('input, textarea, select').forEach(element => {
            if (element.id && element.id.startsWith(prefix)) {
                // Extraer el nombre del campo desde el ID
                const fieldName = element.id.replace(prefix, '');
                const camelCaseName = fieldName.charAt(0).toLowerCase() + fieldName.slice(1);
                
                // Capturar el valor según el tipo
                if (element.type === 'checkbox') {
                    item[camelCaseName] = element.checked;
                } else if (element.type === 'number') {
                    item[camelCaseName] = parseInt(element.value) || 0;
                } else {
                    item[camelCaseName] = element.value || '';
                }
            }
        });
        
        console.log(`Guardando ${type}:`, item);
        
        if (this.currentEditingItem) {
            // Edit existing item
            item.id = this.currentEditingItem.id;
            const index = this.portfolioData[type + 's'].findIndex(i => i.id === this.currentEditingItem.id);
            if (index !== -1) {
                this.portfolioData[type + 's'][index] = item;
            }
        } else {
            // Add new item
            item.id = Date.now();
            this.portfolioData[type + 's'].push(item);
        }
        
        this.savePortfolioData();
        this.renderSection(type + 's');
        this.updateProgress();
        this.closeModal();
        this.showToast(`${type.charAt(0).toUpperCase() + type.slice(1)} guardado exitosamente`, 'success');
        
        if (window.playSound) {
            window.playSound('success');
        }
    }
    
    deleteItem(type, id) {
        if (confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
            this.portfolioData[type] = this.portfolioData[type].filter(item => item.id !== id);
            this.savePortfolioData();
            this.renderSection(type);
            this.updateProgress();
            
            if (window.playSound) {
                window.playSound('success');
            }
        }
    }
    
    // === RENDERIZADO ===
    renderAllSections() {
        this.renderSection('logros');
        this.renderSection('proyectos');
        this.renderSection('experiencias');
        this.renderSection('habilidades');
    }
    
    renderSection(sectionName) {
        const container = document.getElementById(sectionName + 'List');
        if (!container) return;
        
        const items = this.portfolioData[sectionName] || [];
        
        if (items.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-${this.getSectionIcon(sectionName)}"></i>
                    <h3>No hay ${this.getSectionTitle(sectionName).toLowerCase()}</h3>
                    <p>Agrega tu primer ${this.getSectionTitle(sectionName).toLowerCase().slice(0, -1)} para comenzar</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = items.map(item => this.renderItem(sectionName, item)).join('');
        
        // Add event listeners for edit/delete buttons
        container.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                const item = this.portfolioData[sectionName].find(i => i.id === id);
                this.showModal(sectionName.slice(0, -1), item);
            });
        });
        
        container.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                this.deleteItem(sectionName, id);
            });
        });
    }
    
    renderItem(sectionName, item) {
        switch (sectionName) {
            case 'logros':
                return this.renderLogro(item);
            case 'proyectos':
                return this.renderProyecto(item);
            case 'experiencias':
                return this.renderExperiencia(item);
            case 'habilidades':
                return this.renderHabilidad(item);
            default:
                return '';
        }
    }
    
    renderLogro(logro) {
        return `
            <div class="item-card">
                <div class="item-header">
                    <h3 class="item-title">${logro.titulo || 'Sin título'}</h3>
                    <div class="item-actions">
                        <button class="btn btn-sm btn-secondary-portfolio btn-edit" data-id="${logro.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger-portfolio btn-delete" data-id="${logro.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="item-content">${logro.descripcion || 'Sin descripción'}</div>
                <div class="item-meta">
                    <span><i class="fas fa-tag"></i> ${logro.tipo || 'No especificado'}</span>
                    <span><i class="fas fa-calendar"></i> ${logro.fecha ? this.formatDate(logro.fecha) : 'Sin fecha'}</span>
                    ${logro.institucion ? `<span><i class="fas fa-building"></i> ${logro.institucion}</span>` : ''}
                </div>
            </div>
        `;
    }
    
    renderProyecto(proyecto) {
        return `
            <div class="item-card">
                <div class="item-header">
                    <h3 class="item-title">${proyecto.titulo || 'Sin título'}</h3>
                    <div class="item-actions">
                        <button class="btn btn-sm btn-secondary-portfolio btn-edit" data-id="${proyecto.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger-portfolio btn-delete" data-id="${proyecto.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="item-content">${proyecto.descripcion || 'Sin descripción'}</div>
                <div class="item-meta">
                    <span><i class="fas fa-info-circle"></i> ${proyecto.estado || 'No especificado'}</span>
                    <span><i class="fas fa-calendar"></i> ${proyecto.fechaInicio ? this.formatDate(proyecto.fechaInicio) : 'Sin fecha'}</span>
                    ${proyecto.tecnologias ? `<span><i class="fas fa-code"></i> ${proyecto.tecnologias}</span>` : ''}
                </div>
            </div>
        `;
    }
    
    renderExperiencia(experiencia) {
        return `
            <div class="item-card">
                <div class="item-header">
                    <h3 class="item-title">${experiencia.cargo || 'Sin cargo'} - ${experiencia.empresa || 'Sin empresa'}</h3>
                    <div class="item-actions">
                        <button class="btn btn-sm btn-secondary-portfolio btn-edit" data-id="${experiencia.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger-portfolio btn-delete" data-id="${experiencia.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="item-content">${experiencia.descripcion || 'Sin descripción'}</div>
                <div class="item-meta">
                    <span><i class="fas fa-briefcase"></i> ${experiencia.tipo || 'No especificado'}</span>
                    <span><i class="fas fa-calendar"></i> ${experiencia.fechaInicio ? this.formatDate(experiencia.fechaInicio) : 'Sin fecha'} - ${experiencia.fechaFin ? this.formatDate(experiencia.fechaFin) : 'Actual'}</span>
                    ${experiencia.ubicacion ? `<span><i class="fas fa-map-marker-alt"></i> ${experiencia.ubicacion}</span>` : ''}
                </div>
            </div>
        `;
    }
    
    renderHabilidad(habilidad) {
        const nivel = habilidad.nivel || 1;
        const stars = '★'.repeat(nivel) + '☆'.repeat(5 - nivel);
        
        return `
            <div class="skill-item">
                <div class="skill-name">${habilidad.nombre || 'Sin nombre'}</div>
                <div class="skill-level">${stars}</div>
                <div class="skill-category">${habilidad.categoria || 'No especificado'}</div>
                <div class="item-actions mt-2">
                    <button class="btn btn-sm btn-secondary-portfolio btn-edit" data-id="${habilidad.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger-portfolio btn-delete" data-id="${habilidad.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }
    
    // === PROGRESS ===
    updateProgress() {
        const totalFields = 8; // Perfil básico
        const totalItems = 4; // Logros, proyectos, experiencias, habilidades
        
        let completedFields = 0;
        let completedItems = 0;
        
        // Check profile fields
        const perfil = this.portfolioData.perfil;
        if (perfil.nombre) completedFields++;
        if (perfil.email) completedFields++;
        if (perfil.carrera) completedFields++;
        if (perfil.telefono) completedFields++;
        if (perfil.linkedin) completedFields++;
        if (perfil.github) completedFields++;
        if (this.portfolioData.configuracion.tituloProfesional) completedFields++;
        if (this.portfolioData.configuracion.resumenProfesional) completedFields++;
        
        // Check items
        if (this.portfolioData.logros.length > 0) completedItems++;
        if (this.portfolioData.proyectos.length > 0) completedItems++;
        if (this.portfolioData.experiencias.length > 0) completedItems++;
        if (this.portfolioData.habilidades.length > 0) completedItems++;
        
        const totalProgress = ((completedFields / totalFields) * 0.6) + ((completedItems / totalItems) * 0.4);
        const percentage = Math.round(totalProgress * 100);
        
        document.getElementById('completitudPorcentaje').textContent = `${percentage}%`;
        document.getElementById('completitudFill').style.width = `${percentage}%`;
        
        // Update stats
        const stats = document.getElementById('completitudStats');
        if (stats) {
            stats.innerHTML = `
                <div class="row text-center">
                    <div class="col-3">
                        <div class="stat-item">
                            <div class="stat-number">${completedFields}</div>
                            <div class="stat-label">Campos</div>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="stat-item">
                            <div class="stat-number">${this.portfolioData.logros.length}</div>
                            <div class="stat-label">Logros</div>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="stat-item">
                            <div class="stat-number">${this.portfolioData.proyectos.length}</div>
                            <div class="stat-label">Proyectos</div>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="stat-item">
                            <div class="stat-number">${this.portfolioData.experiencias.length}</div>
                            <div class="stat-label">Experiencias</div>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    // === PDF GENERATION ===
    async generatePDF() {
        try {
            this.showToast('Generando PDF...', 'info');
            
            // Verificar que jsPDF esté disponible
            if (typeof window.jspdf === 'undefined') {
                throw new Error('jsPDF no está cargado');
            }
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            const perfil = this.portfolioData.perfil;
            const config = this.portfolioData.configuracion;
            
            let y = 30;
            
            // Título principal - Nombre
            doc.setFontSize(24);
            doc.setFont(undefined, 'bold');
            doc.text(perfil.nombre || 'Curriculum Vitae', 20, y);
            y += 10;
            
            // Título profesional
            if (config.tituloProfesional || perfil.tituloProfesional) {
                doc.setFontSize(16);
                doc.setFont(undefined, 'normal');
                doc.setTextColor(100);
                doc.text(config.tituloProfesional || perfil.tituloProfesional, 20, y);
                y += 10;
            }
            
            // Línea separadora
            doc.setLineWidth(0.5);
            doc.line(20, y, 190, y);
            y += 10;
            
            // Resumen profesional
            if (config.resumenProfesional || perfil.resumenProfesional) {
                doc.setFontSize(12);
                doc.setFont(undefined, 'bold');
                doc.setTextColor(0);
                doc.text('Resumen Profesional', 20, y);
                y += 8;
                
                doc.setFont(undefined, 'normal');
                const resumen = config.resumenProfesional || perfil.resumenProfesional;
                const lineasResumen = doc.splitTextToSize(resumen, 170);
                doc.text(lineasResumen, 20, y);
                y += (lineasResumen.length * 6) + 10;
            }
            
            // Información de contacto
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.text('Información de Contacto', 20, y);
            y += 8;
            
            doc.setFontSize(11);
            doc.setFont(undefined, 'normal');
            
            if (perfil.email) {
                doc.text(`Email: ${perfil.email}`, 20, y);
                y += 6;
            }
            if (perfil.telefono) {
                doc.text(`Teléfono: ${perfil.telefono}`, 20, y);
                y += 6;
            }
            if (perfil.carrera) {
                doc.text(`Carrera: ${perfil.carrera}`, 20, y);
                y += 6;
            }
            if (perfil.campus) {
                doc.text(`Campus: ${perfil.campus}`, 20, y);
                y += 6;
            }
            if (perfil.linkedin) {
                doc.text(`LinkedIn: ${perfil.linkedin}`, 20, y);
                y += 6;
            }
            if (perfil.github) {
                doc.text(`GitHub: ${perfil.github}`, 20, y);
                y += 6;
            }
            if (perfil.sitioWeb) {
                doc.text(`Sitio Web: ${perfil.sitioWeb}`, 20, y);
                y += 6;
            }
            
            y += 5;
            
            // Add sections
            y = this.addSectionToPDF(doc, 'Logros y Certificaciones', this.portfolioData.logros, y + 20);
            y = this.addSectionToPDF(doc, 'Proyectos', this.portfolioData.proyectos, y + 20);
            y = this.addSectionToPDF(doc, 'Experiencia Laboral', this.portfolioData.experiencias, y + 20);
            y = this.addSectionToPDF(doc, 'Habilidades', this.portfolioData.habilidades, y + 20);
            
            // Save PDF
            const fileName = `cv_${(perfil.nombre || 'usuario').replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
            doc.save(fileName);
            
            this.showToast('PDF generado exitosamente', 'success');
            
            if (window.playSound) {
                window.playSound('success');
            }
            
        } catch (error) {
            console.error('Error generating PDF:', error);
            this.showToast(`Error al generar el PDF: ${error.message}`, 'error');
        }
    }
    
    addSectionToPDF(doc, title, items, startY) {
        if (!items || items.length === 0) {
            return startY;
        }
        
        doc.setFontSize(16);
        doc.text(title, 20, startY);
        
        let y = startY + 10;
        items.forEach(item => {
            if (y > 280) {
                doc.addPage();
                y = 20;
            }
            
            doc.setFontSize(12);
            const titulo = item.titulo || item.nombre || item.cargo || 'Sin título';
            doc.text(titulo, 20, y);
            y += 10;
            
            doc.setFontSize(10);
            const descripcion = item.descripcion || '';
            if (descripcion) {
                const lines = doc.splitTextToSize(descripcion, 170);
                doc.text(lines, 20, y);
                y += lines.length * 5 + 5;
            }
            
            // Agregar información adicional según el tipo
            if (item.tipo) {
                doc.text(`Tipo: ${item.tipo}`, 20, y);
                y += 8;
            }
            if (item.estado) {
                doc.text(`Estado: ${item.estado}`, 20, y);
                y += 8;
            }
            if (item.nivel && title === 'Habilidades') {
                doc.text(`Nivel: ${item.nivel}/5`, 20, y);
                y += 8;
            }
            
            y += 5; // Espacio entre items
        });
        
        return y;
    }
    
    // === VISTA PREVIA ===
    showPreview() {
        // Create preview modal
        const previewModal = document.createElement('div');
        previewModal.className = 'modal show';
        previewModal.innerHTML = `
            <div class="modal-content" style="max-width: 800px;">
                <div class="modal-header">
                    <h2 class="modal-title">Vista Previa del Portafolio</h2>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="pdf-preview-body">
                        ${this.generatePreviewHTML()}
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary-portfolio" onclick="portfolioManager.generatePDF()">
                        <i class="fas fa-file-pdf"></i> Generar PDF
                    </button>
                    <button class="btn btn-secondary-portfolio modal-close">Cerrar</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(previewModal);
        
        // Close modal
        previewModal.querySelector('.modal-close').addEventListener('click', () => {
            document.body.removeChild(previewModal);
        });
        
        previewModal.addEventListener('click', (e) => {
            if (e.target === previewModal) {
                document.body.removeChild(previewModal);
            }
        });
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    generatePreviewHTML() {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        
        return `
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: ${config.temaColor}; text-align: center; margin-bottom: 30px;">
                    ${perfil.nombre || 'Tu Nombre'}
                </h1>
                
                ${config.tituloProfesional ? `<h2 style="text-align: center; color: #666; margin-bottom: 20px;">${config.tituloProfesional}</h2>` : ''}
                
                ${config.resumenProfesional ? `<p style="text-align: center; font-style: italic; margin-bottom: 30px;">${config.resumenProfesional}</p>` : ''}
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                    ${config.mostrarContacto ? `
                        <div>
                            <h3>Contacto</h3>
                            <p>Email: ${perfil.email || 'No especificado'}</p>
                            <p>Teléfono: ${perfil.telefono || 'No especificado'}</p>
                        </div>
                    ` : ''}
                    
                    ${config.mostrarRedes ? `
                        <div>
                            <h3>Redes Sociales</h3>
                            ${perfil.linkedin ? `<p>LinkedIn: ${perfil.linkedin}</p>` : ''}
                            ${perfil.github ? `<p>GitHub: ${perfil.github}</p>` : ''}
                        </div>
                    ` : ''}
                </div>
                
                ${config.mostrarLogros && this.portfolioData.logros.length > 0 ? `
                    <div style="margin-bottom: 30px;">
                        <h3>Logros y Certificaciones</h3>
                        ${this.portfolioData.logros.map(logro => `
                            <div style="margin-bottom: 15px; padding: 10px; border-left: 3px solid ${config.temaColor};">
                                <h4 style="margin: 0;">${logro.titulo}</h4>
                                <p style="margin: 5px 0;">${logro.descripcion}</p>
                                <small style="color: #666;">${logro.tipo} - ${this.formatDate(logro.fecha)}</small>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${config.mostrarProyectos && this.portfolioData.proyectos.length > 0 ? `
                    <div style="margin-bottom: 30px;">
                        <h3>Proyectos</h3>
                        ${this.portfolioData.proyectos.map(proyecto => `
                            <div style="margin-bottom: 15px; padding: 10px; border-left: 3px solid ${config.temaColor};">
                                <h4 style="margin: 0;">${proyecto.titulo}</h4>
                                <p style="margin: 5px 0;">${proyecto.descripcion}</p>
                                <small style="color: #666;">${proyecto.estado} - ${proyecto.tecnologias || ''}</small>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${config.mostrarExperiencia && this.portfolioData.experiencias.length > 0 ? `
                    <div style="margin-bottom: 30px;">
                        <h3>Experiencia Laboral</h3>
                        ${this.portfolioData.experiencias.map(exp => `
                            <div style="margin-bottom: 15px; padding: 10px; border-left: 3px solid ${config.temaColor};">
                                <h4 style="margin: 0;">${exp.cargo} - ${exp.empresa}</h4>
                                <p style="margin: 5px 0;">${exp.descripcion}</p>
                                <small style="color: #666;">${exp.tipo} - ${this.formatDate(exp.fechaInicio)} ${exp.fechaFin ? `a ${this.formatDate(exp.fechaFin)}` : 'a la fecha'}</small>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${config.mostrarHabilidades && this.portfolioData.habilidades.length > 0 ? `
                    <div style="margin-bottom: 30px;">
                        <h3>Habilidades</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                            ${this.portfolioData.habilidades.map(habilidad => `
                                <div style="padding: 10px; background: #f5f5f5; border-radius: 5px;">
                                    <strong>${habilidad.nombre}</strong>
                                    <div>${''.repeat(habilidad.nivel)}${''.repeat(5 - habilidad.nivel)}</div>
                                    <small style="color: #666;">${habilidad.categoria}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    // === UTILIDADES ===
    getSectionIcon(sectionName) {
        const icons = {
            logros: 'trophy',
            proyectos: 'code',
            experiencias: 'briefcase',
            habilidades: 'cogs'
        };
        return icons[sectionName] || 'file';
    }
    
    getSectionTitle(sectionName) {
        const titles = {
            logros: 'Logros',
            proyectos: 'Proyectos',
            experiencias: 'Experiencias',
            habilidades: 'Habilidades'
        };
        return titles[sectionName] || 'Elementos';
    }
    
    formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}

// Initialize portfolio manager
let portfolioManager;
document.addEventListener('DOMContentLoaded', () => {
    portfolioManager = new PortfolioManager();
    
    // Play page load sound
    if (window.playSound) {
        window.playSound('pageLoad');
    }
});
