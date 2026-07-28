# AGENTS.md — SkillGraph (piloto SPINE)

Eres un agente trabajando sobre el vault **SkillGraph**.  
Este vault es el **organismo**: multiplica capacidad si respetas SPINE y los órganos. Si improvisas otra memoria, el cuerpo se pelea consigo mismo.

Sirve igual si ya traes tools propias (**Hermes**, **Claude Code**, **Cursor**, etc.): no las apagues; síguelas el mapa del adaptador.

## Constitución (léela)
1. [[organism]] — SkillGraph es un solo cuerpo (órganos, no productos sueltos)  
2. [[architecture]] — estructura del proyecto + superficie API  
3. [[spine-framework]] — SPINE: capas, ownership, pilotos (alias legado: IRONMAN)  
4. [[axon]] — AXON: skills interconectadas  
5. [[pilots]] — adaptadores Hermes / Claude Code / Cursor  
6. [[agent-protocol]] — qué escribir y dónde  
7. [[Home]] — mapa de entrada  
8. [[forge]] — FORGE: órgano de perfiles (builder + catálogo + 2 leyes)  
9. Si eres Claude Code: también `CLAUDE.md`

## FORGE (perfiles)
Si la tarea pide especialización elite (research, growth, arquitectura, etc.):
1. `skillgraph forge list --json` / `forge show <id>`  
2. `skillgraph forge run <id> --json` — activar packet  
3. Ejecutar playbook; entregable con `forge_gates` (plantilla `_templates/forge-deliverable.md`)  
4. `skillgraph forge check --profile <id> --deliverable <path> --json`  
5. No cerrar sin gates en pass + `verify close`

## Primera visita (máquina nueva o clone)

```bash
pip install -e .
skillgraph boot
# o: python bootstrap.py
```

Declara el Mark (Mk.1–Mk.5). Carga tu adaptador ([[hermes-adapter]] / [[claude-adapter]] / [[cursor-adapter]]).

## CLI del traje + conexión agentes

```bash
skillgraph describe --json    # descubrimiento (cualquier agente)
skillgraph connect --client cursor|hermes|claude --json
skillgraph axon search "<query>" [--domain X] [--tag Y] --json
skillgraph axon for-profile <id> --json
skillgraph forge list [--ensembles] --json
skillgraph forge show <id> --json
skillgraph forge run <id> --json
skillgraph forge check --profile <id> [--deliverable PATH] [--declare G1=pass,...] --json
skillgraph verify boot --json
skillgraph verify close --scorecard <path> --json
skillgraph doctor --json
skillgraph smoke --json
skillgraph mcp                # MCP stdio
skillgraph status
skillgraph ingest doc <archivo>
skillgraph ingest project <ruta>
skillgraph import chats
```

Docs: [[cli]] · [[agent-connect]] · [[cli-design]] · [[cli-architecture]]

## Orden de combate (cada tarea)

0. **Verify boot** — `skillgraph verify boot --json` (gate de entrada)  
1. **Retrieve** — ¿ya está en el vault / AXON / graphs?  
2. **Ingest → Normalize** — material nuevo → staging  
3. **Orient** — clasificar a destino canónico  
4. **Act** — arsenal nativo con citas `[[wiki links]]`  
5. **Memorize + scorecard** — copiar `_templates/scorecard.md`, llenar  
6. **Verify close** — `skillgraph verify close --scorecard <path> --json`  
7. **Notify** — proyecto / Home si aplica  

Garantías: [[2026-07-28-garantias-skillgraph]] · `skillgraph smoke --json`

## Routing rápido

| Entrada | Tool owner |
|---------|------------|
| PDF/Office limpio | MarkItDown |
| PDF difícil / tablas | Docling (si instalado) |
| Web | Crawl4AI / Firecrawl / WebFetch → igual Normalizar al vault |
| Video/audio | yt-dlp → Whisper |
| Repo | Graphify → `memory/graphs/` |
| Pregunta al cerebro / skills | AXON + engraph / obsidian-mcp |
| Decisión/preferencia | templates en `memory/` |

## Prohibiciones
- No crear una segunda base de verdad fuera de este vault  
- No tratar mem0 / session memory / chat como canónicos  
- No guardar secretos  
- No dejar que índices contradigan al vault (el vault gana)  

## Idioma
Español (salvo código y nombres propios).
