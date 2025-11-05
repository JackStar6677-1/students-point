"""Configuración del administrador para la app de cuentas."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CambioCarrera
from .models_audit import LoginLog, RegistrationLog, UserActivityLog


class CambioCarreraInline(admin.TabularInline):
    model = CambioCarrera
    extra = 0
    readonly_fields = ('carrera_anterior', 'carrera_nueva', 'razon', 'fecha_cambio')
    can_delete = False


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):  # pragma: no cover - interfaz de administración
    list_display = ("email", "name", "career", "semestre", "campus", "role", "is_email_verified", "is_active", "date_joined")
    list_filter = ("role", "career", "campus", "is_active", "is_email_verified", "es_estudiante_gmail")
    search_fields = ("email", "name", "career")
    inlines = [CambioCarreraInline]
    readonly_fields = ("date_joined", "last_login", "google_id", "email_verification_sent_at", "password_reset_sent_at")
    
    fieldsets = (
        ('Informacion Basica', {
            'fields': ('email', 'name', 'is_active', 'picture_file')
        }),
        ('Informacion Academica', {
            'fields': ('career', 'semestre', 'campus', 'role')
        }),
        ('Contacto Adicional', {
            'fields': ('telefono', 'linkedin_url', 'github_url')
        }),
        ('Verificacion de Email', {
            'fields': ('is_email_verified', 'email_verification_code', 'email_verification_sent_at'),
            'classes': ('collapse',)
        }),
        ('Recuperacion de Password', {
            'fields': ('password_reset_code', 'password_reset_sent_at'),
            'classes': ('collapse',)
        }),
        ('Autenticacion Externa', {
            'fields': ('es_estudiante_gmail', 'google_id', 'picture', 'is_verified'),
            'classes': ('collapse',)
        }),
        ('Permisos y Estado', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('date_joined', 'last_login')
        }),
    )


@admin.register(CambioCarrera)
class CambioCarreraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'carrera_anterior', 'carrera_nueva', 'fecha_cambio')
    list_filter = ('carrera_anterior', 'carrera_nueva', 'fecha_cambio')
    search_fields = ('usuario__email', 'usuario__name', 'carrera_anterior', 'carrera_nueva', 'razon')
    readonly_fields = ('usuario', 'carrera_anterior', 'carrera_nueva', 'fecha_cambio')
    date_hierarchy = 'fecha_cambio'
    
    def has_add_permission(self, request):
        # Los cambios de carrera se crean mediante el método del modelo
        return False


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('email_intentado', 'usuario', 'estado', 'ip_address', 'created_at')
    list_filter = ('estado', 'created_at')
    search_fields = ('email_intentado', 'usuario__email', 'ip_address', 'razon_fallo')
    readonly_fields = ('usuario', 'email_intentado', 'estado', 'ip_address', 'user_agent', 'razon_fallo', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(RegistrationLog)
class RegistrationLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'usuario', 'estado', 'career_intentada', 'ip_address', 'created_at')
    list_filter = ('estado', 'created_at', 'career_intentada')
    search_fields = ('email', 'usuario__email', 'name_intentado', 'career_intentada', 'ip_address')
    readonly_fields = ('usuario', 'email', 'name_intentado', 'career_intentada', 'estado', 'ip_address', 'user_agent', 'razon_fallo', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'ip_address', 'created_at')
    list_filter = ('tipo', 'created_at')
    search_fields = ('usuario__email', 'usuario__name', 'descripcion', 'ip_address')
    readonly_fields = ('usuario', 'tipo', 'descripcion', 'datos_adicionales', 'ip_address', 'user_agent', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
