"""Permisos personalizados basados en el rol del usuario."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsModerator(BasePermission):
    """Permite el acceso sólo a usuarios con rol ``moderator``."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - lógica simple
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Staff o superusuarios siempre pueden moderar
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        # Roles con permisos de moderación
        return user.role in {
            User.Roles.MODERATOR,
            User.Roles.ADMIN_GLOBAL,
            User.Roles.DIRECTOR_CARRERA,
        }


class IsModeratorOrDirector(BasePermission):
    """Permite acceso a ``moderator`` o ``director_carrera``."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - lógica simple
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        return user.role in {
            User.Roles.MODERATOR,
            User.Roles.DIRECTOR_CARRERA,
            User.Roles.ADMIN_GLOBAL,
        }

