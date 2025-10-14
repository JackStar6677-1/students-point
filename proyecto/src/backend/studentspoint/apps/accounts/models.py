"""Modelos para la aplicación de cuentas.

Contiene el modelo de usuario personalizado utilizado por todo el
proyecto. El objetivo principal es extender el modelo por defecto de
`django.contrib.auth` para utilizar el correo electrónico como
identificador principal y agregar metadatos adicionales como la sede,
la carrera y el rol del usuario.

Para validar que sólo se utilicen correos institucionales se define el
validador :func:`validate_duoc_email`. Se permiten dominios StudentsPoint, 
DuocUC (compatibilidad) y Gmail.
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


STUDENTS_DOMAIN = "@studentspoint.app"
DUOC_DOMAIN = "@duocuc.cl"  # Mantener compatibilidad

# Carreras disponibles en la plataforma
CARRERAS_DISPONIBLES = [
    "Ingeniería en Informática",
    "Ingeniería en Conectividad y Redes",
    "Ingeniería en Construcción",
    "Ingeniería en Electricidad",
    "Ingeniería Industrial",
    "Derecho",
    "Medicina",
    "Arquitectura",
    "Psicología",
    "Administración de Empresas",
    "Contabilidad",
    "Técnico en Informática",
    "Estudiante Genérico",  # Para estudiantes en exploración o programas interdisciplinarios
]


def validate_duoc_email(value: str) -> None:
    """Ensure that the email is valid (any valid email domain allowed).

    Parameters
    ----------
    value:
        Correo electrónico ingresado por el usuario.

    Raises
    ------
    ValidationError
        Si el correo no es válido.
    """
    import re
    
    # Validar formato básico de email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError("Formato de email inválido")
    
    # Permitir cualquier dominio válido
    # Los dominios preferidos son @studentspoint.app, @duocuc.cl y @gmail.com
    # pero se aceptan otros dominios para mayor flexibilidad


class UserManager(BaseUserManager):
    """Administrador para el modelo :class:`User`.

    Maneja la creación de usuarios asegurando que siempre exista un
    correo válido. Las contraseñas se almacenan usando el método de
    hashing de Django.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        validate_duoc_email(email)
        email = self.normalize_email(email)
        
        # Marcar si es estudiante Gmail
        if email.lower().endswith("@gmail.com"):
            extra_fields.setdefault("es_estudiante_gmail", True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Usuario principal del sistema.

    Campos principales
    ------------------
    email:
        Identificador único del usuario. Debe pertenecer al dominio
        institucional ``@duocuc.cl``.
    name:
        Nombre visible del usuario.
    campus:
        Sede a la que pertenece el usuario. Es opcional para permitir
        registros tempranos.
    career:
        Carrera o programa del estudiante.
    role:
        Define los permisos generales del usuario dentro de la
        plataforma. Para añadir nuevos roles basta con extender
        :class:`User.Roles`.
    """

    class Roles(models.TextChoices):
        STUDENT = "student", "Student"
        MODERATOR = "moderator", "Moderator"
        DIRECTOR_CARRERA = "director_carrera", "Director de Carrera"
        ADMIN_GLOBAL = "admin_global", "Administrador Global"

    email = models.EmailField("email address", unique=True, validators=[validate_duoc_email])
    name = models.CharField(max_length=150)
    campus = models.ForeignKey(
        "campuses.Sede", on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    career = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    semestre = models.PositiveIntegerField(default=1, help_text="Semestre actual del estudiante")
    
    # Campos adicionales para Gmail
    es_estudiante_gmail = models.BooleanField(default=False, help_text="True si es estudiante con Gmail")
    telefono = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Foto de perfil
    picture_file = models.ImageField(upload_to='profiles/', null=True, blank=True, help_text="Foto de perfil del usuario")
    
    # Verificacion de email
    email_verification_code = models.CharField(max_length=6, blank=True, help_text="Codigo de verificacion de 6 digitos")
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False, help_text="True si el email fue verificado")
    
    # Recuperacion de contraseña
    password_reset_code = models.CharField(max_length=6, blank=True, help_text="Codigo de recuperacion de contraseña")
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Campos para OAuth de Google
    google_id = models.CharField(max_length=100, blank=True, help_text="ID único de Google")
    picture = models.URLField(blank=True, help_text="URL de la foto de perfil de Google")
    is_verified = models.BooleanField(default=False, help_text="True si el email está verificado")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return self.email
    
    @property
    def es_duoc(self) -> bool:
        """Verifica si el usuario tiene correo institucional."""
        return self.email.lower().endswith(DUOC_DOMAIN)
    
    @property
    def es_gmail(self) -> bool:
        """Verifica si el usuario tiene correo Gmail."""
        return self.email.lower().endswith("@gmail.com")
    
    def generar_codigo_verificacion(self):
        """Genera un código de verificación de 6 dígitos para email."""
        import random
        from django.utils import timezone
        
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.email_verification_code = codigo
        self.email_verification_sent_at = timezone.now()
        self.save(update_fields=['email_verification_code', 'email_verification_sent_at'])
        return codigo
    
    def verificar_codigo_email(self, codigo):
        """Verifica el código de verificación de email.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.email_verification_code:
            return False, "No hay código de verificación pendiente"
        
        if self.email_verification_code != codigo:
            return False, "Código incorrecto"
        
        # Verificar que no haya expirado (15 minutos)
        if self.email_verification_sent_at:
            expiracion = self.email_verification_sent_at + timedelta(minutes=15)
            if timezone.now() > expiracion:
                return False, "Código expirado"
        
        # Marcar como verificado
        self.is_email_verified = True
        self.email_verification_code = ''
        self.save(update_fields=['is_email_verified', 'email_verification_code'])
        return True, "Email verificado exitosamente"
    
    def generar_codigo_recuperacion(self):
        """Genera un código de recuperación de contraseña de 6 dígitos."""
        import random
        from django.utils import timezone
        
        codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.password_reset_code = codigo
        self.password_reset_sent_at = timezone.now()
        self.save(update_fields=['password_reset_code', 'password_reset_sent_at'])
        return codigo
    
    def verificar_codigo_recuperacion(self, codigo):
        """Verifica el código de recuperación de contraseña.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.password_reset_code:
            return False, "No hay código de recuperación pendiente"
        
        if self.password_reset_code != codigo:
            return False, "Código incorrecto"
        
        # Verificar que no haya expirado (30 minutos)
        if self.password_reset_sent_at:
            expiracion = self.password_reset_sent_at + timedelta(minutes=30)
            if timezone.now() > expiracion:
                return False, "Código expirado"
        
        return True, "Código válido"
    
    def resetear_password(self, nueva_password):
        """Resetea la contraseña del usuario."""
        self.set_password(nueva_password)
        self.password_reset_code = ''
        self.save(update_fields=['password', 'password_reset_code'])
    
    def enviar_codigo_verificacion(self):
        """Envía el código de verificación por email."""
        from django.core.mail import send_mail
        from django.conf import settings
        import logging
        
        logger = logging.getLogger(__name__)
        codigo = self.generar_codigo_verificacion()
        
        asunto = 'Verificación de email - StudentsPoint'
        mensaje = f'''
Hola {self.name},

Tu código de verificación es: {codigo}

Este código expirará en 15 minutos.

Si no solicitaste este código, puedes ignorar este email.

Saludos,
Equipo StudentsPoint
        '''
        
        logger.info(f"========================================")
        logger.info(f"CODIGO DE VERIFICACION PARA: {self.email}")
        logger.info(f"CODIGO: {codigo}")
        logger.info(f"========================================")
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
            )
            logger.info(f"Email de verificación enviado exitosamente a {self.email}")
            return True, "Código enviado"
        except Exception as e:
            logger.error(f"Error enviando email a {self.email}: {str(e)}")
            return False, f"Error enviando email: {str(e)}"
    
    def enviar_codigo_recuperacion(self):
        """Envía el código de recuperación de contraseña por email."""
        from django.core.mail import send_mail
        from django.conf import settings
        import logging
        
        logger = logging.getLogger(__name__)
        codigo = self.generar_codigo_recuperacion()
        
        asunto = 'Recuperación de contraseña - StudentsPoint'
        mensaje = f'''
Hola {self.name},

Tu código de recuperación de contraseña es: {codigo}

Este código expirará en 30 minutos.

Si no solicitaste este código, puedes ignorar este email.

Saludos,
Equipo StudentsPoint
        '''
        
        logger.info(f"========================================")
        logger.info(f"CODIGO DE RECUPERACION PARA: {self.email}")
        logger.info(f"CODIGO: {codigo}")
        logger.info(f"========================================")
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
            )
            logger.info(f"Email de recuperación enviado exitosamente a {self.email}")
            return True, "Código enviado"
        except Exception as e:
            logger.error(f"Error enviando email a {self.email}: {str(e)}")
            return False, f"Error enviando email: {str(e)}"
    
    def cambiar_carrera(self, nueva_carrera, razon=""):
        """Cambia la carrera del usuario.
        
        Al cambiar de carrera, el usuario pierde privilegios de publicación 
        en el foro de la carrera anterior y se le asigna automáticamente 
        el foro correspondiente a su nueva carrera.
        
        Args:
            nueva_carrera: Nombre de la nueva carrera
            razon: Razón del cambio (opcional)
        
        Returns:
            dict: Información sobre el cambio realizado
        """
        from django.utils import timezone
        
        carrera_anterior = self.career
        self.career = nueva_carrera
        self.save(update_fields=['career'])
        
        # Registrar el cambio
        CambioCarrera.objects.create(
            usuario=self,
            carrera_anterior=carrera_anterior,
            carrera_nueva=nueva_carrera,
            razon=razon
        )
        
        return {
            'usuario': self.email,
            'carrera_anterior': carrera_anterior,
            'carrera_nueva': nueva_carrera,
            'fecha_cambio': timezone.now(),
            'mensaje': f'Tu carrera ha sido cambiada de {carrera_anterior} a {nueva_carrera}. '
                      f'Ahora puedes crear publicaciones en el foro de {nueva_carrera}.'
        }


class CambioCarrera(models.Model):
    """Registra los cambios de carrera de los usuarios.
    
    Mantiene un historial de todos los cambios de carrera para auditoría.
    """
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cambios_carrera"
    )
    carrera_anterior = models.CharField(max_length=150)
    carrera_nueva = models.CharField(max_length=150)
    razon = models.TextField(blank=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_cambio']
        verbose_name = "Cambio de Carrera"
        verbose_name_plural = "Cambios de Carrera"
    
    def __str__(self):
        return f"{self.usuario.name}: {self.carrera_anterior} → {self.carrera_nueva}"

