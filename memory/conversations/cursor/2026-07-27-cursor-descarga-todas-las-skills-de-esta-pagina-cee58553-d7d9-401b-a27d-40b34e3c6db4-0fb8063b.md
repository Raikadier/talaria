---
date: 2026-07-27
type: conversation
source_agent: cursor
session_id: "cee58553-d7d9-401b-a27d-40b34e3c6db4"
project: "empty-window"
source_path: "C:\\Users\\david\\.cursor\\projects\\empty-window\\agent-transcripts\\cee58553-d7d9-401b-a27d-40b34e3c6db4\\cee58553-d7d9-401b-a27d-40b34e3c6db4.jsonl"
tags: [conversation, imported, cursor]
title: "descarga TODAS las skills de esta pagina:"
---

# descarga TODAS las skills de esta pagina:

**Fecha:** 2026-07-27  
**Agente:** cursor  
**Proyecto/contexto:** empty-window  
**Sesión:** `cee58553-d7d9-401b-a27d-40b34e3c6db4`  
**Origen:** `C:\Users\david\.cursor\projects\empty-window\agent-transcripts\cee58553-d7d9-401b-a27d-40b34e3c6db4\cee58553-d7d9-401b-a27d-40b34e3c6db4.jsonl`

## Mensajes

### Usuario

descarga TODAS las skills de esta pagina:

https://hermes-agent.nousresearch.com/docs/skills

luego organizalas y subelas a mi banco personal de skills en github

### Asistente

Voy a revisar la página de skills y localizar tu banco personal en GitHub para bajarlas, organizarlas y subirlas.
[tool:WebFetch]
[tool:GetMcpTools]
[tool:Shell]

### Asistente

La página carga el catálogo de forma dinámica; voy a inspeccionar la API y tu repo de skills en GitHub.
[tool:AwaitShell]
[tool:GetMcpTools]
[tool:WebSearch]

### Asistente

Encontré tu banco `Raikadier/agent-skills-bank`. El catálogo indica ~88k skills; voy a inspeccionar el índice, la estructura del repo y qué es descargable de forma realista.
[tool:Shell]
[tool:Shell]
[tool:GetMcpTools]
[tool:GetMcpTools]

### Asistente

El índice parece muy grande; voy a medir su tamaño y localizar las skills oficiales de Hermes.
[tool:Shell]
[tool:CallMcpTool]

### Asistente

El catálogo ya cargó: **90.681 skills** en 12 registros. Antes de seguir, necesito acotar el alcance.
[tool:CallMcpTool]
[tool:Shell]

### Asistente

El Skills Hub tiene **90.681 skills** en 12 registros. Tu banco ya es [`Raikadier/agent-skills-bank`](https://github.com/Raikadier/agent-skills-bank) (privado), con ~73 skills oficiales de Hermes + 989 de comunidad.

Descargar el contenido completo de las 90k no es realista en una sola pasada (ClawHub solo son ~69k; el repo se haría enorme y chocaría con rate limits).

| Fuente | Cantidad |
|--------|----------|
| ClawHub | 69.150 |
| skills.sh | 19.967 |
| LobeHub | 505 |
| browse.sh | 440 |
| NVIDIA | 299 |
| optional (Hermes) | 111 |
| built-in (Hermes) | 69 |
| gstack / OpenAI / HF / Anthropic / Marketplace | ~140 |

¿Qué alcance quieres?

1. **Oficiales Hermes** — built-in + optional (~180), organizadas como en tu banco
2. **Oficiales + taps GitHub** — Anthropic, OpenAI, HF, NVIDIA, gstack (~620)
3. **Catálogo completo en metadatos** — las 90k como índice + contenido solo de oficiales/GitHub
4. **Literalmente todo el contenido** — incluye ClawHub/skills.sh; puede tardar días y ocupar mucho

Dime el número (o una mezcla) y lo ejecuto.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

Las tareas en segundo plano ya cerraron: localicé tu banco en `Raikadier/agent-skills-bank` y el catálogo útil es `skills.json` (~90k entradas). La descarga del índice grande se interrumpió a propósito; no hace falta.

Sigo esperando que elijas el alcance (1–4) de mi mensaje anterior para empezar a bajar y subir.

### Usuario

4. TODO. vez descargando por secciones ordenadamente.

### Asistente

Opción 4: vamos a bajar todo por secciones, empezando por las más pequeñas y ordenadas. Primero inspecciono el catálogo y preparo el repo.
[tool:TodoWrite]
[tool:GetMcpTools]
[tool:Shell]

### Asistente

Voy a clonar el banco y bajar por secciones: primero repos GitHub enteros, luego ClawHub/skills.sh por API.
[tool:WebFetch]
[tool:CallMcpTool]
[tool:Shell]


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
