from rest_framework import serializers
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
    class Meta:
        model = ConversionJob
        fields = ['tipo_conversion', 'archivo_original', 'usar_ocr']

