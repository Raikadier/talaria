---
name: nex-arq-worker-pattern
domain: agensi
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\nex-arq-worker-pattern\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\nex-arq-worker-pattern\\SKILL.md"
  - "C:\\Users\\david\\Skills\\agensi-free\\nex-arq-worker-pattern\\SKILL.md"
tags: [coding, agensi]
description: "Generate a production-ready ARQ background worker for a FastAPI app, with a Redis-backed queue, an enqueue helper for the API, a Redis heartbeat the API can read, scheduled cron jobs, and a systemd unit, all wired the way a multi-tenant Pi-hosted SaaS actually runs it. Use this skill whenever the user wants to add background jobs to a FastAPI app, run a Python worker as a systemd service on a Raspberry Pi or Linux box, queue jobs from the API without blocking the request, schedule cron-style recurring jobs in Python, expose worker health to a `/api/infra/status` endpoint, or move from synchronous to async background processing. Pi-deploy hardened, no managed Celery service required."
---

# nex-arq-worker-pattern

**Dominio:** [[agensi]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agensi-free\nex-arq-worker-pattern\SKILL.md`
- `C:\Users\david\Skills\agensi-free\nex-arq-worker-pattern\SKILL.md`

**Descripción:** Generate a production-ready ARQ background worker for a FastAPI app, with a Redis-backed queue, an enqueue helper for the API, a Redis heartbeat the API can read, scheduled cron jobs, and a systemd unit, all wired the way a multi-tenant Pi-hosted SaaS actually runs it. Use this skill whenever the user wants to add background jobs to a FastAPI app, run a Python worker as a systemd service on a Raspberry Pi or Linux box, queue jobs from the API without blocking the request, schedule cron-style recurring jobs in Python, expose worker health to a `/api/infra/status` endpoint, or move from synchronous to async background processing. Pi-deploy hardened, no managed Celery service required.

**Cuándo usar:** Generates the background-job layer of a FastAPI app: an ARQ `WorkerSettings` class with the heartbeat loop, an `enqueue()` helper that the API calls, the cron-jobs block, the systemd unit that runs it under a non-root user, and the wiring on the API side that lets `/api/infra/sta

## Tags
#coding #agensi

## Ejes temáticos
- [[coding]]

## Skills relacionadas
- [[0-refactor-advisor]]
- [[a11y-code-auditor]]
- [[accessibility-auditor]]
- [[advise-project-approach]]
- [[Agensi Skill Authoring]]
- [[agent-context-engineer]]
- [[agent-loop-guardian]]
- [[agent-ready-api]]
- [[agent-ready-cli]]
- [[agent-ready-mcp]]
- [[agent-rule-compliance-auditor]]
- [[agent-rules-generator]]
- [[agent-self-verification-gate]]
- [[agent-skill-regression-tester]]
- [[agent-team-orchestrator]]
- [[agent-token-budget-manager]]
- [[agent-tool-call-resilience-engineer]]
- [[agentic-workflow]]
