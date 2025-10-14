"""
Comando para crear usuarios de demostración.
"""
from django.core.management.base import BaseCommand
from studentspoint.apps.accounts.models import User


class Command(BaseCommand):
    help = 'Crea usuarios de demostración para testing'

    def handle(self, *args, **options):
        demo_users = [
            {
                'email': 'estudiante@studentspoint.app',
                'password': 'estudiante123',
                'name': 'Estudiante Demo',
                'role': 'estudiante',
                'career': 'Ingeniería en Informática',
                'is_email_verified': True,
            },
            {
                'email': 'profesor@studentspoint.app',
                'password': 'profesor123',
                'name': 'Profesor Demo',
                'role': 'profesor',
                'career': 'Docencia',
                'is_email_verified': True,
            },
            {
                'email': 'moderador@studentspoint.app',
                'password': 'moderador123',
                'name': 'Moderador Demo',
                'role': 'moderador',
                'career': 'Administración',
                'is_email_verified': True,
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for user_data in demo_users:
            email = user_data.pop('email')
            password = user_data.pop('password')
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults=user_data
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {email}'))
                created_count += 1
            else:
                # Actualizar contraseña y verificación
                user.set_password(password)
                user.is_email_verified = True
                user.email_verification_code = ''
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.save()
                self.stdout.write(self.style.WARNING(f'Usuario actualizado: {email}'))
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nResumen:'))
        self.stdout.write(self.style.SUCCESS(f'- Usuarios creados: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'- Usuarios actualizados: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'\nCredenciales:'))
        self.stdout.write(self.style.SUCCESS(f'- estudiante@studentspoint.app / estudiante123'))
        self.stdout.write(self.style.SUCCESS(f'- profesor@studentspoint.app / profesor123'))
        self.stdout.write(self.style.SUCCESS(f'- moderador@studentspoint.app / moderador123'))
        self.stdout.write(self.style.SUCCESS(f'- admin@studentspoint.app / admin123'))

