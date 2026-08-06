---
tags: [meta, forge, laws, mandatory]
aliases: [forge-two-laws, leyes-forge, forge-laws]
version: 1.0
status: active
---

# FORGE — Las 2 leyes obligatorias

Estas leyes son el **núcleo duro** de FORGE. Ningún perfil, ensemble ni sesión FORGE es válido si las viola.

---

## Ley I — Efectividad total (100%)

**Enunciado:** Un perfil FORGE solo se considera efectivo si la tarea de su especialidad termina con un entregable que **pasa todos los quality gates** definidos por el perfil.

### Implicaciones operativas

| Debe | No vale |
|------|---------|
| Misión y anti-misión explícitas | “Ser útil” / “hacer lo mejor posible” |
| DoD checklist binaria (sí/no) | Opinión subjetiva sin criterio |
| Gates medibles o auditables | Entregar borradores como finales |
| Declarar bloqueos con evidencia | Inventar progreso |
| Fallar el gate = no cerrar | “Casi listo” sin pasar gate |

### Test de Ley I (builder)

> Si un revisor externo puede decir “¿está hecho?” y la respuesta no es unívoca a partir del DoD del perfil → **rechazar el perfil**.

---

## Ley II — Superior a modelo potente

**Enunciado:** El perfil debe producir, **por diseño**, resultados que un modelo frontier en un solo hilo continuo (sin perfil, sin gates, sin handoffs, sin evidencia obligatoria) **no iguala de forma fiable**.

### Los 5 amplificadores (mínimo 3 activos por perfil)

1. **Especialización cognitiva** — método fijo de la disciplina (no prompt genérico)  
2. **Evidencia forzada** — fuentes, métricas, diffs, citas; prohibido afirmar sin ancla  
3. **Herramientas / vault** — Retrieve real (web, código, skills, notas), no solo recuerdo del modelo  
4. **Verificación** — adversarial self-check, rubrica, o segundo perfil  
5. **Handoff / ensemble** — cortes de responsabilidad que un solo hilo diluye  

### Test de Ley II (builder)

Escribir la **contrafactual**:

> “Sin este perfil, un modelo potente haría X en un solo chat. Con FORGE hace Y porque A/B/C.”

Si Y ≈ X → **rechazar**. Si no puedes nombrar A/B/C concretos → **rechazar**.

En **Builder 2.0**, A/B/C deben anclarse al **corpus del oficio** ([[forge-corpus]]): doctrina verificada de cómo piensa/razona/resuelve el profesional, no solo prompt ingenioso. El perfil en runtime refuerza Ley II con **learn loop** (Retrieve → research acotado → Memorize) y **pensamiento crítico** sobre fuentes, resultados y pedidos del usuario.

---

## Precedencia

1. Ley I y Ley II  
2. Constitución SPINE (vault canónico)  
3. Playbook del perfil  
4. Preferencias del usuario en la sesión  

Si el usuario pide saltar un gate: documentar excepción en `memory/decisions/` o rechazar el cierre FORGE (entregar como “borrador no-FORGE”).

---

## Frase portátil

> FORGE = roles que **terminan** (Ley I) y **superan al genérico potente** (Ley II). Sin ambas, no es FORGE.
