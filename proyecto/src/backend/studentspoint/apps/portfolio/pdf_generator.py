"""
Generador de PDF para Portfolio usando ReportLab
Funciona en Windows, Linux y macOS
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
from django.conf import settings
import os


class PortfolioPDFGenerator:
    """Generador de PDF para portfolios estudiantiles"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0066CC')
        ))
        
        # Subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#004499')
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Información de contacto
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        ))
    
    def generate_portfolio_pdf(self, portfolio_data, output_path=None):
        """
        Generar PDF del portfolio
        
        Args:
            portfolio_data: Diccionario con datos del portfolio
            output_path: Ruta donde guardar el PDF (opcional)
        
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        if output_path:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
        else:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Construir el contenido del PDF
        story = []
        
        # Título principal
        title = Paragraph(f"Portfolio de {portfolio_data.get('nombre', 'Estudiante')}", 
                         self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Información de contacto
        contact_info = self._build_contact_info(portfolio_data)
        story.extend(contact_info)
        story.append(Spacer(1, 20))
        
        # Resumen profesional
        if portfolio_data.get('resumen'):
            story.append(Paragraph("Resumen Profesional", self.styles['CustomHeading']))
            story.append(Paragraph(portfolio_data['resumen'], self.styles['CustomBody']))
            story.append(Spacer(1, 15))
        
        # Habilidades técnicas
        if portfolio_data.get('habilidades'):
            story.append(Paragraph("Habilidades Técnicas", self.styles['CustomHeading']))
            skills_table = self._build_skills_table(portfolio_data['habilidades'])
            story.append(skills_table)
            story.append(Spacer(1, 15))
        
        # Proyectos
        if portfolio_data.get('proyectos'):
            story.append(Paragraph("Proyectos Destacados", self.styles['CustomHeading']))
            for proyecto in portfolio_data['proyectos']:
                story.extend(self._build_project_section(proyecto))
            story.append(Spacer(1, 15))
        
        # Experiencia laboral
        if portfolio_data.get('experiencia'):
            story.append(Paragraph("Experiencia Laboral", self.styles['CustomHeading']))
            for exp in portfolio_data['experiencia']:
                story.extend(self._build_experience_section(exp))
            story.append(Spacer(1, 15))
        
        # Educación
        if portfolio_data.get('educacion'):
            story.append(Paragraph("Educación", self.styles['CustomHeading']))
            for edu in portfolio_data['educacion']:
                story.extend(self._build_education_section(edu))
            story.append(Spacer(1, 15))
        
        # Logros y certificaciones
        if portfolio_data.get('logros'):
            story.append(Paragraph("Logros y Certificaciones", self.styles['CustomHeading']))
            for logro in portfolio_data['logros']:
                story.append(Paragraph(f"• {logro}", self.styles['CustomBody']))
            story.append(Spacer(1, 15))
        
        # Construir el PDF
        doc.build(story)
        
        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer
    
    def _build_contact_info(self, portfolio_data):
        """Construir sección de información de contacto"""
        story = []
        
        contact_items = []
        if portfolio_data.get('email'):
            contact_items.append(f" {portfolio_data['email']}")
        if portfolio_data.get('telefono'):
            contact_items.append(f" {portfolio_data['telefono']}")
        if portfolio_data.get('linkedin'):
            contact_items.append(f" LinkedIn: {portfolio_data['linkedin']}")
        if portfolio_data.get('github'):
            contact_items.append(f" GitHub: {portfolio_data['github']}")
        if portfolio_data.get('sitio_web'):
            contact_items.append(f" Sitio Web: {portfolio_data['sitio_web']}")
        
        if contact_items:
            contact_text = " | ".join(contact_items)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        return story
    
    def _build_skills_table(self, habilidades):
        """Construir tabla de habilidades"""
        # Organizar habilidades en columnas
        skills_data = []
        for i in range(0, len(habilidades), 3):
            row = []
            for j in range(3):
                if i + j < len(habilidades):
                    skill = habilidades[i + j]
                    row.append(f"• {skill}")
                else:
                    row.append("")
            skills_data.append(row)
        
        if not skills_data:
            return Spacer(1, 10)
        
        table = Table(skills_data, colWidths=[2*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _build_project_section(self, proyecto):
        """Construir sección de proyecto"""
        story = []
        
        # Título del proyecto
        title = Paragraph(f"<b>{proyecto.get('titulo', 'Proyecto')}</b>", self.styles['CustomBody'])
        story.append(title)
        
        # Descripción
        if proyecto.get('descripcion'):
            desc = Paragraph(proyecto['descripcion'], self.styles['CustomBody'])
            story.append(desc)
        
        # Tecnologías
        if proyecto.get('tecnologias'):
            techs = ", ".join(proyecto['tecnologias'])
            tech_text = Paragraph(f"<i>Tecnologías: {techs}</i>", self.styles['CustomBody'])
            story.append(tech_text)
        
        # Enlace
        if proyecto.get('enlace'):
            link_text = Paragraph(f"Enlace: {proyecto['enlace']}", self.styles['CustomBody'])
            story.append(link_text)
        
        story.append(Spacer(1, 10))
        return story
    
    def _build_experience_section(self, experiencia):
        """Construir sección de experiencia"""
        story = []
        
        # Título y empresa
        title = f"<b>{experiencia.get('titulo', 'Posición')}</b> - {experiencia.get('empresa', 'Empresa')}"
        story.append(Paragraph(title, self.styles['CustomBody']))
        
        # Fechas
        if experiencia.get('fecha_inicio') and experiencia.get('fecha_fin'):
            dates = f"{experiencia['fecha_inicio']} - {experiencia['fecha_fin']}"
            story.append(Paragraph(f"<i>{dates}</i>", self.styles['CustomBody']))
        
        # Descripción
        if experiencia.get('descripcion'):
            desc = Paragraph(experiencia['descripcion'], self.styles['CustomBody'])
            story.append(desc)
        
        story.append(Spacer(1, 10))
        return story
    
    def _build_education_section(self, educacion):
        """Construir sección de educación"""
        story = []
        
        # Título y institución
        title = f"<b>{educacion.get('titulo', 'Título')}</b> - {educacion.get('institucion', 'Institución')}"
        story.append(Paragraph(title, self.styles['CustomBody']))
        
        # Fechas
        if educacion.get('fecha_inicio') and educacion.get('fecha_fin'):
            dates = f"{educacion['fecha_inicio']} - {educacion['fecha_fin']}"
            story.append(Paragraph(f"<i>{dates}</i>", self.styles['CustomBody']))
        
        # Descripción
        if educacion.get('descripcion'):
            desc = Paragraph(educacion['descripcion'], self.styles['CustomBody'])
            story.append(desc)
        
        story.append(Spacer(1, 10))
        return story


def generate_portfolio_pdf(portfolio_data, output_path=None):
    """
    Función de conveniencia para generar PDF del portfolio
    
    Args:
        portfolio_data: Diccionario con datos del portfolio
        output_path: Ruta donde guardar el PDF (opcional)
    
    Returns:
        BytesIO o str: Buffer con el PDF o ruta del archivo
    """
    generator = PortfolioPDFGenerator()
    return generator.generate_portfolio_pdf(portfolio_data, output_path)

