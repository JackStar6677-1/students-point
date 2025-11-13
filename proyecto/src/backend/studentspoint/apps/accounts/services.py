"""Servicios para el módulo de autenticación y cuentas."""

import logging
from typing import Dict, Optional, Tuple
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from studentspoint.apps.campuses.models import Sede

logger = logging.getLogger(__name__)

User = get_user_model()

# Importar modelos de auditoría
try:
    from .models_audit import LoginLog, RegistrationLog, UserActivityLog
except ImportError:
    # Si no existen aún, definir None para evitar errores
    LoginLog = None
    RegistrationLog = None
    UserActivityLog = None


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
            'is_email_verified': usuario.is_email_verified,
            'is_staff': usuario.is_staff,
            'is_superuser': getattr(usuario, "is_superuser", False),
        }


class AuthService:
    """Servicio para lógica de autenticación."""
    
    DOMINIOS_LAXOS = ('@duocuc.cl', '@studentspoint.app')
    
    @classmethod
    def autenticar_usuario(cls, email: str, password: str, request=None) -> Tuple[Optional[User], Optional[str]]:
        """Autentica un usuario con email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            request: Request HTTP (opcional, para registrar IP y user agent)
            
        Returns:
            tuple: (usuario, mensaje_error) - Si hay error, usuario es None
        """
        email = email.lower()
        
        # Extraer información de la solicitud
        ip_address = None
        user_agent = ''
        if request:
            ip_address = cls._obtener_ip_address(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        try:
            user = User.objects.get(email=email)
            logger.info(f"Login attempt for user: {email}")
        except User.DoesNotExist:
            logger.warning(f"Login failed: User {email} not found")
            # Registrar login fallido
            if LoginLog:
                LoginLog.objects.create(
                    usuario=None,
                    email_intentado=email,
                    estado=LoginLog.Estado.FALLIDO,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    razon_fallo='Usuario no encontrado'
                )
            return None, 'Credenciales inválidas'
        
        # Verificar email verificado
        if not cls._puede_iniciar_sesion(user):
            razon = 'Email no verificado'
            if LoginLog:
                LoginLog.objects.create(
                    usuario=user,
                    email_intentado=email,
                    estado=LoginLog.Estado.FALLIDO,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    razon_fallo=razon
                )
            return None, 'Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja e ingresa el código de verificación.'
        
        # Verificar contraseña
        if not user.check_password(password):
            logger.warning(f"Login failed: Invalid password for user {email}")
            # Registrar login fallido
            if LoginLog:
                LoginLog.objects.create(
                    usuario=user,
                    email_intentado=email,
                    estado=LoginLog.Estado.FALLIDO,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    razon_fallo='Contraseña incorrecta'
                )
            return None, 'Credenciales inválidas'
        
        # Registrar login exitoso
        if LoginLog:
            LoginLog.objects.create(
                usuario=user,
                email_intentado=email,
                estado=LoginLog.Estado.EXITOSO,
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        # Registrar actividad
        if UserActivityLog:
            UserActivityLog.objects.create(
                usuario=user,
                tipo=UserActivityLog.TipoActividad.LOGIN,
                descripcion=f'Login exitoso desde {ip_address or "IP desconocida"}',
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        logger.info(f"Login successful for user: {email}")
        return user, None
    
    @staticmethod
    def _obtener_ip_address(request):
        """Obtiene la IP real del cliente desde el request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
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
                     sede_nombre: Optional[str] = None, request=None) -> Tuple[Optional[User], Optional[str]]:
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
        
        # Extraer información de la solicitud para auditoría
        ip_address = None
        user_agent = ''
        if request:
            ip_address = cls._obtener_ip_address(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
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
            
            # Registrar registro exitoso
            if RegistrationLog:
                RegistrationLog.objects.create(
                    usuario=usuario,
                    email=email,
                    name_intentado=name,
                    career_intentada=career,
                    estado=RegistrationLog.Estado.PENDIENTE_VERIFICACION,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            
            # Registrar actividad
            if UserActivityLog:
                UserActivityLog.objects.create(
                    usuario=usuario,
                    tipo=UserActivityLog.TipoActividad.REGISTRO,
                    descripcion=f'Usuario registrado desde {ip_address or "IP desconocida"}',
                    ip_address=ip_address,
                    user_agent=user_agent,
                    datos_adicionales={'career': career, 'campus': campus.nombre if campus else None}
                )
            
            return usuario, None
            
        except Exception as e:
            logger.error(f"Error creando usuario {email}: {e}", exc_info=True)
            
            # Registrar registro fallido
            if RegistrationLog:
                RegistrationLog.objects.create(
                    usuario=None,
                    email=email,
                    name_intentado=name,
                    career_intentada=career,
                    estado=RegistrationLog.Estado.FALLIDO,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    razon_fallo=str(e)
                )
            
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

