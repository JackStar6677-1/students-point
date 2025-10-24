"""Modelos para el sistema de portafolio automático."""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Logro(models.Model):
    """Logros y certificaciones del usuario."""
    
    class TiposLogro(models.TextChoices):
        ACADEMICO = "academico", "Académico"
        PROFESIONAL = "profesional", "Profesional"
        VOLUNTARIADO = "voluntariado", "Voluntariado"
        DEPORTIVO = "deportivo", "Deportivo"
        CULTURAL = "cultural", "Cultural"
        OTRO = "otro", "Otro"
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="logros"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TiposLogro.choices)
    fecha_obtencion = models.DateField()
    institucion = models.CharField(max_length=200, blank=True)
    certificado_url = models.URLField(blank=True, help_text="URL del certificado o evidencia")
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_obtencion']
        verbose_name = "Logro"
        verbose_name_plural = "Logros"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.titulo}"


class Proyecto(models.Model):
    """Proyectos realizados por el usuario."""
    
    class EstadosProyecto(models.TextChoices):
        EN_DESARROLLO = "en_desarrollo", "En Desarrollo"
        COMPLETADO = "completado", "Completado"
        EN_PAUSA = "en_pausa", "En Pausa"
        CANCELADO = "cancelado", "Cancelado"
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="proyectos"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.JSONField(
        default=list, 
        help_text="Lista de tecnologías utilizadas"
    )
    estado = models.CharField(max_length=20, choices=EstadosProyecto.choices, default=EstadosProyecto.EN_DESARROLLO)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    url_repositorio = models.URLField(blank=True)
    url_demo = models.URLField(blank=True)
    imagenes = models.JSONField(
        default=list, 
        help_text="URLs de imágenes del proyecto"
    )
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.titulo}"


class ExperienciaLaboral(models.Model):
    """Experiencia laboral del usuario."""
    
    class TiposContrato(models.TextChoices):
        PRACTICA = "practica", "Práctica Profesional"
        PART_TIME = "part_time", "Medio Tiempo"
        FULL_TIME = "full_time", "Tiempo Completo"
        FREELANCE = "freelance", "Freelance"
        VOLUNTARIADO = "voluntariado", "Voluntariado"
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="experiencias_laborales"
    )
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_contrato = models.CharField(max_length=20, choices=TiposContrato.choices)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actual = models.BooleanField(default=False)
    ubicacion = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.cargo} en {self.empresa}"


class Habilidad(models.Model):
    """Habilidades técnicas y blandas del usuario."""
    
    class CategoriasHabilidad(models.TextChoices):
        TECNICA = "tecnica", "Técnica"
        BLANDA = "blanda", "Blanda"
        IDIOMA = "idioma", "Idioma"
        HERRAMIENTA = "herramienta", "Herramienta"
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="habilidades"
    )
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CategoriasHabilidad.choices)
    nivel = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nivel de 1 a 5"
    )
    descripcion = models.TextField(blank=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['categoria', 'nombre']
        unique_together = ['usuario', 'nombre']
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.nombre} ({self.nivel}/5)"


class PortafolioConfig(models.Model):
    """Configuración personalizada del portafolio del usuario."""
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="portafolio_config"
    )
    
    # Información personal
    titulo_profesional = models.CharField(max_length=200, blank=True)
    resumen_profesional = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Configuración de visualización
    mostrar_contacto = models.BooleanField(default=True)
    mostrar_redes_sociales = models.BooleanField(default=True)
    mostrar_logros = models.BooleanField(default=True)
    mostrar_proyectos = models.BooleanField(default=True)
    mostrar_experiencia = models.BooleanField(default=True)
    mostrar_habilidades = models.BooleanField(default=True)
    
    # Tema y estilo
    tema_color = models.CharField(max_length=7, default="#2e004f", help_text="Color principal en hexadecimal")
    incluir_foto = models.BooleanField(default=False)
    foto_url = models.URLField(blank=True)
    
    # Metadatos
    ultima_generacion = models.DateTimeField(null=True, blank=True)
    version_pdf = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Portafolio"
        verbose_name_plural = "Configuraciones de Portafolio"
    
    def __str__(self):
        return f"Portafolio: {self.usuario.name}"
    
    def generar_pdf(self):
        """Marca que se generó un nuevo PDF."""
        self.ultima_generacion = timezone.now()
        self.version_pdf += 1
        self.save()


class PortafolioSugerencia(models.Model):
    """Sugerencias automáticas para mejorar el portafolio."""
    
    class TiposSugerencia(models.TextChoices):
        COMPLETAR_PERFIL = "completar_perfil", "Completar Perfil"
        AGREGAR_PROYECTOS = "agregar_proyectos", "Agregar Proyectos"
        MEJORAR_HABILIDADES = "mejorar_habilidades", "Mejorar Habilidades"
        AGREGAR_EXPERIENCIA = "agregar_experiencia", "Agregar Experiencia"
        AGREGAR_LOGROS = "agregar_logros", "Agregar Logros"
        MEJORAR_DESCRIPCION = "mejorar_descripcion", "Mejorar Descripción"
    
    class Prioridades(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="sugerencias_portafolio"
    )
    tipo = models.CharField(max_length=30, choices=TiposSugerencia.choices)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=Prioridades.choices, default=Prioridades.MEDIA)
    completada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-prioridad', '-created_at']
        verbose_name = "Sugerencia de Portafolio"
        verbose_name_plural = "Sugerencias de Portafolio"
    
    def __str__(self):
        return f"{self.usuario.name} - {self.titulo}"


class PortafolioAnalytics(models.Model):
    """Analytics del portafolio del usuario."""
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="portafolio_analytics"
    )
    
    # Métricas de completitud
    completitud_perfil = models.FloatField(default=0.0, help_text="Porcentaje de completitud del perfil")
    total_logros = models.PositiveIntegerField(default=0)
    total_proyectos = models.PositiveIntegerField(default=0)
    total_experiencias = models.PositiveIntegerField(default=0)
    total_habilidades = models.PositiveIntegerField(default=0)
    
    # Métricas de engagement
    visualizaciones_pdf = models.PositiveIntegerField(default=0)
    descargas_pdf = models.PositiveIntegerField(default=0)
    ultima_visualizacion = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytics de Portafolio"
        verbose_name_plural = "Analytics de Portafolios"
    
    def actualizar_estadisticas(self):
        """Recalcula todas las estadísticas del portafolio."""
        # Contar elementos
        self.total_logros = self.usuario.logros.filter(visible=True).count()
        self.total_proyectos = self.usuario.proyectos.filter(visible=True).count()
        self.total_experiencias = self.usuario.experiencias_laborales.filter(visible=True).count()
        self.total_habilidades = self.usuario.habilidades.filter(visible=True).count()
        
        # Calcular completitud (algoritmo simple)
        campos_completados = 0
        campos_totales = 8  # Ajustar según campos importantes
        
        if self.usuario.name: campos_completados += 1
        if self.usuario.career: campos_completados += 1
        if self.usuario.campus: campos_completados += 1
        if self.total_logros > 0: campos_completados += 1
        if self.total_proyectos > 0: campos_completados += 1
        if self.total_experiencias > 0: campos_completados += 1
        if self.total_habilidades > 0: campos_completados += 1
        
        # Verificar configuración de portafolio
        try:
            config = self.usuario.portafolio_config
            if config.titulo_profesional and config.resumen_profesional:
                campos_completados += 1
        except:
            pass
        
        self.completitud_perfil = round((campos_completados / campos_totales) * 100, 2)
        self.save()
    
    def __str__(self):
        return f"Analytics: {self.usuario.name}"