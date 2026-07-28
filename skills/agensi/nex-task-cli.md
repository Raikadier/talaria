---
name: nex-task-cli
domain: agensi
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\nex-task-cli\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\agensi-free\\nex-task-cli\\SKILL.md"
  - "C:\\Users\\david\\Skills\\agensi-free\\nex-task-cli\\SKILL.md"
tags: [youtube, data, agent, agensi]
description: "Generate a JSON-backed agent-callable task CLI in the shape of nex-task (the production CLI ZeroClaw uses). The CLI is a single-file Python script with a flat JSON store at ~/nex-data/taskboard.json, no database, no daemon, callable by humans (`task today`, `task add \"buy bread\" --due 2026-05-27 --high`) AND by orchestrator agents as a shell tool. Ships the canonical command set (list, today, overdue, done, stats, add, check, snooze, delete, search, cleanup, help), priority plus category plus due-date plus recurrence plus dedupe semantics, the prefix-id matching pattern (find by first 4-8 chars of UUID), and the recurring-task regeneration rule (check rolls forward by daily/weekday/weekly/monthly). Use this skill whenever the user wants a small personal task CLI without a SaaS dependency, builds an agent that needs a tool to schedule its own followups, or wants a JSON-as-DB pattern for any small list-shaped CLI (notes, bookmarks, snippets)."
---

# nex-task-cli

**Dominio:** [[agensi]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\agensi-free\nex-task-cli\SKILL.md`
- `C:\Users\david\Skills\agensi-free\nex-task-cli\SKILL.md`

**Descripción:** Generate a JSON-backed agent-callable task CLI in the shape of nex-task (the production CLI ZeroClaw uses). The CLI is a single-file Python script with a flat JSON store at ~/nex-data/taskboard.json, no database, no daemon, callable by humans (`task today`, `task add "buy bread" --due 2026-05-27 --high`) AND by orchestrator agents as a shell tool. Ships the canonical command set (list, today, overdue, done, stats, add, check, snooze, delete, search, cleanup, help), priority plus category plus due-date plus recurrence plus dedupe semantics, the prefix-id matching pattern (find by first 4-8 chars of UUID), and the recurring-task regeneration rule (check rolls forward by daily/weekday/weekly/monthly). Use this skill whenever the user wants a small personal task CLI without a SaaS dependency, builds an agent that needs a tool to schedule its own followups, or wants a JSON-as-DB pattern for any small list-shaped CLI (notes, bookmarks, snippets).

**Cuándo usar:** A JSON-backed agent-callable task CLI in the shape of `nex-task`, the production CLI used by ZeroClaw. One Python file, no DB server, no daemon, no install dance: `pip install -e .` and you have `task` on your `$PATH`.

## Tags
#youtube #data #agent #agensi

## Ejes temáticos
- [[youtube]]
- [[data]]
- [[agent]]

## Skills relacionadas
- [[Agensi Community Demand Analyzer with Grok]]
- [[Agensi Performance & Engagement Analyzer with Grok]]
- [[agent-memory-privacy-check]]
- [[agent-tool-trace-for-debug]]
- [[ai-security-auditor]]
- [[aomi-transact]]
- [[browser-act]]
- [[content-architect]]
- [[dataecho]]
- [[designer-carousel-post]]
- [[hotspot-radar]]
- [[lead-generation-agent]]
- [[longbridge]]
- [[markdown-to-pptx-deck]]
- [[marm-init]]
- [[normalize-prompt-set]]
- [[openhop]]
- [[prompt-injection-auditor]]
