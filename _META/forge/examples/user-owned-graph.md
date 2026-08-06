---
tags: [meta, forge, example, tutorial]
aliases: [forge-example-user-graph]
status: example
---

# Ejemplo (no canon) — grafo que **tú** podrías crear

Esto **no** es el organigrama de Talaria. Es un tutorial de composición.

```bash
# 1) Orquestador tuyo
talaria forge build --brief "orquestador de entrega de software" \
  --id my-sw-orchestrator --kind orchestrator \
  --invokes my-code-reviewer,my-qa-tester --json

# 2) Especialistas (multi-padre posible)
talaria forge build --brief "code reviewer estricto" \
  --id my-code-reviewer --kind specialist \
  --invocable-by my-sw-orchestrator,my-poster-designer \
  --invocable-by-mode allowlist --json

talaria forge build --brief "qa tester" \
  --id my-qa-tester --kind specialist \
  --invocable-by my-sw-orchestrator --json

# 3) Ver grafo y delegar
talaria forge graph --json
talaria forge invoke my-sw-orchestrator my-code-reviewer --brief "revisar PR X" --json
```

Completa corpus C1–C5 antes de `status: active`.  
Doc: [[forge-delegation]]
