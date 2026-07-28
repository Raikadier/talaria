---
tags: [tool, cli, skillgraph]
aliases: [skillgraph-cli, cli]
---

# CLI `skillgraph`

Cinturón SPINE + **conector para agentes** + **gates de garantía** (verify/smoke).  
Diseño: [[cli-design]] · Arquitectura: [[cli-architecture]] · Conexión: [[agent-connect]] · Garantías: [[2026-07-28-garantias-skillgraph]]

**Versión:** 0.5.0

## Instalar

```bash
cd "<vault SkillGraph>"
pip install -e .
```

Sin instalar: `python -m skillgraph_cli …` o `.\skillgraph.cmd …`

## Para agentes (lo importante)

```bash
skillgraph describe --json
skillgraph verify boot --json
skillgraph axon search "refactor testing" --json
skillgraph axon for-profile researcher --json
skillgraph forge list --json
skillgraph forge run researcher --with-axon --json
skillgraph connect --client generic --json
skillgraph mcp
skillgraph smoke --json
# al cerrar trabajo útil:
skillgraph forge check --profile <id> --deliverable <path> --json
skillgraph verify close --scorecard <path-al-scorecard.md> --json
```

Scorecard: `_templates/scorecard.md` · Deliverable FORGE: `_templates/forge-deliverable.md`

Tools MCP: `skillgraph_describe`, `skillgraph_doctor`, `skillgraph_boot`, `skillgraph_status`, `skillgraph_vault_path`, `skillgraph_verify_boot`, `skillgraph_verify_close`, `skillgraph_smoke`, `skillgraph_forge_list`, `skillgraph_forge_show`, `skillgraph_forge_check`, `skillgraph_forge_run`, `skillgraph_ingest_doc`, `skillgraph_ingest_project`, `skillgraph_import_chats`

## Comandos humanos

```bash
skillgraph doctor          # tools + organismo
skillgraph status
skillgraph verify boot
skillgraph smoke
skillgraph ingest doc .\archivo.pdf
skillgraph ingest project "D:\Github repos\mi-repo"
skillgraph import chats
```

## Env

`SKILLGRAPH_VAULT` — override del path del vault
