---
tags: [meta, framework, spine, standard, agents, organ]
aliases: [SPINE, spine, spine-framework, ironman, JARVIS, marco-ironman, suit-protocol]
version: 2.0
status: active
formerly: IRONMAN
---

# SPINE — Structured Protocol for Integrated Neural Execution

**Órgano:** sistema nervioso de [[organism|Talaria]]  
**Nombre técnico:** *Structured Protocol for Integrated Neural Execution*  
**Nombre de uso:** **SPINE**  
**Alias legado:** IRONMAN (mismo protocolo; no es otro producto)  
**Loop (7 capas):** Ingest → Normalize → Orient → Retrieve → Memorize → Act → Notify  
**Metáfora:** el vault es el cuerpo; el agente es el piloto; SPINE coordina los órganos. Las tools son efectores, no cerebros rivales.  
**Objetivo:** que cualquier agente (Cursor, Hermes, Claude…) opere el organismo **sin** que las tools se pisen.  
**Hermanos:** [[axon|AXON]] · [[forge|FORGE]] · [[memory-index|Memoria]] · [[cli|CLI/MCP]]

## Principio rector

> **Una sola fuente de verdad: el vault Markdown (Talaria).**  
> Toda tool es un *adaptador* o un *índice*. Ninguna tool es otra memoria canónica.

Si dos tools pueden escribir “la verdad”, una gana por contrato; la otra solo propone o indexa.

---

## Las 7 capas (no se cancelan: se encadenan)

```
[ Mundo exterior ]
       │
       ▼
┌──────────────┐
│ 1. INGEST    │  Capturar bytes/URLs/repos (sin decidir significado)
└──────┬───────┘
       ▼
┌──────────────┐
│ 2. NORMALIZE │  Todo → Markdown + YAML en el vault
└──────┬───────┘
       ▼
┌──────────────┐
│ 3. ORIENT    │  Clasificar: inbox → project/decision/learning/skill
└──────┬───────┘
       ▼
┌──────────────┐
│ 4. RETRIEVE  │  Índices de solo lectura (RAG/grafo/código)
└──────┬───────┘
       ▼
┌──────────────┐
│ 5. MEMORIZE  │  Escribir memoria canónica (protocolo agentes)
└──────┬───────┘
       ▼
┌──────────────┐
│ 6. ACT       │  Cambiar el mundo (código, PRs, mensajes) con evidencia del vault
└──────┬───────┘
       ▼
┌──────────────┐
│ 7. NOTIFY    │  Actualizar proyecto + enlaces + “última actividad”
└──────────────┘
```

| Capa | Pregunta que responde | Quién escribe al vault |
|------|------------------------|-------------------------|
| Ingest | ¿Qué entró? | Solo staging (`memory/inbox/**`) |
| Normalize | ¿Cómo se lee? | Staging convertido |
| Orient | ¿Dónde vive? | Mueve/enlaza a destino final |
| Retrieve | ¿Qué es relevante? | **Nadie** (solo índices) |
| Memorize | ¿Qué debe persistir? | `memory/` canónico |
| Act | ¿Qué hago fuera? | Evidencia en conversation/decision |
| Notify | ¿Qué cambió el estado? | `memory/projects/`, Home |

---

## Matriz de ownership (anti-colisión)

Cada capacidad tiene **un owner primario**. Los demás son fallback o índice.

### A. Documentos (PDF/Office/HTML)

| Situación | Owner | Fallback |
|-----------|-------|----------|
| Digital limpio, rápido | **MarkItDown** | — |
| Tablas, layout, papers | **Docling** | MarkItDown |
| Escaneado / OCR duro | **Marker/Surya** | Docling |
| Router automático | **parse-anything** | elige según MIME |

**Regla:** una conversión por archivo. Si Docling gana, MarkItDown no reescribe. Timestamp + `converter:` en frontmatter.

### B. Web

| Situación | Owner |
|-----------|-------|
| Página → MD | **Crawl4AI** |
| Ya es URL de archivo/doc | MarkItDown/Docling |
| Meta-search (opcional) | SearXNG (no escribe vault) |

### C. Media (audio/video)

| Paso | Owner | Salida |
|------|-------|--------|
| Bajar / extraer | **yt-dlp** | `memory/inbox/media/` (o solo audio) |
| Transcribir | **faster-whisper** | `memory/inbox/converted/*.md` |
| Resumir | Agente (+ Ollama opcional) | nota en `memory/conversations/` o proyecto |

**Regla:** yt-dlp no “entiende”; Whisper no “organiza”; el agente Orient/Memorize sí.

### D. Código / repos

| Necesidad | Owner | No hacer |
|-----------|-------|----------|
| Mapa del repo (AST, onboarding) | **Graphify** | Duplicar el mismo grafo con otra tool |
| Query en vivo vía MCP en el IDE | **Nexus-MCP** (si instalado) | Tratar Nexus como segunda verdad |
| Skill discovery | Grafo `skills/` del vault | Re-escanear origen en cada pregunta |

**Regla:** Graphify escribe artefactos bajo `memory/graphs/<proyecto>/`. Nexus/engraph **leen/indexan**, no inventan otra carpeta de verdad.

### E. Recuperación del vault

| Necesidad | Owner |
|-----------|-------|
| Buscar en notas del cerebro | **engraph** (preferido) o korely-graphrag |
| Leer/escribir nota puntual | **obsidian-mcp** |
| Memoria episódica extra (opcional) | PMB / Knowledge Keeper — **espejo**, no canónico |

**Regla de oro:** si PMB y el vault discrepan → **gana el vault**. PMB se reconcilia o se ignora.

---

## Contrato del piloto (cualquier agente)

Al “ponerse el traje”, el agente obedece este orden:

### Boot (cada sesión / máquina nueva)
1. `python bootstrap.py` si faltan tools  
2. Leer [[Home]] + este marco + [[agent-protocol]]  
3. Identificar proyecto activo en [[active-projects]]  
4. Si eres piloto con arsenal propio (Hermes / Claude Code / Cursor): cargar tu **adaptador** en [[pilots]]

### Loop de trabajo
1. **Retrieve** antes de reinventar (engraph / search vault / graphs / tools nativas de búsqueda)  
2. **Ingest→Normalize** solo si el material no está en el vault (usa tools nativas *o* CLI del traje)  
3. **Orient** (nunca dejar basura eterna en inbox > 7 días)  
4. **Act** con citas a notas `[[...]]` (aquí brillan terminal/browser/edit nativos)  
5. **Memorize + Notify** al cerrar trabajo útil  

### Prohibiciones
- No crear una segunda base de notas fuera de Talaria  
- No guardar secretos  
- No ejecutar dos converters sobre el mismo archivo sin `force: true` y nota de por qué  
- No usar índices (engraph/nexus) ni memoria del agente (mem0, session) como sustituto de escribir decisiones  
- No “apagar” tools nativas del piloto: **reclasificarlas** en una capa SPINE  

---

## Pilotos con arsenal integrado (Hermes, Claude Code, Cursor…)

Muchos agentes **ya** traen tools. SPINE no las reemplaza: las **mapea**.

### Modelo mental

```
┌─────────────────────────────────────────────┐
│  PILOTO (Hermes / Claude Code / Cursor…)    │
│  tools nativas = manos, ojos, reflejos      │
└──────────────────┬──────────────────────────┘
                   │ se pone
                   ▼
┌─────────────────────────────────────────────┐
│  ORGANISMO Talaria (SPINE)              │
│  vault MD = verdad · staging · graphs       │
│  MarkItDown/Graphify/… = sistemas del traje │
└─────────────────────────────────────────────┘
```

| Memoria del piloto | Rol SPINE | ¿Canónica? |
|--------------------|-------------|------------|
| Chat / sesión | Efímera | No |
| mem0 / session store / JSONL agente | Retrieve corto / caché | No |
| Talaria `memory/` | Memorize | **Sí** |
| MCP / índices | Retrieve | No (no escriben verdad nueva) |

### Adaptadores oficiales

| Piloto | Doc | Archivo de arranque |
|--------|------|---------------------|
| Todos | [[pilots]] | — |
| Hermes | [[hermes-adapter]] | MCP `obsidian` + leer Home |
| Claude Code | [[claude-adapter]] | `CLAUDE.md` en la raíz del vault |
| Cursor | [[cursor-adapter]] | `AGENTS.md` |

### Regla de convivencia

1. **Act** con lo nativo (browser Hermes, bash Claude, edit Cursor).  
2. **Memorize** siempre en el vault (MCP obsidian o Write al path).  
3. Si el nativo ya hizo Ingest (Firecrawl, WebFetch): igual **Normalize** a `memory/inbox/converted/` y Orient.  
4. Subagentes / delegation heredan el mismo adaptador.  

### Frase portátil (cualquier sistema prompt)

> Talaria + SPINE es tu segundo cerebro canónico. Tus tools integradas son sensores y actuadores. La memoria interna del agente es caché. Decisiones, preferencias y resúmenes útiles se escriben en el vault.

---

## Estándar de artefacto (Normalize)

Todo lo que entra al vault cumple:

```yaml
---
date: YYYY-MM-DD
type: converted-document | transcript | web-capture | project-graph | conversation | ...
source: "<origen>"
converter: markitdown|docling|crawl4ai|whisper|graphify|...
pipeline: spine
layer: ingest|normalize|orient|memorize
tags: [...]
---
```

Carpetas de staging (escritura de Ingest/Normalize):

| Ruta | Contenido |
|------|-----------|
| `memory/inbox/docs/` | Binarios originales (opcional) |
| `memory/inbox/converted/` | MD normalizado |
| `memory/inbox/media/` | Audio/video staging |
| `memory/inbox/` | Capturas sin clasificar |
| `memory/graphs/<proyecto>/` | Salidas Graphify |

Destino canónico tras Orient:

| Tipo | Destino |
|------|---------|
| Conversación útil | `memory/conversations/` |
| Decisión | `memory/decisions/` |
| Aprendizaje | `memory/learnings/` |
| Estado de proyecto | `memory/projects/` |
| Skill index | `skills/` (solo vía build script) |

---

## Bus de eventos (cómo “hablan” las tools)

No hace falta un message broker. El bus es el **filesystem + frontmatter**:

1. Tool A deja un `.md` en staging con `pipeline: spine`  
2. Agente Orient lee staging, mueve/enlaza, pone `layer: memorize`  
3. Retrieve reindexa (engraph watch / rebuild)  
4. Siguiente agente solo consulta índices + canónico  

Idempotencia: mismo `source` + mismo `converter` el mismo día → **actualizar** nota, no duplicar (`agent-protocol`).

---

## Routing rápido (decision tree)

```
¿Es un repo/código?
  SÍ → Graphify (mapa) + opcional Nexus-MCP (query)
¿Es audio/video/URL de media?
  SÍ → yt-dlp → whisper → MD → Orient
¿Es URL web (artículo/docs online)?
  SÍ → Crawl4AI → MD → Orient
¿Es PDF/Office?
  ¿tablas/paper/scan? Docling/Marker : MarkItDown → Orient
¿Es pregunta sobre lo ya sabido?
  SÍ → engraph/obsidian-mcp (NO re-ingestar)
¿Es decisión/preferencia nueva?
  SÍ → Memorize (templates) → Notify proyecto
```

---

## Niveles del organismo (Mark I → Lxxx)

| Mark | Capacidad | Tools mínimas |
|------|-----------|---------------|
| **Mk.1** | Cerebro usable | vault + obsidian-mcp + agent-protocol |
| **Mk.2** | Ingest docs/código | + MarkItDown + Graphify + bootstrap |
| **Mk.3** | Ingest multimodal | + Docling + Crawl4AI + yt-dlp + Whisper |
| **Mk.4** | Super-retrieval | + engraph (o korely) + Nexus-MCP |
| **Mk.5** | Autonomía local | + Ollama + (PMB espejo opcional) |

El agente declara en qué Mark opera. No inventa tools del Mark superior si no están instaladas: ejecuta `bootstrap.py` o degrada con honestidad.

---

## SLAs entre sistemas

| Conflicto | Resolución |
|-----------|------------|
| Dos MD del mismo PDF | Queda el de mayor `converter_rank` (Marker>Docling>MarkItDown) o el marcado `canonical: true` |
| Grafo Graphify vs Nexus | Vault `memory/graphs/` es el snapshot versionable; Nexus es runtime |
| PMB vs vault | Vault gana |
| Chat vs vault | Vault gana (el chat es efímero) |
| Skill origen vs nota skill | La nota en `skills/` es el índice; origen SKILL.md no se edita |

`converter_rank`: `marker=30`, `docling=20`, `markitdown=10`.

---

## Checklist “¿el traje está bien calibrado?”

- [ ] Una sola carpeta vault es la verdad  
- [ ] Staging ≠ canónico  
- [ ] Índices no escriben conocimiento nuevo  
- [ ] Cada tool tiene ownership en la matriz  
- [ ] Bootstrap instala el Mark declarado  
- [ ] AGENTS.md apunta a este marco  
- [ ] Tras Act siempre hay Memorize o razón explícita de no hacerlo  

---

## FORGE — órgano de perfiles (no otro producto)

**FORGE** = *Framework for Operational Role Generation & Excellence*.

Es un **órgano** del organismo [[organism|Talaria]]: fabrica/aloja perfiles operativos. Comparte el mismo vault que memoria, [[axon|AXON]], CLI y tools.

| Pieza | Nota |
|-------|------|
| Mapa del cuerpo | [[organism]] |
| Hub | [[forge]] |
| Leyes | [[forge-two-laws]] |
| Builder | [[forge-builder]] |
| Catálogo | [[forge-catalog]] |
| Ensembles | [[forge-ensembles]] |

**Orient:** elegir `forge_profile` / `forge_ensemble`. **Act:** playbook del perfil. **Memorize:** entregables canónicos en el vault.

---

## Referencias

- Protocolo escritura: [[agent-protocol]]  
- Portabilidad: [[PORTABILITY]]  
- Tools: [[tools-index]] · investigación: [[2026-07-28-herramientas-gratis-talaria]]  
- MCP: [[mcp-obsidian]]  
- Perfiles: [[forge]]  
- Home: [[Home]]
