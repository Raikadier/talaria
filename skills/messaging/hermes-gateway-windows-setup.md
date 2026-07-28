---
name: hermes-gateway-windows-setup
domain: messaging
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-gateway-windows-setup\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-gateway-windows-setup\\SKILL.md"
tags: [agent, messaging]
description: "Configure and make persistent Hermes Agent's messaging gateway (WhatsApp, Telegram, etc.) on Windows. Covers sending WhatsApp via `hermes send` with the E.164/+57 number format, the allowlist format, bringing up the gateway, and the Windows Task Scheduler Job Object pitfall that silently breaks the WhatsApp Node.js bridge. Use whenever the user wants to send a WhatsApp message through Hermes, keep the bot alive across reboots, or debug \"whatsapp failed to connect\" / \"Access is denied\" / \"Node.js not found\"."
---

# hermes-gateway-windows-setup

**Dominio:** [[messaging]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\messaging\hermes-gateway-windows-setup\SKILL.md`

**Descripción:** Configure and make persistent Hermes Agent's messaging gateway (WhatsApp, Telegram, etc.) on Windows. Covers sending WhatsApp via `hermes send` with the E.164/+57 number format, the allowlist format, bringing up the gateway, and the Windows Task Scheduler Job Object pitfall that silently breaks the WhatsApp Node.js bridge. Use whenever the user wants to send a WhatsApp message through Hermes, keep the bot alive across reboots, or debug "whatsapp failed to connect" / "Access is denied" / "Node.js not found".

**Cuándo usar:** - User wants to send a WhatsApp (or other platform) message via Hermes. - User wants the gateway / WhatsApp bot to stay alive and auto-start on Windows login ("siempre activo", "que arranque sola"). - Debugging `whatsapp failed to connect`, `WinError 5 Access is denied`, `Node.js

## Tags
#agent #messaging

## Ejes temáticos
- [[agent]]

## Skills relacionadas
- [[hermes-gateway-windows]]
- [[hermes-send]]
- [[hermes-whatsapp]]
