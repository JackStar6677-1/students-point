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
    
    # Campos adicionales para Gmail
    es_estudiante_gmail = models.BooleanField(default=False, help_text="True si es estudiante con Gmail")
    telefono = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
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

