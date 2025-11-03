// Conversor de Documentos - StudentsPoint

let wordFile = null;
let pdfFile = null;

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    loadHistory();
    setupFileInputs();
    setupDragAndDrop();
});

// Configurar inputs de archivo
function setupFileInputs() {
    document.getElementById('wordInput').addEventListener('change', (e) => {
        handleWordFile(e.target.files[0]);
    });
    
    document.getElementById('pdfInput').addEventListener('change', (e) => {
        handlePdfFile(e.target.files[0]);
    });
}

// Configurar drag and drop
function setupDragAndDrop() {
    const wordZone = document.getElementById('uploadZoneWord');
    const pdfZone = document.getElementById('uploadZonePdf');
    
    setupDragZone(wordZone, 'wordInput', handleWordFile);
    setupDragZone(pdfZone, 'pdfInput', handlePdfFile);
}

function setupDragZone(zone, inputId, handler) {
    zone.addEventListener('click', () => {
        document.getElementById(inputId).click();
    });
    
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('dragover');
    });
    
    zone.addEventListener('dragleave', () => {
        zone.classList.remove('dragover');
    });
    
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handler(e.dataTransfer.files[0]);
        }
    });
}

// Constantes de validación
const MAX_FILE_SIZE_MB = 50;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

// Manejar archivo Word
function handleWordFile(file) {
    if (!file) return;
    
    // Validar extensión
    if (!file.name.match(/\.(doc|docx)$/i)) {
        showAlert('Por favor selecciona un archivo Word (.doc o .docx)', 'danger');
        return;
    }
    
    // Validar tamaño
    if (file.size > MAX_FILE_SIZE_BYTES) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        showAlert(`El archivo es demasiado grande (${sizeMB} MB). Tamaño máximo: ${MAX_FILE_SIZE_MB} MB`, 'danger');
        return;
    }
    
    // Validar que no esté vacío
    if (file.size === 0) {
        showAlert('El archivo está vacío', 'danger');
        return;
    }
    
    wordFile = file;
    document.getElementById('uploadZoneWord').style.display = 'none';
    document.getElementById('wordFileInfo').style.display = 'block';
    document.getElementById('wordFileName').textContent = file.name;
    document.getElementById('wordFileSize').textContent = formatFileSize(file.size);
}

// Manejar archivo PDF
function handlePdfFile(file) {
    if (!file) return;
    
    // Validar extensión
    if (!file.name.match(/\.pdf$/i)) {
        showAlert('Por favor selecciona un archivo PDF', 'danger');
        return;
    }
    
    // Validar tamaño
    if (file.size > MAX_FILE_SIZE_BYTES) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        showAlert(`El archivo es demasiado grande (${sizeMB} MB). Tamaño máximo: ${MAX_FILE_SIZE_MB} MB`, 'danger');
        return;
    }
    
    // Validar que no esté vacío
    if (file.size === 0) {
        showAlert('El archivo está vacío', 'danger');
        return;
    }
    
    pdfFile = file;
    document.getElementById('uploadZonePdf').style.display = 'none';
    document.getElementById('pdfFileInfo').style.display = 'block';
    document.getElementById('pdfFileName').textContent = file.name;
    document.getElementById('pdfFileSize').textContent = formatFileSize(file.size);
}

// Limpiar selección de archivo
function clearWordFile() {
    wordFile = null;
    document.getElementById('wordInput').value = '';
    document.getElementById('uploadZoneWord').style.display = 'block';
    document.getElementById('wordFileInfo').style.display = 'none';
}

function clearPdfFile() {
    pdfFile = null;
    document.getElementById('pdfInput').value = '';
    document.getElementById('uploadZonePdf').style.display = 'block';
    document.getElementById('pdfFileInfo').style.display = 'none';
}

// Convertir Word a PDF
async function convertWordToPdf() {
    if (!wordFile) {
        showAlert('Por favor selecciona un archivo Word primero', 'warning');
        return;
    }
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        showAlert('Debes iniciar sesión para usar el conversor', 'warning');
        window.location.href = '/login.html';
        return;
    }
    
    console.log('Iniciando conversión Word a PDF...');
    showProgress();
    
    const formData = new FormData();
    formData.append('archivo_original', wordFile);
    formData.append('tipo_conversion', 'word_to_pdf');
    formData.append('usar_ocr', 'false');
    
    try {
        updateProgress(20, 'Subiendo archivo...');
        
        console.log('Enviando archivo al servidor...');
        
        // Crear AbortController para timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutos timeout
        
        const response = await fetch('/api/converter/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log('Respuesta del servidor:', response.status, response.statusText);
        
        updateProgress(50, 'Procesando documento...');
        
        if (!response.ok) {
            let errorMsg = `Error del servidor (${response.status})`;
            try {
                const errorData = await response.json();
                errorMsg = errorData.archivo_original?.[0] || errorData.detail || errorData.error || errorMsg;
            } catch {
                try {
                    const errorText = await response.text();
                    errorMsg = errorText || errorMsg;
                } catch {
                    // Usar mensaje por defecto
                }
            }
            throw new Error(errorMsg);
        }
        
        const data = await response.json();
        console.log('Datos recibidos:', data);
        
        if (!data || !data.id) {
            throw new Error('Respuesta inválida del servidor');
        }
        
        updateProgress(80, 'Generando PDF...');
        
        // Esperar a que se complete
        await waitForCompletion(data.id);
        
        updateProgress(100, 'Completado');
        
        setTimeout(() => {
            showResult(data.id);
            loadHistory();
        }, 500);
        
    } catch (error) {
        console.error('Error completo:', error);
        
        let errorMessage = 'Error al convertir el archivo';
        if (error.name === 'AbortError') {
            errorMessage = 'Tiempo de espera agotado. Por favor, intenta con un archivo más pequeño.';
        } else if (error.message) {
            errorMessage = error.message;
        } else if (error instanceof TypeError && error.message.includes('fetch')) {
            errorMessage = 'Error de conexión. Por favor, verifica tu conexión a internet e intenta de nuevo.';
        }
        
        showAlert(errorMessage, 'danger');
        resetConverter();
    }
}

// Convertir PDF a Word
async function convertPdfToWord() {
    if (!pdfFile) {
        showAlert('Por favor selecciona un archivo PDF primero', 'warning');
        return;
    }
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        showAlert('Debes iniciar sesión para usar el conversor', 'warning');
        window.location.href = '/login.html';
        return;
    }
    
    console.log('Iniciando conversión PDF a Word...');
    showProgress();
    
    const useOcr = document.getElementById('useOcr').checked;
    
    const formData = new FormData();
    formData.append('archivo_original', pdfFile);
    formData.append('tipo_conversion', 'pdf_to_word');
    formData.append('usar_ocr', useOcr ? 'true' : 'false');
    
    try {
        updateProgress(20, 'Subiendo archivo...');
        
        console.log('Enviando archivo al servidor...');
        
        // Crear AbortController para timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutos timeout
        
        const response = await fetch('/api/converter/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log('Respuesta del servidor:', response.status, response.statusText);
        
        updateProgress(50, useOcr ? 'Aplicando OCR...' : 'Extrayendo texto...');
        
        if (!response.ok) {
            let errorMsg = `Error del servidor (${response.status})`;
            try {
                const errorData = await response.json();
                errorMsg = errorData.archivo_original?.[0] || errorData.detail || errorData.error || errorMsg;
            } catch {
                try {
                    const errorText = await response.text();
                    errorMsg = errorText || errorMsg;
                } catch {
                    // Usar mensaje por defecto
                }
            }
            throw new Error(errorMsg);
        }
        
        const data = await response.json();
        console.log('Datos recibidos:', data);
        
        if (!data || !data.id) {
            throw new Error('Respuesta inválida del servidor');
        }
        
        updateProgress(80, 'Generando Word...');
        
        // Esperar a que se complete
        await waitForCompletion(data.id);
        
        updateProgress(100, 'Completado');
        
        setTimeout(() => {
            showResult(data.id);
            loadHistory();
        }, 500);
        
    } catch (error) {
        console.error('Error completo:', error);
        
        let errorMessage = 'Error al convertir el archivo';
        if (error.name === 'AbortError') {
            errorMessage = 'Tiempo de espera agotado. Por favor, intenta con un archivo más pequeño.';
        } else if (error.message) {
            errorMessage = error.message;
        } else if (error instanceof TypeError && error.message.includes('fetch')) {
            errorMessage = 'Error de conexión. Por favor, verifica tu conexión a internet e intenta de nuevo.';
        }
        
        showAlert(errorMessage, 'danger');
        resetConverter();
    }
}

// Esperar a que se complete la conversión
async function waitForCompletion(jobId) {
    const token = localStorage.getItem('access_token');
    let attempts = 0;
    const maxAttempts = 60; // Aumentado a 60 intentos (60 segundos)
    
    console.log(`Esperando completar conversión ${jobId}...`);
    
    while (attempts < maxAttempts) {
        try {
            // Crear timeout para cada request
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            const response = await fetch(`/api/converter/${jobId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('El trabajo de conversión no se encontró');
                }
                throw new Error(`Error verificando estado: ${response.status}`);
            }
            
            const data = await response.json();
            console.log(`Estado de conversión ${jobId}:`, data.estado);
            
            if (data.estado === 'completado') {
                console.log('Conversión completada exitosamente');
                return data;
            } else if (data.estado === 'error') {
                const errorMsg = data.error_mensaje || 'Error en la conversión';
                throw new Error(errorMsg);
            }
            
            // Actualizar progreso basado en intentos
            const progress = Math.min(80 + (attempts * 0.33), 95);
            updateProgress(progress, `Procesando... (${attempts + 1}/${maxAttempts})`);
            
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
            
        } catch (error) {
            console.error(`Error verificando estado (intento ${attempts + 1}):`, error);
            
            // Si es un error de conexión, esperar un poco más antes de reintentar
            if (error.name === 'TimeoutError' || error.message.includes('fetch')) {
                await new Promise(resolve => setTimeout(resolve, 2000));
            } else {
                // Para otros errores, lanzar inmediatamente
                if (error.message.includes('Error en la conversión') || error.message.includes('no se encontró')) {
                    throw error;
                }
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            
            attempts++;
        }
    }
    
    throw new Error('Tiempo de espera agotado. La conversión está tomando más tiempo del esperado. Por favor, intenta con un archivo más pequeño.');
}

// Cargar historial
async function loadHistory() {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    
    try {
        const response = await fetch('/api/converter/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Error cargando historial');
        
        const jobs = await response.json();
        renderHistory(jobs);
        
    } catch (error) {
        console.error('Error cargando historial:', error);
        document.getElementById('historyList').innerHTML = `
            <div class="text-center py-5">
                <p class="text-muted">No se pudo cargar el historial</p>
            </div>
        `;
    }
}

// Renderizar historial
function renderHistory(jobs) {
    const container = document.getElementById('historyList');
    
    if (jobs.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                <p class="text-muted">No hay conversiones aun</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = jobs.map(job => `
        <div class="history-item">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center gap-2 mb-2">
                        <i class="fas ${job.tipo_conversion === 'word_to_pdf' ? 'fa-file-pdf' : 'fa-file-word'}"></i>
                        <strong>${job.tipo_conversion_display}</strong>
                        <span class="status-badge ${job.estado}">${job.estado_display}</span>
                    </div>
                    <p class="text-muted small mb-1">
                        ${new Date(job.created_at).toLocaleString('es-CL')}
                    </p>
                    ${job.usar_ocr ? '<span class="badge bg-info">OCR</span>' : ''}
                </div>
                <div class="d-flex gap-2">
                    ${job.archivo_convertido_url ? `
                        <a href="${job.archivo_convertido_url}" class="btn btn-sm btn-gradient-gold" download>
                            <i class="fas fa-download"></i>
                        </a>
                    ` : ''}
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteJob(${job.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            ${job.error_mensaje ? `<p class="text-danger small mt-2 mb-0">${job.error_mensaje}</p>` : ''}
        </div>
    `).join('');
}

// Eliminar trabajo
async function deleteJob(jobId) {
    if (!confirm('¿Eliminar esta conversion?')) return;
    
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`/api/converter/${jobId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Conversion eliminada', 'success');
            loadHistory();
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al eliminar', 'danger');
    }
}

// Mostrar progreso
function showProgress() {
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    updateProgress(0, 'Iniciando...');
}

// Actualizar progreso
function updateProgress(percent, status) {
    const bar = document.getElementById('progressBar');
    const text = document.getElementById('progressText');
    const statusText = document.getElementById('progressStatus');
    
    bar.style.width = percent + '%';
    text.textContent = Math.round(percent) + '%';
    statusText.textContent = status;
}

// Mostrar resultado
async function showResult(jobId) {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`/api/converter/${jobId}/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('resultSection').style.display = 'block';
        
        const downloadLink = document.getElementById('downloadLink');
        downloadLink.href = data.archivo_convertido_url;
        
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al obtener el archivo convertido', 'danger');
    }
}

// Resetear conversor
function resetConverter() {
    clearWordFile();
    clearPdfFile();
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
}

// Formatear tamaño de archivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Mostrar alerta
function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5`;
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => alert.remove(), 5000);
}

// Autenticación
async function initAuth() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        document.querySelector('.user-menu').style.display = 'none';
        document.querySelector('.auth-buttons').style.display = 'block';
        return;
    }
    
    try {
        const response = await fetch('/api/auth/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            document.querySelector('.user-name').textContent = user.name;
            document.querySelector('.user-menu').style.display = 'flex';
            document.querySelector('.auth-buttons').style.display = 'none';
        } else {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    } catch (error) {
        console.error('Error verificando auth:', error);
    }
}

// Logout
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login.html';
        });
    }
});

