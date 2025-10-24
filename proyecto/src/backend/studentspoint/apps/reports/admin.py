"""Admin para reportes."""

from django.contrib import admin

from .models import Reporte, ReporteMedia

admin.site.register(Reporte)
admin.site.register(ReporteMedia)
