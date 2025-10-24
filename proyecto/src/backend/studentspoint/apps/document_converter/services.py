"""
Servicios de conversión de documentos
"""
import os
import logging
from pathlib import Path
from django.core.files.base import ContentFile
from django.utils import timezone

logger = logging.getLogger(__name__)


class DocumentConverter:
    """Conversor de documentos Word-PDF y PDF-Word"""
    
    @staticmethod
    def word_to_pdf(word_file_path, output_path=None):
        """Convierte Word a PDF usando python-docx y reportlab"""
        try:
            from docx import Document
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
            
            # Leer documento Word
            doc = Document(word_file_path)
            
            # Crear PDF
            if output_path is None:
                output_path = str(word_file_path).replace('.docx', '.pdf').replace('.doc', '.pdf')
            
            pdf = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#1a0933',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            )
            
            # Procesar párrafos del Word
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():
                    # Detectar si es título
                    if i == 0 or paragraph.style.name.startswith('Heading'):
                        story.append(Paragraph(paragraph.text, title_style))
                    else:
                        story.append(Paragraph(paragraph.text, normal_style))
                    story.append(Spacer(1, 0.2 * inch))
            
            # Construir PDF
            pdf.build(story)
            
            logger.info(f"Conversion Word a PDF exitosa: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error convirtiendo Word a PDF: {e}", exc_info=True)
            raise
    
    @staticmethod
    def pdf_to_word(pdf_file_path, output_path=None, usar_ocr=False):
        """Convierte PDF a Word usando PyPDF2 y python-docx"""
        try:
            from PyPDF2 import PdfReader
            from docx import Document
            from docx.shared import Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            # Leer PDF
            reader = PdfReader(pdf_file_path)
            
            # Crear documento Word
            doc = Document()
            
            # Configurar estilos
            style = doc.styles['Normal']
            font = style.font
            font.name = 'Arial'
            font.size = Pt(11)
            
            # Extraer texto de cada página
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                
                if usar_ocr and not text.strip():
                    # Si no hay texto, intentar OCR
                    text = DocumentConverter._extract_with_ocr(pdf_file_path, page_num)
                
                if text.strip():
                    # Agregar número de página
                    heading = doc.add_heading(f'Pagina {page_num + 1}', level=2)
                    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    # Agregar contenido
                    paragraphs = text.split('\n')
                    for para_text in paragraphs:
                        if para_text.strip():
                            p = doc.add_paragraph(para_text)
                            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    
                    # Separador de página
                    if page_num < len(reader.pages) - 1:
                        doc.add_page_break()
            
            # Guardar documento Word
            if output_path is None:
                output_path = str(pdf_file_path).replace('.pdf', '.docx')
            
            doc.save(output_path)
            
            logger.info(f"Conversion PDF a Word exitosa: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error convirtiendo PDF a Word: {e}", exc_info=True)
            raise
    
    @staticmethod
    def _extract_with_ocr(pdf_path, page_num):
        """Extrae texto usando OCR (pytesseract)"""
        try:
            from pdf2image import convert_from_path
            import pytesseract
            
            # Convertir página a imagen
            images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
            
            if images:
                # Aplicar OCR
                text = pytesseract.image_to_string(images[0], lang='spa')
                return text
            return ""
            
        except Exception as e:
            logger.warning(f"OCR fallido en pagina {page_num}: {e}")
            return ""


def convert_document(conversion_job):
    """Ejecuta la conversión de documento"""
    from .models import ConversionJob
    
    try:
        conversion_job.estado = ConversionJob.Estado.PROCESANDO
        conversion_job.save()
        
        # Obtener rutas
        input_path = conversion_job.archivo_original.path
        
        # Ejecutar conversión según tipo
        if conversion_job.tipo_conversion == ConversionJob.TipoConversion.WORD_TO_PDF:
            output_path = DocumentConverter.word_to_pdf(input_path)
            output_filename = Path(input_path).stem + '.pdf'
        else:
            output_path = DocumentConverter.pdf_to_word(
                input_path, 
                usar_ocr=conversion_job.usar_ocr
            )
            output_filename = Path(input_path).stem + '.docx'
        
        # Guardar archivo convertido
        with open(output_path, 'rb') as f:
            conversion_job.archivo_convertido.save(
                output_filename,
                ContentFile(f.read()),
                save=False
            )
        
        # Actualizar estado
        conversion_job.estado = ConversionJob.Estado.COMPLETADO
        conversion_job.completed_at = timezone.now()
        conversion_job.save()
        
        # Limpiar archivo temporal
        if os.path.exists(output_path) and output_path != conversion_job.archivo_convertido.path:
            os.remove(output_path)
        
        logger.info(f"Conversion completada: {conversion_job.id}")
        return True
        
    except Exception as e:
        conversion_job.estado = ConversionJob.Estado.ERROR
        conversion_job.error_mensaje = str(e)
        conversion_job.save()
        logger.error(f"Error en conversion {conversion_job.id}: {e}", exc_info=True)
        return False

