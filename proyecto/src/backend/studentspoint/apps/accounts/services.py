"""Servicios para el módulo de autenticación y cuentas."""

import logging
from typing import Dict, Optional, Tuple
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from studentspoint.apps.campuses.models import Sede

logger = logging.getLogger(__name__)

User = get_user_model()


class TokenService:
    """Servicio para generar y manejar tokens JWT."""
    
    @staticmethod
    def generar_tokens_usuario(usuario) -> Dict[str, str]:
        """Genera tokens JWT para un usuario.
        
        Args:
            usuario: Instancia de User
            
        Returns:
            dict: Diccionario con access y refresh tokens
        """
        refresh = RefreshToken.for_user(usuario)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
    
    @staticmethod
    def obtener_datos_usuario(usuario) -> Dict:
        """Obtiene datos del usuario para incluir en respuesta de autenticación.
        
        Args:
            usuario: Instancia de User
            
        Returns:
            dict: Datos del usuario
        """
        return {
            'id': usuario.id,
            'email': usuario.email,
            'name': usuario.name,
            'role': usuario.role,
            'campus': usuario.campus.nombre if usuario.campus else None,
            'career': usuario.career,
            'is_email_verified': usuario.is_email_verified
        }


class AuthService:
    """Servicio para lógica de autenticación."""
    
    DOMINIOS_LAXOS = ('@duocuc.cl', '@studentspoint.app')
    
    @classmethod
    def autenticar_usuario(cls, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """Autentica un usuario con email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            tuple: (usuario, mensaje_error) - Si hay error, usuario es None
        """
        email = email.lower()
        
        try:
            user = User.objects.get(email=email)
            logger.info(f"Login attempt for user: {email}")
        except User.DoesNotExist:
            logger.warning(f"Login failed: User {email} not found")
            return None, 'Credenciales inválidas'
        
        # Verificar email verificado
        if not cls._puede_iniciar_sesion(user):
            return None, 'Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja e ingresa el código de verificación.'
        
        # Verificar contraseña
        if not user.check_password(password):
            logger.warning(f"Login failed: Invalid password for user {email}")
            return None, 'Credenciales inválidas'
        
        logger.info(f"Login successful for user: {email}")
        return user, None
    
    @classmethod
    def _puede_iniciar_sesion(cls, usuario) -> bool:
        """Verifica si un usuario puede iniciar sesión.
        
        Args:
            usuario: Instancia de User
            
        Returns:
            bool: True si puede iniciar sesión
        """
        # Si el email está verificado, puede iniciar sesión
        if usuario.is_email_verified:
            return True
        
        # Dominios institucionales no requieren verificación
        email_l = (usuario.email or '').lower()
        if any(email_l.endswith(d) for d in cls.DOMINIOS_LAXOS):
            return True
        
        return False
    
    @classmethod
    def crear_usuario(cls, email: str, password: str, name: str, career: str, 
                      role: str = 'student', campus_id: Optional[int] = None,
                      sede_nombre: Optional[str] = None) -> Tuple[Optional[User], Optional[str]]:
        """Crea un nuevo usuario.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            name: Nombre del usuario
            career: Carrera del usuario
            role: Rol del usuario (default: 'student')
            campus_id: ID del campus (opcional)
            sede_nombre: Nombre de la sede (opcional)
            
        Returns:
            tuple: (usuario, mensaje_error) - Si hay error, usuario es None
        """
        email = email.lower()
        
        # Validaciones básicas
        if not all([email, password, name, career]):
            return None, 'Todos los campos son requeridos'
        
        if len(password) < 8:
            return None, 'La contraseña debe tener al menos 8 caracteres'
        
        # Verificar si el email ya existe
        if User.objects.filter(email=email).exists():
            return None, 'Este email ya está registrado'
        
        # Resolver campus
        campus = None
        if campus_id:
            try:
                campus = Sede.objects.filter(id=int(campus_id)).first()
            except (TypeError, ValueError):
                pass
        elif sede_nombre:
            campus = Sede.objects.filter(nombre__iexact=sede_nombre.strip()).first()
        
        try:
            user_kwargs = {
                'email': email,
                'password': password,
                'name': name,
                'role': role,
                'career': career,
                'is_email_verified': False
            }
            if campus:
                user_kwargs['campus'] = campus
            
            usuario = User.objects.create_user(**user_kwargs)
            logger.info(f"Usuario creado: {email}")
            return usuario, None
            
        except Exception as e:
            logger.error(f"Error creando usuario {email}: {e}", exc_info=True)
            return None, f'Error creando usuario: {str(e)}'


class EmailValidationService:
    """Servicio para validaciones de email."""
    
    @staticmethod
    def validar_tipo_email(email: str) -> Dict[str, str]:
        """Valida el tipo de email y si está permitido.
        
        Args:
            email: Email a validar
            
        Returns:
            dict: Información sobre el tipo de email
        """
        email_lower = email.lower()
        
        if email_lower.endswith('@duocuc.cl'):
            return {
                'status': 'success',
                'message': 'Email institucional válido',
                'type': 'duoc'
            }
        elif email_lower.endswith('@gmail.com'):
            return {
                'status': 'success',
                'message': 'Email Gmail válido para estudiantes',
                'type': 'gmail'
            }
        else:
            return {
                'status': 'error',
                'message': 'Solo se permiten correos @duocuc.cl o @gmail.com',
                'type': 'not_allowed'
            }
    
    @staticmethod
    def normalizar_email(email: str) -> str:
        """Normaliza un email (minúsculas, trim).
        
        Args:
            email: Email a normalizar
            
        Returns:
            str: Email normalizado
        """
        return email.lower().strip()


class PasswordValidationService:
    """Servicio para validaciones de contraseñas."""
    
    MIN_LENGTH = 8
    
    @classmethod
    def validar_longitud(cls, password: str) -> bool:
        """Valida que la contraseña tenga la longitud mínima.
        
        Args:
            password: Contraseña a validar
            
        Returns:
            bool: True si es válida
        """
        return len(password) >= cls.MIN_LENGTH
    
    @classmethod
    def validar_coincidencia(cls, password: str, confirmacion: str) -> bool:
        """Valida que dos contraseñas coincidan.
        
        Args:
            password: Contraseña
            confirmacion: Confirmación de contraseña
            
        Returns:
            bool: True si coinciden
        """
        return password == confirmacion
    
    @classmethod
    def obtener_fortaleza(cls, password: str) -> Dict[str, any]:
        """Calcula la fortaleza de una contraseña.
        
        Args:
            password: Contraseña a evaluar
            
        Returns:
            dict: Información sobre la fortaleza de la contraseña
        """
        fuerza = 0
        criterios = {
            'longitud': len(password) >= 8,
            'minuscula': bool(password and any(c.islower() for c in password)),
            'mayuscula': bool(password and any(c.isupper() for c in password)),
            'numero': bool(password and any(c.isdigit() for c in password)),
            'especial': bool(password and any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password))
        }
        
        fuerza = sum(1 for v in criterios.values() if v)
        
        if fuerza <= 2:
            nivel = 'debil'
        elif fuerza <= 3:
            nivel = 'media'
        elif fuerza <= 4:
            nivel = 'buena'
        else:
            nivel = 'excelente'
        
        return {
            'fuerza': fuerza,
            'nivel': nivel,
            'criterios': criterios
        }


class RegistrationDataMapper:
    """Mapea datos de registro desde diferentes formatos."""
    
    @staticmethod
    def extraer_datos_registro(request_data: Dict) -> Dict:
        """Extrae y normaliza datos de registro del request.
        
        Args:
            request_data: Datos del request
            
        Returns:
            dict: Datos normalizados para registro
        """
        email = EmailValidationService.normalizar_email(
            request_data.get('email', '')
        )
        
        # Mapear nombre
        name = request_data.get('name')
        if not name:
            first_name = request_data.get('first_name', '').strip()
            last_name = request_data.get('last_name', '').strip()
            name = (first_name + ' ' + last_name).strip()
        
        # Mapear carrera
        career = request_data.get('career') or request_data.get('carrera', '')
        
        # Mapear campus
        campus_id = request_data.get('campus')
        sede_nombre = request_data.get('sede')
        
        return {
            'email': email,
            'password': request_data.get('password', ''),
            'name': name,
            'career': career,
            'role': request_data.get('role', 'student'),
            'campus_id': campus_id,
            'sede_nombre': sede_nombre
        }

