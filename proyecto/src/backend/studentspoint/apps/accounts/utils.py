"""Utilidades para el módulo de autenticación y cuentas."""

from typing import Optional, Dict
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


def normalizar_carrera(carrera: str, carreras_disponibles: list) -> Optional[str]:
    """Normaliza una carrera comparando sin acentos.
    
    Args:
        carrera: Nombre de la carrera a normalizar
        carreras_disponibles: Lista de carreras disponibles
        
    Returns:
        str: Carrera normalizada con acentos originales o None si no se encuentra
    """
    import unicodedata
    
    def norm(s):
        return ''.join(c for c in unicodedata.normalize('NFKD', s) 
                      if not unicodedata.combining(c)).lower()
    
    carrera_norm = norm(carrera)
    disponibles_norm = [norm(c) for c in carreras_disponibles]
    
    if carrera_norm in disponibles_norm:
        idx = disponibles_norm.index(carrera_norm)
        return carreras_disponibles[idx]
    
    return None


def verificar_expiracion_codigo(sent_at, minutos_expiracion: int = 15) -> bool:
    """Verifica si un código ha expirado.
    
    Args:
        sent_at: DateTime cuando se envió el código
        minutos_expiracion: Minutos hasta que expire (default: 15)
        
    Returns:
        bool: True si el código expiró
    """
    if not sent_at:
        return True
    
    expiracion = sent_at + timedelta(minutes=minutos_expiracion)
    return timezone.now() > expiracion


def formatear_respuesta_exito(mensaje: str, datos_adicionales: Optional[Dict] = None) -> Dict:
    """Formatea una respuesta de éxito estándar.
    
    Args:
        mensaje: Mensaje de éxito
        datos_adicionales: Datos adicionales a incluir
        
    Returns:
        dict: Respuesta formateada
    """
    respuesta = {
        'status': 'success',
        'message': mensaje
    }
    
    if datos_adicionales:
        respuesta.update(datos_adicionales)
    
    return respuesta


def formatear_respuesta_error(mensaje: str, codigo: Optional[str] = None) -> Dict:
    """Formatea una respuesta de error estándar.
    
    Args:
        mensaje: Mensaje de error
        codigo: Código de error opcional
        
    Returns:
        dict: Respuesta formateada
    """
    respuesta = {
        'status': 'error',
        'message': mensaje
    }
    
    if codigo:
        respuesta['code'] = codigo
    
    return respuesta

