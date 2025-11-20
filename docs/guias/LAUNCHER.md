# StudentsPoint Launcher - Guia Completa

## Que es el Launcher

`iniciar_studentspoint.bat` es un script maestro que:
- Instala todas las dependencias automaticamente
- Permite elegir el modo de inicio mediante menu interactivo
- Detecta que herramientas tienes instaladas
- Configura todo automaticamente

## Inicio Rapido

```batch
iniciar_studentspoint.bat
```

Se abrira un menu con todas las opciones disponibles.

---

## Opciones del Menu

### [1] Local - Solo en esta PC

**Cuando usar:** Desarrollo basico, sin necesidad de acceso externo.

**Que hace:**
- Inicia Django en 127.0.0.1:8000
- Solo accesible desde esta PC
- No requiere herramientas adicionales

**URLs:**
- http://127.0.0.1:8000

**Ventajas:**
- Mas rapido
- No necesita configuracion adicional
- Ideal para desarrollo inicial

**Desventajas:**
- No puedes acceder desde otros dispositivos
- No puedes probar PWA en celular

---

### [2] Red Local - Acceso WiFi

**Cuando usar:** Quieres probar en tu celular/tablet sin internet externo.

**Que hace:**
- Detecta tu IP local (192.168.x.x)
- Inicia Django en 0.0.0.0:8000
- Accesible desde cualquier dispositivo en tu red WiFi

**URLs:**
- Local: http://127.0.0.1:8000
- Red: http://192.168.x.x:8000 (tu IP)

**Ventajas:**
- Facil de configurar
- No requiere internet
- Rapido y estable

**Desventajas:**
- Solo en tu red WiFi
- Sin HTTPS (PWA puede fallar)
- No accesible desde internet

---

### [3] Tailscale - Red Privada VPN

**Cuando usar:** Desarrollo en equipo o acceso remoto privado.

**Requisitos:**
- Tailscale instalado: https://tailscale.com/download
- Cuenta de Tailscale (gratuita)
- Tailscale corriendo en todos los dispositivos

**Que hace:**
- Detecta tu IP de Tailscale (100.x.x.x)
- Inicia Django en 0.0.0.0:8000
- Accesible desde cualquier dispositivo con Tailscale

**URLs:**
- Local: http://127.0.0.1:8000
- Tailscale: http://100.x.x.x:8000

**Ventajas:**
- Conexion privada y segura (VPN)
- IP fija (no cambia)
- Acceso desde cualquier lugar
- Perfecto para equipos

**Desventajas:**
- Requiere Tailscale en todos los dispositivos
- Sin HTTPS automatico
- Configuracion inicial necesaria

---

### [4] ngrok - Tunel HTTPS Publico

**Cuando usar:** Probar PWA en celular, compartir demo, necesitas HTTPS.

**Requisitos:**
- ngrok instalado (el script puede instalarlo automaticamente)
- Token de ngrok: https://dashboard.ngrok.com/

**Que hace:**
- Instala ngrok si no esta (con winget)
- Configura authtoken
- Inicia Django en 0.0.0.0:8000
- Inicia ngrok con tunel HTTPS

**URLs:**
- Local: http://127.0.0.1:8000
- Publico: https://xxx.ngrok-free.app (cambia cada vez)

**Ventajas:**
- HTTPS automatico sin configuracion
- Perfecto para PWA en celular
- Sin advertencias de seguridad
- Accesible desde internet

**Desventajas:**
- URL cambia cada reinicio (version gratuita)
- 40 conexiones/minuto (limite gratuito)
- Pagina de aviso en version gratuita

**Recomendado para:**
- Instalar PWA en celulares
- Demos rapidos
- Testing de HTTPS

---

### [5] playit.gg - Tunel HTTP Permanente

**Cuando usar:** Necesitas URL permanente, sin limites de conexion.

**Requisitos:**
- playit.gg instalado: https://playit.gg/download
- Tunel configurado en: https://playit.gg/account

**Que hace:**
- Inicia Django en 127.0.0.1:8000
- Inicia agente de playit.gg
- Tunel apunta a tu servidor local

**URLs:**
- Local: http://127.0.0.1:8000
- Publico: http://best-wales.gl.at.ply.gg:16063

**Ventajas:**
- URL permanente (no cambia)
- Sin limites de conexion
- Completamente gratuito
- Multi-protocolo

**Desventajas:**
- Solo HTTP (no HTTPS por defecto)
- Advertencia de seguridad en navegador
- PWA puede no instalarse correctamente

**Recomendado para:**
- APIs publicas
- Desarrollo backend
- Cuando necesitas URL fija

---

### [6] playit.gg HTTPS - Con Certificados SSL

**Cuando usar:** Necesitas HTTPS con playit.gg y URL permanente.

**IMPORTANTE:** No compatible con Python 3.13+. Ver `docs/guias/HTTPS-PYTHON313.md`

**Requisitos:**
- Python 3.12 o inferior (django-sslserver no funciona con Python 3.13+)
- playit.gg instalado
- OpenSSL instalado (el script puede instalarlo)
- Configurar tunel al puerto 8443

**Alternativa para Python 3.13:** Usa opcion [4] - ngrok (HTTPS automatico sin problemas)

**Que hace:**
- Instala django-sslserver
- Genera certificados SSL self-signed
- Inicia Django en 0.0.0.0:8443 con HTTPS
- Inicia agente de playit.gg

**URLs:**
- Local: https://127.0.0.1:8443
- Publico: https://best-wales.gl.at.ply.gg:16063

**Pasos adicionales:**
1. Ve a https://playit.gg/account
2. Edita tu tunel
3. Cambia "Local Port" de 8000 a 8443
4. Guarda y reinicia playit

**Ventajas:**
- HTTPS con URL permanente
- Sin limites de conexion
- Gratis

**Desventajas:**
- Configuracion mas compleja
- Certificado self-signed (advertencia en navegador)
- Requiere OpenSSL

**Recomendado para:**
- Cuando necesitas HTTPS y URL fija
- Produccion de bajo presupuesto

---

### [7] Produccion

**Cuando usar:** Despliegue en servidor real.

**Que hace:**
- Ejecuta el script de produccion completo
- Configuraciones optimizadas
- Logs avanzados

**Recomendado para:**
- Despliegue real en servidor

---

### [8] Instalar Dependencias

**Cuando usar:** Primera vez, o despues de actualizar el repositorio.

**Que hace:**
- Verifica Python
- Actualiza pip
- Instala todas las dependencias de Python
- Instala django-sslserver
- Intenta instalar ngrok automaticamente
- Intenta instalar OpenSSL automaticamente
- Verifica Tailscale y playit.gg
- Ejecuta migraciones
- Recolecta archivos estaticos
- Crea superusuario

**Duracion:** 3-5 minutos la primera vez

**Instalaciones automaticas:**
- Python packages (Django, DRF, etc.)
- django-sslserver
- ngrok (via winget)
- OpenSSL (via winget)

**Instalaciones manuales:**
- Tailscale (opcional)
- playit.gg (opcional)

**Resultado:**
- Todo listo para usar cualquier modo de inicio

---

## Comparacion Rapida

| Opcion | HTTPS | URL Fija | Internet | Dificultad | Recomendado Para |
|--------|-------|----------|----------|------------|------------------|
| Local | No | Si (local) | No | Muy Facil | Desarrollo basico |
| Red Local | No | Si (local) | No | Facil | Testing en WiFi |
| Tailscale | No | Si | Si (VPN) | Media | Equipos remotos |
| ngrok | Si | No | Si | Facil | PWA en celular |
| playit HTTP | No | Si | Si | Facil | APIs publicas |
| playit HTTPS | Si | Si | Si | Media | Produccion low-cost |
| Produccion | Configurable | Si | Si | Alta | Despliegue real |

---

## Flujo de Trabajo Recomendado

### Primera Vez

1. Ejecuta `iniciar_studentspoint.bat`
2. Selecciona opcion [8] - Instalar Dependencias
3. Espera a que termine (3-5 minutos)
4. Vuelve al menu y elige tu modo de inicio

### Desarrollo Diario

1. Ejecuta `iniciar_studentspoint.bat`
2. Selecciona opcion [1] - Local
3. Desarrolla normalmente

### Testing en Celular (PWA)

1. Ejecuta `iniciar_studentspoint.bat`
2. Selecciona opcion [4] - ngrok
3. Copia la URL HTTPS que aparece
4. Abre esa URL en tu celular
5. Instala la PWA

### Compartir Demo

1. Ejecuta `iniciar_studentspoint.bat`
2. Selecciona opcion [4] - ngrok (URL temporal)
   O opcion [5] - playit.gg (URL permanente)
3. Comparte la URL publica

---

## Solucionar Problemas

### Error: Python no encontrado

**Solucion:**
```batch
winget install Python.Python.3.11
```

O descarga desde: https://www.python.org/downloads/

### Error: ngrok no encontrado

**Solucion automatica:**
- Selecciona opcion [8] del menu
- El script instalara ngrok automaticamente

**Solucion manual:**
```batch
winget install ngrok.ngrok
```

### Error: OpenSSL no encontrado

**Solucion automatica:**
- Selecciona opcion [8] del menu

**Solucion manual:**
```batch
winget install ShiningLight.OpenSSL.Light
```

### Error: No se puede instalar ngrok/OpenSSL

**Causa:** winget no disponible o fallo de red

**Solucion:**
- ngrok: https://ngrok.com/download
- OpenSSL: https://slproweb.com/products/Win32OpenSSL.html

### Django no inicia

**Verificar:**
1. Puerto 8000 esta ocupado?
   ```batch
   netstat -ano | findstr :8000
   ```

2. Dependencias instaladas?
   - Selecciona opcion [8] del menu

3. Migraciones aplicadas?
   ```batch
   cd proyecto\src\backend
   python manage.py migrate
   ```

### playit.gg no funciona

**Verificar:**
1. Esta instalado?
   ```batch
   playit --version
   ```

2. Tunel configurado?
   - Ve a https://playit.gg/account
   - Verifica que el tunel este activo
   - Puerto correcto: 8000 (HTTP) o 8443 (HTTPS)

3. Agente conectado?
   - Debe aparecer "Connected" en la ventana de playit

---

## Atajos de Teclado

En el menu:
- `1-8` - Seleccionar opcion
- `0` - Salir
- `Ctrl+C` - Cancelar operacion actual

En el servidor:
- `Ctrl+C` - Detener servidor
- Cerrar ventana - Detener servicio

---

## Credenciales por Defecto

Todas las opciones usan las mismas credenciales:

**Admin Django:**
- Usuario: `admin@studentspoint.app`
- Password: `admin123`

**Base de Datos:**
- SQLite (desarrollo)
- Archivo: `proyecto/src/backend/db.sqlite3`

---

## Logs y Depuracion

**Logs de Django:**
```
proyecto/src/backend/logs/general.log
proyecto/src/backend/logs/errors.log
proyecto/src/backend/logs/api.log
proyecto/src/backend/logs/auth.log
```

**Ver logs en tiempo real:**
```batch
scripts\ver_logs.bat
```

---

## Preguntas Frecuentes

### Puedo usar multiple opciones al mismo tiempo?

No directamente. Cada opcion usa un puerto especifico:
- Opciones 1-5: Puerto 8000
- Opcion 6: Puerto 8443

Puedes tener ventanas abiertas, pero solo una puede usar el puerto.

### Como cambio entre opciones?

1. Detener el servidor actual (Ctrl+C o cerrar ventana)
2. Volver al menu
3. Seleccionar nueva opcion

### Cual es la mejor opcion para PWA?

**Opcion [4] - ngrok** es la mejor para PWA porque:
- HTTPS automatico
- Sin advertencias de seguridad
- Funciona inmediatamente

### Cual opcion es mas rapida?

**Opcion [1] - Local** porque:
- Sin configuracion adicional
- Sin servicios externos
- Conexion directa

### Puedo personalizar las opciones?

Si, edita el archivo `iniciar_studentspoint.bat` y modifica:
- URLs
- Puertos
- Configuraciones
- Comandos

---

## Documentacion Adicional

- `USAR-NGROK.md` - Guia completa de ngrok
- `USAR-PLAYIT.md` - Guia completa de playit.gg
- `docs/GUIA-COMPLETA.md` - Documentacion general
- `docs/guias/GUIA-RAPIDA-MOVIL.md` - PWA en celular

---

**Todo listo! Ejecuta `iniciar_studentspoint.bat` y elige tu modo de inicio.**

