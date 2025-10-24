from django.core.management.base import BaseCommand
from django.utils.text import slugify

from studentspoint.apps.campuses.models import Sede
from studentspoint.apps.forum.models import Foro


class Command(BaseCommand):
    help = "Crea foros por defecto por sede y carrera si no existen"

    def handle(self, *args, **options):
        carreras = [
            "Ingeniería en Informática",
            "Ingeniería en Construcción",
            "Ingeniería en Electricidad",
            "Administración",
            "Contabilidad",
            "Técnico en Informática",
        ]

        sedes = list(Sede.objects.all())
        if not sedes:
            sedes = [Sede.objects.create(slug="sede-central", nombre="Sede Central", direccion="-", lat=0, lng=0)]

        created = 0
        for sede in sedes:
            for carrera in carreras:
                slug = f"{sede.slug}-{slugify(carrera)}"
                _, was_created = Foro.objects.get_or_create(
                    sede=sede,
                    carrera=carrera,
                    defaults={"titulo": f"{carrera} - {sede.nombre}", "slug": slug},
                )
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Foros verificados. Nuevos creados: {created}"))


