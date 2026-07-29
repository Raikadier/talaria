---
tags: [meta, cli, architecture, ironman]
aliases: [cli-architecture, arquitectura-cli]
version: 1.0
status: active
---

# Arquitectura — CLI `talaria`

Diseño: [[cli-design]] · Marco: [[ironman-framework]]

## Vista lógica

```
┌─────────────────────────────────────────────┐
│  Piloto (humano / agente)                   │
│    talaria <cmd>                         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  talaria_cli (facade)                    │
│  · argparse · vault discovery · --json      │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┼───────────┬──────────────┐
       ▼           ▼           ▼              ▼
  bootstrap.py  ingest_*   import_chats   status/report
       │           │           │              │
       └───────────┴───────────┴──────────────┘
                   │
                   ▼
         Talaria VAULT (Markdown)
```

La CLI **no** posee estado propio. Estado = filesystem del vault + tools del sistema.

## Layout de código

```
Talaria/
  pyproject.toml              # entry point talaria
  talaria.cmd              # Windows helper
  bootstrap.py                # existente (invocado)
  _tools/
    ingest_document.py
    ingest_project.py
    import_agent_chats.py
  talaria_cli/
    __init__.py
    __main__.py               # talaria
    cli.py                    # router argparse
    vault.py                  # resolución de raíz
    util.py                   # run, json_out, exit codes
    cmds/
      boot.py
      doctor.py
      status.py
      ingest.py
      import_chats.py
      vault_cmd.py
```

## Resolución del vault

Orden:

1. `--vault PATH`
2. Env `TALARIA_VAULT`
3. Caminar desde `cwd` hacia arriba: existe `Home.md` ∧ `AGENTS.md` ∧ `bootstrap.py`
4. Paquete instalado: padre de `talaria_cli/` si cumple (3)
5. Error claro si no se encuentra

## Contratos de comandos

| Cmd | Input | Side effects | Exit |
|-----|-------|--------------|------|
| boot | `[--check-only]` implícito en doctor | pip/npm, dirs, `.talaria.local.json` | 0/1 |
| doctor | — | ninguno (solo lectura) | 0 si Mk.2 ok else 1 |
| status | `[--json]` | ninguno | 0 |
| ingest doc | `source`, `[-o]` | escribe `memory/inbox/converted/` | 0/1 |
| ingest project | `path`, `[--name]` | graphify + `memory/graphs/` | 0/1 |
| import chats | — | regenera imports en `memory/conversations/` | 0/1 |
| vault | — | print path | 0 |

## Integración con IRONMAN

| Comando | Capas |
|---------|-------|
| boot/doctor | Boot |
| ingest * | Ingest + Normalize (+ hint Orient) |
| import chats | Ingest + Memorize (histórico) |
| status | Notify / observabilidad |

El **Orient** canónico lo sigue haciendo el agente (mover de inbox a conversations/decisions); la CLI deja staging listo.

## Empaquetado

```toml
[project.scripts]
talaria = "talaria_cli.cli:main"
```

`pip install -e .` desde la raíz del vault.

## Extensión futura

Nuevos cmds = módulo en `cmds/` + registro en `cli.py`.  
Tools Mk.3+ se declaran en `tools/manifest.json`; `boot` las instala sin cambiar la fachada.

## Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| OneDrive locks | mismos patrones ignore_errors que import |
| Paths Windows con espacios | Path + comillas en subprocess |
| Agente en otro cwd | `--vault` / env / walk-up |
