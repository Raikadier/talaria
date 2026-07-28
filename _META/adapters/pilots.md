---
tags: [moc, pilots, spine, adapters]
aliases: [pilotos, adapters]
---

# Pilotos del organismo SPINE

Cualquier IA con agente y tools propias puede “ponerse” SkillGraph.  
El traje es el mismo; cambia el **adaptador** del piloto.

| Piloto | Adaptador | Tools nativas |
|--------|-----------|---------------|
| Hermes | [[hermes-adapter]] | browser, web, mem0, file, terminal, skills, MCP… |
| Claude Code | [[claude-adapter]] | bash, edit, agent, MCP, skills… |
| Cursor | [[cursor-adapter]] | edit, terminal, MCP, subagentes… |
| Otro (Codex, Copilot, Windsurf…) | Mismo contrato | Mapear sus tools → capas SPINE |

## Regla universal para pilotos “ya armados”

1. **No desactives** el arsenal nativo.  
2. **Clasifícalo** en una capa SPINE (Ingest/Act/Retrieve…).  
3. **Canónico** = vault SkillGraph. Memoria del agente (mem0, session, JSONL) = caché.  
4. **Al cerrar** trabajo útil → Memorize + Notify en el vault.  
5. Si el piloto tiene MCP: conecta `obsidian` al path del vault.

## Constitución

[[spine-framework]] · [[agent-protocol]] · [[AGENTS]] · `CLAUDE.md`
