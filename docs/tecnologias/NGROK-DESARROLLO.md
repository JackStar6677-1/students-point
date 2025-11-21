# 🌐 ngrok en Desarrollo - StudentsPoint

## 📋 Resumen Ejecutivo

ngrok es un **servicio de túnel reverso** que permite exponer tu servidor local (localhost) a internet de forma segura mediante un endpoint HTTPS público. En StudentsPoint lo utilizamos para probar la PWA en dispositivos móviles durante el desarrollo, ya que las PWA requieren HTTPS para funcionar correctamente.

---

## 🎯 ¿Qué es ngrok?

### Definición Simple

ngrok crea un **túnel seguro** desde internet hasta tu computadora, permitiendo que cualquier persona acceda a tu aplicación local mediante una URL pública con HTTPS.

```
┌─────────────────────────────────────────────────────────┐
│                   ¿QUÉ ES NGROK?                        │
└─────────────────────────────────────────────────────────┘

Tu Computadora (localhost:8000)
        ↓ Túnel cifrado
Servidores de ngrok.com
        ↓ URL pública
https://abc123.ngrok-free.app
        ↓
Accesible desde cualquier dispositivo
```

### ¿Qué NO es ngrok?

- ❌ No es un servidor web (como Nginx)
- ❌ No es un servidor de aplicaciones (como Gunicorn)
- ❌ No es un hosting
- ❌ No reemplaza ningún componente de tu stack

ngrok es simplemente un **túnel** que conecta tu localhost con internet.

---

## 🔧 Stack de Desarrollo con ngrok

### Arquitectura Completa

```
┌─────────────────────────────────────────────────────────────┐
│                CLIENTE (Navegador/Móvil)                    │
│  - Chrome, Firefox, Safari                                  │
│  - Android, iOS                                             │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTPS Request
                   │ https://abc123.ngrok-free.app
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                  INTERNET (Cloud)                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            Servidores de ngrok.com                    │  │
│  │  - Reciben requests HTTPS                             │  │
│  │  - Enrutan a través del túnel                        │  │
│  │  - Proveen certificado SSL válido                    │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────────┘
                   │ Túnel cifrado (protocolo propietario)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│              TU COMPUTADORA (Localhost)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ngrok Agent (Puerto 4040 para dashboard)            │  │
│  │  - Mantiene conexión con ngrok.com                   │  │
│  │  - Reenvía requests a localhost:8000                 │  │
│  └──────────────┬────────────────────────────────────────┘  │
│                 │ HTTP (local)                              │
│  ┌──────────────▼────────────────────────────────────────┐  │
│  │  Django Development Server (runserver)               │  │
│  │  - Puerto: 8000                                      │  │
│  │  - Single-threaded                                   │  │
│  │  - Auto-reload habilitado                            │  │
│  │  - DEBUG=True                                        │  │
│  └──────────────┬────────────────────────────────────────┘  │
│                 │                                           │
│  ┌──────────────▼────────────────────────────────────────┐  │
│  │  SQLite Database (db.sqlite3)                        │  │
│  │  - Base de datos local                               │  │
│  │  - Archivo único                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 ¿Por Qué Usar ngrok?

### Problema: PWA Requiere HTTPS

Las Progressive Web Apps (PWA) tienen requisitos estrictos:

```
❌ SIN ngrok:
http://localhost:8000
├─→ Service Workers NO funcionan
├─→ Push Notifications NO funcionan
├─→ Install prompt NO aparece
└─→ "Add to Home Screen" NO disponible

✅ CON ngrok:
https://abc123.ngrok-free.app
├─→ Service Workers ✓
├─→ Push Notifications ✓
├─→ Install prompt ✓
└─→ "Add to Home Screen" ✓
```

### Ventajas de ngrok

| Ventaja | Descripción | Impacto |
|---------|-------------|---------|
| **HTTPS Instantáneo** | Sin configurar certificados SSL | ⚡ Inmediato |
| **Sin configuración** | No necesitas Nginx, Let's Encrypt, etc. | 🎯 Simple |
| **Acceso móvil** | Prueba en celular sin estar en misma WiFi | 📱 Flexible |
| **Compartir demos** | Envía link a cliente/equipo | 🤝 Colaborativo |
| **Inspector integrado** | Dashboard para ver requests | 🔍 Debug fácil |
| **Gratis** | Plan gratuito suficiente para desarrollo | 💰 Económico |

---

## 📦 Instalación de ngrok

### Windows

#### Opción 1: Con winget (Recomendado)

```powershell
winget install ngrok
```

#### Opción 2: Descarga Manual

1. Descarga desde: https://ngrok.com/download
2. Descomprime el archivo
3. Mueve `ngrok.exe` a una carpeta en PATH

**Verificar instalación:**

```bash
ngrok version
# Output: ngrok version 3.x.x
```

### Linux/Mac

```bash
# Homebrew (Mac)
brew install ngrok/ngrok/ngrok

# Snap (Linux)
snap install ngrok

# Manual (Linux/Mac)
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

---

## 🔑 Configuración Inicial

### 1. Crear Cuenta en ngrok

1. Visita: https://dashboard.ngrok.com/signup
2. Regístrate con Google o email
3. Verifica tu email

### 2. Obtener Auth Token

1. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copia tu authtoken (algo como: `2abc...xyz`)

### 3. Configurar Token

```bash
ngrok config add-authtoken TU_TOKEN_AQUI
```

**Ejemplo:**

```bash
ngrok config add-authtoken 2abc123def456ghi789jkl
```

**Verificar configuración:**

```bash
# El archivo de config se guarda en:
# Windows: C:\Users\TU_USUARIO\.ngrok2\ngrok.yml
# Linux/Mac: ~/.ngrok2/ngrok.yml

# Ver contenido:
cat ~/.ngrok2/ngrok.yml
```

✅ **Solo necesitas hacerlo UNA VEZ**

---

## 🎮 Uso en StudentsPoint

### Método 1: Script Automático (Recomendado)

```bash
# Ejecutar desde la raíz del proyecto
scripts\iniciar_con_ngrok.bat
```

**Lo que hace el script:**

```batch
1. Verifica que ngrok esté instalado
2. Navega a proyecto/src/backend
3. Instala/actualiza dependencias Python
4. Aplica migraciones de base de datos
5. Recolecta archivos estáticos
6. Inicia Django en ventana separada (puerto 8000)
7. Espera 10 segundos a que Django esté listo
8. Inicia ngrok apuntando al puerto 8000
```

**Resultado:**

```
Ventana 1: Django Server - NO CERRAR
Starting development server at http://0.0.0.0:8000/
Watching for file changes with StatReloader
...

Ventana 2: ngrok
ngrok                                                                                                            

Session Status                online                                                                            
Account                       tu_email@ejemplo.com (Plan: Free)                                                
Version                       3.5.0                                                                            
Region                        United States (us)                                                               
Latency                       45ms                                                                             
Web Interface                 http://127.0.0.1:4040                                                            
Forwarding                    https://healthy-gnat-evolved.ngrok-free.app -> http://localhost:8000           

Connections                   ttl     opn     rt1     rt5     p50     p90                                      
                              0       0       0.00    0.00    0.00    0.00                                     
```

### Método 2: Script Manual

**Si Django ya está corriendo:**

```bash
scripts\iniciar_solo_ngrok.bat
```

Este script:
- Verifica que Django esté en puerto 8000
- Solo inicia el túnel ngrok
- Útil para reiniciar ngrok sin reiniciar Django

### Método 3: Manual Completo

```bash
# Terminal 1: Iniciar Django
cd proyecto/src/backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2: Iniciar ngrok
ngrok http 8000
```

---

## 🔍 Dashboard de ngrok

### Acceder al Inspector Web

Mientras ngrok está corriendo, abre en tu navegador:

```
http://localhost:4040
```

o

```
http://127.0.0.1:4040
```

### Funciones del Dashboard

```
┌─────────────────────────────────────────┐
│         ngrok Web Inspector             │
├─────────────────────────────────────────┤
│  Status:    Online                      │
│  Requests:  15                          │
│  Duration:  00:23:45                    │
├─────────────────────────────────────────┤
│  REQUESTS:                              │
│  ┌─────────────────────────────────┐   │
│  │ GET /api/auth/me/      200      │   │
│  │ POST /api/auth/login/  200      │   │
│  │ GET /static/css/...    200      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Información que puedes ver:**

1. **Lista de Requests**
   - Método HTTP (GET, POST, etc.)
   - URL completa
   - Status code
   - Tiempo de respuesta

2. **Detalles de Request**
   - Headers completos
   - Query parameters
   - Body (JSON, form data)
   - Cookies

3. **Detalles de Response**
   - Status code
   - Headers
   - Body completo
   - Tiempo de procesamiento

4. **Replay de Requests**
   - Re-ejecutar cualquier request
   - Modificar parámetros
   - Testing manual fácil

---

## 📱 Uso en Dispositivos Móviles

### Flujo Completo para Probar PWA

#### 1. Iniciar ngrok

```bash
scripts\iniciar_con_ngrok.bat
```

#### 2. Copiar URL HTTPS

En la terminal de ngrok, busca la línea:

```
Forwarding    https://healthy-gnat-evolved.ngrok-free.app -> http://localhost:8000
```

Copia la URL: `https://healthy-gnat-evolved.ngrok-free.app`

#### 3. Abrir en Celular

**Android (Chrome):**

1. Abre Chrome
2. Pega la URL
3. Verás página de aviso de ngrok: **"You are about to visit..."**
4. Click en **"Visit Site"**
5. Ya estás en StudentsPoint con HTTPS

**iOS (Safari):**

1. Abre Safari
2. Pega la URL
3. Click en "Visit Site" si aparece aviso
4. Ya estás en StudentsPoint

#### 4. Instalar PWA

**Android:**

```
1. Chrome → Menú (⋮) → "Instalar app"
2. Confirma instalación
3. Icono aparece en home screen
4. Abre como app nativa
```

**iOS:**

```
1. Safari → Compartir (□↑) → "Agregar a pantalla de inicio"
2. Edita nombre si quieres
3. Añadir
4. Icono aparece en home screen
```

#### 5. Probar Funcionalidades PWA

```
✓ App instalada sin bordes de navegador
✓ Service Worker registrado
✓ Funciona offline (después de primera visita)
✓ Push notifications (si las configuras)
✓ Add to home screen funcionó
✓ Se ve como app nativa
```

---

## ⚙️ Configuración Avanzada

### Archivo de Configuración

**Ubicación:** `~/.ngrok2/ngrok.yml`

```yaml
version: "2"
authtoken: TU_TOKEN_AQUI
region: us
console_ui: true
console_ui_color: transparent
tunnels:
  studentspoint:
    proto: http
    addr: 8000
    inspect: true
    bind_tls: true
```

### Múltiples Túneles

```yaml
tunnels:
  django:
    proto: http
    addr: 8000
  redis:
    proto: tcp
    addr: 6379
```

**Iniciar múltiples:**

```bash
ngrok start django redis
```

### Subdominios Personalizados (Plan Pago)

```yaml
tunnels:
  studentspoint:
    proto: http
    addr: 8000
    subdomain: mi-proyecto  # Requiere plan pago
    # URL fija: https://mi-proyecto.ngrok.io
```

### Autenticación Básica

```yaml
tunnels:
  studentspoint:
    proto: http
    addr: 8000
    auth: "usuario:contraseña"
```

---

## 🔒 Seguridad

### Consideraciones Importantes

#### ✅ Seguro para Desarrollo

- Túnel está cifrado end-to-end
- Solo tú puedes crear túneles a tu máquina
- Auth token es privado
- Conexiones son efímeras

#### ⚠️ No para Producción

```
❌ NO uses ngrok para:
- Sitios en producción permanente
- Datos sensibles de usuarios reales
- Alta disponibilidad
- Performance crítico
```

#### 🛡️ Mejores Prácticas

1. **No compartas el authtoken**
   ```bash
   # Mantén privado tu ~/.ngrok2/ngrok.yml
   echo ".ngrok2" >> .gitignore
   ```

2. **URLs son públicas**
   ```
   Cualquiera con la URL puede acceder
   → Usa auth básica si compartes
   → O usa IP whitelisting (plan pago)
   ```

3. **Monitorea el dashboard**
   ```
   Revisa http://localhost:4040
   → Ve quién accede
   → Detecta requests sospechosos
   ```

4. **Cierra túneles al terminar**
   ```bash
   # Presiona Ctrl+C para detener
   # Túnel se cierra automáticamente
   ```

---

## 📊 Planes y Límites

### Plan Free (Actual)

```
✅ Características Incluidas:
- HTTPS automático
- Túneles TCP/HTTP
- Dashboard web
- 1 túnel simultáneo
- 40 conexiones por minuto
- URLs aleatorias (cambian cada reinicio)
- Página de aviso antes de entrar

⚠️ Limitaciones:
- Sin subdominios personalizados
- Sin IP whitelisting
- Sin múltiples túneles simultáneos
- 8 horas máximo de sesión
```

### Plan Personal ($8/mes)

```
✅ Mejoras sobre Free:
- 3 túneles simultáneos
- Subdominios personalizados
- Sin página de aviso
- 60 conexiones por minuto
- Sesiones ilimitadas
```

### Plan Pro ($12/mes)

```
✅ Mejoras sobre Personal:
- 10 túneles simultáneos
- IP whitelisting
- Autenticación básica
- 120 conexiones por minuto
- Custom domains
```

### ¿Vale la Pena Pagar?

**Para desarrollo en StudentsPoint: NO**

```
Plan Free es suficiente porque:
✓ Solo necesitas 1 túnel
✓ 40 conexiones/min es suficiente para testing
✓ URL aleatoria no es problema en desarrollo
✓ Página de aviso no molesta (solo 1 click)
```

**Considera pagar si:**
- Necesitas URL fija para demos a clientes
- Quieres subdominios personalizados
- Necesitas múltiples túneles (ej: API + Frontend)

---

## 🐛 Solución de Problemas

### Error: "ERR_NGROK_8012"

**Mensaje:**
```
The connection to http://localhost:8000 was successfully tunneled to your ngrok client, 
but the client itself is having trouble establishing a connection to the local address.
```

**Causa:** Django no está corriendo en puerto 8000

**Solución:**

```bash
# 1. Verifica que Django esté corriendo
netstat -ano | findstr :8000

# 2. Si no hay salida, inicia Django:
cd proyecto/src/backend
python manage.py runserver 0.0.0.0:8000

# 3. En otra terminal, inicia ngrok:
ngrok http 8000
```

### Error: "Invalid credentials"

**Causa:** Auth token no configurado o inválido

**Solución:**

```bash
# Reconfigurar token
ngrok config add-authtoken TU_TOKEN_NUEVO

# Verificar
cat ~/.ngrok2/ngrok.yml
```

### Error: "Account limit exceeded"

**Causa:** Excediste el límite de conexiones (40/min en free)

**Solución:**

```
1. Espera 1 minuto
2. Reduce requests automáticos (polling, etc.)
3. Considera upgrade a plan Personal
```

### Puerto 8000 Ocupado

**Síntoma:** Django no inicia porque puerto está en uso

**Solución:**

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID NUMERO_PID /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### ngrok No Responde

**Síntomas:**
- ngrok se queda colgado
- No aparece URL
- Sin output

**Solución:**

```bash
# 1. Cerrar todos los procesos ngrok
taskkill /IM ngrok.exe /F  # Windows
killall ngrok  # Linux/Mac

# 2. Verificar conexión a internet
ping ngrok.com

# 3. Reiniciar ngrok
ngrok http 8000
```

### Página de Aviso Molesta

**Síntoma:** Siempre aparece "You are about to visit..."

**Causa:** Plan gratuito

**Soluciones:**

```
Opción 1: Hacer click "Visit Site" (1 segundo)
Opción 2: Upgrade a plan Personal ($8/mes)
Opción 3: Usar alternativa como localtunnel
```

### Tunnel Cerrado Inesperadamente

**Causa:** Sesión expiró (8 horas en plan free)

**Solución:**

```bash
# Simplemente reinicia
ngrok http 8000
# Nueva URL se generará
```

---

## 🆚 Alternativas a ngrok

### Comparación de Opciones

| Herramienta | HTTPS | Free | URL Fija | Límites | Recomendado Para |
|-------------|-------|------|----------|---------|------------------|
| **ngrok** | ✅ | ✅ | ❌* | 40/min | PWA, demos, compartir |
| **localtunnel** | ✅ | ✅ | ❌ | Sin límite | Testing rápido |
| **Tailscale** | ⚠️** | ✅ | ✅ | Sin límite | Trabajo remoto, equipo |
| **serveo** | ✅ | ✅ | ❌ | Moderado | SSH tunneling |
| **Cloudflare Tunnel** | ✅ | ✅ | ✅ | Sin límite | Producción ligera |
| **playit.gg** | ❌ | ✅ | ✅ | Sin límite | Gaming, HTTP sin SSL |

**Notas:**
- *ngrok: URL fija solo en plan pago
- **Tailscale: HTTPS requiere configuración adicional

### Cuándo Usar Cada Una

```
✅ ngrok: Tu opción principal
- Instalación fácil
- HTTPS automático
- Dashboard útil
- Plan free suficiente

✅ localtunnel: Alternativa rápida
npm install -g localtunnel
lt --port 8000

✅ Tailscale: Para trabajo en equipo
- Red privada entre dispositivos
- Sin exponer a internet público
- Requiere Tailscale en todos los dispositivos

✅ Cloudflare Tunnel: Para semi-producción
- Gratis e ilimitado
- Integración con Cloudflare
- Más complejo de configurar
```

---

## 📈 Mejores Prácticas

### 1. Desarrollo Local Normal

```bash
# Para trabajo diario:
scripts\iniciar_desarrollo.bat

# ngrok solo cuando necesites:
- Probar en celular
- Compartir con cliente
- Testing de PWA
```

### 2. Naming de Túneles

```yaml
# ~/.ngrok2/ngrok.yml
tunnels:
  studentspoint-dev:
    proto: http
    addr: 8000
  studentspoint-api:
    proto: http
    addr: 8001
```

### 3. Logging

```bash
# Guardar logs de ngrok
ngrok http 8000 --log=stdout > ngrok.log

# Ver en tiempo real
tail -f ngrok.log
```

### 4. Environment Variables

```bash
# .env
NGROK_AUTHTOKEN=tu_token_aqui
NGROK_REGION=us

# Usar en scripts
ngrok authtoken $NGROK_AUTHTOKEN
```

### 5. Testing Automatizado

```python
# test_with_ngrok.py
import subprocess
import time
import requests

def test_with_ngrok():
    # Iniciar ngrok
    ngrok = subprocess.Popen(['ngrok', 'http', '8000'])
    time.sleep(5)
    
    # Obtener URL pública
    tunnels = requests.get('http://localhost:4040/api/tunnels').json()
    public_url = tunnels['tunnels'][0]['public_url']
    
    # Hacer tests
    response = requests.get(f'{public_url}/api/health/')
    assert response.status_code == 200
    
    # Cerrar ngrok
    ngrok.terminate()
```

---

## 🎓 Tutoriales Rápidos

### Tutorial 1: Primera Vez con ngrok

```bash
# 1. Instalar ngrok
winget install ngrok

# 2. Obtener token de https://dashboard.ngrok.com
ngrok config add-authtoken TU_TOKEN

# 3. Iniciar Django
cd proyecto/src/backend
python manage.py runserver 0.0.0.0:8000

# 4. En otra terminal, iniciar ngrok
ngrok http 8000

# 5. Copiar URL HTTPS y abrir en celular
# https://abc123.ngrok-free.app

# ¡Listo! 🎉
```

### Tutorial 2: Instalar PWA en Celular

```bash
# 1. Inicia el script automático
scripts\iniciar_con_ngrok.bat

# 2. Espera a ver la URL:
Forwarding  https://xxx.ngrok-free.app

# 3. En tu celular:
- Abre Chrome
- Pega la URL
- Click "Visit Site"
- Menú (⋮) → "Instalar app"

# 4. PWA instalada como app nativa ✅
```

### Tutorial 3: Compartir Demo con Cliente

```bash
# 1. Inicia ngrok
scripts\iniciar_con_ngrok.bat

# 2. Copia la URL
https://abc123.ngrok-free.app

# 3. Envía por email/WhatsApp al cliente

# 4. Cliente abre, hace click en "Visit Site"

# 5. Cliente ve tu aplicación en vivo

# Nota: URL cambia cada reinicio
# Para URL fija, considera plan pago o Cloudflare Tunnel
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **ngrok Docs**: https://ngrok.com/docs
- **API Reference**: https://ngrok.com/docs/api
- **Dashboard**: https://dashboard.ngrok.com

### Scripts del Proyecto

```
scripts/
├── iniciar_con_ngrok.bat        # Inicia Django + ngrok
├── iniciar_solo_ngrok.bat       # Solo ngrok
└── README.md                     # Documentación de scripts
```

### Documentación Relacionada

```
docs/
├── guias/
│   ├── USAR-NGROK.md           # Guía rápida
│   └── LAUNCHER.md             # Menú de opciones
└── tecnologias/
    ├── STACK-TECNOLOGICO-COMPLETO.md
    └── NGROK-DESARROLLO.md     # Este documento
```

---

## ✅ Checklist de ngrok

### Configuración Inicial
- [ ] ngrok instalado (`ngrok version`)
- [ ] Cuenta creada en https://dashboard.ngrok.com
- [ ] Auth token configurado
- [ ] Primer túnel funcionando

### Uso Diario
- [ ] Django corriendo en puerto 8000
- [ ] ngrok apuntando al puerto correcto
- [ ] URL pública accesible
- [ ] Dashboard http://localhost:4040 funcionando

### Testing PWA
- [ ] URL HTTPS copiada
- [ ] Abierta en celular
- [ ] "Visit Site" clickeado
- [ ] PWA instala correctamente
- [ ] Service Worker registrado
- [ ] Funcionalidad offline comprobada

---

## 🎯 Resumen

### ¿Qué es ngrok?
Túnel que expone localhost a internet con HTTPS automático.

### ¿Cuándo usarlo?
- Probar PWA en celular
- Compartir demos
- Testing de HTTPS

### ¿Cómo usarlo en StudentsPoint?
```bash
scripts\iniciar_con_ngrok.bat
```

### ¿Es necesario en producción?
No. En producción usas Nginx + Gunicorn + Let's Encrypt.

### ¿Es gratis?
Sí, plan free es suficiente para desarrollo.

---

**Última actualización**: Noviembre 2025  
**ngrok Version**: 3.x  
**Estado**: ✅ Activo en desarrollo de StudentsPoint

