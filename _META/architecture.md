---
tags: [meta, architecture, skillgraph, organism, api]
aliases: [arquitectura-skillgraph, project-structure, estructura-skillgraph]
version: 1.0
status: active
---

# SkillGraph — estructura del proyecto (organismo + API)

**Proyecto único:** SkillGraph  
**Metáfora interna:** organismo (órganos con funciones vitales)  
**Metáfora externa:** **API de capacidades** para cualquier agente  

Mapa vivo de órganos: [[organism]] · Protocolo: [[spine-framework]] · Conexión: [[agent-connect]]

---

## Opinión de diseño (posición oficial)

SkillGraph **sí** es una super-API que un agente usa para maximizar capacidad — pero **no solo** una caja de tools.

| Si solo fuera… | Faltaría… |
|----------------|-----------|
| API de tools | Memoria durable, roles, grafo de skills |
| Segundo cerebro pasivo | Contrato de ejecución (SPINE) + superficie máquina |
| Prompt framework | Estado compartido entre pilotos |

**Definición corta:**

> SkillGraph = **sustrato cognitivo + estado canónico + protocolo SPINE**, expuesto como **API (CLI/MCP)** para que cualquier piloto multiplique capacidad sin inventar otro cerebro.

- **Hacia fuera:** API (descubrir → conectar → operar → persistir).  
- **Hacia dentro:** organismo (órganos que no se pisan).  
- **Riesgo a evitar:** tratarlo como “mega-toolkit” y saltarse Memorize. Sin persistir en el vault, la API no acumula poder entre sesiones.

---

## Capas del sistema (de fuera hacia adentro)

```
┌─────────────────────────────────────────────────────────────┐
│ 0. PILOTOS          Cursor · Hermes · Claude · futuros      │
│    (clientes de la API; no son el cuerpo)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ describe / connect / MCP / CLI
┌───────────────────────────▼─────────────────────────────────┐
│ 1. SUPERFICIE API     skillgraph CLI + MCP + contract JSON  │
│    Órgano: interfaz     [[cli]] · [[agent-connect]]         │
└───────────────────────────┬─────────────────────────────────┘
                            │ obedece
┌───────────────────────────▼─────────────────────────────────┐
│ 2. SPINE              7 capas · ownership · Marks           │
│    Órgano: nervioso     [[spine-framework]]                 │
└───────────────────────────┬─────────────────────────────────┘
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐
│ 3a. MEMORIA     │ │ 3b. AXON     │ │ 3c. FORGE       │
│ episodios       │ │ skills graph │ │ perfiles / roles│
│ memory/         │ │ skills/      │ │ _META/forge/    │
└────────┬────────┘ └──────┬───────┘ └────────┬────────┘
         └─────────────────┼──────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. TEJIDO             Markdown + YAML en el vault           │
│    (única verdad)     OneDrive / Obsidian                   │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌───────────────────────────┴─────────────────────────────────┐
│ 5. MÚSCULOS / TOOLS   MarkItDown · Graphify · …             │
│    Efectores SPINE    tools/ · bootstrap · _tools/          │
└─────────────────────────────────────────────────────────────┘
```

Los **adaptadores** (`_META/adapters/`) no son un órgano de datos: son **traductores** piloto → SPINE.

---

## Estructura de carpetas (layout canónico)

```
SkillGraph/                          ← raíz del organismo (= proyecto)
│
├── Home.md                          ← puerta humana / agente
├── AGENTS.md · CLAUDE.md            ← constitución por piloto
├── SPINE-STATUS-CURSOR.md           ← notify de estado
├── PORTABILITY.md · README.md
├── bootstrap.py · build_skillgraph.py
├── pyproject.toml · skillgraph.cmd
│
├── memory/                          ← ÓRGANO: Memoria
│   ├── conversations/ decisions/ projects/ learnings/
│   ├── research/ context/ graphs/ inbox/ archives/
│   └── active-projects.md · memory-index.md
│
├── skills/                          ← ÓRGANO: AXON (datos)
│   └── <dominio>/…                  ← notas skill + wiki-links
│
├── _META/                           ← constitución + índices
│   ├── organism.md                  ← mapa de órganos
│   ├── architecture.md              ← ESTE archivo
│   ├── spine-framework.md           ← ÓRGANO: SPINE
│   ├── axon.md                      ← hub AXON
│   ├── forge/                       ← ÓRGANO: FORGE
│   ├── adapters/                    ← traductores piloto
│   ├── domains/ · axes/ · taxonomy.md
│   ├── agent-protocol.md · agent-connect.md
│   └── cli-*.md · mcp-obsidian.md
│
├── skillgraph_cli/                  ← ÓRGANO: superficie API (código)
│   ├── cli.py · mcp_server.py · agent_contract.py
│   └── cmds/
│
├── tools/                           ← ÓRGANO: Tools (manifest, connect)
├── _tools/                          ← scripts de ingest/import
├── _templates/                      ← moldes de notas / perfiles
├── .cursor/rules/                   ← regla local SPINE
└── .obsidian/                       ← UI del tejido (opcional)
```

**Regla:** si algo es “verdad durable”, vive en Markdown bajo esta raíz. El código CLI solo **orquesta**.

---

## Órganos actuales (registro)

| ID | Nombre uso | Función | Contrato de crecimiento |
|----|------------|---------|-------------------------|
| `memory` | Memoria | Estado episódico y decisiones | Carpetas tipadas + [[agent-protocol]] |
| `axon` | AXON | Capacidades enlazadas | Solo vía `build_skillgraph.py` / taxonomía |
| `forge` | FORGE | Roles elite | Solo vía [[forge-builder]] + Leyes I/II |
| `spine` | SPINE | Protocolo / ownership | Cambios = decisión en `memory/decisions/` |
| `api` | CLI/MCP | Superficie máquina | `describe --json` estable; bump version |
| `tools` | Tools | Efectores ingest/act | `tools/manifest.json` + bootstrap Mark |
| `adapters` | Adaptadores | Mapa piloto→SPINE | Un `.md` por piloto |

---

## Cómo añadir un órgano nuevo (futuro)

1. **Función vital** — una frase; si solapa con otro órgano, no se crea.  
2. **Nombre** — técnico + acrónimo de uso (estilo FORGE / SPINE / AXON).  
3. **Home en vault** — carpeta o hub `_META/<organ>/`.  
4. **Registro** — fila en [[organism]] + aquí + decisión en `memory/decisions/`.  
5. **SPINE** — mapear a capas (qué escribe, qué solo lee).  
6. **API** — si el agente debe invocarlo: comando CLI y/o tool MCP + entrada en `describe --json`.  
7. **No** segunda base de verdad fuera del vault.

Plantilla mínima de hub:

```markdown
# <ACRONIMO> — <Nombre técnico>
Órgano de SkillGraph. Función: …
Dónde: …
SPINE: capas …
API: (ninguna | skillgraph <cmd> | MCP tool)
Hermanos: …
```

---

## Contrato de la “super API” (lo que todo agente debe ver)

```
1. describe --json     → descubrir el cuerpo
2. connect --client X  → cablear MCP/CLI
3. doctor | boot       → Mark operativo
4. status              → salud
5. Operate vía SPINE   → Retrieve / Ingest / Act / Memorize…
6. Órganos bajo demanda→ AXON · FORGE · Memoria · Tools
```

La API **no reemplaza** al piloto: le da estado compartido, skills, roles y un protocolo para no degradar a chat efímero.

---

## Anti-patrones

| Anti-patrón | Por qué duele |
|-------------|----------------|
| “SkillGraph es solo MCP tools” | Se pierde Memoria/FORGE/AXON |
| Nuevo órgano con su propia DB | Rompe una verdad |
| FORGE sin gates | Deja de ser FORGE |
| Regenerar AXON a mano archivo a archivo | Inconsistencia masiva |
| CLI con estado propio | Duplica el vault |

## Hardening (garantías)

Plan para que funcionamiento y resultados no dependan solo de disciplina del piloto: [[2026-07-28-garantias-skillgraph]]

---

## Referencias

- [[organism]] · [[Home]] · [[spine-framework]] · [[axon]] · [[forge]]  
- [[cli]] · [[cli-architecture]] · [[agent-connect]] · [[SkillGraph]]
