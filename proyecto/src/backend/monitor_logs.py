#!/usr/bin/env python
"""
Script de monitoreo de logs en tiempo real
Detecta errores críticos y envía notificaciones
"""
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LogMonitor:
    def __init__(self, logs_dir='logs'):
        self.logs_dir = Path(logs_dir)
        self.error_counts = defaultdict(int)
        self.last_check = defaultdict(int)
        self.critical_keywords = [
            'CRITICAL',
            'Database',
            'Connection',
            'Memory',
            'Exception',
            'Traceback',
        ]
        
    def count_errors(self, log_file, level='ERROR'):
        """Cuenta errores en un archivo de log"""
        try:
            result = subprocess.run(
                ['grep', '-c', level, str(self.logs_dir / log_file)],
                capture_output=True,
                text=True
            )
            return int(result.stdout.strip()) if result.returncode == 0 else 0
        except:
            # Fallback para Windows
            try:
                with open(self.logs_dir / log_file, 'r', encoding='utf-8') as f:
                    return sum(1 for line in f if level in line)
            except FileNotFoundError:
                return 0
            
    def get_recent_errors(self, log_file, lines=10):
        """Obtiene los últimos errores del log"""
        try:
            result = subprocess.run(
                ['tail', '-n', str(lines), str(self.logs_dir / log_file)],
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else ""
        except:
            # Fallback para Windows
            try:
                with open(self.logs_dir / log_file, 'r', encoding='utf-8') as f:
                    lines_list = f.readlines()
                    return ''.join(lines_list[-lines:])
            except FileNotFoundError:
                return ""
    
    def check_for_critical(self, log_file):
        """Verifica si hay errores críticos nuevos"""
        recent = self.get_recent_errors(log_file, 50)
        critical_issues = []
        
        for keyword in self.critical_keywords:
            if keyword in recent:
                critical_issues.append(keyword)
        
        return critical_issues
    
    def print_summary(self):
        """Imprime resumen del estado de los logs"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD} Resumen de Logs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")
        
        # Verificar archivos
        log_files = {
            'general.log': 'General',
            'errors.log': 'Errores',
            'api.log': 'API',
            'auth.log': 'Autenticación'
        }
        
        for log_file, name in log_files.items():
            if not (self.logs_dir / log_file).exists():
                print(f"{Colors.WARNING}  {name:15s} - Archivo no encontrado{Colors.ENDC}")
                continue
                
            errors = self.count_errors(log_file, 'ERROR')
            warnings = self.count_errors(log_file, 'WARNING')
            critical = self.count_errors(log_file, 'CRITICAL')
            
            # Detectar nuevos errores
            new_errors = errors - self.last_check[log_file]
            self.last_check[log_file] = errors
            
            # Determinar color según estado
            if critical > 0:
                status_color = Colors.FAIL
                status_icon = ''
            elif errors > 0:
                status_color = Colors.WARNING
                status_icon = ''
            else:
                status_color = Colors.OKGREEN
                status_icon = ''
            
            print(f"{status_color}{status_icon} {name:15s}{Colors.ENDC} - ", end='')
            print(f"Errores: {Colors.FAIL if errors > 0 else Colors.OKGREEN}{errors}{Colors.ENDC} ", end='')
            print(f"Warnings: {Colors.WARNING if warnings > 0 else Colors.OKGREEN}{warnings}{Colors.ENDC} ", end='')
            print(f"Críticos: {Colors.FAIL if critical > 0 else Colors.OKGREEN}{critical}{Colors.ENDC}")
            
            # Alertar sobre nuevos errores
            if new_errors > 0:
                print(f"   {Colors.FAIL} {new_errors} nuevos errores detectados!{Colors.ENDC}")
                critical_issues = self.check_for_critical(log_file)
                if critical_issues:
                    print(f"   {Colors.FAIL} Problemas críticos: {', '.join(critical_issues)}{Colors.ENDC}")
        
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}\n")
    
    def show_recent_errors(self, log_file='errors.log', lines=5):
        """Muestra los errores más recientes"""
        print(f"\n{Colors.BOLD} Últimos {lines} errores en {log_file}:{Colors.ENDC}\n")
        recent = self.get_recent_errors(log_file, lines)
        if recent:
            for line in recent.split('\n'):
                if 'ERROR' in line:
                    print(f"{Colors.FAIL}{line}{Colors.ENDC}")
                elif 'WARNING' in line:
                    print(f"{Colors.WARNING}{line}{Colors.ENDC}")
                elif 'CRITICAL' in line:
                    print(f"{Colors.FAIL}{Colors.BOLD}{line}{Colors.ENDC}")
                elif line.strip():
                    print(line)
        else:
            print(f"{Colors.OKGREEN} No hay errores recientes{Colors.ENDC}")
    
    def monitor_continuous(self, interval=60):
        """Monitorea logs continuamente"""
        print(f"{Colors.OKGREEN} Iniciando monitoreo continuo (intervalo: {interval}s){Colors.ENDC}")
        print(f"{Colors.OKCYAN} Presiona Ctrl+C para detener{Colors.ENDC}\n")
        
        try:
            while True:
                self.print_summary()
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}⏹  Monitoreo detenido{Colors.ENDC}\n")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor de logs de StudentsPoint')
    parser.add_argument('--dir', default='logs', help='Directorio de logs')
    parser.add_argument('--interval', type=int, default=60, help='Intervalo de monitoreo en segundos')
    parser.add_argument('--once', action='store_true', help='Ejecutar una sola vez')
    parser.add_argument('--recent', type=int, help='Mostrar N errores recientes')
    
    args = parser.parse_args()
    
    monitor = LogMonitor(args.dir)
    
    if args.recent:
        monitor.show_recent_errors(lines=args.recent)
    elif args.once:
        monitor.print_summary()
    else:
        monitor.monitor_continuous(args.interval)

if __name__ == '__main__':
    main()

