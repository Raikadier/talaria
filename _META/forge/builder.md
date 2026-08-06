---
tags: [meta, forge, builder]
aliases: [forge-builder, profile-builder, constructor-perfiles, builder-2]
version: 2.0
status: active
---

# FORGE Builder 2.0 — fabricar perfiles como profesionales reales

El builder es el **protocolo** (humano o agente) para crear/actualizar perfiles.  
**v1** tallaba el contrato (DoD, gates, handoffs).  
**v2** añade lo que faltaba para Ley II de verdad: **formar el oficio con evidencia**, **aprender al vault en runtime**, **relacionar conocimiento** y **pensar con crítica**.

> FORGE no cosplaya al rol. **Estudia el oficio, duda, documenta, relaciona y se niega a cerrar sin evidencia.**

Leyes: [[forge-two-laws]] · Schema: [[forge-schema]] · Corpus: [[forge-corpus]] · Hub: [[forge]]

---

## Modelo mental (3 capas)

```
┌─────────────────────────────────────────────────────────┐
│ A. CORPUS DEL OFICIO   memory/research/forge/<id>/      │
│    Doctrina verificada (cómo piensa / razona / decide)  │
└───────────────────────────┬─────────────────────────────┘
                            │ cita / ancla
┌───────────────────────────▼─────────────────────────────┐
│ B. PERFIL EJECUTABLE   _META/forge/profiles/<id>.md     │
│    Misión, DoD, gates, stack, handoffs, learn loop      │
└───────────────────────────┬─────────────────────────────┘
                            │ runtime
┌───────────────────────────▼─────────────────────────────┐
│ C. LEARN LOOP          Retrieve → (gap?) → Research     │
│    → Validate → Memorize → Relacionar → Act → Critique  │
└─────────────────────────────────────────────────────────┘
```

**Regla de oro:** el perfil **cita** el corpus; no engulle libros enteros. El conocimiento durable vive en Markdown del vault (SPINE Memorize). Nunca segunda base fuera de Talaria.

---

## Entrada mínima del pedido

| Campo | Pregunta |
|-------|----------|
| Especialidad | ¿En qué debe ser elite? |
| Entregable | ¿Qué artefacto prueba el éxito? |
| Usuario del perfil | ¿Qué piloto lo usará? |
| Solo o ensemble | ¿Trabaja con otros roles? |
| Anti-ejemplos | ¿Qué hace un modelo genérico que debemos superar? |
| Corpus seed | ¿Hay libros/normas/fuentes obligatorias del oficio? |

---

## Desde cualquier piloto (Claude Code / Cursor / …)

Si el usuario dice algo como:

> «crea un agente que sepa responder correos usando talaria»

el piloto **no improvisa un system prompt**: ejecuta el builder vía CLI o MCP y sigue el `pilot_playbook` del JSON.

```bash
talaria forge build --brief "crea un agente que sepa responder correos usando talaria" --json
# MCP: talaria_forge_build { "brief": "..." }
```

Eso crea:
- perfil draft `_META/forge/profiles/<id>.md`
- corpus scaffold `memory/research/forge/<id>/`
- `pilot_playbook` (research → `forge check` → `active` → `forge run`)

Luego el piloto **ejecuta** ese playbook (rellena doctrina/fuentes, no deja cosplay).

Flags útiles: `--id`, `--specialty`, `--deliverable`, `--force`,  
`--kind orchestrator|specialist|both`, `--invokes a,b`, `--invocable-by x,y`, `--invocable-by-mode open|allowlist|deny_direct`.

El organigrama lo defines tú ([[forge-delegation]] · ejemplo [[forge-example-user-graph]]).

---

## Playbook Builder 2.0 (14 pasos)

### Fase A — Formar el oficio (antes del perfil)

#### 1. Nombrar
- `forge_id` kebab-case + título humano  
- Registrar en [[forge-catalog]] como `draft` hasta calibrar  
- Crear carpeta corpus: `memory/research/forge/<forge_id>/` (ver [[forge-corpus]])

#### 2. Research del oficio (verificado)
Activar mentalidad **researcher** (o perfil `researcher` si hay ensemble). Recopilar:
- rol, función, propósito en la industria  
- cómo **piensa / razona / resuelve** un profesional excelente  
- marcos, patrones, anti-patrones, entregables típicos  
- fuentes: libros, normas, papers, docs oficiales, practitioners reconocidos  

**Gates de esta fase (obligatorios):**

| Gate | Evidencia | Si falla |
|------|-----------|----------|
| C1 Scope | Pregunta del oficio + exclusiones | No buscar aún |
| C2 Sources | ≥5 fuentes serias con grado (primaria/secundaria) | Ampliar o bajar claims |
| C3 Trace | Claims clave del corpus → cita | Eliminar claim |
| C4 Doctrine | Nota `00-doctrine.md` con método cognitivo del rol | No tallar perfil |
| C5 Limits | Sección “qué no es este rol” | Reabrir |

Salida mínima del corpus: ver plantilla [[forge-corpus-template]].

#### 3. Contrafactual Ley II (con anclas)
Completar: sin perfil → X; con FORGE → Y; amplificadores A/B/C **citando** el corpus.  
Si Y ≈ X → **rechazar** (falta doctrina o gates).

### Fase B — Tallar el perfil ejecutable

#### 4. Misión / anti-misión
1–2 frases de resultado + qué **nunca** hace (evita dilución y cosplay).

#### 5. DoD (Ley I)
Checklist binaria del entregable final. Cada ítem auditable.

#### 6. Stack cognitivo
5–12 pasos. **Debe** incluir:
- Retrieve corpus + vault/proyecto  
- Detectar hueco de conocimiento → learn loop  
- Relacionar conocimientos previos (ADRs, notas, patrones)  
- Verificación / crítica **antes** del entregable final  

#### 7. Quality gates
≥ 3 gates con evidencia + fallo (parar / iterar / escalar).  
Incluir al menos un gate de **crítica** (fuentes, resultado o pedido del usuario).

#### 8. Contratos I/O y handoff
Si ensemble: formatos (ADR, brief, patch set…). Si solo: decirlo explícito.

#### 9. Retrieve map + corpus refs
- Ejes/dominios AXON, fuentes externas permitidas/prohibidas  
- Frontmatter `corpus_path` + wiki-links a `00-doctrine.md` y guías clave  

#### 10. Learn loop (runtime)
Declarar política:
1. Retrieve corpus/proyecto primero  
2. Si el vacío **bloquea un gate** → research acotado  
3. Validar (grado de fuente + crítica)  
4. Memorize en `memory/research/forge/<id>/` o `memory/projects/…` ordenado  
5. Reanudar Act con el nuevo conocimiento  
**Prohibido:** investigar infinito; fabricar URLs; Memorize sin traza.

#### 11. Pensamiento crítico (obligatorio en el perfil)
El perfil debe razonar explícitamente sobre:
- **Información investigada** — sesgo, frescura, grado, contradicciones  
- **Resultados de la tarea** — ¿pasan gates? ¿over/under-design?  
- **Pedidos del usuario** — ¿piden saltar un gate? ¿fuera de anti-misión? documentar excepción o rechazar cierre FORGE  

#### 12. Fallos y activación
Tabla de fallos + bloque copy-paste de activación.

#### 13. Calibración
Checklist abajo. Si algún NO → `status: draft`, no `active`.

#### 14. Publicar
- Archivo: `_META/forge/profiles/<forge_id>.md`  
- Bump catálogo · `talaria forge check --profile <id> --json`  
- Decisión en `memory/decisions/` si cambia contrato de un perfil ya usado  

---

## Checklist de calibración (obligatoria)

### Contrato (v1)
- [ ] Ley I: DoD unívoco  
- [ ] Ley II: contrafactual + ≥3 amplificadores anclados a corpus  
- [ ] Schema completo ([[forge-schema]])  
- [ ] Gates con evidencia (≥1 gate de crítica)  
- [ ] Anti-misión clara  
- [ ] Handoffs definidos o “solo” explícito  
- [ ] Salida con plantilla  
- [ ] Compatible SPINE (Memorize al vault)  
- [ ] Ejecutable solo con la nota del perfil + corpus enlazado  
- [ ] No depende de un solo vendor/modelo  

### Oficio (v2)
- [ ] Corpus con C1–C5 en pass  
- [ ] `00-doctrine.md` describe cómo piensa/razona/resuelve el rol  
- [ ] Learn loop documentado (cuándo investigar / dónde guardar)  
- [ ] Política de pensamiento crítico explícita  
- [ ] Relación de conocimientos: cómo usa ADRs/notas previas del vault  

---

## Anti-patrones del builder

| Anti-patrón | Por qué mata FORGE |
|-------------|-------------------|
| Perfil = system prompt largo | Sin gates → falla Ley I |
| “Experto en todo X” | Sin especialización → falla Ley II |
| Personalidad sin método | Cosplay, no efectividad |
| Ensemble sin contratos | Los roles se pisan |
| Gates subjetivos (“queda bien”) | No auditables |
| Corpus = dump de PDFs sin síntesis | No hay doctrina usable |
| Perfil engulle el corpus entero | Hinchado; no ejecutable |
| Aprender sin gate de traza | Contamina el vault |
| Investigación en cada turno | Paraliza; ignora Retrieve |
| “Parecer humano” vía ego/rolplay | Diluye juicio profesional |

---

## Actualizar un perfil existente → v2

1. Crear/completar corpus bajo `memory/research/forge/<id>/`  
2. Añadir secciones Learn loop + Crítica + `corpus_path`  
3. Reescribir contrafactual Ley II con anclas de corpus  
4. Bump `forge_version` (p. ej. `2.0`)  
5. Diff de DoD/gates en `memory/decisions/` si cambia el contrato  
6. Re-correr checklist + `talaria forge check`  

Perfiles v1 siguen válidos como contrato; **no se marcan elite v2** hasta pasar Fase A.

---

## Salida del builder

| Artefacto | Ruta |
|-----------|------|
| Corpus del oficio | `memory/research/forge/<id>/` |
| Perfil | `_META/forge/profiles/<id>.md` |
| Plantilla perfil | [[forge-profile-template]] |
| Plantilla corpus | [[forge-corpus-template]] |
| Índice | [[forge-catalog]] · [[forge-corpus]] |

## Relación con researcher

Para Fase A, el builder **debe** comportarse como [[forge-profile-researcher]] (método, citas, adversarial).  
Si la tarea es grande: ensemble corto `researcher → forge-builder` antes de publicar el perfil.
