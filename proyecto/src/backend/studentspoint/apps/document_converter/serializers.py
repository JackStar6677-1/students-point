from rest_framework import serializers
from pathlib import Path
from .models import ConversionJob


class ConversionJobSerializer(serializers.ModelSerializer):
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    tipo_conversion_display = serializers.CharField(source='get_tipo_conversion_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    archivo_original_url = serializers.SerializerMethodField()
    archivo_convertido_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversionJob
        fields = [
            'id', 'usuario_email', 'tipo_conversion', 'tipo_conversion_display',
            'estado', 'estado_display', 'usar_ocr', 'error_mensaje',
            'archivo_original', 'archivo_original_url',
            'archivo_convertido', 'archivo_convertido_url',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'estado', 'error_mensaje', 'created_at', 'completed_at']
    
    def get_archivo_original_url(self, obj):
        if obj.archivo_original:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.archivo_original.url)
        return None
    
    def get_archivo_convertido_url(self, obj):
        if obj.archivo_convertido:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.archivo_convertido.url)
        return None


class ConversionCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear trabajos de conversión con validaciones."""
    
    class Meta:
        model = ConversionJob
        fields = ['tipo_conversion', 'archivo_original', 'usar_ocr']
    
    def validate_archivo_original(self, value):
        """Valida el archivo original según el tipo de conversión."""
        from .utils import DocumentValidator
        
        if not value:
            raise serializers.ValidationError("Debe proporcionar un archivo")
        
        # Obtener tipo de conversión del contexto o datos
        tipo_conversion = None
        if hasattr(self, 'initial_data'):
            tipo_conversion = self.initial_data.get('tipo_conversion')
        
        # Si no hay tipo de conversión aún, validar genéricamente
        if not tipo_conversion:
            # Validar que sea Word o PDF
            file_ext = Path(value.name).suffix.lower()
            from .utils import ALLOWED_WORD_EXTENSIONS, ALLOWED_PDF_EXTENSIONS
            
            if file_ext not in ALLOWED_WORD_EXTENSIONS + ALLOWED_PDF_EXTENSIONS:
                raise serializers.ValidationError(
                    f"Tipo de archivo no permitido: {file_ext}. "
                    f"Permitidos: {', '.join(ALLOWED_WORD_EXTENSIONS + ALLOWED_PDF_EXTENSIONS)}"
                )
        else:
            # Validar específicamente según tipo de conversión
            is_valid, error_msg = DocumentValidator.validate_file_for_conversion(
                value, 
                tipo_conversion
            )
            if not is_valid:
                raise serializers.ValidationError(error_msg)
        
        return value
    
    def validate(self, data):
        """Valida que el tipo de conversión coincida con el tipo de archivo."""
        archivo = data.get('archivo_original')
        tipo_conversion = data.get('tipo_conversion')
        
        if archivo and tipo_conversion:
            file_ext = Path(archivo.name).suffix.lower()
            from .utils import ALLOWED_WORD_EXTENSIONS, ALLOWED_PDF_EXTENSIONS
            
            if tipo_conversion == 'word_to_pdf' and file_ext not in ALLOWED_WORD_EXTENSIONS:
                raise serializers.ValidationError({
                    'archivo_original': f'Para convertir Word a PDF, debe subir un archivo Word (.doc o .docx), no {file_ext}'
                })
            
            if tipo_conversion == 'pdf_to_word' and file_ext not in ALLOWED_PDF_EXTENSIONS:
                raise serializers.ValidationError({
                    'archivo_original': f'Para convertir PDF a Word, debe subir un archivo PDF, no {file_ext}'
                })
        
        return data

