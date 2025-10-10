from django.db import models
from django.conf import settings


class ConversionJob(models.Model):
    """Registro de trabajos de conversión de documentos"""
    
    class TipoConversion(models.TextChoices):
        WORD_TO_PDF = 'word_to_pdf', 'Word a PDF'
        PDF_TO_WORD = 'pdf_to_word', 'PDF a Word'
        
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PROCESANDO = 'procesando', 'Procesando'
        COMPLETADO = 'completado', 'Completado'
        ERROR = 'error', 'Error'
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversiones'
    )
    tipo_conversion = models.CharField(max_length=20, choices=TipoConversion.choices)
    archivo_original = models.FileField(upload_to='conversiones/originales/')
    archivo_convertido = models.FileField(upload_to='conversiones/convertidos/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    usar_ocr = models.BooleanField(default=False, help_text='Usar OCR para extraer texto de imágenes')
    error_mensaje = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Trabajo de Conversión'
        verbose_name_plural = 'Trabajos de Conversión'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_tipo_conversion_display()} - {self.usuario.email} - {self.get_estado_display()}"

