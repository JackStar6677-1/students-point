# CONFIGURACION DE GOOGLE OAUTH Y EMAIL - STUDENTSPOINT

## Estado Actual del Proyecto

### Sistema de Email

**DESARROLLO (SMTP Real Configurado)**
- Backend: `django.core.mail.backends.smtp.EmailBackend`
- Servidor: smtp.gmail.com
- Email: pablo.elias.miranda.292003@gmail.com
- App Password: jiyn qwpy soku ghfd
- **Los emails se envian REALMENTE a los usuarios**
- NO se necesita configuracion adicional
- Funciona inmediatamente al ejecutar el servidor

**PRODUCCION (Requiere configuracion)**
- Backend: `django.core.mail.backends.smtp.EmailBackend`
- Necesita cuenta de email SMTP configurada

### Google OAuth 2.0

**ESTADO ACTUAL**
- Credenciales de desarrollo incluidas en el codigo
- Funcional para `localhost:8000` y `127.0.0.1:8000`
- NO requiere configuracion adicional para desarrollo local

**PARA PRODUCCION**
- Requiere crear proyecto propio en Google Cloud Console
- Requiere configurar URIs de redireccion con tu dominio

---

## DESARROLLO (Ya esta configurado - Emails Reales)

### Email en Desarrollo

El sistema de email YA FUNCIONA con SMTP REAL en desarrollo:

```python
# settings/dev.py (ya configurado)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pablo.elias.miranda.292003@gmail.com'
EMAIL_HOST_PASSWORD = 'jiyn qwpy soku ghfd'  # App Password
DEFAULT_FROM_EMAIL = 'StudentsPoint <pablo.elias.miranda.292003@gmail.com>'
```

**Como funciona:**
1. Usuario se registra con SU EMAIL REAL
2. Sistema genera codigo de 6 digitos
3. Sistema ENVIA EMAIL REAL via Gmail SMTP
4. Usuario RECIBE EMAIL en su bandeja de entrada
5. Usuario ve el codigo en su email
6. Usuario ingresa codigo en la app

**El email que recibira el usuario:**
```
De: StudentsPoint <pablo.elias.miranda.292003@gmail.com>
Para: usuario@example.com
Asunto: Verificacion de email - StudentsPoint

Hola Juan Perez,

Tu codigo de verificacion es: 456789

Este codigo expirara en 15 minutos.

Si no solicitaste este codigo, puedes ignorar este email.

Saludos,
Equipo StudentsPoint
```

**LOS EMAILS SE ENVIAN REALMENTE** - Los usuarios los reciben en su correo.

### Google OAuth en Desarrollo

El sistema OAuth YA FUNCIONA en desarrollo:

**Credenciales configuradas:**
- Client ID: 307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s.apps.googleusercontent.com
- Client Secret: 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
- URIs autorizados: localhost:8000, 127.0.0.1:8000

**Estas credenciales pertenecen a:** pablo.elias.miranda.292003@gmail.com

**Como funciona:**
1. Usuario hace clic en "Login con Google"
2. Redirige a Google para autenticacion
3. Usuario selecciona su cuenta de Google
4. Google redirige de vuelta con token
5. Sistema crea/busca usuario y genera JWT

**NO NECESITAS CONFIGURAR NADA EN GOOGLE** - Ya esta todo listo.

**IMPORTANTE:** Las credenciales OAuth que tienes YA estan incluidas en el codigo:
- Ubicacion: `settings/dev.py` lineas 67-70
- Ya funcionales para localhost
- NO necesitas hacer nada adicional

---

## PRODUCCION (Cuando despliegues)

### 1. Configurar Email SMTP (Produccion)

Cuando despliegues a produccion, necesitaras configurar email SMTP real.

#### Opcion 1: Gmail (Recomendado para proyectos pequenos)

**Paso 1: Habilitar App Password en Gmail**

1. Ir a tu cuenta de Google: https://myaccount.google.com
2. Ir a "Seguridad"
3. Habilitar "Verificacion en 2 pasos" (requerido)
4. Ir a "Contraseñas de aplicaciones"
5. Crear nueva contraseña de aplicacion:
   - Seleccionar app: "Correo"
   - Seleccionar dispositivo: "Otro (nombre personalizado)"
   - Escribir: "StudentsPoint"
   - Hacer clic en "Generar"
6. Copiar la contraseña de 16 caracteres generada

**Paso 2: Configurar variables de entorno**

Crear archivo `.env` en `proyecto/src/backend/`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-16-caracteres
DEFAULT_FROM_EMAIL=noreply@studentspoint.app
```

**Paso 3: Reiniciar servidor**

```bash
python manage.py runserver
```

#### Opcion 2: Servidor SMTP Propio

Si tienes servidor de email propio:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.tu-servidor.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=usuario@tu-dominio.com
EMAIL_HOST_PASSWORD=tu-password
DEFAULT_FROM_EMAIL=noreply@studentspoint.app
```

#### Opcion 3: Servicios de Email (SendGrid, Mailgun, etc.)

Para produccion profesional, considera servicios especializados:

**SendGrid:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
DEFAULT_FROM_EMAIL=noreply@studentspoint.app
```

### 2. Configurar Google OAuth (Produccion)

Cuando despliegues con tu dominio propio:

**Paso 1: Crear Proyecto en Google Cloud Console**

1. Ir a: https://console.cloud.google.com
2. Crear nuevo proyecto:
   - Nombre: "StudentsPoint"
   - Hacer clic en "Crear"

**Paso 2: Habilitar API**

1. Ir a "APIs y servicios" > "Biblioteca"
2. Buscar "Google+ API"
3. Hacer clic en "Habilitar"

**Paso 3: Crear Credenciales OAuth**

1. Ir a "APIs y servicios" > "Credenciales"
2. Hacer clic en "Crear credenciales" > "ID de cliente de OAuth 2.0"
3. Configurar pantalla de consentimiento (si no lo has hecho):
   - Tipo de usuario: "Externo"
   - Nombre de la aplicacion: "StudentsPoint"
   - Email de asistencia: tu-email@example.com
   - Dominios autorizados: tu-dominio.com
   - Guardar y continuar

4. Crear ID de cliente OAuth:
   - Tipo de aplicacion: "Aplicacion web"
   - Nombre: "StudentsPoint Web"
   
5. URIs de redireccion autorizados:
   ```
   https://tu-dominio.com/api/auth/google/callback/web/
   http://localhost:8000/api/auth/google/callback/web/
   http://127.0.0.1:8000/api/auth/google/callback/web/
   ```

6. Hacer clic en "Crear"
7. COPIAR el Client ID y Client Secret generados

**Paso 4: Configurar en el Proyecto**

Actualizar archivo `.env`:

```env
GOOGLE_OAUTH_CLIENT_ID=tu-nuevo-client-id
GOOGLE_OAUTH_CLIENT_SECRET=tu-nuevo-client-secret
GOOGLE_REDIRECT_URI=https://tu-dominio.com/api/auth/google/callback/web/
FRONTEND_URL=https://tu-dominio.com
```

---

## COMO PROBAR EL SISTEMA DE EMAIL (Desarrollo)

### Paso 1: Iniciar el servidor

```bash
cd proyecto\src\backend
python manage.py runserver
```

### Paso 2: Registrar un usuario con TU EMAIL REAL

**IMPORTANTE:** Usa tu email REAL para recibir el codigo.

Hacer request a:
```
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "email": "TU-EMAIL-REAL@gmail.com",
  "password": "password123",
  "name": "Tu Nombre",
  "career": "Ingenieria en Informatica"
}
```

### Paso 3: REVISAR TU BANDEJA DE ENTRADA

**VE A TU EMAIL** y encontraras:

```
De: StudentsPoint <pablo.elias.miranda.292003@gmail.com>
Para: TU-EMAIL-REAL@gmail.com
Asunto: Verificacion de email - StudentsPoint

Hola Tu Nombre,

Tu codigo de verificacion es: 456789

Este codigo expirara en 15 minutos.

Si no solicitaste este codigo, puedes ignorar este email.

Saludos,
Equipo StudentsPoint
```

### Paso 4: Verificar el email con el codigo recibido

```
POST http://127.0.0.1:8000/api/auth/verificar-email/
Content-Type: application/json

{
  "email": "TU-EMAIL-REAL@gmail.com",
  "codigo": "456789"
}
```

**Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Email verificado exitosamente"
}
```

**EL SISTEMA ENVIA EMAILS REALES** - No es simulacion.

---

## COMO PROBAR GOOGLE OAUTH (Desarrollo)

### Paso 1: Acceder al login de Google

En el navegador:
```
http://127.0.0.1:8000/api/auth/google/login/web/
```

### Paso 2: Seleccionar cuenta de Google

El navegador te redirigira a Google para autenticarte.

### Paso 3: Aprobar permisos

Google pedira permisos para:
- Ver tu informacion basica
- Ver tu email

### Paso 4: Redireccion automatica

Google te redirige de vuelta con tus tokens JWT.

**YA ESTA FUNCIONANDO** - No necesitas configurar nada.

---

## VERIFICACION RAPIDA DEL SISTEMA

### Verificar que todo funciona:

```bash
cd proyecto\src\backend
python manage.py check
```

**Resultado esperado:** `System check identified no issues (0 silenced).`

### Verificar migraciones:

```bash
python manage.py showmigrations
```

**Resultado esperado:** Todas con `[X]`

### Probar servidor:

```bash
python manage.py runserver
```

**Resultado esperado:** Servidor inicia en `http://127.0.0.1:8000`

---

## RESUMEN PARA TI (DESARROLLADOR)

### QUE YA FUNCIONA (Sin configuracion adicional):

1. **Email en desarrollo**: Los emails se muestran en consola
2. **Google OAuth**: Ya configurado con credenciales de desarrollo
3. **Base de datos**: SQLite con todas las migraciones aplicadas
4. **Sistema de verificacion**: Codigos de 6 digitos funcionando
5. **Recuperacion de password**: Flujo completo implementado
6. **Cambio de carrera**: Historial y permisos funcionando
7. **Sistema de foros**: Restricciones por carrera operativas

### QUE NECESITAS HACER (NADA para desarrollo):

**Para desarrollo local:** NADA - Todo ya funciona

**Para produccion (cuando despliegues):**
1. Configurar email SMTP (Gmail App Password o servicio profesional)
2. Crear proyecto Google OAuth propio con tu dominio
3. Configurar variables de entorno en servidor

### PARA PROBAR AHORA MISMO:

```bash
# 1. Iniciar servidor
cd proyecto\src\backend
python manage.py runserver

# 2. Abrir navegador
http://127.0.0.1:8000

# 3. Registrarte en /register.html
# 4. Ver codigo en la consola del servidor
# 5. Verificar email en la app
```

**TODO FUNCIONA SIN CONFIGURACION ADICIONAL**

---

## TROUBLESHOOTING

### Email no se muestra en consola

**Problema:** No veo emails en la consola

**Solucion:** Asegurate de que en `settings/base.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Google OAuth da error

**Problema:** Error al hacer login con Google

**Solucion 1:** Verificar que las URLs autorizadas incluyan:
- `http://localhost:8000/api/auth/google/callback/web/`
- `http://127.0.0.1:8000/api/auth/google/callback/web/`

**Solucion 2:** Las credenciales de desarrollo ya estan configuradas. Si no funciona:
1. Verificar conexion a internet
2. Verificar que Google+ API este habilitada en el proyecto

### Codigos no funcionan

**Problema:** Codigo de verificacion no funciona

**Causa posible:** Codigo expiro (15 minutos para verificacion, 30 para password)

**Solucion:** Usar endpoint de reenvio:
```
POST /api/auth/reenviar-codigo/
{"email": "usuario@example.com"}
```

---

## DOCUMENTOS RELACIONADOS

- `DEPLOYMENT.md` - Guia completa de despliegue en produccion
- `autenticacion-implementacion-completa.txt` - Detalles tecnicos del sistema
- `README.md` - Documentacion general del proyecto

---

**Fecha:** Octubre 2025  
**Estado:** Sistema funcional en desarrollo  
**Accion requerida para desarrollo:** NINGUNA - Todo funciona

