---
name: hermes-send
domain: messaging
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-send\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\messaging\\hermes-send\\SKILL.md"
tags: [coding, agent, messaging]
description: "Send messages to external platforms (WhatsApp, Telegram, Signal, Discord, Slack) via the Hermes `send` CLI and the WhatsApp bridge. Use when the user asks to \"send a message\", \"mandar un mensaje por WhatsApp/Telegram\", or wire up a cron/notification that delivers text. Covers target format, the WhatsApp E.164 country-code pitfall, and verification."
---

# hermes-send

**Dominio:** [[messaging]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\messaging\hermes-send\SKILL.md`

**Descripción:** Send messages to external platforms (WhatsApp, Telegram, Signal, Discord, Slack) via the Hermes `send` CLI and the WhatsApp bridge. Use when the user asks to "send a message", "mandar un mensaje por WhatsApp/Telegram", or wire up a cron/notification that delivers text. Covers target format, the WhatsApp E.164 country-code pitfall, and verification.

**Cuándo usar:** Use `hermes send` to push text (and optional media) to any platform Hermes is already configured for. No LLM, no agent loop, no running gateway needed for bot-token platforms (Telegram/Discord/Slack/Signal). WhatsApp goes through a local bridge paired via QR and REQUIRES the inte

## Tags
#coding #agent #messaging

## Ejes temáticos
- [[coding]]
- [[agent]]

## Skills relacionadas
- [[hermes-gateway-windows]]
- [[hermes-gateway-windows-setup]]
- [[hermes-whatsapp]]
