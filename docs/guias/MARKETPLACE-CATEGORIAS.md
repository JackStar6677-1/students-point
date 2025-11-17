# Marketplace - Categorías

## Problema Resuelto

Se ha solucionado el problema donde no aparecían categorías al crear productos en el marketplace.

## Solución Implementada

Se creó un comando de management para poblar automáticamente **12 categorías iniciales** del marketplace con descripciones e iconos.

### Categorías Creadas

1. **Libros y Apuntes** - Libros de texto, apuntes, guías de estudio
2. **Electrónicos** - Laptops, tablets, smartphones, calculadoras
3. **Ropa y Accesorios** - Ropa, zapatos, mochilas, carteras
4. **Hogar y Decoración** - Artículos para el hogar, decoración, muebles
5. **Deportes y Fitness** - Equipamiento deportivo, ropa deportiva
6. **Instrumentos Musicales** - Guitarras, pianos, instrumentos de viento
7. **Arte y Manualidades** - Materiales de arte, pinturas, pinceles
8. **Videojuegos y Consolas** - Consolas, videojuegos, controles
9. **Bicicletas y Transporte** - Bicicletas, scooters, patinetas
10. **Servicios** - Tutorías, clases particulares, servicios
11. **Material de Oficina** - Cuadernos, lápices, calculadoras
12. **Otros** - Otros productos

## Cómo Usar

### Opción 1: Comando Específico (Recomendado)

```bash
cd proyecto/src/backend
python manage.py poblar_categorias
```

Este comando:
- Crea las 12 categorías si no existen
- Actualiza descripciones e iconos si las categorías ya existen pero no tienen estos datos
- Muestra un resumen de categorías creadas/actualizadas

### Opción 2: Comando General de Población

```bash
cd proyecto/src/backend
python manage.py populate_data
```

Este comando también crea las categorías junto con otros datos de ejemplo.

## Verificación

Después de ejecutar el comando, puedes verificar que las categorías se crearon correctamente:

1. **Desde el Admin de Django:**
   - Ir a `http://127.0.0.1:8000/admin/`
   - Navegar a "Market" → "Categorías de Productos"
   - Deberías ver las 12 categorías listadas

2. **Desde la API:**
   - Hacer una petición GET a `/api/marketplace/categories/`
   - Deberías recibir un array con las categorías

3. **Desde el Frontend:**
   - Ir al marketplace (`/market/`)
   - Al hacer clic en "Publicar producto"
   - El select de categorías debería mostrar las 12 opciones

## Solución de Problemas

### Si no aparecen categorías después de ejecutar el comando:

1. **Verificar que las migraciones estén aplicadas:**
   ```bash
   python manage.py migrate
   ```

2. **Verificar que el comando se ejecutó correctamente:**
   ```bash
   python manage.py poblar_categorias
   ```
   Deberías ver mensajes como "✓ Creada categoría: ..."

3. **Verificar en la base de datos:**
   ```bash
   python manage.py shell
   ```
   ```python
   from studentspoint.apps.market.models import CategoriaProducto
   print(CategoriaProducto.objects.filter(activa=True).count())
   # Debería mostrar 12
   ```

### Si el endpoint no devuelve categorías:

1. Verificar que estás autenticado (el endpoint requiere autenticación)
2. Verificar que las categorías tienen `activa=True`
3. Revisar la consola del navegador para ver errores de red

## Notas Técnicas

- Las categorías se crean con `activa=True` por defecto
- El comando es idempotente: puedes ejecutarlo múltiples veces sin crear duplicados
- Si una categoría ya existe, se actualiza su descripción e icono si no los tiene
- El endpoint `/api/marketplace/categories/` solo devuelve categorías activas

## Archivos Modificados

- `proyecto/src/backend/studentspoint/apps/market/management/commands/poblar_categorias.py` (nuevo)
- `proyecto/src/backend/studentspoint/management/commands/populate_data.py` (actualizado)

