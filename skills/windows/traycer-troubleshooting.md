---
name: traycer-troubleshooting
domain: windows
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows\\traycer-troubleshooting\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\windows\\traycer-troubleshooting\\SKILL.md"
tags: [windows]
description: "Diagnose and fix Traycer Desktop / Traycer Host installation failures on Windows, especially the \"traycer-cli timed out after 600000ms (host ensure --json)\" error. Covers where the logs live, `host doctor`, the 10-minute desktop timeout trap, and the out-of-band `host install` workaround. Use when the user reports Traycer won't start, hangs on \"host ensure\", or shows HOST_NOT_READY."
---

# traycer-troubleshooting

**Dominio:** [[windows]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\windows\traycer-troubleshooting\SKILL.md`

**Descripción:** Diagnose and fix Traycer Desktop / Traycer Host installation failures on Windows, especially the "traycer-cli timed out after 600000ms (host ensure --json)" error. Covers where the logs live, `host doctor`, the 10-minute desktop timeout trap, and the out-of-band `host install` workaround. Use when the user reports Traycer won't start, hangs on "host ensure", or shows HOST_NOT_READY.

**Cuándo usar:** Traycer Desktop (an Electron app) is a thin shell. The real work is done by a separate **"Host"** binary (~808 MB on win32-x64) that the CLI downloads and runs as a supervised OS service (`ai.traycer.host`). On startup the desktop auto-runs `traycer host ensure`; if the host is m

## Tags
#windows

## Skills relacionadas
- [[windows-cli-install]]
- [[windows-pc-optimization]]
- [[windows-selective-elevation]]
