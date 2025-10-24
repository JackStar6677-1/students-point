# SOLUCION AL ERROR DE OAUTH GOOGLE

## Error Reportado

```
No puedes acceder a esta app porque no cumple con la politica OAuth 2.0 de Google.

Si eres el desarrollador de la app, registra el URI de redireccionamiento en Google Cloud Console.
Detalles de la solicitud: redirect_uri=http://localhost:8000/api/auth/google/callback/web/
```

---

## CAUSA DEL PROBLEMA

Las credenciales OAuth que tienes (Client ID y Secret) no tienen configurado el URI de redireccion:
`http://localhost:8000/api/auth/google/callback/web/`

---

## SOLUCION COMPLETA

### Opcion 1: Configurar las Credenciales Existentes (RECOMENDADO)

**Paso 1:** Ir a Google Cloud Console

1. Acceder a: https://console.cloud.google.com
2. Iniciar sesion con: pablo.elias.miranda.292003@gmail.com

**Paso 2:** Seleccionar/Crear Proyecto

1. En la barra superior, seleccionar el proyecto asociado a tus credenciales
2. O crear nuevo proyecto si no existe:
   - Clic en el dropdown de proyectos
   - "Nuevo Proyecto"
   - Nombre: "StudentsPoint"
   - Crear

**Paso 3:** Habilitar APIs Necesarias

1. Menu lateral > "APIs y servicios" > "Biblioteca"
2. Buscar: "Google+ API" o "People API"
3. Hacer clic en "Habilitar"

**Paso 4:** Configurar Pantalla de Consentimiento (Si no esta hecha)

1. Menu lateral > "APIs y servicios" > "Pantalla de consentimiento de OAuth"
2. Tipo de usuario: "Externo"
3. Hacer clic en "Crear"
4. Configurar:
   - Nombre de la aplicacion: StudentsPoint
   - Correo de asistencia: pablo.elias.miranda.292003@gmail.com
   - Dominios autorizados: (dejar en blanco por ahora)
   - Correo del desarrollador: pablo.elias.miranda.292003@gmail.com
5. Guardar y continuar
6. Alcances (Scopes): No agregar nada adicional
7. Usuarios de prueba: Agregar tu email y el de tus compañeros
   - pablo.elias.miranda.292003@gmail.com
   - (otros emails del equipo)
8. Guardar y continuar
9. Resumen: Volver al panel

**Paso 5:** Agregar URIs de Redireccion a tus Credenciales

1. Menu lateral > "APIs y servicios" > "Credenciales"
2. Buscar tu Client ID: 307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s
3. Hacer clic en el para editarlo
4. En "URIs de redireccion autorizados" agregar:
   ```
   http://localhost:8000/api/auth/google/callback/web/
   http://127.0.0.1:8000/api/auth/google/callback/web/
   ```
5. Hacer clic en "Guardar"

**Paso 6:** Probar

1. Cerrar el navegador completamente
2. Abrir de nuevo
3. Ir a: http://127.0.0.1:8000/api/auth/google/login/web/
4. Deberia funcionar ahora

---

### Opcion 2: Usar Solo Autenticacion Tradicional (TEMPORAL)

Si no puedes configurar OAuth inmediatamente, puedes usar solo el login tradicional:

**Login con email y contraseña:**
- Funciona inmediatamente
- No requiere configuracion OAuth
- Email: cualquier email registrado
- Password: la que configuraste

**Como probar:**
1. Ir a /register.html
2. Registrarte con tu email
3. Verificar email con codigo recibido
4. Usar login tradicional

---

## VERIFICACION DE CONFIGURACION ACTUAL

### Verificar que Credenciales Esten en el Proyecto

**Archivo:** `proyecto/src/backend/studentspoint/settings/dev.py`

```python
GOOGLE_CLIENT_ID = '307562557576-0fd8ta7i09i1e6it5hstla13jsomeq2s.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/api/auth/google/callback/web/'
```

 Ya configuradas

### Verificar URIs en Google Cloud

Debes asegurarte que en Google Cloud Console, en tu proyecto OAuth,
los siguientes URIs esten autorizados:

**URIs de redireccion autorizados:**
```
http://localhost:8000/api/auth/google/callback/web/
http://127.0.0.1:8000/api/auth/google/callback/web/
```

**URIs de JavaScript autorizados:**
```
http://localhost:8000
http://127.0.0.1:8000
```

---

## FLUJO CORRECTO DE OAUTH

1. Usuario hace clic en "Login con Google"
2. App redirige a: `/api/auth/google/login/web/`
3. Backend redirige a Google con Client ID
4. Google muestra pantalla de seleccion de cuenta
5. Usuario selecciona cuenta
6. Google valida que redirect_uri este autorizado
7. Si OK: Google redirige a `/api/auth/google/callback/web/` con codigo
8. Backend intercambia codigo por token de Google
9. Backend obtiene info del usuario de Google
10. Backend crea/busca usuario en BD
11. Backend genera tokens JWT
12. Backend redirige a frontend con tokens
13. Usuario logueado exitosamente

**El error ocurre en el paso 6:** Google no reconoce el redirect_uri como autorizado.

---

## ALTERNATIVA: DESHABILITAR OAUTH TEMPORALMENTE

Si prefieres enfocarte en otras funcionalidades primero:

**Comentar el boton de OAuth en login.html y register.html:**

En `login.html` y `register.html`, buscar el boton de Google y comentarlo:

```html
<!-- TEMPORALMENTE DESHABILITADO
<button onclick="loginWithGoogle()" class="btn btn-google">
  <i class="fab fa-google"></i> Continuar con Google
</button>
-->
```

Asi te enfocas en el login tradicional que ya funciona perfectamente.

---

## RESUMEN

**PROBLEMA:** URIs de redireccion no configurados en Google Cloud Console

**SOLUCION RAPIDA:**
1. Ir a Google Cloud Console
2. Seleccionar tu proyecto
3. Credenciales > Editar tu Client ID
4. Agregar URIs de redireccion
5. Guardar

**ALTERNATIVA:** Usar solo login tradicional (ya funciona al 100%)

**TIEMPO ESTIMADO:** 5-10 minutos para configurar

---

**Nota:** El login tradicional con email y contraseña funciona perfectamente
y no depende de OAuth. Puedes usar ese mientras configuras Google.

**Fecha:** 9 de Octubre 2025

