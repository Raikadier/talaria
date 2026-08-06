---
tags: [meta, forge, delegation, graph, user-owned]
aliases: [forge-delegation, grafo-agentes, subagentes-forge]
version: 1.0
status: active
---

# FORGE Delegation — grafo de agentes **del usuario**

Talaria es la **fábrica** (`forge build`). El organigrama lo crea **el usuario**.  
No hay árbol canónico “software developer → …” en el producto: eso sería contenido ajeno.

## Principios

1. **User-owned** — cada perfil en `_META/forge/profiles/` es del dueño del vault.  
2. **Grafo, no RR.HH.** — edges `invokes` / `invocable_by` (many-to-many).  
3. **Default abierto** — `invocable_by_mode: open`. El dueño siempre puede `forge run <id>`.  
4. **Policy opcional** — `allowlist` / `deny_direct` solo para *delegación automática* (`forge invoke`).  
5. **Mismo builder** — orquestadores y especialistas se fabrican igual (Builder 2.0 + corpus).

## Frontmatter

```yaml
role_kind: both          # orchestrator | specialist | both
invocable_by_mode: open  # open | allowlist | deny_direct
invocable_by: []         # callers preferidos / allowlist
invokes: []              # a quién puede delegar este perfil
```

## CLI / MCP

```bash
talaria forge build --brief "…" --kind orchestrator --invokes code-reviewer,qa-tester --json
talaria forge build --brief "…" --kind specialist --invocable-by my-orchestrator --invocable-by-mode allowlist --json
talaria forge graph --json
talaria forge invoke <parent> <child> --brief "…" [--strict] --json
talaria forge list --graph --json
```

MCP: `talaria_forge_build` · `talaria_forge_invoke` · `talaria_forge_graph`

## Relación con ensembles

[[forge-ensembles]] = pipeline secuencial con handoff por artefacto (ej. `software-triad` **ejemplo**).  
Delegation graph = quién *puede* llamar a quién en runtime del piloto. Pueden coexistir.

## Ejemplo tutorial

Ver [[forge-example-user-graph]] — *sample*, no catálogo elite.

## Anti-patrones

- Precocinar 40 roles de industria en el repo como “el” modelo  
- ACL duro que impida al dueño `forge run`  
- Hijos sin corpus C1–C5 (cosplay)  
- Creer que más edges = más calidad sin evals  

Schema: [[forge-schema]] · Builder: [[forge-builder]] · Hub: [[forge]]
