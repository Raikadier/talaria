---
date: 2026-07-25
type: conversation
source_agent: hermes
session_id: "20260725_143230_713d42"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Instalación de skill Impeccable para diseño UI/UX"
---

# Instalación de skill Impeccable para diseño UI/UX

**Fecha:** 2026-07-25  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260725_143230_713d42`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

descarga la skill impeccable para hacer diseños ui/ux

### Asistente

Voy a buscar qué es la skill "impeccable" para UI/UX, porque no aparece en mi lista local de skills.

### Asistente

Encontré la skill: `pbakaus/impeccable` en GitHub. Es un "upgrade" del skill `frontend-design` de Anthropic. Voy a revisar la estructura del repo para instalarla correctamente en Hermes.

### Asistente

Es `pbakaus/impeccable` — un skill de diseño UI/UX (el "upgrade" de `frontend-design` de Anthropic). Voy a inspeccionar la estructura real del skill dentro del repo para copiarla correctamente a la carpeta de skills de Hermes.

### Asistente

Git está disponible. Voy a clonar el repo (shallow) para extraer el skill real y adaptarlo a Hermes.

### Asistente

Tengo el skill clonado. Voy a revisar el SKILL.md y la estructura de scripts/agents para entender cómo adaptarlo a Hermes.

### Asistente

Es el skill `pbakaus/impeccable` (v4.0.2) — 1 skill con 23 comandos, 60 reglas deterministas anti-"AI slop", y referencias de diseño. Lo tengo clonado. Ahora lo adapto al formato de skills de Hermes (renombro `reference/`→`references/` que es lo que Hermes reconoce, y corrijo las rutas de scripts).

### Asistente

Ahora verifico cómo resuelven su propia ruta los scripts (para no dejar rutas rotas de `.agents/skills/impeccable`) y corrijo los links `reference/`→`references/` en el SKILL.md.

### Asistente

Los scripts usan imports relativos (`./lib/...`), así que resuelven bien desde su propia ubicación. Solo hay 1 ruta hardcodeada `.agents/skills/impeccable` en hook-admin.mjs (gestión de hooks de Claude Code, no esencial en Hermes). Verdad reviso si los scripts referencian `reference/` y corrijo los links del SKILL.md.

### Asistente

Los `reference/` en los scripts son texto de guía (strings que el LLM lee), no rutas de disco. Pero debo confirmar cómo `context.mjs` carga realmente los archivos de referencia desde el filesystem, para saber si renombrar afecta.

### Asistente

Los scripts leen los archivos de referencia parseando los links `reference/...` del propio SKILL.md (línea 967: `path.join(here, '..', 'SKILL.md')`). Así que renombrar a `references/` requiere también corregir los links del SKILL.md. Voy a confirmar cómo resuelve la ruta y luego hacer el reemplazo masivo.

### Asistente

Confirmado: los scripts parsean los links `reference/...` del SKILL.md para localizar los archivos. Renombrar la carpeta a `references/` y dejar los links como `reference/` rompería la carga. La solución limpia es **dejar la carpeta como `reference/`** (no `references/`) para que todo encaje sin tocar 88 scripts. 

De todos modos, Hermes lista las skills por el frontmatter del SKILL.md, y `skill_view` con `file_path` accede a archivos dentro de la skill. La convención `references/` es para el índice de skill_view, pero el acceso por ruta funciona con cualquier nombre. Verifico cómo Hermes indexa el skill.

### Asistente

Mantengo la carpeta como `reference/` (los scripts parsean los links del SKILL.md para localizar archivos, renombrar rompería la carga). Ahora verifico que Hermes carga el skill correctamente.

### Asistente

El skill no se encontró porque Hermes busca skills en `Local\hermes\skills`, no en `Roaming`. Muevo la carpeta al lugar correcto.

### Asistente

El listado muestra `references` (con s) — pero los scripts parsean los links `reference/` del SKILL.md, así que la carpeta debe llamarse exactamente `reference`. Renombro.

### Asistente

Ahora verifico que Hermes carga el skill. Puede requerir recargar el índice de skills; intento `skill_view`.

### Asistente

Listo. El skill cargó correctamente (v4.0.2, readiness "available"). Marco las tareas como completadas y verifico un archivo de referencia por ruta.

### Asistente

Listo. La skill `impeccable` (v4.0.2) quedó instalada y verificada en Hermes.

## ✅ Skill `impeccable` instalada

**Qué es:** el "upgrade" de `frontend-design` de Anthropic — un sistema de diseño UI/UX para agentes de IA. 1 skill, **23 comandos**, **60 reglas deterministas anti-"AI slop"** (evita lo típico: Inter para todo, gradientes morado-azul, tarjetas anidadas, texto gris sobre fondos de color, etc.).

**Dónde quedó:** `C:\Users\david\AppData\Local\hermes\skills\impeccable\`
- `SKILL.md` (frontmatter + comandos)
- `reference/` — 34 playbooks (new-work, critique, audit, polish, bolder, quieter, animate, live, etc.)
- `scripts/` — 88 archivos `.mjs` (context loader, detector de anti-patrones, live browser mode, etc.)
- `agents/` — subagentes (asset producer, documenter, finish reviewer, manual-edit applier)

**Comandos principales** (se invocan como `impeccable <comando> [target]`):
- `init` — captura contexto del producto en `PRODUCT.md` / `DESIGN.md`
- `craft` / `shape` / `new-work` — construir o rediseñar desde cero
- `critique` / `audit` — revisión UX y chequeos técnicos (a11y, perf, responsive)
- `polish` / `bolder` / `quieter` / `distill` / `harden` / `onboard` — refinar
- `animate` / `colorize` / `typeset` / `layout` / `delight` / `overdrive` — mejorar
- `clarify` / `adapt` / `optimize` / `live` — corregir/iterar

**Notas:**
- Node v22 ya está disponible (viene con Hermes), así que los scripts `.mjs` corren sin instalar nada.
- Los scripts resuelven su propia ruta desde `SKILL.md`, por eso dejé la carpeta como `reference/` (no `references/`) para que no se rompa la carga.
- El hook de detector automático (corre tras editar UI) y el CLI `npx impeccable` son para Claude Code/Cursor/Codex; en Hermes usas los comandos vía `skill_view(name='impeccable')` y cargando el playbook que toque.

Para usarla: dime qué diseño quieres (landing, dashboard, app, etc.) y cargo `impeccable` + el playbook correspondiente.

### Usuario

ahora quiero que lo subas a mi banco de skills personal

### Asistente

Voy a cargar el skill `personal-skills-bank` para saber dónde está tu banco personal y cómo agregar la skill ahí.

### Asistente

El banco es el repo privado `Raikadier/agent-skills-bank`. `impeccable` es una skill comunitaria (de `pbakaus/impeccable`), así que va namespaced bajo `skills/community/pbakaus-impeccable/`. Primero sondo el estado del banco local y la autenticación.

### Asistente

El banco local existe, está en `main` con `origin` remoto, y hay borrados pre-existentes en el index (de un import anterior, sin commitear). Voy a copiar `impeccable` namespaced bajo `community/pbakaus-impeccable/`, descartar esos borrados del index (sin tocarlos en disco) y commitear solo la nueva skill. Primero verifico `.gitignore` y el conteo actual.

### Asistente

El banco está en `main` con `origin`. Hay 42 borrados pre-existentes en el index (de un import anterior, sin commitear) — no los toco. `impeccable` es comunitaria → va a `skills/community/pbakaus-impeccable/`. 

Primero verifico `.gitignore` con una ruta válida y copio la skill (tar pipe, sin `rsync`).

### Asistente

Copiado. Ahora commiteo **solo** el dir nuevo (sin tocar los 42 borrados pre-existentes), haciendo `git add` explícito del dir.

### Asistente

Commit exitoso (128 archivos de impeccable, 0 borrados tocados). Ahora hago push en background y verifico remotamente.

### Asistente

Push exitoso (`abb5f0de..f2cffaa4 main -> main`). Ahora verifico remotamente que la skill quedó.

### Asistente

Verificado remotamente. La skill quedó en tu banco.

### Asistente

✅ **`impeccable` subida a tu banco de skills personal** (`Raikadier/agent-skills-bank`).

**Detalles de la operación:**
- **Origen:** `C:\Users\david\AppData\Local\hermes\skills\impeccable` (donde la instalé en el paso anterior)
- **Destino en el banco:** `skills/community/pbakaus-impeccable/` (namespaced como skill comunitaria, siguiendo la regla del banco de no pisar tus 73 skills originales)
- **Commit:** `f2cffaa4` — *"Add community skill: pbakaus/impeccable (UI/UX design, v4.0.2)"* — 128 archivos (SKILL.md + 34 referencias + 88 scripts + 5 agents)
- **Push:** `abb5f0de..f2cffaa4 main -> main` ✓
- **Verificación remota:** el `SKILL.md` tiene sha `f954d4a5...` (confirmado que sí llegó)

**Notas importantes:**
- No toqué los **42 borrados pre-existentes** del index (eran de un import `sickn33/comfyui` anterior sin commitear). El commit de impeccable fue limpio: solo los 128 archivos nuevos, 0 borrados. Quedan ahí pendientes por si quieres resolverlos después.
- La skill **ya vive también en tu dir local de Hermes**, así que la puedes usar en cualquier sesión con `skill_view(name='impeccable')` o simplemente pidiéndome diseño UI/UX.

Para usarla: dime qué diseño quieres (landing, dashboard, app, rediseño) y cargo el playbook correspondiente.

¿Quieres que también cree un skill wrapper `impeccable` en tu categoría personal que llame la versión del banco, o con esto es suficiente?

### Usuario

esta bien

### Asistente

Perfecto. Queda disponible en dos lados:

- **Local (Hermes):** `C:\Users\david\AppData\Local\hermes\skills\impeccable` — usable ya en cualquier sesión.
- **Banco (GitHub):** `Raikadier/agent-skills-bank` → `skills/community/pbakaus-impeccable/` — respaldada.

Cuando quieras diseño UI/UX, solo dile y cargo el playbook (`init`, `critique`, `polish`, `bolder`, `live`, etc.).


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
