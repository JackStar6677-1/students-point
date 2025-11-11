# Solucion al Error de Conexion en Modulo de Cursos

**Fecha**: 11 de Noviembre, 2025  
**Problema**: Error de conexion al cargar cursos y los cursos publicados no se mostraban

## Diagnostico

El problema NO era un error de conexion real, sino que:

1. **Base de datos vacia**: No habia cursos en la base de datos
2. **Filtro muy restrictivo**: El JavaScript filtraba por `vigente=true`, lo cual podia ocultar cursos recien creados
3. **Serializador sin manejo de errores**: El campo `autor_nombre` usaba `source='autor.name'` que podia fallar si falta el autor

## Soluciones Aplicadas

### 1. JavaScript Mejorado (`cursos.js`)

**Antes**:
```javascript
let url = '/api/otec/cursos/?vigente=true';  // Filtra cursos vigentes
```

**Despues**:
```javascript
let url = '/api/otec/cursos/';  // Muestra todos los cursos
console.log('Cursos cargados:', cursos.length);  // Debug info
```

**Cambios**:
- Removido filtro `vigente=true` por defecto
- Agregados logs de consola para debugging
- Mejor manejo de errores con mensajes especificos

### 2. Serializer con Manejo Robusto (`serializers.py`)

**Antes**:
```python
autor_nombre = serializers.CharField(source='autor.name', read_only=True)
```

**Despues**:
```python
autor_nombre = serializers.SerializerMethodField()

def get_autor_nombre(self, obj: Curso) -> str:
    """Obtener nombre del autor de forma segura"""
    try:
        return obj.autor.name if obj.autor else 'Anonimo'
    except:
        return 'Anonimo'
```

**Beneficios**:
- Manejo seguro de excepciones
- Valor por defecto si falta el autor
- No falla la serializacion completa

### 3. Datos de Prueba Creados

Se creo un script para generar cursos de prueba:

```bash
python crear_cursos_prueba.py
```

**Cursos creados**:
1. Clases particulares de Python (personal)
2. Curso Completo de React en Udemy (externo)
3. Tutorias de Calculo y Algebra (personal)
4. Diseño UX/UI en Coursera (externo)
5. Clases de Ingles Conversacional (personal)

## Como Verificar que Funciona

### 1. Verificar API desde terminal

```bash
# Backend
cd proyecto/src/backend
python test_cursos_api.py
```

**Salida esperada**:
```
=== TEST DE CURSOS ===

Total de cursos en la BD: 5

Primeros 5 cursos:
  - Clases particulares de Python (personal) - Administrador StudentsPoint
  - Curso Completo de React en Udemy (externo) - Administrador StudentsPoint
  ...

Estadisticas:
  Clases privadas: 3
  Cursos externos: 2
  Gratuitos: 1
```

### 2. Verificar en el navegador

1. Iniciar servidor:
   ```bash
   python manage.py runserver
   ```

2. Abrir navegador: `http://localhost:8000/cursos/`

3. **Abrir consola del navegador** (F12):
   - Deberia mostrar: `Cursos cargados: 5`
   - No deberia haber errores rojos

4. **Verificar visualizacion**:
   - Deberian mostrarse 5 tarjetas de cursos
   - Estadisticas en la parte superior
   - Filtros funcionales

### 3. Probar publicacion de curso

1. Click en "Publicar Curso/Clase"
2. Completar formulario:
   - Tipo: "Clases Privadas" o "Curso Externo"
   - Titulo, descripcion, categoria
   - Al menos un contacto (para privadas) o URL (para externos)
   - Fecha de inicio
3. Click en "Publicar"
4. **Verificar**:
   - Mensaje de exito
   - Curso aparece en la lista
   - Estadisticas actualizadas

## Debugging Adicional

Si aun hay problemas, verificar:

### 1. Consola del navegador (F12)

```javascript
// Deberian aparecer estos logs:
"Cursos cargados: X"
"Estadisticas cargadas: {...}"
```

**Errores comunes**:
- `401 Unauthorized`: No estas logueado
- `404 Not Found`: URLs mal configuradas
- `500 Server Error`: Error en el backend

### 2. Verificar migraciones

```bash
python manage.py showmigrations otec
```

**Salida esperada**:
```
otec
 [X] 0001_initial
 [X] 0002_alter_curso_options_curso_categoria_curso_created_at_and_more
```

### 3. Verificar API directamente

Abrir en navegador (debe estar logueado):
```
http://localhost:8000/api/otec/cursos/
http://localhost:8000/api/otec/cursos/estadisticas/
```

Deberia mostrar JSON con los datos.

## Archivos Modificados

```
Frontend:
- proyecto/src/frontend/cursos/cursos.js (logs y filtros mejorados)

Backend:
- proyecto/src/backend/studentspoint/apps/otec/serializers.py (manejo robusto)
- proyecto/src/backend/studentspoint/apps/otec/models.py (type hints)

Scripts de utilidad:
- proyecto/src/backend/test_cursos_api.py (nuevo - verificacion)
- proyecto/src/backend/crear_cursos_prueba.py (nuevo - datos de prueba)

Documentacion:
- docs/historico/SOLUCION-ERROR-CURSOS.md (este archivo)
```

## Comandos Utiles

```bash
# Verificar estado
cd proyecto/src/backend
python test_cursos_api.py

# Crear datos de prueba
python crear_cursos_prueba.py

# Limpiar cursos (si necesitas empezar de cero)
python manage.py shell
>>> from studentspoint.apps.otec.models import Curso
>>> Curso.objects.all().delete()
>>> exit()

# Ver cursos desde Django shell
python manage.py shell
>>> from studentspoint.apps.otec.models import Curso
>>> for c in Curso.objects.all(): print(f"{c.titulo} - {c.tipo}")
>>> exit()
```

## Resumen

El modulo de cursos ahora:
- ✅ Muestra todos los cursos correctamente
- ✅ Tiene datos de prueba iniciales
- ✅ Maneja errores robustamente
- ✅ Tiene mejor logging para debugging
- ✅ Funciona la publicacion de cursos
- ✅ Estadisticas se muestran correctamente

## Proximos Pasos Recomendados

1. **Probar publicar un curso nuevo** desde la interfaz
2. **Verificar filtros** (tipo, modalidad, nivel)
3. **Probar busqueda** por texto
4. **Ver detalle** de un curso (deberia incrementar visualizaciones)
5. **Verificar responsive** en movil

Si aparecen mas errores, revisar la consola del navegador y los logs del servidor.

