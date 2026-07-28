---
name: windows-cli-install
domain: windows
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows\\windows-cli-install\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows\\windows-cli-install\\SKILL.md"
tags: [windows]
description: "Install and run global Node/npm CLI tools and interactive TUIs on David's Windows machine (terminal runs through git-bash/MSYS). Covers recurring failures: npx path corruption under MSYS, npm -g postinstall scripts that tar a downloaded binary and break on Windows backslash paths, and interactive TUI selectors that need -y (and where -g fails for PromptScript skills). Use whenever you must install a global CLI, run npx, or drive an interactive terminal installer on this host."
---

# windows-cli-install

**Dominio:** [[windows]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\windows\windows-cli-install\SKILL.md`

**Descripción:** Install and run global Node/npm CLI tools and interactive TUIs on David's Windows machine (terminal runs through git-bash/MSYS). Covers recurring failures: npx path corruption under MSYS, npm -g postinstall scripts that tar a downloaded binary and break on Windows backslash paths, and interactive TUI selectors that need -y (and where -g fails for PromptScript skills). Use whenever you must install a global CLI, run npx, or drive an interactive terminal installer on this host.

**Cuándo usar:** Environment facts for David's machine (stable, not a one-off): - Shell is **git-bash / MSYS** (POSIX syntax: `ls`, `$HOME`, `&&`, single quotes). `C:\Users\david` = `$HOME` = `/c/Users/david`. - `npm` global prefix = `%APPDATA%\npm` = `C:\Users\david\AppData\Roaming\npm`, and **t

## Tags
#windows

## Skills relacionadas
- [[traycer-troubleshooting]]
- [[windows-pc-optimization]]
- [[windows-selective-elevation]]
