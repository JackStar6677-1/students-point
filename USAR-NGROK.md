# Usar ngrok - Guía Rápida

## ✅ Ya tienes ngrok configurado

Tu authtoken ya está guardado. No necesitas configurarlo de nuevo.

---

## 🚀 Ejecutar StudentsPoint con ngrok

### Opción 1: Script Automático (Recomendado)

**Paso 1: Inicia el script**

```bash
iniciar_con_ngrok.bat
```

Este script:
- Inicia Django en una ventana separada
- Espera a que Django esté listo
- Inicia ngrok automáticamente

**Paso 2: Verás 2 ventanas**

1. **Ventana "Django Server - NO CERRAR"** - Déjala abierta
2. **Ventana de ngrok** - Aquí verás el enlace HTTPS

**Paso 3: Copia el enlace HTTPS**

En la ventana de ngrok verás algo como:

```
Forwarding    https://healthy-gnat-evolved.ngrok-free.app -> http://localhost:8000
```

Copia ese enlace (el que empieza con https://)

### Opción 2: Script Manual (Si ya tienes Django corriendo)

Si Django ya está corriendo en puerto 8000:

```bash
scripts\iniciar_solo_ngrok.bat
```

Este script solo inicia ngrok y verifica que Django esté corriendo.

### Paso 4: Abre en tu celular

1. Abre Chrome en tu celular
2. Pega el enlace HTTPS
3. Haz clic en **"Visit Site"** (página de aviso de ngrok)
4. ¡Listo! Ya estás en StudentsPoint con HTTPS

### Paso 5: Instala la PWA

1. Menú (⋮) → **"Instalar app"**
2. La PWA se instalará correctamente (sin bordes del navegador)
3. Funcionará como app nativa

---

## ⚠️ Solución de Problemas

### Error: "ERR_NGROK_8012"

**Causa:** Django no está corriendo en puerto 8000

**Solución:**

1. **Verifica la ventana de Django**
   - Debe existir una ventana "Django Server - NO CERRAR"
   - Debe mostrar "Starting development server at http://0.0.0.0:8000/"
   - Si no existe o está cerrada, reinicia el script

2. **Verifica manualmente que Django funcione:**
   ```bash
   # En un navegador, abre:
   http://localhost:8000
   ```
   Si ves StudentsPoint, Django está corriendo correctamente.

3. **Si Django no inicia:**
   - Cierra todas las ventanas
   - Ejecuta primero: `iniciar_desarrollo.bat`
   - Luego ejecuta: `scripts\iniciar_solo_ngrok.bat`

4. **Puerto ocupado:**
   - Si el puerto 8000 está en uso por otro programa:
   ```bash
   # Ver qué está usando el puerto 8000:
   netstat -ano | findstr :8000
   ```

### Django no responde

**Si ves el error pero Django parece estar corriendo:**

1. Espera 15-20 segundos más (Django puede tardar en iniciar)
2. Detén ngrok (Ctrl+C)
3. Verifica en el navegador: http://localhost:8000
4. Si funciona, vuelve a ejecutar solo ngrok:
   ```bash
   scripts\iniciar_solo_ngrok.bat
   ```

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

