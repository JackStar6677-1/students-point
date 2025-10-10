#!/bin/bash
# Script para detener servicios de StudentsPoint

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Deteniendo servicios de StudentsPoint...${NC}"

# Detener monitor de logs
if [ -f /tmp/studentspoint_monitor.pid ]; then
    PID=$(cat /tmp/studentspoint_monitor.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo -e "${GREEN}[OK]${NC} Monitor de logs detenido (PID: $PID)"
    fi
    rm /tmp/studentspoint_monitor.pid
fi

# Detener sistema de alertas
if [ -f /tmp/studentspoint_alerts.pid ]; then
    PID=$(cat /tmp/studentspoint_alerts.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo -e "${GREEN}[OK]${NC} Sistema de alertas detenido (PID: $PID)"
    fi
    rm /tmp/studentspoint_alerts.pid
fi

# Detener Gunicorn
if [ -f /tmp/studentspoint_gunicorn.pid ]; then
    PID=$(cat /tmp/studentspoint_gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo -e "${GREEN}[OK]${NC} Gunicorn detenido (PID: $PID)"
    fi
    rm /tmp/studentspoint_gunicorn.pid
fi

# Buscar y detener cualquier proceso restante
echo -e "${YELLOW}Buscando procesos restantes...${NC}"
pkill -f "monitor_logs.py" 2>/dev/null && echo -e "${GREEN}[OK]${NC} Procesos de monitor detenidos"
pkill -f "alert_system.py" 2>/dev/null && echo -e "${GREEN}[OK]${NC} Procesos de alertas detenidos"
pkill -f "gunicorn.*studentspoint" 2>/dev/null && echo -e "${GREEN}[OK]${NC} Procesos de Gunicorn detenidos"

echo -e "${GREEN}Todos los servicios han sido detenidos${NC}"

