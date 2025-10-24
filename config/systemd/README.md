# Servicios Systemd para StudentsPoint

Este directorio contiene los archivos de configuración de systemd para ejecutar StudentsPoint en producción Linux.

## Servicios Disponibles

### 1. studentspoint-gunicorn.service
Servicio principal que ejecuta la aplicación Django con Gunicorn.

### 2. studentspoint-monitor.service
Servicio que monitorea los logs en tiempo real y detecta problemas.

### 3. studentspoint-alerts.service
Servicio que ejecuta verificaciones cada 5 minutos y envía alertas.

### 4. studentspoint-celery.service (Opcional)
Worker de Celery para tareas asíncronas.

## Instalación

```bash
# Copiar archivos de servicio
sudo cp config/systemd/*.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicios para inicio automático
sudo systemctl enable studentspoint-gunicorn.service
sudo systemctl enable studentspoint-monitor.service
sudo systemctl enable studentspoint-alerts.service

# Iniciar servicios
sudo systemctl start studentspoint-gunicorn.service
sudo systemctl start studentspoint-monitor.service
sudo systemctl start studentspoint-alerts.service
```

## Comandos Útiles

```bash
# Ver estado de servicios
sudo systemctl status studentspoint-gunicorn
sudo systemctl status studentspoint-monitor
sudo systemctl status studentspoint-alerts

# Ver logs
sudo journalctl -u studentspoint-gunicorn -f
sudo journalctl -u studentspoint-monitor -f
sudo journalctl -u studentspoint-alerts -f

# Reiniciar servicios
sudo systemctl restart studentspoint-gunicorn
sudo systemctl restart studentspoint-monitor

# Detener servicios
sudo systemctl stop studentspoint-gunicorn
sudo systemctl stop studentspoint-monitor
sudo systemctl stop studentspoint-alerts

# Deshabilitar inicio automático
sudo systemctl disable studentspoint-gunicorn
```

## Verificación

```bash
# Verificar que todos los servicios están corriendo
systemctl list-units --type=service | grep studentspoint
```

Deberías ver:
```
studentspoint-gunicorn.service    loaded active running StudentsPoint Gunicorn daemon
studentspoint-monitor.service     loaded active running StudentsPoint Log Monitor
studentspoint-alerts.service      loaded active running StudentsPoint Alert System
```

## Troubleshooting

### El servicio no inicia

```bash
# Ver logs detallados
sudo journalctl -u studentspoint-gunicorn -n 100 --no-pager

# Verificar configuración
sudo systemctl status studentspoint-gunicorn
```

### El servicio se reinicia constantemente

```bash
# Ver por qué falla
sudo journalctl -u studentspoint-gunicorn -f

# Verificar permisos
ls -la /home/studentspoint/students-point/proyecto/src/backend/
```

### Modificar configuración

```bash
# Editar servicio
sudo nano /etc/systemd/system/studentspoint-gunicorn.service

# Recargar después de editar
sudo systemctl daemon-reload
sudo systemctl restart studentspoint-gunicorn
```

