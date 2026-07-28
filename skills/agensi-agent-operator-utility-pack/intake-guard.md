---
name: intake-guard
domain: agensi-agent-operator-utility-pack
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-operator-utility-pack\\skills\\intake-guard\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-operator-utility-pack\\skills\\intake-guard\\SKILL.md"
  - "C:\\Users\\david\\Skills\\agensi-free\\agent-operator-utility-pack\\skills\\intake-guard\\SKILL.md"
tags: [coding, security, agensi-agent-operator-utility-pack]
description: Statically inspect a file, bounded directory walk, zip, or tar archive for security and coverage signals before extracting, packaging, or executing code. Emits a bounded JSON guard report with PASS/WARN/FAIL verdicts. Does not execute untrusted code. Use when you need to vet an artifact before further processing.
---

# intake-guard

**Dominio:** [[agensi-agent-operator-utility-pack]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agensi-free\agent-operator-utility-pack\skills\intake-guard\SKILL.md`
- `C:\Users\david\Skills\agensi-free\agent-operator-utility-pack\skills\intake-guard\SKILL.md`

**Descripción:** Statically inspect a file, bounded directory walk, zip, or tar archive for security and coverage signals before extracting, packaging, or executing code. Emits a bounded JSON guard report with PASS/WARN/FAIL verdicts. Does not execute untrusted code. Use when you need to vet an artifact before further processing.

**Cuándo usar:** Accept one raw artifact (file, directory, zip, tar, tar.gz, tar.bz2) and emit a bounded static guard report. This is the first stage of any guarded code-extraction pipeline — it checks the artifact surface and adapter coverage. It does **not** certify safety.

## Tags
#coding #security #agensi-agent-operator-utility-pack

## Ejes temáticos
- [[coding]]
- [[security]]

## Skills relacionadas
- [[context-handoff-spine]]
- [[mcp-candidate-inspector-lite]]
- [[test-surface-finder]]
- [[zip-preflight-guard]]
