# Instrucciones de Uso - Conversor de Documentos

## Acceso

**URL:** http://127.0.0.1:8000/converter/

**Desde el menu:** Navbar > Conversor

**Requisito:** Sesion iniciada (login requerido)

---

## Funcionalidades

### 1. Convertir Word a PDF

**Paso a paso:**

1. Accede a la pestana "Word a PDF"
2. Arrastra tu archivo .doc o .docx a la zona de carga
   - O haz click en "Seleccionar Archivo"
3. El archivo aparecera con su nombre y tamano
4. Click en "Convertir a PDF"
5. Espera a que la barra de progreso complete
6. Click en "Descargar Archivo" para obtener tu PDF

**Formatos soportados:**
- .doc (Word 97-2003)
- .docx (Word 2007+)

**Caracteristicas:**
- Preserva formato y estilos
- Mantiene imagenes
- Genera tabla de contenidos
- Profesional y limpio

---

### 2. Convertir PDF a Word

**Paso a paso:**

1. Accede a la pestana "PDF a Word"
2. Arrastra tu archivo .pdf a la zona de carga
   - O haz click en "Seleccionar Archivo"
3. El archivo aparecera con su nombre y tamano
4. (Opcional) Activa "Usar OCR" si el PDF es una imagen escaneada
5. Click en "Convertir a Word"
6. Espera a que la barra de progreso complete
7. Click en "Descargar Archivo" para obtener tu .docx

**Formatos soportados:**
- .pdf (cualquier version)

**Opciones:**
- **Sin OCR:** Extrae texto nativo del PDF (mas rapido)
- **Con OCR:** Aplica reconocimiento optico de caracteres (para PDFs escaneados)

**Nota sobre OCR:**
- Requiere Tesseract-OCR instalado en el servidor
- Procesa imagenes dentro del PDF
- Mas lento pero extrae texto de documentos escaneados
- Precision: ~95% en documentos limpios

---

### 3. Historial de Conversiones

**Acceso:** Pestana "Historial"

**Que muestra:**
- Todas tus conversiones realizadas
- Tipo de conversion (Word to PDF / PDF to Word)
- Fecha y hora
- Estado (Completado, Procesando, Error)
- Si se uso OCR
- Botones de descarga y eliminacion

**Acciones disponibles:**
- Descargar archivos convertidos
- Eliminar conversiones antiguas
- Ver detalles de cada trabajo

---

## Limitaciones y Requisitos

### Tamano de Archivos
- Maximo: 20MB por archivo
- Recomendado: <10MB para mejor rendimiento

### Formatos
- Word: .doc, .docx
- PDF: .pdf
- Salida Word: .docx (formato moderno)
- Salida PDF: .pdf

### Requisitos del Sistema (Servidor)
- Python 3.11+
- Librerias: python-docx, reportlab, PyPDF2, Pillow
- Para OCR: Tesseract-OCR instalado

---

## Instalacion de Tesseract (Para OCR)

### Windows
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Ejecutar instalador
3. Agregar al PATH: C:\Program Files\Tesseract-OCR
4. Instalar paquete de idioma espanol

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-spa
```

### macOS
```bash
brew install tesseract
brew install tesseract-lang
```

### Verificar instalacion
```bash
tesseract --version
```

---

## Casos de Uso

### Estudiantes
- Convertir apuntes de Word a PDF para entregar
- Convertir PDF de presentaciones a Word para editar
- Extraer texto de documentos escaneados con OCR
- Compartir documentos en formato universal (PDF)

### Profesores
- Convertir syllabi a PDF
- Editar PDFs de examenes
- Extraer texto de documentos escaneados

### Administracion
- Convertir documentos oficiales
- Procesar formularios escaneados
- Generar documentos en formatos especificos

---

## Preguntas Frecuentes

### ¿Los archivos se guardan en el servidor?
Si, se guardan en media/conversiones/ pero solo tu puedes acceder a ellos.

### ¿Cuanto tiempo se mantienen?
Indefinidamente hasta que los elimines manualmente desde el historial.

### ¿Hay limite de conversiones?
No, conversiones ilimitadas y gratuitas.

### ¿Que tan preciso es el OCR?
- Documentos limpios: ~95% precision
- Documentos de baja calidad: ~70-80%
- Depende de la calidad del escaneo original

### ¿Puedo convertir archivos protegidos?
No, los PDFs con proteccion DRM no se pueden convertir.

### ¿Se mantiene el formato?
- Word a PDF: Si, preserva estilos y formato
- PDF a Word: Se hace mejor esfuerzo, puede requerir ajustes menores

---

## Soluc ion de Problemas

### "Error al convertir el archivo"
- Verifica que el archivo no este corrupto
- Intenta con un archivo mas pequeno
- Revisa que el formato sea correcto

### "OCR no funciona"
- Verifica que Tesseract este instalado
- Revisa logs del servidor
- Intenta sin OCR primero

### "Archivo muy grande"
- Reduce el tamano del archivo
- Comprime imagenes en el documento original
- Limite: 20MB

---

## Soporte Tecnico

**Logs del servidor:**
```bash
cd proyecto/src/backend
# Ver errores
Get-Content logs\errors.log -Tail 50

# Ver logs de conversion
Get-Content logs\api.log | Select-String "converter"
```

**Admin:**
http://127.0.0.1:8000/admin/document_converter/conversionjob/

---

Fecha: 9 de Octubre 2025
Version: 1.0.0
Estado: FUNCIONAL

