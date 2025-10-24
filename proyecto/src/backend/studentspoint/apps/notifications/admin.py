"""Admin bindings for push subscriptions."""

from django.contrib import admin

from .models import PushSub


@admin.register(PushSub)
class PushSubAdmin(admin.ModelAdmin):
    list_display = ("usuario", "endpoint", "activo", "created_at")
    readonly_fields = ("created_at",)
