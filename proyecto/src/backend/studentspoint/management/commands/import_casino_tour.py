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

        try:
            campus = Campus.objects.get(slug=campus_slug, is_active=True)
        except Campus.DoesNotExist:
            raise CommandError(f"Campus con slug '{campus_slug}' no encontrado o inactivo")

        images_dir = Path(__file__).resolve().parents[4] / 'imagenes' / 'mapa' / 'casino'
        if not images_dir.exists():
            raise CommandError(f"Directorio de imágenes no encontrado: {images_dir}")

        image_files = sorted(images_dir.glob('*.jpeg')) + sorted(images_dir.glob('*.jpg')) + sorted(images_dir.glob('*.png'))
        if not image_files:
            raise CommandError(f"No se encontraron imágenes en {images_dir}")

        # Asegurar Location de tipo cafeteria (renombrado a Casino)
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
        # Si existía como 'Cafetería' y queremos usar 'Casino', actualizar nombre
        if location.name != location_name:
            location.name = location_name
            if not dry_run:
                location.save()

        # Crear/obtener VirtualTour
        tour, created_tour = VirtualTour.objects.get_or_create(
            campus=campus,
            title='Recorrido al Casino',
            defaults={'description': 'Recorrido guiado hacia el casino'}
        )

        if created_tour:
            self.stdout.write(self.style.SUCCESS(f"Creado tour: {tour.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Usando tour existente: {tour.title}"))

        # Limpiar pasos previos
        if not dry_run:
            TourStep.objects.filter(tour=tour).delete()

        # Crear pasos a partir de imágenes enumeradas
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


