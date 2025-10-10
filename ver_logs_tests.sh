#!/bin/bash
# Script para ver logs de tests - Linux/Mac

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

LOGS_DIR="logs_tests"

menu() {
    clear
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}   Ver Logs de Tests - StudentsPoint${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    echo "Selecciona el tipo de log:"
    echo ""
    echo -e "  ${GREEN}1)${NC} Resumen de ultima ejecucion"
    echo -e "  ${RED}2)${NC} Errores de tests"
    echo -e "  ${BLUE}3)${NC} Log completo de tests"
    echo -e "  ${PURPLE}4)${NC} Log detallado (con lineas de codigo)"
    echo -e "  ${YELLOW}5)${NC} Ver todos los logs disponibles"
    echo -e "  ${RED}6)${NC} Limpiar logs antiguos"
    echo -e "  ${BLUE}7)${NC} Salir"
    echo ""
    read -p "Opcion (1-7): " opcion
    
    case $opcion in
        1) ver_resumen ;;
        2) ver_errores ;;
        3) ver_completo ;;
        4) ver_detallado ;;
        5) listar ;;
        6) limpiar ;;
        7) exit 0 ;;
        *)
            echo -e "${RED}Opcion invalida${NC}"
            sleep 2
            menu
            ;;
    esac
}

ver_resumen() {
    clear
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}   Resumen de Tests${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/pytest_summary_latest.log" ]; then
        cat "$LOGS_DIR/pytest_summary_latest.log"
    else
        echo -e "${YELLOW}[INFO]${NC} No hay resumen disponible"
        echo -e "${YELLOW}[INFO]${NC} Ejecuta primero: python run_pytest.py"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

ver_errores() {
    clear
    echo -e "${RED}============================================================${NC}"
    echo -e "${RED}   Errores de Tests${NC}"
    echo -e "${RED}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/pytest_errors_latest.log" ]; then
        cat "$LOGS_DIR/pytest_errors_latest.log" | grep --color=always -E 'ERROR|FAILED|AssertionError|$'
    else
        echo -e "${GREEN}[INFO]${NC} No hay errores registrados"
        echo -e "${GREEN}[INFO]${NC} Esto es bueno - significa que todos los tests pasaron"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

ver_completo() {
    clear
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}   Log Completo de Tests${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/tests_execution.log" ]; then
        tail -n 100 "$LOGS_DIR/tests_execution.log"
    else
        echo -e "${RED}[ERROR]${NC} Archivo no encontrado"
        echo -e "${YELLOW}[INFO]${NC} Ejecuta primero: python run_pytest.py"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

ver_detallado() {
    clear
    echo -e "${PURPLE}============================================================${NC}"
    echo -e "${PURPLE}   Log Detallado de Tests${NC}"
    echo -e "${PURPLE}============================================================${NC}"
    echo ""
    
    lastfile=$(ls -t $LOGS_DIR/test_detailed_*.log 2>/dev/null | head -n 1)
    
    if [ -n "$lastfile" ]; then
        tail -n 150 "$lastfile"
    else
        echo -e "${RED}[ERROR]${NC} No hay logs detallados disponibles"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

listar() {
    clear
    echo -e "${YELLOW}============================================================${NC}"
    echo -e "${YELLOW}   Logs Disponibles${NC}"
    echo -e "${YELLOW}============================================================${NC}"
    echo ""
    
    if [ -d "$LOGS_DIR" ]; then
        ls -lh $LOGS_DIR/*.log 2>/dev/null || echo "No hay logs disponibles"
    else
        echo -e "${YELLOW}[INFO]${NC} Directorio logs_tests no encontrado"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

limpiar() {
    clear
    echo -e "${RED}============================================================${NC}"
    echo -e "${RED}   Limpiar Logs Antiguos${NC}"
    echo -e "${RED}============================================================${NC}"
    echo ""
    
    read -p "¿Eliminar logs antiguos (mantener ultimos 5)? (s/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Limpiando logs antiguos..."
        
        # Mantener solo ultimos 5 de cada tipo
        ls -t $LOGS_DIR/pytest_*.log 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
        ls -t $LOGS_DIR/test_*.log 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
        
        echo -e "${GREEN}[OK]${NC} Logs antiguos eliminados"
    else
        echo -e "${YELLOW}[INFO]${NC} Operacion cancelada"
    fi
    
    echo ""
    read -p "Presiona Enter para continuar..."
    menu
}

# Verificar directorio
if [ ! -d "$LOGS_DIR" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Directorio logs_tests no encontrado"
    echo -e "${YELLOW}[INFO]${NC} Se creara al ejecutar tests por primera vez"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

menu

