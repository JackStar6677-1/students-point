"""Servicios para el módulo de foros."""

from typing import TYPE_CHECKING
import unicodedata
import re

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model
    User = get_user_model()


def normalizar_carrera(carrera: str) -> str:
    """Normaliza el nombre de una carrera para comparación.
    
    Elimina tildes, convierte a minúsculas y normaliza espacios.
    
    Args:
        carrera: Nombre de la carrera
        
    Returns:
        str: Nombre normalizado
    """
    if not carrera:
        return ""
    # Convertir a minúsculas
    carrera = carrera.lower()
    # Eliminar tildes y caracteres especiales
    carrera = unicodedata.normalize('NFD', carrera)
    carrera = ''.join(c for c in carrera if unicodedata.category(c) != 'Mn')
    # Normalizar espacios (múltiples espacios a uno solo)
    carrera = re.sub(r'\s+', ' ', carrera).strip()
    return carrera


class ForumPermissionService:
    """Servicio centralizado para gestionar permisos del foro."""
    
    ROLES_MODERADOR = ['moderator', 'admin_global']
    
    @classmethod
    def puede_moderar(cls, usuario) -> bool:
        """Verifica si un usuario puede moderar contenido.
        
        Args:
            usuario: Instancia de usuario de Django
            
        Returns:
            bool: True si el usuario puede moderar
        """
        if not usuario or not usuario.is_authenticated:
            return False
        return usuario.is_staff or usuario.role in cls.ROLES_MODERADOR
    
    @classmethod
    def puede_postear_en_foro(cls, usuario, foro) -> bool:
        """Verifica si un usuario puede crear posts en un foro específico.
        
        Args:
            usuario: Instancia de usuario de Django
            foro: Instancia del modelo Foro
            
        Returns:
            bool: True si el usuario puede postear en el foro
        """
        if not usuario or not usuario.is_authenticated:
            return False
            
        # Admin y moderadores pueden postear en todos los foros
        if cls.puede_moderar(usuario):
            return True
            
        # Usuario normal solo puede postear en foro de su carrera
        # Comparación normalizada para manejar diferencias de tildes y mayúsculas
        carrera_usuario = normalizar_carrera(usuario.career) if usuario.career else ""
        carrera_foro = normalizar_carrera(foro.carrera) if foro.carrera else ""
        return carrera_usuario == carrera_foro
    
    @classmethod
    def puede_ver_foro(cls, usuario, foro) -> bool:
        """Verifica si un usuario puede ver un foro.
        
        Args:
            usuario: Instancia de usuario de Django (puede ser None para anónimos)
            foro: Instancia del modelo Foro
            
        Returns:
            bool: True si el usuario puede ver el foro
        """
        # Foros públicos: todos pueden ver
        if not foro.es_privado:
            return True
            
        # Usuarios no autenticados no pueden ver foros privados
        if not usuario or not usuario.is_authenticated:
            return False
            
        # Admin y moderadores pueden ver todos los foros
        if cls.puede_moderar(usuario):
            return True
            
        # Usuario normal solo puede ver foros privados de su carrera
        # Comparación normalizada para manejar diferencias de tildes y mayúsculas
        carrera_usuario = normalizar_carrera(usuario.career) if usuario.career else ""
        carrera_foro = normalizar_carrera(foro.carrera) if foro.carrera else ""
        return carrera_usuario == carrera_foro
    
    @classmethod
    def filtrar_foros_visibles(cls, usuario, queryset):
        """Filtra un queryset de foros según los permisos del usuario.
        
        Args:
            usuario: Instancia de usuario de Django (puede ser None)
            queryset: QuerySet de Foro
            
        Returns:
            QuerySet: QuerySet filtrado de foros visibles
        """
        from django.db.models import Q
        
        # Admin y moderadores ven todos los foros
        if usuario and usuario.is_authenticated and cls.puede_moderar(usuario):
            return queryset
            
        # Para usuarios autenticados normales
        if usuario and usuario.is_authenticated:
            return queryset.filter(
                Q(es_privado=False) | 
                Q(es_privado=True, carrera=usuario.career)
            )
            
        # Usuarios no autenticados: solo foros públicos
        return queryset.filter(es_privado=False)


class PostValidationService:
    """Servicio para validar contenido de posts."""
    
    @staticmethod
    def determinar_estado_post(titulo: str, cuerpo: str, tiene_imagen: bool, 
                                imagen_aprobada: bool = False) -> str:
        """Determina el estado inicial de un post según su contenido.
        
        Args:
            titulo: Título del post
            cuerpo: Contenido del post
            tiene_imagen: Si el post tiene imagen adjunta
            imagen_aprobada: Si la imagen ya fue aprobada
            
        Returns:
            str: Estado del post (publicado, revision, etc.)
        """
        from .models import Post
        
        texto_completo = f"{titulo} {cuerpo}".lower()
        
        # Si tiene imagen sin aprobar, va a revisión
        if tiene_imagen and not imagen_aprobada:
            return Post.Estado.REVISION
        
        # Verificar palabras prohibidas
        from .utils import contiene_palabras_prohibidas, contiene_palabras_moderacion
        
        if contiene_palabras_prohibidas(texto_completo):
            return Post.Estado.REVISION
        
        # Verificar palabras que requieren moderación
        if contiene_palabras_moderacion(texto_completo):
            return Post.Estado.REVISION
        
        return Post.Estado.PUBLICADO

