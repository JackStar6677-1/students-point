"""
Sistema de OAuth de Google para StudentsPoint
"""
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import requests

User = get_user_model()

# Configuración de OAuth de Google
GOOGLE_CLIENT_ID = getattr(settings, 'GOOGLE_CLIENT_ID', '307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = getattr(settings, 'GOOGLE_CLIENT_SECRET', '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')
GOOGLE_REDIRECT_URI = getattr(settings, 'GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback/web/')

# Scopes de Google
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]


class GoogleOAuthService:
    """Servicio para manejar OAuth de Google"""
    
    def __init__(self):
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = GOOGLE_REDIRECT_URI
        self.scopes = SCOPES
    
    def get_authorization_url(self):
        """
        Obtener URL de autorización de Google
        
        Returns:
            str: URL para redirigir al usuario a Google
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state
    
    def exchange_code_for_token(self, code):
        """
        Intercambiar código de autorización por token de acceso
        
        Args:
            code: Código de autorización de Google
            
        Returns:
            dict: Información del token y usuario
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        # Intercambiar código por token
        flow.fetch_token(code=code)
        
        # Obtener información del usuario
        credentials = flow.credentials
        user_info = self._get_user_info(credentials)
        
        return {
            'credentials': credentials,
            'user_info': user_info
        }
    
    def _get_user_info(self, credentials):
        """
        Obtener información del usuario desde Google
        
        Args:
            credentials: Credenciales de Google
            
        Returns:
            dict: Información del usuario
        """
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info
        except Exception as e:
            # Fallback usando requests
            return self._get_user_info_fallback(credentials.token)
    
    def _get_user_info_fallback(self, access_token):
        """
        Fallback para obtener información del usuario
        
        Args:
            access_token: Token de acceso de Google
            
        Returns:
            dict: Información del usuario
        """
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error obteniendo información del usuario: {str(e)}")
    
    def create_or_update_user(self, user_info):
        """
        Crear o actualizar usuario basado en información de Google
        
        Args:
            user_info: Información del usuario de Google
            
        Returns:
            User: Usuario creado o actualizado
        """
        email = user_info.get('email')
        if not email:
            raise ValidationError("No se pudo obtener el email del usuario")
        
        # Verificar si el usuario ya existe
        try:
            user = User.objects.get(email=email)
            # Actualizar información del usuario
            user.name = user_info.get('name', user.name)
            user.picture = user_info.get('picture', '')
            user.google_id = user_info.get('id', '')
            user.save()
            return user
        except User.DoesNotExist:
            # Crear nuevo usuario
            user = User.objects.create_user(
                email=email,
                name=user_info.get('name', ''),
                role='estudiante',
                career='Estudiante',
                picture=user_info.get('picture', ''),
                google_id=user_info.get('id', ''),
                is_verified=True  # Los usuarios de Google están verificados
            )
            return user


def get_google_oauth_service():
    """Obtener instancia del servicio de OAuth de Google"""
    return GoogleOAuthService()


# Funciones de utilidad
def validate_google_email(email):
    """
    Validar email de Google (cualquier email válido)
    
    Args:
        email: Email a validar
        
    Returns:
        bool: True si es válido
    """
    if not email or '@' not in email:
        return False
    
    # Permitir cualquier email válido para OAuth de Google
    return True


def get_google_login_url():
    """
    Obtener URL de login de Google
    
    Returns:
        str: URL de autorización
    """
    service = get_google_oauth_service()
    url, state = service.get_authorization_url()
    return url, state


def handle_google_callback(code):
    """
    Manejar callback de Google OAuth
    
    Args:
        code: Código de autorización
        
    Returns:
        dict: Información del usuario y token
    """
    service = get_google_oauth_service()
    result = service.exchange_code_for_token(code)
    user = service.create_or_update_user(result['user_info'])
    
    return {
        'user': user,
        'credentials': result['credentials'],
        'user_info': result['user_info']
    }
