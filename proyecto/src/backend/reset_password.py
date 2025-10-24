"""Script para resetear contraseña de usuario."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
django.setup()

from studentspoint.apps.accounts.models import User

email = 'pablo.elias.miranda.292003@gmail.com'
new_password = 'Pablo123456'

try:
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.is_email_verified = True
    user.email_verification_code = ''
    user.save()
    print(f'Contraseña actualizada exitosamente para {email}')
    print(f'Nueva contraseña: {new_password}')
    print(f'Email verificado: {user.is_email_verified}')
except User.DoesNotExist:
    print(f'Usuario {email} no encontrado')

