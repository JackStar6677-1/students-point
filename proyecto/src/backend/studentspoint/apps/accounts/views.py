"""Views para autenticación y gestión de usuarios."""

import json
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import (
    UserDetailSerializer, LoginSerializer, RegisterSerializer, 
    TokenPairSerializer, UserUpdateSerializer, EmailCheckSerializer,
    StatusResponseSerializer
)
from studentspoint.apps.campuses.models import Sede

User = get_user_model()


@extend_schema(
    summary="Obtener información del usuario actual",
    responses={200: UserDetailSerializer}
)
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """Obtiene información del usuario actual."""
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    summary="Actualizar perfil del usuario",
    request=UserUpdateSerializer,
    responses={200: UserDetailSerializer}
)
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Actualiza el perfil del usuario."""
    serializer = UserUpdateSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        for field, value in serializer.validated_data.items():
            setattr(user, field, value)
        user.save()
        
        response_serializer = UserDetailSerializer(user)
        return Response(response_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Verificar si un email está permitido",
    request=EmailCheckSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_email(request):
    """Verifica si un email está permitido en el sistema."""
    serializer = EmailCheckSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    
    if email.endswith('@duocuc.cl'):
        return Response({
            'status': 'success',
            'message': 'Email institucional válido',
            'type': 'duoc'
        })
    elif email.endswith('@gmail.com'):
        return Response({
            'status': 'success',
            'message': 'Email Gmail válido para estudiantes',
            'type': 'gmail'
        })
    else:
        return Response({
            'status': 'error',
            'message': 'Solo se permiten correos @duocuc.cl o @gmail.com',
            'type': 'not_allowed'
        })


@extend_schema(
    summary="Iniciar sesión",
    responses={200: {"description": "Login exitoso"}, 400: {"description": "Credenciales inválidas"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """Inicia sesión con email y contraseña."""
    try:
        # Obtener datos del request
        if hasattr(request, 'data'):
            email = request.data.get('email', '').lower()
            password = request.data.get('password', '')
        else:
            # Fallback para request.POST
            email = request.POST.get('email', '').lower()
            password = request.POST.get('password', '')
        
        if not email or not password:
            return Response(
                {'detail': 'Email y contraseña son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar contraseña
        if user.check_password(password):
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role,
                    'campus': user.campus.nombre if user.campus else None,
                    'career': user.career
                }
            })
        else:
            return Response(
                {'detail': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        return Response(
            {'detail': f'Error en el servidor: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Registrar nuevo usuario",
    responses={201: {"description": "Usuario creado exitosamente"}, 400: {"description": "Datos inválidos"}}
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Registra un nuevo usuario.

    Acepta tanto el payload usado por el frontend (first_name, last_name, carrera, sede)
    como el payload directo del backend (name, career, campus).
    """
    email = (request.data.get('email') or '').lower()
    password = request.data.get('password', '')

    # Mapear nombre completo
    provided_name = request.data.get('name')
    if provided_name:
        name = provided_name
    else:
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        name = (first_name + ' ' + last_name).strip()

    role = request.data.get('role', 'student')

    # Mapear carrera
    career = request.data.get('career') or request.data.get('carrera', '')

    # Resolver campus: aceptar id en "campus" o nombre en "sede"
    campus = None
    campus_id = request.data.get('campus')
    sede_name = request.data.get('sede')
    if campus_id:
        try:
            campus_id = int(campus_id)
            campus = Sede.objects.filter(id=campus_id).first()
        except (TypeError, ValueError):
            campus = None
    elif sede_name:
        campus = Sede.objects.filter(nombre__iexact=sede_name.strip()).first()
    
    # Validaciones
    if not all([email, password, name, career]):
        return Response(
            {'detail': 'Todos los campos son requeridos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(password) < 8:
        return Response(
            {'detail': 'La contraseña debe tener al menos 8 caracteres'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar si el email ya existe
    if User.objects.filter(email=email).exists():
        return Response(
            {'detail': 'Este email ya está registrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Crear usuario (campus es opcional)
        user_kwargs = {
            'email': email,
            'password': password,
            'name': name,
            'role': role,
            'career': career,
        }
        if campus is not None:
            user_kwargs['campus'] = campus

        user = User.objects.create_user(**user_kwargs)
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'campus': user.campus.nombre if user.campus else None,
                'career': user.career
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Error creando usuario: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )