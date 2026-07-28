---
date: 2026-07-27
type: conversation
source_agent: cursor
session_id: "e1d76327-2dbf-4cb2-a7d1-3d2fb2bbec2c"
project: "c-Users-david-projects-agent-skills-bank"
source_path: "C:\\Users\\david\\.cursor\\projects\\c-Users-david-projects-agent-skills-bank\\agent-transcripts\\b9ceeac9-6e10-4944-8a65-a13cc484fa14\\subagents\\e1d76327-2dbf-4cb2-a7d1-3d2fb2bbec2c.jsonl"
tags: [conversation, imported, cursor]
title: "CRITICAL: Previous push-batch agents keep failing with max retries. Be extremely careful w"
---

# CRITICAL: Previous push-batch agents keep failing with max retries. Be extremely careful w

**Fecha:** 2026-07-27  
**Agente:** cursor  
**Proyecto/contexto:** c-Users-david-projects-agent-skills-bank  
**Sesión:** `e1d76327-2dbf-4cb2-a7d1-3d2fb2bbec2c`  
**Origen:** `C:\Users\david\.cursor\projects\c-Users-david-projects-agent-skills-bank\agent-transcripts\b9ceeac9-6e10-4944-8a65-a13cc484fa14\subagents\e1d76327-2dbf-4cb2-a7d1-3d2fb2bbec2c.jsonl`

## Mensajes

### Usuario

CRITICAL: Previous push-batch agents keep failing with max retries. Be extremely careful with short shell commands.

User wants Hermes Skills Hub mirror finished into Raikadier/agent-skills-bank.

Repo: C:\Users\david\projects\agent-skills-bank
Python: C:\Users\david\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe
Script: scripts/download_hermes_hub.py
Progress: skills/hermes-hub/_state/progress.json
Logs: C:\Users\david\projects\skills-cache\clawhub-download.log and skills-sh-download.log

DO THIS IN ORDER — one short shell at a time:

1. Read progress stats only:
   python -c "import json; print(json.load(open(r'C:\Users\david\projects\agent-skills-bank\skills\hermes-hub\_state\progress.json',encoding='utf-8')).get('stats'))"

2. Check if download processes alive (Get-CimInstance for download_hermes_hub). If none, restart:
   Start-Process with -u script --section ClawHub --workers 20
   Start-Process with -u script --section skills.sh --workers 6
   Set GH_TOKEN from gh auth token first.

3. If .git/index.lock exists and no git process: Remove-Item the lock.

4. List clawhub category dirs. For the FIRST category that is not fully tracked in git, do:
   git add skills/hermes-hub/clawhub/<category>
   git add skills/hermes-hub/_state/progress.json
   git commit -m "..."
   git push origin HEAD
   Then optionally ONE more small category if first succeeded.

5. Final Spanish reply: counts, downloads running?, what pushed, blockers.

AVOID: giant git add, waiting forever, parallel huge ops, reading progress.json while writing if possible.
Timeouts: prefer block_until 60000 for git add of one category.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
