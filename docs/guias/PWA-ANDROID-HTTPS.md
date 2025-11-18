# PWA en Android - Solución HTTPS

## Problema Identificado

Chrome en Android **requiere HTTPS** para instalar PWAs como aplicaciones nativas. HTTP solo funciona en `localhost` o `127.0.0.1`.

### Síntomas:
- ❌ La app se agrega como "acceso directo"
- ❌ Se ve con bordes del navegador
- ❌ No funciona como app independiente
- ❌ No aparece en el cajón de aplicaciones

### Causa:
Chrome en Android NO considera las IPs de Tailscale (100.x.x.x) como "contexto seguro" cuando se usa HTTP.

---

## Soluciones Disponibles

### Opción 1: HTTPS con Certificado Self-Signed (Recomendado)

Esta es la solución más limpia y funcional.

#### Paso 1: Generar Certificado

En tu servidor (donde corre StudentsPoint):

```bash
# Instalar openssl si no lo tienes
# Windows: descargar desde https://slproweb.com/products/Win32OpenSSL.html

# Generar certificado
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=100.75.238.19"
```

Esto creará:
- `cert.pem` - Certificado
- `key.pem` - Llave privada

#### Paso 2: Configurar Django para HTTPS

Crear archivo `proyecto/src/backend/run_https.py`:

```python
#!/usr/bin/env python
"""
Servidor HTTPS para desarrollo con Tailscale
"""
import os
import sys
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings.dev')

import django
django.setup()

from django.core.management import execute_from_command_line

# Rutas a los certificados
BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / 'cert.pem'
KEY_FILE = BASE_DIR / 'key.pem'

if not CERT_FILE.exists() or not KEY_FILE.exists():
    print("ERROR: Certificados no encontrados")
    print(f"Genera certificados con:")
    print(f"  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes")
    sys.exit(1)

# Ejecutar servidor HTTPS
sys.argv = [
    'manage.py',
    'runsslserver',
    '0.0.0.0:8443',
    '--certificate', str(CERT_FILE),
    '--key', str(KEY_FILE)
]

execute_from_command_line(sys.argv)
```

#### Paso 3: Instalar django-sslserver

```bash
cd proyecto\src\backend
pip install django-sslserver
```

Agregar a `INSTALLED_APPS` en `settings/dev.py`:

```python
INSTALLED_APPS = [
    # ... apps existentes ...
    'sslserver',  # Para HTTPS en desarrollo
]
```

#### Paso 4: Crear Script de Inicio HTTPS

Crear `iniciar_https.bat`:

```batch
@echo off
chcp 65001 >nul
title StudentsPoint - HTTPS
color 0A

cd /d "%~dp0proyecto\src\backend"

echo ============================================================
echo    StudentsPoint - Servidor HTTPS (PWA Android)
echo ============================================================
echo.

if not exist cert.pem (
    echo [ERROR] Certificado no encontrado
    echo.
    echo Genera el certificado con:
    echo   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=100.75.238.19"
    echo.
    pause
    exit /b 1
)

echo [OK] Certificados encontrados
echo.

python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput >nul 2>&1

echo.
echo ============================================================
echo SERVIDOR HTTPS INICIADO
echo ============================================================
echo.
echo IMPORTANTE: Primera vez en el celular:
echo   1. Navega a https://100.75.238.19:8443
echo   2. Acepta el certificado self-signed (Avanzado -^> Continuar)
echo   3. Ahora podras instalar la PWA
echo.
echo URLs:
echo   HTTPS: https://100.75.238.19:8443
echo   Admin: https://100.75.238.19:8443/admin/
echo.
echo Credenciales: admin@studentspoint.app / admin123
echo.
echo Presiona Ctrl+C para detener
echo.

timeout /t 3 /nobreak >nul

python manage.py runsslserver 0.0.0.0:8443 --certificate cert.pem --key key.pem

pause
```

#### Paso 5: Configurar Tailscale

En `dev.py`:

```python
ALLOWED_HOSTS = [
    # ... hosts existentes ...
]

# Para HTTPS
SECURE_PROXY_SSL_HEADER = None  # Desactivar en desarrollo
SECURE_SSL_REDIRECT = False  # No forzar HTTPS
SESSION_COOKIE_SECURE = False  # Cookies en HTTP/HTTPS
CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    # ... orígenes existentes ...
    "https://100.75.238.19:8443",  # HTTPS Tailscale
    "https://100.113.204.115:8443",
]
```

#### Paso 6: Usar en Android

1. **En la laptop/desktop:**
   ```bash
   iniciar_https.bat
   ```

2. **En el celular:**
   - Abre Chrome
   - Navega a `https://100.75.238.19:8443`
   - Aparecerá advertencia de certificado
   - Toca "Avanzado" → "Continuar de todos modos"
   - **Ahora podrás instalar la PWA**
   - Menú (⋮) → "Instalar app" o "Agregar a pantalla de inicio"
   - La app se instalará en modo standalone

---

### Opción 2: Chrome Flags (Temporal, Solo Para Pruebas)

**ADVERTENCIA:** Esto es INSEGURO y solo para pruebas.

1. En Chrome Android, navega a:
   ```
   chrome://flags
   ```

2. Busca: `Insecure origins treated as secure`

3. Agrega:
   ```
   http://100.75.238.19:8000
   ```

4. Reinicia Chrome

5. Ahora la PWA debería instalarse correctamente

**Nota:** Esto solo funciona en tu Chrome, no en el de otros usuarios.

---

### Opción 3: Túnel HTTPS Gratuito (ngrok/Cloudflare Tunnel)

#### Usando ngrok:

1. **Instala ngrok:**
   ```bash
   # Descargar desde https://ngrok.com/download
   ```

2. **Ejecuta el servidor local:**
   ```bash
   iniciar_desarrollo.bat
   ```

3. **Crea túnel HTTPS:**
   ```bash
   ngrok http 8000
   ```

4. **Usa la URL HTTPS generada:**
   ```
   https://abc123.ngrok.io
   ```

5. **Instala PWA desde la URL de ngrok**

**Ventajas:**
- ✅ HTTPS real
- ✅ Funciona en cualquier dispositivo
- ✅ No requiere certificados

**Desventajas:**
- ❌ URL cambia cada vez
- ❌ Requiere conexión a internet
- ❌ Versión gratuita tiene límites

---

## Verificar que Funciona

### En el Celular:

1. **Abre la URL HTTPS**
2. **Abre DevTools Remoto:**
   - En la computadora: `chrome://inspect`
   - En el celular: Habilita "Depuración USB"
   - Conecta el celular por USB

3. **En la consola del celular, ejecuta:**
   ```javascript
   window.isSecureContext
   // Debe devolver: true
   
   navigator.serviceWorker.getRegistrations().then(regs => {
       console.log('Service Workers:', regs.length);
   });
   // Debe mostrar: Service Workers: 1
   
   window.matchMedia('(display-mode: standalone)').matches
   // Después de instalar, debe devolver: true
   ```

---

## Instalación Correcta vs Incorrecta

### ✅ PWA Instalada Correctamente:
- Aparece en el cajón de aplicaciones
- Ícono propio (no ícono de Chrome)
- Se abre SIN barra del navegador
- Se abre SIN botones de navegación
- Splash screen al iniciar
- Funciona offline

### ❌ Solo Acceso Directo:
- Aparece como marcador
- Ícono genérico o de Chrome
- Se abre CON barra del navegador
- Se abre CON botones de navegación
- No hay splash screen
- No funciona offline

---

## Recomendación Final

**Para desarrollo diario con PWA en celular:**

1. Usa **Opción 1 (HTTPS con certificado)** - La más robusta
2. Genera certificados una vez
3. Usa `iniciar_https.bat`
4. Acepta el certificado en el celular la primera vez
5. PWA funcionará perfectamente

**Para demostración rápida:**

1. Usa **Opción 3 (ngrok)** - La más fácil
2. No requiere configuración
3. HTTPS real
4. Funciona inmediatamente

---

## Script de Diagnóstico Móvil

Cuando abras la app en el celular, abre la consola remota y ejecuta:

```javascript
// Diagnóstico completo PWA
const diagnostico = {
    contextoSeguro: window.isSecureContext,
    protocol: window.location.protocol,
    hostname: window.location.hostname,
    serviceWorkerSupport: 'serviceWorker' in navigator,
    standalone: window.matchMedia('(display-mode: standalone)').matches,
    instalado: window.matchMedia('(display-mode: standalone)').matches || 
               window.navigator.standalone === true
};

console.table(diagnostico);

// Ver Service Workers
navigator.serviceWorker.getRegistrations().then(regs => {
    console.log('Service Workers registrados:', regs.length);
    regs.forEach(reg => console.log('SW:', reg));
});

// Ver Manifest
fetch('/manifest.json').then(r => r.json()).then(m => {
    console.log('Manifest:', m);
    console.log('Display:', m.display);
    console.log('Icons:', m.icons.length);
});
```

Si `contextoSeguro: false`, **necesitas HTTPS obligatoriamente**.

---

## Archivos Necesarios

Estructura final para HTTPS:

```
proyecto/
├── src/
│   └── backend/
│       ├── cert.pem          # Certificado SSL
│       ├── key.pem           # Llave privada
│       ├── run_https.py      # Script Python HTTPS
│       └── manage.py
├── iniciar_https.bat         # Script Windows HTTPS
└── iniciar_desarrollo.bat    # Script HTTP normal
```

---

**Última actualización:** 18 de Noviembre de 2025  
**Versión:** 1.0

