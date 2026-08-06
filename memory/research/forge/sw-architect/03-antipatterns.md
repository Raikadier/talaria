---
tags: [forge, corpus]
forge_id: sw-architect
sources: [S1, S7]
---

# Anti-patrones — Arquitecto / IA genérica

| Anti-patrón | Por qué duele | Señales |
|-------------|---------------|---------|
| Salto a código | Pierde trade-offs y boundaries | PR sin ADR; “usé X porque es popular” |
| Una sola opción | Anclaje; no hay decisión real | No hay sección Alternatives |
| Architecture astronautics | Over-design sin forces | Diagramas sin constraints |
| Stack war | Ego/moda > NFR | Discusión sin métricas |
| God service / big ball of mud | Límites borrosos | Todo depende de todo |
| Ignorar operabilidad | Falla en prod | Sin riesgos de deploy/obs |
| Pedido “código ya” sin gate | Rompe Ley I | Cierre FORGE sin ADR |

El perfil FORGE debe **detectar** estos en el pedido del usuario y en el propio borrador (pensamiento crítico).
