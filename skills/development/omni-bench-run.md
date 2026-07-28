---
name: omni-bench-run
domain: development
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\omni-bench-run\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\omni-bench-run\\SKILL.md"
tags: [development]
description: "Run a model through the omni-bench benchmark to MEASURE it — produce a run-artifact and score it, then read the numbers. Use when asked to run, benchmark, measure, evaluate, or \"test the results of\" a model with omni-bench — ASR (WER/CER, RTFx) or text generation (tok/s, TTFT, prefill tok/s, prompt-cache speedup). Covers the adapter seam (Transcriber/Generator), the prepare→run→score→diff CLI flow, the offline no-download smoke task, and how to interpret each metric. NOT for publishing to a leaderboard (use omni-bench-publish) or changing the framework itself (use omni-bench)."
---

# omni-bench-run

**Dominio:** [[development]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\community\beshkenadze\skills\development\omni-bench-run\SKILL.md`

**Descripción:** Run a model through the omni-bench benchmark to MEASURE it — produce a run-artifact and score it, then read the numbers. Use when asked to run, benchmark, measure, evaluate, or "test the results of" a model with omni-bench — ASR (WER/CER, RTFx) or text generation (tok/s, TTFT, prefill tok/s, prompt-cache speedup). Covers the adapter seam (Transcriber/Generator), the prepare→run→score→diff CLI flow, the offline no-download smoke task, and how to interpret each metric. NOT for publishing to a leaderboard (use omni-bench-publish) or changing the framework itself (use omni-bench).

**Cuándo usar:** omni-bench measures **quality + speed tied to specific hardware** (ASR: WER/CER + RTFx; text generation: tok/s, TTFT/prefill, prompt-cache benefit). It is a **framework, not a runner**: YOU provide inference through a small adapter seam; omni-bench owns the datasets, the scoring,

## Tags
#development

## Skills relacionadas
- [[biome]]
- [[codex-code-review]]
- [[dev-workflow]]
- [[git-worktree-workflow]]
- [[gitea-tea]]
- [[gitea-wiki]]
- [[ios-design-review]]
- [[ios-design-workflow]]
- [[ios-hig-reference]]
- [[ios-swiftui-generator]]
- [[omni-bench]]
- [[omni-bench-publish]]
- [[python-uv]]
- [[research-guide]]
- [[swiftui-developer]]
- [[typescript-advanced-types]]
- [[zamokctl]]
- [[zenstack]]
