"""
Script interactivo para probar el sistema de verificación de email.

Este script permite:
1. Ingresar un email
2. Enviar código de verificación
3. Ingresar el código recibido
4. Verificar que la verificación funciona correctamente

Uso:
    python manage.py test_email_verification
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import sys

User = get_user_model()


class Command(BaseCommand):
    help = 'Script interactivo para probar el sistema de verificación de email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email del usuario a probar (opcional, se pedirá si no se proporciona)',
        )
        parser.add_argument(
            '--create-user',
            action='store_true',
            help='Crear usuario si no existe',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('  TEST DE VERIFICACIÓN DE EMAIL'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        # Obtener email
        email = options.get('email')
        if not email:
            email = input('Ingresa el email a probar: ').strip()
        
        if not email:
            self.stdout.write(self.style.ERROR('Email requerido'))
            return

        email = email.lower()

        # Verificar si el usuario existe
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'✓ Usuario encontrado: {user.email}'))
            self.stdout.write(f'  - Nombre: {user.name}')
            self.stdout.write(f'  - Email verificado: {user.is_email_verified}')
            self.stdout.write(f'  - Código actual: {user.email_verification_code or "Ninguno"}\n')
        except User.DoesNotExist:
            if options.get('create_user'):
                self.stdout.write(self.style.WARNING(f'Usuario no existe. Creando usuario...'))
                name = input('Ingresa el nombre del usuario: ').strip() or 'Usuario Test'
                career = input('Ingresa la carrera: ').strip() or 'Ingeniería en Informática'
                password = input('Ingresa la contraseña: ').strip() or 'test123456'
                
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                    career=career,
                    is_email_verified=False
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario creado: {user.email}\n'))
            else:
                self.stdout.write(self.style.ERROR(f'Usuario {email} no existe. Usa --create-user para crearlo.'))
                return

        # Paso 1: Enviar código de verificación
        self.stdout.write(self.style.SUCCESS('\n' + '-'*60))
        self.stdout.write(self.style.SUCCESS('PASO 1: Enviar código de verificación'))
        self.stdout.write(self.style.SUCCESS('-'*60))
        
        input('\nPresiona Enter para enviar el código de verificación...')
        
        try:
            exito, mensaje = user.enviar_codigo_verificacion()
            
            if exito:
                self.stdout.write(self.style.SUCCESS(f'\n✓ {mensaje}'))
                self.stdout.write(f'\n📧 Email enviado a: {user.email}')
                
                # Mostrar código en desarrollo
                if settings.DEBUG:
                    self.stdout.write(self.style.WARNING('\n⚠️  MODO DEBUG: El código se muestra en los logs'))
                    self.stdout.write(self.style.WARNING(f'   Código: {user.email_verification_code}'))
                    self.stdout.write(self.style.WARNING('   (En producción, revisa tu bandeja de correo)\n'))
                
                # Actualizar usuario desde BD
                user.refresh_from_db()
                self.stdout.write(f'   Código generado: {user.email_verification_code}')
                self.stdout.write(f'   Enviado a las: {user.email_verification_sent_at}')
                
                # Calcular expiración
                from datetime import timedelta
                if user.email_verification_sent_at:
                    expiracion = user.email_verification_sent_at + timedelta(minutes=15)
                    self.stdout.write(f'   Expira a las: {expiracion}')
                    tiempo_restante = expiracion - timezone.now()
                    if tiempo_restante.total_seconds() > 0:
                        minutos = int(tiempo_restante.total_seconds() / 60)
                        self.stdout.write(f'   Tiempo restante: ~{minutos} minutos')
                
            else:
                self.stdout.write(self.style.ERROR(f'\n✗ Error: {mensaje}'))
                return
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error enviando código: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            return

        # Paso 2: Verificar código
        self.stdout.write(self.style.SUCCESS('\n' + '-'*60))
        self.stdout.write(self.style.SUCCESS('PASO 2: Verificar código'))
        self.stdout.write(self.style.SUCCESS('-'*60))
        
        # Si estamos en DEBUG y el código está disponible, ofrecerlo
        codigo_ingresado = None
        if settings.DEBUG and user.email_verification_code:
            usar_codigo_debug = input(f'\n¿Usar código de DEBUG ({user.email_verification_code})? (s/n): ').strip().lower()
            if usar_codigo_debug == 's':
                codigo_ingresado = user.email_verification_code
            else:
                codigo_ingresado = input('Ingresa el código de verificación (6 dígitos): ').strip()
        else:
            codigo_ingresado = input('\nIngresa el código de verificación recibido por email (6 dígitos): ').strip()
        
        if not codigo_ingresado or len(codigo_ingresado) != 6:
            self.stdout.write(self.style.ERROR('Código inválido. Debe tener 6 dígitos.'))
            return
        
        # Verificar código
        self.stdout.write('\nVerificando código...')
        
        try:
            user.refresh_from_db()
            exito, mensaje = user.verificar_codigo_email(codigo_ingresado)
            
            if exito:
                user.refresh_from_db()
                self.stdout.write(self.style.SUCCESS(f'\n✓ {mensaje}'))
                self.stdout.write(self.style.SUCCESS(f'✓ Email verificado exitosamente'))
                self.stdout.write(f'\nEstado del usuario:')
                self.stdout.write(f'  - Email verificado: {user.is_email_verified}')
                self.stdout.write(f'  - Código limpiado: {not user.email_verification_code or "Sí"}\n')
                
                # Verificar que puede iniciar sesión
                self.stdout.write(self.style.SUCCESS('\n' + '-'*60))
                self.stdout.write(self.style.SUCCESS('PRUEBA ADICIONAL: Verificar que puede iniciar sesión'))
                self.stdout.write(self.style.SUCCESS('-'*60))
                
                from studentspoint.apps.accounts.services import AuthService
                puede_login, _ = AuthService._puede_iniciar_sesion(user)
                if puede_login:
                    self.stdout.write(self.style.SUCCESS('\n✓ El usuario puede iniciar sesión'))
                else:
                    self.stdout.write(self.style.WARNING('\n⚠️  El usuario aún no puede iniciar sesión'))
                
            else:
                self.stdout.write(self.style.ERROR(f'\n✗ {mensaje}'))
                user.refresh_from_db()
                self.stdout.write(f'\nEstado actual:')
                self.stdout.write(f'  - Email verificado: {user.is_email_verified}')
                self.stdout.write(f'  - Código en BD: {user.email_verification_code or "Ninguno"}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error verificando código: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))

        # Resumen final
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('  RESUMEN'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        user.refresh_from_db()
        self.stdout.write(f'\nEmail: {user.email}')
        self.stdout.write(f'Email verificado: {user.is_email_verified}')
        self.stdout.write(f'Código actual: {user.email_verification_code or "Ninguno (limpiado)"}')
        
        if user.is_email_verified:
            self.stdout.write(self.style.SUCCESS('\n✓ TEST COMPLETADO: Sistema de verificación funcionando correctamente\n'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️  TEST INCOMPLETO: El email no fue verificado\n'))

