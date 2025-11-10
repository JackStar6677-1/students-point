# Correcciones al Modulo de Conversor de Documentos

**Fecha**: 10 de Noviembre, 2025  
**Problemas Reportados**:
- El dialogo de seleccion de archivos se abria 2 veces
- El modulo no funcionaba correctamente
- Timeouts muy largos que causaban fallos

## Problemas Identificados y Soluciones

### 1. Doble Dialogo de Seleccion de Archivos

**Problema**: En el HTML, habia un boton "Seleccionar Archivo" dentro de la zona de drag & drop. Cuando el usuario hacia click en el boton, se disparaban DOS eventos:
- El evento click del boton (`onclick`)
- El evento click del contenedor drag & drop

**Solucion**: Se eliminaron los botones redundantes del HTML. Ahora la zona de drag & drop maneja todo el comportamiento de seleccion de archivos.

**Archivos modificados**:
- `proyecto/src/frontend/converter/conversor.html` (lineas 147-156 y 174-186)

### 2. Conversion Sincrona Bloqueante

**Problema**: El backend ejecutaba la conversion de forma sincrona en la vista, bloqueando la peticion HTTP durante todo el proceso de conversion. Esto causaba:
- Timeouts en archivos grandes
- La aplicacion parecia congelada
- Mala experiencia de usuario

**Solucion**: Implementado procesamiento asincrono usando threading:
- La vista ahora devuelve inmediatamente despues de crear el job
- La conversion se ejecuta en un thread separado en background
- El frontend hace polling para verificar el estado

**Archivos modificados**:
- `proyecto/src/backend/studentspoint/apps/document_converter/views.py`

```python
# Antes:
convert_document(job)

# Despues:
conversion_thread = threading.Thread(
    target=convert_document,
    args=(job,),
    daemon=True
)
conversion_thread.start()
```

### 3. Timeouts Excesivos

**Problema**: Los timeouts eran demasiado largos:
- 5 minutos (300,000 ms) para la subida del archivo
- 60 intentos de polling (60 segundos) con timeout de 5 segundos cada uno

**Solucion**: Ajustados a valores mas razonables:
- **Timeout de subida**: 60 segundos (suficiente para archivos de hasta 50MB)
- **Polling**: 30 intentos de 1 segundo con timeout de 10 segundos por request
- Mejor retroalimentacion visual del progreso

**Archivos modificados**:
- `proyecto/src/frontend/converter/converter.js`

## Cambios Detallados

### Frontend (converter.js)

1. **Timeout de subida reducido**: De 300s a 60s
2. **Polling optimizado**: De 60 intentos a 30 intentos
3. **Timeout por request**: De 5s a 10s
4. **Mejor manejo de errores**: Mensajes mas claros y especificos
5. **Retroalimentacion mejorada**: Indicador de progreso mas preciso

### Backend (views.py)

1. **Threading implementado**: Conversion no bloqueante
2. **Respuesta inmediata**: El endpoint devuelve el job creado sin esperar
3. **Procesamiento en background**: La conversion se ejecuta en paralelo

### HTML (conversor.html)

1. **Botones redundantes eliminados**: Solo la zona drag & drop es clickeable
2. **Interfaz mas limpia**: Menos elementos confusos para el usuario

## Como Probar

### 1. Preparar el Entorno

```bash
# Desde la raiz del proyecto
cd proyecto/src/backend

# Activar entorno virtual (si aplica)
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows

# Asegurar que las dependencias estan instaladas
pip install python-docx reportlab PyPDF2
```

### 2. Iniciar el Servidor

```bash
# Desde proyecto/src/backend
python manage.py runserver
```

### 3. Probar la Conversion

1. **Abrir el navegador**: http://localhost:8000/converter/
2. **Iniciar sesion** con una cuenta de usuario
3. **Probar Word a PDF**:
   - Hacer click en la zona de "Arrastra tu archivo Word aqui" (solo deberia abrir el dialogo UNA vez)
   - O arrastrar un archivo .docx directamente
   - Hacer click en "Convertir a PDF"
   - Verificar que el progreso se actualiza correctamente
   - Descargar el PDF generado

4. **Probar PDF a Word**:
   - Cambiar a la pestaña "PDF a Word"
   - Seleccionar un archivo PDF
   - (Opcional) Activar OCR si el PDF tiene imagenes con texto
   - Hacer click en "Convertir a Word"
   - Descargar el archivo Word generado

5. **Verificar el Historial**:
   - Ir a la pestaña "Historial"
   - Verificar que las conversiones aparecen listadas
   - Probar descargar archivos desde el historial

### 4. Verificar que NO Hay Problemas

- ✓ El dialogo de archivos se abre solo UNA vez
- ✓ La conversion completa en menos de 60 segundos para archivos normales
- ✓ No hay timeouts ni errores de conexion
- ✓ El indicador de progreso se actualiza correctamente
- ✓ Los archivos se descargan correctamente

## Mejoras Adicionales Implementadas

1. **Mejor manejo de errores**: Mensajes especificos para cada tipo de error
2. **Validacion de archivos**: Validacion de extension y tamaño antes de subir
3. **Retroalimentacion visual**: Indicador de progreso mas informativo
4. **Optimizacion de recursos**: Threads daemon que se limpian automaticamente

## Consideraciones para Produccion

Para un entorno de produccion con alto trafico, se recomienda:

1. **Usar Celery** en lugar de threading para manejar conversiones
2. **Implementar Redis** para caching y cola de tareas
3. **Aumentar timeouts** si se esperan archivos muy grandes (>50MB)
4. **Implementar limites de rate** para prevenir abuso
5. **Monitorear threads activos** para prevenir memory leaks

## Correcciones Adicionales

### 4. URLs de Archivos Media No Configuradas

**Problema**: Las URLs para servir archivos media (archivos subidos por usuarios) no estaban configuradas. El catch-all `spa_serve` capturaba las URLs `/media/*` y devolvia `index.html` en lugar del archivo convertido.

**Solucion**: Agregada configuracion de URLs media ANTES del catch-all en `urls.py`:

```python
# Servir archivos media (archivos subidos por usuarios)
re_path(r'^media/(?P<path>.*)$', serve, {'document_root': Path(settings.MEDIA_ROOT)})
```

**Archivos modificados**:
- `proyecto/src/backend/studentspoint/urls.py`

### 5. Respuesta del Backend sin ID

**Problema**: El metodo `perform_create` no controlaba la respuesta HTTP completa, causando que el frontend recibiera datos incompletos sin el campo `id`.

**Solucion**: Sobrescrito el metodo `create` completo para devolver la respuesta con `ConversionJobSerializer` que incluye todos los campos necesarios.

**Archivos modificados**:
- `proyecto/src/backend/studentspoint/apps/document_converter/views.py`

## Archivos Modificados

```
proyecto/src/frontend/converter/conversor.html
proyecto/src/frontend/converter/converter.js
proyecto/src/backend/studentspoint/apps/document_converter/views.py
proyecto/src/backend/studentspoint/urls.py
docs/historico/CORRECCION-CONVERSOR-DOCUMENTOS.md (nuevo)
```

## Resultado Final

El modulo de conversion ahora:
- ✓ Funciona correctamente sin doble dialogo
- ✓ Responde rapidamente sin timeouts
- ✓ Procesa conversiones en background
- ✓ Proporciona retroalimentacion clara al usuario
- ✓ Maneja errores apropiadamente

## Notas Adicionales

- El modulo soporta archivos de hasta 50MB
- La conversion Word a PDF preserva el formato basico del documento
- La conversion PDF a Word extrae el texto pero puede perder formato complejo
- El OCR esta disponible para PDFs que son imagenes escaneadas

