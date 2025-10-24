"""Celery tasks for scheduling and sending push notifications."""

import json
from datetime import datetime, timedelta
from pathlib import Path

from celery import shared_task
from django.conf import settings
import pytz
from pywebpush import WebPushException, webpush
import yaml

from .models import PushSub
# from studentspoint.apps.schedules.models import Horario  # Eliminado: schedules ya no existe

CONFIG_DIR = Path(settings.BASE_DIR).parent.parent / "config"
PUSH_CONFIG_FILE = CONFIG_DIR / "push.yaml"

# Cargar configuración de push con valores por defecto
try:
    PUSH_CONF = yaml.safe_load(PUSH_CONFIG_FILE.read_text())
except FileNotFoundError:
    # Configuración por defecto para desarrollo
    PUSH_CONF = {
        "vapid_public": "BEl62iUYgUivxIkv69yViEuiBIa40HI8l8V6V1V8H3BZ7pRJvnSW4UPHW3v3T1td1K3_fSqiNI2j_lLQ6Ypy1XM",
        "vapid_private": "3K1XdXz0L8Fz0aJSOdwuSeiJfZ5JWY7BdI3R2kS2aJ8",
        "subject": "mailto:admin@duocuc.cl"
    }


# @shared_task
# def schedule_class_alerts(user_id: str):
#     """Schedule push notifications 20 minutes before each class for 30 days."""
#     # DESHABILITADO: schedules/Horario eliminado - funcionalidad de horarios removida del proyecto
#     pass


@shared_task
def send_class_push(user_id: str, horario_id=None, fecha_clase=None, hora_alerta=None, test_only=True):
    """Send a Web Push notification to all active subscriptions of a user."""

    subs = PushSub.objects.filter(usuario_id=user_id, activo=True)
    if not subs:
        return

    # Solo modo de prueba disponible (schedules/Horario eliminado)
    title = "Prueba de notificación"
    body = "Service worker operativo"

    payload = json.dumps({"title": title, "body": body})

    for sub in subs:
        try:
            webpush(
                {
                    "endpoint": sub.endpoint,
                    "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                },
                data=payload,
                vapid_private_key=PUSH_CONF["vapid_private"],
                vapid_public_key=PUSH_CONF["vapid_public"],
                vapid_claims={"sub": PUSH_CONF["subject"]},
            )
        except WebPushException:
            sub.activo = False
            sub.save(update_fields=["activo"])
