# Alternativas a ngrok - Problema de Ancho de Banda

## El Problema

```
ERR_NGROK_726
Network bandwidth exceeded
```

ngrok gratuito tiene límites de **transferencia de datos por mes**. Si compartes archivos grandes o hay mucho tráfico, se agota el ancho de banda.

---

## Soluciones Inmediatas

### Solución 1: Nueva Cuenta de ngrok

**Más rápido y fácil:**

1. Crea una nueva cuenta con otro email
2. Obtén nuevo authtoken
3. Configura el nuevo token:

```bash
ngrok authtoken TU_NUEVO_TOKEN
```

**Ventajas:**
- Rápido (5 minutos)
- Mismo funcionamiento
- HTTPS automático

---

### Solución 2: Tailscale (Recomendado)

**Red privada VPN sin límites:**

```bash
# Desde el launcher
iniciar_studentspoint.bat
# Opción [3] - Tailscale
```

**Instalar Tailscale:**

**Windows:**
```powershell
winget install tailscale.tailscale
```

**Linux/Mac:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

**Configurar:**
```bash
# Iniciar Tailscale
tailscale up

# Ver tu IP de Tailscale
tailscale ip
```

**En tu celular:**
1. Instala Tailscale desde Play Store o App Store
2. Inicia sesión con la misma cuenta
3. Accede a tu app con la IP de Tailscale: `http://100.x.x.x:8000`

**Ventajas:**
- Sin límites de ancho de banda
- Conexión privada y segura
- IP fija
- Funciona desde cualquier lugar
- Gratis

**Desventajas:**
- Sin HTTPS automático (necesitas certificado)
- Requiere Tailscale en todos los dispositivos

---

### Solución 3: LocalTunnel

**Alternativa gratuita a ngrok:**

**Instalar:**
```bash
npm install -g localtunnel
```

**Usar:**
```bash
# Terminal 1: Iniciar Django
cd proyecto\src\backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2: Iniciar LocalTunnel
lt --port 8000
```

**Output:**
```
your url is: https://random-name.loca.lt
```

**Ventajas:**
- Sin límites de ancho de banda
- HTTPS automático
- Gratis y open source
- Sin cuenta necesaria

**Desventajas:**
- URL cambia cada vez
- Menos estable que ngrok
- Puede ser más lento

---

### Solución 4: Cloudflare Tunnel

**Gratis y sin límites:**

**Instalar:**
```bash
# Windows
winget install --id Cloudflare.cloudflared

# Linux/Mac
brew install cloudflare/cloudflare/cloudflared
```

**Configurar:**
```bash
# Autenticar (abre navegador)
cloudflared tunnel login

# Crear túnel
cloudflared tunnel create studentspoint

# Configurar (crea config.yml)
cloudflared tunnel route dns studentspoint studentspoint.tu-dominio.com

# Iniciar
cloudflared tunnel --url http://localhost:8000
```

**Ventajas:**
- Sin límites de ancho de banda
- HTTPS automático
- Red global de Cloudflare (rápido)
- Gratis
- Dominio personalizado opcional

**Desventajas:**
- Configuración inicial más compleja
- Requiere cuenta de Cloudflare

---

### Solución 5: Pagsmile/Bore

**Simple y rápido:**

**Instalar:**
```bash
cargo install bore-cli
```

**Usar:**
```bash
bore local 8000 --to bore.pub
```

**Ventajas:**
- Muy simple
- Sin cuenta
- Open source

**Desventajas:**
- Solo HTTP (no HTTPS)
- No apto para PWA

---

## Comparación de Alternativas

| Solución | HTTPS | Límites | Setup | PWA | Recomendado |
|----------|-------|---------|-------|-----|-------------|
| Nueva cuenta ngrok | Sí | 40GB/mes | 5 min | Sí | Temporal |
| **Tailscale** | No* | Sin límites | 10 min | Sí* | **Sí** |
| LocalTunnel | Sí | Sin límites | 5 min | Sí | Sí |
| Cloudflare Tunnel | Sí | Sin límites | 20 min | Sí | Producción |
| Bore | No | Sin límites | 5 min | No | Desarrollo |

*Con certificado adicional

---

## Recomendaciones por Caso de Uso

### Para Probar PWA en Celular (Ahora)
**LocalTunnel** o **Nueva cuenta ngrok**
- Rápido de configurar
- HTTPS automático
- Funciona inmediatamente

### Para Desarrollo en Equipo
**Tailscale**
- Conexión privada
- Sin límites
- Muy estable

### Para Demos a Clientes
**Cloudflare Tunnel**
- Profesional
- Rápido globalmente
- Dominio personalizado

### Para Producción
**Servidor propio con Nginx**
- Mejor rendimiento
- Control total
- Más seguro

---

## Script Rápido: LocalTunnel

Crea un script `iniciar_con_localtunnel.bat`:

```batch
@echo off
echo Instalando LocalTunnel...
npm install -g localtunnel

echo Iniciando Django...
cd proyecto\src\backend
start "Django Server" cmd /k "python manage.py runserver 0.0.0.0:8000"

timeout /t 5

echo Iniciando LocalTunnel...
lt --port 8000

pause
```

---

## Por Qué Pasó Esto con ngrok

**Posibles causas:**

1. **Archivos grandes subidos/descargados**
   - Imágenes del marketplace
   - Documentos del conversor
   - Archivos estáticos repetidos

2. **Muchas conexiones/recargas**
   - Testing intensivo
   - Múltiples dispositivos
   - Recargas frecuentes

3. **Cuenta compartida**
   - Si Darosh usó la misma cuenta
   - El límite es global para la cuenta

**Solución:** Usar cuentas separadas o alternativas sin límites.

---

## Límites de ngrok Gratuito

- **Ancho de banda:** 1GB/mes
- **Conexiones:** 40/minuto
- **Túneles:** 1 simultáneo
- **Dominios:** Aleatorios
- **Región:** Variable

**ngrok Pro:** $8/mes
- 5GB/mes
- 120 conexiones/min
- 3 túneles
- Dominios personalizados
- Regiones fijas

---

## Conclusión

**Para reemplazar ngrok ahora:**

1. **Más fácil:** Nueva cuenta ngrok (5 min)
2. **Más estable:** Tailscale (10 min)
3. **Más versátil:** LocalTunnel (5 min)

**Recomendación:** Usa Tailscale para desarrollo, es gratis, sin límites y muy confiable.

---

## Links Útiles

- **Tailscale:** https://tailscale.com/
- **LocalTunnel:** https://theboroer.github.io/localtunnel-www/
- **Cloudflare Tunnel:** https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Bore:** https://github.com/ekzhang/bore

