---
tags: [meta, adapter, hermes, spine]
aliases: [hermes-adapter, piloto-hermes]
---

# Adaptador SPINE → Hermes

Hermes ya trae **toolsets integrados** (browser, web, file, memory/mem0, terminal, skills, MCP…).  
SPINE no los apaga: los **encauza** para que el vault Talaria sea la armadura compartida.

## Mapa toolset Hermes → capas SPINE

| Toolset Hermes | Capa SPINE | Rol |
|----------------|--------------|-----|
| `web` / Firecrawl | Ingest | Traer páginas; **Normalize** a MD en `memory/inbox/converted/` |
| `browser` | Ingest / Act | Explorar UI; no sustituye Memorize |
| `file` / `terminal` | Act + Normalize | Editar repos; al cerrar, resumen → vault |
| `memory` (mem0) | Retrieve **corto plazo** | Espejo/caché. **Canónico = vault** |
| `session_search` | Retrieve | Buscar chats Hermes; si es durable → exportar a `memory/conversations/` |
| `skills` | Retrieve / Act | Skills locales; el catálogo portable vive en `skills/` del vault |
| MCP `obsidian` | Retrieve + Memorize | Leer/escribir Talaria |
| MCP `youtube` | Ingest | Metadata/subs → Normalize |
| `tts` / `stt` / `vision` | Ingest / Act | Multimodal; transcripciones → vault |
| `kanban` / `todo` / `cronjob` | Act / Notify | Operación; estado de proyecto también en `memory/projects/` |
| `delegation` | Act | Subagentes deben heredar este adaptador |

## Reglas Hermes-específicas

1. **mem0 no gana al vault.** Si mem0 y Talaria discrepan → corregir vault y, si aplica, actualizar mem0.  
2. Tras trabajo útil en CLI/WhatsApp: escribir nota vía MCP `obsidian` o archivo directo al path del vault.  
3. Firecrawl/browser = Ingest; no dejes el hallazgo solo en el chat.  
4. `SOUL.md` / `USER.md` de Hermes son contexto del piloto; preferencias duraderas también en `memory/learnings/`.  
5. MCP `obsidian` ya está en `config.yaml` → reiniciar gateway si no carga.

## Boot Hermes

```
1. ¿MCP obsidian activo? → sí
2. Leer Home + ironman-framework (search-vault / read-note)
3. Proyecto activo → memory/projects/
4. Operar toolsets nativos según mapa de arriba
5. Cerrar con Memorize + Notify
```

## Frase de sistema (pegar en sesión / SOUL addendum)

> Usas el vault Talaria como segundo cerebro canónico (marco SPINE). Tus tools nativas son sensores/actuadores. mem0 es caché. Toda decisión, preferencia y resumen útil se escribe en el vault vía MCP obsidian.

## Enlaces

- [[spine-framework]] · [[mcp-obsidian]] · [[agent-protocol]] · [[pilots]]
