#!/usr/bin/env python
"""
Sistema de alertas para StudentsPoint
Detecta problemas críticos y envía notificaciones
"""
import os
import sys
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

class AlertSystem:
    """Sistema de alertas para monitoreo del sistema"""
    
    def __init__(self):
        self.logs_dir = Path('logs')
        self.alert_email = getattr(settings, 'ALERT_EMAIL', 'admin@studentspoint.app')
        self.thresholds = {
            'errors_per_hour': 50,
            'critical_per_hour': 5,
            'response_time': 2.0,  # segundos
            'database_errors': 10,
            'auth_failures': 20,
        }
    
    def check_error_rate(self):
        """Verifica la tasa de errores"""
        try:
            # Leer últimas líneas del error log
            with open(self.logs_dir / 'errors.log', 'r') as f:
                lines = f.readlines()[-100:]  # Últimas 100 líneas
            
            # Contar errores en la última hora
            hour_ago = datetime.now() - timedelta(hours=1)
            recent_errors = 0
            critical_errors = 0
            
            for line in lines:
                if '[ERROR]' in line or '[CRITICAL]' in line:
                    # Parsear timestamp
                    try:
                        timestamp_str = line.split(']')[1].strip().split()[0:2]
                        timestamp = datetime.strptime(' '.join(timestamp_str), '%Y-%m-%d %H:%M:%S')
                        
                        if timestamp > hour_ago:
                            recent_errors += 1
                            if '[CRITICAL]' in line:
                                critical_errors += 1
                    except:
                        continue
            
            # Verificar umbrales
            alerts = []
            if recent_errors > self.thresholds['errors_per_hour']:
                alerts.append({
                    'level': 'HIGH',
                    'message': f'Tasa de errores elevada: {recent_errors} errores en la última hora (umbral: {self.thresholds["errors_per_hour"]})'
                })
            
            if critical_errors > self.thresholds['critical_per_hour']:
                alerts.append({
                    'level': 'CRITICAL',
                    'message': f'Errores críticos detectados: {critical_errors} en la última hora (umbral: {self.thresholds["critical_per_hour"]})'
                })
            
            return alerts
            
        except FileNotFoundError:
            return []
    
    def check_database_health(self):
        """Verifica la salud de la base de datos"""
        from django.db import connection
        
        alerts = []
        
        try:
            # Verificar conexión
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                
            # Verificar número de conexiones
            if hasattr(connection, 'queries'):
                query_count = len(connection.queries)
                if query_count > 100:
                    alerts.append({
                        'level': 'WARNING',
                        'message': f'Alto número de queries: {query_count}'
                    })
                    
        except Exception as e:
            alerts.append({
                'level': 'CRITICAL',
                'message': f'Error de conexión a base de datos: {str(e)}'
            })
        
        return alerts
    
    def check_disk_space(self):
        """Verifica el espacio en disco"""
        import shutil
        
        alerts = []
        
        try:
            total, used, free = shutil.disk_usage("/")
            percent_used = (used / total) * 100
            
            if percent_used > 90:
                alerts.append({
                    'level': 'CRITICAL',
                    'message': f'Espacio en disco crítico: {percent_used:.1f}% usado'
                })
            elif percent_used > 80:
                alerts.append({
                    'level': 'WARNING',
                    'message': f'Espacio en disco bajo: {percent_used:.1f}% usado'
                })
                
        except Exception as e:
            logger.error(f"Error verificando espacio en disco: {e}")
        
        return alerts
    
    def send_alert(self, alerts):
        """Envía alerta por email"""
        if not alerts:
            return
        
        # Agrupar por nivel
        critical = [a for a in alerts if a['level'] == 'CRITICAL']
        high = [a for a in alerts if a['level'] == 'HIGH']
        warning = [a for a in alerts if a['level'] == 'WARNING']
        
        # Construir mensaje
        subject = f" Alerta StudentsPoint - {len(critical)} críticas, {len(high)} altas"
        
        body = f"""
        <html>
        <body>
        <h2> Alertas del Sistema StudentsPoint</h2>
        <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        """
        
        if critical:
            body += "<h3 style='color: red;'> CRÍTICAS</h3><ul>"
            for alert in critical:
                body += f"<li>{alert['message']}</li>"
            body += "</ul>"
        
        if high:
            body += "<h3 style='color: orange;'> ALTAS</h3><ul>"
            for alert in high:
                body += f"<li>{alert['message']}</li>"
            body += "</ul>"
        
        if warning:
            body += "<h3 style='color: yellow;'> ADVERTENCIAS</h3><ul>"
            for alert in warning:
                body += f"<li>{alert['message']}</li>"
            body += "</ul>"
        
        body += """
        <hr>
        <p><em>Este es un mensaje automático del sistema de monitoreo de StudentsPoint.</em></p>
        </body>
        </html>
        """
        
        try:
            # Enviar email
            send_mail(
                subject,
                strip_tags(body),
                settings.DEFAULT_FROM_EMAIL,
                [self.alert_email],
                html_message=body,
                fail_silently=False
            )
            logger.info(f"Alerta enviada: {subject}")
        except Exception as e:
            logger.error(f"Error enviando alerta: {e}")
            # Imprimir en consola como fallback
            print(f"\n{'='*60}")
            print(f"ALERTA: {subject}")
            print(f"{'='*60}")
            for alert in critical + high + warning:
                print(f"[{alert['level']}] {alert['message']}")
            print(f"{'='*60}\n")
    
    def run_checks(self):
        """Ejecuta todas las verificaciones"""
        print(" Ejecutando verificaciones del sistema...")
        
        all_alerts = []
        
        # Verificar tasa de errores
        print("   - Verificando tasa de errores...")
        all_alerts.extend(self.check_error_rate())
        
        # Verificar base de datos
        print("   - Verificando base de datos...")
        all_alerts.extend(self.check_database_health())
        
        # Verificar espacio en disco
        print("   - Verificando espacio en disco...")
        all_alerts.extend(self.check_disk_space())
        
        # Enviar alertas si hay problemas
        if all_alerts:
            print(f"\n  {len(all_alerts)} alertas detectadas")
            self.send_alert(all_alerts)
        else:
            print("\n Sistema funcionando correctamente")
        
        return all_alerts

def strip_tags(html):
    """Elimina tags HTML del texto"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

def main():
    """Función principal"""
    alert_system = AlertSystem()
    alerts = alert_system.run_checks()
    
    # Retornar código de salida según alertas
    if any(a['level'] == 'CRITICAL' for a in alerts):
        sys.exit(2)
    elif any(a['level'] == 'HIGH' for a in alerts):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

