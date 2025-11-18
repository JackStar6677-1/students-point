# Usar ngrok - Guía Rápida

## ✅ Ya tienes ngrok configurado

Tu authtoken ya está guardado. No necesitas configurarlo de nuevo.

---

## 🚀 Ejecutar StudentsPoint con ngrok

### Paso 1: Inicia el script

```bash
iniciar_con_ngrok.bat
```

### Paso 2: Copia el enlace HTTPS

Verás algo como:

```
Forwarding    https://healthy-gnat-evolved.ngrok-free.app -> http://localhost:8000
```

Copia ese enlace (el que empieza con https://)

### Paso 3: Abre en tu celular

1. Abre Chrome en tu celular
2. Pega el enlace HTTPS
3. Haz clic en **"Visit Site"** (página de aviso de ngrok)
4. ¡Listo! Ya estás en StudentsPoint con HTTPS

### Paso 4: Instala la PWA

1. Menú (⋮) → **"Instalar app"**
2. La PWA se instalará correctamente (sin bordes del navegador)
3. Funcionará como app nativa

---

## 🎯 Ventajas de usar ngrok

✅ **HTTPS automático** - No necesitas certificados  
✅ **Acceso desde cualquier lugar** - No solo Tailscale  
✅ **PWA funciona perfecto** - Chrome reconoce como contexto seguro  
✅ **Fácil de compartir** - Envía el link a otros para probar  

---

## ⚠️ Notas Importantes

- **El enlace cambia** cada vez que reinicias ngrok
- **Página de aviso** es normal en versión gratuita (solo haz clic "Visit Site")
- **40 conexiones/minuto** en versión gratuita
- **Detén con Ctrl+C** cuando termines

---

## 📊 Ver Dashboard

Mientras ngrok está corriendo, abre:
```
http://127.0.0.1:4040
```

Verás todas las requests en tiempo real.

---

## 🆚 Comparación

### ngrok (Recomendado para pruebas):
✅ HTTPS automático  
✅ Fácil de usar  
✅ Funciona inmediatamente  
⚠️ URL cambia cada vez  

### Tailscale + HTTPS:
✅ URL fija  
✅ Sin límites  
⚠️ Requiere configuración  
⚠️ Solo red Tailscale  

---

## Documentación Completa

Lee `GUIA-NGROK.md` para más detalles.

---

**¡Eso es todo!** Ejecuta `iniciar_con_ngrok.bat` y tendrás HTTPS funcionando en segundos.

