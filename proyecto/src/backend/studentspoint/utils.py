"""
Utilidades para StudentsPoint
"""

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from functools import wraps
from typing import Tuple

import os
import logging

import requests

def csrf_exempt_api(view_func):
    """
    Decorador para deshabilitar CSRF en APIs REST
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return csrf_exempt(view_func)(*args, **kwargs)
    return wrapper

def csrf_exempt_class(cls):
    """
    Decorador de clase para deshabilitar CSRF
    """
    cls.dispatch = method_decorator(csrf_exempt)(cls.dispatch)
    return cls


def verify_recaptcha(token: str | None, remote_ip: str | None = None) -> Tuple[bool, float]:
    """Verifica un token de reCAPTCHA v3 (no estricto).

    Args:
        token: Token recibido desde el cliente (captcha_token)
        remote_ip: IP del cliente (opcional)

    Returns:
        (success, score): Tupla con éxito y score (0.0 si no disponible)

    Política no estricta:
    - Si no hay RECAPTCHA_SECRET configurado, no se aplica verificación (retorna (True, 1.0)).
    - Si no hay token, registra advertencia y retorna (True, 0.0) para no bloquear.
    - Umbral bajo (>= 0.3) considerado aceptable.
    """
    logger = logging.getLogger(__name__)
    secret = os.getenv("RECAPTCHA_SECRET")
    if not secret:
        return True, 1.0
    if not token:
        logger.warning("reCAPTCHA: token ausente; política laxa permite continuar")
        return True, 0.0

    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret, "response": token, **({"remoteip": remote_ip} if remote_ip else {})},
            timeout=5,
        )
        data = resp.json() if resp.ok else {}
        success = bool(data.get("success"))
        score = float(data.get("score", 0.0))
        # Umbral laxo
        if success and score >= 0.3:
            return True, score
        logger.warning("reCAPTCHA: verificación no satisfactoria success=%s score=%.2f", success, score)
        return False, score
    except Exception as exc:  # pragma: no cover - falla de red no debe bloquear
        logger.warning("reCAPTCHA: excepción en verificación: %s", exc)
        # Política laxa: no bloquear por errores de red
        return True, 0.0
