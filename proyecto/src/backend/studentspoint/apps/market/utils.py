"""Utilidades para el módulo de marketplace."""

from typing import Optional


def formatear_precio(precio: float, moneda: str = "CLP") -> str:
    """Formatea un precio para mostrar.
    
    Args:
        precio: Precio a formatear
        moneda: Código de moneda (CLP, USD, etc.)
        
    Returns:
        str: Precio formateado
    """
    if moneda == "CLP":
        return f"${precio:,.0f}".replace(",", ".")
    else:
        return f"${precio:,.2f} {moneda}"


def humanizar_tiempo(timezone_aware_datetime) -> Optional[str]:
    """Convierte un datetime a formato legible (ej: "hace 2 días").
    
    Args:
        timezone_aware_datetime: datetime con timezone
        
    Returns:
        str: Tiempo humanizado o None si no hay datetime
    """
    if not timezone_aware_datetime:
        return None
    
    from django.utils import timezone
    from datetime import timedelta
    
    ahora = timezone.now()
    diferencia = ahora - timezone_aware_datetime
    
    if diferencia.days > 0:
        return f"hace {diferencia.days} día{'s' if diferencia.days > 1 else ''}"
    elif diferencia.seconds >= 3600:
        horas = diferencia.seconds // 3600
        return f"hace {horas} hora{'s' if horas > 1 else ''}"
    elif diferencia.seconds >= 60:
        minutos = diferencia.seconds // 60
        return f"hace {minutos} minuto{'s' if minutos > 1 else ''}"
    else:
        return "hace unos segundos"

