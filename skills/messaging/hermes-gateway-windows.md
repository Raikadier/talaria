---
name: hermes-gateway-windows
domain: messaging
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-gateway-windows\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-gateway-windows\\SKILL.md"
tags: [agent, messaging]
description: "Configure and troubleshoot the Hermes Agent messaging gateway (WhatsApp, Telegram) on Windows. Covers hermes whatsapp pairing, hermes send targets, the WHATSAPP_ALLOWED_USERS allowlist format, and the two Windows-specific pitfalls that silently break the WhatsApp bridge under the Scheduled Task - the Task Scheduler Job Object (WinError 5 Access is denied) and unreliable node PATH resolution. Use when a Windows user reports WhatsApp won't connect, the bot won't reply, or the gateway exits."
---

# hermes-gateway-windows

**Dominio:** [[messaging]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\messaging\hermes-gateway-windows\SKILL.md`

**Descripción:** Configure and troubleshoot the Hermes Agent messaging gateway (WhatsApp, Telegram) on Windows. Covers hermes whatsapp pairing, hermes send targets, the WHATSAPP_ALLOWED_USERS allowlist format, and the two Windows-specific pitfalls that silently break the WhatsApp bridge under the Scheduled Task - the Task Scheduler Job Object (WinError 5 Access is denied) and unreliable node PATH resolution. Use when a Windows user reports WhatsApp won't connect, the bot won't reply, or the gateway exits.

**Cuándo usar:** Applies to Hermes Agent running on Windows (MSYS/git-bash shell; PowerShell also used). The gateway multiplexes messaging platforms (Telegram, WhatsApp, etc.) and the in-process cron scheduler. This skill is about getting it **running and persistent on Windows**, which has two tr

## Tags
#agent #messaging

## Ejes temáticos
- [[agent]]

## Skills relacionadas
- [[hermes-gateway-windows-setup]]
- [[hermes-send]]
- [[hermes-whatsapp]]
