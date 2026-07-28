---
name: agent-guardrails
domain: agensi
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-guardrails-tiered-hitl-governance-for-ai-agent-writes\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\agent-guardrails-tiered-hitl-governance-for-ai-agent-writes\\SKILL.md"
  - "C:\\Users\\david\\Skills\\agensi-free\\agent-guardrails-tiered-hitl-governance-for-ai-agent-writes\\SKILL.md"
tags: [agent, security, agensi]
description: "Use when an AI agent is about to perform a WRITE action (a payment, a delete, a deploy, a schema/auth change, a bulk mutation, or any irreversible side effect) and you need to decide whether it can run automatically, needs a lightweight confirmation, or requires explicit human approval. Triggers on: agent write-action, irreversible action, human-in-the-loop, HITL, approval gate, guardrail, \"should the agent be allowed to do this unattended\", destructive operation, bulk operation."
---

# agent-guardrails

**Dominio:** [[agensi]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agensi-free\agent-guardrails-tiered-hitl-governance-for-ai-agent-writes\SKILL.md`
- `C:\Users\david\Skills\agensi-free\agent-guardrails-tiered-hitl-governance-for-ai-agent-writes\SKILL.md`

**Descripción:** Use when an AI agent is about to perform a WRITE action (a payment, a delete, a deploy, a schema/auth change, a bulk mutation, or any irreversible side effect) and you need to decide whether it can run automatically, needs a lightweight confirmation, or requires explicit human approval. Triggers on: agent write-action, irreversible action, human-in-the-loop, HITL, approval gate, guardrail, "should the agent be allowed to do this unattended", destructive operation, bulk operation.

**Cuándo usar:** Autonomous agents read safely. The risk is when they **write**. This skill is the decision procedure that sits between an agent's *intent* and the *action*: it classifies how dangerous a proposed action is and forces the right level of approval before anything runs. The invariant

## Tags
#agent #security #agensi

## Ejes temáticos
- [[agent]]
- [[security]]

## Skills relacionadas
- [[agent-handoff-orchestrator]]
- [[agent-memory-privacy-check]]
- [[agent-rule-compliance-auditor]]
- [[agent-supply-chain-auditor]]
- [[ai-security-auditor]]
- [[ci-cd-pipeline-validator]]
- [[code-reviewer]]
- [[crypto-arb-signal]]
- [[Effective Debugging with Grok]]
- [[longbridge]]
- [[marm-init]]
- [[openhop]]
- [[production-agent-design]]
- [[prompt-injection-auditor]]
- [[skill-preflight]]
- [[snap-private-payments]]
- [[technical-scanner]]
- [[ac-buying-consultant]]
