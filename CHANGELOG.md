# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-10-09

### Agregado
- **Sistema de foros avanzado** personalizado por carrera
- **Restriccion de publicacion** por carrera validada en backend
- **Tipos de publicaciones**: comentarios, encuestas, imagenes, otros
- **Censura automatica** de contenido ofensivo con sistema parcial
- **Revision manual de imagenes** por administradores
- **Foros publicos y privados** con control de acceso
- **Sistema de moderacion** automatica y manual
- **Gestion de cambio de carrera** con historial completo
- **Panel de administracion** mejorado con acciones masivas
- **Modelos nuevos**: OpcionEncuesta, VotoEncuesta, CambioCarrera

### Cambiado
- **Modelo Foro** actualizado con campos es_privado y descripcion
- **Modelo Post** con tipos, imagen y sistema de censura
- **Vistas de foros** con validacion de permisos por carrera
- **Admin** mejorado con inline para opciones de encuesta
- **Documentacion** completa y actualizada
- **README y ROADMAP** actualizados con fechas correctas

### Corregido
- Referencias antiguas a "DuocPoint" eliminadas
- Fechas actualizadas a 2025
- Manifests actualizados con StudentsPoint

## [2.0.0] - 2025-08-15

### 🎉 Agregado
- **Migración completa** de Duoc Point a Students Point
- **Sistema de recorridos virtuales** con navegación por diapositivas
- **Sistema de encuestas completo** con votación y resultados en tiempo real
- **API REST mejorada** con serializers profesionales
- **Middleware personalizado** para CORS
- **Configuración de producción** optimizada
- **Documentación completa** con instrucciones paso a paso

### 🔧 Cambiado
- **URLs de imágenes** actualizadas (`imagenes/` → `static/images/`)
- **Serializers duplicados** resueltos (`SimpleStatusSerializer` → `NotificationStatusSerializer`)
- **Configuración de base de datos** mejorada para producción
- **Dockerfile de producción** actualizado
- **Scripts de instalación** actualizados

### 🐛 Corregido
- **29 warnings** del sistema resueltos
- **Servidor no iniciaba** - problema de configuración corregido
- **Rutas de archivos estáticos** corregidas
- **Referencias legacy** a Duoc Point eliminadas
- **Configuración CORS** para producción

### 🗑️ Eliminado
- **Carpeta `duocpoint/`** legacy eliminada
- **Configuraciones obsoletas** removidas
- **Archivos duplicados** consolidados

## [1.5.0] - 2025-08-10

### Agregado
- Sistema de autenticación JWT implementado
- Integración Google OAuth configurada
- PWA básica con Service Worker
- Sistema de foros basico
- Marketplace con integración externa
- Portafolio con generación PDF

### Cambiado
- Arquitectura migrada a Django 5.2
- Frontend actualizado a Bootstrap 5
- Base de datos configurada para SQLite/PostgreSQL

## [1.0.0] - 2025-08-01

### Agregado
- Version inicial del proyecto
- Estructura basica de Django
- Aplicaciones core implementadas
- Documentacion inicial creada

---

## Proximas Versiones

### [2.2.0] - Planeado para Noviembre 2025
- [ ] Performance optimization
- [ ] Testing coverage mejorado
- [ ] Panel de moderacion frontend
- [ ] Notificaciones push mejoradas

### [3.0.0] - Planeado para Diciembre 2025
- [ ] Integracion con calendarios externos
- [ ] Sistema de badges y gamificacion
- [ ] WebSockets para chat en tiempo real
- [ ] App movil nativa (fase inicial)
