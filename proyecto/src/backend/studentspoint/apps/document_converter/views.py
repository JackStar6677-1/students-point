import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import ConversionJob
from .serializers import ConversionJobSerializer, ConversionCreateSerializer
from .services import convert_document

logger = logging.getLogger('studentspoint.apps.document_converter')


class ConversionListCreateView(generics.ListCreateAPIView):
    """Lista y crea trabajos de conversión de documentos"""
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversionCreateSerializer
        return ConversionJobSerializer
    
    def get_queryset(self):
        return ConversionJob.objects.filter(usuario=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        job = serializer.save(usuario=self.request.user)
        
        # Ejecutar conversión en background (o sincrono para desarrollo)
        logger.info(f"Iniciando conversion {job.id} para usuario {self.request.user.email}")
        convert_document(job)
        
        return job


class ConversionDetailView(generics.RetrieveAPIView):
    """Obtiene detalles de un trabajo de conversión"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ConversionJobSerializer
    
    def get_queryset(self):
        return ConversionJob.objects.filter(usuario=self.request.user)


class ConversionDeleteView(generics.DestroyAPIView):
    """Elimina un trabajo de conversión"""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ConversionJob.objects.filter(usuario=self.request.user)
    
    def perform_destroy(self, instance):
        # Eliminar archivos físicos
        if instance.archivo_original:
            instance.archivo_original.delete(save=False)
        if instance.archivo_convertido:
            instance.archivo_convertido.delete(save=False)
        instance.delete()

