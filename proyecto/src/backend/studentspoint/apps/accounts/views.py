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
    StatusResponseSerializer, VerificarEmailSerializer, ReenviarCodigoSerializer,
    SolicitarRecuperacionSerializer, VerificarCodigoRecuperacionSerializer,
    ResetearPasswordSerializer, CambiarCarreraSerializer, CarrerasDisponiblesSerializer
)
from .models import CARRERAS_DISPONIBLES
from studentspoint.apps.campuses.models import Sede
from studentspoint.utils import verify_recaptcha

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
@api_view(['PATCH', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Actualiza el perfil del usuario."""
    # Verificar que el usuario esté autenticado
    if not request.user or not request.user.is_authenticated:
        return Response(
            {'error': 'Usuario no autenticado'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = UserUpdateSerializer(data=request.data, partial=True)
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
        # Verificación reCAPTCHA (no estricta)
        captcha_token = request.data.get('captcha_token')
        _ok, _score = verify_recaptcha(captcha_token, request.META.get('REMOTE_ADDR'))
        
        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Requerir email verificado salvo dominios institucionales permitidos
        if not user.is_email_verified:
            email_l = (user.email or '').lower()
            dominios_laxos = ('@duocuc.cl', '@studentspoint.app')
            if not any(email_l.endswith(d) for d in dominios_laxos):
                return Response(
                    {'error': 'Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja e ingresa el código de verificación.'},
                    status=status.HTTP_400_BAD_REQUEST
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
    # Verificación reCAPTCHA (no estricta)
    captcha_token = request.data.get('captcha_token')
    _ok, _score = verify_recaptcha(captcha_token, request.META.get('REMOTE_ADDR'))
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
            'is_email_verified': False,  # Requiere verificación
        }
        if campus is not None:
            user_kwargs['campus'] = campus

        user = User.objects.create_user(**user_kwargs)
        
        # Enviar código de verificación por email
        exito, mensaje = user.enviar_codigo_verificacion()
        
        # Generar tokens JWT (usuario puede usar la app pero con limitaciones)
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
                'career': user.career,
                'is_email_verified': user.is_email_verified
            },
            'verification_email_sent': exito,
            'message': 'Usuario registrado. Por favor verifica tu email con el código enviado.'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Error creando usuario: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    summary="Verificar email con código",
    request=VerificarEmailSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verificar_email(request):
    """Verifica el email del usuario con el código enviado."""
    # Aceptar alias 'code' además de 'codigo' para compatibilidad
    payload = request.data.copy()
    if 'codigo' not in payload and 'code' in payload:
        payload['codigo'] = payload.get('code')
    serializer = VerificarEmailSerializer(data=payload)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    codigo = serializer.validated_data['codigo']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Usuario no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    exito, mensaje = user.verificar_codigo_email(codigo)
    
    if exito:
        return Response({
            'status': 'success',
            'message': mensaje
        })
    else:
        return Response(
            {'status': 'error', 'message': mensaje}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    summary="Reenviar código de verificación",
    request=ReenviarCodigoSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reenviar_codigo_verificacion(request):
    """Reenvía el código de verificación al email del usuario."""
    serializer = ReenviarCodigoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Usuario no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if user.is_email_verified:
        return Response({
            'status': 'info',
            'message': 'El email ya está verificado'
        })
    
    exito, mensaje = user.enviar_codigo_verificacion()
    
    if exito:
        return Response({
            'status': 'success',
            'message': 'Código reenviado al email'
        })
    else:
        return Response(
            {'status': 'error', 'message': mensaje}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Solicitar recuperación de contraseña",
    request=SolicitarRecuperacionSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def solicitar_recuperacion_password(request):
    """Envía código de recuperación de contraseña al email."""
    serializer = SolicitarRecuperacionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Por seguridad, no revelar si el email existe o no
        return Response({
            'status': 'success',
            'message': 'Si el email existe, se enviará un código de recuperación'
        })
    
    exito, mensaje = user.enviar_codigo_recuperacion()
    
    return Response({
        'status': 'success',
        'message': 'Si el email existe, se enviará un código de recuperación'
    })


@extend_schema(
    summary="Verificar código de recuperación",
    request=VerificarCodigoRecuperacionSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verificar_codigo_recuperacion(request):
    """Verifica si el código de recuperación es válido."""
    serializer = VerificarCodigoRecuperacionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    codigo = serializer.validated_data['codigo']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Código inválido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exito, mensaje = user.verificar_codigo_recuperacion(codigo)
    
    if exito:
        return Response({
            'status': 'success',
            'message': 'Código válido. Procede a cambiar tu contraseña.'
        })
    else:
        return Response(
            {'status': 'error', 'message': mensaje}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    summary="Resetear contraseña con código",
    request=ResetearPasswordSerializer,
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resetear_password(request):
    """Resetea la contraseña del usuario usando el código de recuperación."""
    serializer = ResetearPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email'].lower()
    codigo = serializer.validated_data['codigo']
    nueva_password = serializer.validated_data['nueva_password']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Código inválido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar código
    exito, mensaje = user.verificar_codigo_recuperacion(codigo)
    
    if not exito:
        return Response(
            {'status': 'error', 'message': mensaje}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Cambiar contraseña
    user.resetear_password(nueva_password)
    
    return Response({
        'status': 'success',
        'message': 'Contraseña cambiada exitosamente'
    })


@extend_schema(
    summary="Cambiar contraseña (usuario autenticado)",
    responses={200: StatusResponseSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cambiar_password(request):
    """Permite a un usuario autenticado cambiar su contraseña."""
    password_actual = request.data.get('password_actual')
    nueva_password = request.data.get('nueva_password')
    confirmar_password = request.data.get('confirmar_password')
    
    if not all([password_actual, nueva_password, confirmar_password]):
        return Response(
            {'status': 'error', 'message': 'Todos los campos son requeridos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if nueva_password != confirmar_password:
        return Response(
            {'status': 'error', 'message': 'Las contraseñas no coinciden'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(nueva_password) < 8:
        return Response(
            {'status': 'error', 'message': 'La contraseña debe tener al menos 8 caracteres'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar contraseña actual
    if not request.user.check_password(password_actual):
        return Response(
            {'status': 'error', 'message': 'Contraseña actual incorrecta'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Cambiar contraseña
    request.user.set_password(nueva_password)
    request.user.save()
    
    return Response({
        'status': 'success',
        'message': 'Contraseña cambiada exitosamente'
    })


@extend_schema(
    summary="Cambiar carrera del usuario",
    request=CambiarCarreraSerializer,
    responses={200: UserDetailSerializer}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cambiar_carrera_usuario(request):
    """Permite al usuario cambiar su carrera/área de estudio."""
    serializer = CambiarCarreraSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    nueva_carrera = serializer.validated_data['nueva_carrera']
    razon = serializer.validated_data.get('razon', 'Cambio de carrera')
    
    # Validar que la carrera esté en la lista de disponibles
    # Normalizar para comparar con acentos: comparar en minúsculas sin tildes
    import unicodedata
    def norm(s):
        return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).lower()
    disponibles_norm = [norm(c) for c in CARRERAS_DISPONIBLES]
    if norm(nueva_carrera) not in disponibles_norm:
        return Response(
            {'status': 'error', 'message': f'Carrera no disponible. Opciones: {", ".join(CARRERAS_DISPONIBLES)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Cambiar carrera
    # Usar la forma original con acentos de la carrera elegida si hay match
    try:
        idx = disponibles_norm.index(norm(nueva_carrera))
        nueva_carrera_normalizada = CARRERAS_DISPONIBLES[idx]
    except ValueError:
        nueva_carrera_normalizada = nueva_carrera
    resultado = request.user.cambiar_carrera(nueva_carrera_normalizada, razon)
    
    # Retornar perfil actualizado
    user_serializer = UserDetailSerializer(request.user, context={'request': request})
    return Response({
        'status': 'success',
        'message': resultado['mensaje'],
        'user': user_serializer.data
    })


@extend_schema(
    summary="Obtener lista de carreras disponibles",
    responses={200: CarrerasDisponiblesSerializer}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def lista_carreras(request):
    """Retorna la lista de carreras disponibles en la plataforma."""
    return Response({
        'carreras': CARRERAS_DISPONIBLES
    })