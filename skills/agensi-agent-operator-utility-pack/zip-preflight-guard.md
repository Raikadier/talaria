---
name: zip-preflight-guard
domain: agensi-agent-operator-utility-pack
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-operator-utility-pack\\skills\\zip-preflight-guard\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-operator-utility-pack\\skills\\zip-preflight-guard\\SKILL.md"
  - "C:\\Users\\david\\Skills\\agensi-free\\agent-operator-utility-pack\\skills\\zip-preflight-guard\\SKILL.md"
tags: [security, agensi-agent-operator-utility-pack]
description: Wrapper skill that runs a bundled intake-guard security scan then a built-in release-readiness flightcheck on a zip archive or directory. Emits a unified GO/NO-GO verdict. Use when you want both bomb/traversal/secret detection AND launch-readiness checks in one pass.
---

# zip-preflight-guard

**Dominio:** [[agensi-agent-operator-utility-pack]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agensi-free\agent-operator-utility-pack\skills\zip-preflight-guard\SKILL.md`
- `C:\Users\david\Skills\agensi-free\agent-operator-utility-pack\skills\zip-preflight-guard\SKILL.md`

**Descripción:** Wrapper skill that runs a bundled intake-guard security scan then a built-in release-readiness flightcheck on a zip archive or directory. Emits a unified GO/NO-GO verdict. Use when you want both bomb/traversal/secret detection AND launch-readiness checks in one pass.

**Cuándo usar:** A **wrapper/orchestrator** skill. Does not replace its children — it chains them in sequence and unifies their outputs.

## Tags
#security #agensi-agent-operator-utility-pack

## Ejes temáticos
- [[security]]

## Skills relacionadas
- [[intake-guard]]
- [[context-handoff-spine]]
- [[mcp-candidate-inspector-lite]]
- [[test-surface-finder]]
