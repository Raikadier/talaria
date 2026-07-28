---
name: omni-bench-publish
domain: development
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\omni-bench-publish\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\omni-bench-publish\\SKILL.md"
tags: [coding, development]
description: "Publish a scored omni-bench result (ASR or text-generation) to a leaderboard platform (e.g. bench.bshk.app) via its write API. Use when asked to publish, upload, submit, or \"send a report\" for an omni-bench result.json or parity-report.json — sharing ASR WER/RTFx numbers or text-generation TTFT/tok-per-s/prompt-cache numbers. Covers the one modality-agnostic `omni-bench publish` command and the MANDATORY secret handling: the api-key is injected from a secrets manager (1Password `op run` / AgentVault `av run`) at runtime, never read into context, never hardcoded."
---

# omni-bench-publish

**Dominio:** [[development]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\community\beshkenadze\skills\development\omni-bench-publish\SKILL.md`

**Descripción:** Publish a scored omni-bench result (ASR or text-generation) to a leaderboard platform (e.g. bench.bshk.app) via its write API. Use when asked to publish, upload, submit, or "send a report" for an omni-bench result.json or parity-report.json — sharing ASR WER/RTFx numbers or text-generation TTFT/tok-per-s/prompt-cache numbers. Covers the one modality-agnostic `omni-bench publish` command and the MANDATORY secret handling: the api-key is injected from a secrets manager (1Password `op run` / AgentVault `av run`) at runtime, never read into context, never hardcoded.

**Cuándo usar:** Upload a **scored** `result.json` (and optionally a `parity-report.json`) to an omni-bench results platform (default `https://bench.bshk.app`) via `POST /api/v1/results`. The command is **identical for every modality** — ASR (WER / RTFx) and text generation (tok/s / TTFT / prompt

## Tags
#coding #development

## Ejes temáticos
- [[coding]]

## Skills relacionadas
- [[biome]]
- [[codex-code-review]]
- [[ios-design-review]]
- [[ios-swiftui-generator]]
- [[swiftui-developer]]
- [[dev-workflow]]
- [[git-worktree-workflow]]
- [[gitea-tea]]
- [[gitea-wiki]]
- [[ios-design-workflow]]
- [[ios-hig-reference]]
- [[omni-bench]]
- [[omni-bench-run]]
- [[python-uv]]
- [[research-guide]]
- [[typescript-advanced-types]]
- [[zamokctl]]
- [[zenstack]]
