"""
Script para poblar la base de datos con contenido de bienestar
específico para Ingeniería en Informática
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentspoint.settings')
django.setup()

from studentspoint.apps.wellbeing.models import BienestarItem

CARRERA = "Ingeniería en Informática"

# Contenidos de Bienestar Físico
contenidos_fisicos = [
    {
        "tipo": BienestarItem.Tipos.FISICO,
        "categoria": BienestarItem.Categorias.POSTURA,
        "titulo": "Ergonomía para Programadores",
        "descripcion_corta": "Aprende la postura correcta para largas jornadas frente al computador",
        "duracion_minutos": 5,
        "orden": 1,
        "contenido_md": """
# Ergonomía para Programadores

## ¿Por qué es importante?
Pasar muchas horas frente al computador puede causar problemas de postura y dolores crónicos.

## Posición correcta del monitor
- **Altura**: La parte superior del monitor debe estar a la altura de los ojos
- **Distancia**: 50-70 cm de distancia de tus ojos
- **Ángulo**: Ligeramente inclinado hacia atrás (10-20 grados)

## Postura en la silla
1. **Pies**: Apoyados completamente en el suelo
2. **Rodillas**: En ángulo de 90 grados
3. **Espalda**: Recta, apoyada en el respaldo
4. **Brazos**: En ángulo de 90 grados, antebrazos paralelos al suelo
5. **Muñecas**: Rectas, no dobladas

## Configuración del teclado y mouse
- Teclado: A la misma altura que tus codos
- Mouse: Cerca del teclado, al mismo nivel
- Evita estirar el brazo para alcanzarlos

## Regla 20-20-20
Cada 20 minutos, mira algo a 20 pies de distancia (6 metros) por 20 segundos.

## Tips adicionales
- Ajusta el brillo de la pantalla (no muy brillante)
- Usa una silla con soporte lumbar
- Mantén objetos de uso frecuente cerca
- Considera un soporte para laptop si trabajas en una
        """,
        "media_url": "https://www.youtube.com/watch?v=F8_ME4VwTiw"
    },
    {
        "tipo": BienestarItem.Tipos.FISICO,
        "categoria": BienestarItem.Categorias.EJERCICIOS_OCULARES,
        "titulo": "Ejercicios para Cuidar tu Vista",
        "descripcion_corta": "Ejercicios simples para reducir la fatiga visual por pantallas",
        "duracion_minutos": 3,
        "orden": 2,
        "contenido_md": """
# Cuidado Visual para Desarrolladores

## Síndrome Visual Informático (SVI)
El uso prolongado de pantallas puede causar:
- Ojos secos
- Visión borrosa
- Dolores de cabeza
- Fatiga visual

## Ejercicios de Relajación Visual

### 1. Parpadeo Consciente
- Parpadea 10 veces lentamente
- Hazlo cada 20 minutos
- Ayuda a lubricar los ojos

### 2. Palming (Calor en los ojos)
1. Frota tus manos hasta que estén calientes
2. Cierra los ojos
3. Coloca las palmas sobre tus párpados cerrados
4. Respira profundamente por 30 segundos
5. Repite 3 veces

### 3. Enfoque Lejano-Cercano
1. Enfoca un objeto cercano (30 cm) por 5 segundos
2. Cambia el enfoque a un objeto lejano (6 metros) por 5 segundos
3. Repite 10 veces

### 4. Movimientos Oculares
- Mira arriba y abajo: 10 veces
- Mira izquierda y derecha: 10 veces
- Dibuja círculos con los ojos: 5 veces cada dirección

### 5. Masaje Ocular
1. Cierra los ojos
2. Con las yemas de los dedos, masajea suavemente alrededor de los ojos
3. Hazlo en movimientos circulares por 30 segundos

## Prevención
- Usa filtros de luz azul o modo nocturno
- Mantén la pantalla limpia
- Ajusta el brillo y contraste
- Usa lágrimas artificiales si es necesario
- Descansa tus ojos cada hora

## Configuración de Pantalla Ideal
- **Brillo**: Igual que el ambiente
- **Contraste**: Alto, texto negro sobre fondo blanco
- **Tamaño de fuente**: Al menos 12pt
- **Filtro de luz azul**: Activo después de las 6 PM
        """,
        "media_url": ""
    },
    {
        "tipo": BienestarItem.Tipos.FISICO,
        "categoria": BienestarItem.Categorias.ESTIRAMIENTOS,
        "titulo": "Estiramientos Anti-Dolor de Cuello y Hombros",
        "descripcion_corta": "Rutina de 5 minutos para aliviar tensión por largas horas de código",
        "duracion_minutos": 5,
        "orden": 3,
        "contenido_md": """
# Estiramientos para Programadores

## ¿Por qué estirarse?
- Reduce tensión muscular
- Previene lesiones
- Mejora circulación
- Aumenta concentración

## Rutina de 5 Minutos

### 1. Cuello (1 minuto)

**Inclinación lateral**:
- Inclina la cabeza hacia un hombro
- Mantén 10 segundos
- Repite del otro lado (3 veces cada lado)

**Rotación**:
- Gira la cabeza lentamente a la izquierda
- Mantén 5 segundos
- Gira a la derecha
- Repite 5 veces

**Flexión y extensión**:
- Lleva el mentón al pecho (10 seg)
- Mira hacia el techo (10 seg)
- Repite 3 veces

### 2. Hombros (1 minuto)

**Encogimientos**:
- Sube ambos hombros hacia las orejas
- Mantén 5 segundos
- Suéltalos relajadamente
- Repite 10 veces

**Rotaciones circulares**:
- Gira los hombros hacia atrás 10 veces
- Gira los hombros hacia adelante 10 veces

### 3. Brazos y Muñecas (1 minuto)

**Estiramiento de antebrazo**:
- Extiende un brazo con la palma hacia arriba
- Con la otra mano, tira los dedos hacia abajo
- Mantén 15 segundos cada brazo

**Círculos de muñeca**:
- Gira las muñecas en círculos
- 10 veces en cada dirección

**Apretones de puño**:
- Cierra los puños fuertemente (5 seg)
- Abre y estira los dedos lo más posible (5 seg)
- Repite 10 veces

### 4. Espalda (1 minuto)

**Giro de torso sentado**:
- Sentado, gira el torso a la derecha
- Agarra el respaldo de la silla
- Mantén 15 segundos
- Repite del otro lado

**Estiramiento de gato-vaca**:
- Si puedes ponerte de pie: arquea la espalda, luego encórvala
- Repite 10 veces lentamente

### 5. Piernas (1 minuto)

**Elevación de piernas**:
- Sentado, extiende una pierna
- Mantén 10 segundos
- Alterna entre piernas (5 veces cada una)

**Círculos de tobillo**:
- Gira los tobillos en círculos
- 10 veces cada dirección

## Frecuencia Recomendada
- Cada 1-2 horas de trabajo
- Al menos 3 veces al día
- Antes y después de sesiones largas de coding

## Pro Tip
Programa una alarma cada hora para recordarte estirarte. Tu cuerpo te lo agradecerá.
        """,
        "media_url": "https://www.youtube.com/watch?v=q6e0Nfk_M1s"
    },
    {
        "tipo": BienestarItem.Tipos.FISICO,
        "categoria": BienestarItem.Categorias.PAUSAS_ACTIVAS,
        "titulo": "Pausas Activas Express (2 minutos)",
        "descripcion_corta": "Ejercicios rápidos para hacer entre bloques de código",
        "duracion_minutos": 2,
        "orden": 4,
        "contenido_md": """
# Pausas Activas para Developers

## ¿Qué son las pausas activas?
Breves momentos de movimiento que interrumpen el sedentarismo y reactivan el cuerpo.

## Rutina Express (2 minutos)

### Opción 1: En tu escritorio
1. **Párate y siéntate**: 10 veces seguidas
2. **Elevación de talones**: Sube y baja sobre las puntas de los pies (20 veces)
3. **Sentadillas en la silla**: Baja casi a sentarte y levántate (10 veces)
4. **Marcha en el lugar**: Levanta las rodillas alto (30 segundos)

### Opción 2: Movimiento de brazos
1. **Brazos arriba**: Estira los brazos hacia el techo (10 seg)
2. **Abrazo**: Cruza los brazos y abrázate (10 seg)
3. **Círculos de brazos**: Grandes círculos con ambos brazos (10 veces)
4. **Boxeo suave**: Golpes al aire, alterna brazos (30 seg)

### Opción 3: Micro-cardio
1. **Saltos suaves**: Pequeños saltos en el lugar (20 veces)
2. **Rodillas altas**: Trota elevando rodillas (20 seg)
3. **Talones al glúteo**: Trota llevando talones atrás (20 seg)
4. **Jumping jacks suaves**: Abre y cierra brazos y piernas (15 veces)

## Cuándo hacer pausas activas
- Después de resolver un bug difícil ✅
- Antes de una reunión 👔
- A media mañana (11 AM) ☕
- A media tarde (3 PM) 🌅
- Cada vez que subes un commit importante 🚀

## Beneficios
- Mejora circulación sanguínea
- Aumenta oxigenación del cerebro
- Reduce riesgo de problemas cardiovasculares
- Mejora el estado de ánimo
- Aumenta productividad

## Challenge
Intenta hacer al menos una pausa activa cada hora durante una semana. 
Notarás la diferencia.
        """,
        "media_url": ""
    },
]

# Contenidos de Bienestar Mental
contenidos_mentales = [
    {
        "tipo": BienestarItem.Tipos.MENTAL,
        "categoria": BienestarItem.Categorias.ESTRES,
        "titulo": "Manejo del Estrés en Épocas de Exámenes",
        "descripcion_corta": "Técnicas probadas para mantener la calma durante períodos intensos",
        "duracion_minutos": 10,
        "orden": 5,
        "contenido_md": """
# Manejo del Estrés para Estudiantes de Informática

## Identificando el Estrés
### Señales físicas:
- Tensión muscular
- Dolor de cabeza
- Problemas para dormir
- Fatiga constante

### Señales mentales:
- Dificultad para concentrarse
- Pensamientos negativos recurrentes
- Irritabilidad
- Sensación de estar abrumado

## Técnicas de Manejo

### 1. Respiración 4-7-8
1. Exhala completamente por la boca
2. Inhala por la nariz contando hasta 4
3. Mantén el aire contando hasta 7
4. Exhala por la boca contando hasta 8
5. Repite 4 veces

**Úsala cuando**: Te sientes ansioso, antes de un examen, o antes de dormir

### 2. Técnica Pomodoro Modificada
- 25 min de estudio concentrado
- 5 min de descanso activo
- Cada 4 pomodoros: 15-30 min de descanso largo

**Durante los descansos**:
- Camina
- Estírate
- Respira profundamente
- Toma agua

### 3. Priorización con Matriz de Eisenhower
Clasifica tus tareas en:
- **Urgente e Importante**: Hazlo YA
- **Importante, no urgente**: Programa tiempo
- **Urgente, no importante**: Delega o minimiza
- **Ni urgente ni importante**: Elimina

### 4. Mindfulness para Programadores
**Meditación del código**:
1. Siéntate cómodamente
2. Cierra los ojos
3. Visualiza líneas de código fluyendo
4. Cuando aparezca un pensamiento estresante, déjalo pasar como un comentario
5. Vuelve a visualizar el código fluyendo
6. Hazlo por 5 minutos

### 5. Journaling Anti-Estrés
**Al final del día, escribe**:
- 3 cosas que lograste hoy
- 1 desafío que superaste
- 1 cosa por la que estás agradecido
- Tus pendientes para mañana (máximo 3 prioritarios)

## Prevención del Estrés

### Organización
- Usa herramientas: Trello, Notion, GitHub Projects
- Desglosa proyectos grandes en tareas pequeñas
- Establece deadlines realistas

### Rutina Saludable
- Duerme 7-8 horas
- Come regularmente
- Haz ejercicio (aunque sean 15 min al día)
- Mantén contacto social

### Límites Digitales
- No revises el correo después de las 8 PM
- Desactiva notificaciones durante estudio profundo
- Ten un "día de descanso" sin código

## Cuándo Buscar Ayuda
Si experimentas:
- Ataques de pánico
- Pensamientos suicidas
- Imposibilidad de realizar actividades diarias
- Aislamiento prolongado

**Contacta**:
- Servicio de psicología de la universidad
- Salud estudiantil
- Línea de ayuda: 600 360 7777 (Salud Responde)

## Recuerda
El estrés es normal. Lo importante es manejarlo de forma saludable.
**Eres más que tus notas, tus proyectos o tu código.**
        """,
        "media_url": ""
    },
    {
        "tipo": BienestarItem.Tipos.MENTAL,
        "categoria": BienestarItem.Categorias.ANSIEDAD,
        "titulo": "Ansiedad por Programación: Síndrome del Impostor",
        "descripcion_corta": "Cómo lidiar con la sensación de no ser suficientemente bueno",
        "duracion_minutos": 8,
        "orden": 6,
        "contenido_md": """
# Síndrome del Impostor en Informática

## ¿Qué es?
La sensación persistente de que:
- No eres tan inteligente como los demás piensan
- Tus logros son suerte, no habilidad
- Pronto serás "descubierto" como un fraude
- Todos los demás saben más que tú

## ¿Por qué es común en Informática?
1. **Cambio constante**: Siempre hay tecnologías nuevas por aprender
2. **Cultura de comparación**: GitHub, Stack Overflow, redes sociales
3. **Complejidad**: Es imposible saberlo todo
4. **Autodidactas**: Muchos aprenden solos y dudan de su conocimiento

## Señales de Síndrome del Impostor
- Atribuyes tus éxitos a la suerte
- Miedo a ser cuestionado
- Perfeccionismo extremo
- Evitas desafíos por miedo a fallar
- Te comparas constantemente con otros

## Estrategias para Superarlo

### 1. Documenta tus logros
Crea un archivo "wins.md":
```markdown
# Mis Logros en Programación

## 2024
- [x] Completé mi primer proyecto full-stack
- [x] Resolví un bug complejo en producción
- [x] Ayudé a un compañero a entender recursión
- [x] Aprendí React y construí una app funcional
```

Léelo cuando te sientas impostor.

### 2. Reframe tus pensamientos
**En vez de**: "No sé nada"
**Di**: "Estoy aprendiendo constantemente"

**En vez de**: "Todos saben más que yo"
**Di**: "Cada uno tiene fortalezas diferentes"

**En vez de**: "Tuve suerte"
**Di**: "Trabajé duro y lo logré"

### 3. Comparte tus luchas
- Habla con compañeros sobre tus dudas
- Descubrirás que muchos sienten lo mismo
- La vulnerabilidad crea conexión

### 4. Acepta que NO saber es normal
- Nadie sabe TODO sobre programación
- Senior developers también consultan Stack Overflow
- Hacer preguntas es señal de inteligencia, no ignorancia

### 5. Practica la "Exposición Progresiva"
Hazte visible gradualmente:
1. **Semana 1**: Comenta en un foro
2. **Semana 2**: Haz una pregunta en clase
3. **Semana 3**: Comparte un pequeño proyecto
4. **Semana 4**: Ayuda a alguien con un problema

### 6. Encuentra mentores
- Alguien que ya pasó por donde estás
- Te darán perspectiva
- Te recordarán que todos empezamos desde cero

## Técnica: El "Mapa de Conocimiento"

Crea un mapa visual:
- **Centro**: Lo que dominas
- **Capa 2**: Lo que conoces parcialmente
- **Capa 3**: Lo que has visto
- **Exterior**: Lo que existe pero no conoces

Verás que tu "Centro" es más grande de lo que crees.

## Ejercicio Práctico

**"De Junior a Senior en mi mente"**:

Escribe respuestas a:
1. ¿Qué sabía hace 1 año?
2. ¿Qué sé ahora?
3. ¿Qué problemas he resuelto?
4. ¿Qué le enseñaría a mi yo del pasado?

Esto te muestra tu progreso real.

## Mantras Anti-Impostor

- "Estoy exactamente donde debo estar"
- "Mi valor no depende de mi código"
- "Cada expert fue alguna vez un principiante"
- "No sé todo, pero sé suficiente para seguir aprendiendo"

## Comunidad de Apoyo
Busca:
- **r/learnprogramming**: Reddit community de aprendizaje
- **Dev.to**: Blogging platform para developers
- **CodeNewbie**: Podcast y comunidad
- **Grupos de estudio**: En tu universidad o Discord

## Recuerda
El síndrome del impostor es señal de que te importa. 
Los verdaderos impostores no se preocupan por ser impostores.
        """,
        "media_url": ""
    },
    {
        "tipo": BienestarItem.Tipos.MENTAL,
        "categoria": BienestarItem.Categorias.CONCENTRACION,
        "titulo": "Deep Work: Concentración Profunda para Programar",
        "descripcion_corta": "Técnicas para entrar en estado de flow y maximizar productividad",
        "duracion_minutos": 12,
        "orden": 7,
        "contenido_md": """
# Concentración Profunda para Programadores

## ¿Qué es Deep Work?
Estado de concentración intensa donde:
- Produces tu mejor código
- Aprendes conceptos complejos rápidamente
- Resuelves problemas difíciles
- El tiempo "vuela"

## El Costo de las Distracciones

**Un solo ping de Whatsapp**: 23 minutos para volver al flow

**Multitasking**: Reduce productividad en 40%

**Notificaciones constantes**: Aumentan el estrés y reducen la calidad del trabajo

## Preparando tu Entorno

### 1. Configuración Física
- **Escritorio limpio**: Solo lo esencial
- **Buena iluminación**: Preferiblemente natural
- **Temperatura**: 20-22°C es ideal
- **Sonido**: Silencio o música sin letra

### 2. Configuración Digital

**Modo Focus en Mac/iOS**:
```bash
# Configura un modo "Deep Code"
- Bloquea todas las notificaciones
- Permite solo llamadas de emergencia
- Pantalla en blanco y negro (reduce distracción)
```

**Extensiones de Chrome útiles**:
- **Forest**: Planta un árbol mientras trabajas
- **StayFocusd**: Bloquea sitios distractores
- **News Feed Eradicator**: Elimina feed de redes sociales

**VS Code - Modo Zen**:
```
Ctrl/Cmd + K → Z
```
Pantalla completa sin distracciones.

### 3. Configuración Mental
- Mentalidad: "Las próximas 2 horas son sagradas"
- Objetivo claro: "Voy a implementar la autenticación JWT"
- Sin expectativas irreales: "Avanzaré lo que pueda, sin presión"

## Técnicas de Concentración

### 1. Timeboxing con Pomodoro Extendido
Para deep work:
- **50 min** de concentración intensa
- **10 min** de descanso
- Repite 3 veces
- **Descanso largo**: 30 min

### 2. Time Blocking en el calendario
Ejemplo de un día productivo:

```
09:00 - 11:00: Deep Work - Desarrollo feature X
11:00 - 11:30: Break + Responder emails
11:30 - 13:00: Deep Work - Debugging
13:00 - 14:00: Almuerzo
14:00 - 15:30: Deep Work - Code review
15:30 - 16:00: Meetings permitidas
16:00 - 17:30: Shallow work - Testing, docs
17:30 - 18:00: Planeación del día siguiente
```

### 3. La Regla del "No Multitasking"
**Una ventana = Un proyecto**

Cierra TODO lo demás:
- Email
- Slack
- Pestañas irrelevantes
- Segundo monitor (si distrae)

### 4. Pre-Loading Mental
Antes de empezar:
1. Lee el código relacionado (5 min)
2. Anota el objetivo en un papel
3. Desglosa en subtareas
4. Respira profundo 3 veces
5. ¡Comienza!

### 5. Ciclo de Carga Mental
**Primer Pomodoro**: Calentamiento (50% productividad)
**Segundo-Tercero**: Peak flow (100% productividad)
**Cuarto+**: Disminuye (70% productividad)

**Conclusión**: Programa tareas difíciles para el segundo y tercer bloque.

## Señales de que Estás en Flow
✅ El tiempo pasa sin notarlo
✅ No sientes hambre ni sed
✅ Las distracciones no te afectan
✅ El código "fluye naturalmente"
✅ Te sientes energizado (no cansado)

## Señales de Fatiga Mental
❌ Relees el mismo código sin entenderlo
❌ Errores tontos repetidos
❌ Frustración excesiva
❌ Buscas distracciones activamente

**Solución**: Para. Descansa 15-30 min. Vuelve fresco.

## Optimización por Hora del Día

**Mañana (7-11 AM)**: 
- Mejor momento para deep work
- Resuelve los problemas más difíciles

**Mediodía (11-14)**: 
- Energía media
- Bueno para reuniones y colaboración

**Tarde (14-17)**: 
- Post-almuerzo: baja energía (14-15)
- Segundo pico: 15-17
- Ideal para tareas creativas

**Noche (17-21)**:
- Algunos son más productivos aquí
- Menos distracciones
- Cuidado con afectar el sueño

## Entrenando tu Concentración

**Semana 1**: 25 min sin distracciones
**Semana 2**: 40 min sin distracciones
**Semana 3**: 60 min sin distracciones
**Semana 4+**: 90 min sin distracciones

Como un músculo, se fortalece con práctica.

## Herramientas Recomendadas

**Para bloquear distracciones**:
- Freedom
- Cold Turkey
- Forest
- Focus@Will (música para concentración)

**Para tracking**:
- Toggl Track
- RescueTime
- ActivityWatch

**Para planificación**:
- Notion
- Obsidian
- Trello con time blocking

## Deep Work Ritual

**Inicio** (5 min):
1. Limpia escritorio
2. Cierra todas las ventanas
3. Pon temporizador de 50 min
4. Respira profundo 3 veces
5. Escribe tu objetivo
6. Comienza

**Fin** (5 min):
1. Commit y push tu código
2. Anota lo que lograste
3. Anota pendientes para la próxima sesión
4. Estírate y toma agua
5. Descansa genuinamente

## Mentalidad del Día siguiente

**Antes de dormir**:
- Anota las 3 tareas prioritarias de mañana
- Visualízate completándolas
- Tu cerebro procesará soluciones mientras duermes

## Recuerda
La capacidad de concentración profunda es el superpoder del siglo XXI.
Quienes la dominen, destacarán.
        """,
        "media_url": "https://www.youtube.com/watch?v=gTaJhjQHcf8"
    },
    {
        "tipo": BienestarItem.Tipos.MENTAL,
        "categoria": BienestarItem.Categorias.DESCANSO,
        "titulo": "Optimiza tu Sueño como Optimizas tu Código",
        "descripcion_corta": "La guía definitiva para dormir mejor y rendir más",
        "duracion_minutos": 10,
        "orden": 8,
        "contenido_md": """
# Guía del Sueño para Programadores

## Por qué el Sueño es tu Debug Tool más Importante

**Después de una noche sin dormir**:
- ❌ 30% menos de productividad
- ❌ 40% menos de creatividad
- ❌ Más bugs en el código
- ❌ Decisiones pobres
- ❌ Memoria de corto plazo afectada

**Después de 7-9 horas de sueño**:
- ✅ Soluciones creativas a problemas
- ✅ Mejor retención de lo aprendido
- ✅ Código más limpio
- ✅ Estado de ánimo positivo
- ✅ Sistema inmune fuerte

## La Ciencia del Sueño

### Fases del Sueño
1. **NREM 1-2** (Sueño ligero): 50% del tiempo
2. **NREM 3** (Sueño profundo): 20% - Recuperación física
3. **REM** (Sueño MOR): 25% - Consolidación de memoria y aprendizaje

**Un ciclo completo**: 90 minutos
**Ciclos por noche**: 4-6 (idealmente 5)

### Cálculo de Hora de Despertar

Si necesitas despertar a las 7 AM:
- 5 ciclos: Dormir a las 22:30 (7.5 horas)
- 6 ciclos: Dormir a las 21:00 (9 horas)

Usa: **sleepyti.me** para calcular

## Higiene del Sueño - Best Practices

### 1. Luz (el factor #1)

**Durante el día**:
- Exponte a luz brillante apenas despiertes
- Trabaja cerca de ventanas si es posible
- Sal al exterior al menos 15 min

**De noche (2 horas antes de dormir)**:
- Activa modo nocturno en dispositivos
- Usa `f.lux` o Night Shift
- Baja las luces de tu casa
- Evita luces LED azules

### 2. Temperatura

**Dormitorio ideal**: 16-19°C

Tu cuerpo necesita bajar temperatura para dormir:
- Ducha caliente 90 min antes de dormir (paradójico pero funciona)
- Usa calcetines (redistribuye calor)
- Mantén el cuarto fresco

### 3. Rutina Pre-Sueño

**90 minutos antes**:
```
21:00 - Apaga pantallas grandes (TV, monitor)
21:30 - Ducha caliente
21:45 - Lectura física (no Kindle con luz)
22:00 - Meditación o journaling
22:15 - Apaga el celular
22:30 - A dormir
```

### 4. Ambiente del Dormitorio

**Oscuridad total**:
- Cortinas blackout
- Cinta en LEDs de electrodomésticos
- Antifaz si es necesario

**Silencio**:
- Tapones para oídos
- Ruido blanco si hay ruido externo inevitable
- App: myNoise

**Comodidad**:
- Colchón y almohada adecuados
- Sábanas frescas
- Sin desorden visible (afecta psicológicamente)

## Enemigos del Sueño

### Cafeína
- Vida media: 5-7 horas
- Si duermes a las 23:00, último café a las 14:00
- Alternativas de tarde: Té de hierbas, agua

### Alcohol
- Te hace dormir MÁS RÁPIDO
- Pero DESTRUYE la calidad del sueño
- Evita alcohol 3 horas antes de dormir

### Pantallas
- La luz azul engaña a tu cerebro: "¡Es de día!"
- Suprime melatonina (hormona del sueño)

**Solución**:
```bash
# Mac: Activar Night Shift automático
# iPhone: Settings → Display → Night Shift → Sunset to Sunrise
# Android: Settings → Display → Night Mode
# Windows: Night light en Settings
```

### Siestas largas
- Siesta poder: 20 min ✅
- Siesta larga: 90+ min ❌ (afecta sueño nocturno)

## Rutina de Sueño Consistente

**El hack más infravalorado**:

Duerme y despierta a la misma hora TODOS LOS DÍAS.
Incluyendo fines de semana.

Tu cuerpo ama la consistencia.

## Tracking de Sueño

**Apps recomendadas**:
- Sleep Cycle
- AutoSleep (Apple Watch)
- Fitbit
- Oura Ring (wearable)

**Qué trackear**:
- Horas de sueño
- Calidad percibida (1-10)
- Energía al despertar (1-10)
- Hora de acostar y despertar
- Productividad del día siguiente

## Power Naps Estratégicos

### Nap de 20 minutos

**Cuándo**: Entre 13:00 - 15:00

**Cómo**:
1. Busca un lugar tranquilo
2. Pon alarma de 25 min (5 min para dormirte)
3. Cierra ojos y relájate
4. Despierta y actívate con agua fría en la cara

**Beneficios**:
- Reset mental
- Mejora concentración
- No afecta sueño nocturno

### Nap Coffee (Pro tip)

1. Toma un café expresso
2. Nap de 20 min inmediatamente
3. La cafeína hace efecto justo cuando despiertas
4. ⚡ Energía máxima

## Solución a Problemas Comunes

### No puedo dormirme (insomnio inicial)

**Causas**:
- Mente muy activa
- Ansiedad
- No tienes sueño

**Soluciones**:
- Técnica 4-7-8 de respiración
- Meditación guiada (Headspace, Calm)
- Levántate y lee hasta tener sueño (no fuerces)
- Journaling: Escribe lo que piensas

### Me despierto a mitad de la noche

**Causas**:
- Apnea del sueño (visita un doctor)
- Demasiado alcohol
- Temperatura inadecuada

**Soluciones**:
- No mires el reloj
- No prendas luces
- Respira y vuelve a dormir
- Si no puedes en 20 min, levántate y lee

### No me puedo levantar

**Causas**:
- Despiertas en mitad de un ciclo
- No duermes suficiente
- Apnea del sueño

**Soluciones**:
- Alarma en múltiplos de 90 min
- Duerme 30 min más temprano
- Alarma con luz gradual (Philips Wake-Up Light)
- Deja el celular lejos (oblígarte a levantarte)

## Challenge: 30 Días de Mejor Sueño

**Semana 1**: Hora consistente
**Semana 2**: No pantallas 1 hora antes
**Semana 3**: Rutina pre-sueño
**Semana 4**: Optimiza ambiente

Trackea tu energía y productividad. Verás la diferencia.

## El Sueño es tu Compiler

Código sin compilar = Inútil
Mente sin sueño = Inútil

**Prioriza tu sueño tanto como tu código.**

## Recursos

**Libros**:
- "Why We Sleep" - Matthew Walker
- "Sleep Smarter" - Shawn Stevenson

**Apps**:
- Calm
- Headspace
- Sleep Cycle

**Websites**:
- Sleepyti.me (calculadora de ciclos)
- HubermanLab podcast (episodio sobre sueño)

## Recuerda
Los mejores programadores no son los que trabajan más horas.
Son los que trabajan con un cerebro bien descansado.
        """,
        "media_url": "https://www.youtube.com/watch?v=5MuIMqhT8DM"
    },
]

# Contenidos de Nutrición
contenidos_nutricionales = [
    {
        "tipo": BienestarItem.Tipos.NUTRICIONAL,
        "categoria": BienestarItem.Categorias.ALIMENTACION,
        "titulo": "Alimentación para el Cerebro Programmer",
        "descripcion_corta": "Qué comer para maximizar tu rendimiento mental",
        "duracion_minutos": 15,
        "orden": 9,
        "contenido_md": """
# Nutrición para Programadores

## Tu Cerebro Consume 20% de tu Energía

Necesita el combustible correcto para:
- Concentración sostenida
- Memoria de trabajo
- Resolución de problemas
- Aprendizaje de nuevas tecnologías

## Macronutrientes para el Cerebro

### Carbohidratos Complejos
El cerebro usa glucosa como combustible.

**Buenos**:
- Avena
- Arroz integral
- Pan integral
- Quinoa
- Papas
- Camote

**Malos** (picos y caídas de azúcar):
- Dulces
- Bebidas azucaradas
- Pan blanco
- Pasteles

### Proteínas
Para neurotransmisores y concentración.

**Fuentes**:
- Huevos (desayuno perfecto)
- Pollo
- Pescado (especialmente salmón)
- Legumbres
- Frutos secos
- Yogurt griego

### Grasas Saludables
El cerebro es 60% grasa.

**Omega-3** (crítico):
- Salmón
- Atún
- Sardinas
- Nueces
- Chía
- Linaza
- Suplemento de aceite de pescado

## Alimentos Brain-Boost

### Top 10

1. **Arándanos**: Antioxidantes para memoria
2. **Nueces**: Omega-3 y vitamina E
3. **Aguacate**: Grasas saludables para flujo sanguíneo
4. **Huevos**: Colina para neurotransmisores
5. **Salmón**: Omega-3 DHA (esencial)
6. **Espinaca**: Hierro y ácido fólico
7. **Brócoli**: Vitamina K para función cerebral
8. **Chocolate negro (85%+)**: Flavonoides y cafeína natural
9. **Té verde**: L-teanina para calma concentrada
10. **Plátano**: Potasio y vitamina B6 para energía

## Plan de Alimentación para un Día de Coding

### Desayuno (7:00 AM)
**Opción 1**: Power Breakfast
- 2 huevos revueltos
- 1 taza de avena con arándanos y nueces
- 1 plátano
- Té verde o café

**Opción 2**: Quick Start
- Smoothie: Plátano + espinaca + proteína en polvo + leche de almendras + mantequilla de maní

**Opción 3**: Para los con poco tiempo
- Yogurt griego con granola y frutas

### Snack Media Mañana (10:30 AM)
- Puñado de almendras (20-25)
- Manzana
- O: Yogurt griego

### Almuerzo (13:00)
**Opción 1**: Balanced Bowl
- Arroz integral o quinoa
- Pollo o salmón asado
- Brócoli y espinaca
- Aguacate

**Opción 2**: Universitario Realista
- Sandwich de pollo/atún en pan integral
- Ensalada pequeña
- Fruta

**Opción 3**: Batch Cooking
- Meal prep del domingo
- Combina: Proteína + Carbohidrato complejo + 2 vegetales

### Snack Tarde (16:00)
- Zanahorias baby con hummus
- O: Plátano con mantequilla de maní
- O: Trail mix (nueces + pasas)

### Cena (19:30)
**Ligera, 3 horas antes de dormir**:
- Ensalada con proteína (pollo/tofu/atún)
- Sopa de verduras
- Evita carbohidratos pesados

### Post-Cena (si es necesario)
- Té de hierbas
- Kiwi (ayuda a dormir)
- Evita: Cafeína, azúcar, comida pesada

## Hidratación

**El 75% de tu cerebro es agua.**

Deshidratación leve (2%) → 20% menos de rendimiento cognitivo

### Regla
**33 ml por kg de peso**

Si pesas 70 kg: 2.3 litros al día

### Señales de deshidratación
- Dolor de cabeza
- Dificultad para concentrarse
- Fatiga
- Orina oscura

### Estrategias
1. Botella de 1L visible en escritorio
2. Toma un vaso cada Pomodoro
3. App recordatorio: WaterMinder
4. Infusión de frutas si el agua te aburre

## Cafeína: Guía de Uso

### Beneficios
- Alerta aumentada
- Mejor concentración
- Rendimiento mejorado

### Límite seguro
**Máximo 400mg al día** (4 tazas de café)

### Timing óptimo
- Primera taza: 90-120 min después de despertar (cuando el cortisol baja)
- Segunda: 10:30 - 11:30 AM
- Última: Antes de las 14:00

### Tolerancia
- El cuerpo desarrolla tolerancia en 1-2 semanas
- Considera "descansos de cafeína" 1 semana cada mes

### Alternativas
- Té verde: Cafeína + L-teanina (concentración sin jitters)
- Yerba Mate
- Té matcha

## Suplementos Útiles (Consulta con médico)

### Esenciales
1. **Omega-3**: Si no comes pescado 2-3x/semana
   - Dosis: 1000mg EPA+DHA al día

2. **Vitamina D**: Especialmente si pasas todo el día adentro
   - Dosis: 2000-4000 IU al día

3. **Magnesio**: Para sueño y relajación
   - Dosis: 200-400mg antes de dormir

### Opcionales
- **Creatina**: Mejora memoria de trabajo (5g al día)
- **L-teanina**: Concentración calmada (200mg con cafeína)
- **Bacopa Monnieri**: Memoria a largo plazo

## Foods to Avoid (o minimizar)

### Durante Horas de Estudio/Trabajo
❌ **Azúcar refinada**: Crash energético después
❌ **Comidas pesadas**: Te dan sueño
❌ **Alcohol**: Afecta función cognitiva por días
❌ **Frituras**: Inflamación y letargo
❌ **Bebidas energéticas**: Picos y crashes dramáticos

### En General
❌ **Comida rápida frecuente**: Inflamación cerebral
❌ **Exceso de sodio**: Afecta flujo sanguíneo
❌ **Grasas trans**: Deterioro cognitivo

## Meal Prep para Programadores Ocupados

### Domingo: 2 horas de prep = Semana resuelta

**Paso 1: Cocinar proteínas en masa**
- 1 kg de pollo asado con especias
- 800g de pescado al horno
- Huevos duros (12)

**Paso 2: Carbohidratos**
- 2 tazas de arroz integral
- 1 kg de camote horneado

**Paso 3: Vegetales**
- Brócoli y zanahorias al vapor
- Ensalada pre-lavada en contenedores

**Paso 4: Snacks**
- Cortar frutas y guardar en contenedores
- Porcionar frutos secos en bolsitas

**Paso 5: Contenedores**
- Ensambla 5 almuerzos en contenedores
- Refrigera o congela

## Comer Consciente vs. Comer Distraído

### ❌ Frente a la pantalla (Evitar)
- Comes 20% más sin notarlo
- No registras saciedad
- Mala digestión

### ✅ Consciente (Ideal)
- Apaga pantallas
- 20 min mínimo para comer
- Mastica despacio
- Disfruta la comida

## Budget-Friendly Tips

**Proteínas baratas**:
- Huevos
- Atún enlatado
- Legumbres (lentejas, garbanzos)
- Pollo entero (más barato que piezas)

**Batch cooking**:
- Cocina grandes cantidades
- Congela porciones
- Ahorra tiempo y dinero

**Compra inteligente**:
- Frutas y verduras de temporada
- Compra al por mayor (frutos secos, arroz)
- Evita comida procesada (cara y poco nutritiva)

## Tracking (si quieres optimizar)

**Apps**:
- MyFitnessPal
- Cronometer
- Nutrients

**Qué trackear**:
- Proteína: 1.6-2g por kg de peso
- Omega-3: Al menos 250mg EPA+DHA
- Agua: 2-3L
- Cafeína: Max 400mg

## Relación Comida-Energía-Rendimiento

**Experimento de 30 días**:
1. Come balanceado (como esta guía)
2. Trackea tu energía (1-10) cada 3 horas
3. Trackea productividad al final del día
4. Compara con tu dieta anterior

Verás la diferencia MASIVA.

## Red Flags Nutricionales

Consulta un nutricionista si:
- Pérdida drástica de peso sin intención
- Fatiga constante a pesar de dormir
- Dificultad extrema para concentrarte
- Cambios drásticos en apetito

## Recuerda

> "Let food be thy medicine and medicine be thy food" - Hipócrates

Tu cerebro es tu herramienta más valiosa.
Aliméntalo como tal.

**Basura adentro = Basura afuera**
**Calidad adentro = Calidad afuera**
        """,
        "media_url": ""
    },
    {
        "tipo": BienestarItem.Tipos.NUTRICIONAL,
        "categoria": BienestarItem.Categorias.HIDRATACION,
        "titulo": "Hidratación Óptima para Largas Sesiones de Coding",
        "descripcion_corta": "Mantén tu cerebro hidratado para máximo rendimiento",
        "duracion_minutos": 5,
        "orden": 10,
        "contenido_md": """
# Hidratación para Programadores

## El Bug Silencioso: Deshidratación

**Síntomas de deshidratación leve (1-2%)**:
- Dificultad para concentrarse
- Dolor de cabeza
- Fatiga
- Irritabilidad
- Memoria de corto plazo afectada

**¿Te suena familiar?** Puede ser simple deshidratación.

## La Ciencia

- **75%** de tu cerebro es agua
- **2%** de deshidratación → **20%** menos rendimiento cognitivo
- La sed ya indica 1-2% de deshidratación

**Conclusión**: No esperes a tener sed.

## ¿Cuánta agua necesitas?

### Fórmula simple
**33ml x tu peso en kg**

Ejemplos:
- 60 kg → 2.0 L/día
- 70 kg → 2.3 L/día
- 80 kg → 2.6 L/día
- 90 kg → 3.0 L/día

### Ajustes
Aumenta si:
- Hace calor
- Haces ejercicio
- Tomas café (diurético)
- Ambiente con calefacción/aire acondicionado

## Plan de Hidratación para un Día de Coding

```
07:00 - Al despertar: 500ml (rehidrata después del sueño)
09:00 - Con desayuno: 250ml
11:00 - Media mañana: 250ml
13:00 - Con almuerzo: 500ml
15:00 - Media tarde: 250ml
17:00 - Antes de salir: 250ml
19:00 - Con cena: 250ml
21:00 - Última agua: 250ml (2-3h antes de dormir)
---
Total: ~2.5L
```

## Estrategias Prácticas

### 1. La Botella Visible
- Botella de 1L en tu escritorio
- Objetivo: 2-3 botellas al día
- Marcadores horarios en la botella

Ejemplo:
```
9 AM  → [Marca 1]
11 AM → [Marca 2]
13 PM → [Marca 3]
15 PM → [Marca 4]
17 PM → [Meta!]
```

### 2. Regla del Pomodoro Hidratante
Cada vez que terminas un Pomodoro:
1. Para de trabajar
2. Levántate
3. Toma un vaso de agua (200ml)
4. Estírate
5. Vuelve al trabajo

**8 Pomodoros = 1.6L de agua**

### 3. Apps Recordatorio
- **WaterMinder** (iOS/Android)
- **Plant Nanny** (gamificación)
- **Hydro Coach**
- **Alarma cada hora** (low-tech pero efectivo)

### 4. Infusiones Si te Aburre el Agua

**Agua infusionada casera**:
- Limón + menta
- Pepino + limón
- Naranja + arándanos
- Jengibre + limón
- Sandía + albahaca

**Preparación**:
1. Llena una jarra grande
2. Agrega frutas/hierbas cortadas
3. Refrigera 2-4 horas
4. Disfruta

### 5. Té sin Cafeína
- Té de hierbas
- Rooibos
- Manzanilla
- Té de frutas

*Cuenta como hidratación*

## Monitoreo

### Color de la Orina (El mejor indicator)

**Ideal**: Amarillo claro (como limonada)

**Escala**:
1. Transparente → Sobrehidratado (raro, pero posible)
2. Amarillo muy claro → Perfecto ✅
3. Amarillo claro → Bien
4. Amarillo → Necesitas agua
5. Amarillo oscuro → Deshidratado ❌
6. Naranja/marrón → Muy deshidratado, bebe YA

**Revisa cada vez que vas al baño.**

### Otros Indicadores
- Boca seca → Ya deshidratado
- Piel seca → Deshidratación crónica
- Ojos hundidos → Muy deshidratado
- Orina poco frecuente → Deshidratado

## Mitos Comunes

### Mito 1: "El café deshidrata"
**Realidad**: Efecto diurético mínimo. El agua del café cuenta.
**Pero**: No uses café como única fuente de hidratación.

### Mito 2: "Necesitas 8 vasos (2L) siempre"
**Realidad**: Depende de tu peso, actividad, clima.
Usa la fórmula: 33ml x peso.

### Mito 3: "Solo el agua cuenta"
**Realidad**: Frutas, verduras, té, café, todos hidratan.
**Pero**: El agua pura es lo mejor.

### Mito 4: "Puedes sobrehidratarte fácilmente"
**Realidad**: Muy difícil. Necesitarías beber 7-8L en pocas horas.
**Pero**: Sí es posible en maratones sin electrolitos.

## Bebidas que NO Hidratan (o Deshidratan)

❌ **Alcohol**: Diurético fuerte. Ratio 1:2 (1 copa = 2 vasos de agua)
❌ **Bebidas energéticas**: Azúcar + cafeína + sodio = deshidratación
❌ **Gaseosas**: Azúcar no ayuda, sodio deshidrata
⚠️ **Café en exceso**: > 4 tazas puede deshidratar

## Electrolitos

Para sesiones largas (> 4 horas intensas):

**Electrolitos necesarios**:
- Sodio
- Potasio
- Magnesio

**Fuentes**:
- Agua de coco (natural)
- Bebidas deportivas (con moderación)
- Tabletas de electrolitos
- Comida (plátano, aguacate, frutos secos)

**DIY Sports Drink**:
```
500ml agua
Jugo de 1 limón
1 cucharada de miel
1 pizca de sal
```

## Hidratación y Rendimiento

**Estudio real**:
- Grupo A: Hidratado (2.5L/día)
- Grupo B: Deshidratado (1L/día)

**Resultados**:
- Grupo A: 14% más productivo
- Grupo A: 23% menos errores
- Grupo A: Mejor estado de ánimo

**Conclusión**: La hidratación es gratis y mejora tu código.

## Hidratación para Exámenes/Entrevistas

**Día antes**:
- Hidrátate bien todo el día
- No tomes exceso la noche antes (interrumpe sueño)

**Día del examen**:
- 500ml al despertar
- 250ml 1 hora antes del examen
- Lleva agua al examen
- Pequeños sorbos durante el examen

**Beneficios**:
- Mejor memoria
- Pensamiento más claro
- Menos ansiedad
- Mejor toma de decisiones

## Challenge: 7 Días Hidratado

**Reglas**:
1. Bebe 2.5L al día (mínimo)
2. Trackea con app o papel
3. Revisa color de orina
4. Anota tu energía (1-10) cada día

**Compara**:
- Energía día 1 vs día 7
- Productividad
- Calidad de sueño
- Concentración

**Apuesta**: Notarás diferencia en día 3.

## Tips para Recordar Beber Agua

1. **Rutinas**:
   - Agua al despertar (antes de café)
   - Agua antes de cada comida
   - Agua después de ir al baño
   - Agua al llegar a casa

2. **Visual**:
   - Botella grande en escritorio
   - Post-it: "¿Ya tomaste agua?"
   - Marca horaria en botella

3. **Tecnología**:
   - Alarma cada hora
   - App con notificaciones
   - Smartwatch reminder

4. **Gamificación**:
   - Compite con amigos
   - Trackea streaks
   - Recompénsate por alcanzar meta

## Hidratación Nocturna

**Problema**: Agua antes de dormir → Despertares para orinar

**Solución**:
- Hidrátate bien durante el DÍA
- Última agua grande: 3 horas antes de dormir
- Última agua: 1 hora antes, solo 100-200ml
- Si despiertas con sed, pequeños sorbos

## Señales de que tu Hidratación Mejoró

Después de 1-2 semanas:
✅ Más energía sostenida
✅ Menos dolores de cabeza
✅ Mejor concentración
✅ Piel más saludable
✅ Mejor digestión
✅ Menos antojos de comida (muchas veces es sed)

## Recuerda

> "Water is life's matter and matrix, mother and medium.
> There is no life without water." - Albert Szent-Gyorgyi

Tu código depende de tu cerebro.
Tu cerebro depende del agua.

**Hidrátate. Codea mejor.**
        """,
        "media_url": ""
    },
]

def poblar():
    """Función principal para poblar la base de datos"""
    print(f"🚀 Poblando base de datos con contenido para {CARRERA}")
    print("=" * 60)
    
    # Verificar si ya existe contenido
    existe = BienestarItem.objects.filter(carrera=CARRERA).exists()
    if existe:
        respuesta = input(f"\n⚠️  Ya existe contenido para {CARRERA}. ¿Deseas eliminarlo y recrearlo? (s/N): ")
        if respuesta.lower() == 's':
            BienestarItem.objects.filter(carrera=CARRERA).delete()
            print("✅ Contenido anterior eliminado")
        else:
            print("❌ Operación cancelada")
            return
    
    # Combinar todos los contenidos
    todos_contenidos = contenidos_fisicos + contenidos_mentales + contenidos_nutricionales
    
    # Crear contenidos
    creados = 0
    for contenido in todos_contenidos:
        item = BienestarItem.objects.create(
            carrera=CARRERA,
            **contenido
        )
        creados += 1
        print(f"✅ Creado: {item.titulo} ({item.get_tipo_display()})")
    
    print("\n" + "=" * 60)
    print(f"🎉 ¡Listo! Se crearon {creados} contenidos para {CARRERA}")
    print("\nResumen:")
    print(f"  - Bienestar Físico: {len(contenidos_fisicos)} items")
    print(f"  - Bienestar Mental: {len(contenidos_mentales)} items")
    print(f"  - Nutrición: {len(contenidos_nutricionales)} items")
    print("\n💡 Ahora puedes acceder al módulo de Bienestar en la plataforma")

if __name__ == '__main__':
    poblar()

