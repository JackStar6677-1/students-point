"""Serializadores utilizados en la app de cuentas."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class UserSerializer(serializers.ModelSerializer):
    """Representación básica del usuario para respuestas API."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "campus", "career", "role"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Representación completa del usuario para respuestas API."""
    
    campus_nombre = serializers.CharField(source="campus.nombre", read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "name", "campus", "campus_nombre", "career", "role", 
            "role_display", "es_duoc", "es_gmail", "es_estudiante_gmail", 
            "telefono", "linkedin_url", "github_url", "date_joined", "is_verified"
        ]
        read_only_fields = ["id", "date_joined", "is_verified"]


class LoginSerializer(serializers.Serializer):
    """Datos requeridos para autenticarse."""

    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    """Datos requeridos para registro de usuario."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField()
    name = serializers.CharField(max_length=150)
    career = serializers.CharField(max_length=100, required=False)
    telefono = serializers.CharField(max_length=20, required=False)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs


class TokenPairSerializer(serializers.Serializer):
    """Tokens JWT de acceso y refresco."""

    access = serializers.CharField()
    refresh = serializers.CharField()


class UserUpdateSerializer(serializers.Serializer):
    """Datos para actualizar perfil de usuario."""
    
    name = serializers.CharField(max_length=150, required=False)
    career = serializers.CharField(max_length=100, required=False)
    telefono = serializers.CharField(max_length=20, required=False)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    github_url = serializers.URLField(required=False, allow_blank=True)


class EmailCheckSerializer(serializers.Serializer):
    """Datos para verificar disponibilidad de email."""
    
    email = serializers.EmailField()


class StatusResponseSerializer(serializers.Serializer):
    """Respuesta simple de estado."""
    
    status = serializers.CharField()
    message = serializers.CharField(required=False)

