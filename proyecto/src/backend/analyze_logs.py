#!/usr/bin/env python
"""
Script de análisis de logs
Genera reportes detallados sobre el estado del sistema
"""
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict

class LogAnalyzer:
    def __init__(self, logs_dir='logs'):
        self.logs_dir = Path(logs_dir)
        self.error_patterns = {
            'auth': r'(login|register|password|token|authentication)',
            'database': r'(database|postgres|sqlite|connection|query)',
            'api': r'(api|endpoint|request|response|HTTP)',
            'permission': r'(permission|forbidden|unauthorized|403|401)',
            'not_found': r'(404|not found|does not exist)',
            'server': r'(500|internal server error|exception)',
        }
    
    def read_log_file(self, log_file):
        """Lee un archivo de log y retorna las líneas"""
        try:
            with open(self.logs_dir / log_file, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            return []
    
    def parse_log_line(self, line):
        """Parsea una línea de log y extrae información"""
        # Formato: [LEVEL] YYYY-MM-DD HH:MM:SS logger module function - message
        pattern = r'\[(\w+)\]\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(\S+)\s+-\s+(.+)'
        match = re.match(pattern, line)
        
        if match:
            return {
                'level': match.group(1),
                'timestamp': match.group(2),
                'logger': match.group(3),
                'module': match.group(4),
                'function': match.group(5),
                'message': match.group(6),
            }
        return None
    
    def categorize_error(self, message):
        """Categoriza un error según su mensaje"""
        message_lower = message.lower()
        for category, pattern in self.error_patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                return category
        return 'other'
    
    def analyze_errors(self, log_file='errors.log', last_hours=24):
        """Analiza errores en un período de tiempo"""
        lines = self.read_log_file(log_file)
        
        cutoff_time = datetime.now() - timedelta(hours=last_hours)
        errors_by_category = Counter()
        errors_by_hour = defaultdict(int)
        top_errors = []
        
        for line in lines:
            if 'ERROR' not in line and 'CRITICAL' not in line:
                continue
                
            parsed = self.parse_log_line(line)
            if not parsed:
                continue
            
            try:
                timestamp = datetime.strptime(parsed['timestamp'], '%Y-%m-%d %H:%M:%S')
                if timestamp < cutoff_time:
                    continue
                
                # Contar por categoría
                category = self.categorize_error(parsed['message'])
                errors_by_category[category] += 1
                
                # Contar por hora
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                errors_by_hour[hour_key] += 1
                
                # Guardar errores únicos
                error_summary = f"{parsed['module']}.{parsed['function']}: {parsed['message'][:100]}"
                top_errors.append(error_summary)
                
            except ValueError:
                continue
        
        return {
            'by_category': dict(errors_by_category),
            'by_hour': dict(errors_by_hour),
            'top_errors': Counter(top_errors).most_common(10),
            'total': sum(errors_by_category.values())
        }
    
    def generate_report(self, hours=24):
        """Genera un reporte completo de análisis"""
        print(f"\n{'='*70}")
        print(f" REPORTE DE ANÁLISIS DE LOGS - Últimas {hours} horas")
        print(f"{'='*70}\n")
        
        # Analizar errors.log
        analysis = self.analyze_errors('errors.log', hours)
        
        print(f" RESUMEN GENERAL")
        print(f"   Total de errores: {analysis['total']}")
        print(f"   Período: {datetime.now() - timedelta(hours=hours)} - {datetime.now()}")
        print()
        
        # Errores por categoría
        if analysis['by_category']:
            print(f" ERRORES POR CATEGORÍA:")
            for category, count in sorted(analysis['by_category'].items(), key=lambda x: x[1], reverse=True):
                bar = '' * min(count, 50)
                print(f"   {category:15s}: {bar} ({count})")
            print()
        
        # Distribución por hora
        if analysis['by_hour']:
            print(f"⏰ DISTRIBUCIÓN POR HORA:")
            for hour, count in sorted(analysis['by_hour'].items()):
                bar = '' * min(count, 50)
                print(f"   {hour}: {bar} ({count})")
            print()
        
        # Top errores
        if analysis['top_errors']:
            print(f" TOP 10 ERRORES MÁS FRECUENTES:")
            for i, (error, count) in enumerate(analysis['top_errors'], 1):
                print(f"   {i:2d}. [{count:3d}x] {error}")
            print()
        
        # Recomendaciones
        print(f" RECOMENDACIONES:")
        if analysis['by_category'].get('database', 0) > 10:
            print(f"     Alto número de errores de base de datos - revisar conexiones")
        if analysis['by_category'].get('auth', 0) > 20:
            print(f"     Muchos errores de autenticación - posible ataque o problema de configuración")
        if analysis['total'] > 100:
            print(f"     Tasa de errores elevada - requiere atención urgente")
        if analysis['total'] == 0:
            print(f"    Sistema funcionando correctamente")
        
        print(f"\n{'='*70}\n")
    
    def export_report(self, filename='log_report.txt', hours=24):
        """Exporta el reporte a un archivo"""
        import sys
        original_stdout = sys.stdout
        
        with open(filename, 'w', encoding='utf-8') as f:
            sys.stdout = f
            self.generate_report(hours)
        
        sys.stdout = original_stdout
        print(f" Reporte exportado a: {filename}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analizador de logs de StudentsPoint')
    parser.add_argument('--dir', default='logs', help='Directorio de logs')
    parser.add_argument('--hours', type=int, default=24, help='Horas a analizar')
    parser.add_argument('--export', help='Exportar reporte a archivo')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.dir)
    
    if args.export:
        analyzer.export_report(args.export, args.hours)
    else:
        analyzer.generate_report(args.hours)

if __name__ == '__main__':
    main()

