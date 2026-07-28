---
name: hermes-whatsapp-gateway
domain: messaging-automation
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging-automation\\hermes-whatsapp-gateway\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging-automation\\hermes-whatsapp-gateway\\SKILL.md"
tags: [agent, messaging-automation]
description: "Set up, fix, and persist the Hermes WhatsApp bot gateway on Windows. Covers allowlist/DM policy, Windows auto-start (Startup folder vs the Scheduled Task Job Object trap), .env editing, session persistence, and \"receives but won't reply\" diagnosis. Use when David asks to configure the WhatsApp bot, switch the bot number, make it \"always on / start on boot\", or debug \"bot not responding / not connected / Access denied\"."
---

# hermes-whatsapp-gateway

**Dominio:** [[messaging-automation]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\messaging-automation\hermes-whatsapp-gateway\SKILL.md`

**Descripción:** Set up, fix, and persist the Hermes WhatsApp bot gateway on Windows. Covers allowlist/DM policy, Windows auto-start (Startup folder vs the Scheduled Task Job Object trap), .env editing, session persistence, and "receives but won't reply" diagnosis. Use when David asks to configure the WhatsApp bot, switch the bot number, make it "always on / start on boot", or debug "bot not responding / not connected / Access denied".

**Cuándo usar:** Recurring class of work for David. The Hermes WhatsApp bot is a `gateway` process that spawns a node.js bridge (`hermes-agent/scripts/whatsapp-bridge/bridge.js`) listening on **port 3000**. Agent core lives in `C:\Users\david\AppData\Local\hermes` (HERMES_HOME). Config is in `.en

## Tags
#agent #messaging-automation

## Ejes temáticos
- [[agent]]

## Skills relacionadas
- [[messaging-automation]]
