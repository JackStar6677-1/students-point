"""Modelos para cursos abiertos OTEC."""

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Curso(models.Model):
    """Curso abierto publicado por la comunidad."""
    
    class TipoCurso(models.TextChoices):
        ANUNCIO_PERSONAL = 'personal', 'Clases Privadas / Tutorias'
        ENLACE_EXTERNO = 'externo', 'Curso Externo'
        
    class Modalidad(models.TextChoices):
        PRESENCIAL = 'presencial', 'Presencial'
        ONLINE = 'online', 'Online'
        HIBRIDO = 'hibrido', 'Hibrido'
        
    class Nivel(models.TextChoices):
        PRINCIPIANTE = 'principiante', 'Principiante'
        INTERMEDIO = 'intermedio', 'Intermedio'
        AVANZADO = 'avanzado', 'Avanzado'
        TODOS = 'todos', 'Todos los niveles'

    # Campos básicos
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cursos")
    titulo = models.CharField(max_length=200, help_text='Titulo del curso o clase')
    descripcion = models.TextField(help_text='Descripcion detallada')
    
    # Tipo y categoría
    tipo = models.CharField(
        max_length=20, 
        choices=TipoCurso.choices,
        default=TipoCurso.ENLACE_EXTERNO,
        help_text='Tipo de publicacion'
    )
    categoria = models.CharField(
        max_length=100,
        default='General',
        help_text='Categoria: Programacion, Diseño, Matematicas, etc.'
    )
    etiquetas = models.CharField(
        max_length=200,
        blank=True,
        help_text='Etiquetas separadas por comas'
    )
    
    # Detalles del curso
    modalidad = models.CharField(
        max_length=20,
        choices=Modalidad.choices,
        default=Modalidad.ONLINE
    )
    nivel = models.CharField(
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.TODOS
    )
    duracion = models.CharField(
        max_length=100,
        blank=True,
        help_text='Ej: 40 horas, 3 meses, etc.'
    )
    
    # Precio
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text='Precio en pesos chilenos. Dejar vacio para gratuito'
    )
    es_gratuito = models.BooleanField(default=False)  # type: ignore
    
    # URLs y contacto
    url = models.URLField(
        blank=True,
        help_text='URL del curso (para cursos externos) o plataforma de contacto'
    )
    email_contacto = models.EmailField(
        blank=True,
        help_text='Email de contacto (solo para anuncios personales)'
    )
    telefono_contacto = models.CharField(
        max_length=20,
        blank=True,
        help_text='Telefono de contacto (solo para anuncios personales)'
    )
    
    # Imagen opcional
    imagen_url = models.URLField(
        blank=True,
        help_text='URL de imagen del curso'
    )
    
    # Fechas
    fecha_inicio = models.DateField(
        help_text='Fecha de inicio del curso'
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        help_text='Fecha de fin (opcional)'
    )
    
    # Metadata
    visible = models.BooleanField(default=True)  # type: ignore
    visualizaciones = models.IntegerField(default=0)  # type: ignore
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['tipo']),
            models.Index(fields=['categoria']),
            models.Index(fields=['visible']),
        ]

    def esta_vigente(self) -> bool:
        today = timezone.now().date()
        if not self.visible:
            return False
        if self.fecha_inicio > today:
            return False
        if self.fecha_fin and self.fecha_fin < today:
            return False
        return True
    
    def precio_formateado(self) -> str:
        """Retorna el precio formateado"""
        if self.es_gratuito or not self.precio:
            return 'Gratuito'
        # Convertir Decimal a int para formateo (el type checker no entiende Decimal de Django)
        try:
            precio_int = int(self.precio)  # type: ignore
        except (ValueError, TypeError):
            return 'Gratuito'
        return f'${precio_int:,}'.replace(',', '.')

    def __str__(self) -> str:
        return f"{self.titulo} - {self.get_tipo_display()}"
