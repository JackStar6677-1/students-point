import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings')
django.setup()

from studentspoint.apps.market.models import Producto

print("=" * 50)
print("VERIFICANDO PRODUCTOS EN BD")
print("=" * 50)

total = Producto.objects.count()
publicados = Producto.objects.filter(estado='publicado').count()

print(f"\n📦 Total productos: {total}")
print(f"✅ Publicados: {publicados}")
print(f"📝 Borradores: {Producto.objects.filter(estado='borrador').count()}")

print("\n" + "=" * 50)
print("PRODUCTOS PUBLICADOS:")
print("=" * 50)

for p in Producto.objects.filter(estado='publicado').order_by('-id')[:10]:
    print(f"\nID: {p.id}")
    print(f"Título: {p.titulo}")
    print(f"Descripción: {p.descripcion[:100] if p.descripcion else 'Sin descripción'}")
    print(f"URL: {p.url_principal}")
    print(f"Estado: {p.estado}")
    print(f"Vendedor: {p.vendedor.email}")
    print("-" * 50)

