---
tags: [meta, agent, protocol, second-brain]
aliases: [protocolo-agentes, agent protocol]
---

# Protocolo para agentes de IA

Reglas para **cualquier** agente (Cursor, Hermes, Claude, etc.) que use este vault como memoria compartida.

## Principio

Este vault es la **fuente de verdad** persistente. El chat es efímero; lo importante se escribe aquí en Markdown con `[[wiki links]]`.

Opera bajo el marco **[[ironman-framework]]** (capas IRONMAN + ownership de tools). Las tools son sistemas del traje; no crean memorias paralelas.

## Qué guardar (siempre)

| Tipo | Carpeta | Cuándo |
|------|---------|--------|
| Resumen de conversación útil | `memory/conversations/` | Tras decisiones, planes, hallazgos o contexto reutilizable |
| Decisión | `memory/decisions/` | Cuando se elige A sobre B con consecuencias |
| Aprendizaje / preferencia | `memory/learnings/` | Preferencias del usuario, lecciones, anti-patrones |
| Estado de proyecto | `memory/projects/` | Al iniciar o al cambiar estado material |
| Captura rápida | `memory/inbox/` | Si no sabes dónde va aún |

## Qué NO guardar

- Secretos (API keys, passwords, tokens) — nunca en claro
- Volcados crudos de chat enteros sin resumen
- Ruido trivial (“ok”, “continua”) sin contenido nuevo

## Cómo escribir

1. Usa la plantilla de `_templates/` correspondiente.
2. Frontmatter YAML + cuerpo en español (salvo código/nombres propios).
3. Enlaza siempre a:
   - `[[Home]]` o proyecto relacionado
   - skills relevantes (`[[nombre-skill]]`)
   - ejes (`[[youtube]]`, `[[coding]]`, etc.) si aplica
4. Tags: `#conversation` `#decision` `#project` `#learning` + dominio
5. Título de archivo: `YYYY-MM-DD-slug-corto.md` (conversaciones/decisiones/learnings)

## Flujo mínimo al cerrar una sesión útil

```
1. ¿Hubo decisión? → memory/decisions/
2. ¿Hay contexto reutilizable? → memory/conversations/
3. ¿Cambió un proyecto? → actualizar memory/projects/<nombre>.md
4. ¿Preferencia nueva del usuario? → memory/learnings/
5. Actualizar "Última actividad" en el proyecto o en Home
```

## Cómo consultar (antes de actuar)

1. Leer `[[Home]]` y `[[agent-protocol]]` si es la primera vez en el vault.
2. Si es un clone nuevo: `python bootstrap.py` (ver [[PORTABILITY]]).
3. Buscar en `memory/projects/` el proyecto activo.
4. Revisar conversaciones/decisiones recientes del mismo tema.
5. Si la tarea usa una capacidad concreta, mirar `skills/` o `[[taxonomy]]`.
6. Documentos externos → [[markitdown]]; repos → [[graphify]].

## Ingestión

- Documento: `python _tools/ingest_document.py <archivo|url>`
- Proyecto: `python _tools/ingest_project.py <ruta>`
- Auto-deps: `python bootstrap.py`

## Idempotencia

Si ya existe una nota del mismo tema el mismo día, **actualiza** esa nota en lugar de crear duplicados.
