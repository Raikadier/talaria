---
name: research
domain: community
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\alirezarezvani\\research\\research\\skills\\research\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\alirezarezvani\\research\\research\\skills\\research\\SKILL.md"
tags: [agent, research, community]
description: "Default entry point for any research request — a hybrid router that classifies the question deterministically and either delegates to a specialist research skill (pulse for trends/sentiment, grants for NIH funding, litreview for academic literature, syllabus for course reading, patent for prior-art + IP landscape, dossier for entity research) or runs its own plan-decompose-multi-source-search-synthesize-cite fallback workflow when no specialist matches. Always surfaces the routing decision so users can override. Use when the user makes any research request that doesn't obviously match a more-specific specialist skill (e.g., \"research [topic]\", \"look into [topic]\", \"what do we know about [topic]\", \"investigate [topic]\", \"find me information on [topic]\", \"do some research on [topic]\", \"I need to understand [topic]\"). Output is a markdown briefing (default) or .docx document (on request) with full citations and an audit log."
---

# research

**Dominio:** [[community]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\community\alirezarezvani\research\research\skills\research\SKILL.md`

**Descripción:** Default entry point for any research request — a hybrid router that classifies the question deterministically and either delegates to a specialist research skill (pulse for trends/sentiment, grants for NIH funding, litreview for academic literature, syllabus for course reading, patent for prior-art + IP landscape, dossier for entity research) or runs its own plan-decompose-multi-source-search-synthesize-cite fallback workflow when no specialist matches. Always surfaces the routing decision so users can override. Use when the user makes any research request that doesn't obviously match a more-specific specialist skill (e.g., "research [topic]", "look into [topic]", "what do we know about [topic]", "investigate [topic]", "find me information on [topic]", "do some research on [topic]", "I need to understand [topic]"). Output is a markdown briefing (default) or .docx document (on request) with full citations and an audit log.

**Cuándo usar:** **The runtime orchestrator for the research domain.** Architecture C: deterministic classification → specialist delegation OR own plan-decompose-search-synthesize-cite workflow.

## Tags
#agent #research #community

## Ejes temáticos
- [[agent]]
- [[research]]

## Skills relacionadas
- [[agent-decision-receipts]]
- [[agent-designer]]
- [[agent-protocol]]
- [[agenthub]]
- [[board-meeting]]
- [[grants]]
- [[hermes-tweet]]
- [[litreview]]
- [[llm-wiki]]
- [[notebooklm]]
- [[parallel-debugging]]
- [[pm-skills]]
- [[product-skills]]
- [[pulse]]
- [[research-summarizer]]
- [[senior-qa]]
- [[syllabus]]
- [[agent-harness]]
