# Guia de Verificacion de Estandarizacion

## Pasos para Verificar los Cambios

### 1. Limpiar Cache del Navegador

**En Chrome/Edge:**
1. Presiona `Ctrl + Shift + Delete`
2. Selecciona "Todo el tiempo"
3. Marca "Imagenes y archivos en cache"
4. Marca "Archivos de aplicaciones web"
5. Haz clic en "Borrar datos"

**Alternativa Rapida:**
- Presiona `Ctrl + F5` (recarga forzada)
- O abre DevTools (`F12`) > Network > marca "Disable cache" > Recarga

### 2. Verificar Paginas con Sidebar

Visita cada una de estas URLs y verifica:

#### Homepage
- URL: `http://127.0.0.1:8000/`
- Verificar: Sidebar oscuro izquierdo, contenido central claro, item "Inicio" activo

#### Mi Cuenta
- URL: `http://127.0.0.1:8000/account.html`
- Verificar: Formularios de perfil, cambio de contraseña, item "Mi Cuenta" activo

#### Foro
- URL: `http://127.0.0.1:8000/forum/`
- Verificar: Lista de posts estilo Reddit, sidebar con item "Foro" activo

#### Marketplace
- URL: `http://127.0.0.1:8000/market/`
- Verificar: Productos en grid, item "Marketplace" activo

#### Portafolio
- URL: `http://127.0.0.1:8000/portfolio/`
- Verificar: Proyectos y habilidades, item "Portafolio" activo

#### Cursos
- URL: `http://127.0.0.1:8000/cursos/`
- Verificar: Lista de cursos, item "Cursos" activo

#### Encuestas
- URL: `http://127.0.0.1:8000/encuestas/`
- Verificar: Encuestas disponibles, item "Encuestas" activo

#### Reportes
- URL: `http://127.0.0.1:8000/reportes/`
- Verificar: Dashboard de reportes, item "Reportes" activo

#### Bienestar
- URL: `http://127.0.0.1:8000/bienestar/`
- Verificar: Servicios de bienestar, item "Bienestar" activo

#### Conversor
- URL: `http://127.0.0.1:8000/converter/`
- Verificar: Herramienta de conversion, item "Conversor" activo

#### Recorridos Virtuales
- URL: `http://127.0.0.1:8000/streetview/`
- Verificar: Mapa interactivo, item "Recorridos" activo

### 3. Verificar Elementos del Sidebar

En cada pagina, verifica que el sidebar tenga:

#### Header del Sidebar:
- [ ] Logo de StudentsPoint visible
- [ ] Titulo "StudentsPoint" visible
- [ ] Avatar de usuario
- [ ] Nombre de usuario (dinamico)
- [ ] Rol de usuario (dinamico)

#### Menu de Navegacion:
- [ ] 10 items de menu visibles
- [ ] Iconos correctos para cada item
- [ ] Item activo resaltado (fondo morado, borde izquierdo)
- [ ] Hover effect funcional (fondo cambia al pasar el mouse)

#### Footer del Sidebar:
- [ ] "Mi Cuenta" visible
- [ ] "Cerrar Sesion" visible
- [ ] Click en "Cerrar Sesion" redirige a login

### 4. Verificar Top Header

En cada pagina, verifica que el header superior tenga:

- [ ] Titulo de la pagina correcto
- [ ] Fondo blanco
- [ ] Borde inferior sutil
- [ ] Boton de notificaciones (campana)
- [ ] Boton de configuracion (engranaje)
- [ ] Header fijo al hacer scroll

### 5. Verificar Contenido Principal

En cada pagina, verifica:

- [ ] Contenido centrado en area principal
- [ ] Fondo claro (`#f9fafb`)
- [ ] Cards con fondo blanco
- [ ] Sombras sutiles en cards
- [ ] Border-radius de 12px en cards
- [ ] Padding adecuado (32px en desktop)

### 6. Verificar Botones

Busca botones en las paginas y verifica:

#### Botones Primarios (`.btn-studentspoint`):
- [ ] Fondo morado (`#6366f1`)
- [ ] Texto blanco
- [ ] Border-radius 8px
- [ ] Hover: color mas oscuro + elevacion
- [ ] Cursor: pointer

#### Botones Secundarios (`.btn-studentspoint-outline`):
- [ ] Borde morado
- [ ] Texto morado
- [ ] Fondo transparente
- [ ] Hover: fondo morado + texto blanco

### 7. Verificar Responsive (Mobile)

Redimensiona el navegador a menos de 768px y verifica:

- [ ] Sidebar se oculta
- [ ] Contenido principal ocupa ancho completo
- [ ] Cards se ajustan al ancho disponible
- [ ] Padding reducido (16px)
- [ ] Botones se adaptan al ancho

### 8. Verificar Navegacion

Haz clic en cada item del sidebar y verifica:

- [ ] Redirige a la URL correcta
- [ ] Nueva pagina carga correctamente
- [ ] Item activo cambia segun la pagina
- [ ] No hay errores 404
- [ ] CSS y JS cargan correctamente

### 9. Verificar Consistencia

Compara visualmente todas las paginas y verifica:

- [ ] Mismo estilo de sidebar en todas
- [ ] Misma paleta de colores
- [ ] Misma tipografia
- [ ] Mismos estilos de cards
- [ ] Mismos botones
- [ ] Mismas animaciones

### 10. Verificar en Console del Navegador

Abre DevTools (`F12`) > Console y verifica:

- [ ] No hay errores de JavaScript
- [ ] No hay errores de CSS
- [ ] No hay recursos 404
- [ ] Scripts cargan correctamente
- [ ] Fuentes cargan correctamente

### 11. Verificar Performance

En DevTools > Network:

- [ ] CSS de base-layout.css carga una sola vez
- [ ] Cache funciona correctamente
- [ ] No hay recursos duplicados
- [ ] Tiempo de carga razonable (<2s)

### 12. Verificar Login/Logout

#### Login:
1. Ve a `http://127.0.0.1:8000/login.html`
2. Verifica que NO tenga sidebar (diseño especial)
3. Inicia sesion
4. Verifica redireccion a homepage con sidebar

#### Logout:
1. En cualquier pagina con sidebar
2. Haz clic en "Cerrar Sesion"
3. Verifica redireccion a login
4. Verifica que tokens se eliminan de localStorage

## Checklist Final

- [ ] Todas las paginas cargan sin errores
- [ ] Sidebar visible y funcional en todas las paginas
- [ ] Menu items activos correctamente
- [ ] Navegacion fluida entre paginas
- [ ] Responsive funciona en mobile
- [ ] Botones y cards con estilos correctos
- [ ] No hay errores en console
- [ ] Performance aceptable
- [ ] Login/Logout funciona correctamente

## Problemas Comunes y Soluciones

### Problema: CSS no carga
**Solucion**: Ejecutar `python manage.py collectstatic --noinput`

### Problema: Sidebar no aparece
**Solucion**: Limpiar cache del navegador (`Ctrl + Shift + Delete`)

### Problema: Item activo no resalta
**Solucion**: Verificar que la clase `active` este en el item correcto del HTML

### Problema: 404 en archivos estaticos
**Solucion**: Verificar que `base-layout.css` este en `staticfiles/css/`

### Problema: Contenido se ve mal en mobile
**Solucion**: Verificar que `viewport` meta tag este en el `<head>`

## Logs a Revisar

Si hay problemas, revisar logs en:
- `proyecto/src/backend/logs/studentspoint.log`
- Console del navegador (F12 > Console)
- Network tab (F12 > Network) para recursos 404

## Exito!

Si todos los checks pasan, la estandarizacion esta completa y funcionando correctamente.

**Disfruta del nuevo diseño profesional y unificado de StudentsPoint!**

---

**Fecha de Verificacion**: 10 de Octubre de 2025

