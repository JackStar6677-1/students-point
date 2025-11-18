# 🚀 Inicio Rápido - StudentsPoint

## Para Desarrollo Local (Windows)

### Opción 1: Script Completo (Recomendado)

Simplemente haz **doble click** en:

```
iniciar_desarrollo_full.bat
```

Este script automáticamente:
- ✅ Crea/activa entorno virtual Python (.venv)
- ✅ Instala todas las dependencias
- ✅ Crea archivo .env de desarrollo
- ✅ Aplica migraciones de base de datos
- ✅ Recolecta archivos estáticos
- ✅ Crea superusuario (admin/admin123)
- ✅ Crea usuarios de prueba
- ✅ Puebla categorías del marketplace
- ✅ Crea datos de ejemplo
- ✅ Inicia Redis (si está instalado)
- ✅ Inicia Celery worker
- ✅ Inicia servidor Django

**Listo en ~2-3 minutos** ⚡

### Opción 2: Script Básico (más rápido)

Si ya has ejecutado la opción 1 antes:

```
iniciar_desarrollo.bat
```

Solo inicia el servidor sin reinstalar todo.

---

## URLs de Acceso

Después de ejecutar el script, accede a:

- **Aplicación**: http://127.0.0.1:8000
- **Panel Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/

### Credenciales por defecto:
- **Superusuario**: `admin` / `admin123`
- **Usuario demo**: `estudiante` / `demo123`

---

## ¿Qué hacer si algo falla?

### Problema: Python no encontrado
**Solución**: Instala Python 3.11+ desde https://python.org

### Problema: Error en migraciones
**Solución**: 
```bash
cd proyecto/src/backend
python manage.py migrate --run-syncdb
```

### Problema: Redis no inicia
**Solución**: No es crítico para desarrollo básico. Puedes continuar sin Redis.

### Problema: Celery falla
**Solución**: Tampoco es crítico. El sistema funciona sin tareas asíncronas.

---

## Para Desarrollo en Linux/Mac

```bash
./iniciar_desarrollo.sh
```

O manualmente:
```bash
# 1. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
cd proyecto/src/backend
pip install -r requirements.txt

# 3. Configurar entorno
cp ../../env.development.example .env

# 4. Migrar base de datos
python manage.py migrate
python manage.py collectstatic --noinput

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

---

## Para PWA/Móvil

Ver guía completa: [`docs/guias/GUIA-RAPIDA-MOVIL.md`](docs/guias/GUIA-RAPIDA-MOVIL.md)

**Resumen**: Necesitas HTTPS. Opciones gratis:
- PythonAnywhere (~5 minutos)
- Render.com (~10 minutos)
- Railway.app (~10 minutos)

---

## Documentación Completa

- 📚 **Guía completa**: [`docs/GUIA-COMPLETA.md`](docs/GUIA-COMPLETA.md)
- 📂 **Toda la documentación**: [`docs/`](docs/)
- 📋 **Notas de versión**: [`docs/releases/`](docs/releases/)
- 🔧 **Guías técnicas**: [`docs/guias/`](docs/guias/)

---

## Atajos de Desarrollo

### Ver logs en tiempo real:
```bash
scripts/ver_logs.bat          # Windows
scripts/ver_logs.sh           # Linux/Mac
```

### Ejecutar tests:
```bash
python tests/test_suite_completo.py --verbose --coverage
```

### Detener servicios:
Presiona `Ctrl+C` en cada ventana (Django, Celery, Redis) o ciérralas.

---

**¡Listo para desarrollar! 🎉**

