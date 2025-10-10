from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Comentario, Foro, ModeracionEvent, Post, VotoComentario, VotoPost,
    OpcionEncuesta, VotoEncuesta, PostReporte
)


@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'carrera', 'sede', 'es_privado', 'created_at']
    list_filter = ['es_privado', 'sede', 'carrera']
    search_fields = ['titulo', 'carrera']
    prepopulated_fields = {'slug': ('titulo',)}


class OpcionEncuestaInline(admin.TabularInline):
    model = OpcionEncuesta
    extra = 2
    fields = ['texto', 'votos', 'orden']
    readonly_fields = ['votos']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'foro', 'tipo', 'estado', 'imagen_status', 'total_reportes', 'created_at']
    list_filter = ['estado', 'tipo', 'imagen_aprobada', 'created_at', 'foro__carrera']
    search_fields = ['titulo', 'cuerpo', 'usuario__name', 'usuario__email']
    readonly_fields = ['score', 'total_reportes', 'ultimo_reporte_at', 'created_at', 'updated_at']
    inlines = [OpcionEncuestaInline]
    actions = ['aprobar_imagenes', 'rechazar_imagenes', 'aprobar_posts', 'rechazar_posts']
    
    def imagen_status(self, obj):
        if obj.imagen:
            if obj.imagen_aprobada:
                return format_html('<span style="color: green;"> Aprobada</span>')
            else:
                return format_html('<span style="color: orange;"> Pendiente</span>')
        return '-'
    imagen_status.short_description = 'Imagen'
    
    def aprobar_imagenes(self, request, queryset):
        """Acción para aprobar imágenes en posts seleccionados."""
        count = queryset.filter(imagen__isnull=False).update(imagen_aprobada=True, estado='publicado')
        self.message_user(request, f'{count} imágenes aprobadas.')
    aprobar_imagenes.short_description = "Aprobar imágenes seleccionadas"
    
    def rechazar_imagenes(self, request, queryset):
        """Acción para rechazar imágenes en posts seleccionados."""
        count = queryset.filter(imagen__isnull=False).update(imagen_aprobada=False, estado='rechazado')
        self.message_user(request, f'{count} imágenes rechazadas.')
    rechazar_imagenes.short_description = "Rechazar imágenes seleccionadas"
    
    def aprobar_posts(self, request, queryset):
        """Acción para aprobar posts."""
        count = queryset.update(estado='publicado')
        self.message_user(request, f'{count} posts aprobados.')
    aprobar_posts.short_description = "Aprobar posts seleccionados"
    
    def rechazar_posts(self, request, queryset):
        """Acción para rechazar posts."""
        count = queryset.update(estado='rechazado')
        self.message_user(request, f'{count} posts rechazados.')
    rechazar_posts.short_description = "Rechazar posts seleccionados"


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['post', 'usuario', 'cuerpo_preview', 'score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cuerpo', 'usuario__name']
    readonly_fields = ['score', 'created_at']
    
    def cuerpo_preview(self, obj):
        return obj.cuerpo[:50] + '...' if len(obj.cuerpo) > 50 else obj.cuerpo
    cuerpo_preview.short_description = 'Contenido'


@admin.register(OpcionEncuesta)
class OpcionEncuestaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'post', 'votos', 'orden']
    list_filter = ['post']
    search_fields = ['texto']
    readonly_fields = ['votos']


@admin.register(PostReporte)
class PostReporteAdmin(admin.ModelAdmin):
    list_display = ['post', 'usuario', 'tipo', 'created_at']
    list_filter = ['tipo', 'created_at']
    search_fields = ['post__titulo', 'usuario__name', 'descripcion']
    readonly_fields = ['created_at']


admin.site.register(VotoPost)
admin.site.register(VotoComentario)
admin.site.register(VotoEncuesta)
admin.site.register(ModeracionEvent)
