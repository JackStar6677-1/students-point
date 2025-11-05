"""Views para autenticación y gestión de usuarios."""

import logging
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User, CARRERAS_DISPONIBLES
from .serializers import (
    UserDetailSerializer, LoginSerializer, RegisterSerializer, 
    TokenPairSerializer, UserUpdateSerializer, EmailCheckSerializer,
    StatusResponseSerializer, VerificarEmailSerializer, ReenviarCodigoSerializer,
    SolicitarRecuperacionSerializer, VerificarCodigoRecuperacionSerializer,
    ResetearPasswordSerializer, CambiarCarreraSerializer, CarrerasDisponiblesSerializer
)
from .services import (
    AuthService, TokenService, EmailValidationService, 
    PasswordValidationService, RegistrationDataMapper
)
from .utils import normalizar_carrera, formatear_respuesta_exito, formatear_respuesta_error
from studentspoint.utils import verify_recaptcha

User = get_user_model()
logger = logging.getLogger(__name__)


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
    
    email = EmailValidationService.normalizar_email(serializer.validated_data['email'])
    resultado = EmailValidationService.validar_tipo_email(email)
    
    return Response(resultado)


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
            email = EmailValidationService.normalizar_email(request.data.get('email', ''))
            password = request.data.get('password', '')
        else:
            # Fallback para request.POST
            email = EmailValidationService.normalizar_email(request.POST.get('email', ''))
            password = request.POST.get('password', '')
        
        if not email or not password:
            return Response(
                {'detail': 'Email y contraseña son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificación reCAPTCHA (no estricta)
        captcha_token = request.data.get('captcha_token')
        _ok, _score = verify_recaptcha(captcha_token, request.META.get('REMOTE_ADDR'))
        
        # Autenticar usuario usando el servicio (pasar request para auditoría)
        user, error_msg = AuthService.autenticar_usuario(email, password, request=request)
        
        if not user:
            status_code = status.HTTP_401_UNAUTHORIZED if 'Credenciales' in error_msg else status.HTTP_400_BAD_REQUEST
            return Response(
                {'detail': error_msg if 'Credenciales' in error_msg else error_msg, 
                 'error': error_msg if 'Credenciales' not in error_msg else None}, 
                status=status_code
            )
        
        # Generar tokens usando el servicio
        tokens = TokenService.generar_tokens_usuario(user)
        user_data = TokenService.obtener_datos_usuario(user)
        
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': user_data
        })
            
    except Exception as e:
        logger.error(f"Error en login: {e}", exc_info=True)
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
    # Verificación reCAPTCHA (no estricta)
    captcha_token = request.data.get('captcha_token')
    _ok, _score = verify_recaptcha(captcha_token, request.META.get('REMOTE_ADDR'))
    
    # Extraer y normalizar datos usando el mapper
    datos = RegistrationDataMapper.extraer_datos_registro(request.data)
    
    # Validar contraseña
    if not PasswordValidationService.validar_longitud(datos['password']):
        return Response(
            {'detail': 'La contraseña debe tener al menos 8 caracteres'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Crear usuario usando el servicio (pasar request para auditoría)
    user, error_msg = AuthService.crear_usuario(
        email=datos['email'],
        password=datos['password'],
        name=datos['name'],
        career=datos['career'],
        role=datos['role'],
        campus_id=datos.get('campus_id'),
        sede_nombre=datos.get('sede_nombre'),
        request=request
    )
    
    if not user:
        return Response(
            {'detail': error_msg}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Enviar código de verificación por email
        exito, mensaje = user.enviar_codigo_verificacion()
        
        # Generar tokens JWT usando el servicio
        tokens = TokenService.generar_tokens_usuario(user)
        user_data = TokenService.obtener_datos_usuario(user)
        
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': user_data,
            'verification_email_sent': exito,
            'message': 'Usuario registrado. Por favor verifica tu email con el código enviado.'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error después de crear usuario {datos['email']}: {e}", exc_info=True)
        return Response(
            {'detail': f'Error enviando código de verificación: {str(e)}'}, 
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
        # Generar tokens JWT para iniciar sesión automáticamente usando el servicio
        tokens = TokenService.generar_tokens_usuario(user)
        user_data = TokenService.obtener_datos_usuario(user)
        
        return Response({
            'status': 'success',
            'message': mensaje,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': user_data
        })
    else:
        return Response(
            formatear_respuesta_error(mensaje), 
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
        return Response(formatear_respuesta_exito('El email ya está verificado', {'status': 'info'}))
    
    exito, mensaje = user.enviar_codigo_verificacion()
    
    if exito:
        return Response(formatear_respuesta_exito('Código reenviado al email'))
    else:
        return Response(
            formatear_respuesta_error(mensaje), 
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
    
    if not PasswordValidationService.validar_coincidencia(nueva_password, confirmar_password):
        return Response(
            formatear_respuesta_error('Las contraseñas no coinciden'), 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not PasswordValidationService.validar_longitud(nueva_password):
        return Response(
            formatear_respuesta_error('La contraseña debe tener al menos 8 caracteres'), 
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
    
    # Validar que la carrera esté en la lista de disponibles usando utilidad
    nueva_carrera_normalizada = normalizar_carrera(nueva_carrera, CARRERAS_DISPONIBLES)
    
    if not nueva_carrera_normalizada:
        return Response(
            formatear_respuesta_error(
                f'Carrera no disponible. Opciones: {", ".join(CARRERAS_DISPONIBLES)}'
            ), 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Cambiar carrera
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