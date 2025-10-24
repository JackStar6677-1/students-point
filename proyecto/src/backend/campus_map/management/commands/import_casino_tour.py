from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from campus_map.models import Campus, Location, VirtualTour, TourStep


class Command(BaseCommand):
    help = "Importa el tour 'Casino' creando pasos ordenados desde proyecto/imagenes/mapa/casino/*.jpeg"

    def add_arguments(self, parser):
        parser.add_argument('--campus-slug', required=True, help='Slug del campus al que pertenece el tour')
        parser.add_argument('--location-name', default='Casino', help='Nombre de la ubicación destino (se crea/actualiza)')
        parser.add_argument('--dry-run', action='store_true', help='Solo mostrar acciones sin escribir cambios')

    def handle(self, *args, **options):
        campus_slug = options['campus_slug']
        location_name = options['location_name']
        dry_run = options['dry_run']

        # Obtener o crear Campus (mapeando desde Sede si es necesario)
        campus = Campus.objects.filter(slug=campus_slug, is_active=True).first()
        if campus is None:
            try:
                from studentspoint.apps.campuses.models import Sede
            except Exception as exc:
                raise CommandError(
                    f"No se encontró Campus con slug '{campus_slug}' y no se pudo importar Sede: {exc}"
                )

            sede = Sede.objects.filter(slug=campus_slug).first()
            if sede is None:
                # Crear Sede por defecto (Maipú) si no existe
                if campus_slug == 'maipu':
                    sede = Sede(
                        slug='maipu',
                        nombre='Sede Maipú',
                        direccion='Av. Américo Vespucio 1501, Maipú, Santiago',
                        lat=-33.5111,
                        lng=-70.7525,
                    )
                    if not dry_run:
                        sede.save()
                else:
                    raise CommandError(
                        f"No existe Campus ni Sede con slug '{campus_slug}'. Crea la Sede o provee otro slug."
                    )

            campus = Campus(
                name=sede.nombre,
                slug=sede.slug,
                address=sede.direccion,
                latitude=sede.lat,
                longitude=sede.lng,
                is_active=True,
            )
            if not dry_run:
                campus.save()

        # Ruta: proyecto/imagenes/mapa/casino
        images_dir = Path(__file__).resolve().parents[5] / 'imagenes' / 'mapa' / 'casino'
        if not images_dir.exists():
            raise CommandError(f"Directorio de imágenes no encontrado: {images_dir}")

        image_files = sorted(images_dir.glob('*.jpeg')) + sorted(images_dir.glob('*.jpg')) + sorted(images_dir.glob('*.png'))
        if not image_files:
            raise CommandError(f"No se encontraron imágenes en {images_dir}")

        location, _ = Location.objects.get_or_create(
            campus=campus,
            name=location_name,
            defaults={
                'location_type': 'cafeteria',
                'description': 'Casino del campus',
                'latitude': campus.latitude,
                'longitude': campus.longitude,
            }
        )
        if location.name != location_name:
            location.name = location_name
            if not dry_run:
                location.save()

        tour, created_tour = VirtualTour.objects.get_or_create(
            campus=campus,
            title='Recorrido al Casino',
            defaults={'description': 'Recorrido guiado hacia el casino'}
        )

        if created_tour:
            self.stdout.write(self.style.SUCCESS(f"Creado tour: {tour.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Usando tour existente: {tour.title}"))

        if not dry_run:
            TourStep.objects.filter(tour=tour).delete()

        for idx, img_path in enumerate(image_files, start=1):
            title = f"Paso {idx}"
            description = f"Imagen {img_path.name} para el recorrido al casino"
            if dry_run:
                self.stdout.write(f"[DRY RUN] Añadir paso {idx}: {img_path.name}")
                continue

            step = TourStep(
                tour=tour,
                location=location,
                order=idx,
                title=title,
                description=description,
            )
            with img_path.open('rb') as f:
                step.image.save(img_path.name, File(f), save=False)
            step.save()

        self.stdout.write(self.style.SUCCESS("Importación de recorrido 'Casino' completada"))


