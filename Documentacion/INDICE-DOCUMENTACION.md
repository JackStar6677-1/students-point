# INDICE DE DOCUMENTACION - STUDENTSPOINT

Este documento proporciona un indice completo de toda la documentacion del proyecto,
organizada por categorias para facilitar su navegacion.

---

## ESTRUCTURA DE CARPETAS

```
Documentacion/
├── config-avanzada/          # Documentacion tecnica del proyecto
├── implementaciones/         # Implementaciones completas de sistemas
├── especificaciones/         # Especificaciones de requisitos
├── guias/                    # Guias de configuracion y uso
└── academico/                # Documentos academicos y evidencias
```

---

## 1. DOCUMENTACION TECNICA (config-avanzada/)

### Descripcion General del Proyecto
**Archivo:** `config-avanzada/descripcion-proyecto.txt`
**Contenido:**
- Nombre y tipo de proyecto
- Vision general y proposito
- Caracteristicas principales (11 sistemas)
- Arquitectura tecnica
- Modelo de datos
- Capacidades offline
- Seguridad
- Estado actual del proyecto

### Estructura del Proyecto
**Archivo:** `config-avanzada/estructura-proyecto.txt`
**Contenido:**
- Organizacion de directorios completa
- Estructura de cada carpeta principal
- 11 aplicaciones Django con componentes
- Frontend modular
- Flujo de datos y comunicacion
- Convenciones y estandares

### Herramientas Utilizadas
**Archivo:** `config-avanzada/herramientas-utilizadas.txt`
**Contenido:**
- Stack tecnologico completo
- Backend: Django, DRF, PostgreSQL
- Frontend: HTML5, CSS3, JavaScript
- Cache y tareas asincronas: Redis, Celery
- PWA: Service Worker, Manifest
- Razon de eleccion de cada herramienta
- Versiones minimas requeridas

### Desarrollo Desde Cero
**Archivo:** `config-avanzada/desarrollo-desde-cero.txt`
**Contenido:**
- Enfasis en desarrollo original
- Modulos desarrollados sin plantillas
- Diseño personalizado
- Arquitectura propia
- Funcionalidades unicas

### Instrucciones para Asistentes Automatizados
**Archivo:** `config-avanzada/instrucciones-ia.txt`
**Contenido:**
- Contexto del proyecto
- Directrices de codigo backend
- Directrices de codigo frontend
- Sistema de autenticacion
- Sistema de foros
- PWA y Service Worker
- Patrones de codigo especificos
- Soluciones a problemas comunes

---

## 2. IMPLEMENTACIONES COMPLETAS (implementaciones/)

### Sistema de Autenticacion
**Archivo:** `implementaciones/autenticacion-implementacion-completa.txt`
**Contenido:**
- Registro con verificacion de email
- Sistema anti-bots con codigos de 6 digitos
- Recuperacion de contraseña por email
- Personalizacion de perfil completa
- 12 carreras disponibles
- Cambio de carrera con historial
- Endpoints API
- Flujos de usuario
- Casos de uso

### Sistema de Foros
**Archivo:** `implementaciones/foro-implementacion-completa.txt`
**Contenido:**
- Foros por carrera
- Restriccion de publicacion por carrera
- Tipos de publicaciones
- Censura automatica de contenido
- Revision manual de imagenes
- Foros publicos y privados
- Sistema de moderacion
- Encuestas con opciones
- Endpoints API
- Flujos completos

---

## 3. ESPECIFICACIONES DE REQUISITOS (especificaciones/)

### Especificacion del Sistema de Foros
**Archivo:** `especificaciones/foro detallado.txt`
**Contenido:**
- Foros personalizados por carrera
- Tipos de publicaciones requeridos
- Filtrado y censura de contenido
- Revision de imagenes
- Roles de usuario
- Foros publicos vs privados
- Cambio de carrera

### Especificacion del Sistema de Autenticacion
**Archivo:** `especificaciones/login-profile-register detallado.txt`
**Contenido:**
- Registro de usuario
- Login seguro
- Cambio de contraseña
- Personalizacion de perfil
- Areas de estudio multiples
- Gestion de perfiles y privilegios
- Verificacion de email anti-bots

---

## 4. GUIAS DE CONFIGURACION Y USO (guias/)

### Configuracion de Google OAuth y Email
**Archivo:** `guias/CONFIGURACION-GOOGLE-EMAIL.md`
**Contenido:**
- Estado actual del sistema de email (SMTP real)
- Configuracion de email en desarrollo
- Configuracion de email en produccion
- Google OAuth en desarrollo (ya configurado)
- Google OAuth en produccion
- Como probar el sistema
- Troubleshooting

### Estado del Proyecto y Pruebas
**Archivo:** `guias/PRUEBAS-Y-ESTADO-PROYECTO.md`
**Contenido:**
- Verificaciones de sistema Django
- Estado de migraciones de BD
- Resultados de tests unitarios
- Archivos estaticos
- Sistema de email (estado funcional)
- Google OAuth (estado funcional)
- Estado de funcionalidades
- Endpoints API funcionales
- Bugs conocidos (ninguno)
- Acciones requeridas

### Configuracion de Email Desarrollo
**Archivo:** `guias/config_email_desarrollo.txt`
**Contenido:**
- Credenciales configuradas
- Ubicacion de la configuracion
- Como funciona el sistema
- Como probar
- Notas importantes

### Recorridos Virtuales
**Archivo:** `guias/Recorridos_Virtuales.md`
**Contenido:**
- Documentacion del sistema de recorridos
- Como funciona
- Configuracion

---

## 5. DOCUMENTOS ACADEMICOS (academico/)

### Fase 1 del Proyecto
**Carpeta:** `academico/FASE 1/`
**Contenido:**
- Evidencias grupales
  - Formativa Fase 1
  - Guia del estudiante
  - Presentacion
  - Planilla de evaluacion
- Evidencias individuales
  - Autoevaluaciones de competencias
  - Diarios de reflexion
  - Autoevaluaciones de fase

### Cronograma del Capstone
**Archivo:** `academico/2025_2_Cronograma_Capstone.xlsx`
**Contenido:** Planificacion temporal del proyecto

### Presentacion del Proyecto
**Archivo:** `academico/Duoc-Point.pptx`
**Contenido:** Presentacion PowerPoint del proyecto

### Instructivo 2025
**Archivo:** `academico/Instructivo 2025.pdf`
**Contenido:** Instructivo del proyecto Capstone

### Documento II2020
**Archivo:** `academico/II2020.pdf`
**Contenido:** Documentacion academica relacionada

### Resumen de Evidencias
**Archivo:** `academico/Resumen evidencias.xlsx`
**Contenido:** Resumen de evidencias del proyecto

### Kanban del Proyecto
**Archivo:** `academico/N3qcyggF - duoc-point-kanban.json`
**Contenido:** Tablero Kanban exportado del proyecto

---

## DOCUMENTOS EN LA RAIZ DEL PROYECTO

### README.md
**Ubicacion:** `/README.md`
**Contenido:**
- Descripcion general del proyecto
- Caracteristicas principales
- Stack tecnologico
- Instalacion y configuracion
- Estructura del proyecto
- Uso del sistema
- API endpoints
- Seguridad
- Equipo de desarrollo

### ROADMAP.md
**Ubicacion:** `/ROADMAP.md`
**Contenido:**
- Vision general
- Cronograma de desarrollo (Fases 1-3)
- Funcionalidades actuales
- Criterios de evaluacion
- Potencial de expansion

### CHANGELOG.md
**Ubicacion:** `/CHANGELOG.md`
**Contenido:**
- Historial de cambios del proyecto
- Version 2.1.0 (actual)
- Version 2.0.0
- Version 1.5.0
- Version 1.0.0
- Proximas versiones

### DEPLOYMENT.md
**Ubicacion:** `/DEPLOYMENT.md`
**Contenido:**
- Guia de despliegue completa
- Desarrollo local
- Despliegue en servidor
- Configuracion de servicios externos
- Monitoreo y mantenimiento
- Solucion de problemas

---

## COMO USAR ESTA DOCUMENTACION

### Para Desarrolladores Nuevos
1. Leer `README.md` (vision general)
2. Leer `config-avanzada/descripcion-proyecto.txt` (detalle completo)
3. Leer `config-avanzada/estructura-proyecto.txt` (organizacion)
4. Revisar `implementaciones/` (sistemas implementados)

### Para Configurar el Proyecto
1. Seguir `README.md` seccion Instalacion
2. Revisar `guias/CONFIGURACION-GOOGLE-EMAIL.md` (email y OAuth)
3. Revisar `guias/PRUEBAS-Y-ESTADO-PROYECTO.md` (verificar estado)

### Para Entender Implementaciones
1. Revisar `especificaciones/` (que se requeria)
2. Revisar `implementaciones/` (como se implemento)
3. Revisar codigo fuente en `proyecto/src/backend/`

### Para Despliegue en Produccion
1. Leer `DEPLOYMENT.md` (guia completa)
2. Leer `guias/CONFIGURACION-GOOGLE-EMAIL.md` seccion produccion

### Para Documentacion Academica
1. Revisar `academico/FASE 1/` (evidencias)
2. Revisar `academico/Cronograma` (planificacion)
3. Revisar `academico/Presentacion` (materiales)

### Para Asistentes Automatizados
1. Leer `config-avanzada/instrucciones-ia.txt` (guia completa)
2. Revisar `config-avanzada/herramientas-utilizadas.txt` (stack)
3. Revisar `implementaciones/` (sistemas implementados)

---

## DOCUMENTOS POR AUDIENCIA

### Estudiantes/Desarrolladores
- README.md
- config-avanzada/* (todo)
- implementaciones/* (todo)
- guias/CONFIGURACION-GOOGLE-EMAIL.md
- guias/PRUEBAS-Y-ESTADO-PROYECTO.md

### Profesores/Evaluadores
- README.md
- ROADMAP.md
- config-avanzada/descripcion-proyecto.txt
- academico/* (todo)
- implementaciones/* (revisionar funcionalidades)

### Usuarios Finales
- guias/CONFIGURACION-GOOGLE-EMAIL.md (como usar)
- README.md seccion Uso

### Administradores de Sistema
- DEPLOYMENT.md
- guias/CONFIGURACION-GOOGLE-EMAIL.md
- guias/PRUEBAS-Y-ESTADO-PROYECTO.md

---

## ACTUALIZACIONES DE DOCUMENTACION

**Ultima actualizacion general:** Octubre 2025

**Documentos actualizados recientemente:**
- implementaciones/autenticacion-implementacion-completa.txt (09/10/2025)
- implementaciones/foro-implementacion-completa.txt (09/10/2025)
- guias/CONFIGURACION-GOOGLE-EMAIL.md (09/10/2025)
- guias/PRUEBAS-Y-ESTADO-PROYECTO.md (09/10/2025)
- config-avanzada/descripcion-proyecto.txt (09/10/2025)

**Mantenedores de documentacion:**
- Equipo StudentsPoint
- Pablo Avendaño, Darosh Luco, Isaac Paz

---

## CONTRIBUIR A LA DOCUMENTACION

Si encuentras:
- Informacion desactualizada
- Errores o inconsistencias
- Falta de claridad
- Necesidad de nuevos documentos

Por favor:
1. Crear issue en GitHub
2. O actualizar directamente y hacer PR

---

**Duoc UC - Ingenieria en Informatica**  
**Proyecto de Capstone 2025**

