---
tags: [meta, cli, design, ironman]
aliases: [cli-design, diseño-cli]
version: 1.0
status: active
---

# Diseño — CLI `skillgraph`

## Objetivo

Una **CLI fina** que orquesta el traje IRONMAN sin reemplazar el vault.  
El cerebro sigue siendo Markdown en SkillGraph; la CLI es el cinturón de herramientas del piloto.

## No-objetivos

- No UI gráfica
- No base de datos propia
- No daemon permanente (Mk.5 futuro opcional)
- No duplicar memoria fuera del vault

## Usuarios

| Quién | Cómo |
|-------|------|
| Agente (Cursor/Hermes/Claude) | `skillgraph boot` / `ingest` / `status` |
| David en terminal | mismos comandos |
| CI / scripts | exit codes estables (0 ok, 1 error deps, 2 uso) |

## Principios de UX

1. **Un binario:** `skillgraph`  
2. **Vault auto-descubierto:** cwd → padres buscando `AGENTS.md`+`Home.md`, o `$SKILLGRAPH_VAULT`, o instalación relativa al paquete  
3. **Comandos = capas IRONMAN** (nombres alineados al marco)  
4. **Json opcional:** `--json` para agentes  
5. **Cero deps extra** en v1 (stdlib `argparse`)

## Superficie de comandos (v1)

| Comando | Capa IRONMAN | Hace |
|---------|--------------|------|
| `skillgraph boot` | Boot | Instala/verifica tools (`bootstrap.py`) |
| `skillgraph doctor` | Boot | Solo check (`--check-only`) |
| `skillgraph status` | Notify | Mark, tools, path vault, reglas |
| `skillgraph ingest doc <src>` | Ingest+Normalize | MarkItDown → inbox/converted |
| `skillgraph ingest project <path>` | Ingest+Normalize | Graphify → memory/graphs |
| `skillgraph import chats` | Ingest+Memorize | Hermes/Claude/Cursor → memory/conversations |
| `skillgraph vault` | — | Imprime path absoluto del vault |
| `skillgraph help` | — | Ayuda / mapa IRONMAN corto |

## Flags globales

```
skillgraph [--vault PATH] [--json] <command> ...
```

## Ejemplos

```bash
skillgraph doctor
skillgraph boot
skillgraph ingest doc .\informe.pdf
skillgraph ingest project "D:\Github repos\captus-web"
skillgraph import chats
skillgraph status --json
```

## Criterios de éxito

- Agente nuevo: un solo comando `skillgraph boot` deja Mk.2 listo  
- Ingest no inventa schemas: reutiliza helpers existentes  
- Portable: funciona tras `git clone` + `pip install -e .`  

## Fuera de v1 (backlog)

- `skillgraph ingest url` (Crawl4AI)  
- `skillgraph ingest media` (yt-dlp+whisper)  
- `skillgraph search` (engraph)  
- Plugins / Mark levels automáticos  

→ Arquitectura: [[cli-architecture]]
