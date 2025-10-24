"""Permisos personalizados basados en el rol del usuario."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsModerator(BasePermission):
    """Permite el acceso sólo a usuarios con rol ``moderator``."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - lógica simple
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Roles.MODERATOR)


class IsModeratorOrDirector(BasePermission):
    """Permite acceso a ``moderator`` o ``director_carrera``."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - lógica simple
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {User.Roles.MODERATOR, User.Roles.DIRECTOR_CARRERA}
        )

