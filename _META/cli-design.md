---
tags: [meta, cli, design, ironman]
aliases: [cli-design, diseño-cli]
version: 1.0
status: active
---

# Diseño — CLI `talaria`

## Objetivo

Una **CLI fina** que orquesta el traje IRONMAN sin reemplazar el vault.  
El cerebro sigue siendo Markdown en Talaria; la CLI es el cinturón de herramientas del piloto.

## No-objetivos

- No UI gráfica
- No base de datos propia
- No daemon permanente (Mk.5 futuro opcional)
- No duplicar memoria fuera del vault

## Usuarios

| Quién | Cómo |
|-------|------|
| Agente (Cursor/Hermes/Claude) | `talaria boot` / `ingest` / `status` |
| David en terminal | mismos comandos |
| CI / scripts | exit codes estables (0 ok, 1 error deps, 2 uso) |

## Principios de UX

1. **Un binario:** `talaria`  
2. **Vault auto-descubierto:** cwd → padres buscando `AGENTS.md`+`Home.md`, o `$TALARIA_VAULT`, o instalación relativa al paquete  
3. **Comandos = capas IRONMAN** (nombres alineados al marco)  
4. **Json opcional:** `--json` para agentes  
5. **Cero deps extra** en v1 (stdlib `argparse`)

## Superficie de comandos (v1)

| Comando | Capa IRONMAN | Hace |
|---------|--------------|------|
| `talaria boot` | Boot | Instala/verifica tools (`bootstrap.py`) |
| `talaria doctor` | Boot | Solo check (`--check-only`) |
| `talaria status` | Notify | Mark, tools, path vault, reglas |
| `talaria ingest doc <src>` | Ingest+Normalize | MarkItDown → inbox/converted |
| `talaria ingest project <path>` | Ingest+Normalize | Graphify → memory/graphs |
| `talaria import chats` | Ingest+Memorize | Hermes/Claude/Cursor → memory/conversations |
| `talaria vault` | — | Imprime path absoluto del vault |
| `talaria help` | — | Ayuda / mapa IRONMAN corto |

## Flags globales

```
talaria [--vault PATH] [--json] <command> ...
```

## Ejemplos

```bash
talaria doctor
talaria boot
talaria ingest doc .\informe.pdf
talaria ingest project "D:\Github repos\captus-web"
talaria import chats
talaria status --json
```

## Criterios de éxito

- Agente nuevo: un solo comando `talaria boot` deja Mk.2 listo  
- Ingest no inventa schemas: reutiliza helpers existentes  
- Portable: funciona tras `git clone` + `pip install -e .`  

## Fuera de v1 (backlog)

- `talaria ingest url` (Crawl4AI)  
- `talaria ingest media` (yt-dlp+whisper)  
- `talaria search` (engraph)  
- Plugins / Mark levels automáticos  

→ Arquitectura: [[cli-architecture]]
