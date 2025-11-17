# Release v5.1.0 - Sistema de Reportes con Fotos y Mejoras de Módulos

## 🎯 Resumen

Esta release incluye mejoras significativas en los módulos principales (Foros, Marketplace, Reportes, Encuestas) y la implementación completa del sistema de reportes de incidencias con subida de fotos opcionales.

## ✨ Nuevas Funcionalidades

### Sistema de Reportes de Incidencias
- **Subida de fotos opcionales**: Los estudiantes pueden adjuntar fotos para documentar problemas en salas de clases y espacios del campus
- **Formulario completo**: Modal con campos para categoría, descripción, ubicación (lat/lng) y múltiples fotos
- **Visualización mejorada**: Las fotos se muestran en las tarjetas de reportes con preview
- **Obtención automática de ubicación**: El sistema puede usar la ubicación del dispositivo del usuario
- **Validación de archivos**: Límite de 5MB por imagen con validación de tipo

### Mejoras en Módulos Existentes

#### Foros
- Comentarios, reportes y moderación operan con permisos y auditoría reforzada
- Sistema de moderación mejorado con cola de revisión

#### Marketplace
- Visualización del campo `precio_student_point` para ofertas preferentes dentro de StudentsPoint
- Validaciones de términos y condiciones obligatorias
- Analytics automáticos mejorados
- Comando para poblar categorías: `python manage.py poblar_categorias`

#### Encuestas
- Integración completa con roles (`moderator`, `director_carrera`)
- Sistema de votación mejorado
- Resultados en tiempo real
- Creación avanzada de encuestas

## 🔧 Mejoras Técnicas

### Scripts de Inicio
- **Nuevo script completo**: `iniciar_desarrollo_full.bat`
  - Crea entorno virtual automáticamente
  - Copia `env.development.example` si falta `.env`
  - Ejecuta migraciones y `collectstatic`
  - Crea usuarios demo
  - Intenta levantar Redis, Celery y Django en ventanas separadas

### PWA (Progressive Web App)
- Corrección de rutas en Service Worker
- Manejo de errores mejorado
- Soporte completo en todas las páginas
- Mejoras en notificaciones push

### Documentación
- Organización mejorada: carpetas para arquitectura, modelo de datos, tecnologías y módulos
- README actualizado con sección específica sobre sistema de reportes
- Documentación técnica expandida

### Base de Datos
- Nueva migración: `0002_reportemedia_imagen_alter_reportemedia_url.py`
- Campo `imagen` agregado a `ReporteMedia` (opcional)
- Soporte para almacenar imágenes subidas localmente

## 🐛 Correcciones

- Ajustes en suites de tests para alinearse con la API actual
- Corrección de imports y compatibilidad con linters
- Mejoras en el manejo de errores en frontend

## 📦 Archivos Modificados

### Backend
- `studentspoint/apps/reports/models.py` - Modelo actualizado con ImageField
- `studentspoint/apps/reports/serializers.py` - Serializer con soporte de imágenes
- `studentspoint/apps/reports/views.py` - ViewSet con manejo de multipart/form-data
- `studentspoint/apps/reports/migrations/0002_*.py` - Nueva migración

### Frontend
- `frontend/reportes/reportes.html` - Modal y formulario de creación
- `frontend/static/js/reportes.js` - Lógica de subida de fotos y creación de reportes

### Documentación
- `README.md` - Sección sobre sistema de reportes agregada
- Organización de documentación en carpetas temáticas

## 🚀 Cómo Usar las Nuevas Funcionalidades

### Crear un Reporte con Fotos

1. Navega a `/reportes/`
2. Haz clic en "Nuevo Reporte"
3. Completa el formulario:
   - Selecciona la sede/campus
   - Ingresa la categoría (ej: "Computador roto")
   - Describe el problema
   - Las coordenadas se pueden obtener automáticamente o ingresar manualmente
   - (Opcional) Selecciona fotos del problema
4. Haz clic en "Crear Reporte"

### Poblar Categorías del Marketplace

```bash
cd proyecto/src/backend
python manage.py poblar_categorias
```

## 📋 Requisitos

- Python 3.11+
- Django 5.2
- PostgreSQL (producción) o SQLite (desarrollo)
- Pillow (para manejo de imágenes)

## 🔄 Migraciones

**Importante**: Aplica las migraciones antes de usar las nuevas funcionalidades:

```bash
cd proyecto/src/backend
python manage.py migrate reports
```

## 📝 Notas

- Las imágenes en reportes son **opcionales** - permiten documentar visualmente el problema
- El sistema soporta múltiples fotos por reporte
- Las fotos se almacenan en `reports/images/` (configurable en settings)
- Los reportes sin fotos funcionan normalmente

## 🙏 Agradecimientos

Gracias al equipo por las pruebas y feedback continuo.

---

**Versión**: 5.1.0  
**Fecha**: Diciembre 2025  
**Estado**: Production-Ready

