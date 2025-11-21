"""
Crea datos de demostración para foros, posts, encuestas, comentarios y votos.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from studentspoint.apps.campuses.models import Sede
from studentspoint.apps.forum.models import Foro, Post, Comentario, OpcionEncuesta, VotoEncuesta
from studentspoint.apps.accounts.models import CARRERAS_DISPONIBLES


class Command(BaseCommand):
    help = "Crea datos de demostración para el módulo de foros"

    def handle(self, *args, **options):
        with transaction.atomic():
            sede_defaults = {"slug": "sede-maipu", "lat": -33.513, "lng": -70.761}
            sede, _ = Sede.objects.get_or_create(nombre="Sede Maipú", defaults=sede_defaults)

            # Usar solo las primeras 3 carreras para demo
            carreras = CARRERAS_DISPONIBLES[:3]
            foros = []
            for carrera in carreras:
                foro, _ = Foro.objects.get_or_create(
                    sede=sede,
                    carrera=carrera,
                    defaults={"titulo": f"Foro {carrera}", "slug": f"foro-{carrera.lower().replace(' ', '-')}", "es_privado": False},
                )
                foros.append(foro)

            User = get_user_model()
            admin, _ = User.objects.get_or_create(
                email="admin@studentspoint.app",
                defaults={
                    "name": "Admin",
                    "career": "Ingeniería en Informática",
                    "role": "admin_global",
                    "is_email_verified": True,
                },
            )
            admin.set_password("admin123")
            admin.save()

            # Posts de muestra: texto e imagen
            texto_post, _ = Post.objects.get_or_create(
                foro=foros[0], usuario=admin, titulo="Bienvenida",
                defaults={"tipo": Post.TipoPost.COMENTARIO, "cuerpo": "Bienvenidos al foro de Informática"},
            )

            # Encuesta con opciones
            encuesta, _ = Post.objects.get_or_create(
                foro=foros[0], usuario=admin, titulo="¿Qué editor usas?",
                defaults={"tipo": Post.TipoPost.ENCUESTA, "cuerpo": "Elige tu editor favorito"},
            )
            if encuesta.opciones_encuesta.count() == 0:
                OpcionEncuesta.objects.create(post=encuesta, texto="VS Code", orden=0)
                OpcionEncuesta.objects.create(post=encuesta, texto="PyCharm", orden=1)
                OpcionEncuesta.objects.create(post=encuesta, texto="Vim", orden=2)

            # Comentarios de ejemplo
            Comentario.objects.get_or_create(post=texto_post, usuario=admin, cuerpo="Mensaje de prueba")

            # Un voto de ejemplo en encuesta (admin en VS Code)
            opcion_vscode = encuesta.opciones_encuesta.order_by("orden").first()
            if opcion_vscode:
                VotoEncuesta.objects.update_or_create(opcion=opcion_vscode, usuario=admin)
                # Recalcular conteos
                for opt in encuesta.opciones_encuesta.all():
                    opt.votos = opt.votos_usuarios.count()
                    opt.save(update_fields=["votos"])

        self.stdout.write(self.style.SUCCESS("Datos de demo creados/actualizados correctamente."))


