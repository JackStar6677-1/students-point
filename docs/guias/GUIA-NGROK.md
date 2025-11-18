# Guía de ngrok para StudentsPoint

## ¿Qué es ngrok?

ngrok crea un túnel HTTPS público a tu servidor local, permitiendo:
- ✅ Probar PWA con HTTPS sin certificados
- ✅ Acceder desde cualquier dispositivo con internet
- ✅ Compartir la app temporalmente
- ✅ Testing en celular sin Tailscale

---

## Configuración Inicial (Ya Hecha)

Ya configuraste tu authtoken:
```bash
ngrok config add-authtoken 2nj4KpmQLI7tF2uhgvcjuMgWkNV_4fDDWsj3cwpBLvnaNnr9x
```

✅ Esta configuración es permanente, no necesitas repetirla.

---

## Uso Rápido

### Opción 1: Script Automatizado (Recomendado)

```bash
iniciar_con_ngrok.bat
```

Este script:
1. Inicia el servidor Django en puerto 8000
2. Inicia ngrok automáticamente
3. Te muestra el enlace HTTPS

### Opción 2: Manual

**Terminal 1 - Django:**
```bash
cd proyecto\src\backend
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - ngrok:**
```bash
ngrok http 8000
```

---

## Uso del Enlace HTTPS

ngrok te dará un enlace como:
```
https://healthy-gnat-evolved.ngrok-free.app
```

### En tu celular:

1. **Abre Chrome**
2. **Navega al enlace de ngrok**
3. **Verás una página de aviso de ngrok**
   - Haz clic en **"Visit Site"**
4. **Ahora verás StudentsPoint**
5. **Instala la PWA:**
   - Menú (⋮) → "Instalar app"
   - La PWA se instalará correctamente porque usa HTTPS

### En tu computadora:

También puedes probar en:
```
https://tu-dominio.ngrok-free.app
```

---

## Características de ngrok

### Versión Gratuita:

✅ **Incluye:**
- HTTPS automático
- 1 túnel simultáneo
- Sin límite de tiempo
- Dominio aleatorio

⚠️ **Limitaciones:**
- URL cambia cada vez que reinicias ngrok
- Página de aviso "Visit Site" antes de acceder
- 40 conexiones/minuto

### Versión de Pago:

Si necesitas:
- URL fija (custom domain)
- Sin página de aviso
- Múltiples túneles
- Más conexiones

Visita: https://ngrok.com/pricing

---

## Comandos Útiles

### Ver túneles activos:
```bash
ngrok http 8000 --log=stdout
```

### Ver dashboard web:
Cuando ngrok está corriendo, abre:
```
http://127.0.0.1:4040
```

Verás:
- Requests en tiempo real
- Headers
- Response bodies
- Tiempos de respuesta

### Detener ngrok:
```
Ctrl+C
```

---

## Configuración Django

Django ya está configurado para aceptar dominios de ngrok:

```python
# En dev.py:
ALLOWED_HOSTS = ["*"]  # Acepta cualquier dominio en desarrollo
```

Esto permite que ngrok funcione sin configuración adicional.

---

## Troubleshooting

### Problema: "Invalid Host header"

**Solución:**
Ya está corregido en `dev.py` con `ALLOWED_HOSTS = ["*"]`

### Problema: Página de aviso de ngrok

**Solución:**
Esto es normal en la versión gratuita. Simplemente haz clic en "Visit Site".

### Problema: URL cambia cada vez

**Solución:**
Esto es normal en la versión gratuita. Opciones:
1. Usar la misma sesión de ngrok sin reiniciar
2. Actualizar a plan de pago para URL fija
3. Usar Tailscale + HTTPS para URL fija gratis

### Problema: "Too many connections"

**Solución:**
Límite de 40 conexiones/minuto en versión gratuita.
Espera 1 minuto o actualiza a plan de pago.

---

## Comparación: ngrok vs Tailscale

| Característica | ngrok (Gratis) | Tailscale + HTTPS |
|----------------|----------------|-------------------|
| HTTPS | ✅ Automático | ⚠️ Requiere certificado |
| URL Fija | ❌ Cambia | ✅ Fija |
| Configuración | ✅ Fácil | ⚠️ Media |
| Acceso público | ✅ Cualquiera | ❌ Solo red Tailscale |
| Velocidad | ⚠️ Túnel | ✅ Directa |
| Límites | ⚠️ 40 conn/min | ✅ Sin límites |

**Recomendación:**
- **ngrok:** Para pruebas rápidas y demos
- **Tailscale + HTTPS:** Para uso diario

---

## Testing de PWA con ngrok

### Checklist:

1. **Inicia ngrok:**
   ```bash
   iniciar_con_ngrok.bat
   ```

2. **Copia el enlace HTTPS**
   Ejemplo: `https://abc123.ngrok-free.app`

3. **Abre en celular**
   - Chrome Android/iOS
   - Toca "Visit Site" en página de aviso

4. **Verifica contexto seguro:**
   - F12 → Console (remoto)
   - `window.isSecureContext` debe ser `true`

5. **Verifica Service Worker:**
   - DevTools → Application → Service Workers
   - Debe aparecer registrado

6. **Instala PWA:**
   - Menú → "Instalar app"
   - Debe instalarse en modo standalone

7. **Verifica funcionamiento:**
   - Sin barra del navegador
   - Splash screen
   - Funciona offline

---

## Scripts Disponibles

### iniciar_con_ngrok.bat
```bash
# Inicia Django y ngrok automáticamente
iniciar_con_ngrok.bat
```

### iniciar_desarrollo.bat
```bash
# Inicia Django normal (HTTP local)
iniciar_desarrollo.bat
```

### iniciar_https.bat
```bash
# Inicia Django con HTTPS self-signed (Tailscale)
iniciar_https.bat
```

---

## Seguridad

### En Desarrollo:

⚠️ **IMPORTANTE:**
- ngrok expone tu servidor local a internet
- Solo usar en desarrollo
- No exponer datos sensibles
- Detener cuando no uses

### Para Producción:

Usa un servidor real con:
- Certificado SSL válido
- Dominio propio
- Firewall configurado
- HTTPS obligatorio

---

## Recursos

- **ngrok Docs:** https://ngrok.com/docs
- **Dashboard:** https://dashboard.ngrok.com/
- **Status:** https://status.ngrok.com/
- **Community:** https://github.com/inconshreveable/ngrok/discussions

---

## Ejemplo de Uso Completo

```bash
# 1. Inicia el servidor con ngrok
iniciar_con_ngrok.bat

# 2. Verás algo como:
#    ngrok by @inconshreveable
#    
#    Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
#    
#    Web Interface http://127.0.0.1:4040

# 3. Copia el enlace HTTPS:
#    https://abc123.ngrok-free.app

# 4. Abre en tu celular

# 5. Haz clic en "Visit Site"

# 6. ¡Listo! Ahora puedes instalar la PWA

# 7. Para detener: Ctrl+C
```

---

## Notas Importantes

1. **El enlace cambia:** Cada vez que reinicias ngrok, obtienes un nuevo dominio
2. **Página de aviso:** Es normal, solo haz clic en "Visit Site"
3. **Sin límite de tiempo:** Puedes dejar ngrok corriendo todo el día
4. **Dashboard útil:** http://127.0.0.1:4040 muestra todas las requests
5. **Gratis para siempre:** No necesitas pagar para uso básico

---

**¿Preguntas?** Consulta la documentación completa en https://ngrok.com/docs

