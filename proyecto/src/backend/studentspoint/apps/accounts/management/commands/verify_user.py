"""
Comando para verificar manualmente el email de un usuario.
"""
from django.core.management.base import BaseCommand
from studentspoint.apps.accounts.models import User


class Command(BaseCommand):
    help = 'Verifica manualmente el email de un usuario'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario a verificar')

    def handle(self, *args, **options):
        email = options['email'].lower()
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_email_verified:
                self.stdout.write(self.style.WARNING(f'El usuario {email} ya tiene el email verificado'))
            else:
                user.is_email_verified = True
                user.email_verification_code = ''
                user.save(update_fields=['is_email_verified', 'email_verification_code'])
                self.stdout.write(self.style.SUCCESS(f'Email de {email} verificado exitosamente'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario con email {email} no encontrado'))

