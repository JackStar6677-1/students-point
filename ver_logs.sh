#!/bin/bash
# Script para ver logs de StudentsPoint de manera amigable

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

LOGS_DIR="proyecto/src/backend/logs"

menu() {
    clear
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}   Ver Logs - StudentsPoint${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    echo "Selecciona el log que deseas ver:"
    echo ""
    echo -e "  ${GREEN}1)${NC} General (todos los eventos)"
    echo -e "  ${RED}2)${NC} Errores (solo errores)"
    echo -e "  ${CYAN}3)${NC} API (peticiones y respuestas)"
    echo -e "  ${YELLOW}4)${NC} Autenticación (login, registro, etc)"
    echo -e "  ${PURPLE}5)${NC} Monitor en Tiempo Real"
    echo -e "  ${BLUE}6)${NC} Análisis Completo"
    echo -e "  ${RED}7)${NC} Salir"
    echo ""
    read -p "Opción (1-7): " opcion
    
    case $opcion in
        1) ver_general ;;
        2) ver_errores ;;
        3) ver_api ;;
        4) ver_auth ;;
        5) monitor ;;
        6) analisis ;;
        7) exit 0 ;;
        *) 
            echo -e "${RED}Opción inválida${NC}"
            sleep 2
            menu
            ;;
    esac
}

ver_general() {
    clear
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}   Log General - Presiona Ctrl+C para volver${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/general.log" ]; then
        tail -f "$LOGS_DIR/general.log"
    else
        echo -e "${RED}[ERROR]${NC} Archivo $LOGS_DIR/general.log no encontrado"
        echo -e "${YELLOW}[INFO]${NC} Inicia el servidor primero"
        read -p "Presiona Enter para continuar..."
    fi
    menu
}

ver_errores() {
    clear
    echo -e "${RED}============================================================${NC}"
    echo -e "${RED}   Log de Errores - Presiona Ctrl+C para volver${NC}"
    echo -e "${RED}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/errors.log" ]; then
        tail -f "$LOGS_DIR/errors.log" | grep --color=always -E 'ERROR|CRITICAL|$'
    else
        echo -e "${GREEN}[INFO]${NC} No hay errores registrados aún"
        echo -e "${GREEN}[INFO]${NC} ¡Esto es bueno! Significa que no hay errores"
        read -p "Presiona Enter para continuar..."
    fi
    menu
}

ver_api() {
    clear
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}   Log de API - Presiona Ctrl+C para volver${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/api.log" ]; then
        tail -f "$LOGS_DIR/api.log" | grep --color=always -E 'GET|POST|PUT|DELETE|ERROR|$'
    else
        echo -e "${RED}[ERROR]${NC} Archivo $LOGS_DIR/api.log no encontrado"
        read -p "Presiona Enter para continuar..."
    fi
    menu
}

ver_auth() {
    clear
    echo -e "${YELLOW}============================================================${NC}"
    echo -e "${YELLOW}   Log de Autenticación - Presiona Ctrl+C para volver${NC}"
    echo -e "${YELLOW}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/auth.log" ]; then
        tail -f "$LOGS_DIR/auth.log" | grep --color=always -E 'login|register|password|ERROR|$'
    else
        echo -e "${RED}[ERROR]${NC} Archivo $LOGS_DIR/auth.log no encontrado"
        read -p "Presiona Enter para continuar..."
    fi
    menu
}

monitor() {
    clear
    echo -e "${PURPLE}============================================================${NC}"
    echo -e "${PURPLE}   Monitor en Tiempo Real${NC}"
    echo -e "${PURPLE}============================================================${NC}"
    echo ""
    echo "Presiona Ctrl+C para volver al menú"
    echo ""
    
    cd proyecto/src/backend
    python monitor_logs.py --interval 30
    cd ../../..
    menu
}

analisis() {
    clear
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}   Análisis de Logs${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    
    read -p "Horas a analizar (default 24): " horas
    horas=${horas:-24}
    
    cd proyecto/src/backend
    python analyze_logs.py --hours $horas
    cd ../../..
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

# Verificar que existe el directorio de logs
if [ ! -d "$LOGS_DIR" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Directorio de logs no encontrado"
    echo -e "${YELLOW}[INFO]${NC} Inicia el servidor primero con ./iniciar_desarrollo.sh o ./iniciar_produccion.sh"
    exit 1
fi

# Mostrar menú
menu

