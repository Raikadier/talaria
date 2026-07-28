---
name: agent-auto-routing
domain: agent-auto-routing
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agent-auto-routing\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agent-auto-routing\\SKILL.md"
tags: [agent, research, security, agent-auto-routing]
description: "Reflex router that auto-loads high-value agent/multi-agent/automation skills (agent-workflow-designer, agenthub, deep-research, agent-harness, autoresearch-agent, handoff, agent-decision-receipts, ai-security, board-meeting, etc.) based on signal words in the user's prompt — no explicit invocation needed. Enforced standard: see AGENT-ROUTING-STANDARD.md."
---

# agent-auto-routing

**Dominio:** [[agent-auto-routing]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agent-auto-routing\SKILL.md`

**Descripción:** Reflex router that auto-loads high-value agent/multi-agent/automation skills (agent-workflow-designer, agenthub, deep-research, agent-harness, autoresearch-agent, handoff, agent-decision-receipts, ai-security, board-meeting, etc.) based on signal words in the user's prompt — no explicit invocation needed. Enforced standard: see AGENT-ROUTING-STANDARD.md.

**Cuándo usar:** On EVERY user prompt, before answering, run the routing pass. If a registered skill matches with sufficient confidence, load it via `skill_view` and follow its body. This is a reflex, not a menu. The full spec (signal table, tie-break, guards) lives at `skills/community/../../AGE

## Tags
#agent #research #security #agent-auto-routing

## Ejes temáticos
- [[agent]]
- [[research]]
- [[security]]

## Skills relacionadas
- [[agent-auto-routing]]
