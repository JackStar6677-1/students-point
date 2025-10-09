# RELEASES - STUDENTSPOINT

Registro de versiones oficiales del proyecto StudentsPoint.

---

## v2.1.0 - Sistema de Foros y Autenticacion Completa (9 Octubre 2025)

**Tag:** v2.1.0  
**Fecha:** 9 de Octubre 2025  
**Estado:** RELEASE ESTABLE

### Sistemas Implementados

#### Sistema de Foros Avanzado
- Foros personalizados por carrera
- Restriccion de publicacion por carrera (validada en backend)
- Libertad de comentarios en todos los foros
- Tipos de publicaciones: comentarios, encuestas, imagenes, otros
- Censura automatica de contenido ofensivo (ejemplo: "palabra" -> "p######")
- Revision manual de imagenes por administradores
- Foros publicos y privados con control de acceso
- Sistema de moderacion automatica basada en palabras prohibidas
- Sistema de moderacion manual para administradores
- Panel de administracion con acciones masivas
- Modelo OpcionEncuesta para encuestas con opciones
- Modelo VotoEncuesta para registro de votos

#### Sistema de Autenticacion Completo
- Registro con verificacion obligatoria de email
- Codigos de verificacion de 6 digitos enviados por email
- Sistema anti-bots con codigos temporales (expiran en 15 min)
- Reenvio de codigos de verificacion si expiran
- Recuperacion de contraseña completa por email
- Codigos de recuperacion de 6 digitos (expiran en 30 min)
- Cambio de contraseña para usuarios autenticados
- Perfil personalizable con foto de perfil
- Campo semestre (1-12) para estudiantes
- 12 carreras disponibles mas "Estudiante Generico"
- Cambio de carrera cada semestre con historial completo
- Modelo CambioCarrera para auditoria
- Telefono, LinkedIn, GitHub en perfil

### Configuracion

#### Email SMTP Real
- Configurado Gmail SMTP en desarrollo
- Backend: smtp.EmailBackend
- Servidor: smtp.gmail.com:587
- Los emails se envian REALMENTE a usuarios
- Codigos de verificacion enviados por email real

#### Google OAuth 2.0
- Client ID y Secret configurados
- URIs autorizados: localhost:8000, 127.0.0.1:8000
- Login con Google funcional
- Integracion completa con sistema de usuarios

### Base de Datos

#### Migraciones Aplicadas
- accounts/0005: Verificacion email y recuperacion password
- accounts/0004: Modelo CambioCarrera
- forum/0003: Tipos de publicaciones, imagenes, encuestas, privacidad

#### Nuevos Campos
- User: semestre, picture_file, email_verification_code, is_email_verified, password_reset_code
- Foro: es_privado, descripcion, created_at
- Post: tipo, imagen, imagen_aprobada

#### Nuevos Modelos
- OpcionEncuesta
- VotoEncuesta
- CambioCarrera

### Testing

#### Tests Unitarios
- 6/6 tests pasando (100%)
- test_auth_me: 1 test
- test_campus_map: 2 tests
- test_login_api: 2 tests
- test_register_api: 1 test
- Tiempo de ejecucion: 7.99 segundos

#### Tests E2E
- 3 archivos disponibles
- test_homepage.py
- test_login.py
- test_register.py

### Documentacion

#### Reorganizacion Completa
- 5 subcarpetas tematicas creadas
- 32 archivos organizados
- Documentacion tecnica en config-avanzada/
- Implementaciones en implementaciones/
- Especificaciones en especificaciones/
- Guias en guias/
- Documentos academicos en academico/

#### Documentos Nuevos
- INDICE-DOCUMENTACION.md
- INFORME-TESTS.md
- Documentacion/README.md
- autenticacion-implementacion-completa.txt (842 lineas)
- foro-implementacion-completa.txt (549 lineas)
- CONFIGURACION-GOOGLE-EMAIL.md
- PRUEBAS-Y-ESTADO-PROYECTO.md

#### Documentos Actualizados
- README.md con nueva estructura organizada
- ROADMAP.md ajustado a escala realista
- CHANGELOG.md con detalles de v2.1.0

### Estructura del Proyecto

#### Carpetas FASE (En Raiz)
- FASE 1/ - Evidencias completas (Agosto-Septiembre 2025)
- FASE 2/ - Preparada para evidencias (Septiembre-Octubre 2025)
- FASE 3/ - Preparada para evidencias (Noviembre-Diciembre 2025)

NOTA IMPORTANTE: Las carpetas FASE deben permanecer en la raiz del proyecto
para compatibilidad con scripts automatizados de revision academica.

### Estadisticas

- Archivos modificados en release: 60+
- Lineas agregadas: 5,000+
- Nuevos endpoints API: 11
- Nuevos modelos de BD: 3
- Documentacion: 3,500+ lineas

---

## v2.0.0 - Arquitectura Base (15 Agosto 2025)

**Tag:** v2.0.0  
**Fecha:** 15 de Agosto 2025  
**Estado:** BASE DEL PROYECTO

### Caracteristicas Principales
- Arquitectura base con Django 5.2
- PWA con Service Worker
- Sistema de autenticacion JWT basico
- Google OAuth 2.0 basico
- Aplicaciones core implementadas
- API REST con Django REST Framework
- Sistema de foros basico
- Marketplace estudiantil
- Portafolio profesional con generacion de PDF
- Recorridos virtuales del campus
- Sistema de encuestas
- Sistema de reportes
- Bienestar estudiantil
- Gestion de horarios

---

## v1.5.0 - Sistema Base (10 Agosto 2025)

**Tag:** v1.5.0 (implicito)  
**Fecha:** 10 de Agosto 2025  
**Estado:** VERSION INICIAL

### Caracteristicas
- Sistema de autenticacion JWT
- Integracion Google OAuth
- PWA basica con Service Worker
- Sistema de foros basico
- Marketplace con integracion externa
- Portafolio con generacion PDF

---

## v1.0.0 - Proyecto Inicial (1 Agosto 2025)

**Tag:** v1.0.0 (implicito)  
**Fecha:** 1 de Agosto 2025  
**Estado:** INICIO DEL PROYECTO

### Caracteristicas
- Version inicial del proyecto
- Estructura basica de Django
- Aplicaciones core creadas
- Documentacion inicial

---

## Proximas Versiones

### v2.2.0 - Entrega Final (Diciembre 2025)

**Planeado para:** Diciembre 2025

**Objetivos:**
- Testing completo de funcionalidades
- Optimizacion de rendimiento
- Correccion de todos los bugs
- Documentacion tecnica final
- Manual de usuario completo
- Preparacion de presentacion final
- Video demostrativo

---

## Como Usar Releases

### Ver Todas las Releases
```bash
git tag -l
```

### Ver Detalles de un Release
```bash
git show v2.1.0
```

### Cambiar a un Release Especifico
```bash
git checkout v2.1.0
```

### Volver a la Version Mas Reciente
```bash
git checkout main
```

### Comparar Versiones
```bash
git diff v2.0.0..v2.1.0
```

---

## Semantic Versioning

El proyecto sigue Semantic Versioning (semver.org):

**MAJOR.MINOR.PATCH**

- **MAJOR** (X.0.0): Cambios incompatibles en API
- **MINOR** (0.X.0): Nueva funcionalidad compatible con versiones anteriores
- **PATCH** (0.0.X): Correcciones de bugs

**Ejemplos:**
- v2.1.0: Nueva funcionalidad (foros avanzados, autenticacion completa)
- v2.0.0: Version base del proyecto
- v2.1.1: Seria correccion de bugs en v2.1.0

---

## Notas de Release

Las notas completas de cada version se encuentran en:
- CHANGELOG.md (historial de cambios detallado)
- GitHub Releases (cuando se publiquen)

---

**Equipo StudentsPoint**  
**Duoc UC - Ingenieria en Informatica**  
**Proyecto de Capstone 2025**

