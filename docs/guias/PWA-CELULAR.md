# PWA en Celular - Guía Rápida

## El Problema

Cuando intentas instalar StudentsPoint en tu celular desde Tailscale (http://100.x.x.x:8000), Chrome solo crea un "acceso directo" que se ve con bordes del navegador.

**Esto NO es una PWA real.**

### Causa

Chrome en Android **requiere HTTPS** para instalar PWAs como aplicaciones nativas. HTTP solo funciona en localhost.

---

## Solución Rápida con HTTPS

### Opción A: Script Automatizado (Recomendado)

**Paso 1:** Instala OpenSSL

```bash
# Windows
winget install ShiningLight.OpenSSL.Light

# O descarga desde:
# https://slproweb.com/products/Win32OpenSSL.html
```

**Paso 2:** Ejecuta el configurador

```bash
configurar_https.bat
```

Este script:
- Genera certificados SSL automáticamente
- Instala django-sslserver
- Crea el script iniciar_https.bat

**Paso 3:** Inicia el servidor HTTPS

```bash
iniciar_https.bat
```

**Paso 4:** En tu celular

1. Abre Chrome
2. Ve a `https://100.75.238.19:8443` (tu IP Tailscale)
3. Aparecerá advertencia de certificado
4. Toca "Avanzado" → "Continuar de todos modos"
5. Menú (⋮) → "Instalar app"
6. ¡Listo! PWA instalada correctamente

---

### Opción B: Usar ngrok (Sin configuración)

**Paso 1:** Descarga ngrok

https://ngrok.com/download

**Paso 2:** Inicia tu servidor normal

```bash
iniciar_desarrollo.bat
```

**Paso 3:** En otra terminal, ejecuta ngrok

```bash
ngrok http 8000
```

**Paso 4:** Usa la URL HTTPS que ngrok te da

Ejemplo: `https://abc123.ngrok.io`

**Paso 5:** Abre esa URL en tu celular e instala la PWA

**Ventajas:**
- HTTPS real sin configuración
- Funciona inmediatamente
- No requiere certificados

**Desventajas:**
- La URL cambia cada vez
- Requiere dejar ngrok corriendo

---

## Verificar que Funciona

### PWA Correctamente Instalada:

✅ Aparece en el cajón de aplicaciones  
✅ Ícono propio (no de Chrome)  
✅ Se abre SIN barra del navegador  
✅ Pantalla de carga al iniciar  
✅ Funciona offline  

### Solo Acceso Directo (Mal):

❌ Se abre CON barra del navegador  
❌ Muestra URL arriba  
❌ Botones de navegación visibles  
❌ No funciona offline  

---

## Resumen

**HTTP sobre Tailscale = Solo acceso directo**  
**HTTPS sobre Tailscale = PWA completa**

**Usa:**
- `configurar_https.bat` → `iniciar_https.bat` para HTTPS permanente
- O `ngrok` para HTTPS temporal

**Documentación completa:**  
`docs/guias/PWA-ANDROID-HTTPS.md`

