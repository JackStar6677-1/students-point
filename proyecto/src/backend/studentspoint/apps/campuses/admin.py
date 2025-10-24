"""Registro de modelos de sedes en el administrador."""

from django.contrib import admin

from .models import Recorrido, RecorridoPaso, Sede


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):  # pragma: no cover - solo interfaz
    list_display = ("nombre", "slug")
    search_fields = ("nombre", "slug")


@admin.register(Recorrido)
class RecorridoAdmin(admin.ModelAdmin):  # pragma: no cover - solo interfaz
    list_display = ("titulo", "sede")
    list_filter = ("sede",)


@admin.register(RecorridoPaso)
class RecorridoPasoAdmin(admin.ModelAdmin):  # pragma: no cover - solo interfaz
    list_display = ("recorrido", "orden", "titulo")
    list_filter = ("recorrido",)
    ordering = ("recorrido", "orden")
