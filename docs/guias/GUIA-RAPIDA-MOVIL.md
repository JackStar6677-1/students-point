# Guía Rápida: StudentsPoint en Móvil (PWA)

## ✅ Lo que YA tienes listo

- ✅ **PWA configurado** - manifest.json, service worker, todo listo
- ✅ **Integración móvil** - La app funciona como app nativa
- ✅ **Offline support** - Service worker cachea recursos
- ✅ **Instalable** - Se puede instalar en Android/iOS

## ⚠️ Lo ÚNICO que falta: HTTPS

**El PWA NO funciona sin HTTPS** (excepto localhost). Google lo exige.

## 🚀 Opciones RÁPIDAS (sin servidor propio)

### Opción 1: PythonAnywhere (GRATIS, 5 minutos)

1. **Crear cuenta**: https://www.pythonanywhere.com (gratis)
2. **Subir código**: 
   - Files → Upload → Sube tu proyecto
   - O conecta con Git desde la consola
3. **Configurar**:
   ```bash
   # En la consola de PythonAnywhere
   cd ~/students-point
   pip3.10 install -r proyecto/src/backend/requirements.txt
   python3.10 manage.py migrate
   python3.10 manage.py collectstatic --noinput
   ```
4. **Web tab**:
   - Source code: `/home/tuusuario/students-point/proyecto/src/backend`
   - WSGI: `/var/www/tuusuario_pythonanywhere_com_wsgi.py`
   - Static files: `/static/` → `/home/tuusuario/students-point/proyecto/src/backend/staticfiles/`
5. **HTTPS**: PythonAnywhere lo da GRATIS automáticamente
6. **Listo**: Tu app funciona en móvil con HTTPS

### Opción 2: Render.com (GRATIS, 10 minutos)

1. **Crear cuenta**: https://render.com
2. **Nuevo Web Service**:
   - Conecta tu GitHub
   - Build: `cd proyecto/src/backend && pip install -r requirements.txt`
   - Start: `gunicorn studentspoint.wsgi:application`
3. **HTTPS**: Automático y gratis
4. **Listo**: Funciona en móvil

### Opción 3: Railway.app (GRATIS, 10 minutos)

1. **Crear cuenta**: https://railway.app
2. **Nuevo proyecto** desde GitHub
3. **Auto-detecta Django** y despliega
4. **HTTPS**: Automático
5. **Listo**: Funciona en móvil

## 📱 Cómo probar en móvil

### Android (Chrome)
1. Abre tu URL con HTTPS
2. Menú (3 puntos) → "Agregar a pantalla de inicio"
3. Se instala como app nativa
4. Funciona offline

### iOS (Safari)
1. Abre tu URL con HTTPS
2. Compartir → "Agregar a pantalla de inicio"
3. Se instala como app
4. Funciona offline

## ✅ Checklist Pre-Despliegue

- [x] PWA configurado (manifest.json, sw.js)
- [x] Service Worker registrado
- [x] Iconos presentes (192x192, 512x512)
- [ ] **HTTPS activo** (solo falta esto)
- [ ] Dominio configurado

## 🎯 Recomendación RÁPIDA

**PythonAnywhere** es la opción más rápida:
- ✅ Gratis
- ✅ HTTPS automático
- ✅ Soporta Django
- ✅ 5 minutos de setup
- ✅ Funciona en móvil inmediatamente

## 📝 Nota sobre el Profe

Le puedes decir:
- ✅ "El bat funciona perfecto en local"
- ✅ "Para móvil necesitamos HTTPS (requisito de Google para PWA)"
- ✅ "PythonAnywhere es gratis y toma 5 minutos"
- ✅ "El proyecto YA tiene integración móvil (PWA), solo falta el HTTPS"

## 🔧 Si ya tienes servidor

Solo necesitas:
1. Configurar HTTPS (Let's Encrypt es gratis)
2. Asegurar que `/static/manifest.json` y `/static/sw.js` sean accesibles
3. Listo - funciona en móvil

---

**TL;DR**: Tu app YA funciona en móvil. Solo sube a PythonAnywhere (gratis, 5 min) y tendrás HTTPS. Listo.


