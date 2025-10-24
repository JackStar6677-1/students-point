"""Admin de contenidos de bienestar."""

from django.contrib import admin

from .models import BienestarItem

admin.site.register(BienestarItem)
