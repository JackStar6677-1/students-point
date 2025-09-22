"""Comando para poblar la base de datos con datos de ejemplo."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from studentspoint.apps.campuses.models import Sede, RecorridoVirtual, RecorridoPaso
from studentspoint.apps.forum.models import Foro, Post, Comentario
from studentspoint.apps.market.models import CategoriaProducto, Producto
from studentspoint.apps.portfolio.models import Logro, Proyecto, ExperienciaLaboral, Habilidad
from studentspoint.apps.polls.models import Poll, PollOpcion

User = get_user_model()


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de datos de ejemplo...')
        
        # Crear usuarios
        self.create_users()
        
        # Crear sedes y recorridos
        self.create_campuses()
        
        # Crear foros
        self.create_forums()
        
        # Crear posts y comentarios
        self.create_posts()
        
        # Crear categorías y productos del mercado
        self.create_market_data()
        
        # Crear datos de portafolio
        self.create_portfolio_data()
        
        # Crear encuestas
        self.create_polls()
        
        self.stdout.write(
            self.style.SUCCESS('¡Datos de ejemplo creados exitosamente!')
        )

    def create_users(self):
        """Crear usuarios de ejemplo."""
        self.stdout.write('Creando usuarios...')
        
        # Usuario administrador
        admin_user, created = User.objects.get_or_create(
            email='admin@duocuc.cl',
            defaults={
                'name': 'Administrador StudentsPoint',
                'role': 'admin_global',
                'is_staff': True,
                'is_superuser': True,
                'campus_id': 1,
                'career': 'Administración'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Usuario moderador
        moderator_user, created = User.objects.get_or_create(
            email='moderador@duocuc.cl',
            defaults={
                'name': 'Moderador StudentsPoint',
                'role': 'moderator',
                'campus_id': 1,
                'career': 'Administración'
            }
        )
        if created:
            moderator_user.set_password('moderador123')
            moderator_user.save()
        
        # Usuarios estudiantes
        estudiantes_data = [
            ('juan.perez@duocuc.cl', 'Juan Pérez', 'student', 'Ingeniería en Informática'),
            ('maria.gonzalez@duocuc.cl', 'María González', 'student', 'Administración'),
            ('carlos.rodriguez@duocuc.cl', 'Carlos Rodríguez', 'student', 'Contabilidad'),
            ('ana.martinez@gmail.com', 'Ana Martínez', 'student', 'Psicología'),
            ('luis.silva@gmail.com', 'Luis Silva', 'student', 'Derecho'),
        ]
        
        for email, name, role, career in estudiantes_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'role': role,
                    'campus_id': 1,
                    'career': career,
                    'es_estudiante_gmail': email.endswith('@gmail.com')
                }
            )
            if created:
                user.set_password('estudiante123')
                user.save()

    def create_campuses(self):
        """Crear sedes y recorridos virtuales."""
        self.stdout.write('Creando sedes y recorridos...')
        
        # Crear sede Maipú
        sede, created = Sede.objects.get_or_create(
            nombre='Sede Maipú',
            defaults={
                'direccion': 'Av. Américo Vespucio 1501, Maipú, Santiago',
                'telefono': '+56 2 2345 6789',
                'email': 'maipu@duocuc.cl',
                'latitud': -33.5111,
                'longitud': -70.7525,
                'descripcion': 'Sede principal de Duoc UC en Maipú'
            }
        )
        
        if created:
            # Crear recorrido virtual
            recorrido, created = RecorridoVirtual.objects.get_or_create(
                sede=sede,
                titulo='Recorrido Virtual Sede Maipú',
                defaults={
                    'descripcion': 'Conoce las instalaciones de nuestra sede en Maipú',
                    'duracion_minutos': 15,
                    'activo': True
                }
            )
            
            if created:
                # Crear pasos del recorrido
                pasos_data = [
                    ('Entrada Principal', 'Bienvenidos a Duoc UC Sede Maipú', 0, 0, 0),
                    ('Biblioteca', 'Nuestra biblioteca cuenta con más de 50,000 libros', 0, 0, 0),
                    ('Laboratorio de Computación', 'Espacios equipados con tecnología de punta', 0, 0, 0),
                    ('Cafetería', 'Lugar de encuentro para estudiantes', 0, 0, 0),
                    ('Auditorio', 'Espacio para eventos y presentaciones', 0, 0, 0),
                ]
                
                for i, (titulo, descripcion, heading, pitch, fov) in enumerate(pasos_data):
                    RecorridoPaso.objects.create(
                        recorrido=recorrido,
                        titulo=titulo,
                        descripcion=descripcion,
                        orden=i + 1,
                        streetview_heading=heading,
                        streetview_pitch=pitch,
                        streetview_fov=fov,
                        imagen_360_url=f'/static/images/maipu/paso_{i+1}.jpg',
                        imagen_360_thumbnail=f'/static/images/maipu/thumb_{i+1}.jpg',
                        usar_streetview=False
                    )

    def create_forums(self):
        """Crear foros de ejemplo."""
        self.stdout.write('Creando foros...')
        
        sede = Sede.objects.first()
        if not sede:
            return
        
        foros_data = [
            ('General', 'Discusiones generales sobre la vida estudiantil'),
            ('Académico', 'Preguntas y discusiones académicas'),
            ('Eventos', 'Información sobre eventos y actividades'),
            ('Empleos', 'Oportunidades laborales y prácticas'),
            ('Ventas', 'Compra y venta de artículos estudiantiles'),
        ]
        
        for titulo, descripcion in foros_data:
            Foro.objects.get_or_create(
                sede=sede,
                carrera='Todas',
                titulo=titulo,
                defaults={
                    'slug': titulo.lower().replace(' ', '-')
                }
            )

    def create_posts(self):
        """Crear posts y comentarios de ejemplo."""
        self.stdout.write('Creando posts y comentarios...')
        
        foro = Foro.objects.first()
        usuarios = User.objects.filter(role='student')[:3]
        
        if not foro or not usuarios.exists():
            return
        
        posts_data = [
            ('Bienvenidos al nuevo semestre', '¡Hola a todos! Espero que tengan un excelente semestre. ¿Alguien más está emocionado por las nuevas materias?'),
            ('Recomendaciones de libros', '¿Podrían recomendarme algunos libros para la materia de Programación Avanzada?'),
            ('Evento de networking', 'El próximo viernes habrá un evento de networking con empresas del sector tecnológico. ¡No se lo pierdan!'),
            ('Vendo calculadora científica', 'Vendo mi calculadora Casio FX-991EX en excelente estado. Precio: $25,000'),
            ('Consulta sobre horarios', '¿Alguien sabe si hay cambios en los horarios de la biblioteca este semestre?'),
        ]
        
        for titulo, cuerpo in posts_data:
            usuario = random.choice(usuarios)
            post, created = Post.objects.get_or_create(
                foro=foro,
                usuario=usuario,
                titulo=titulo,
                defaults={
                    'cuerpo': cuerpo,
                    'anonimo': random.choice([True, False]),
                    'estado': 'publicado'
                }
            )
            
            if created:
                # Crear algunos comentarios
                for _ in range(random.randint(1, 3)):
                    comentario_usuario = random.choice(usuarios)
                    Comentario.objects.create(
                        post=post,
                        usuario=comentario_usuario,
                        cuerpo=f'Excelente post, {usuario.name}!',
                        anonimo=random.choice([True, False])
                    )

    def create_market_data(self):
        """Crear datos del mercado."""
        self.stdout.write('Creando datos del mercado...')
        
        # Crear categorías
        categorias_data = [
            'Libros y Apuntes',
            'Electrónicos',
            'Ropa y Accesorios',
            'Hogar y Decoración',
            'Deportes',
            'Otros'
        ]
        
        for nombre in categorias_data:
            CategoriaProducto.objects.get_or_create(nombre=nombre)
        
        # Crear productos
        usuarios = User.objects.filter(role='student')[:3]
        categorias = CategoriaProducto.objects.all()
        
        productos_data = [
            ('Calculadora Casio FX-991EX', 'Calculadora científica en excelente estado', 25000, 'Libros y Apuntes'),
            ('Libro de Programación', 'Libro usado de Java Programming', 15000, 'Libros y Apuntes'),
            ('Laptop Dell Inspiron', 'Laptop usada, funciona perfectamente', 350000, 'Electrónicos'),
            ('Mochila North Face', 'Mochila para laptop, muy resistente', 45000, 'Ropa y Accesorios'),
            ('Mouse Logitech', 'Mouse inalámbrico, como nuevo', 12000, 'Electrónicos'),
        ]
        
        for titulo, descripcion, precio, categoria_nombre in productos_data:
            usuario = random.choice(usuarios)
            categoria = categorias.get(nombre=categoria_nombre)
            
            Producto.objects.get_or_create(
                titulo=titulo,
                vendedor=usuario,
                defaults={
                    'descripcion': descripcion,
                    'precio': precio,
                    'categoria': categoria,
                    'estado': 'disponible',
                    'campus': usuario.campus,
                    'carrera': usuario.career
                }
            )

    def create_portfolio_data(self):
        """Crear datos de portafolio."""
        self.stdout.write('Creando datos de portafolio...')
        
        usuarios = User.objects.filter(role='student')[:3]
        
        for usuario in usuarios:
            # Crear logros
            logros_data = [
                ('Certificación en Java', 'Oracle Certified Java Programmer', '2023'),
                ('Proyecto destacado', 'Mejor proyecto del semestre en Programación', '2023'),
                ('Participación en hackathon', 'Segundo lugar en Hackathon Duoc UC', '2022'),
            ]
            
            for titulo, descripcion, fecha in logros_data:
                Logro.objects.get_or_create(
                    usuario=usuario,
                    titulo=titulo,
                    defaults={
                        'descripcion': descripcion,
                        'fecha_obtencion': fecha,
                        'institucion': 'Duoc UC'
                    }
                )
            
            # Crear proyectos
            proyectos_data = [
                ('Sistema de Gestión Escolar', 'Desarrollo de sistema web para gestión de estudiantes', 'Python, Django, PostgreSQL'),
                ('App Móvil de Tareas', 'Aplicación móvil para gestión de tareas estudiantiles', 'React Native, Firebase'),
                ('Sitio Web Corporativo', 'Diseño y desarrollo de sitio web para empresa local', 'HTML, CSS, JavaScript'),
            ]
            
            for titulo, descripcion, tecnologias in proyectos_data:
                Proyecto.objects.get_or_create(
                    usuario=usuario,
                    titulo=titulo,
                    defaults={
                        'descripcion': descripcion,
                        'tecnologias': tecnologias,
                        'url_repositorio': f'https://github.com/{usuario.name.lower().replace(" ", "")}/{titulo.lower().replace(" ", "-")}',
                        'fecha_inicio': '2023-01-01',
                        'fecha_fin': '2023-06-30'
                    }
                )
            
            # Crear habilidades
            habilidades_data = [
                ('Python', 'Avanzado'),
                ('JavaScript', 'Intermedio'),
                ('Django', 'Intermedio'),
                ('React', 'Básico'),
                ('SQL', 'Intermedio'),
            ]
            
            for nombre, nivel in habilidades_data:
                Habilidad.objects.get_or_create(
                    usuario=usuario,
                    nombre=nombre,
                    defaults={'nivel': nivel}
                )

    def create_polls(self):
        """Crear encuestas de ejemplo."""
        self.stdout.write('Creando encuestas...')
        
        usuarios = User.objects.filter(role__in=['student', 'moderator'])[:2]
        
        if not usuarios.exists():
            return
        
        # Encuesta sobre satisfacción estudiantil
        poll, created = Poll.objects.get_or_create(
            titulo='Satisfacción con los servicios estudiantiles',
            defaults={
                'descripcion': 'Ayúdanos a mejorar nuestros servicios respondiendo esta encuesta',
                'creador': usuarios[0],
                'estado': 'activa',
                'multi': False,
                'anonima': True
            }
        )
        
        if created:
            opciones_data = [
                'Muy satisfecho',
                'Satisfecho',
                'Neutral',
                'Insatisfecho',
                'Muy insatisfecho'
            ]
            
            for i, texto in enumerate(opciones_data):
                PollOpcion.objects.create(
                    poll=poll,
                    texto=texto,
                    orden=i + 1
                )
        
        # Encuesta sobre actividades extracurriculares
        poll2, created = Poll.objects.get_or_create(
            titulo='¿Qué actividades extracurriculares te interesan?',
            defaults={
                'descripcion': 'Selecciona las actividades que más te interesan (puedes elegir varias)',
                'creador': usuarios[0] if len(usuarios) > 0 else usuarios[0],
                'estado': 'activa',
                'multi': True,
                'anonima': False
            }
        )
        
        if created:
            opciones_data = [
                'Deportes',
                'Música',
                'Arte',
                'Voluntariado',
                'Tecnología',
                'Emprendimiento'
            ]
            
            for i, texto in enumerate(opciones_data):
                PollOpcion.objects.create(
                    poll=poll2,
                    texto=texto,
                    orden=i + 1
                )
