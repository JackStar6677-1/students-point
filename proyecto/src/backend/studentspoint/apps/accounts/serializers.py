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
    picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "name", "campus", "campus_nombre", "career", "semestre",
            "role", "role_display", "es_duoc", "es_gmail", "es_estudiante_gmail", 
            "telefono", "linkedin_url", "github_url", "picture_file", "picture_url",
            "is_email_verified", "date_joined"
        ]
        read_only_fields = ["id", "date_joined", "is_email_verified", "picture_url"]
    
    def get_picture_url(self, obj):
        """Retorna la URL de la foto de perfil."""
        if obj.picture_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.picture_file.url)
            return obj.picture_file.url
        elif obj.picture:
            return obj.picture
        return None


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
    semestre = serializers.IntegerField(required=False, min_value=1, max_value=12)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    github_url = serializers.URLField(required=False, allow_blank=True)
    picture_file = serializers.ImageField(required=False)


class EmailCheckSerializer(serializers.Serializer):
    """Datos para verificar disponibilidad de email."""
    
    email = serializers.EmailField()


class StatusResponseSerializer(serializers.Serializer):
    """Respuesta simple de estado."""
    
    status = serializers.CharField()
    message = serializers.CharField(required=False)


class VerificarEmailSerializer(serializers.Serializer):
    """Datos para verificar email con código."""
    
    email = serializers.EmailField()
    codigo = serializers.CharField(min_length=6, max_length=6)


class ReenviarCodigoSerializer(serializers.Serializer):
    """Datos para reenviar código de verificación."""
    
    email = serializers.EmailField()


class SolicitarRecuperacionSerializer(serializers.Serializer):
    """Datos para solicitar recuperación de contraseña."""
    
    email = serializers.EmailField()


class VerificarCodigoRecuperacionSerializer(serializers.Serializer):
    """Datos para verificar código de recuperación."""
    
    email = serializers.EmailField()
    codigo = serializers.CharField(min_length=6, max_length=6)


class ResetearPasswordSerializer(serializers.Serializer):
    """Datos para resetear contraseña."""
    
    email = serializers.EmailField()
    codigo = serializers.CharField(min_length=6, max_length=6)
    nueva_password = serializers.CharField(min_length=8)
    confirmar_password = serializers.CharField(min_length=8)
    
    def validate(self, attrs):
        if attrs['nueva_password'] != attrs['confirmar_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs


class CambiarCarreraSerializer(serializers.Serializer):
    """Datos para cambiar de carrera."""
    
    nueva_carrera = serializers.CharField(max_length=150)
    razon = serializers.CharField(required=False, allow_blank=True)


class CarrerasDisponiblesSerializer(serializers.Serializer):
    """Lista de carreras disponibles."""
    
    carreras = serializers.ListField(child=serializers.CharField())

