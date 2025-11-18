# Como Iniciar StudentsPoint

## Opcion 1: Inicio Completo (Recomendado)

```bash
iniciar_desarrollo.bat
```

**Incluye:**
- ✅ Verificacion de Python
- ✅ Instalacion automatica de dependencias
- ✅ Migraciones de base de datos
- ✅ Creacion de superusuario
- ✅ Recoleccion de archivos estaticos (PWA)
- ✅ Deteccion de IP de Tailscale
- ✅ Apertura automatica del navegador

---

## Opcion 2: Inicio Simple (Si hay problemas)

```bash
iniciar_simple.bat
```

**Incluye:**
- ✅ Instalacion basica
- ✅ Migraciones
- ✅ Archivos estaticos
- ✅ Inicio del servidor

---

## Opcion 3: Manual (Para desarrollo avanzado)

```bash
cd proyecto\src\backend
python manage.py runserver 0.0.0.0:8000
```

---

## Acceso a la Aplicacion

### Localhost
- **App:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin/

### Tailscale (para celular)
- **App:** http://100.75.238.19:8000
- **Admin:** http://100.75.238.19:8000/admin/

### Credenciales
- **Usuario:** admin@studentspoint.app
- **Password:** admin123

---

## Instalar PWA en Celular

1. Conecta tu celular a Tailscale
2. Abre Chrome en el celular
3. Navega a http://100.75.238.19:8000
4. Menu (⋮) → "Agregar a pantalla de inicio"
5. La app aparecera como una app nativa

---

## Solucion de Problemas

### Error: "Python no encontrado"
Instala Python 3.11+ desde python.org

### Error: "No se encontro el directorio backend"
Asegurate de estar en la raiz del proyecto

### Error: "no se esperaba : en este momento"
Usa `iniciar_simple.bat` en lugar de `iniciar_desarrollo.bat`

### El servidor no inicia
1. Cierra todas las ventanas de CMD
2. Ejecuta `iniciar_simple.bat`
3. Si persiste, ejecuta manualmente:
```bash
cd proyecto\src\backend
python manage.py runserver 0.0.0.0:8000
```

---

## Verificar PWA

```bash
verificar_pwa.bat
```

Este script verifica:
- Archivos PWA (sw.js, manifest.json)
- Iconos (8 tamaños)
- Estructura correcta

---

## Logs del Sistema

Los logs se guardan en `proyecto/src/backend/logs/`:
- `general.log` - Todos los eventos
- `errors.log` - Solo errores
- `api.log` - Peticiones API
- `auth.log` - Autenticacion

---

Para mas informacion, consulta:
- `INICIO_RAPIDO.md` - Guia rapida
- `docs/GUIA-COMPLETA.md` - Guia completa
- `docs/guias/INSTALACION-PWA.md` - PWA especifica

