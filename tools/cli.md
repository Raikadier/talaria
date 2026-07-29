---
tags: [tool, cli, talaria]
aliases: [talaria, cli]
---

# CLI `talaria`

Cinturón SPINE + **conector para agentes** + **gates de garantía** (verify/smoke).  
Diseño: [[cli-design]] · Arquitectura: [[cli-architecture]] · Conexión: [[agent-connect]] · Garantías: [[2026-07-28-garantias-talaria]]

**Versión:** 0.5.0

## Instalar

```bash
cd "<vault Talaria>"
pip install -e .
```

Sin instalar: `talaria …` o `.\talaria.cmd …`

## Para agentes (lo importante)

```bash
talaria describe --json
talaria verify boot --json
talaria axon search "refactor testing" --json
talaria axon for-profile researcher --json
talaria forge list --json
talaria forge run researcher --with-axon --json
talaria connect --client generic --json
talaria mcp
talaria smoke --json
# al cerrar trabajo útil:
talaria forge check --profile <id> --deliverable <path> --json
talaria verify close --scorecard <path-al-scorecard.md> --json
```

Scorecard: `_templates/scorecard.md` · Deliverable FORGE: `_templates/forge-deliverable.md`

Tools MCP: `talaria_describe`, `talaria_doctor`, `talaria_boot`, `talaria_status`, `talaria_vault_path`, `talaria_verify_boot`, `talaria_verify_close`, `talaria_smoke`, `talaria_forge_list`, `talaria_forge_show`, `talaria_forge_check`, `talaria_forge_run`, `talaria_ingest_doc`, `talaria_ingest_project`, `talaria_import_chats`

## Comandos humanos

```bash
talaria doctor          # tools + organismo
talaria status
talaria verify boot
talaria smoke
talaria ingest doc .\archivo.pdf
talaria ingest project "D:\Github repos\mi-repo"
talaria import chats
```

## Env

`TALARIA_VAULT` — override del path del vault
