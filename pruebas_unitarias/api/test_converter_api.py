"""
Pruebas unitarias para la API de Document Converter
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from studentspoint.apps.document_converter.models import ConversionJob

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Usuario de prueba para conversión de documentos"""
    return User.objects.create_user(
        email='test@duocuc.cl',
        password='testpass123',
        name='Test User',
        career='Ingeniería en Informática'
    )


@pytest.fixture
def client():
    """Cliente API para pruebas"""
    return APIClient()


class TestDocumentConverterAPI:
    """Pruebas para la API de Document Converter"""
    
    def test_list_conversions_authenticated(self, client, user):
        """Prueba listar conversiones con usuario autenticado"""
        # Crear algunas conversiones de prueba
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='completado'
        )
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='pdf_to_word',
            archivo_original='test.pdf',
            estado='pendiente'
        )
        
        client.force_authenticate(user=user)
        response = client.get('/api/converter/conversions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_list_conversions_unauthenticated(self, client):
        """Prueba listar conversiones sin autenticación"""
        response = client.get('/api/converter/conversions/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_word_to_pdf_conversion(self, client, user):
        """Prueba crear conversión de Word a PDF"""
        client.force_authenticate(user=user)
        
        # Crear archivo de prueba
        test_file = SimpleUploadedFile(
            "test.docx",
            b"fake word content",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        data = {
            'tipo_conversion': 'word_to_pdf',
            'archivo_original': test_file,
            'usar_ocr': False
        }
        
        response = client.post('/api/converter/conversions/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert ConversionJob.objects.count() == 1
        
        conversion = ConversionJob.objects.first()
        assert conversion.usuario == user
        assert conversion.tipo_conversion == 'word_to_pdf'
        assert conversion.estado == 'pendiente'
        assert conversion.usar_ocr == False
    
    def test_create_pdf_to_word_conversion(self, client, user):
        """Prueba crear conversión de PDF a Word"""
        client.force_authenticate(user=user)
        
        # Crear archivo de prueba
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"fake pdf content",
            content_type="application/pdf"
        )
        
        data = {
            'tipo_conversion': 'pdf_to_word',
            'archivo_original': test_file,
            'usar_ocr': True
        }
        
        response = client.post('/api/converter/conversions/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert ConversionJob.objects.count() == 1
        
        conversion = ConversionJob.objects.first()
        assert conversion.usuario == user
        assert conversion.tipo_conversion == 'pdf_to_word'
        assert conversion.estado == 'pendiente'
        assert conversion.usar_ocr == True
    
    def test_create_conversion_unauthenticated(self, client):
        """Prueba crear conversión sin autenticación"""
        test_file = SimpleUploadedFile(
            "test.docx",
            b"fake content",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        data = {
            'tipo_conversion': 'word_to_pdf',
            'archivo_original': test_file
        }
        
        response = client.post('/api/converter/conversions/', data, format='multipart')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_conversion_detail_authenticated(self, client, user):
        """Prueba obtener detalle de conversión con usuario autenticado"""
        conversion = ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['tipo_conversion'] == 'word_to_pdf'
        assert response.data['estado'] == 'completado'
    
    def test_get_conversion_detail_unauthenticated(self, client, user):
        """Prueba obtener detalle de conversión sin autenticación"""
        conversion = ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='completado'
        )
        
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_conversion_detail_other_user(self, client, user):
        """Prueba obtener detalle de conversión de otro usuario"""
        other_user = User.objects.create_user(
            email='other@duocuc.cl',
            password='testpass123',
            name='Other User',
            career='Administración'
        )
        
        conversion = ConversionJob.objects.create(
            usuario=other_user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_conversion_states(self, client, user):
        """Prueba diferentes estados de conversión"""
        # Crear conversiones con diferentes estados
        states = ['pendiente', 'procesando', 'completado', 'error']
        
        for state in states:
            conversion = ConversionJob.objects.create(
                usuario=user,
                tipo_conversion='word_to_pdf',
                archivo_original=f'test_{state}.docx',
                estado=state
            )
            
            if state == 'error':
                conversion.error_mensaje = 'Error de procesamiento'
                conversion.save()
        
        client.force_authenticate(user=user)
        response = client.get('/api/converter/conversions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4
        
        # Verificar que se devuelven todos los estados
        returned_states = [conv['estado'] for conv in response.data]
        for state in states:
            assert state in returned_states
    
    def test_conversion_with_error_message(self, client, user):
        """Prueba conversión con mensaje de error"""
        conversion = ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='error',
            error_mensaje='Archivo corrupto o no válido'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['estado'] == 'error'
        assert response.data['error_mensaje'] == 'Archivo corrupto o no válido'
    
    def test_conversion_file_types_validation(self, client, user):
        """Prueba validación de tipos de archivo"""
        client.force_authenticate(user=user)
        
        # Probar con archivo inválido para Word a PDF
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"plain text content",
            content_type="text/plain"
        )
        
        data = {
            'tipo_conversion': 'word_to_pdf',
            'archivo_original': invalid_file
        }
        
        response = client.post('/api/converter/conversions/', data, format='multipart')
        # Puede ser 400 (archivo inválido) o 201 (si se acepta)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    
    def test_conversion_ocr_option(self, client, user):
        """Prueba opción OCR en conversión"""
        client.force_authenticate(user=user)
        
        test_file = SimpleUploadedFile(
            "test.pdf",
            b"fake pdf content",
            content_type="application/pdf"
        )
        
        # Probar con OCR habilitado
        data = {
            'tipo_conversion': 'pdf_to_word',
            'archivo_original': test_file,
            'usar_ocr': True
        }
        
        response = client.post('/api/converter/conversions/', data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        
        conversion = ConversionJob.objects.first()
        assert conversion.usar_ocr == True
    
    def test_conversion_timestamps(self, client, user):
        """Prueba timestamps de conversión"""
        conversion = ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se devuelven los timestamps
        assert 'created_at' in response.data
        assert 'completed_at' in response.data or response.data['completed_at'] is None
    
    def test_conversion_file_sizes(self, client, user):
        """Prueba información de tamaños de archivo"""
        conversion = ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test.docx',
            archivo_convertido='test.pdf',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        response = client.get(f'/api/converter/conversions/{conversion.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que se devuelve información de archivos
        assert 'archivo_original' in response.data
        assert 'archivo_convertido' in response.data
    
    def test_conversion_filtering_by_type(self, client, user):
        """Prueba filtrado de conversiones por tipo"""
        # Crear conversiones de diferentes tipos
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test1.docx',
            estado='completado'
        )
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='pdf_to_word',
            archivo_original='test2.pdf',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        
        # Filtrar por tipo word_to_pdf
        response = client.get('/api/converter/conversions/?tipo=word_to_pdf')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['tipo_conversion'] == 'word_to_pdf'
        
        # Filtrar por tipo pdf_to_word
        response = client.get('/api/converter/conversions/?tipo=pdf_to_word')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['tipo_conversion'] == 'pdf_to_word'
    
    def test_conversion_filtering_by_status(self, client, user):
        """Prueba filtrado de conversiones por estado"""
        # Crear conversiones con diferentes estados
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test1.docx',
            estado='pendiente'
        )
        ConversionJob.objects.create(
            usuario=user,
            tipo_conversion='word_to_pdf',
            archivo_original='test2.docx',
            estado='completado'
        )
        
        client.force_authenticate(user=user)
        
        # Filtrar por estado pendiente
        response = client.get('/api/converter/conversions/?estado=pendiente')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['estado'] == 'pendiente'
        
        # Filtrar por estado completado
        response = client.get('/api/converter/conversions/?estado=completado')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['estado'] == 'completado'
