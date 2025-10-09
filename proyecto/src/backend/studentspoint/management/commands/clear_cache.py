from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Limpia el cache de Django'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cache limpiado exitosamente'))
