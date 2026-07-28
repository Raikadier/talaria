---
date: 2026-07-11
type: conversation
source_agent: hermes
session_id: "20260711_123912_fa129e"
project: "tui"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, tui]
title: "examina todas las tools y skills que tiene opencode y absorvelas, despues subelas a mi ban"
---

# examina todas las tools y skills que tiene opencode y absorvelas, despues subelas a mi ban

**Fecha:** 2026-07-11  
**Agente:** hermes  
**Proyecto/contexto:** tui  
**Sesión:** `20260711_123912_fa129e`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

examina todas las tools y skills que tiene opencode y absorvelas, despues subelas a mi banco personal de skills y tools

### Asistente

Voy a examinar primero las skills relevantes: la de `opencode` y las de tu banco personal de skills.

### Asistente

Voy a investigar el estado actual antes de actuar: dónde vive el skill `opencode`, sus skills relacionadas (claude-code, codex, hermes-agent), y si tu banco de GitHub (`Raikadier/agent-skills-bank`) ya está clonado localmente.

### Asistente

El find no encontró nada porque el skill vive en `AppData\Local` (no `Roaming`). Déjame buscar correctamente y ver la estructura del banco local.

### Asistente

El skill `opencode` pertenece a la categoría `autonomous-ai-agents`, que además contiene `claude-code`, `codex` y `hermes-agent` (los "coding agents" que delegan a distintas CLIs). Esa es la familia completa de "tools y skills que tiene opencode". Déjame ver qué ya existe en el banco para no duplicar.

### Asistente

Tanto el banco como el directorio live ya contienen `opencode/SKILL.md` junto a sus skills hermanas (`claude-code`, `codex`, `hermes-agent`). Esa es la familia completa de "coding agents" que `opencode` agrupa. Déjame verificar si el banco está sincronizado con el live y si OpenCode CLI está realmente instalado (por si "tools y skills que tiene opencode" se refiere a su propia instalación).

### Asistente

El banco ya tiene `opencode` + `claude-code` + `codex` + `hermes-agent` comprometidos y sincronizados (git status limpio, sin diferencias con el live). Pero hay una config de OpenCode en `~/.config/opencode`. "Las tools y skills que tiene opencode" podría referirse a lo que OpenCode define en su config propia. Déjame leerla.

### Asistente

Encontré el dato clave: OpenCode tiene configurado un **MCP server de Supabase** (`https://mcp.supabase.com/mcp?project_ref=adretkrvrrezyvoyegkx`). Esa es una "tool" real de OpenCode que no está en el skill. Déjame confirmar si OpenCode define más tools/skills (agentes propios, comandos) inspeccionando su config completa y caché.

### Asistente

OpenCode CLI no tiene agentes/comandos extra — su única "tool" configurada es el **MCP server de Supabase** (con auth guardada en `mcp-auth.json`). El banco tiene una carpeta `tools/` según su estructura. Déjame ver qué hay ahí y confirmar el estado del repo remoto.

### Asistente

Ya tengo el panorama completo. Resumen de lo que "tiene" OpenCode en tu entorno:

- **Skill de Hermes `opencode`** (categoría `autonomous-ai-agents`) → ya está en tu banco y sincronizado con GitHub (git status limpio, 0↔0 con origin/main).
- **Familia de skills hermanas** del mismo coding-agent: `claude-code`, `codex`, `hermes-agent` → también ya en el banco.
- **La única "tool" real configurada de OpenCode**: un **MCP server de Supabase** (`~/.config/opencode/opencode.json`), con auth cacheada. Esto NO estaba documentado en el banco.
- **OpenCode CLI no está instalado** actualmente (no hay binario) — dato importante para que el skill sea usable.

Voy a absorber esa tool real (el MCP de Supabase + estado de instalación) como referencia del skill, en ambos lados (live de Hermes y banco), y luego subirlo a GitHub.

### Asistente

Ahora también linkeo esta referencia en el SKILL.md del banco (para que `skill_view` la muestre) y actualizo el README del banco con la nota de la tool de Supabase. Luego commiteo y subo a GitHub.

### Asistente

Ahora commiteo en el banco y subo a GitHub (siguiendo los gotchas de MSYS del skill: `git -c core.autocrlf=false`, push en background con notify).

### Asistente

Commit hecho. Ahora subo a GitHub.

### Asistente

Listo. Subido correctamente a GitHub (`a3ddbaa..7ce4f31`). Verifico que el live de Hermes y el banco queden idénticos.

### Asistente

Voy a hacer una verificación ad-hoc enfocada (no hay suite de tests para skills): confirmar existencia de los archivos en ambos lados, validar el JSON, y que el callout quedó en el SKILL.md.

### Asistente

`python3` no existe; uso `python` (3.11 instalado).

### Asistente

El FAIL es un falso negativo de mi script: busqué `"NOT installed"` (mayúsculas) pero el callout dice `"not installed"` (minúsculas). Confirmo leyendo el SKILL.md directamente.

### Asistente

El callout sí está (líneas 14-17), con "not installed" en minúsculas. Mi script falló por sensibilidad a mayúsculas. Re-ejecuto la verificación corregida para confirmar limpio.

### Asistente

Bug mío: intercambié la tupla (label, base). Corrijo.

### Asistente

Re-ejecuto una verificación final limpia para dejar evidencia fresca (el archivo temporal ya fue borrado; lo recreo, corro y limpio).

### Asistente

Verificación ad-hoc fresca (no hay suite de tests para skills — esto es verificación manual enfocada, NO "suite green"):

- ✅ `references/davids-opencode-tools.md` y `references/opencode-config.json` existen en **live** y en el **banco**.
- ✅ JSON válido y con el MCP de Supabase (`project_ref=adretkrvrrezyvoyegkx`) en ambos lados.
- ✅ Callout de absorción presente en el `SKILL.md` (live + banco).
- ✅ Las 4 skills (`opencode`, `claude-code`, `codex`, `hermes-agent`) son **idénticas** entre live y banco.
- 🧹 Temp de verificación creado y borrado.

Resultado: **ALL PASS**. No queda nada por corregir; el trabajo de absorción y subida al banco quedó verificado localmente y el push a GitHub ya se confirmó vía API.


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
