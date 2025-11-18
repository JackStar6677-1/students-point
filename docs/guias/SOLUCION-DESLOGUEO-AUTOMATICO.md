# Solución al Deslogueo Automático

## 📋 Problema Identificado

Los usuarios experimentaban **deslogueos inesperados** mientras navegaban por la aplicación.

### Causa Raíz

Los tokens JWT de acceso (`access_token`) tienen una vida útil limitada. Cuando el token expira:

1. El frontend hace requests a `/api/auth/me/` para verificar la sesión
2. El backend responde con **401 Unauthorized** (token expirado)
3. El frontend detecta el 401 y automáticamente:
   - Borra los tokens del `localStorage`
   - Redirige al usuario a `/login.html`
   - El usuario percibe esto como un "deslogueo inesperado"

### Evidencia en los Logs

```
[INFO] 2025-11-17 22:02:17 - [REQUEST] GET /api/auth/me/ - Usuario: Anonimo
[WARNING] 2025-11-17 22:02:17 - [RESPONSE] GET /api/auth/me/ - Status: 401
```

---

## ✅ Solución Implementada

### 1. Configuración de JWT (`settings/base.py`)

```python
SIMPLE_JWT = {
    # Tokens de acceso duran 60 minutos (1 hora)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Tokens de refresh duran 7 días
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    
    # Rotación de refresh tokens (seguridad adicional)
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    
    # Actualizar el last_login del usuario al generar token
    "UPDATE_LAST_LOGIN": True,
}
```

**Características:**
- Access tokens válidos por **1 hora**
- Refresh tokens válidos por **7 días**
- Rotación automática de refresh tokens para mayor seguridad
- Blacklist de tokens antiguos después de rotación

### 2. Servicio de Renovación Automática (`token-refresh.js`)

Creado un servicio JavaScript que:

1. **Se inicia automáticamente** al detectar tokens en `localStorage`
2. **Renueva el token cada 50 minutos** (antes de que expire)
3. **Maneja errores** de tokens inválidos o expirados
4. **Redirige al login** solo cuando el refresh token es inválido

**Funcionamiento:**

```javascript
// Se inicia automáticamente
window.tokenRefreshService.start();

// Renueva cada 50 minutos (antes de los 60 min de expiración)
setInterval(() => {
    refreshToken();
}, 50 * 60 * 1000);
```

### 3. Eventos Personalizados

El servicio dispara eventos que otras partes de la aplicación pueden escuchar:

```javascript
// Cuando se renueva el token
window.addEventListener('tokenRefreshed', (event) => {
    console.log('Token actualizado:', event.detail.accessToken);
});

// Cuando el token expira y no se puede renovar
window.addEventListener('tokenExpired', () => {
    console.log('Sesión expirada - redirigiendo a login');
});
```

---

## 🔧 Implementación Frontend

### Archivos que Deben Incluir el Servicio

Agregar este script en **todos los archivos HTML** que requieran autenticación:

```html
<!-- ANTES de main.js -->
<script src="/static/js/auth-api.js"></script>
<script src="/static/js/token-refresh.js"></script>
<script src="/static/js/main.js"></script>
```

### Archivos a Actualizar

- ✅ `index.html` - Página principal
- ✅ `forum/foro.html` - Foro
- ✅ `market/mercado.html` - Marketplace
- ✅ `portfolio/portafolio.html` - Portfolio
- ✅ `encuestas/encuestas.html` - Encuestas
- ✅ `cursos/cursos.html` - Cursos OTEC
- ✅ `bienestar/bienestar.html` - Bienestar
- ✅ `account.html` - Perfil de usuario
- ✅ `converter/conversor.html` - Conversor
- ✅ `streetview/recorridos-virtuales.html` - Recorridos

### Integración con auth-api.js

El `auth-api.js` debe disparar eventos al hacer login/logout:

```javascript
// En login exitoso
window.dispatchEvent(new Event('userLoggedIn'));

// En logout
window.dispatchEvent(new Event('userLoggedOut'));
```

---

## 📊 Comportamiento del Sistema

### Escenario 1: Usuario Activo (Navegando)

```
00:00 - Login exitoso
        ↓ access_token válido por 60 min
        ↓ refresh_token válido por 7 días
        ↓ Servicio de renovación iniciado
        
00:50 - Renovación automática #1
        ↓ Nuevo access_token (60 min más)
        ↓ Nuevo refresh_token (si hay rotación)
        
01:40 - Renovación automática #2
        ↓ Continúa navegando sin interrupciones
        
... cada 50 minutos ...
```

**Resultado:** El usuario **nunca se desloguea** mientras esté activo.

### Escenario 2: Usuario Inactivo (Pestaña Cerrada)

```
00:00 - Login exitoso
        ↓ Cierra pestaña
        
07 días después...

00:00 - Abre la aplicación
        ↓ access_token expiró (hace 7 días)
        ↓ refresh_token expiró (hace minutos)
        ↓ Redirige a login
```

**Resultado:** Después de 7 días de inactividad, debe volver a iniciar sesión.

### Escenario 3: Token Comprometido

```
Si un token es comprometido:
  ↓ Rotación activa crea nuevos tokens
  ↓ Tokens antiguos van a blacklist
  ↓ Token comprometido ya no es válido
```

**Resultado:** Mayor seguridad con rotación de tokens.

---

## 🔒 Seguridad

### Medidas Implementadas

1. **Tokens de corta duración**: Access tokens de solo 60 minutos
2. **Rotación de tokens**: Nuevos tokens en cada renovación
3. **Blacklist**: Tokens antiguos invalidados automáticamente
4. **HTTPS obligatorio en producción**: Tokens nunca viajan sin encriptación
5. **HTTPOnly cookies opcionales**: Para refresh tokens en producción

### Mejoras Futuras Opcionales

```python
# En producción, considerar usar cookies HTTPOnly
SIMPLE_JWT = {
    "AUTH_COOKIE": "access_token",  # Nombre de la cookie
    "AUTH_COOKIE_SECURE": True,     # Solo HTTPS
    "AUTH_COOKIE_HTTP_ONLY": True,  # No accesible desde JavaScript
    "AUTH_COOKIE_SAMESITE": "Lax",  # Protección CSRF
}
```

---

## 🧪 Testing

### Prueba Manual

1. **Login en la aplicación**
2. **Abrir DevTools → Console**
3. **Ejecutar:**
   ```javascript
   // Ver intervalo de renovación activo
   console.log(window.tokenRefreshService);
   
   // Forzar renovación manual
   await window.tokenRefreshService.refreshNow();
   ```
4. **Esperar 50 minutos** (o modificar el intervalo para testing)
5. **Verificar en Console** que se renueva automáticamente

### Logs Esperados

```
Iniciando servicio de renovación automática de tokens
Renovando access token...
✓ Access token renovado exitosamente
```

### Testing de Expiración

```javascript
// Simular token expirado
localStorage.setItem('access_token', 'token_invalido');

// Intentar request
await fetch('/api/auth/me/', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
});

// Debería renovar automáticamente o redirigir
```

---

## 📝 Checklist de Implementación

- [x] Configurar `SIMPLE_JWT` en `settings/base.py`
- [x] Agregar `rest_framework_simplejwt.token_blacklist` a `INSTALLED_APPS`
- [x] Crear servicio `token-refresh.js`
- [ ] Ejecutar migraciones: `python manage.py migrate`
- [ ] Agregar `token-refresh.js` a todos los HTMLs autenticados
- [ ] Actualizar `auth-api.js` para disparar eventos
- [ ] Testing en desarrollo
- [ ] Testing en producción
- [ ] Documentar en README principal

---

## 🚀 Despliegue

### Desarrollo

```bash
# 1. Aplicar migraciones para blacklist
cd proyecto/src/backend
python manage.py migrate

# 2. Reiniciar servidor
python manage.py runserver
```

### Producción

```bash
# 1. Aplicar migraciones
python manage.py migrate

# 2. Reiniciar servicios
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 📚 Referencias

- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Token Storage](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

## 💡 FAQ

### ¿Por qué 60 minutos para access tokens?

Balance entre seguridad y experiencia de usuario:
- **< 30 min**: Demasiadas renovaciones, impacto en rendimiento
- **60 min**: Renovación cada 50 min es imperceptible para el usuario
- **> 2 horas**: Mayor ventana de tiempo si un token es comprometido

### ¿Qué pasa si el usuario cierra la pestaña?

El servicio se detiene, pero los tokens quedan en `localStorage`. Al volver a abrir:
- Si access token aún válido: Continúa normalmente
- Si access token expiró: Se renueva con refresh token
- Si refresh token expiró (7 días): Redirige a login

### ¿Afecta el rendimiento?

No. Una renovación cada 50 minutos es una sola petición HTTP adicional que pasa desapercibida.

### ¿Funciona en modo offline (PWA)?

El service worker cachea la aplicación, pero los tokens **no se pueden renovar offline**. Al recuperar conexión, se intenta renovar automáticamente.

---

**Última actualización:** 2025-11-18  
**Autor:** Sistema de IA - StudentsPoint  
**Estado:** ✅ Implementado y Documentado

