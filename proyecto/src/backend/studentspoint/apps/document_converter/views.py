import logging
import threading
import os
from django.http import FileResponse, Http404
from django.conf import settings
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
    
    def create(self, request, *args, **kwargs):
        """Crea un trabajo de conversión y lo procesa en background"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar el job
        job = serializer.save(usuario=request.user)
        
        # Ejecutar conversión en background usando threading
        logger.info(f"Iniciando conversion {job.id} para usuario {request.user.email}")
        conversion_thread = threading.Thread(
            target=convert_document,
            args=(job,),
            daemon=True
        )
        conversion_thread.start()
        
        # Devolver respuesta con el serializer completo
        response_serializer = ConversionJobSerializer(job, context={'request': request})
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


class ConversionDownloadView(APIView):
    """Descarga un archivo convertido"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            job = ConversionJob.objects.get(pk=pk, usuario=request.user)
        except ConversionJob.DoesNotExist:
            raise Http404("Trabajo de conversión no encontrado")
        
        if not job.archivo_convertido:
            return Response(
                {'error': 'El archivo convertido no está disponible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if job.estado != ConversionJob.Estado.COMPLETADO:
            return Response(
                {'error': 'La conversión no está completada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            file_path = job.archivo_convertido.path
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'El archivo no existe en el servidor'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Obtener el nombre del archivo
            filename = os.path.basename(file_path)
            
            # Crear FileResponse con headers para forzar descarga
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = os.path.getsize(file_path)
            
            return response
            
        except Exception as e:
            logger.error(f"Error descargando archivo {job.id}: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Error al descargar el archivo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

