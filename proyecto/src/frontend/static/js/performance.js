/**
 * Performance Monitor para StudentsPoint
 * Monitorea y optimiza el rendimiento del frontend
 */

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            pageLoad: 0,
            apiCalls: [],
            renderTimes: []
        };
        
        this.init();
    }

    init() {
        // Medir tiempo de carga de página
        window.addEventListener('load', () => {
            this.measurePageLoad();
        });

        // Interceptar fetch para medir APIs
        this.interceptFetch();
    }

    measurePageLoad() {
        if ('performance' in window && 'timing' in performance) {
            const timing = performance.timing;
            const pageLoad = timing.loadEventEnd - timing.navigationStart;
            this.metrics.pageLoad = pageLoad;

            // Métricas detalladas
            const metrics = {
                'DNS': timing.domainLookupEnd - timing.domainLookupStart,
                'TCP': timing.connectEnd - timing.connectStart,
                'Request': timing.responseStart - timing.requestStart,
                'Response': timing.responseEnd - timing.responseStart,
                'DOM Processing': timing.domInteractive - timing.responseEnd,
                'DOM Complete': timing.domComplete - timing.domInteractive,
                'Load Event': timing.loadEventEnd - timing.loadEventStart
            };

            console.group(' Performance Metrics');
            console.log(`⏱ Total Page Load: ${pageLoad}ms`);
            Object.entries(metrics).forEach(([key, value]) => {
                console.log(`   ${key}: ${value}ms`);
            });
            console.groupEnd();

            // Advertir si la carga es lenta
            if (pageLoad > 3000) {
                console.warn(' Carga de página lenta detectada (>3s)');
                this.suggestOptimizations();
            }
        }
    }

    interceptFetch() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = function(...args) {
            const startTime = performance.now();
            const url = args[0];

            return originalFetch.apply(this, args).then(response => {
                const endTime = performance.now();
                const duration = endTime - startTime;

                // Registrar llamada API
                self.metrics.apiCalls.push({
                    url,
                    duration,
                    status: response.status,
                    timestamp: new Date()
                });

                // Advertir sobre APIs lentas
                if (duration > 1000) {
                    console.warn(` API lenta detectada: ${url} (${duration.toFixed(0)}ms)`);
                }

                return response;
            });
        };
    }

    measureRenderTime(componentName, callback) {
        const startTime = performance.now();
        
        const result = callback();
        
        const endTime = performance.now();
        const duration = endTime - startTime;

        this.metrics.renderTimes.push({
            component: componentName,
            duration,
            timestamp: new Date()
        });

        if (duration > 16) { // 60fps = 16ms por frame
            console.warn(` Render lento: ${componentName} (${duration.toFixed(2)}ms)`);
        }

        return result;
    }

    getReport() {
        const avgApiTime = this.metrics.apiCalls.length > 0
            ? this.metrics.apiCalls.reduce((sum, call) => sum + call.duration, 0) / this.metrics.apiCalls.length
            : 0;

        const slowApis = this.metrics.apiCalls.filter(call => call.duration > 1000);

        return {
            pageLoadTime: this.metrics.pageLoad,
            totalApiCalls: this.metrics.apiCalls.length,
            averageApiTime: avgApiTime.toFixed(0),
            slowApiCalls: slowApis.length,
            totalRenders: this.metrics.renderTimes.length,
            slowApis: slowApis.map(api => ({
                url: api.url,
                duration: `${api.duration.toFixed(0)}ms`
            }))
        };
    }

    printReport() {
        const report = this.getReport();

        console.group(' Performance Report');
        console.log(`Page Load: ${report.pageLoadTime}ms`);
        console.log(`API Calls: ${report.totalApiCalls} (avg: ${report.averageApiTime}ms)`);
        console.log(`Slow APIs: ${report.slowApiCalls}`);
        
        if (report.slowApis.length > 0) {
            console.group(' Slow API Calls:');
            report.slowApis.forEach(api => {
                console.log(`   ${api.url}: ${api.duration}`);
            });
            console.groupEnd();
        }
        
        console.groupEnd();
    }

    suggestOptimizations() {
        const report = this.getReport();
        const suggestions = [];

        if (report.pageLoadTime > 3000) {
            suggestions.push('• Considera usar lazy loading para imágenes');
            suggestions.push('• Minifica y comprime assets CSS/JS');
        }

        if (report.slowApiCalls > 0) {
            suggestions.push('• Implementa caché para APIs lentas');
            suggestions.push('• Considera paginación o lazy loading de datos');
        }

        if (suggestions.length > 0) {
            console.group(' Sugerencias de Optimización:');
            suggestions.forEach(s => console.log(s));
            console.groupEnd();
        }
    }

    // Debounce helper para optimizar eventos
    debounce(func, wait) {
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

    // Throttle helper para optimizar scroll/resize
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Instancia global
const perfMonitor = new PerformanceMonitor();

// Exportar helpers globalmente
window.debounce = perfMonitor.debounce;
window.throttle = perfMonitor.throttle;

// Mostrar reporte después de 5 segundos
setTimeout(() => {
    if (window.location.search.includes('debug=performance')) {
        perfMonitor.printReport();
    }
}, 5000);

