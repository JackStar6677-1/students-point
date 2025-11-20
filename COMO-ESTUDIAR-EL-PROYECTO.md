# Como Estudiar StudentsPoint - Plan de Estudio

## Resumen de lo que Hicimos

### Limpieza Completada
- ✅ **37 archivos .md eliminados** (redundantes y desactualizados)
- ✅ **2 documentos nuevos creados** para presentacion
- ✅ **Playit.gg eliminado** completamente del proyecto
- ✅ **Documentacion reorganizada** y actualizada
- ✅ **De 96 a 59 archivos .md** (-38%)

### Documentos Clave Creados
1. **`docs/PRESENTACION-PROYECTO.md`** - Tu guia maestra para la presentacion
2. **`docs/BASE-DE-DATOS-RESUMEN.md`** - Esquema completo de la base de datos

---

## Plan de Estudio (3-4 Horas)

### Fase 1: Vision General (30 min)

**1. Lee el README principal**
```
Archivo: README.md (raiz)
Que aprenderas: Que es el proyecto, stack tecnologico, inicio rapido
```

**2. Lee PRESENTACION-PROYECTO.md (primeras 3 secciones)**
```
Archivo: docs/PRESENTACION-PROYECTO.md
Lee hasta: "Arquitectura del Sistema"
Que aprenderas: Problema que resuelve, stack completo, estructura
```

**3. Inicia el proyecto**
```bash
# Opcion 1: Launcher (recomendado)
iniciar_studentspoint.bat
# Selecciona [1] Local

# Opcion 2: Script directo
scripts\iniciar_desarrollo.bat
```

**4. Navega la aplicacion (15 min)**
```
URLs:
- http://127.0.0.1:8000 - Homepage
- http://127.0.0.1:8000/admin/ - Panel admin (admin@studentspoint.app / admin123)
- http://127.0.0.1:8000/api/docs/ - API documentada (Swagger)

Explora:
- Foro (crea un post)
- Marketplace (publica un producto)
- Portafolio (agrega proyecto)
- Encuestas
```

---

### Fase 2: Arquitectura y Base de Datos (45 min)

**5. Estudia la Arquitectura**
```
Archivo: docs/arquitectura/ARQUITECTURA-SOFTWARE.md

Enfocate en:
- Diagrama de componentes
- Estructura de apps Django
- Flujo de request/response
- Separacion de concerns

Tiempo: 20 minutos
```

**6. Entiende la Base de Datos**
```
Archivo: docs/BASE-DE-DATOS-RESUMEN.md

Enfocate en:
- Tablas principales (CustomUser, Post, Producto, Portafolio)
- Relaciones FK (quien se relaciona con quien)
- Indices (que campos estan indexados)
- Consultas SQL utiles (al final del documento)

Tiempo: 25 minutos

TIP: Abre la base de datos con DB Browser for SQLite:
1. Descarga: https://sqlitebrowser.org/
2. Abre: proyecto\src\backend\db.sqlite3
3. Explora las tablas visualmente
```

---

### Fase 3: Modulos Funcionales (60 min)

**7. Estudia cada modulo (10 min cada uno)**

```
Archivo: docs/PRESENTACION-PROYECTO.md (seccion "Modulos Funcionales")

Modulos prioritarios:
1. Foro - Sistema de posts con moderacion
2. Marketplace - Compra/venta
3. Portafolio - CV digital
4. Encuestas - Sistema de votacion
5. Reportes - Incidencias del campus
6. Cursos OTEC - Capacitaciones

Para cada modulo entiende:
- Que problema resuelve
- Flujo de usuario
- Tablas de BD involucradas
- Endpoints API principales
```

**Practica:** Usa cada modulo en la app mientras lees su documentacion

---

### Fase 4: API y Frontend (45 min)

**8. Explora la API**
```
URL: http://127.0.0.1:8000/api/docs/

Endpoints prioritarios:
- POST /api/auth/login/ - Como se autentica
- GET /api/forum/posts/ - Listar posts
- POST /api/forum/posts/ - Crear post
- GET /api/market/productos/ - Listar productos
- GET /api/portfolio/portafolio/ - Obtener portafolio

Prueba:
1. Click en un endpoint
2. Click en "Try it out"
3. Modifica parametros
4. Click "Execute"
5. Ve la respuesta

Tiempo: 20 minutos
```

**9. Entiende el Frontend**
```
Ubicacion: proyecto/src/frontend/

Archivos clave:
- static/manifest.json - Configuracion PWA
- static/sw.js - Service Worker (funciona offline)
- static/css/styles.css - Estilos principales
- static/js/auth.js - Manejo de autenticacion
- forum/foro.html - Pagina del foro
- market/mercado.html - Pagina del marketplace

Que buscar:
- Como se hacen las peticiones fetch() a la API
- Como se maneja el JWT token
- Como se actualiza el DOM

Tiempo: 25 minutos
```

---

### Fase 5: PWA y Seguridad (30 min)

**10. Entiende la PWA**
```
Archivo: docs/PRESENTACION-PROYECTO.md (seccion "Progressive Web App")

Conceptos clave:
- Que es una PWA (web + app nativa)
- Service Worker (cache, offline)
- Web App Manifest (instalable)
- Ventajas sobre web/app tradicional

Practica:
1. Instala la PWA en tu Chrome:
   - Menu -> "Instalar StudentsPoint"
2. Prueba sin internet:
   - Cierra servidor
   - Abre la app instalada
   - Navega (algunas paginas funcionaran por cache)

Tiempo: 15 minutos
```

**11. Seguridad**
```
Archivo: docs/PRESENTACION-PROYECTO.md (seccion "Seguridad")

Enfocate en:
- JWT (como funciona el token)
- OAuth 2.0 (login con Google)
- Permisos por rol (estudiante/profesor/admin)
- CSRF, XSS, SQL Injection (como se previenen)

Tiempo: 15 minutos
```

---

### Fase 6: Testing y Deployment (30 min)

**12. Testing**
```
Archivo: pruebas_unitarias/README.md

Ejecuta tests:
cd proyecto\src\backend
pytest pruebas_unitarias/ -v

Ve que se prueba:
- APIs (test_api/)
- Models
- Serializers

Tiempo: 15 minutos
```

**13. Deployment**
```
Archivo: docs/guias/DEPLOYMENT-PRODUCTION.md

Lee sobre:
- Diferencia desarrollo vs produccion
- Nginx + Gunicorn
- PostgreSQL en produccion
- SSL/HTTPS

Tiempo: 15 minutos
```

---

## Preparacion para la Presentacion (1 hora)

### 14. Prepara tu Demo (30 min)

**Flujo sugerido (18-20 min):**

1. **Introduccion (2 min)**
   - Problema: Servicios estudiantiles fragmentados
   - Solucion: Plataforma centralizada

2. **Inicio (2 min)**
   - Muestra launcher: `iniciar_studentspoint.bat`
   - Explica opciones de inicio
   - Inicia servidor

3. **Demo Foro (3 min)**
   - Login como usuario
   - Crea post con imagen
   - Otro usuario comenta
   - Da like

4. **Demo Marketplace (3 min)**
   - Publica producto
   - Busca productos
   - Muestra filtros

5. **Demo Portafolio (2 min)**
   - Agrega proyecto
   - Muestra vista publica

6. **PWA (3 min)**
   - Instala en celular (grabado o en vivo)
   - Muestra funcionamiento offline

7. **Panel Admin (2 min)**
   - Dashboard
   - Moderacion

8. **Arquitectura (3 min)**
   - Diagrama de componentes
   - Stack tecnologico
   - Escalabilidad

**Practica este flujo 2-3 veces**

### 15. Prepara Respuestas a Preguntas (30 min)

**Lee y memoriza:**
```
Archivo: docs/PRESENTACION-PROYECTO.md (seccion "Preguntas Frecuentes")

Preguntas tipicas:
- Por que Django y no Node.js?
- Por que PWA y no app nativa?
- Como manejan la escalabilidad?
- Seguridad de datos sensibles?
- Cuanto tardo el desarrollo?
- Puede adaptarse a otras instituciones?

Prepara respuestas de 30-60 segundos cada una
```

---

## Atajos Rapidos

### Durante el Desarrollo
```bash
# Ver logs
scripts\ver_logs.bat

# Ejecutar tests
cd proyecto\src\backend
pytest pruebas_unitarias/ -v

# Crear superusuario manual
cd proyecto\src\backend
python manage.py createsuperuser

# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell de Django
python manage.py shell
```

### Base de Datos
```bash
# Abrir SQLite shell
cd proyecto\src\backend
sqlite3 db.sqlite3

# Comandos utiles en SQLite:
.tables                  # Listar tablas
.schema accounts_customuser  # Ver estructura de tabla
SELECT * FROM forum_post LIMIT 10;  # Query simple
.quit                    # Salir
```

### Explorar Codigo
```
Backend principal:
- proyecto/src/backend/studentspoint/apps/  - Todas las apps
- proyecto/src/backend/studentspoint/settings/  - Configuracion

Frontend:
- proyecto/src/frontend/  - HTML/CSS/JS
- proyecto/src/frontend/static/  - Archivos estaticos

Models importantes:
- accounts/models.py - CustomUser
- forum/models.py - Post, Categoria, Comentario
- market/models.py - Producto, CategoriaProducto

Views importantes:
- forum/views.py - APIs del foro
- market/views.py - APIs del marketplace
```

---

## Documentos de Referencia por Tema

### Para Entender Tecnico
- `docs/PRESENTACION-PROYECTO.md` - TODO
- `docs/BASE-DE-DATOS-RESUMEN.md` - Base de datos
- `docs/arquitectura/ARQUITECTURA-SOFTWARE.md` - Arquitectura
- `docs/GUIA-COMPLETA.md` - Documentacion completa

### Para la Defensa Academica
- `docs/academico/DEFENSA-PWA-CAPSTONE.md` - Argumentos
- `docs/academico/PWA-ARGUMENTOS-RAPIDOS.md` - Respuestas rapidas

### Para Iniciar/Configurar
- `README.md` - Inicio rapido
- `docs/guias/LAUNCHER.md` - Launcher universal
- `docs/guias/COMO-INICIAR.md` - Scripts disponibles
- `docs/guias/USAR-NGROK.md` - HTTPS para PWA

### Para Entender Modulos
- `docs/modulos/` - Documentacion especifica
- `docs/tecnologias/TECNOLOGIAS-USADAS.md` - Stack completo

---

## Checklist Pre-Presentacion

### Dia Antes
- [ ] Practica demo completo 3 veces
- [ ] Memoriza preguntas frecuentes
- [ ] Verifica que el servidor inicie sin errores
- [ ] Ten backup de la BD (cp db.sqlite3 db_backup.sqlite3)
- [ ] Graba video de respaldo por si falla internet

### Dia de la Presentacion
- [ ] Inicia servidor 10 min antes
- [ ] Abre pestañas clave:
  - [ ] http://127.0.0.1:8000
  - [ ] http://127.0.0.1:8000/admin/
  - [ ] http://127.0.0.1:8000/api/docs/
- [ ] Ten usuarios de prueba listos
- [ ] Cierra notificaciones/programas innecesarios
- [ ] Modo presentacion activado

---

## Numeros Importantes (Memorizalos)

```
Lineas de codigo: ~23,000
  - Backend: ~15,000
  - Frontend: ~8,000

Apps Django: 12
Modelos (tablas): 47
Endpoints API: 120+
Tests: 50+

Desarrollo: 4 meses (Agosto-Diciembre 2025)
Version: 5.0.0 Production-Ready

Stack:
- Backend: Django 5.2 + DRF
- Frontend: JavaScript ES6+ + CSS3
- BD: SQLite/PostgreSQL
- PWA: Service Workers + Manifest
```

---

## Recursos Finales

**Repositorio:** https://github.com/JackStar6677-1/students-point  
**Documentacion:** `docs/`  
**API Docs:** http://127.0.0.1:8000/api/docs/  
**Admin:** http://127.0.0.1:8000/admin/  

---

**Tiempo total estimado:** 3-4 horas para estudiar completamente  
**Enfoque:** Entiende el COMO y el POR QUE, no memorices codigo

**Exito en tu presentacion!** 🚀

