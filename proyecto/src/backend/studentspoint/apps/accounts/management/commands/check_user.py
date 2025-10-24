"""
Comando para verificar el estado de un usuario.
"""
from django.core.management.base import BaseCommand
from studentspoint.apps.accounts.models import User


class Command(BaseCommand):
    help = 'Verifica el estado de un usuario por email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario a verificar')

    def handle(self, *args, **options):
        email = options['email'].lower()
        
        try:
            user = User.objects.get(email=email)
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('INFORMACION DEL USUARIO'))
            self.stdout.write(self.style.SUCCESS('='*60))
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Nombre: {user.name}')
            self.stdout.write(f'Rol: {user.role}')
            self.stdout.write(f'Carrera: {user.career}')
            self.stdout.write(f'Campus: {user.campus.nombre if user.campus else "Sin campus"}')
            self.stdout.write(f'Email verificado: {user.is_email_verified}')
            self.stdout.write(f'Codigo verificacion: {user.email_verification_code or "(vacio)"}')
            self.stdout.write(f'Fecha envio codigo: {user.email_verification_sent_at or "(ninguna)"}')
            self.stdout.write(f'Activo: {user.is_active}')
            self.stdout.write(f'Staff: {user.is_staff}')
            self.stdout.write(f'Superuser: {user.is_superuser}')
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
            
            # Verificar si puede iniciar sesión
            if not user.is_email_verified:
                email_l = user.email.lower()
                dominios_laxos = ('@duocuc.cl', '@studentspoint.app')
                if not any(email_l.endswith(d) for d in dominios_laxos):
                    self.stdout.write(self.style.WARNING('ATENCION: Email no verificado. Usuario NO puede iniciar sesion.'))
                else:
                    self.stdout.write(self.style.SUCCESS('Email no verificado pero dominio permitido. Usuario PUEDE iniciar sesion.'))
            else:
                self.stdout.write(self.style.SUCCESS('Email verificado. Usuario PUEDE iniciar sesion.'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario con email {email} no encontrado'))

