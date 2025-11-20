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
            configuracion: {
                plantilla: 'profesional',
                temaColor: '#2e004f',
                mostrarContacto: true,
                mostrarRedes: true,
                mostrarLogros: true,
                mostrarProyectos: true,
                mostrarExperiencia: true
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
                
                // Cargar configuración y llenar formulario de información personal
                if (data.config) {
                    const config = data.config;
                    // Llenar campos de información personal desde la configuración
                    if (document.getElementById('inputTelefono')) {
                        document.getElementById('inputTelefono').value = config.telefono || '';
                    }
                    if (document.getElementById('inputLinkedin')) {
                        document.getElementById('inputLinkedin').value = config.linkedin_url || '';
                    }
                    if (document.getElementById('inputGithub')) {
                        document.getElementById('inputGithub').value = config.github_url || '';
                    }
                    
                    // Llenar campos de configuración
                    if (document.getElementById('inputTituloProfesional')) {
                        document.getElementById('inputTituloProfesional').value = config.titulo_profesional || '';
                    }
                    if (document.getElementById('inputResumenProfesional')) {
                        document.getElementById('inputResumenProfesional').value = config.resumen_profesional || '';
                    }
                    if (document.getElementById('inputMostrarContacto')) {
                        document.getElementById('inputMostrarContacto').checked = config.mostrar_contacto ?? true;
                    }
                    if (document.getElementById('inputMostrarRedes')) {
                        document.getElementById('inputMostrarRedes').checked = config.mostrar_redes_sociales ?? true;
                    }
                    if (document.getElementById('inputMostrarLogros')) {
                        document.getElementById('inputMostrarLogros').checked = config.mostrar_logros ?? true;
                    }
                    if (document.getElementById('inputMostrarProyectos')) {
                        document.getElementById('inputMostrarProyectos').checked = config.mostrar_proyectos ?? true;
                    }
                    if (document.getElementById('inputMostrarExperiencia')) {
                        document.getElementById('inputMostrarExperiencia').checked = config.mostrar_experiencia ?? true;
                    }
                    
                    // Actualizar datos locales
                    this.portfolioData.configuracion = {
                        tituloProfesional: config.titulo_profesional || '',
                        resumenProfesional: config.resumen_profesional || '',
                        mostrarContacto: config.mostrar_contacto ?? true,
                        mostrarRedes: config.mostrar_redes_sociales ?? true,
                        mostrarLogros: config.mostrar_logros ?? true,
                        mostrarProyectos: config.mostrar_proyectos ?? true,
                        mostrarExperiencia: config.mostrar_experiencia ?? true,
                    };
                    
                    this.portfolioData.perfil = {
                        ...this.portfolioData.perfil,
                        telefono: config.telefono || '',
                        linkedin: config.linkedin_url || '',
                        github: config.github_url || '',
                    };
                }
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
        
        // Template Selection
        document.querySelectorAll('.template-card').forEach(card => {
            card.addEventListener('click', () => {
                this.selectTemplate(card.dataset.template);
            });
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
    async savePerfil() {
        try {
            // Capturar todos los valores del formulario
            const perfilData = {
                telefono: document.getElementById('inputTelefono')?.value || '',
                linkedin_url: document.getElementById('inputLinkedin')?.value || '',
                github_url: document.getElementById('inputGithub')?.value || '',
            };
            
            // Guardar en el backend usando updateConfiguracion
            if (window.portfolioAPI) {
                await window.portfolioAPI.updateConfiguracion(perfilData);
            }
            
            // Actualizar datos locales
            this.portfolioData.perfil = {
                nombre: document.getElementById('inputNombre')?.value || '',
                email: document.getElementById('inputEmail')?.value || '',
                telefono: perfilData.telefono,
                linkedin: perfilData.linkedin_url,
                github: perfilData.github_url,
                carrera: document.getElementById('inputCarrera')?.value || '',
                campus: document.getElementById('inputCampus')?.value || '',
            };
            
            this.updateProgress();
            this.showToast('Perfil guardado exitosamente', 'success');
            
            if (window.playSound) {
                window.playSound('success');
            }
        } catch (error) {
            console.error('Error guardando perfil:', error);
            this.showToast('Error al guardar el perfil', 'error');
        }
    }
    
    async saveConfiguracion() {
        try {
            // Capturar configuración y datos adicionales del perfil
            const tituloProfesional = document.getElementById('inputTituloProfesional')?.value || '';
            const resumenProfesional = document.getElementById('inputResumenProfesional')?.value || '';
            
            const configData = {
                titulo_profesional: tituloProfesional,
                resumen_profesional: resumenProfesional,
                mostrar_contacto: document.getElementById('inputMostrarContacto')?.checked ?? true,
                mostrar_redes_sociales: document.getElementById('inputMostrarRedes')?.checked ?? true,
                mostrar_logros: document.getElementById('inputMostrarLogros')?.checked ?? true,
                mostrar_proyectos: document.getElementById('inputMostrarProyectos')?.checked ?? true,
                mostrar_experiencia: document.getElementById('inputMostrarExperiencia')?.checked ?? true
            };
            
            // Guardar en el backend
            if (window.portfolioAPI) {
                await window.portfolioAPI.updateConfiguracion(configData);
            }
            
            // Actualizar datos locales
            this.portfolioData.configuracion = {
                tituloProfesional: tituloProfesional,
                resumenProfesional: resumenProfesional,
                mostrarContacto: configData.mostrar_contacto,
                mostrarRedes: configData.mostrar_redes_sociales,
                mostrarLogros: configData.mostrar_logros,
                mostrarProyectos: configData.mostrar_proyectos,
                mostrarExperiencia: configData.mostrar_experiencia
            };
            
            // Actualizar también el perfil con título y resumen
            this.portfolioData.perfil.tituloProfesional = tituloProfesional;
            this.portfolioData.perfil.resumenProfesional = resumenProfesional;
            
            this.showToast('Configuración guardada exitosamente', 'success');
            
            if (window.playSound) {
                window.playSound('success');
            }
        } catch (error) {
            console.error('Error guardando configuración:', error);
            this.showToast('Error al guardar la configuración', 'error');
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
    
    // === PROGRESS ===
    updateProgress() {
        const totalFields = 8; // Perfil básico
        const totalItems = 3; // Logros, proyectos, experiencias
        
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
            const plantilla = this.portfolioData.configuracion.plantilla || 'profesional';
            
            // Generar PDF según la plantilla seleccionada
            switch(plantilla) {
                case 'profesional':
                    this.generateProfesionalTemplate(doc);
                    break;
                case 'creativa':
                    this.generateCreativaTemplate(doc);
                    break;
                case 'minimalista':
                    this.generateMinimalistaTemplate(doc);
                    break;
                case 'moderna':
                    this.generateModernaTemplate(doc);
                    break;
                case 'ejecutiva':
                    this.generateEjecutivaTemplate(doc);
                    break;
                case 'corporativa':
                    this.generateCorporativaTemplate(doc);
                    break;
                case 'tecnica':
                    this.generateTecnicaTemplate(doc);
                    break;
                default:
                    this.generateProfesionalTemplate(doc);
            }
            
            // Save PDF
            const perfil = this.portfolioData.perfil;
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
    
    // Plantilla Profesional - Elegante y corporativo
    generateProfesionalTemplate(doc) {
            const perfil = this.portfolioData.perfil;
            const config = this.portfolioData.configuracion;
        let y = 20;
            
        // Header con fondo azul
        doc.setFillColor(46, 0, 79); // Morado oscuro
        doc.rect(0, 0, 210, 40, 'F');
            
        // Nombre en blanco
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(26);
            doc.setFont(undefined, 'bold');
        doc.text(perfil.nombre || 'Nombre Completo', 20, 20);
            
            // Título profesional
        doc.setFontSize(14);
                doc.setFont(undefined, 'normal');
        doc.text(config.tituloProfesional || perfil.tituloProfesional || 'Título Profesional', 20, 30);
        
        y = 50;
        doc.setTextColor(0, 0, 0);
        
        // Información de contacto
        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');
        let contactInfo = [];
        if (perfil.email) contactInfo.push(perfil.email);
        if (perfil.telefono) contactInfo.push(perfil.telefono);
        if (perfil.linkedin) contactInfo.push(perfil.linkedin);
        doc.text(contactInfo.join(' | '), 20, y);
                y += 10;
            
            // Línea separadora
        doc.setDrawColor(200, 200, 200);
            doc.setLineWidth(0.5);
            doc.line(20, y, 190, y);
            y += 10;
            
            // Resumen profesional
            if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(46, 0, 79);
            doc.text('PERFIL PROFESIONAL', 20, y);
            y += 7;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 170);
            doc.text(lineasResumen, 20, y);
            y += (lineasResumen.length * 5) + 10;
        }
        
        // Experiencia
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addProfesionalSection(doc, 'EXPERIENCIA LABORAL', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        // Proyectos
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addProfesionalSection(doc, 'PROYECTOS', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        // Logros
        if (this.portfolioData.logros.length > 0) {
            y = this.addProfesionalSection(doc, 'LOGROS Y CERTIFICACIONES', this.portfolioData.logros, y, 'logro');
        }
    }
    
    addProfesionalSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            y = 20;
        }
        
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(46, 0, 79);
        doc.text(title, 20, y);
        y += 2;
        
        // Línea bajo el título
        doc.setDrawColor(46, 0, 79);
        doc.setLineWidth(1);
        doc.line(20, y, 190, y);
        y += 8;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach(item => {
            if (y > 270) {
                doc.addPage();
                y = 20;
            }
            
                doc.setFontSize(12);
                doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || ''} - ${item.empresa || ''}`, 20, y);
                y += 6;
                doc.setFontSize(9);
                doc.setFont(undefined, 'italic');
                doc.setTextColor(100, 100, 100);
                doc.text(`${item.fechaInicio ? this.formatDate(item.fechaInicio) : ''} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 20, y);
                y += 5;
            } else {
                doc.text(item.titulo || item.nombre || '', 20, y);
                y += 6;
                doc.setFontSize(9);
                doc.setFont(undefined, 'italic');
                doc.setTextColor(100, 100, 100);
                if (item.fecha) doc.text(this.formatDate(item.fecha), 20, y);
                if (item.fechaInicio) doc.text(this.formatDate(item.fechaInicio), 20, y);
                y += 5;
            }
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 170);
                doc.text(lineas, 20, y);
                y += (lineas.length * 5) + 3;
            }
            
            y += 5;
        });
        
        return y + 5;
    }
    
    // Plantilla Creativa - Moderna y colorida
    generateCreativaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        let y = 15;
        
        // Nombre con color vibrante
        doc.setTextColor(13, 202, 240); // Cyan
        doc.setFontSize(28);
        doc.setFont(undefined, 'bold');
        doc.text(perfil.nombre || 'Nombre Completo', 105, y, { align: 'center' });
        y += 10;
        
        // Título profesional
        doc.setTextColor(32, 201, 151); // Verde
        doc.setFontSize(16);
        doc.text(config.tituloProfesional || perfil.tituloProfesional || 'Título Profesional', 105, y, { align: 'center' });
        y += 15;
        
        // Decoración colorida
        doc.setFillColor(13, 202, 240, 0.3);
        doc.circle(15, 15, 8, 'F');
        doc.setFillColor(32, 201, 151, 0.3);
        doc.circle(195, 15, 6, 'F');
        doc.setFillColor(255, 193, 7, 0.3);
        doc.circle(195, 280, 8, 'F');
        
        doc.setTextColor(0, 0, 0);
        
        // Información de contacto en una caja
        doc.setFillColor(240, 240, 240);
        doc.roundedRect(20, y, 170, 15, 3, 3, 'F');
        
        doc.setFontSize(9);
        y += 10;
        let contactInfo = [];
        if (perfil.email) contactInfo.push(perfil.email);
        if (perfil.telefono) contactInfo.push(perfil.telefono);
        if (perfil.linkedin) contactInfo.push(perfil.linkedin);
        doc.text(contactInfo.join(' • '), 105, y, { align: 'center' });
        y += 12;
        
        // Resumen profesional con borde colorido
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setDrawColor(13, 202, 240);
            doc.setLineWidth(2);
            doc.line(20, y, 35, y);
            
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(13, 202, 240);
            doc.text('SOBRE MÍ', 40, y);
                y += 8;
                
            doc.setFontSize(10);
                doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
                const resumen = config.resumenProfesional || perfil.resumenProfesional;
                const lineasResumen = doc.splitTextToSize(resumen, 170);
                doc.text(lineasResumen, 20, y);
            y += (lineasResumen.length * 5) + 10;
        }
        
        // Secciones con colores alternados
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addCreativaSection(doc, 'EXPERIENCIA', this.portfolioData.experiencias, y, '#20c997', 'experiencia');
        }
        
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addCreativaSection(doc, 'PROYECTOS', this.portfolioData.proyectos, y, '#ffc107', 'proyecto');
        }
        
        if (this.portfolioData.logros.length > 0) {
            y = this.addCreativaSection(doc, 'LOGROS', this.portfolioData.logros, y, '#dc3545', 'logro');
        }
    }
    
    addCreativaSection(doc, title, items, startY, color, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            y = 20;
        }
        
        // Título con línea colorida
        const colors = {
            '#20c997': [32, 201, 151],
            '#ffc107': [255, 193, 7],
            '#dc3545': [220, 53, 69]
        };
        
        const rgb = colors[color] || [0, 0, 0];
        doc.setDrawColor(...rgb);
        doc.setLineWidth(2);
        doc.line(20, y, 35, y);
        
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
        doc.setTextColor(...rgb);
        doc.text(title, 40, y);
        y += 10;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach(item => {
            if (y > 270) {
                doc.addPage();
                y = 20;
            }
            
            doc.setFontSize(12);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || ''} @ ${item.empresa || ''}`, 20, y);
            } else {
                doc.text(item.titulo || item.nombre || '', 20, y);
            }
            y += 5;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(100, 100, 100);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 20, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 20, y);
            }
            y += 5;
            
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 170);
                doc.text(lineas, 20, y);
                y += (lineas.length * 5);
            }
            
            y += 8;
        });
        
        return y;
    }
    
    // Plantilla Minimalista - Limpia y simple
    generateMinimalistaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        let y = 30;
        
        // Nombre centrado
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(24);
        doc.setFont(undefined, 'bold');
        doc.text(perfil.nombre || 'Nombre Completo', 105, y, { align: 'center' });
        y += 8;
        
        // Título profesional
        doc.setFontSize(12);
        doc.setFont(undefined, 'normal');
        doc.text(config.tituloProfesional || perfil.tituloProfesional || '', 105, y, { align: 'center' });
        y += 6;
        
        // Contacto minimalista
        doc.setFontSize(9);
        let contactInfo = [];
        if (perfil.email) contactInfo.push(perfil.email);
        if (perfil.telefono) contactInfo.push(perfil.telefono);
        doc.text(contactInfo.join('  ·  '), 105, y, { align: 'center' });
        y += 15;
        
        // Línea separadora simple
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.line(20, y, 190, y);
        y += 10;
        
        // Resumen
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 170);
            doc.text(lineasResumen, 20, y);
            y += (lineasResumen.length * 5) + 15;
        }
        
        // Secciones minimalistas
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addMinimalistaSection(doc, 'Experiencia', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addMinimalistaSection(doc, 'Proyectos', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        if (this.portfolioData.logros.length > 0) {
            y = this.addMinimalistaSection(doc, 'Certificaciones', this.portfolioData.logros, y, 'logro');
        }
    }
    
    addMinimalistaSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            y = 20;
        }
        
        // Título simple
        doc.setFontSize(12);
        doc.setFont(undefined, 'bold');
        doc.text(title.toUpperCase(), 20, y);
        y += 8;
        
        items.forEach(item => {
            if (y > 270) {
                doc.addPage();
                y = 20;
            }
            
            doc.setFontSize(11);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || ''}`, 20, y);
            doc.setFont(undefined, 'normal');
                doc.text(`${item.empresa || ''}`, 100, y);
            } else {
                doc.text(item.titulo || item.nombre || '', 20, y);
            }
            y += 5;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(120, 120, 120);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Presente'}`, 20, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 20, y);
            }
            y += 5;
            
            doc.setFontSize(9);
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 170);
                doc.text(lineas, 20, y);
                y += (lineas.length * 4);
            }
            
            y += 8;
        });
        
        return y;
    }
    
    // Plantilla Moderna - Con elementos gráficos
    generateModernaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        
        // Sidebar izquierdo con info personal
        doc.setFillColor(46, 0, 79);
        doc.rect(0, 0, 60, 297, 'F');
        
        // Nombre y título en sidebar
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(18);
        doc.setFont(undefined, 'bold');
        const nombreLines = doc.splitTextToSize(perfil.nombre || 'Nombre', 50);
        doc.text(nombreLines, 10, 30);
        
        let y = 30 + (nombreLines.length * 7) + 5;
        doc.setFontSize(11);
        doc.setFont(undefined, 'normal');
        const tituloLines = doc.splitTextToSize(config.tituloProfesional || perfil.tituloProfesional || '', 50);
        doc.text(tituloLines, 10, y);
        
        y += (tituloLines.length * 6) + 15;
        
        // Contacto en sidebar
        doc.setFontSize(9);
        doc.setFont(undefined, 'bold');
        doc.text('CONTACTO', 10, y);
                y += 6;
        doc.setFont(undefined, 'normal');
        
        if (perfil.email) {
            const emailLines = doc.splitTextToSize(perfil.email, 50);
            doc.text(emailLines, 10, y);
            y += emailLines.length * 5 + 4;
            }
            if (perfil.telefono) {
            doc.text(perfil.telefono, 10, y);
            y += 8;
        }
        if (perfil.linkedin) {
            const linkedinLines = doc.splitTextToSize(perfil.linkedin, 50);
            doc.text(linkedinLines, 10, y);
            y += linkedinLines.length * 5;
        }
        
        // Contenido principal
        doc.setTextColor(0, 0, 0);
        y = 30;
        
        // Resumen profesional
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(46, 0, 79);
            doc.text('PERFIL', 70, y);
            y += 8;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 130);
            doc.text(lineasResumen, 70, y);
            y += (lineasResumen.length * 5) + 12;
        }
        
        // Secciones con diseño moderno
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addModernaSection(doc, 'EXPERIENCIA', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addModernaSection(doc, 'PROYECTOS', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        if (this.portfolioData.logros.length > 0) {
            y = this.addModernaSection(doc, 'LOGROS', this.portfolioData.logros, y, 'logro');
        }
    }
    
    addModernaSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            // Mantener sidebar en nuevas páginas
            doc.setFillColor(46, 0, 79);
            doc.rect(0, 0, 60, 297, 'F');
            y = 20;
        }
        
        // Título de sección
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(46, 0, 79);
        doc.text(title, 70, y);
        y += 2;
        
        // Línea decorativa
        doc.setDrawColor(13, 202, 240);
        doc.setLineWidth(2);
        doc.line(70, y, 100, y);
        y += 10;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach(item => {
            if (y > 270) {
                doc.addPage();
                doc.setFillColor(46, 0, 79);
                doc.rect(0, 0, 60, 297, 'F');
                y = 20;
            }
            
            doc.setFontSize(11);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || ''}`, 70, y);
                y += 5;
                doc.setFontSize(10);
                doc.setFont(undefined, 'normal');
                doc.setTextColor(100, 100, 100);
                doc.text(`${item.empresa || ''}`, 70, y);
                y += 4;
            } else {
                doc.text(item.titulo || item.nombre || '', 70, y);
                y += 5;
            }
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'italic');
            doc.setTextColor(120, 120, 120);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 70, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 70, y);
            }
            y += 5;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 130);
                doc.text(lineas, 70, y);
                y += (lineas.length * 4.5);
            }
            
            y += 7;
        });
        
        return y;
    }
    
    // Plantilla Ejecutiva - Sidebar verde a la izquierda
    generateEjecutivaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        
        // Sidebar verde oscuro
        doc.setFillColor(16, 71, 52); // Verde oscuro profesional
        doc.rect(0, 0, 70, 297, 'F');
        
        // Nombre en sidebar
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(20);
        doc.setFont(undefined, 'bold');
        const nombreLines = doc.splitTextToSize(perfil.nombre || 'Nombre Completo', 60);
        doc.text(nombreLines, 10, 25);
        
        let ySidebar = 25 + (nombreLines.length * 8) + 5;
        
        // Título profesional en sidebar
        doc.setFontSize(11);
        doc.setFont(undefined, 'normal');
        const tituloLines = doc.splitTextToSize(config.tituloProfesional || perfil.tituloProfesional || '', 60);
        doc.text(tituloLines, 10, ySidebar);
        ySidebar += (tituloLines.length * 6) + 15;
        
        // Línea divisoria
        doc.setDrawColor(255, 255, 255);
        doc.setLineWidth(0.5);
        doc.line(10, ySidebar, 60, ySidebar);
        ySidebar += 10;
        
        // Detalles en sidebar
        doc.setFontSize(12);
        doc.setFont(undefined, 'bold');
        doc.text('DETALLES', 10, ySidebar);
        ySidebar += 8;
        
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        
        if (perfil.email) {
            doc.setFont(undefined, 'bold');
            doc.text('Email', 10, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const emailLines = doc.splitTextToSize(perfil.email, 55);
            doc.text(emailLines, 10, ySidebar);
            ySidebar += (emailLines.length * 5) + 6;
        }
        
        if (perfil.telefono) {
            doc.setFont(undefined, 'bold');
            doc.text('Teléfono', 10, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            doc.text(perfil.telefono, 10, ySidebar);
            ySidebar += 10;
        }
        
            if (perfil.carrera) {
            doc.setFont(undefined, 'bold');
            doc.text('Carrera', 10, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const carreraLines = doc.splitTextToSize(perfil.carrera, 55);
            doc.text(carreraLines, 10, ySidebar);
            ySidebar += (carreraLines.length * 5) + 6;
        }
        
            if (perfil.campus) {
            doc.setFont(undefined, 'bold');
            doc.text('Campus', 10, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const campusLines = doc.splitTextToSize(perfil.campus, 55);
            doc.text(campusLines, 10, ySidebar);
            ySidebar += (campusLines.length * 5) + 10;
        }
        
        // Enlaces en sidebar
        if (perfil.linkedin || perfil.github) {
            doc.setFillColor(255, 255, 255, 0.1);
            doc.roundedRect(10, ySidebar, 50, 3, 1, 1, 'F');
            ySidebar += 8;
            
            doc.setFontSize(12);
            doc.setFont(undefined, 'bold');
            doc.text('ENLACES', 10, ySidebar);
            ySidebar += 8;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            
            if (perfil.linkedin) {
                const linkedinLines = doc.splitTextToSize(perfil.linkedin, 55);
                doc.text(linkedinLines, 10, ySidebar);
                ySidebar += (linkedinLines.length * 5) + 4;
            }
            
            if (perfil.github) {
                const githubLines = doc.splitTextToSize(perfil.github, 55);
                doc.text(githubLines, 10, ySidebar);
                ySidebar += (githubLines.length * 5);
            }
        }
        
        // Contenido principal
        doc.setTextColor(0, 0, 0);
        let y = 25;
        
        // Perfil/Resumen
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(16);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(16, 71, 52);
            doc.text('Perfil', 80, y);
            y += 8;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 120);
            doc.text(lineasResumen, 80, y);
            y += (lineasResumen.length * 5) + 12;
        }
        
        // Experiencia laboral
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addEjecutivaSection(doc, 'Experiencia Laboral', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        // Proyectos
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addEjecutivaSection(doc, 'Proyectos', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        // Formación/Logros
        if (this.portfolioData.logros.length > 0) {
            y = this.addEjecutivaSection(doc, 'Formación y Certificaciones', this.portfolioData.logros, y, 'logro');
        }
    }
    
    addEjecutivaSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            // Mantener sidebar
            doc.setFillColor(16, 71, 52);
            doc.rect(0, 0, 70, 297, 'F');
            y = 20;
        }
        
        // Título de sección
        doc.setFontSize(16);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(16, 71, 52);
        doc.text(title, 80, y);
        y += 2;
        
        // Línea bajo título
        doc.setDrawColor(16, 71, 52);
        doc.setLineWidth(1.5);
        doc.line(80, y, 200, y);
        y += 10;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach((item, index) => {
            if (y > 265) {
                doc.addPage();
                doc.setFillColor(16, 71, 52);
                doc.rect(0, 0, 70, 297, 'F');
                y = 20;
            }
            
            // Bullet point
            doc.setFillColor(16, 71, 52);
            doc.circle(82, y - 1, 1.5, 'F');
            
            doc.setFontSize(12);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || 'Cargo'}`, 87, y);
            y += 5;
                doc.setFontSize(10);
                doc.setFont(undefined, 'italic');
                doc.setTextColor(100, 100, 100);
                doc.text(`${item.empresa || 'Empresa'}`, 87, y);
                y += 4;
            } else {
                doc.text(item.titulo || item.nombre || '', 87, y);
                y += 5;
            }
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(120, 120, 120);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 87, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 87, y);
            }
            y += 5;
            
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 115);
                doc.text(lineas, 87, y);
                y += (lineas.length * 5);
            }
            
            y += 8;
        });
        
        return y;
    }
    
    // Plantilla Corporativa - Sidebar azul a la derecha
    generateCorporativaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        
        // Sidebar azul oscuro a la derecha
        doc.setFillColor(25, 55, 109); // Azul oscuro corporativo
        doc.rect(140, 0, 70, 297, 'F');
        
        // Contenido principal (lado izquierdo)
        doc.setTextColor(0, 0, 0);
        let y = 25;
        
        // Nombre en área principal
        doc.setFontSize(24);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(25, 55, 109);
        doc.text(perfil.nombre || 'Nombre Completo', 20, y);
        y += 10;
        
        // Título profesional
        doc.setFontSize(14);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(100, 100, 100);
        doc.text(config.tituloProfesional || perfil.tituloProfesional || '', 20, y);
        y += 15;
        
        doc.setTextColor(0, 0, 0);
        
        // Perfil
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(25, 55, 109);
            doc.text('Perfil', 20, y);
            y += 8;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 110);
            doc.text(lineasResumen, 20, y);
            y += (lineasResumen.length * 5) + 12;
        }
        
        // Experiencia laboral
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addCorporativaSection(doc, 'Experiencia Laboral', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        // Proyectos
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addCorporativaSection(doc, 'Proyectos', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        // Logros
        if (this.portfolioData.logros.length > 0) {
            y = this.addCorporativaSection(doc, 'Formación', this.portfolioData.logros, y, 'logro');
        }
        
        // Sidebar contenido
        let ySidebar = 25;
        doc.setTextColor(255, 255, 255);
        
        // Detalles en sidebar
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.text('Detalles', 145, ySidebar);
        ySidebar += 10;
        
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        
        if (perfil.email) {
            doc.setFont(undefined, 'bold');
            doc.text('Correo', 145, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const emailLines = doc.splitTextToSize(perfil.email, 60);
            doc.text(emailLines, 145, ySidebar);
            ySidebar += (emailLines.length * 5) + 6;
        }
        
        if (perfil.telefono) {
            doc.setFont(undefined, 'bold');
            doc.text('Teléfono', 145, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            doc.text(perfil.telefono, 145, ySidebar);
            ySidebar += 10;
        }
        
        if (perfil.carrera) {
            doc.setFont(undefined, 'bold');
            doc.text('Carrera', 145, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const carreraLines = doc.splitTextToSize(perfil.carrera, 60);
            doc.text(carreraLines, 145, ySidebar);
            ySidebar += (carreraLines.length * 5) + 6;
        }
        
        if (perfil.campus) {
            doc.setFont(undefined, 'bold');
            doc.text('Campus', 145, ySidebar);
            ySidebar += 5;
            doc.setFont(undefined, 'normal');
            const campusLines = doc.splitTextToSize(perfil.campus, 60);
            doc.text(campusLines, 145, ySidebar);
            ySidebar += (campusLines.length * 5) + 10;
        }
        
        // Enlaces
        if (perfil.linkedin || perfil.github) {
            doc.setDrawColor(255, 255, 255);
            doc.setLineWidth(0.5);
            doc.line(145, ySidebar, 205, ySidebar);
            ySidebar += 8;
            
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.text('Enlaces', 145, ySidebar);
            ySidebar += 8;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            
            if (perfil.linkedin) {
                const linkedinLines = doc.splitTextToSize(perfil.linkedin, 60);
                doc.text(linkedinLines, 145, ySidebar);
                ySidebar += (linkedinLines.length * 5) + 4;
            }
            
            if (perfil.github) {
                const githubLines = doc.splitTextToSize(perfil.github, 60);
                doc.text(githubLines, 145, ySidebar);
            }
        }
    }
    
    addCorporativaSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            // Mantener sidebar
            doc.setFillColor(25, 55, 109);
            doc.rect(140, 0, 70, 297, 'F');
            y = 20;
        }
        
        // Título de sección
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(25, 55, 109);
        doc.text(title, 20, y);
        y += 8;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach(item => {
            if (y > 265) {
                doc.addPage();
                doc.setFillColor(25, 55, 109);
                doc.rect(140, 0, 70, 297, 'F');
                y = 20;
            }
            
            doc.setFontSize(12);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || 'Cargo'}`, 20, y);
                y += 5;
                doc.setFontSize(10);
                doc.setFont(undefined, 'italic');
                doc.setTextColor(80, 80, 80);
                doc.text(`${item.empresa || 'Empresa'}`, 20, y);
                y += 4;
            } else {
                doc.text(item.titulo || item.nombre || '', 20, y);
                y += 5;
            }
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(120, 120, 120);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 20, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 20, y);
            }
            y += 5;
            
            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 110);
                doc.text(lineas, 20, y);
                y += (lineas.length * 5);
            }
            
            y += 8;
        });
        
        return y;
    }
    
    // Plantilla Técnica - Sidebar gris/carbón a la izquierda
    generateTecnicaTemplate(doc) {
        const perfil = this.portfolioData.perfil;
        const config = this.portfolioData.configuracion;
        
        // Sidebar gris oscuro/carbón
        doc.setFillColor(52, 58, 64); // Gris carbón
        doc.rect(0, 0, 65, 297, 'F');
        
        // Nombre y contacto en sidebar
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(18);
        doc.setFont(undefined, 'bold');
        const nombreLines = doc.splitTextToSize(perfil.nombre || 'Nombre', 55);
        doc.text(nombreLines, 8, 20);
        
        let ySidebar = 20 + (nombreLines.length * 7) + 8;
        
        // Contacto compacto con etiquetas
        doc.setFontSize(9);
        doc.setFont(undefined, 'bold');
        doc.text('CONTACTO', 8, ySidebar);
        ySidebar += 7;
        
        doc.setFontSize(8);
        doc.setFont(undefined, 'normal');
        
        if (perfil.telefono) {
            doc.setFont(undefined, 'bold');
            doc.text('Tel:', 8, ySidebar);
            doc.setFont(undefined, 'normal');
            doc.text(perfil.telefono, 18, ySidebar);
            ySidebar += 6;
        }
        
        if (perfil.email) {
            doc.setFont(undefined, 'bold');
            doc.text('Email:', 8, ySidebar);
            ySidebar += 4;
            doc.setFont(undefined, 'normal');
            const emailLines = doc.splitTextToSize(perfil.email, 55);
            doc.text(emailLines, 8, ySidebar);
            ySidebar += (emailLines.length * 4) + 3;
        }
        
        if (perfil.linkedin) {
            doc.setFont(undefined, 'bold');
            doc.text('LinkedIn:', 8, ySidebar);
            ySidebar += 4;
            doc.setFont(undefined, 'normal');
            const linkedinLines = doc.splitTextToSize(perfil.linkedin, 55);
            doc.text(linkedinLines, 8, ySidebar);
            ySidebar += (linkedinLines.length * 4) + 3;
        }
        
        if (perfil.github) {
            doc.setFont(undefined, 'bold');
            doc.text('GitHub:', 8, ySidebar);
            ySidebar += 4;
            doc.setFont(undefined, 'normal');
            const githubLines = doc.splitTextToSize(perfil.github, 55);
            doc.text(githubLines, 8, ySidebar);
            ySidebar += (githubLines.length * 4) + 8;
        }
        
        // Datos académicos en sidebar
        if (perfil.carrera || perfil.campus) {
            doc.setDrawColor(255, 255, 255);
            doc.setLineWidth(0.3);
            doc.line(8, ySidebar, 57, ySidebar);
            ySidebar += 6;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'bold');
            doc.text('EDUCACIÓN', 8, ySidebar);
            ySidebar += 6;
            
            doc.setFontSize(8);
            doc.setFont(undefined, 'normal');
            
            if (perfil.carrera) {
                const carreraLines = doc.splitTextToSize(perfil.carrera, 55);
                doc.text(carreraLines, 8, ySidebar);
                ySidebar += (carreraLines.length * 5) + 3;
            }
            
            if (perfil.campus) {
                const campusLines = doc.splitTextToSize(perfil.campus, 55);
                doc.text(campusLines, 8, ySidebar);
                ySidebar += (campusLines.length * 5);
            }
        }
        
        // Contenido principal
        doc.setTextColor(0, 0, 0);
        let y = 20;
        
        // Título profesional grande
        doc.setFontSize(22);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(52, 58, 64);
        const tituloLines = doc.splitTextToSize(config.tituloProfesional || perfil.tituloProfesional || 'Título Profesional', 135);
        doc.text(tituloLines, 73, y);
        y += (tituloLines.length * 8) + 10;
        
        // Resumen profesional
        if (config.resumenProfesional || perfil.resumenProfesional) {
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(52, 58, 64);
            doc.text('RESUMEN PROFESIONAL', 73, y);
            y += 8;
            
            doc.setFontSize(10);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            const resumen = config.resumenProfesional || perfil.resumenProfesional;
            const lineasResumen = doc.splitTextToSize(resumen, 130);
            doc.text(lineasResumen, 73, y);
            y += (lineasResumen.length * 5) + 12;
        }
        
        // Secciones
        if (this.portfolioData.experiencias.length > 0) {
            y = this.addTecnicaSection(doc, 'EXPERIENCIA', this.portfolioData.experiencias, y, 'experiencia');
        }
        
        if (this.portfolioData.proyectos.length > 0) {
            y = this.addTecnicaSection(doc, 'PROYECTOS', this.portfolioData.proyectos, y, 'proyecto');
        }
        
        if (this.portfolioData.logros.length > 0) {
            y = this.addTecnicaSection(doc, 'FORMACIÓN ACADÉMICA', this.portfolioData.logros, y, 'logro');
        }
    }
    
    addTecnicaSection(doc, title, items, startY, type) {
        let y = startY;
        
        if (y > 250) {
            doc.addPage();
            // Mantener sidebar
            doc.setFillColor(52, 58, 64);
            doc.rect(0, 0, 65, 297, 'F');
            y = 20;
        }
        
        // Título de sección
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(52, 58, 64);
        doc.text(title, 73, y);
        y += 2;
        
        // Línea bajo título
        doc.setDrawColor(52, 58, 64);
        doc.setLineWidth(2);
        doc.line(73, y, 105, y);
        y += 10;
        
        doc.setTextColor(0, 0, 0);
        
        items.forEach(item => {
            if (y > 265) {
                doc.addPage();
                doc.setFillColor(52, 58, 64);
                doc.rect(0, 0, 65, 297, 'F');
                y = 20;
            }
            
            doc.setFontSize(11);
            doc.setFont(undefined, 'bold');
            
            if (type === 'experiencia') {
                doc.text(`${item.cargo || 'Cargo'}`, 73, y);
                y += 5;
                doc.setFontSize(10);
                doc.setFont(undefined, 'normal');
                doc.setTextColor(100, 100, 100);
                doc.text(`${item.empresa || 'Empresa'}`, 73, y);
                y += 4;
            } else {
                doc.text(item.titulo || item.nombre || '', 73, y);
                y += 5;
            }
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'italic');
            doc.setTextColor(120, 120, 120);
            if (item.fechaInicio) {
                doc.text(`${this.formatDate(item.fechaInicio)} - ${item.fechaFin ? this.formatDate(item.fechaFin) : 'Actual'}`, 73, y);
            } else if (item.fecha) {
                doc.text(this.formatDate(item.fecha), 73, y);
            }
            y += 5;
            
            doc.setFontSize(9);
            doc.setFont(undefined, 'normal');
            doc.setTextColor(0, 0, 0);
            if (item.descripcion) {
                const lineas = doc.splitTextToSize(item.descripcion, 130);
                doc.text(lineas, 73, y);
                y += (lineas.length * 4.5);
            }
            
            y += 8;
        });
        
        return y;
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
            </div>
        `;
    }
    
    // === TEMPLATE SELECTION ===
    selectTemplate(templateName) {
        // Remove active class from all cards
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.remove('active');
        });
        
        // Add active class to selected card
        const selectedCard = document.querySelector(`[data-template="${templateName}"]`);
        if (selectedCard) {
            selectedCard.classList.add('active');
        }
        
        // Save template selection
        this.portfolioData.configuracion.plantilla = templateName;
        this.savePortfolioData();
        
        this.showToast(`Plantilla "${templateName}" seleccionada`, 'success');
        
        if (window.playSound) {
            window.playSound('click');
        }
    }
    
    // === UTILIDADES ===
    getSectionIcon(sectionName) {
        const icons = {
            logros: 'trophy',
            proyectos: 'code',
            experiencias: 'briefcase'
        };
        return icons[sectionName] || 'file';
    }
    
    getSectionTitle(sectionName) {
        const titles = {
            logros: 'Logros',
            proyectos: 'Proyectos',
            experiencias: 'Experiencias'
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
