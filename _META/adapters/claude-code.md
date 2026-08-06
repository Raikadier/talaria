---
tags: [meta, adapter, claude-code, spine]
aliases: [claude-adapter, piloto-claude]
---

# Adaptador SPINE → Claude Code

Claude Code ya trae agente con tools (bash, lectura/edición, grep, agentes, MCP, skills…).  
SPINE convierte ese piloto en uno con **armadura compartida** (Talaria), sin desactivar sus tools.

## Mapa Claude Code → capas SPINE

| Capacidad Claude Code | Capa SPINE | Rol |
|----------------------|--------------|-----|
| Bash / shell | Act + Ingest | Correr `bootstrap.py`, markitdown, graphify, yt-dlp… |
| Read / Edit / Write / Glob / Grep | Act + Retrieve | Sobre repos **y** sobre el vault si el cwd es Talaria |
| Agent / Task tool | Act | Subagentes: indicarles `CLAUDE.md` + SPINE |
| MCP servers | Retrieve / Memorize / Act | Añadir `obsidian` apuntando al vault |
| Skills / plugins | Act | Complementan; el catálogo portable está en `skills/` del vault |
| Plan mode | Orient | Plan → al cerrar, decisión en `memory/decisions/` |
| Compact / memoria de sesión | Retrieve corto | Efímero; durable → vault |

## Setup Claude Code (una vez)

1. Abre o añade el vault como directorio de trabajo, **o** referencia absoluta en MCP.  
2. Asegura MCP Obsidian en `~/.claude/settings.json` (o project `.mcp.json`):

```json
"obsidian": {
  "command": "npx",
  "args": [
    "-y",
    "obsidian-mcp",
    "D:\\OneDrive - unicesar.edu.co\\Business Ideas\\Talaria"
  ]
}
```

(En otra máquina: cambia la ruta; ver `tools/mcp-obsidian.template.json`.)

3. Al trabajar **dentro** del vault, Claude lee automáticamente `CLAUDE.md` (constitución del piloto).  
4. `python bootstrap.py` si faltan MarkItDown/Graphify/etc.

## Crear un agente con Talaria

Si el usuario pide crear un agente/perfil («usando talaria»):

```bash
talaria forge build --brief "crea un agente que sepa responder correos" --json
# o MCP: talaria_forge_build
```

Luego ejecuta el `pilot_playbook` del JSON (research del oficio → `forge check` → active → `forge run`).  
No dejes el “agente” solo como prompt de chat.

## Reglas Claude-específicas

1. No uses solo el transcript de sesión como memoria de proyecto.  
2. Si editas un repo externo, el **resumen/decisión** vive en Talaria (`memory/projects/` + conversation).  
3. Skills de `.claude` y skills del vault no compiten: vault = índice portable; `.claude` = runtime local.  
4. Subagentes: primera línea del prompt = “sigue CLAUDE.md / SPINE; vault canónico”.

## Boot Claude Code

```
1. Leer CLAUDE.md (si cwd = vault) o fetch Home vía MCP obsidian
2. bootstrap.py --check-only
3. Retrieve (MCP search / Grep en memory/)
4. Usar bash tools nativas para Ingest/Act
5. Memorize vía Write al vault o MCP obsidian
```

## Enlaces

- [[spine-framework]] · [[mcp-obsidian]] · `CLAUDE.md` · [[pilots]]
