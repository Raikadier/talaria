---
tags: [meta, forge, builder]
aliases: [forge-builder, profile-builder, constructor-perfiles]
version: 1.0
status: active
---

# FORGE Builder — cómo fabricar un perfil 100% efectivo

El builder es el **protocolo** (humano o agente) para crear/actualizar perfiles. No improvisar secciones: seguir este playbook.

## Entrada mínima del pedido

| Campo | Pregunta |
|-------|----------|
| Especialidad | ¿En qué debe ser elite? |
| Entregable | ¿Qué artefacto prueba el éxito? |
| Usuario del perfil | ¿Qué piloto lo usará? (Cursor/Hermes/Claude/cualquiera) |
| Solo o ensemble | ¿Trabaja con otros roles? |
| Anti-ejemplos | ¿Qué hace un modelo genérico que debemos superar? |

## Playbook del builder (10 pasos)

### 1. Nombrar
- `forge_id` kebab-case + título humano  
- Registrar en [[forge-catalog]]

### 2. Tallar misión / anti-misión
- Misión: 1–2 frases, verbos de resultado  
- Anti-misión: qué **nunca** hace (evita dilución)

### 3. Definir DoD (Ley I)
Checklist binaria del entregable final. Cada ítem debe ser auditable.

### 4. Escribir contrafactual (Ley II)
Completar: sin perfil → X; con perfil → Y; amplificadores A/B/C. Mínimo **3 amplificadores**.

### 5. Diseñar stack cognitivo
5–12 pasos ordenados. Incluir Retrieve y verificación **antes** del entregable final.

### 6. Quality gates
≥ 3 gates. Para cada uno: evidencia requerida + qué pasa si falla (parar / iterar / escalar).

### 7. Contratos de I/O y handoff
Si hay ensemble: especificar formato de entrada/salida (ADR, brief, patch set, etc.).

### 8. Retrieve map
Listar: ejes/dominios SkillGraph, tipos de fuente externa, prohibiciones de fuente.

### 9. Fallos y activación
Tabla de fallos + bloque de activación copy-paste.

### 10. Calibración final
Pasar checklist abajo. Si algún NO → no publicar como `active`.

## Checklist de calibración (obligatoria)

- [ ] Ley I: DoD unívoco  
- [ ] Ley II: contrafactual + ≥3 amplificadores  
- [ ] Schema completo ([[forge-schema]])  
- [ ] Gates con evidencia  
- [ ] Anti-misión clara  
- [ ] Handoffs definidos o “solo” explícito  
- [ ] Salida con plantilla  
- [ ] Compatible SPINE (Memorize al vault)  
- [ ] Un agente sin contexto FORGE puede ejecutarlo solo con la nota del perfil  
- [ ] No depende de un solo vendor/modelo  

## Anti-patrones del builder

| Anti-patrón | Por qué mata FORGE |
|-------------|-------------------|
| Perfil = system prompt largo | Sin gates → falla Ley I |
| “Experto en todo X” | Sin especialización → falla Ley II |
| Personalidad sin método | Cosplay, no efectividad |
| Ensemble sin contratos | Los roles se pisan |
| Gates subjetivos (“queda bien”) | No auditables |

## Actualizar un perfil existente

1. Bump `forge_version`  
2. Diff de DoD/gates en `memory/decisions/` si cambia el contrato  
3. Re-correr checklist  
4. Actualizar [[forge-catalog]]

## Salida del builder

Archivo: `_META/forge/profiles/<forge_id>.md`  
Usar plantilla: [[forge-profile-template]]  
Índice: [[forge-catalog]] · Leyes: [[forge-two-laws]] · Hub: [[forge]]
