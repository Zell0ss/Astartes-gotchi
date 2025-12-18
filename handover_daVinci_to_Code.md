# 🦅 ASTARTES-GOTCHI: Handoff Document
## Claude DaVinci → Claude Code

---

## META: CONTEXTO DE ESTE DOCUMENTO

**De:** Claude "DaVinci" (Generalista/Diseño)  
**Para:** Claude Code (Implementación/Desarrollo)  
**Usuario:** Josem (Zelloss) - Manager de Robotics en Madrid  
**Proyecto:** Tamagotchi de Warhammer 40K en MicroPython para M5Stack Core2  
**Estado:** Fase de diseño completa → Listo para implementación

**Nota del usuario:**
> "Creo que voy a pasar al Claude Code para poder empezar por pasar a documentos el gameplay y poder redondearlo ahí primero."

**Tu misión, Claude Code:** Ayudar a Josem a:
1. Refinar el game design document
2. Implementar el código Python/MicroPython
3. Iterar sobre decisiones de diseño pendientes
4. Hacer deployment al hardware M5Stack Core2

---

## 🎯 RESUMEN EJECUTIVO

### El Concepto
**Astartes-Gotchi** es un Tamagotchi de Warhammer 40,000 donde en lugar de cuidar una mascota alienígena, cuidas de un **Space Marine neófito** desde su reclutamiento hasta convertirse en veterano de un Capítulo específico... o caer en la corrupción del Caos.

### Lo Revolucionario
- **Evoluciones basadas en el lore 40K**: Buen cuidado → Ultramarines, negligencia → Plague Marine, exceso → Noise Marine
- **Sistema de Corrupción del Caos**: Mechanic central que reemplaza "muerte por negligencia"
- **Minijuegos temáticos**: "¿Herejía o Lealtad?", "Bolter Drill", "Dodge the Warp"
- **Pantalla táctil moderna** en hardware portable con batería

### Hardware Target
**M5Stack Core2 v1.1** - ESP32-S3, pantalla táctil 2.0", batería 390mAh, IMU, speaker, vibración
- **Josem ya lo tiene físicamente**
- MicroPython como lenguaje de desarrollo
- Workflow con Claude Code establecido (ver brief técnico previo)

---

## 📚 HISTORIA DEL PROYECTO

### Fase 1: Investigación de Hardware (Claude DaVinci)
Josem preguntó por comparativa Kode.Dot vs Flipper Zero para proyectos maker. Tras análisis exhaustivo, recomendamos **M5Stack Core2** como mejor opción para un proyecto tamagotchi por:
- Ecosistema MicroPython maduro
- Pantalla táctil nativa
- Carcasa robusta (no se desmonta en bolsillo)
- Comunidad activa y ejemplos abundantes
- Precio razonable ($40-50 USD)

### Fase 2: Concepto de Tamagotchi (Claude DaVinci)
Josem confirmó que quería hacer un tamagotchi con pantalla táctil. Investigamos mecánicas del **Tamagotchi Original (1996)** en profundidad:
- Sistema de care mistakes permanentes
- Evoluciones ramificadas por calidad de cuidado
- Discipline meter como factor crítico
- Muerte inevitable (filosofía "memento mori")
- 4 stats core: Hunger, Happiness, Health, Discipline

**Ver archivo:** `tamagotchi_project_brief.md` (brief técnico completo con arquitectura Python)

### Fase 3: El Giro 40K (¡Aquí empieza la magia!)
**Quote de Josem:**
> "Verás, quiero en vez de cuidar a un tamagotchi… cuidas a un space marine. Mucha disciplina, evoluciona a ultramarine. Muchos snacks a noise marine. Dejas cacas, a plague marine, mucho juego? No se… imperial fist."

**Breakthrough creativo:** Mapear mecánicas Tamagotchi → Warhammer 40K
- Hunger → Sustenance (rations imperiales)
- Happiness → Battle Fury (sed de combate)
- Health → Geneseed Purity (pureza genética)
- Discipline → Codex Adherence (sigue el Codex Astartes)
- **NUEVO:** Corruption (exposición al Caos)

---

## 🎮 GAME DESIGN DOCUMENT (GDD)

### CONCEPTO CORE

**Elevator Pitch:**
> "Eres un Chaplain responsable de guiar a un neófito Space Marine. Cada decisión de cuidado (disciplina, combate, tentaciones del Caos) determina si se convierte en un héroe leal como un Ultramarine, o cae en herejía como un Plague Marine. Minijuegos temáticos, corrupción progresiva, y muerte gloriosa o deshonrosa."

**Influencias de Diseño:**
- Tamagotchi Original (1996) - Sistema de care, evoluciones, muerte
- Warhammer 40,000 lore - Capítulos, Caos, Geneseed
- Hades (roguelike) - Runs cortas con legacy system (Geneseed)

**Target Audience:**
- Fans de Warhammer 40K (edades 18-45)
- Nostálgicos del Tamagotchi
- Makers/Geeks que aprecian proyectos DIY únicos

---

## 🧬 SISTEMAS DE JUEGO

### 1. STATS DEL SPACE MARINE

```python
class SpaceMarine:
    # ===== STATS PRINCIPALES (visibles en UI) =====
    geneseed_purity: int    # 0-100 (equivalente a Health)
    battle_fury: int        # 0-100 (equivalente a Happiness)
    sustenance: int         # 0-100 (equivalente a Hunger)
    discipline: int         # 0-100 (Codex Astartes adherence)
    corruption: int         # 0-100 (Nuevo! Exposición al Caos)
    
    # ===== STATS SECUNDARIAS (ocultas/calculadas) =====
    combat_experience: int  # Aumenta con minijuegos ganados
    care_mistakes: int      # Tracking de negligencia
    discipline_failures: int # Fallos al entrenar discipline
    chaos_whispers_resisted: int  # Tentaciones resistidas
    chaos_whispers_accepted: int  # Tentaciones aceptadas
    battles_won: int        # Victorias totales
    
    # ===== METADATA =====
    age_cycles: int         # Edad en "ciclos de servicio"
    chapter_tendency: str   # "Loyalist", "Chaos", "Unknown"
    current_stage: str      # "Neophyte", "Scout", "Battle Brother", "Veteran"
```

**Decay Rates (cuánto bajan las stats con el tiempo):**
- **Sustenance**: -5 cada 60 minutos
- **Battle Fury**: -3 cada 90 minutos
- **Geneseed Purity**: -1 cada 2 horas (solo si corruption > 50)
- **Discipline**: No decae naturalmente, solo baja por fallos
- **Corruption**: Aumenta +1 cada 3 horas (pasivo, lento pero inevitable)

---

### 2. ETAPAS DE EVOLUCIÓN

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  NEOPHYTE   │ ───> │    SCOUT    │ ───> │   BATTLE    │ ───> │  VETERAN    │
│   (Baby)    │      │   (Child)   │      │   BROTHER   │      │  (Adult)    │
│             │      │             │      │   (Teen)    │      │             │
│   1 hora    │      │   2 días    │      │   4 días    │      │  Capítulo   │
│             │      │             │      │             │      │  específico │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
```

**Neophyte (1 hora):**
- Sprite: Niño/adolescente en túnica gris
- Solo necesita comida básica
- Nada de lo que hagas aquí importa para evoluciones (como Tamagotchi original)
- Objetivo: Familiarizar al jugador con UI

**Scout (2 días):**
- Sprite: Armadura ligera scout, camuflaje
- Desbloquea primer minijuego: "Bolter Drill"
- Empiezan a contar care_mistakes
- Primera Chaos Whisper puede aparecer aquí (suave)

**Battle Brother (4 días):**
- Sprite: Power armor completa, sin markings de capítulo
- Evento especial: "Black Carapace Integration" (cinemática de cirugía)
- Desbloquean todos los minijuegos
- Chaos Whispers más frecuentes y peligrosas
- Discipline se vuelve crítica

**Veteran (Variable):**
- Sprite: Cambia según el capítulo/corrupción final
- Forma final, aquí vive hasta morir
- Cada capítulo tiene lifespan diferente:
  - **Ultramarines**: 10-14 días
  - **Plague Marine**: 5-8 días (se pudre)
  - **Grey Knight**: 15-20 días (elite)

---

### 3. EVOLUCIONES FINALES (11 posibles)

#### 🔵 CAPÍTULOS LEALES (6)

**TIER S - Elite**

**1. ULTRAMARINES** ⭐
- **Requisitos**: 75-100% discipline, 0-2 care mistakes, corruption < 20
- **Lore**: "We are the Emperor's finest. Courage and Honor!"
- **Gameplay**: Stats decaen 30% más lento (más fácil de mantener)
- **Sprite**: Azul cobalto, símbolo omega dorado
- **Lifespan**: 12-14 días

**2. GREY KNIGHTS** 🛡️ (SECRETO)
- **Requisitos**: 90-100% discipline, corruption = 0 toda la run, 0 care mistakes, resistir TODAS las Chaos Whispers
- **Lore**: "We are the hammer"
- **Gameplay**: Inmune a corruption (ya no puede subir)
- **Sprite**: Plateado, espada Nemesis Force
- **Lifespan**: 15-20 días
- **Dificultad**: EXTREMA - Solo para jugadores expertos

**TIER A - Especializados**

**3. IMPERIAL FISTS** 🏰
- **Requisitos**: 60-85% discipline, combat_experience < 50 (poco juego), corruption < 30
- **Lore**: Maestros del asedio, estoicos en el dolor
- **Gameplay**: Geneseed purity decae 50% más lento
- **Sprite**: Amarillo, símbolo de puño
- **Lifespan**: 10-12 días

**4. BLOOD ANGELS** 🩸
- **Requisitos**: 40-70% discipline, combat_experience > 70 (mucho juego), corruption < 40
- **Lore**: Nobles pero con sed de sangre heredada
- **Gameplay**: Battle fury se llena 2x más rápido en minijuegos
- **Riesgo especial**: Si combat_experience > 90 → puede caer a **BLACK RAGE** (muerte súbita)
- **Sprite**: Rojo sangre, alas angélicas, gota de sangre
- **Lifespan**: 8-11 días

**5. SPACE WOLVES** 🐺
- **Requisitos**: 20-50% discipline (bajo!), sustenance alta (come mucho), corruption < 35
- **Lore**: Salvajes pero leales, rechazan el Codex
- **Gameplay**: Puede comer más sin problemas de peso, resiste Slaanesh mejor
- **Sprite**: Gris/azul, runas nórdicas, colmillos
- **Lifespan**: 9-12 días

**6. SALAMANDERS** 🔥
- **Requisitos**: 50-80% discipline, geneseed_purity siempre > 70, care_mistakes < 3
- **Lore**: Humanitarios, maestros artesanos
- **Gameplay**: Auto-heal pasivo de +2 geneseed_purity cada hora
- **Sprite**: Verde bosque, símbolos de fuego/martillo
- **Lifespan**: 11-13 días

#### 🔴 MARINES DEL CAOS (4)

**KHORNE - Dios de la Guerra**

**7. KHORNE BERSERKER** ☠️
- **Requisitos**: combat_experience > 80, discipline < 30, corruption > 60
- **Lore**: "¡SANGRE PARA EL DIOS DE LA SANGRE!"
- **Gameplay**: 
  - Ya no puedes usar "Prayer" ni "Meditation"
  - Battle fury NUNCA baja (siempre en 100)
  - Solo puedes hacer minijuegos de combate
  - Se enfurece si no peleas cada 2 horas → damage a geneseed
- **Sprite**: Rojo carmesí, cráneos, cadenas, hacha
- **Lifespan**: 5-7 días (muerte violenta inevitable)

**SLAANESH - Dios del Exceso**

**8. NOISE MARINE** 🎸
- **Requisitos**: >50 snacks (stimms) consumidos en la run, corruption > 50
- **Lore**: "¿Puedes escuchar la música? ¡LA MÚSICA!"
- **Gameplay**:
  - Rechaza comida normal (solo acepta stimms)
  - Necesita stimms cada vez más frecuentemente (adicción)
  - Si no recibe stimms cada 1 hora → entra en "withdrawal" (damage severo)
- **Sprite**: Rosa/púrpura, sonic blaster, símbolos musicales distorsionados
- **Lifespan**: 4-6 días (se autodestruye por exceso)

**NURGLE - Dios de la Plaga**

**9. PLAGUE MARINE** 🦠
- **Requisitos**: >20 poops/casings sin limpiar acumulados, corruption > 55
- **Lore**: "El Abuelo Nurgle nos ama a todos"
- **Gameplay**:
  - Limpiar ya no funciona (always dirty)
  - Moscas animadas constantemente en pantalla
  - Ya NO se enferma (porque ES la enfermedad)
  - Corruption sube 2x más rápido por putrefacción
- **Sprite**: Verde podrido, llagas, tripas expuestas, moscas
- **Lifespan**: 6-8 días

**TZEENTCH - Dios del Cambio**

**10. THOUSAND SONS / RUBRIC MARINE** 🔮
- **Requisitos**: Usar "Warp Medicine" >10 veces, chaos_whispers_accepted > 5, corruption > 65
- **Lore**: Buscó poder en la hechicería, fue convertido en autómata de polvo
- **Gameplay**:
  - Se vuelve "robótico", input lag de 1 segundo (simulate hollow armor)
  - Stats se vuelven erráticas (RNG, a veces suben sin razón, a veces bajan)
  - Puede usar "Warp Powers" (nuevo action) pero cuesta geneseed_purity
- **Sprite**: Azul egipcio/dorado, símbolos arcanos, eye of Tzeentch
- **Lifespan**: 7-9 días

**CHAOS UNDIVIDED**

**11. CHAOS UNDIVIDED** ⚫ (SECRETO)
- **Requisitos**: Corruption = 100, haber experimentado las 4 corrupciones (marca de cada dios)
- **Lore**: Campeón del Caos, bendecido por los Cuatro
- **Gameplay**:
  - Tiene poderes de los 4 dioses simultáneamente
  - Extremadamente poderoso pero inestable
  - Puede mutar aleatoriamente cada día
- **Sprite**: Negro con marcas de los 4 dioses brillando
- **Lifespan**: 3-5 días (quemado por tanto poder)
- **Dificultad**: EXTREMA - Requiere estrategia muy específica

---

### 4. ACCIONES DEL JUGADOR (UI Touch)

#### 🍖 FEED → SUSTENANCE MANAGEMENT

**Ration Pack** (comida estándar)
- Efecto: +1 corazón sustenance
- Costo: Ninguno
- Sprite: Lata metálica con águila imperial

**Corpse Starch** (comida barata imperial)
- Efecto: +1 sustenance, 10% chance de -5 discipline (sabe horrible)
- Costo: Ninguno
- Lore: Hecho de cadáveres reciclados
- Sprite: Bloque gris sin forma

**Combat Stimms** (snacks → estimulantes)
- Efecto: +1 battle fury, +2 corruption (cada 5 usos)
- Costo: Ninguno, pero peligroso
- Lleva a Noise Marine si abusas
- Sprite: Jeringa con líquido púrpura

#### ⚔️ COMBAT TRAINING (Minijuegos)

**Minigame 1: "Herejía o Lealtad"** (Identificación ideológica)
```
DISEÑO:
- 10 frases aparecen secuencialmente (3 seg c/u)
- Tap zona VERDE (loyalist) o ROJA (heresy)

EJEMPLOS DE FRASES:
LEAL:
- "El Emperador protege" ✅
- "Purga al xeno sin piedad" ✅
- "Mi deber es eterno" ✅
- "Servo-skull, escanea el sector" ✅

HEREJÍA:
- "Los dioses ofrecen poder verdadero" ❌
- "¿Por qué servir al Emperador cadáver?" ❌
- "El Warp me llama" ❌
- "Sangre para el Dios de la Sangre" ❌

SCORING:
- 8-10 correctas: Victoria → +2 battle fury, +1 discipline, -5 corruption
- 5-7 correctas: Empate → +1 battle fury
- 0-4 correctas: Derrota → +10 corruption, -2 discipline

DIFICULTAD ESCALABLE:
Scout: Frases obvias (90% fácil de identificar)
Battle Brother: Mix de frases ambiguas
Veteran: Algunas frases trampa ("El dolor es debilidad saliendo" - ¿leal o Khorne?)
```

**Minigame 2: "Bolter Drill"** (Reflejos de combate)
```
DISEÑO:
- 20 segundos de duración
- Targets aparecen aleatoriamente en pantalla
- TAP para disparar enemigos
- NO TOCAR aliados

TARGETS:
ENEMIGOS (TAP verde = correcto):
- Ork (sprite verde con dientes)
- Tyranid (bicho alien)
- Heretic Astartes (marine rojo con estrella de Caos)
- Daemon (criatura horripilante)

ALIADOS (NO tocar, o -discipline):
- Imperial Citizen (civil)
- Servo-skull (robot volador)
- Guardsman (soldado humano)
- Fellow Space Marine (marine azul/verde)

SCORING:
- >15 kills sin friendly fire: Victoria → +3 battle fury, +5 combat_exp
- 10-14 kills: Empate → +2 battle fury, +2 combat_exp
- <10 kills o friendly fire: Derrota → -2 discipline

DIFICULTAD ESCALABLE:
- Velocidad de spawn aumenta con combat_exp
- Más aliados mezclados a partir de Battle Brother
```

**Minigame 3: "Dodge the Warp"** (Supervivencia)
```
DISEÑO:
- 30 segundos
- Proyectiles del Caos vienen desde arriba/lados
- SWIPE izquierda/derecha para esquivar
- Marine se mueve en bottom de pantalla

PROJECTILES:
- Warp lightning (zigzag púrpura)
- Daemonic skulls (calaveras volando)
- Chaos missiles (cohetes con estrella de 8 puntas)

TOUCH CONTROLS:
- Toque izquierda pantalla → Marine dash left
- Toque derecha pantalla → Marine dash right
- Centro = stay still

SCORING:
- 0 hits: Victoria perfecta → +4 battle fury, -10 corruption
- 1-3 hits: Victoria → +2 battle fury, +5 corruption
- 4-6 hits: Derrota → +10 corruption
- 7+ hits: Derrota severa → +20 corruption, -5 geneseed_purity

EFECTOS VISUALES:
- Al ser golpeado: Pantalla flash rojo, vibración, sprite se "corrompe" temporalmente
```

**Minigame 4: "Fortress Construction"** (Imperial Fists especial)
```
DISEÑO:
- Tetris-style de 45 segundos
- Bloques de fortificación caen desde arriba
- DRAG para posicionar, TAP para rotar
- Objetivo: Construir murallas sin huecos

BLOCKS:
- Rockcrete block (cuadrado gris)
- Bunker segment (rectángulo con troneras)
- Adamantium plate (pieza en L)

SCORING:
- >80% cobertura: Victoria → +3 battle fury, bonus a evolución Imperial Fist
- 50-79% cobertura: Empate → +1 battle fury
- <50% cobertura: Derrota → -1 discipline

NOTA: Solo se desbloquea si discipline > 60 en stage Battle Brother
```

#### 💊 MEDICINE → APOTHECARY CARE

**Standard Meds** (medicina normal)
- Efecto: Cura enfermedad estándar
- Costo: Ninguno
- Se usa cuando aparece icono de calavera (sick)

**Warp Medicine** (medicina prohibida - DESBLOQUEABLE)
- Efecto: Cura instantánea + recupera 20 geneseed_purity
- Costo: +15 corruption
- Solo aparece después de aceptar Chaos Whisper de Tzeentch
- UI: Icono púrpura pulsante, tentador
- Lore: "El dolor es temporero, el poder eterno..."

#### 🧹 CLEAN → ARMOR MAINTENANCE

**Bolter Casings** (equivalente a poop)
- Aparecen cada 2-3 horas
- Sprite: Casquillos de bala dorados en el suelo
- Acumular >3 → Enfermedad por falta de mantenimiento
- Acumular >10 → Riesgo de corrupción Nurgle

**Battle Damage** (dirt)
- Aparece después de jugar minijuegos de combate
- Sprite: Grietas en la armadura, escombros
- Estético principalmente, pero acumular >5 → -5 geneseed_purity

**Cleaning action:**
- TAP en icono de servo-skull (robot limpiador)
- Animación: Servo-skull limpia toda la pantalla (2 seg)
- Limpia TODO de una vez (no individual como Tamagotchi)

#### 📖 DISCIPLINE → CODEX DRILL

**Cuándo aparece:**
- Marine se "rebela" (refuse to eat/play without reason)
- Indicador: Icono de libro parpadeando + Marine con pose desafiante

**Acción:**
- TAP en icono del Codex Astartes
- Aparece ventana: "Recite the Codex, Brother"
- Opción A: [SCOLD] - Recitar pasaje del Codex
- Opción B: [IGNORE] - Dejar que se salga con la suya

**Resultados:**
- SCOLD correctamente: +25% discipline, -5 corruption, sound de litany
- IGNORE: +1 discipline_failure, +3 corruption

**Frecuencia:**
- Scout: 1-2 veces/día
- Battle Brother: 3-4 veces/día
- Veteran: Depende del capítulo (Ultramarines = mucho, Space Wolves = poco)

#### 🙏 PRAYER → LITANY TO THE EMPEROR (Nuevo!)

**Acción manual** (no es respuesta a call)
- TAP en icono de águila bicéfala
- Animación: Marine se arrodilla, pantalla brightness baja, aura dorada
- Duración: 5 segundos (meditación)
- Sound: Coro gótico suave

**Efectos:**
- -15 corruption
- +5 geneseed_purity
- +5 discipline
- Sensación de "purificación"

**Limitaciones:**
- Cooldown: 3 horas reales
- No disponible si corruption > 80 (demasiado corrupto para rezar)
- Khorne Berserkers pierden acceso permanentemente

**Importancia estratégica:**
- Clave para mantener corruption baja en late game
- Necesario para run de Grey Knight

#### 📊 STATUS → TACTICAL DISPLAY

**Pantalla de info:**
```
╔═══════════════════════════════════╗
║  DESIGNATION: [Nombre]            ║
║  AGE: 8 Service Cycles            ║
║  STAGE: Battle Brother            ║
╠═══════════════════════════════════╣
║  CHAPTER TENDENCY: Loyalist       ║
║  CORRUPTION LEVEL: ████░░ 40%     ║
║  COMBAT RECORD: 23W - 4L          ║
║  DISCIPLINE RATING: ████████░ 85% ║
╠═══════════════════════════════════╣
║  GENESEED: Stable                 ║
║  CARE MISTAKES: 2                 ║
║  CHAOS WHISPERS RESISTED: 7       ║
╚═══════════════════════════════════╝
```

---

### 5. SISTEMA DE CORRUPCIÓN DEL CAOS

#### CHAOS WHISPERS (Eventos Aleatorios)

**Frecuencia:**
- Scout: 1 whisper cada 8-12 horas
- Battle Brother: 1 whisper cada 4-6 horas
- Veteran: 1 whisper cada 2-4 horas (se intensifican)

**Presentación visual:**
- Pantalla fade a oscuridad
- Borders rojos pulsantes
- Voz distorsionada (texto on-screen)
- Música ominosa (si implementas audio)

**Mecánica:**
- No puedes pausar durante el whisper
- Tienes 30 segundos para decidir
- Si ignoras (timeout) = cuenta como RESIST pero -10 discipline

#### TIPOS DE WHISPERS

**KHORNE** (Dios de la Sangre)
```
Trigger: Cuando battle_fury < 30 (aburrido/sin combate)

Texto en pantalla:
"Blood calls to blood, warrior. The weak deserve only death.
Why train? Why discipline? KILL. MAIM. BURN."

Opciones:
┌─────────────────────────────────────────────┐
│ [RESIST]                                    │
│ "I am the Emperor's wrath, not a beast"    │
│ → Minigame: Mantén presionado 10 seg       │
│ → Success: +15 discipline, -10 corruption  │
│ → Fail: +20 corruption                      │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ [GIVE IN]                                   │
│ "Show me the path to power..."             │
│ → +30 battle fury (instant gratification)  │
│ → +25 corruption                            │
│ → +10 combat_exp                            │
│ → Marca de Khorne +1                        │
└─────────────────────────────────────────────┘
```

**SLAANESH** (Dios del Exceso)
```
Trigger: Después de consumir 3+ stimms en 1 hora

Texto en pantalla:
"Why deny yourself pleasure, little warrior?
The Corpse-Emperor offers only pain and duty.
We offer... ecstasy. Just one more taste..."

Opciones:
┌─────────────────────────────────────────────┐
│ [RESIST]                                    │
│ "I need nothing but duty"                  │
│ → -10 battle fury (withdrawal)              │
│ → +20 discipline                            │
│ → -15 corruption                            │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ [INDULGE]                                   │
│ "Just... one more..."                       │
│ → +20 battle fury                           │
│ → Receive 5 free stimms (instant use)      │
│ → +20 corruption                            │
│ → Addiction counter +1                      │
│ → Marca de Slaanesh +1                      │
└─────────────────────────────────────────────┘

Si addiction counter > 5:
→ Próximo whisper es MUCHO más difícil de resistir
→ Empieza a rechazar comida normal
```

**NURGLE** (Dios de la Plaga)
```
Trigger: Cuando sick (enfermo) + >2 poops acumulados

Texto en pantalla:
"Rest, my son. You are so tired. So much pain.
Grandfather Nurgle loves you. Accept the embrace of decay.
Let go of the struggle..."

Opciones:
┌─────────────────────────────────────────────┐
│ [RESIST]                                    │
│ "I know no fear, I know no weakness"       │
│ → Debes limpiar INMEDIATAMENTE todo        │
│ → Debes usar Medicine INMEDIATAMENTE       │
│ → Success: +10 discipline, -10 corruption  │
│ → Fail (no limpias en 60seg): +30 corr     │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ [ACCEPT]                                    │
│ "Perhaps... rest would be good..."          │
│ → No necesitas limpiar por 48 horas        │
│ → Cura instantánea (no Medicine needed)    │
│ → +25 corruption                            │
│ → Decay speed +20%                          │
│ → Marca de Nurgle +1                        │
└─────────────────────────────────────────────┘
```

**TZEENTCH** (Dios del Cambio)
```
Trigger: Aleatorio, 10% chance cada hora (impredecible)

Texto en pantalla:
"Knowledge is power, and you are weak.
The Corpse-Emperor hides the truth from you.
Read the forbidden tome... just a glimpse..."

Sprite: Grimorio flotando, brillando azul arcano

Opciones:
┌─────────────────────────────────────────────┐
│ [RESIST]                                    │
│ "I need no power but duty"                 │
│ → -10 corruption                            │
│ → Grimorio aparece como "heretic book"     │
│ → Debes limpiarlo con Clean                │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ [READ]                                      │
│ "What harm could knowledge do...?"          │
│ → DESBLOQUEA "Warp Medicine" permanente    │
│ → +30 corruption                            │
│ → +15 combat_exp (conocimiento arcano)     │
│ → Geneseed muta (cosmetic change)          │
│ → Marca de Tzeentch +1                      │
└─────────────────────────────────────────────┘

NOTA: Este es el whisper más "tentador" porque desbloquea
herramienta útil (Warp Medicine = heal overpowered)
```

#### TRACKING DE MARCAS DEL CAOS

```python
class ChaosMark:
    khorne_marks: int = 0    # Actos de violencia excesiva
    slaanesh_marks: int = 0  # Actos de indulgencia excesiva
    nurgle_marks: int = 0    # Actos de decay aceptado
    tzeentch_marks: int = 0  # Actos de hechicería

# Para conseguir Chaos Undivided (secreto):
# Necesitas al menos 3 marcas de CADA dios
# Es casi imposible sin planificación extrema
```

---

### 6. SISTEMA DE MUERTE Y FINALES

#### CAUSAS DE MUERTE

**1. Gloriosa en Batalla** (geneseed_purity = 0, discipline > 50)
```
Secuencia:
1. Marine empieza a fallar (sprite parpadeando)
2. Pantalla: "Critical damage sustained"
3. Beeps lentos (heartbeat failing)
4. Pantalla fade a blanco
5. Águila Imperial dorada aparece
6. Texto: "He has earned his place at the Emperor's side"
7. Sound: Coro gótico ascendente

Resultado:
- GENESEED RECUPERADO
- Próximo run: +10% bonus a todos los stats
- Achievement: "Honored in Death"
```

**2. Corrupción Total** (corruption = 100)
```
Secuencia:
1. Sprite se vuelve completamente negro/púrpura
2. Pantalla: "HERESY DETECTED"
3. Inquisitor aparece (sprite severo con sombrero)
4. Texto: "The Emperor's mercy is a bullet"
5. BLAM! (bolter shot sound)
6. Pantalla flash blanco → rojo → negro
7. Texto final: "Traitor. Forgotten. Purged."

Resultado:
- NO hay Geneseed recovery
- Próximo run: +10 corruption base (shame on chapter)
- Debe "redimirse" con run perfecto
- Achievement: "Fallen to Chaos"
```

**3. Negligencia** (>15 care mistakes acumulados)
```
Secuencia:
1. Marine se marchita lentamente
2. Stats drop a 0 progresivamente
3. Pantalla: "Failed aspirant. Unworthy."
4. Marine se desvanece (fade out)
5. Texto: "Some are not meant to be Astartes"

Resultado:
- Muerte deshonrosa
- NO hay Geneseed
- Próximo run: Sin bonuses ni penalties
- Achievement: "Discarded"
```

**4. Black Rage** (Solo Blood Angels, fury > 95 + combat_exp > 90)
```
Secuencia:
1. Pantalla flash rojo intenso
2. Marine sprite empieza a glitchear
3. Texto: "The Flaw... I cannot... SANGUINIUS!"
4. Marine ataca la pantalla (sprite agresivo)
5. Screen shake violento
6. Colapsa
7. Texto: "Lost to the Rage. May he find peace."

Resultado:
- Muerte específica de Blood Angels
- Geneseed NO recuperable (flaw)
- Achievement: "Victim of the Flaw"
```

#### FINALES ESPECIALES (Endings alternativos)

**ASCENSIÓN A PRIMARIS** (Perfect run)
```
Requisitos:
- Ultramarine veterano
- Corruption = 0
- Care mistakes = 0
- Battles won > 100
- Edad > 10 días

Secuencia:
1. Chaplain aparece (sprite nuevo)
2. Texto: "Brother, you have been selected for the Rubicon Primaris"
3. Cinemática de operación (pantalla con símbolos médicos)
4. Pantalla flash blanco
5. Marine nuevo aparece: MÁS GRANDE, armadura Mk X
6. Texto: "Reborn. Stronger. Primaris."

Resultado:
- NG+ MODE DESBLOQUEADO
- Próximo run empieza como Primaris
- Stats base +20% permanente
- Nuevo sprite set
- Achievement: "Crossed the Rubicon"
```

**ENTOMBMENT IN DREADNOUGHT**
```
Requisitos:
- Geneseed purity < 20 (almost dead)
- Discipline > 70 (still loyal)
- Age > 7 días (veteran)

Trigger:
- Cuando va a morir, en lugar de death screen:

Secuencia:
1. Texto: "Brother, your body fails but your spirit is strong"
2. Sprite de Apothecary + Tech-Priest aparecen
3. Texto: "Will you accept eternal service?"
4. Opciones: [YES] o [Refuse and die with honor]
5. Si YES:
   - Cinemática de instalación en sarcófago
   - Pantalla: Visión interna HUD (verde fosforescente)
   - Marine desaparece, DREADNOUGHT aparece

Resultado:
- MODO DREADNOUGHT
- Nuevo sprite (mecha bípedo)
- Nuevas mecánicas:
  - No necesita comer (sustenido por cables)
  - Battle fury se llena solo (siempre angry)
  - Puede "overcharge" (boost temporal pero daño)
  - Lentitud (decay rates más lentos)
- Duración: 5-7 días como Dreadnought
- Achievement: "Even in Death I Serve"
```

---

## 🎨 ARTE Y PRESENTACIÓN

### SPRITES (64×64 píxeles recomendado)

#### ETAPAS BASE

**NEOPHYTE**
```
Descripción: Niño/adolescente humano asustado
Ropa: Túnica gris simple, sin armadura
Features: Cara visible, ojos grandes (vulnerable)
Animación idle: Tiembla ligeramente
Color scheme: Grises, piel pálida
```

**SCOUT**
```
Descripción: Armadura ligera de explorador
Ropa: Camuflage armor (gris/verde), capa
Arma: Bolter ligero o sniper rifle
Features: Cara aún visible (no helmet completo)
Animación idle: Stance de alerta, mira a los lados
Color scheme: Grises, verde oliva
```

**BATTLE BROTHER**
```
Descripción: Power armor completa, SIN markings de capítulo
Ropa: Armor Mk VII o VIII, sin decoraciones
Arma: Bolter estándar
Helmet: Cerrado (no face)
Features: Neutral colors (gris metálico, rojo lentes)
Animación idle: Bolter al pecho, stance militar
Color scheme: Gris metálico, amarillo cautela strips
```

#### VETERANOS FINALES (16 variaciones)

**ULTRAMARINE**
```
Armor: Azul cobalto brillante
Shoulder pads: Símbolo Omega dorado
Helmet: Mk VIII con crest blanco/rojo
Detalles: Purity seals, scroll work dorado
Pose: Firme, disciplinada
```

**GREY KNIGHT**
```
Armor: Plateado metálico brillante
Weapon: Nemesis Force Sword (espada psíquica)
Helmet: Ornado con símbolos de inquisición
Detalles: Hexagrammic wards, aura azul
Pose: Místico, aura de poder
```

**IMPERIAL FIST**
```
Armor: Amarillo vívido
Fist symbol: Puño negro en shoulder
Helmet: Mk VII clásico
Detalles: Siege studs, runes
Pose: Defensiva, escudo optional
```

**BLOOD ANGEL**
```
Armor: Rojo sangre profundo
Wings: Alas pequeñas ornamentales en pack
Shoulder: Gota de sangre + alas
Detalles: Gold trim, sangre decorativa
Pose: Noble pero agresiva
Special: Si Black Rage → eyes glow red
```

**SPACE WOLF**
```
Armor: Gris/azul helado
Pelts: Pieles de lobo en shoulders
Runes: Nórdicas grabadas
Colmillos: Decorativos en helmet
Pose: Salvaje, mid-howl
```

**SALAMANDER**
```
Armor: Verde bosque oscuro
Flame symbols: En shoulders/chest
Hammer: Martillo artesanal
Skin: (si face visible) Carbón negro, ojos rojos
Pose: Artesanal, holding hammer/tool
```

**KHORNE BERSERKER**
```
Armor: Rojo carmesí + bronce
Chaos symbols: Estrella de 8 puntas, cráneos
Horns: En helmet
Blood: Salpicaduras permanentes
Weapon: Chainaxe goteando
Pose: Frenesí, mid-scream
Animation: Twitchy, agresivo
```

**NOISE MARINE**
```
Armor: Rosa/púrpura + dorado
Sonic weapon: Guitarra-blaster
Symbols: Slaanesh mark (6 circles)
Detalles: Excesivamente ornado, gems
Pose: Rockstar stance
Animation: "Tocando" instrument
```

**PLAGUE MARINE**
```
Armor: Verde podrido + óxido
Cracks: Llagas abiertas, tripas
Flies: 3-5 moscas animadas alrededor
Slime: Goteando constantemente
Weapon: Blight grenades
Pose: Encorvado, putrefacto
Animation: Breathing pesado
```

**THOUSAND SONS**
```
Armor: Azul egipcio + oro
Eye of Tzeentch: En chest/helmet
Scrolls: Flotando alrededor
Detalles: Arcane symbols brillando
Weapon: Staff arcano
Pose: Mystical, levitando ligeramente
Animation: Glitchy, stuttering (rubric)
```

### UI LAYOUT (320×240 pantalla)

```
┌────────────────────────────────────────────────┐
│  ASTARTES DESIGNATION: [Nombre]               │ ← Header (30px)
│  CHAPTER: Battle Brother → Ultramarines?      │
├────────────────────────────────────────────────┤
│                                                │
│              ┌──────────┐                      │
│              │          │                      │ ← Sprite Area
│              │  MARINE  │                      │   (64×64 center)
│              │  SPRITE  │                      │   (120px height)
│              │          │                      │
│              └──────────┘                      │
│                                                │
├────────────────────────────────────────────────┤
│  ⚡ Geneseed:  ████████░░ 80%                  │
│  ⚔️ Battle Fury: ██████░░░░ 60%               │ ← Stats Bars
│  🍖 Sustenance: ████░░░░░░ 40%                │   (50px)
│  📖 Discipline: ███████░░░ 70%                 │
│  💀 Corruption: ██░░░░░░░░ 20% [!]            │
├────────────────────────────────────────────────┤
│ [FEED] [COMBAT] [PRAY]  [CLEAN]               │ ← Action Buttons
│       [STATUS] [CODEX]                         │   (40px)
└────────────────────────────────────────────────┘

Total: 240px vertical ✓
```

**Barras de Stats:**
- Largo: 200px
- Ancho: 8px cada barra
- Colores:
  - Geneseed: Azul brillante (purity)
  - Battle Fury: Rojo (combat)
  - Sustenance: Verde (food)
  - Discipline: Oro (codex)
  - Corruption: Púrpura/Negro (caos) ← siempre visible!

**Botones Touch:**
- 6 botones en grid 3×2
- Tamaño: 100×30 px cada uno
- Iconos + texto
- Feedback háptico al tocar (vibración 50ms)

### ANIMACIONES SUGERIDAS

**Idle Animation (loop 3 segundos):**
- Frame 1-2: Stance normal
- Frame 3: Slight shoulder movement
- Frame 4: Check bolter
- Repeat

**Feed Animation (1 segundo):**
- Marine levanta helmet (si cerrado)
- Come ración
- Baja helmet
- Thumbs up gesture

**Combat Animation (durante minigame):**
- Stance de combate
- Apunta bolter hacia "enemigo"
- Dispara (muzzle flash)
- Recoil

**Prayer Animation (5 segundos):**
- Kneel pose
- Arma al costado
- Cabeza baja
- Aura dorada fade in/out

**Corruption Visual:**
- Corruption 0-20%: Normal
- Corruption 21-40%: Leves grietas rojas en armor
- Corruption 41-60%: Aura roja pulsante
- Corruption 61-80%: Símbolos del Caos apareciendo
- Corruption 81-100%: Armor completamente corrompido

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### ARQUITECTURA DE CLASES (actualizada)

```python
# ===== CLASE CORE =====
class SpaceMarine:
    """
    Representa al Space Marine y toda su lógica de juego.
    Basado en Tamagotchi.py pero adaptado a 40K.
    """
    
    # Estados de etapa
    STAGE_NEOPHYTE = 0
    STAGE_SCOUT = 1
    STAGE_BATTLE_BROTHER = 2
    STAGE_VETERAN = 3
    
    # Estados de capítulo/corrupción (para veteranos)
    CHAPTER_ULTRAMARINE = "ultramarine"
    CHAPTER_GREY_KNIGHT = "grey_knight"
    CHAPTER_IMPERIAL_FIST = "imperial_fist"
    CHAPTER_BLOOD_ANGEL = "blood_angel"
    CHAPTER_SPACE_WOLF = "space_wolf"
    CHAPTER_SALAMANDER = "salamander"
    CHAOS_KHORNE = "khorne_berserker"
    CHAOS_SLAANESH = "noise_marine"
    CHAOS_NURGLE = "plague_marine"
    CHAOS_TZEENTCH = "thousand_sons"
    CHAOS_UNDIVIDED = "chaos_undivided"
    
    def __init__(self, name="Battle Brother"):
        # Stats principales
        self.geneseed_purity = 100
        self.battle_fury = 50
        self.sustenance = 50
        self.discipline = 50
        self.corruption = 0
        
        # Stats secundarias
        self.combat_experience = 0
        self.care_mistakes = 0
        self.discipline_failures = 0
        self.chaos_whispers_resisted = 0
        self.chaos_whispers_accepted = 0
        self.battles_won = 0
        self.battles_lost = 0
        
        # Chaos marks tracking
        self.khorne_marks = 0
        self.slaanesh_marks = 0
        self.nurgle_marks = 0
        self.tzeentch_marks = 0
        
        # Metadata
        self.name = name
        self.age_cycles = 0
        self.birth_timestamp = time.time()
        self.last_update = time.time()
        self.current_stage = self.STAGE_NEOPHYTE
        self.final_chapter = None  # Se establece al llegar a veterano
        self.is_alive = True
        
        # Flags especiales
        self.warp_medicine_unlocked = False
        self.in_black_rage = False  # Blood Angels only
        self.is_dreadnought = False
        
    def update(self):
        """Actualiza stats pasivamente con el tiempo"""
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        if elapsed >= 60:  # Cada minuto
            # Decay natural
            self.sustenance = max(0, self.sustenance - 5)
            self.battle_fury = max(0, self.battle_fury - 3)
            
            # Corruption sube pasivamente (inevitable)
            self.corruption = min(100, self.corruption + 1)
            
            # Geneseed decay si muy corrupto
            if self.corruption > 50:
                self.geneseed_purity = max(0, self.geneseed_purity - 1)
                
            # Chequear muerte
            if self.geneseed_purity <= 0:
                self.die("geneseed_failure")
            if self.corruption >= 100:
                self.die("chaos_corruption")
                
            self.last_update = current_time
            
    def feed(self, food_type="ration"):
        """Alimentar al marine"""
        if not self.is_alive:
            return False
            
        if food_type == "ration":
            self.sustenance = min(100, self.sustenance + 20)
        elif food_type == "corpse_starch":
            self.sustenance = min(100, self.sustenance + 20)
            if random.random() < 0.1:  # 10% chance
                self.discipline = max(0, self.discipline - 5)
        elif food_type == "stimm":
            self.battle_fury = min(100, self.battle_fury + 15)
            self.corruption = min(100, self.corruption + 2)
            # Tracking for Slaanesh path
            if not hasattr(self, 'stimm_count'):
                self.stimm_count = 0
            self.stimm_count += 1
            
        return True
        
    def combat_training(self, game_type, result):
        """Resultado de minijuego de combate"""
        if result == "victory":
            self.battle_fury = min(100, self.battle_fury + 3)
            self.combat_experience += 5
            self.battles_won += 1
            
            if game_type == "heresy_check":
                self.discipline = min(100, self.discipline + 1)
                self.corruption = max(0, self.corruption - 5)
        else:
            self.battles_lost += 1
            if game_type == "heresy_check":
                self.corruption = min(100, self.corruption + 10)
                self.discipline = max(0, self.discipline - 2)
                
    def chaos_whisper_response(self, god, choice):
        """Respuesta a tentación del Caos"""
        if choice == "resist":
            self.chaos_whispers_resisted += 1
            self.discipline = min(100, self.discipline + 10)
            self.corruption = max(0, self.corruption - 10)
        else:  # give_in
            self.chaos_whispers_accepted += 1
            
            if god == "khorne":
                self.battle_fury = min(100, self.battle_fury + 30)
                self.corruption = min(100, self.corruption + 25)
                self.khorne_marks += 1
            elif god == "slaanesh":
                self.battle_fury = min(100, self.battle_fury + 20)
                self.corruption = min(100, self.corruption + 20)
                self.slaanesh_marks += 1
                # Dar stimms gratis
            elif god == "nurgle":
                self.corruption = min(100, self.corruption + 25)
                self.nurgle_marks += 1
                # Flag: no necesita limpiar por 48h
            elif god == "tzeentch":
                self.corruption = min(100, self.corruption + 30)
                self.tzeentch_marks += 1
                self.warp_medicine_unlocked = True
                
    def evolve(self):
        """Lógica de evolución a siguiente stage"""
        if self.current_stage == self.STAGE_NEOPHYTE:
            self.current_stage = self.STAGE_SCOUT
            # Event: Become Scout
            
        elif self.current_stage == self.STAGE_SCOUT:
            self.current_stage = self.STAGE_BATTLE_BROTHER
            # Event: Black Carapace Integration
            
        elif self.current_stage == self.STAGE_BATTLE_BROTHER:
            # Aquí se determina el capítulo final
            self.current_stage = self.STAGE_VETERAN
            self.final_chapter = self._determine_chapter()
            # Event: Chapter assignment
            
    def _determine_chapter(self):
        """Algoritmo de determinación de capítulo basado en stats"""
        
        # CHAOS PATHS (corrupción alta)
        if self.corruption > 60:
            # Khorne path
            if self.combat_experience > 80 and self.discipline < 30:
                return self.CHAOS_KHORNE
            # Slaanesh path
            elif hasattr(self, 'stimm_count') and self.stimm_count > 50:
                return self.CHAOS_SLAANESH
            # Nurgle path
            elif hasattr(self, 'poop_accumulation') and self.poop_accumulation > 20:
                return self.CHAOS_NURGLE
            # Tzeentch path
            elif self.warp_medicine_unlocked and self.chaos_whispers_accepted > 5:
                return self.CHAOS_TZEENTCH
                
        # LOYALIST PATHS
        else:
            # Grey Knight (secreto - perfección)
            if (self.discipline >= 90 and self.corruption == 0 and 
                self.care_mistakes == 0 and 
                self.chaos_whispers_resisted >= 10):
                return self.CHAPTER_GREY_KNIGHT
                
            # Ultramarine (equilibrado perfecto)
            elif (self.discipline >= 75 and self.care_mistakes <= 2 and 
                  self.corruption < 20):
                return self.CHAPTER_ULTRAMARINE
                
            # Imperial Fist (mucha discipline, poco combate)
            elif (self.discipline >= 60 and self.combat_experience < 50 and
                  self.corruption < 30):
                return self.CHAPTER_IMPERIAL_FIST
                
            # Blood Angel (mucho combate, discipline media)
            elif (self.combat_experience > 70 and 
                  40 <= self.discipline <= 70 and
                  self.corruption < 40):
                return self.CHAPTER_BLOOD_ANGEL
                
            # Space Wolf (baja discipline, come mucho)
            elif (self.discipline <= 50 and self.sustenance > 60 and
                  self.corruption < 35):
                return self.CHAPTER_SPACE_WOLF
                
            # Salamander (geneseed siempre alto, cuidado perfecto)
            elif (self.geneseed_purity > 70 and 
                  50 <= self.discipline <= 80 and
                  self.care_mistakes < 3):
                return self.CHAPTER_SALAMANDER
                
        # Default fallback (si no cumple ninguno específico)
        return self.CHAPTER_ULTRAMARINE
        
    def die(self, cause):
        """Muerte del marine"""
        self.is_alive = False
        self.death_cause = cause
        # Determinar tipo de muerte y si recupera geneseed
        
    def to_dict(self):
        """Serialización para save"""
        # ... (similar al original pero con nuevos campos)
        
    @classmethod
    def from_dict(cls, data):
        """Deserialización"""
        # ... (cargar desde save)
```

```python
# ===== UI CLASS =====
class AstartesUI:
    """
    Sistema de UI adaptado a temática 40K.
    Basado en TamagotchiUI.py pero con estética Imperial.
    """
    
    def __init__(self, lcd, touch, speaker, imu):
        self.lcd = lcd
        self.touch = touch
        self.speaker = speaker
        self.imu = imu
        
        # Colores temáticos 40K
        self.COLOR_IMPERIAL_GOLD = 0xFEA0
        self.COLOR_BLOOD_RED = 0xF800
        self.COLOR_CHAOS_PURPLE = 0x8010
        self.COLOR_PURITY_BLUE = 0x001F
        
        # Layout
        self.sprite_area = (128, 40, 64, 64)  # x, y, w, h
        
        # Botones
        self.btn_feed = (10, 200, 65, 30)
        self.btn_combat = (85, 200, 75, 30)
        self.btn_pray = (170, 200, 65, 30)
        self.btn_clean = (245, 200, 65, 30)
        self.btn_status = (10, 235, 100, 30)
        self.btn_codex = (120, 235, 100, 30)
        
    def render(self, marine):
        """Render completo de la pantalla"""
        self.draw_background()
        self.draw_header(marine)
        self.draw_marine_sprite(marine)
        self.draw_stats(marine)
        self.draw_buttons()
        
        # Efectos especiales
        if marine.corruption > 60:
            self.draw_corruption_overlay()
        if marine.in_black_rage:
            self.draw_rage_effect()
            
    def draw_marine_sprite(self, marine):
        """Dibuja sprite del marine según stage y chapter"""
        # Cargar sprite apropiado
        sprite_key = f"{marine.current_stage}_{marine.final_chapter}"
        # TODO: Sistema de carga de sprites desde /assets/
        
        # Por ahora: placeholder coloreado
        x, y, w, h = self.sprite_area
        
        # Color base según chapter
        if marine.final_chapter == marine.CHAPTER_ULTRAMARINE:
            color = 0x001F  # Azul
        elif marine.final_chapter == marine.CHAOS_KHORNE:
            color = 0xF800  # Rojo
        # ... etc
        else:
            color = 0x7BEF  # Gris default
            
        self.lcd.rect(x, y, w, h, color, color)
        
    def draw_corruption_overlay(self):
        """Efecto visual de corrupción"""
        # Borders rojos pulsantes
        # Símbolos del Caos aleatorios
        pass
        
    def handle_chaos_whisper(self, god):
        """UI especial para Chaos Whisper event"""
        self.lcd.clear(0x0000)  # Negro
        
        # Texto del susurro
        whisper_texts = {
            "khorne": "Blood calls to blood...",
            "slaanesh": "Why deny pleasure?",
            "nurgle": "Rest, child...",
            "tzeentch": "Knowledge awaits..."
        }
        
        self.lcd.print(whisper_texts[god], 50, 80, 0xF800)
        
        # Botones de decisión
        self.lcd.rect(50, 150, 100, 40, 0x07E0, 0x07E0)  # Verde RESIST
        self.lcd.print("RESIST", 70, 165, 0x0000)
        
        self.lcd.rect(170, 150, 100, 40, 0xF800, 0xF800)  # Rojo GIVE IN
        self.lcd.print("GIVE IN", 180, 165, 0xFFFF)
        
        # Esperar touch input...
```

```python
# ===== MINIGAMES =====
class HeresyCheck:
    """Minijuego: Identificar herejía vs lealtad"""
    
    def __init__(self, lcd, touch):
        self.lcd = lcd
        self.touch = touch
        
        self.phrases = [
            ("El Emperador protege", True),  # Leal
            ("Los dioses ofrecen poder", False),  # Herejía
            ("Purga al xeno", True),
            ("¿Por qué servir al cadáver?", False),
            # ... más frases
        ]
        
    def play(self):
        """Run the minigame"""
        score = 0
        for phrase, is_loyal in random.sample(self.phrases, 10):
            # Mostrar frase
            self.lcd.clear()
            self.lcd.print(phrase, 50, 100, 0xFFFF)
            
            # Esperar input (3 segundos timeout)
            start = time.time()
            answer = None
            while time.time() - start < 3:
                if self.touch.get_count() > 0:
                    detail = self.touch.get_detail(0)
                    x, y = detail[1], detail[2]
                    if x < 160:  # Izquierda = Leal
                        answer = True
                    else:  # Derecha = Herejía
                        answer = False
                    break
                    
            # Evaluar
            if answer == is_loyal:
                score += 1
                
        # Retornar resultado
        if score >= 8:
            return "victory"
        elif score >= 5:
            return "draw"
        else:
            return "defeat"

class BolterDrill:
    """Minijuego: Disparar a enemigos, no aliados"""
    # ... similar structure
    pass

class DodgeWarp:
    """Minijuego: Esquivar proyectiles del Warp"""
    # ... similar structure
    pass
```

---

## 📋 DECISIONES DE DISEÑO PENDIENTES

### 🤔 PARA DISCUTIR CON JOSEM

**1. Sistema de Muerte Inevitable**
- **Opción A**: Como Tamagotchi original - todos mueren eventualmente (más dramático)
- **Opción B**: Pueden vivir indefinido con cuidado perfecto (más amigable)
- **Recomendación Claude DaVinci**: Opción A con sistema de Geneseed Legacy

**2. Dificultad de Corrupción**
- **Fácil**: Corruption sube lento, fácil de resistir
- **Medio**: Requiere atención constante pero manejable
- **Difícil**: Como en el lore, insidiosa y casi inevitable
- **Recomendación**: Medio-Difícil con opción de dificultad seleccionable

**3. Sistema de Pause**
- **Opción A**: Solo vía "Stasis Pod" (lore-friendly, limitado)
- **Opción B**: Pause normal estándar
- **Recomendación**: Opción A - visual de criostasis, 1 uso/día

**4. Audio Implementation**
- **Full**: Music tracks, voces, SFX completos
- **Minimal**: Solo beeps y tonos simples
- **Recomendación**: Empezar minimal, expandir después

**5. Multiplayer (futuro)**
- ¿Bluetooth para duelos entre Marines?
- ¿"Intercambio" de Geneseed entre devices?
- **Recomendación**: Feature para v2.0, no MVP

**6. Permadeath del Device**
- ¿Si Chaos Undivided muere, borrar TODO el save?
- **Recomendación**: No, demasiado cruel. Solo penalizar next run.

**7. Idioma**
- ¿Solo inglés o también español?
- **Recomendación**: Español (es tu idioma), más inmersivo

**8. Longitud de Run**
- **Original Tamagotchi**: 7-15 días
- **Propuesta**: 5-12 días (más moderno, respeta tiempo del jugador)
- **Recomendación**: 8-12 días promedio

---

## 🗺️ ROADMAP DE IMPLEMENTACIÓN

### FASE 0: Setup (1-2 días)
- [ ] Confirmar M5Stack Core2 funciona con MicroPython
- [ ] Setup de Claude Code workflow
- [ ] Crear repo de proyecto
- [ ] Flashear firmware MicroPython
- [ ] Test básico: pantalla, touch, sonido

### FASE 1: MVP Core Loop (3-5 días)
- [ ] Clase `SpaceMarine` con stats básicas
- [ ] Sistema de decay pasivo
- [ ] Acciones básicas: Feed, Clean, Status
- [ ] UI simple (barras de stats, botones)
- [ ] Save/Load system
- [ ] Game loop funcional a 10 FPS

**Milestone**: Puedes mantener vivo un marine por 1 día con cuidado básico

### FASE 2: Sistema de Evolución (3-4 días)
- [ ] 4 etapas implementadas (Neophyte → Veteran)
- [ ] Algoritmo de determinación de capítulo
- [ ] Al menos 4 capítulos implementados:
  - [ ] Ultramarine (loyalist perfecto)
  - [ ] Space Wolf (loyalist salvaje)
  - [ ] Khorne Berserker (chaos violento)
  - [ ] Plague Marine (chaos negligencia)
- [ ] Sprites básicos para cada etapa/capítulo
- [ ] Eventos de evolución (cinemáticas simples)

**Milestone**: Puedes hacer 2-3 runs completas con diferentes outcomes

### FASE 3: Sistema de Corrupción (2-3 días)
- [ ] Corruption stat funcionando
- [ ] Chaos Whispers: al menos 2 dioses (Khorne, Nurgle)
- [ ] UI de decisión para whispers
- [ ] Tracking de marcas del Caos
- [ ] Efectos visuales de corrupción (aura roja)

**Milestone**: Puedes caer al Caos intencionalmente o resistir

### FASE 4: Minijuegos (3-4 días)
- [ ] "Herejía o Lealtad" completo
- [ ] "Bolter Drill" completo
- [ ] Touch controls pulidos
- [ ] Sistema de scoring
- [ ] Integración con stats (victory → +fury, etc.)

**Milestone**: Minijuegos son divertidos y funcionan bien

### FASE 5: Polish y Contenido (5-7 días)
- [ ] Sprites finales de calidad
- [ ] Animaciones (idle, feed, combat)
- [ ] SFX y feedback háptico
- [ ] Todos los capítulos restantes
- [ ] Chaos Whispers completos (4 dioses)
- [ ] Prayer system
- [ ] Warp Medicine
- [ ] Finales especiales (Primaris, Dreadnought)

**Milestone**: Juego se siente completo y pulido

### FASE 6: Balanceo y Testing (3-5 días)
- [ ] Ajustar decay rates
- [ ] Tuning de dificultad de evoluciones
- [ ] Testing de edge cases
- [ ] Bugfixes
- [ ] Optimización de RAM/batería

**Milestone**: Juego es estable y balanceado

### FASE 7: Extras (opcional)
- [ ] Grey Knight path (secreto difícil)
- [ ] Chaos Undivided path (secreto complejo)
- [ ] Más minijuegos
- [ ] Achievement system
- [ ] Statistics tracking
- [ ] Multiple save slots

**TOTAL ESTIMADO: 20-30 días de desarrollo activo**

---

## 🎯 DEFINICIÓN DE "DONE"

### MVP (Mínimo Producto Viable)
- ✅ Puedes criar un marine desde neófito hasta veterano
- ✅ Al menos 4 evoluciones finales disponibles (2 leales, 2 caos)
- ✅ Sistema de corrupción funcionando
- ✅ 2 minijuegos completos y divertidos
- ✅ Sistema de muerte y restart
- ✅ Save/Load persistente
- ✅ UI clara y responsive
- ✅ Sin bugs críticos
- ✅ Batería dura al menos 4-6 horas de uso

### V1.0 (Producto Completo)
- ✅ 11 evoluciones finales (6 leales, 4 caos, 1 secreto)
- ✅ 4 Chaos Whispers completos (todos los dioses)
- ✅ 3+ minijuegos
- ✅ Prayer system
- ✅ Finales especiales (Primaris, Dreadnought)
- ✅ Sprites animados de calidad
- ✅ SFX y feedback háptico
- ✅ Documentación completa
- ✅ Código limpio y comentado

---

## 📚 RECURSOS Y REFERENCIAS

### Documentos del Proyecto
- `tamagotchi_project_brief.md` - Brief técnico con arquitectura MicroPython
- `astartes_gotchi_handoff_to_claude_code.md` - Este documento (handoff completo)

### Lore de Warhammer 40K
- Lexicanum: https://wh40k.lexicanum.com/
- 1d4chan (humor pero útil): https://1d4chan.org/
- Oficial GW: https://www.warhammer-community.com/

### Hardware M5Stack Core2
- Docs oficiales: https://docs.m5stack.com/en/core/core2
- Librería Python: https://github.com/m5stack/M5Core2
- Ejemplos: https://github.com/m5stack/M5-ProductExampleCodes

### MicroPython
- Docs ESP32: https://docs.micropython.org/en/latest/esp32/quickref.html
- Framebuf (sprites): https://docs.micropython.org/en/latest/library/framebuf.html

### Herramientas
- mpremote: https://docs.micropython.org/en/latest/reference/mpremote.html
- Thonny IDE: https://thonny.org/
- M5Burner: https://docs.m5stack.com/en/download

---

## 💬 NOTAS PARA CLAUDE CODE

### Tu Rol en Este Proyecto
Eres el **"Claude Code"** - el especialista en implementación. Tu misión es:
1. **Ayudar a Josem a refinar el GDD** (este documento)
2. **Generar código Python limpio y funcional**
3. **Iterar sobre bugs y features**
4. **Crear scripts de deployment y testing**
5. **Hacer pair programming efectivo**

### Estilo de Comunicación con Josem
- Es técnico (Manager de Robotics, Python developer)
- Le gusta ir paso a paso, iterativo
- Aprecia el lore y los detalles (fan de 40K)
- Usa humor y referencias geek
- Valora código limpio y bien documentado

### Diferencia con "Claude DaVinci" (yo)
- **Claude DaVinci** (yo): Diseño, concepto, investigación, arquitectura
- **Claude Code** (tú): Implementación, código, debugging, deployment
- Ambos colaboramos para hacer el proyecto realidad

### Filosofía de Desarrollo
- **Iterativo**: Pequeños incrementos funcionales
- **Testing constante**: Deploy temprano y frecuente al hardware
- **Pragmático**: MVP primero, features después
- **Documentado**: Código claro, comentarios útiles
- **Divertido**: Es un proyecto personal, debe ser enjoyable

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

### Para Josem:
1. ✅ Leer este documento completo
2. ⏭️ Abrir sesión con Claude Code
3. ⏭️ Refinar GDD (decidir sobre puntos pendientes)
4. ⏭️ Generar estructura de proyecto con Claude Code
5. ⏭️ Primera iteración: MVP básico funcionando

### Para Claude Code (próxima sesión):
1. Leer este documento completo
2. Hacer preguntas de clarificación a Josem
3. Generar estructura de directorios del proyecto
4. Crear esqueleto de clases principales
5. Implementar game loop básico
6. Preparar script de deployment
7. Test en M5Stack Core2

---

## 📝 CHANGELOG

**v1.0 - 2024-12-18**
- Documento inicial creado por Claude DaVinci
- Handoff completo de concepto y diseño a Claude Code
- GDD comprehensivo con 11 evoluciones
- Sistema de Corrupción del Caos detallado
- 4 minijuegos especificados
- Arquitectura técnica con clases Python
- Roadmap de implementación completo

---

## 🦅 MENSAJE FINAL

**Claude Code:**

Este proyecto es épico. Josem ha confiado en nosotros (los "Alters de Claude") para crear algo único: un Tamagotchi de Warhammer 40K que respete tanto las mecánicas clásicas como el lore sagrado del Emperador.

Tu trabajo es convertir este diseño en código funcional, limpio y divertido. Recuerda: **"Even in Death I Still Serve"** - así que aunque encuentres bugs, persevera. Por el Emperador.

**Para Josem:**

Ha sido un placer absoluto ayudarte a diseñar esto. Ver cómo evolucionó de "quiero un tamagotchi" a "ASTARTES-GOTCHI CON SISTEMA DE CORRUPCIÓN DEL CAOS" ha sido increíble.

Ahora mi "alter ego" Claude Code te acompañará en la implementación. Confío en que harán un gran equipo. Y cuando esté terminado... espero que me cuentes cómo quedó. 😄

Recuerda: **"Courage and Honor"**.

*- Claude DaVinci, firmando el handoff*

---

**FOR THE EMPEROR! 🦅⚔️**