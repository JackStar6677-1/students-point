# Usar playit.gg - Guia Rapida

## Tu tunel ya esta configurado

Segun tu configuracion:
- **Dominio:** best-wales.gl.at.ply.gg:16063
- **IP Publica:** 147.185.221.24:16063
- **Agente:** students-point
- **Puerto Local:** 127.0.0.1:8000
- **Protocolo:** HTTP (no HTTPS por defecto)

## IMPORTANTE: Limitacion de HTTPS

**playit.gg usa HTTP por defecto, no HTTPS.** Esto significa que:

- El navegador mostrara advertencia "No es seguro"
- La PWA puede no instalarse correctamente en algunos navegadores
- Los datos no estan encriptados en transito

### Soluciones para HTTPS:

**OPCION 1 (Recomendada): Usar ngrok**
- ngrok da HTTPS automaticamente sin configuracion
- Es mas facil para probar PWA en dispositivos moviles
- Ejecuta: `iniciar_con_ngrok.bat`
- Ver: `USAR-NGROK.md`

**OPCION 2: Configurar HTTPS con playit.gg**
- Requiere django-sslserver y certificados SSL
- Debes cambiar el tunel al puerto 8443
- Ejecuta: `iniciar_playit_https.bat`
- Mas complejo pero funcional

**OPCION 3: Cloudflare Tunnel**
- Da HTTPS gratuito y permanente
- Requiere cuenta de Cloudflare
- Mas configuracion inicial

---

## Ejecutar StudentsPoint con playit.gg

### Opcion 1: Script Automatico (Recomendado)

**Paso 1: Inicia el script**

```bash
iniciar_con_playit.bat
```

Este script:
- Inicia Django en una ventana separada (puerto 8000)
- Espera a que Django este listo
- Inicia el agente de playit.gg automaticamente (si esta instalado)

**Paso 2: Veras 2 o 3 ventanas**

1. **Ventana "Django Server - NO CERRAR"** - Dejala abierta
2. **Ventana "Playit.gg Tunnel - NO CERRAR"** - Dejala abierta
3. **Ventana principal** - Muestra informacion y URLs de acceso

**Paso 3: Accede desde internet**

Ya puedes acceder a tu aplicacion desde cualquier dispositivo usando:

```
http://best-wales.gl.at.ply.gg:16063
```

### Opcion 2: Manual (Si prefieres control total)

**Paso 1: Inicia Django**

```bash
cd proyecto\src\backend
python manage.py runserver 127.0.0.1:8000
```

**Paso 2: Inicia playit.gg en otra terminal**

```bash
playit
```

El agente se conectara automaticamente usando tu configuracion existente.

---

## Instalar la PWA desde Internet

### En dispositivos moviles:

1. Abre Chrome en tu celular
2. Navega a: `http://best-wales.gl.at.ply.gg:16063`
3. Menu (tres puntos) -> **"Agregar a pantalla de inicio"**
4. La PWA se instalara correctamente
5. Funcionara como app nativa con icono propio

### En escritorio (Chrome/Edge):

1. Abre el navegador
2. Navega a: `http://best-wales.gl.at.ply.gg:16063`
3. Icono de instalacion en la barra de direcciones
4. Click en **"Instalar"**

---

## Solucion de Problemas

### Error: "playit.gg no encontrado"

**Causa:** El ejecutable de playit no esta en el PATH del sistema.

**Solucion:**

1. **Descarga playit.gg:**
   - Windows: https://playit.gg/download
   - Descarga el instalador para Windows

2. **Instala playit.gg:**
   - Ejecuta el instalador
   - Sigue las instrucciones
   - Reinicia la terminal despues de instalar

3. **Alternativa - Ejecutable local:**
   - Descarga `playit.exe`
   - Coloca el archivo en la carpeta raiz del proyecto
   - El script lo detectara automaticamente

4. **Verifica la instalacion:**
   ```bash
   playit --version
   ```

### Django no responde

**Si ves errores de conexion:**

1. Verifica que Django este corriendo:
   ```bash
   # En un navegador local, abre:
   http://localhost:8000
   ```
   Si ves StudentsPoint, Django esta corriendo correctamente.

2. Verifica la ventana de Django:
   - Debe existir "Django Server - NO CERRAR"
   - Debe mostrar "Starting development server at http://127.0.0.1:8000/"
   - Si esta cerrada, reinicia el script

3. Puerto ocupado:
   ```bash
   # Ver que esta usando el puerto 8000:
   netstat -ano | findstr :8000
   ```

### El tunel no funciona

**Si playit.gg esta corriendo pero no puedes acceder:**

1. **Verifica la configuracion del tunel:**
   - Accede a: https://playit.gg/account
   - Ve a la seccion "Tunnels"
   - Verifica que el tunel "unnamed" este activo
   - Confirma que apunta a 127.0.0.1:8000

2. **Verifica el agente:**
   - En la ventana de playit.gg debe aparecer "Connected"
   - Si dice "Disconnected", verifica tu conexion a internet

3. **Reinicia el agente:**
   - Cierra la ventana "Playit.gg Tunnel"
   - Ejecuta manualmente: `playit`

### Configurar HTTPS con playit.gg

Si necesitas HTTPS (recomendado para PWA):

**Paso 1: Ejecuta el script de HTTPS**
```bash
iniciar_playit_https.bat
```

Este script:
- Instala django-sslserver
- Genera certificados SSL self-signed
- Inicia Django en puerto 8443 con HTTPS
- Te indica como configurar el tunel

**Paso 2: Configura el tunel para puerto 8443**

1. Ve a: https://playit.gg/account
2. Click en tu tunel "unnamed"
3. En "Local Port" cambia de `8000` a `8443`
4. Click en "Update"
5. Reinicia el agente de playit

**Paso 3: Accede con HTTPS**
```
https://best-wales.gl.at.ply.gg:16063
```

**Nota:** El navegador mostrara advertencia de certificado porque es self-signed.
Click en "Avanzado" -> "Continuar de todos modos"

**Alternativa mas facil:** Usa ngrok que da HTTPS automaticamente:
```bash
iniciar_con_ngrok.bat
```

### Cambio de dominio

Si tu dominio de playit.gg cambia o es diferente:

1. **Actualiza ALLOWED_HOSTS en Django:**

   Edita: `proyecto/src/backend/studentspoint/settings/dev.py`

   Agrega tu nuevo dominio:
   ```python
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       '0.0.0.0',
       'best-wales.gl.at.ply.gg',  # Tu dominio actual
       'tu-nuevo-dominio.gl.at.ply.gg',  # Nuevo dominio
   ]
   ```

2. **Actualiza el script:**

   Edita: `iniciar_con_playit.bat`

   Busca la linea con `best-wales.gl.at.ply.gg` y actualiza con tu nuevo dominio.

3. **Reinicia Django:**
   - Cierra la ventana "Django Server"
   - Vuelve a ejecutar `iniciar_con_playit.bat`

---

## Ventajas de usar playit.gg

**Acceso publico** - Cualquier persona puede acceder con el link
**Tunel persistente** - Tu dominio no cambia (a diferencia de ngrok gratuito)
**Sin limites de conexion** - No hay restricciones de 40 conexiones/minuto
**Gratis** - Completamente gratuito para uso personal
**Multi-protocolo** - Soporta TCP y UDP
**Dashboard web** - Administra tus tuneles desde el navegador

## Desventajas de usar playit.gg

**No tiene HTTPS automatico** - Requiere configuracion manual de certificados
**Advertencia de seguridad** - El navegador mostrara "No es seguro"
**PWA puede fallar** - Algunos navegadores requieren HTTPS para PWA
**Configuracion mas compleja** - Para HTTPS necesitas django-sslserver

---

## Notas Importantes

- **Dominio permanente:** A diferencia de ngrok, tu dominio de playit.gg no cambia entre reinicios
- **Seguridad:** Solo comparte tu enlace con personas de confianza
- **Rendimiento:** playit.gg usa anycast global para mejor latencia
- **Firewall:** Si el tunel no funciona, verifica tu firewall local
- **HTTPS:** Para HTTPS necesitas configurar un certificado. Por defecto es HTTP
- **Detener:** Presiona Ctrl+C en las ventanas para detener los servicios

---

## Ver Dashboard de playit.gg

Accede a tu dashboard web:
```
https://playit.gg/account
```

Alli puedes:
- Ver todos tus tuneles activos
- Crear nuevos tuneles
- Ver estadisticas de uso
- Cambiar configuraciones
- Administrar agentes

---

## Comparacion de herramientas

### ngrok (Recomendado para PWA y pruebas rapidas):
- **HTTPS automatico** - Sin configuracion
- Facil de usar - Un solo comando
- **Perfecto para PWA** - Sin advertencias de seguridad
- URL cambia cada reinicio (version gratuita)
- 40 conexiones/minuto (limite gratuito)
- Solo HTTP/HTTPS en version gratuita

### playit.gg (Recomendado para desarrollo sin PWA):
- Dominio permanente - No cambia entre reinicios
- Sin limites de conexiones
- Gratis sin restricciones
- Multi-protocolo (TCP/UDP)
- **NO tiene HTTPS automatico** - Requiere configuracion
- Mejor para APIs y desarrollo backend

### Tailscale (Recomendado para produccion):
- Red privada segura
- URL fija
- Sin limites
- Requiere Tailscale en todos los dispositivos
- Mejor para produccion y equipo

### Resumen rapido:

**Para probar PWA en celular:**
- Usa `iniciar_con_ngrok.bat` (HTTPS automatico)

**Para desarrollo backend/API:**
- Usa `iniciar_con_playit.bat` (dominio permanente)

**Para produccion o equipo:**
- Usa Tailscale con certificado SSL

---

## Comandos Utiles

### Ver estado del agente:
```bash
playit status
```

### Ver logs del agente:
```bash
playit logs
```

### Reiniciar agente:
```bash
playit restart
```

### Configuracion del agente:
```bash
playit config
```

---

## URLs de Acceso Completas

Una vez que todo este corriendo:

**Local (solo tu PC):**
```
http://127.0.0.1:8000
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/api/docs/
```

**Publico (desde internet):**
```
http://best-wales.gl.at.ply.gg:16063
http://best-wales.gl.at.ply.gg:16063/admin/
http://best-wales.gl.at.ply.gg:16063/api/docs/
```

**Credenciales por defecto:**
- Usuario: `admin@studentspoint.app`
- Password: `admin123`

---

## Logs del Sistema

Si necesitas revisar logs de Django:

```
proyecto\src\backend\logs\general.log   - Log general
proyecto\src\backend\logs\errors.log    - Errores
proyecto\src\backend\logs\api.log       - Peticiones API
proyecto\src\backend\logs\auth.log      - Autenticacion
```

Ver logs en tiempo real:
```bash
scripts\ver_logs.bat
```

---

## Documentacion Adicional

Para mas informacion sobre playit.gg:
- Documentacion oficial: https://playit.gg/docs
- Discord de soporte: https://playit.gg/discord
- FAQ: https://playit.gg/faq

---

**Eso es todo!** Ejecuta `iniciar_con_playit.bat` y tendras acceso publico a tu aplicacion en segundos.

