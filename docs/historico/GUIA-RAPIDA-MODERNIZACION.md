# Guia Rapida de Modernizacion de Modulos

## Template 1: HEAD Estandarizado

Reemplazar el `<head>` completo de cada módulo con:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[NOMBRE DEL MODULO] - StudentsPoint</title>
    
    <!-- Bootstrap 5.3.2 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome 6.5.1 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Custom Styles -->
    <link rel="stylesheet" href="/static/css/theme-dark.css">
    <link rel="stylesheet" href="/static/css/base-layout.css">
    <link rel="stylesheet" href="/static/css/animations.css">
    <link rel="stylesheet" href="[CSS ESPECIFICO DEL MODULO]">
    
    <!-- PWA -->
    <link rel="stylesheet" href="/static/manifest.json">
    <meta name="theme-color" content="#1a1a1b">
    <link rel="icon" href="/static/favicon.ico">
</head>
```

**Cambiar también**:
- `<html lang="es">` → `<html lang="es" data-bs-theme="dark">`
- `<body class="bg-light">` → `<body>`

## Template 2: Estructura BODY Completa

```html
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="brand-section">
                    <img src="/static/images/Logo_StudentsPoint.svg.png" alt="StudentsPoint" class="brand-logo">
                    <h1 class="brand-title">StudentsPoint</h1>
                </div>
                <div class="user-section">
                    <div class="user-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="user-info">
                        <span class="user-name" id="sidebarUserName">Cargando...</span>
                        <span class="user-role" id="sidebarUserRole">Estudiante</span>
                    </div>
                </div>
            </div>
            
            <div class="sidebar-menu">
                <a href="/" class="menu-item">
                    <i class="fas fa-home"></i>
                    <span>Inicio</span>
                </a>
                <a href="/forum/" class="menu-item">
                    <i class="fas fa-comments"></i>
                    <span>Foro</span>
                </a>
                <a href="/market/" class="menu-item">
                    <i class="fas fa-store"></i>
                    <span>Marketplace</span>
                </a>
                <a href="/portfolio/" class="menu-item">
                    <i class="fas fa-briefcase"></i>
                    <span>Portafolio</span>
                </a>
                <a href="/cursos/" class="menu-item">
                    <i class="fas fa-graduation-cap"></i>
                    <span>Cursos</span>
                </a>
                <a href="/encuestas/" class="menu-item">
                    <i class="fas fa-poll"></i>
                    <span>Encuestas</span>
                </a>
                <a href="/reportes/" class="menu-item">
                    <i class="fas fa-chart-bar"></i>
                    <span>Reportes</span>
                </a>
                <a href="/bienestar/" class="menu-item">
                    <i class="fas fa-heart"></i>
                    <span>Bienestar</span>
                </a>
                <a href="/converter/" class="menu-item">
                    <i class="fas fa-file-alt"></i>
                    <span>Conversor</span>
                </a>
                <a href="/streetview/" class="menu-item">
                    <i class="fas fa-map-marked-alt"></i>
                    <span>Recorridos</span>
                </a>
            </div>
            
            <div class="sidebar-footer">
                <a href="/account.html" class="menu-item">
                    <i class="fas fa-user-circle"></i>
                    <span>Mi Cuenta</span>
                </a>
                <a href="#" class="menu-item" onclick="logout(); return false;">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Cerrar Sesion</span>
                </a>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <header class="top-header">
                <h1 class="header-title">[TITULO DEL MODULO]</h1>
                <div class="header-actions">
                    <button class="btn-icon" id="notificationsBtn" title="Notificaciones">
                        <i class="fas fa-bell"></i>
                    </button>
                    <button class="btn-icon" id="settingsBtn" title="Configuracion">
                        <i class="fas fa-cog"></i>
                    </button>
                </div>
            </header>

            <div class="content-wrapper fade-in">
                <!-- AQUI VA TODO EL CONTENIDO ACTUAL DEL MODULO -->
                <!-- Envolver cards principales con clase "glass" -->
                <div class="glass p-4 mb-4">
                    <!-- Contenido -->
                </div>
            </div>
        </main>
    </div>

    <!-- TODOS LOS MODALES SE QUEDAN FUERA DEL app-container -->
    <!-- Scripts al final -->
</body>
```

## Instrucciones por Módulo

### 1. FORO (forum/foro.html)

**Pasos**:
1. Hacer backup: `copy foro.html foro.html.backup`
2. Reemplazar `<head>` con Template 1
3. Cambiar `<html lang="es">` → `<html lang="es" data-bs-theme="dark">`
4. Eliminar todo el `<nav class="navbar">...` (navbar antigua)
5. Agregar `<div class="app-container">` después de `<body>`
6. Pegar Template 2 del sidebar
7. Marcar item activo: `<a href="/forum/" class="menu-item active">`
8. Cambiar título: `[TITULO DEL MODULO]` → `Foro Estudiantil`
9. Envolver contenido principal en `<div class="content-wrapper fade-in">`
10. Agregar clase `glass` a divs principales:
    ```html
    <div class="glass p-4 mb-4">
        <!-- filtros aquí -->
    </div>
    
    <div class="glass p-4">
        <div id="postsContainer"></div>
    </div>
    ```
11. Cambiar botones principales:
    - `btn btn-primary` → `btn btn-gradient-purple`
    - `btn btn-success` → `btn btn-gradient-gold`
12. Cerrar `</main>`, `</div>` (app-container) antes de modales
13. Mantener TODOS los modales intactos
14. Probar funcionalidad

### 2. MARKETPLACE (market/mercado.html)

Mismos pasos que Foro, pero:
- Título: `Marketplace Estudiantil`
- Item activo: `<a href="/market/" class="menu-item active">`
- CSS específico: `/static/css/market.css`

### 3. REPORTES (reportes/reportes.html)

Mismos pasos, pero:
- Título: `Reportes y Estadísticas`
- Item activo: `<a href="/reportes/" class="menu-item active">`
- CSS específico: `/static/css/reportes.css`
- Glass effects en contenedores de gráficos

### 4. PERFIL (account.html)

Mismos pasos, pero:
- Título: `Mi Perfil`
- Item activo: ninguno (o marcar "Mi Cuenta" en footer)
- Glass effects en secciones del perfil

## Reemplazos Rápidos (Buscar y Reemplazar)

Usando el editor (Ctrl+H):

1. **Eliminar navbar antigua**:
   Buscar: `<nav class="navbar.*?</nav>`
   Reemplazar: *(vacío)*
   (Regex activado)

2. **Cambiar botones**:
   Buscar: `btn btn-primary`
   Reemplazar: `btn btn-gradient-purple`

3. **Cambiar background**:
   Buscar: `class="bg-light"`
   Reemplazar: *(vacío)*

4. **Agregar glass**:
   Buscar: `<div class="container`
   Reemplazar: `<div class="glass p-4 mb-4"><div class="container`
   *(Luego cerrar divs manualmente)*

## Checklist Post-Modernización

Después de cada módulo, verificar:

- [ ] Sidebar visible y funcional
- [ ] Navegación entre módulos funciona
- [ ] Contenido principal visible
- [ ] Todos los botones funcionan
- [ ] Modales se abren/cierran correctamente
- [ ] JavaScript sin errores (F12)
- [ ] Formularios funcionan
- [ ] API calls funcionan
- [ ] Responsive en móvil
- [ ] Tema oscuro aplicado

## Solución de Problemas

**Sidebar no visible**: Verificar que `/static/css/base-layout.css` esté cargado

**Contenido muy estrecho**: Asegurar que `content-wrapper` está dentro de `main-content`

**Botones sin estilo**: Verificar que `/static/css/theme-dark.css` esté cargado

**Modales no funcionan**: Asegurar que están FUERA de `app-container`

**JavaScript errors**: Verificar que no cambiaste IDs ni event listeners

## Tiempo Estimado

- Foro: 15-20 minutos
- Marketplace: 15 minutos
- Reportes: 10 minutos
- Perfil: 10 minutos

Total: ~1 hora con pruebas

## Resultado Final

Todos los módulos tendrán:
- ✅ Sidebar uniforme
- ✅ Tema oscuro consistente
- ✅ Efectos glass modernos
- ✅ Navegación intuitiva
- ✅ 100% de funcionalidad preservada

