"""Configuración mejorada del admin para encuestas."""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Poll, PollOpcion, PollVoto, PollAnalytics


class PollOpcionInline(admin.TabularInline):
    """Inline para opciones de encuesta."""
    model = PollOpcion
    extra = 2
    fields = ["texto", "descripcion", "orden", "color"]
    ordering = ["orden"]


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Administración avanzada de encuestas."""
    
    list_display = [
        "titulo", "creador", "estado", "total_votos_display", 
        "esta_activa", "inicia_at", "cierra_at", "created_at"
    ]
    list_filter = [
        "estado", "mostrar_resultados", "multi", "anonima", 
        "created_at", "inicia_at", "sedes"
    ]
    search_fields = ["titulo", "descripcion", "creador__name", "creador__email"]
    readonly_fields = ["created_at", "updated_at", "total_votos_display", "analytics_link"]
    filter_horizontal = ["sedes"]
    
    fieldsets = (
        ("Información Básica", {
            "fields": ("titulo", "descripcion", "creador", "estado")
        }),
        ("Configuración", {
            "fields": ("multi", "anonima", "requiere_justificacion", "mostrar_resultados")
        }),
        ("Filtros", {
            "fields": ("sedes", "carreras"),
            "classes": ("collapse",)
        }),
        ("Fechas", {
            "fields": ("inicia_at", "cierra_at", "created_at", "updated_at")
        }),
        ("Estadísticas", {
            "fields": ("total_votos_display", "analytics_link"),
            "classes": ("collapse",)
        })
    )
    
    inlines = [PollOpcionInline]
    
    def total_votos_display(self, obj):
        """Muestra total de votos únicos."""
        return obj.total_votos
    total_votos_display.short_description = "Total Votos"
    
    def analytics_link(self, obj):
        """Link a analytics de la encuesta."""
        if obj.pk:
            try:
                analytics = obj.analytics
                url = reverse("admin:polls_pollanalytics_change", args=[analytics.pk])
                return format_html('<a href="{}">Ver Analytics</a>', url)
            except PollAnalytics.DoesNotExist:
                return "Sin analytics"
        return "Guarda primero"
    analytics_link.short_description = "Analytics"
    
    def get_queryset(self, request):
        """Optimiza consultas."""
        return super().get_queryset(request).select_related("creador").prefetch_related("sedes")


@admin.register(PollOpcion)
class PollOpcionAdmin(admin.ModelAdmin):
    """Administración de opciones de encuesta."""
    
    list_display = ["texto", "poll", "orden", "total_votos_display", "porcentaje_display"]
    list_filter = ["poll__estado", "poll__created_at"]
    search_fields = ["texto", "descripcion", "poll__titulo"]
    ordering = ["poll", "orden"]
    
    def total_votos_display(self, obj):
        """Muestra total de votos para la opción."""
        return obj.total_votos
    total_votos_display.short_description = "Votos"
    
    def porcentaje_display(self, obj):
        """Muestra porcentaje de votos."""
        return f"{obj.porcentaje_votos}%"
    porcentaje_display.short_description = "Porcentaje"


@admin.register(PollVoto)
class PollVotoAdmin(admin.ModelAdmin):
    """Administración de votos."""
    
    list_display = [
        "poll", "usuario", "opcion", "sede_voto", "carrera_voto", 
        "created_at", "tiene_justificacion"
    ]
    list_filter = [
        "poll", "sede_voto", "carrera_voto", "created_at"
    ]
    search_fields = [
        "poll__titulo", "usuario__name", "usuario__email", 
        "opcion__texto", "justificacion"
    ]
    readonly_fields = ["created_at", "ip_address", "user_agent"]
    
    fieldsets = (
        ("Voto", {
            "fields": ("poll", "usuario", "opcion", "justificacion")
        }),
        ("Metadatos", {
            "fields": ("sede_voto", "carrera_voto", "created_at"),
            "classes": ("collapse",)
        }),
        ("Auditoría", {
            "fields": ("ip_address", "user_agent"),
            "classes": ("collapse",)
        })
    )
    
    def tiene_justificacion(self, obj):
        """Indica si el voto tiene justificación."""
        return bool(obj.justificacion)
    tiene_justificacion.boolean = True
    tiene_justificacion.short_description = "Con Justificación"
    
    def get_queryset(self, request):
        """Optimiza consultas."""
        return super().get_queryset(request).select_related(
            "poll", "usuario", "opcion", "sede_voto"
        )


@admin.register(PollAnalytics)
class PollAnalyticsAdmin(admin.ModelAdmin):
    """Administración de analytics de encuestas."""
    
    list_display = [
        "poll", "total_participantes", "ultima_actualizacion"
    ]
    list_filter = ["ultima_actualizacion", "poll__estado"]
    search_fields = ["poll__titulo"]
    readonly_fields = [
        "poll", "total_participantes", "distribucion_sedes", 
        "distribucion_carreras", "ultima_actualizacion",
        "distribucion_visual"
    ]
    
    fieldsets = (
        ("Encuesta", {
            "fields": ("poll",)
        }),
        ("Estadísticas", {
            "fields": ("total_participantes", "ultima_actualizacion")
        }),
        ("Distribuciones", {
            "fields": ("distribucion_sedes", "distribucion_carreras", "distribucion_visual")
        })
    )
    
    def distribucion_visual(self, obj):
        """Visualización de distribuciones."""
        html = "<h4>Distribución por Sede:</h4><ul>"
        for sede, count in obj.distribucion_sedes.items():
            html += f"<li>{sede}: {count}</li>"
        html += "</ul><h4>Distribución por Carrera:</h4><ul>"
        for carrera, count in obj.distribucion_carreras.items():
            html += f"<li>{carrera}: {count}</li>"
        html += "</ul>"
        return mark_safe(html)
    distribucion_visual.short_description = "Visualización"
    
    actions = ["actualizar_estadisticas"]
    
    def actualizar_estadisticas(self, request, queryset):
        """Acción para actualizar estadísticas."""
        for analytics in queryset:
            analytics.actualizar_estadisticas()
        self.message_user(request, f"Estadísticas actualizadas para {queryset.count()} encuestas.")
    actualizar_estadisticas.short_description = "Actualizar estadísticas seleccionadas"