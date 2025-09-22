"""
Vistas para OAuth de Google
"""
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import json
import logging

from .oauth import get_google_oauth_service, handle_google_callback
from .models import User

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Iniciar proceso de login con Google OAuth
    
    Returns:
        Response: URL de autorización de Google
    """
    try:
        service = get_google_oauth_service()
        auth_url, state = service.get_authorization_url()
        
        # Guardar state en sesión para validación posterior
        request.session['oauth_state'] = state
        
        return Response({
            'auth_url': auth_url,
            'state': state
        })
    except Exception as e:
        logger.error(f"Error iniciando OAuth de Google: {str(e)}")
        return Response({
            'error': 'Error iniciando autenticación con Google'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_callback(request):
    """
    Manejar callback de Google OAuth
    
    Body:
        code: Código de autorización de Google
        
    Returns:
        Response: Tokens JWT y información del usuario
    """
    try:
        code = request.data.get('code')
        if not code:
            return Response({
                'error': 'Código de autorización requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Manejar callback de Google
        result = handle_google_callback(code)
        user = result['user']
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'career': user.career,
                'picture': user.picture,
                'is_verified': user.is_verified,
                'google_id': user.google_id
            },
            'message': 'Autenticación exitosa con Google'
        })
        
    except Exception as e:
        logger.error(f"Error en callback de Google OAuth: {str(e)}")
        return Response({
            'error': f'Error en autenticación: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def google_login_redirect(request):
    """
    Vista para redirección directa a Google (para uso en frontend)
    
    Returns:
        HttpResponseRedirect: Redirección a Google
    """
    try:
        service = get_google_oauth_service()
        auth_url, state = service.get_authorization_url()
        
        # Guardar state en sesión
        request.session['oauth_state'] = state
        
        return HttpResponseRedirect(auth_url)
        
    except Exception as e:
        logger.error(f"Error en redirección a Google: {str(e)}")
        return JsonResponse({
            'error': 'Error iniciando autenticación con Google'
        }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_callback_web(request):
    """
    Callback para autenticación web (redirección desde Google)
    
    Query params:
        code: Código de autorización
        state: Estado de OAuth
        
    Returns:
        Response: Redirección a frontend con tokens
    """
    try:
        code = request.GET.get('code')
        state = request.GET.get('state')
        
        if not code:
            return JsonResponse({
                'error': 'Código de autorización no encontrado'
            }, status=400)
        
        # Validar state si está disponible
        if state and 'oauth_state' in request.session:
            if state != request.session['oauth_state']:
                return JsonResponse({
                    'error': 'Estado de OAuth inválido'
                }, status=400)
        
        # Manejar callback
        result = handle_google_callback(code)
        user = result['user']
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Limpiar state de sesión
        if 'oauth_state' in request.session:
            del request.session['oauth_state']
        
        # Redirigir al frontend con tokens
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:8000')
        redirect_url = f"{frontend_url}/login.html?access_token={access_token}&refresh_token={refresh_token}&google_auth=true"
        
        return HttpResponseRedirect(redirect_url)
        
    except Exception as e:
        logger.error(f"Error en callback web de Google: {str(e)}")
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:8000')
        error_url = f"{frontend_url}/login.html?error=google_auth_failed"
        return HttpResponseRedirect(error_url)


@api_view(['GET'])
@permission_classes([AllowAny])
def google_user_info(request):
    """
    Obtener información del usuario desde Google (para usuarios autenticados)
    
    Returns:
        Response: Información del usuario de Google
    """
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({
                'error': 'Usuario no autenticado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.google_id:
            return Response({
                'error': 'Usuario no vinculado con Google'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'google_id': user.google_id,
            'email': user.email,
            'name': user.name,
            'picture': user.picture,
            'is_verified': user.is_verified
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo información de Google: {str(e)}")
        return Response({
            'error': 'Error obteniendo información del usuario'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def disconnect_google(request):
    """
    Desconectar cuenta de Google del usuario
    
    Returns:
        Response: Confirmación de desconexión
    """
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({
                'error': 'Usuario no autenticado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Limpiar campos de Google
        user.google_id = ''
        user.picture = ''
        user.save()
        
        return Response({
            'message': 'Cuenta de Google desconectada exitosamente'
        })
        
    except Exception as e:
        logger.error(f"Error desconectando Google: {str(e)}")
        return Response({
            'error': 'Error desconectando cuenta de Google'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

