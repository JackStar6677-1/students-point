# 🤖 Bot de Bienestar Estudiantil (Retell AI)

## 📋 Descripción

Se ha integrado un asistente virtual inteligente (SPBott) en el módulo de Bienestar Estudiantil utilizando la plataforma Retell AI. Este bot proporciona soporte y orientación a los estudiantes en temas relacionados con bienestar estudiantil.

## ✨ Características

### Configuración del Bot

- **Nombre**: SPBott
- **Color temático**: Morado (`#4b0082`) - Coincide con el tema de la aplicación
- **Logo**: Icono de robot violeta (combina con el tema morado)
- **Mensaje de bienvenida**: Personalizado con el nombre del usuario
- **Tiempo de popup automático**: 5 segundos
- **Apertura automática**: Desactivada (el usuario debe hacer clic)

### Funcionalidades Implementadas

1. **Integración Visual**
   - Diseño adaptado al tema dark de StudentsPoint
   - Animaciones suaves de entrada
   - Indicador de estado activo (punto verde pulsante)
   - Efectos hover y transiciones

2. **Responsive Design**
   - Adaptación automática a dispositivos móviles
   - Posicionamiento optimizado para no interferir con la navegación
   - Tamaño ajustable del chat según el dispositivo

3. **Personalización Dinámica**
   - Mensaje de bienvenida personalizado con el nombre del usuario
   - Se adapta al contexto del usuario logueado
   - Función programática para abrir el bot desde código

## 🎨 Personalización Visual

### Estilos Aplicados

```css
/* Características principales */
- Shadow con color morado temático
- Animación de pulse en el indicador de estado
- Transiciones suaves (0.3s ease)
- Border radius de 12px para consistencia con el diseño
- Z-index 1000 para asegurar visibilidad
```

### Posicionamiento

- **Desktop**: 
  - Bottom: 20px
  - Right: 20px
  
- **Mobile**: 
  - Bottom: 70px (evita colisión con navegación)
  - Right: 15px
  - Tamaño: 56x56px

## 🔧 Implementación Técnica

### Script Principal

```html
<script 
    id="retell-widget" 
    src="https://dashboard.retellai.com/retell-widget.js" 
    type="module" 
    data-public-key="public_key_185b63a3eada8d6f65c02" 
    data-agent-id="agent_447cb579449f02a59ec24fb63a" 
    data-title="SPBot" 
    data-logo-url="https://icones.pro/wp-content/uploads/2022/10/icone-robot-violet.png" 
    data-color="#4b0082" 
    data-bot-name="SPBott" 
    data-popup-message="Hola bienvenido a bienestar estudiantil" 
    data-show-ai-popup="true" 
    data-show-ai-popup-time="5" 
    data-auto-open="false">
</script>
```

### Función de Control Programático

```javascript
// Abrir el bot desde código JavaScript
window.abrirAsistenteBienestar();
```

Esta función permite abrir el chat del bot desde cualquier parte del código, útil para:
- Botones de ayuda personalizados
- Flujos guiados
- Respuestas a acciones específicas del usuario

## 📱 Experiencia de Usuario

### Flujo de Interacción

1. **Carga de la página**: El bot se inicializa en segundo plano
2. **5 segundos después**: Aparece mensaje de bienvenida personalizado
3. **Usuario interactúa**: Puede hacer clic en el botón flotante
4. **Chat abierto**: Interfaz conversacional completa
5. **Registro**: Las interacciones se registran en consola (preparado para analytics)

### Mensaje de Bienvenida Personalizado

```javascript
`¡Hola ${userName}! 👋 Soy SPBott, tu asistente de bienestar estudiantil. ¿En qué puedo ayudarte hoy?`
```

## 🔐 Configuración de Seguridad

### Claves y IDs

- **Public Key**: `public_key_185b63a3eada8d6f65c02`
- **Agent ID**: `agent_447cb579449f02a59ec24fb63a`

> ⚠️ **Nota**: Estas claves son públicas y están diseñadas para uso en el frontend. No exponen información sensible.

## 📊 Analytics y Monitoreo

### Eventos Registrados

```javascript
// Interacción con el bot
document.addEventListener('click', function(e) {
    if (e.target.closest('#retell-widget-button')) {
        console.log('🤖 Usuario interactuando con SPBott');
        // Integración con analytics futura
    }
});
```

### Posibles Métricas Futuras

- Número de interacciones
- Tiempo promedio de conversación
- Temas más consultados
- Satisfacción del usuario
- Horarios de mayor uso

## 🎯 Casos de Uso

### Temas que Puede Abordar el Bot

1. **Salud Mental**
   - Consejos de manejo de estrés
   - Técnicas de relajación
   - Recursos de apoyo psicológico

2. **Salud Física**
   - Rutinas de ejercicio
   - Consejos nutricionales
   - Pausas activas

3. **Recursos Institucionales**
   - Información sobre servicios de bienestar
   - Horarios de atención
   - Contactos de emergencia

4. **Orientación General**
   - Guía sobre el uso del módulo de bienestar
   - Recomendaciones personalizadas
   - FAQs

## 🛠️ Mantenimiento

### Actualizar Configuración

Para modificar el bot, editar los atributos `data-*` en el script:

```html
data-title="Nuevo Título"
data-color="#nuevo-color"
data-popup-message="Nuevo mensaje"
```

### Cambiar Comportamiento

```javascript
// Cambiar tiempo de popup (en segundos)
data-show-ai-popup-time="10"

// Habilitar apertura automática
data-auto-open="true"

// Deshabilitar popup
data-show-ai-popup="false"
```

## 🔄 Actualizaciones Futuras

### Mejoras Planificadas

- [ ] Integración con sistema de analytics
- [ ] Respuestas basadas en la carrera del estudiante
- [ ] Integración con calendario de actividades de bienestar
- [ ] Notificaciones proactivas basadas en uso de la plataforma
- [ ] Conexión con sistema de tickets de soporte
- [ ] Historial de conversaciones del usuario
- [ ] Modo de voz (aprovechando capacidades de Retell AI)

### Personalización Avanzada

```javascript
// Ejemplo de personalización según contexto
const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
const context = {
    carrera: userData.career,
    sede: userData.campus,
    rol: userData.role
};

// Enviar contexto al bot (implementación futura)
window.retellWidget.setContext(context);
```

## 📞 Soporte

### Retell AI Dashboard

- **URL**: https://dashboard.retellai.com
- **Documentación**: https://docs.retellai.com

### Configuración del Agente

Para modificar el comportamiento del agente (prompts, voz, idioma):
1. Acceder al dashboard de Retell AI
2. Buscar agente: `agent_447cb579449f02a59ec24fb63a`
3. Modificar configuración según necesidades
4. Los cambios se reflejan automáticamente sin necesidad de actualizar código

## 🎓 Ejemplo de Uso

```javascript
// Abrir bot cuando usuario hace clic en "Necesito Ayuda"
document.getElementById('btnAyuda').addEventListener('click', function() {
    window.abrirAsistenteBienestar();
});

// Abrir bot si usuario lleva mucho tiempo en la página
setTimeout(function() {
    if (paginaAbiertaPorMasDeMinutos(5)) {
        window.abrirAsistenteBienestar();
    }
}, 300000); // 5 minutos
```

## ✅ Checklist de Implementación

- [x] Script del widget integrado
- [x] Estilos personalizados aplicados
- [x] Responsive design implementado
- [x] Animaciones agregadas
- [x] Personalización de mensajes
- [x] Función de apertura programática
- [x] Logging básico de interacciones
- [x] Documentación completa
- [ ] Integración con analytics (pendiente)
- [ ] Tests de usabilidad (pendiente)

## 🚀 Despliegue

El bot está activo automáticamente en:
- `/bienestar/` - Módulo de Bienestar Estudiantil
- Funciona en todas las rutas donde esté incluido el archivo `bienestar.html`

No requiere configuración adicional del servidor backend.

---

**Última actualización**: Noviembre 2025  
**Versión del widget**: 1.0  
**Estado**: ✅ Activo en producción

