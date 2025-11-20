#!/usr/bin/env python3
"""
Crear superusuario por defecto si no existe.
"""

import os
import django


def main() -> None:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')
	django.setup()

	from django.contrib.auth import get_user_model

	User = get_user_model()
	email = 'admin@studentspoint.app'
	password = 'admin123'

	user, created = User.objects.get_or_create(
		email=email,
		defaults={
			'name': 'Administrador StudentsPoint',
			'role': 'admin_global',
			'career': 'Administración',
			'is_staff': True,
			'is_superuser': True,
			'is_email_verified': True
		}
	)
	
	# Asegurar que tenga todos los permisos (actualizar si ya existía)
	user.is_staff = True
	user.is_superuser = True
	user.is_email_verified = True
	user.role = 'admin_global'
	user.set_password(password)  # Actualizar contraseña
	user.save()
	
	if created:
		print('Superusuario creado: admin@studentspoint.app / admin123')
	else:
		print('Superusuario actualizado: admin@studentspoint.app / admin123')
	
	print(f'  - Email: {user.email}')
	print(f'  - is_staff: {user.is_staff}')
	print(f'  - is_superuser: {user.is_superuser}')
	print(f'  - role: {user.role}')
	print(f'  - is_email_verified: {user.is_email_verified}')


if __name__ == '__main__':
	main()


