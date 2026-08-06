---
tags: [decision, axon, forge, hydrate, packs]
aliases: [decision-axon-hydrate-packs]
date: 2026-08-05
status: accepted
---

# Decisión — Hidratación AXON + memory + packs (Act real)

## Contexto
El A/B barbería mostró que Cursor sin Talaria ya llega a producto usable; FORGE solo como playbook voluntario no fuerza salto. `--with-axon` devolvía hits/paths sin cuerpos; no había retrieve de `memory/`.

## Decisión
1. **`forge run` / `forge invoke` hidratan por defecto** — bodies de skills + `memory retrieve` en el packet (`skills_hydrated`, `memory`).
2. **Packs de misión** en `_META/axon/packs/` (`software-delivery`, `youtube-channel`). Curar = priorizar/empaquetar/degradar; no borrar el banco.
3. **Gate Gaxon** — entregable cita `axon_skills: [skills/…]`; `forge check --require-axon` (y `require_axon: true` en perfil, p.ej. tech-lead).
4. **Parity MCP** — `talaria_memory_retrieve`, `talaria_axon_pack_*`, args de hydrate/pack en forge run/invoke/check.

## Consecuencias
- Pilotos deben **aplicar** bodies del packet, no solo listar paths.
- Diferencia Talaria vs baseline se mide por uso real de skills/memoria + Gaxon, no solo por código generado.
- Próximo A/B: scoring explícito de cites AXON/memory en el entregable.
