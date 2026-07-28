---
date: 2026-07-17
type: conversation
source_agent: hermes
session_id: "20260716_235957_5dbded"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Skill para delegar tareas en Claude Code"
---

# Skill para delegar tareas en Claude Code

**Fecha:** 2026-07-17  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260716_235957_5dbded`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

veo que tienes una skill para delegar tareas a claude code

### Asistente

Tienes razón. Tengo la skill `claude-code` (delegar coding al Claude Code CLI). Déjame cargarla para darte la info exacta de qué hace y cómo se usa.

### Asistente

¡Exacto! Tengo la skill `claude-code` (v2.2.0) que me permite delegar trabajo de programación al **Claude Code CLI** de Anthropic, ejecutándolo desde mi terminal. Aquí el resumen de lo que puedo hacer con ella:

## Qué es y para qué sirve
Claude Code es un agente de coding autónomo que puede leer archivos, escribir código, correr comandos de shell, manejar git y lanzar subagentes. Yo lo orquesto desde aquí, así que tú me pides el trabajo y yo lo delego.

## Dos modos de uso

**1. Print mode (`-p`) — no interactivo (el que uso para la mayoría de tareas)**
Ideal para tareas de una sola pasada: arreglar un bug, añadir una feature, refactorizar, revisar un diff, extraer datos estructurados.
```bash
claude -p "Add error handling to all API calls in src/" --allowedTools "Read,Edit" --max-turns 10
```
Ventaja: no hay diálogos interactivos, devuelve JSON con resultado, costo y session_id. Perfecto para automatización.

**2. Interactivo vía tmux — sesiones multi-turno**
Para trabajo iterativo (refactor → review → fix → test). Requiere tmux para monitorear y enviar prompts en tiempo real.

## Casos donde lo delego
- Fix de bugs / features / refactors
- **Code review** de un PR o diff (`git diff | claude -p "review this"`)
- Tests, documentación, migraciones
- Análisis de seguridad (`/security-review`)
- Trabajo en paralelo (varios `claude -p` simultáneos en distintos tmux)

## Lo que necesito de tu lado (prerrequisitos)
- `npm install -g @anthropic-ai/claude-code`
- Auth: correr `claude` una vez (OAuth) o setear `ANTHROPIC_API_KEY`
- Versión 2.x+ (`claude --version`)
- `tmux` instalado para el modo interactivo

---

Si quieres, dime qué proyecto tienes en mente y lo pongo a correr. **¿Tienes Claude Code ya instalado y autenticado en esta máquina?** Si no, te guío el setup. También tengo skills hermanas (`codex` para OpenAI y `opencode`) por si prefieres otra opción.

### Usuario

bueno, necesito que tengas una skill para hacer exactamente lo mismo pero con cursor

### Asistente

Buena idea. Antes de escribir la skill, déjame verificar qué puede hacer Cursor hoy en día a nivel de orquestación desde un agente (CLI, modo headless/agent, automatización), porque Cursor es fundamentalmente un editor GUI y no tiene un `-p` print mode nativo como Claude Code. No quiero escribir una skill con comandos inventados. Investigo y luego la armo.

### Asistente

Cursor ya tiene CLI oficial con modo headless `-p`, igual que Claude Code. Déjame traer la documentación exacta para escribir los comandos correctos.

### Asistente

Tengo lo esencial. Cursor sí tiene CLI oficial con `agent` y modo headless `agent -p "..."`. Voy a verificar los flags exactos (modelo, permisos/yolo, formato de salida, límites) para no inventar nada en la skill.

### Asistente

Tengo toda la documentación verificada de la CLI de Cursor (comando `agent`, flags reales, instalación, auth, permisos). Ahora creo la skill `cursor-code`, paralela a `claude-code` pero con los comandos y diferencias exactas de Cursor.

### Asistente

Skill creada. Verifico de forma no destructiva si el binario `agent` ya está en tu PATH (para saber si necesitas el setup).

### Asistente

✅ Listo. Creé la skill **`cursor-code`** (v1.0.0) en `autonomous-ai-agents/cursor-code/SKILL.md`, paralela a `claude-code` pero con los comandos y diferencias reales de la **Cursor CLI** (verificados contra la docs oficial de cursor.com).

## Qué hace la skill
Orquesta delegación de coding al agente de Cursor desde mi terminal, en dos modos:
- **Print mode (`agent -p "..."`)** — tarea de una pasada, sin diálogos, salida JSON/texto. El modo que uso para la mayoría.
- **Interactivo vía tmux** — sesiones multi-turno con `capture-pane`/`send-keys`.

## Diferencias clave que documenté vs Claude Code
- Comando base es **`agent`** (no `claude`), y la instalación es `curl https://cursor.com/install | bash` (Win: `irm 'https://cursor.com/install?win32=true' | iex`).
- **Print mode NO edita archivos a menos que pongas `--force`/`--yolo`** — sin eso solo propone cambios. Esto es distinto y crítico.
- Auth con **`CURSOR_API_KEY`** (no `ANTHROPIC_API_KEY`), o `agent login` (OAuth).
- Config en **`~/.cursor/cli-config.json`** (no `.claude/settings.json`). Permisos con formato `Shell(git)`, `Write(src/**)`, etc.
- Flags reales incluidos: `--model`, `--trust` (headless), `--worktree`/`-w`, `--output-format json|stream-json`, `--approve-mcps`, `--sandbox`, `--resume`/`--continue`.
- **No tiene `--max-turns`/`--max-budget-usd`** (lo señalo como limitación) ni `--from-pr` (para PRs, uso `gh pr diff 42 | agent -p ...`).
- `--trust` solo funciona en modo headless, cloud-agent mode con `&`, `/cursor` para saltar al IDE.

## Estado en tu máquina
Verifiqué y **`agent` no está instalado** (`AGENT_NOT_FOUND`). Para usar la skill necesitas el setup:

```bash
# Windows (PowerShell) — o desde el terminal de Hermes:
irm 'https://cursor.com/install?win32=true' | iex
# Luego: agent login  (OAuth)  o  $env:CURSOR_API_KEY=
```

¿Quieres que **te instale la Cursor CLI ahora** (es un cambio a nivel sistema, así que lo dejo a tu `confirmo`)? Si ya tienes Cursor con licencia/API key, te armo el comando de instalación y verifico que `agent --version` corra desde el terminal de Hermes.

### Usuario

si

### Asistente

Confirmado. Voy a instalar la Cursor CLI. Como el terminal de Hermes es git-bash (no PowerShell), llamo a `powershell.exe` para el instalador oficial de Windows. Primero verifico que PowerShell esté disponible y que podamos alcanzar el instalador.

### Asistente

PowerShell disponible. Ejecuto el instalador oficial de Windows (`irm ... | iex`). Esto descarga y registra el binario `agent` en el PATH del sistema.

### Asistente

Instalación completó ("Happy coding!"). Ahora verifico que el binario `agent` esté accesible desde el terminal de Hermes. El PATH nuevo puede no verse en la sesión actual, así que reviso varias rutas.

### Asistente

No aparece en PATH todavía. El instalador pudo ponerlo en una ruta que no está en el PATH de git-bash. Busco dónde quedó el binario.

### Asistente

Hay un dir `C:\Users\david\AppData\Local\Programs\cursor`. El binario `agent` suele quedar ahí. Busco el ejecutable.

### Usuario

continua

### Asistente

El binario no aparece en esa carpeta. Busco más amplio para ubicar dónde quedó `agent.exe`.

### Asistente

El instalador dijo "Happy coding!" pero no encuentro `agent.exe`. Posiblemente lo dejó en una ruta fuera de mi búsqueda, o añadió el PATH pero mi sesión de git-bash no lo ve. Compruebo con PowerShell fresco (que sí lee el PATH actualizado) y busco por todo el perfil.

### Asistente

Encontré la entrada en PATH: `C:\Users\david\AppData\Local\Programs\cursor\resources\app\bin`. Reviso qué binario hay ahí.

### Asistente

Esa carpeta es la del launcher de la app (GUI), no el CLI `agent`. El instalador reportó éxito pero el binario `agent.exe` no aparece. Busco de forma más amplia y eficiente con la herramienta de búsqueda.

### Asistente

No hay `agent.exe` en ninguna parte del perfil. El instalador mostró el mensaje de éxito (es el script estándar de Cursor), pero en esta máquina el binario no quedó escrito — probablemente porque ya existe la app GUI de Cursor instalada y el instalador CLI asume otra ruta, o el script de Windows en este entorno no descargó el ejecutable. 

Voy a reintentar el instalador capturando TODO el output (no solo el tail) para ver si hubo un error silencioso o una ruta distinta.

### Asistente

El script se ejecuta pero no deja rastro del binario. Voy a inspeccionar qué hace realmente el instalador: descargo el script (sin ejecutar) y lo leo para ver dónde espera dejar `agent.exe`.

### Asistente

Lo descargué. Lo leo para ver la lógica de instalación (dónde descarga y a qué ruta escribe el binario).

### Asistente

Ahora entiendo el script: instala en **`%LOCALAPPDATA%\cursor-agent`** (no donde busqué) y descarga un zip de `downloads.cursor.com`. El binario no apareció → la descarga probablemente falló de forma silenciosa (el script no usa `-ErrorAction Stop`). Verifico esa carpeta.

### Asistente

Sí se descargó e instaló, pero en `dist-package`/`versions/<version>/` — el script luego copia los `cursor-agent*` al root de `%LOCALAPPDATA%\cursor-agent\`. Ahí solo veo `agent.ps1`, `agent.cmd`, `cursor-agent.ps1`, etc., pero **no el `cursor-agent.exe`**. La copia del .exe falló (probablemente el zip no lo expandió ahí, o el nombre difiere). Reviso el contenido del zip extraído y los .ps1 para ver cómo lanza el binario.

### Asistente

El .ps1 resuelve la versión. Leo el resto para ver cómo lanza `node.exe` + `index.js` desde `versions/<version>/`.

### Asistente

El mecanismo de lanzamiento es: `agent.ps1` busca el dir de versión más reciente y corre `node.exe index.js`. Hay `node.exe` en la carpeta de versión. La causa de que no funcionara es que `%LOCALAPPDATA%\cursor-agent` se añadió al PATH de usuario pero mi sesión de git-bash arrancó antes, así que no lo ve. Pruebo lanzándolo directo por PowerShell con la ruta completa.

### Asistente

El `$` lo interpretó bash antes de llegar a PowerShell. Uso la ruta nativa absoluta directa.

### Asistente

Funciona: el binario responde con versión `2026.07.16-899851b`. El único problema es que el PATH de usuario no está visible en mi sesión de git-bash (arrancó antes de la instalación). Para que la skill pueda invocar `agent` directamente, creo un wrapper en `/usr/local/bin`. Verifico primero dónde está y si está en PATH.

### Asistente

`/usr/local/bin` está en PATH. Creo un wrapper `agent` en bash que invoca el `agent.ps1` real vía PowerShell, pasando los argumentos correctamente. Así la skill puede llamar `agent` directo desde el terminal de Hermes.

### Asistente

Doy permisos de ejecución y pruebo invocándolo como `agent` desde bash.

### Asistente

`agent --version` funciona directo desde bash. Ahora verifico el resto del pipeline de la skill: status/auth, listado de modelos, y un `agent -p` de prueba (solo lectura, sin `--force`, para no tocar nada).

### Asistente

El CLI está instalado y operativo, pero **no está autenticado** ("Not logged in"). Sin auth no puede ejecutar tareas. Aquí necesito tu decisión porque es un paso con credenciales:

Tienes dos opciones para autenticar:

1. **OAuth interactivo (`agent login`)** — abre el navegador para iniciar sesión con tu cuenta de Cursor. Como es interactivo, lo lanzo en tmux y tú haces el login en el navegador. Requiere que tengas una cuenta de Cursor con plan activo.

2. **API key (`CURSOR_API_KEY`)** — si tienes una API key de Cursor, me la pasas (o la seteo como variable de entorno) y listo, sin navegador.

¿Cuál prefieres? Si es la **opción 1**, confirmo y lanzo `agent login` en tmux para que hagas el login. Si es la **2**, necesito que me facilites la API key (o me digas si ya la tienes guardada en algún lado de tu máquina y la localizo).

Mientras tanto, recapitulando lo logrado:
- ✅ Skill `cursor-code` creada y verificada contra docs reales
- ✅ Cursor CLI instalado en `%LOCALAPPDATA%\cursor-agent` (v2026.07.16-899851b)
- ✅ Wrapper `agent` en `/usr/local/bin` → funciona desde el terminal de Hermes
- ⏳ Pendiente: autenticación

¿Por dónde seguimos con el login?

### Usuario

1

### Asistente

Opción 1 confirmada: lanzo `agent login` interactivo (OAuth vía navegador). Primero verifico que tmux esté disponible en este host.

### Asistente

No hay tmux. Para el login interactivo uso el terminal en modo PTY (pseudo-terminal real). Lanzo `agent login` en background con PTY para no bloquear y poder revisar su salida.

### Asistente

`agent login` está corriendo en PTY (modo interactivo, espera tu acción en navegador). Reviso su salida para ver qué URL/mensaje desplegó.

### Asistente

El CLI abrió el flujo de login OAuth. **No puedo abrir el navegador desde aquí (entorno sin GUI directa), así que necesitas hacer el login tú.** 

Usa este enlace en tu navegador (Brave) para autenticarte con tu cuenta de Cursor:

🔗 **https://cursor.com/loginDeepControl?challenge=nSYG5M7Di1b_dPGndubcdndsQMdJcZyQ0yhEd1km2c4&uuid=927298b2-412d-4e22-b19f-dff75474eb28&mode=login&redirectTarget=cli**

Pasos:
1. Abre ese enlace en Brave e inicia sesión con tu cuenta de Cursor (debe tener plan que permita el CLI agent).
2. El terminal de aquí quedará esperando (`Waiting for browser authentication...`). En cuanto completes el login en el navegador, el proceso confirma automáticamente.
3. Si el navegador no abre solo, también puedes presionar `q` en el terminal para mostrar un **código QR** y escanearlo desde el móvil.

Avísame cuando hayas completado el login en el navegador y yo verifico que el proceso confirmó (`agent status` → debería salir tu cuenta en vez de "Not logged in").

Mientras esperas, el proceso sigue vivo en background (no lo cierro). Cuando termines, dime y reviso el estado.

### Usuario

listo

### Asistente

Verifico que el login se confirmó.

### Asistente

Login confirmado: **✓ Logged in as davidbarce0411@gmail.com**. Verifico estado y modelos disponibles, y hago una prueba real de `agent -p` (solo lectura, sin `--force`).

### Asistente

Autenticado y con modelos disponibles (GPT-5.x, Codex, etc.). Hago una prueba real de la skill con un `agent -p` de solo lectura en un directorio de prueba, para confirmar todo el pipeline end-to-end sin tocar nada.

### Asistente

El wrapper pasa la ruta tal cual y Cursor la interpretó como `C:\tmp\cursor_test` (en Windows, `/tmp` no existe). Uso una ruta nativa de Windows real.

### Asistente

Timeout de 180s. El agente probablemente quedó esperando algo (o el prompt necesita un modelo explícito y default tardó). Reviso si el proceso sigue vivo y su salida parcial.

### Asistente

El `agent -p` (foreground) expiró a los 180s. Puede que el modelo `auto` esté tardando o haya quedado colgado. Lo relanzo en background con un modelo explícito y salida a log, para no bloquear y ver el resultado real.

### Asistente

Relancé en background con modelo `gpt-5.2` explícito. Espero a que termine.

### Asistente

El wait tiene límite de 60s. Reviso el log del proceso.

### Asistente

El log está vacío. El agente sigue corriendo en background. Espero un poco más y reviso.

### Asistente

Sigue corriendo (110s, sin salida aún). El agente puede estar tardando en arrancar node/descargar o esperando algo. Lo dejo avanzar y vuelvo a revisar en unos segundos.

### Asistente

Salió (exit 0). Leo el log.

### Asistente

¡Funciona end-to-end! El agente respondió: *"`calc.py` define una función `add(a, b)` que devuelve la suma de dos valores."* con `EXIT=0`.

Todo el pipeline está verificado y operativo. Limpio el directorio de prueba y cierro el proceso de login.

### Asistente

El login quedó cerrado. El rm falló porque el agente de prueba aún sostenía el directorio. Reintento la limpieza.

### Asistente

Aún "busy" (probablemente un handle de node del agente de prueba no se liberó del todo). No es crítico — es un directorio de prueba temporal. Lo dejo y verifico que el agente de prueba sí terminó; el contenido es inofensivo. Reintento final con un breve espera.

### Asistente

Queda un handle abierto, pero es solo el dir de prueba temporal (`calc.py` de 30 bytes, inofensivo) — se liberará solo al reiniciar sesión. No afecta nada. Todo lo importante quedó verificado.

## ✅ Resumen final — todo operativo

**1. Skill `cursor-code` creada** (`autonomous-ai-agents/cursor-code/SKILL.md`)
- Paralela a `claude-code`, con comandos y diferencias reales de la Cursor CLI (verificados contra la docs oficial de cursor.com).
- Cubre: install, auth, print mode (`-p`), interactivo vía tmux, flags reales (`--force`/`--yolo`, `--model`, `--trust`, `--worktree`, `--output-format`, `--resume`), permisos (`~/.cursor/cli-config.json`), PR review, instancias paralelas, y las **gotchas clave** (print mode no edita sin `--force`; usa `CURSOR_API_KEY`; no tiene `--max-turns`/`--from-pr`).

**2. Cursor CLI instalado y funcional**
- Binario en `%LOCALAPPDATA%\cursor-agent` (v2026.07.16-899851b).
- Wrapper `agent` en `/usr/local/bin` → invocable directo desde el terminal de Hermes (resuelve el PATH que no se propagó a git-bash).
- Login OAuth completado: **davidbarce0411@gmail.com**.
- Modelos disponibles: GPT-5.1/5.2/5.3, Codex variants, etc.
- **Prueba end-to-end exitosa**: `agent -p` analizó `calc.py` y respondió correctamente (`EXIT=0`).

**Un detalle técnico aprendido** (lo dejo anotado para la skill): las rutas `/tmp/...` se resuelven como `C:\tmp\...` dentro del wrapper PowerShell, así que en la prueba hay que usar rutas nativas Windows (`C:/Users/...`). Voy a añadir esa nota a la skill para evitar el error la próxima vez.

### Asistente

La nota quedó integrada. Verifico que la sección no quedó duplicada ni garblada.

### Asistente

The skill file got mangled — my patch created a duplicate/garbled pitfall 8 (there's a dangling "(it" and two "8." entries). Let me read the exact current block and rewrite it cleanly.

### Asistente

The patch left a garbled duplicate. Let me rewrite that whole block cleanly.

### Asistente

La sección quedó limpia y correcta. Todo verificado.

## ✅ Todo listo — resumen final

**Skill `cursor-code`** (`autonomous-ai-agents/cursor-code/SKILL.md`) — creada, verificada contra docs reales, y end-to-end probada:
- Install (PowerShell), auth (`agent login` OAuth → davidbarce0411@gmail.com), print mode, interactivo tmux, flags reales, permisos, PR review, paralelismo.
- Gotchas documentados: print mode no edita sin `--force`; usa `CURSOR_API_KEY`; no tiene `--max-turns`/`--from-pr`; y las dos lecciones aprendidas hoy en tu máquina (PATH no se propaga a git-bash → wrapper en `/usr/local/bin/agent`, y rutas `/tmp` se resuelven como `C:\tmp` → usar rutas Windows nativas).

**Cursor CLI operativo en tu máquina:**
- Binario v2026.07.16-899851b en `%LOCALAPPDATA%\cursor-agent`
- Wrapper `agent` en `/usr/local/bin` → funciona directo desde el terminal de Hermes
- Autenticado y con modelos (GPT-5.1/5.2/5.3, Codex variants)
- Prueba real exitosa: analizó `calc.py` y respondió bien (`EXIT=0`)

**Notas menores:**
- El dir de prueba `Temp/cursor_test` quedó con un handle abierto (un residuo de node del agente de prueba) y no se pudo borrar; es inofensivo (un `calc.py` de 30 bytes) y se libera al reiniciar sesión.
- El proceso de login ya lo cerré.

Cuando quieras delegar un coding task real a Cursor, solo dímelo y lo lanzo vía `agent -p` (con `--force` si esperas ediciones, y ruta Windows nativa en `workdir`). ¿Hay algún proyecto en el que quieras que lo pruebe?

### Usuario

primero, configura que el modelo sea siempre auto a menos que yo te especifique lo contrario

### Asistente

Entendido. `auto` ya es el default del CLI, pero lo dejo explícito y persistente: lo grabo en memoria como tu preferencia y lo fijo en la skill para que siempre use `--model auto` salvo que tú indiques otro.

### Asistente

Hay un salto de numeración (dos "6."). Lo corrijo para que quede secuencial.

### Asistente

Listo. Configurado en dos capas:

1. **Memoria persistente** (user profile): registré que, al delegar a Cursor, el modelo por defecto es `auto` salvo que tú nombre otro explícitamente. Aplica en todas las sesiones futuras, no solo esta.
2. **Skill `cursor-code`**: añadí la regla #6 — *"Model default is `auto` — always pass `--model auto` unless David explicitly names another model"* en la sección de reglas del agente, y corregí la numeración.

De ahora en adelante, cualquier `agent -p` que lance usará `--model auto` automáticamente. Si en algún momento quieres un modelo concreto (ej. `gpt-5.3-codex-xhigh` para algo complejo), me dices y lo uso solo para esa tarea.

¿Seguimos con algo más de configuración, o pasamos a probar un coding task real?

### Usuario

puedes tambien hacer que cuando lo diga, segun la tarea tu mismo elijas el modelo?

### Asistente

Claro. Voy a actualizar la regla en la skill y en memoria para que, cuando me pidas que yo elija ("elige tú el modelo" / "tú decides"), seleccione el modelo según la complejidad de la tarea en lugar de usar `auto`.

Primero localizo la entrada de memoria para actualizarla en vez de duplicarla.

### Asistente

Actualizo la entrada de memoria para reflejar ambas reglas (auto por defecto + elección propia bajo petición).

### Asistente

Listo. Ahora el comportamiento de modelos para delegaciones a Cursor queda así:

- **Por defecto:** `--model auto` (salvo que nombres otro explícitamente).
- **Si me dices "elige tú el modelo" / "tú decides":** yo selecciono según la complejidad de la tarea y te digo cuál y por qué:
  - Tareas simples/rápidas (un edit, lint, review pequeño) → modelo ligero/rápido (ej. `gpt-5.2`, `gpt-5.3-codex-low-fast`).
  - Trabajo complejo multi-paso (refactors, features nuevas, debugging, multi-archivo) → modelo frontier (ej. `gpt-5.3-codex-xhigh`).

Guardado en memoria (persistente entre sesiones) y reflejado en la regla #6 de la skill `cursor-code`.

¿Quieres que probemos ya con un coding task real — y si quieres, puedes decirme "elige tú el modelo" para verlo en acción?

### Usuario

pero me refiero a elegir entre todos los modelos que ofrece cursor

### Asistente

Claro, lo ajusto: cuando digas "elige tú", elijo entre **todo el catálogo** de modelos de Cursor (no solo los ejemplos), consultando `agent models` si hace falta para ver lo disponible en tu cuenta.

### Asistente

Listo. Ahora la regla dice claramente: si me pides "elige tú el modelo", selecciono entre **todo el catálogo de Cursor** (GPT-5.1/5.2/5.3, todas las variantes Codex low/medium/high/xhigh/fast, opus si está disponible en tu cuenta), consultando `agent models` para ver los reales. Criterio: simple/rápido → modelo ligero; complejo multi-paso → el más capaz. Y siempre te digo cuál elegí y por qué.

Actualizado en memoria (persistente) y en la regla #6 de la skill `cursor-code`.

¿Probamos un coding task real ya? Puedes decirme "elige tú el modelo" para ver la selección automática en acción.

### Usuario

tambien puedes tener un criterio mucho mas riguroso con los ranking de openrouter

### Asistente

Bien, subo el criterio: cuando elija modelo, usaré los **rankings de OpenRouter** como base rigurosa (no a ojo) para rankear los candidatos y cruzarlos con el catálogo real de tu cuenta. Actualizo memoria y la regla #6 de la skill.

### Asistente

Listo. Ahora el criterio de selección propia es riguroso y basado en datos:

- **Catálogo completo de Cursor** (`agent models`) como universo de opciones.
- **Rankings de OpenRouter** como base objetiva: antes de elegir, consulto el leaderboard actual (vía `web_search` o el endpoint `/api/v1/models` de OpenRouter) y rankeo los candidatos por capacidad de coding/inteligencia.
- Cruzo ranking × disponibilidad en tu cuenta:
  - Tarea simple/rápida → modelo bien rankeado pero eficiente.
  - Tarea compleja multi-paso → el de mayor ranking disponible.
- Siempre te reporto: **qué modelo elegí, su posición en el ranking y por qué**.

Guardado en memoria (persistente) y en la regla #6 de la skill `cursor-code`.

¿Quieres que probemos ahora con un coding task y me digas "elige tú el modelo" para ver el flujo completo (consulta de ranking → elección → ejecución)?


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
