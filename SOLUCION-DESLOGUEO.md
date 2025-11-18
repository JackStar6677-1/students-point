# ✅ SOLUCIÓN AL PROBLEMA DE DESLOGUEO AUTOMÁTICO

## 📋 Problema Solucionado

**Síntoma:** Usuarios se deslogueaban inesperadamente mientras navegaban.

**Causa:** Los tokens JWT de acceso expiraban después de un tiempo (no estaba configurado el tiempo de expiración), el frontend detectaba el 401 y los deslogueaba automáticamente.

---

## 🔧 Cambios Implementados

### 1. ✅ Configuración de JWT (`studentspoint/settings/base.py`)

```python
SIMPLE_JWT = {
    # Tokens de acceso duran 60 minutos (1 hora)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Tokens de refresh duran 7 días  
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    
    # Rotación y blacklist para seguridad
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

**Agregado:**
- `rest_framework_simplejwt.token_blacklist` a `INSTALLED_APPS`
- Configuración completa de SIMPLE_JWT
- Import de `timedelta` al inicio del archivo

### 2. ✅ Servicio de Renovación Automática (`static/js/token-refresh.js`)

**Características:**
- Renueva el access_token automáticamente cada **50 minutos**
- Se inicia automáticamente al detectar tokens en localStorage
- Detiene el servicio al hacer logout
- Maneja tokens expirados correctamente

```javascript
// Se auto-inicia al cargar la página
window.tokenRefreshService.start();

// Renueva cada 50 min (antes de expirar a los 60)
setInterval(() => refreshToken(), 50 * 60 * 1000);
```

### 3. ✅ Eventos en `auth-api.js`

**Modificado:**
- `login()`: Dispara evento `userLoggedIn` después de guardar tokens
- `logout()`: Dispara evento `userLoggedOut` antes de redirigir

### 4. ✅ Migraciones Ejecutadas

```bash
✓ token_blacklist.0001_initial
✓ token_blacklist.0002_outstandingtoken_jti_hex
... (12 migraciones aplicadas)
```

---

## 📝 Qué Hacer Ahora

### PASO 1: Agregar el script a los HTMLs

Agrega este script **ANTES de `main.js`** en todos los archivos HTML que requieren autenticación:

```html
<!-- Scripts de autenticación y renovación de tokens -->
<script src="/static/js/auth-api.js"></script>
<script src="/static/js/token-refresh.js"></script> <!-- NUEVO -->
<script src="/static/js/main.js"></script>
```

**Archivos a modificar:**

- ✅ `static/index.html` - Página principal
- ✅ `forum/foro.html` - Foro
- ✅ `market/mercado.html` - Marketplace  
- ✅ `portfolio/portafolio.html` - Portfolio
- ✅ `encuestas/encuestas.html` - Encuestas
- ✅ `cursos/cursos.html` - Cursos OTEC
- ✅ `bienestar/bienestar.html` - Bienestar
- ✅ `account.html` - Perfil de usuario
- ✅ `converter/conversor.html` - Conversor
- ✅ `streetview/recorridos-virtuales.html` - Recorridos

**NO agregar en:**
- ❌ `login.html` (no hay sesión activa)
- ❌ `register.html` (no hay sesión activa)
- ❌ `verify-email.html` (no requiere token)

### PASO 2: Reiniciar el servidor

```bash
# Ctrl+C para detener el servidor actual

# Reiniciar
cd proyecto/src/backend
python manage.py runserver
```

### PASO 3: Probar la solución

1. **Hacer login** en la aplicación
2. **Abrir DevTools** (F12) → Console
3. **Verificar logs:**
   ```
   Iniciando servicio de renovación automática de tokens
   Detectados tokens - iniciando servicio de renovación
   ```
4. **Esperar 50 minutos** o modificar temporalmente el intervalo para testing:
   ```javascript
   // En token-refresh.js línea 12, cambiar temporalmente a 1 minuto
   this.refreshIntervalMs = 1 * 60 * 1000; // 1 minuto
   ```
5. **Observar renovación automática:**
   ```
   Renovando access token...
   ✓ Access token renovado exitosamente
   ```

---

## 🎯 Comportamiento Esperado

### ✅ Usuario Activo (Navegando)
```
Login → Navegando por 50 min → Renovación automática → Continúa navegando
      → Otros 50 min → Renovación automática → Sin interrupciones
```
**Resultado:** El usuario **NUNCA se desloguea** mientras esté navegando.

### ✅ Usuario Inactivo (Pestaña Cerrada)
```
Login → Cierra pestaña → 7 días después → Abre app → Redirige a login
```
**Resultado:** Después de **7 días** de inactividad, debe volver a iniciar sesión.

### ✅ Token Inválido/Expirado
```
Token expirado → Intenta renovar → Refresh token inválido → Logout automático
```
**Resultado:** Logout suave con mensaje (opcional agregar en UI).

---

## 🐛 Troubleshooting

### Error: "tokenRefreshService is not defined"

**Causa:** El script `token-refresh.js` no está cargado.

**Solución:** Verificar que esté agregado en el HTML:
```html
<script src="/static/js/token-refresh.js"></script>
```

### El token no se renueva automáticamente

**Diagnóstico:**
```javascript
// En Console
console.log(window.tokenRefreshService);
// Debería mostrar el objeto con refreshInterval activo
```

**Soluciones:**
1. Verificar que se disparó el evento `userLoggedIn`
2. Verificar que hay tokens en `localStorage`:
   ```javascript
   localStorage.getItem('access_token');
   localStorage.getItem('refresh_token');
   ```
3. Ver errores en Console durante la renovación

### Sigue deslogueándose

**Posibles causas:**
1. El endpoint `/api/auth/token/refresh/` no existe o no funciona
2. El `refresh_token` está inválido o expiró
3. La configuración de SIMPLE_JWT no se aplicó correctamente

**Verificación:**
```bash
# Probar endpoint de refresh manualmente
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "TU_REFRESH_TOKEN_AQUI"}'
```

---

## 📊 Logs para Monitorear

### En el Frontend (Console)
```
Detectados tokens - iniciando servicio de renovación
Iniciando servicio de renovación automática de tokens
Renovando access token...
✓ Access token renovado exitosamente
```

### En el Backend (logs/api.log)
```
[INFO] POST /api/auth/token/refresh/ - Status: 200
[INFO] Refresh token renovado para usuario: email@duocuc.cl
```

---

## 📚 Documentación Completa

Ver: `docs/guias/SOLUCION-DESLOGUEO-AUTOMATICO.md`

Incluye:
- Explicación técnica detallada
- Diagramas de flujo
- Consideraciones de seguridad
- Referencias y mejores prácticas
- FAQ extendido

---

## ✅ Checklist de Implementación

- [x] Configurar SIMPLE_JWT en settings
- [x] Agregar token_blacklist a INSTALLED_APPS
- [x] Crear servicio token-refresh.js
- [x] Actualizar auth-api.js con eventos
- [x] Ejecutar migraciones
- [ ] Agregar token-refresh.js a todos los HTMLs
- [ ] Reiniciar servidor
- [ ] Testing en desarrollo
- [ ] Testing en producción
- [ ] Documentar en README principal

---

**Estado:** ✅ Implementado (Falta agregar scripts a HTMLs)
**Última actualización:** 2025-11-18
**Autor:** Sistema de IA - StudentsPoint

