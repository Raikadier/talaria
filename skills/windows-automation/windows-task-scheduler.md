---
name: windows-task-scheduler
domain: windows-automation
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows-automation\\windows-task-scheduler\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows-automation\\windows-task-scheduler\\SKILL.md"
tags: [windows-automation]
description: Create silent, unattended Windows scheduled tasks (Task Scheduler) for recurring maintenance like weekly winget upgrades — without prompts or admin-elevation pain. Covers the reliable XML + schtasks /create approach, S4U vs InteractiveToken for non-admin users, UAC token-filtering pitfalls when detecting admin, and why to write PowerShell via .ps1 files under git-bash/MSYS. Use when the user wants something to run on a schedule on their Windows PC without being asked every time.
---

# windows-task-scheduler

**Dominio:** [[windows-automation]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\windows-automation\windows-task-scheduler\SKILL.md`

**Descripción:** Create silent, unattended Windows scheduled tasks (Task Scheduler) for recurring maintenance like weekly winget upgrades — without prompts or admin-elevation pain. Covers the reliable XML + schtasks /create approach, S4U vs InteractiveToken for non-admin users, UAC token-filtering pitfalls when detecting admin, and why to write PowerShell via .ps1 files under git-bash/MSYS. Use when the user wants something to run on a schedule on their Windows PC without being asked every time.

**Cuándo usar:** Use when the user wants something to run on a schedule on their Windows PC without being asked every time — e.g. "actualiza todos mis programas cada semana como winget pero sin preguntar", "corre X todos los lunes", "automatiza esto en segundo plano".

## Tags
#windows-automation

## Skills relacionadas
- [[windows-automation]]
