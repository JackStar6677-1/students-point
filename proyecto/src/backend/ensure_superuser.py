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

	if User.objects.filter(email=email).exists():
		print('Superusuario ya existe')
		return

	User.objects.create_superuser(
		email=email,
		password=password,
		name='Administrador StudentsPoint',
		role='admin_global',
		career='Administración'
	)
	print('Superusuario creado: admin@studentspoint.app / admin123')


if __name__ == '__main__':
	main()


