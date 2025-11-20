# HTTPS en Python 3.13 - Problema y Soluciones

## El Problema

**django-sslserver no funciona con Python 3.13+**

Error:
```
AttributeError: module 'ssl' has no attribute 'wrap_socket'
```

Causa: `ssl.wrap_socket()` fue deprecado en Python 3.10 y eliminado completamente en Python 3.13.

## Soluciones

### Solucion 1: Usar ngrok (RECOMENDADO)

**La forma mas facil de obtener HTTPS:**

```batch
# Desde el launcher
iniciar_studentspoint.bat
# Opcion [4] - ngrok

# O directamente
scripts\iniciar_con_ngrok.bat
```

**Ventajas:**
- HTTPS automatico sin certificados
- Funciona con cualquier version de Python
- Sin configuracion compleja
- Perfecto para PWA en celular
- URL publica instantanea

**Ver:** `docs/guias/USAR-NGROK.md`

---

### Solucion 2: Downgrade a Python 3.12

Si necesitas usar django-sslserver:

**Instalar Python 3.12:**
```powershell
winget install Python.Python.3.12
```

**Configurar como version por defecto:**
```powershell
# Verificar versiones instaladas
py -0

# Usar Python 3.12 para el proyecto
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install django-sslserver
```

**Actualizar el PATH:**
1. Configuracion del sistema
2. Variables de entorno
3. Editar PATH
4. Mover Python 3.12 arriba de Python 3.13

---

### Solucion 3: Usar django-extensions + Werkzeug

**Alternativa moderna a django-sslserver:**

**Instalar:**
```bash
pip install django-extensions
pip install werkzeug
pip install pyOpenSSL
```

**Configurar `settings/dev.py`:**
```python
INSTALLED_APPS = [
    # ...
    'django_extensions',
]
```

**Generar certificados:**
```bash
cd proyecto\src\backend

# Generar certificado self-signed
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=CL/ST=Santiago/L=Santiago/O=StudentsPoint/CN=localhost"
```

**Iniciar servidor HTTPS:**
```bash
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8443
```

**Ventajas:**
- Compatible con Python 3.13+
- Mas moderno que django-sslserver
- Mejores herramientas de debugging

**Desventajas:**
- Requiere configuracion manual
- Mas dependencias

---

### Solucion 4: Usar Stunnel como Proxy HTTPS

**Para usuarios avanzados:**

Stunnel actua como proxy HTTPS delante de Django HTTP.

**Instalar Stunnel:**
```powershell
winget install Stunnel.Stunnel
```

**Configurar `stunnel.conf`:**
```ini
[https]
accept = 0.0.0.0:8443
connect = 127.0.0.1:8000
cert = cert.pem
key = key.pem
```

**Iniciar:**
```bash
# Terminal 1: Django HTTP
python manage.py runserver 127.0.0.1:8000

# Terminal 2: Stunnel HTTPS
stunnel stunnel.conf
```

**Ventajas:**
- Funciona con cualquier version de Python
- No depende de librerias Python
- Mas seguro y robusto

**Desventajas:**
- Configuracion mas compleja
- Dos procesos separados

---

### Solucion 5: Usar playit.gg sin HTTPS

Si solo necesitas acceso publico (no PWA):

```batch
iniciar_studentspoint.bat
# Opcion [5] - playit.gg HTTP
```

**Ventajas:**
- URL permanente
- Sin limites de conexion
- No necesita certificados

**Desventajas:**
- Solo HTTP (no HTTPS)
- PWA puede no funcionar correctamente

---

## Comparacion de Soluciones

| Solucion | Dificultad | Python 3.13 | HTTPS | PWA | Recomendado |
|----------|-----------|-------------|-------|-----|-------------|
| ngrok | Muy Facil | Si | Si | Si | **Si** |
| Python 3.12 | Facil | No | Si | Si | Temporal |
| django-extensions | Media | Si | Si | Si | Desarrollo |
| Stunnel | Dificil | Si | Si | Si | Produccion |
| playit HTTP | Facil | Si | No | No | APIs |

---

## Recomendacion Final

### Para PWA en Celular
**Usa ngrok** (Opcion [4] del launcher)
- Mas facil
- HTTPS automatico
- Sin configuracion
- Funciona con Python 3.13

### Para Desarrollo Local
**Usa Python 3.12**
- django-sslserver funciona
- Menos complicaciones
- Configuracion estandar

### Para Produccion
**Usa Nginx + Gunicorn**
- Configuracion profesional
- Mejor rendimiento
- Mas seguro

---

## Script Actualizado

El launcher (`iniciar_studentspoint.bat`) ahora detecta Python 3.13 y:

1. Muestra advertencia sobre incompatibilidad
2. Recomienda usar ngrok
3. Ofrece alternativas
4. Evita el error antes de intentar iniciar

**Si tienes Python 3.13:**
```batch
iniciar_studentspoint.bat
# Opcion [4] - ngrok (funciona perfectamente)
```

---

## Preguntas Frecuentes

### Por que se elimino ssl.wrap_socket()?

Python 3.13 elimino APIs deprecadas para mejorar seguridad. `ssl.wrap_socket()` fue reemplazado por `ssl.SSLContext()`.

### django-sslserver se actualizara?

El proyecto esta inactivo. Ultima actualizacion: 2016. No hay planes de actualizacion.

### Puedo usar Python 3.13 para el resto del proyecto?

Si, solo django-sslserver tiene problemas. Todo lo demas funciona perfectamente con Python 3.13.

### Necesito HTTPS para desarrollo?

No, solo para:
- Instalar PWA en celular
- Probar caracteristicas que requieren HTTPS (geolocation, camera, etc.)
- Compartir con clientes externos

Para desarrollo local normal, HTTP es suficiente.

---

## Links Utiles

- **ngrok:** https://ngrok.com/
- **django-extensions:** https://django-extensions.readthedocs.io/
- **Stunnel:** https://www.stunnel.org/
- **Python 3.12:** https://www.python.org/downloads/release/python-3120/

---

**Resumen:** Si tienes Python 3.13, usa ngrok. Es la solucion mas simple y funciona perfectamente.

