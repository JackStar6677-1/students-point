"""Utilidades para el módulo de conversión de documentos."""

import os
from pathlib import Path
from typing import Tuple, Optional
from django.core.exceptions import ValidationError


# Constantes de validación
MAX_FILE_SIZE_MB = 50  # 50 MB máximo
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_WORD_EXTENSIONS = ['.doc', '.docx']
ALLOWED_PDF_EXTENSIONS = ['.pdf']

ALLOWED_WORD_MIME_TYPES = [
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]
ALLOWED_PDF_MIME_TYPES = ['application/pdf']


class FileValidationError(Exception):
    """Excepción para errores de validación de archivos."""
    pass


class DocumentValidator:
    """Validador de documentos para conversión."""
    
    @staticmethod
    def validate_word_file(file, max_size: int = MAX_FILE_SIZE_BYTES) -> Tuple[bool, Optional[str]]:
        """Valida un archivo Word.
        
        Args:
            file: Archivo Django o objeto con atributos name y size
            max_size: Tamaño máximo en bytes
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not file:
            return False, "No se proporcionó ningún archivo"
        
        # Validar tamaño
        if hasattr(file, 'size') and file.size > max_size:
            size_mb = file.size / (1024 * 1024)
            max_mb = max_size / (1024 * 1024)
            return False, f"El archivo es demasiado grande ({size_mb:.2f} MB). Tamaño máximo: {max_mb} MB"
        
        if file.size == 0:
            return False, "El archivo está vacío"
        
        # Validar extensión
        if hasattr(file, 'name'):
            file_path = Path(file.name)
            extension = file_path.suffix.lower()
            
            if extension not in ALLOWED_WORD_EXTENSIONS:
                return False, f"Extensión no permitida: {extension}. Extensiones permitidas: {', '.join(ALLOWED_WORD_EXTENSIONS)}"
        
        return True, None
    
    @staticmethod
    def validate_pdf_file(file, max_size: int = MAX_FILE_SIZE_BYTES) -> Tuple[bool, Optional[str]]:
        """Valida un archivo PDF.
        
        Args:
            file: Archivo Django o objeto con atributos name y size
            max_size: Tamaño máximo en bytes
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not file:
            return False, "No se proporcionó ningún archivo"
        
        # Validar tamaño
        if hasattr(file, 'size') and file.size > max_size:
            size_mb = file.size / (1024 * 1024)
            max_mb = max_size / (1024 * 1024)
            return False, f"El archivo es demasiado grande ({size_mb:.2f} MB). Tamaño máximo: {max_mb} MB"
        
        if file.size == 0:
            return False, "El archivo está vacío"
        
        # Validar extensión
        if hasattr(file, 'name'):
            file_path = Path(file.name)
            extension = file_path.suffix.lower()
            
            if extension not in ALLOWED_PDF_EXTENSIONS:
                return False, f"Extensión no permitida: {extension}. Extensión permitida: .pdf"
        
        return True, None
    
    @staticmethod
    def validate_file_for_conversion(file, conversion_type: str, max_size: int = MAX_FILE_SIZE_BYTES) -> Tuple[bool, Optional[str]]:
        """Valida un archivo según el tipo de conversión.
        
        Args:
            file: Archivo a validar
            conversion_type: 'word_to_pdf' o 'pdf_to_word'
            max_size: Tamaño máximo en bytes
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if conversion_type == 'word_to_pdf':
            return DocumentValidator.validate_word_file(file, max_size)
        elif conversion_type == 'pdf_to_word':
            return DocumentValidator.validate_pdf_file(file, max_size)
        else:
            return False, f"Tipo de conversión inválido: {conversion_type}"
    
    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, Optional[str]]:
        """Valida que un archivo exista y sea accesible.
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not file_path:
            return False, "Ruta de archivo no proporcionada"
        
        path = Path(file_path)
        
        if not path.exists():
            return False, f"El archivo no existe: {file_path}"
        
        if not path.is_file():
            return False, f"La ruta no es un archivo: {file_path}"
        
        if not os.access(file_path, os.R_OK):
            return False, f"No se tiene permiso de lectura para: {file_path}"
        
        if path.stat().st_size == 0:
            return False, f"El archivo está vacío: {file_path}"
        
        return True, None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitiza un nombre de archivo para evitar problemas.
        
        Args:
            filename: Nombre de archivo original
            
        Returns:
            str: Nombre de archivo sanitizado
        """
        # Eliminar caracteres peligrosos
        dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limitar longitud
        if len(sanitized) > 255:
            name_part = Path(sanitized).stem[:200]
            ext_part = Path(sanitized).suffix
            sanitized = name_part + ext_part
        
        return sanitized

