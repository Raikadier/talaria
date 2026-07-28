---
date: 2026-07-28
type: research
tags: [research, skillgraph, guarantees, architecture, spine]
status: active
projects: [SkillGraph]
aliases: [garantias-skillgraph, hardening-skillgraph]
---

# Cómo garantizar funcionamiento y resultados (hardening SkillGraph)

**Contexto:** el organismo + API ya está planteado ([[architecture]] · [[organism]]). Hoy la efectividad depende demasiado de que el piloto “obedezca”. Esto cierra esa brecha.

## Diagnóstico (qué no está garantizado aún)

| Promesa | Estado hoy | Hueco |
|---------|------------|-------|
| Cualquier agente se conecta | `describe` / MCP existen | Boot no es obligatorio ni verificado al inicio de sesión |
| SPINE se cumple | Documentado | Nadie falla la tarea si se salta Memorize |
| FORGE > modelo potente | Leyes en papel | Gates no se ejecutan ni se auditan |
| AXON usable | Grafo generado | Retrieve no tipado; sin “smoke” de skills críticas |
| Resultados acumulativos | Vault canónico | Sin checklist de cierre ni score de sesión |
| Tools Mk.N | `doctor` parcial | Doctor ≠ organismo completo (órganos + API + reglas) |

**Principio:** lo que no se puede **fallar en máquina** no está garantizado; solo recomendado.

---

## Mejoras (por apalancamiento)

### 1. Runtime de garantías (prioridad máxima)

Añadir un órgano ligero de **verificación** (propuesta de nombre: **LOCK** — *Lifecycle Outcome Checkpoint Kit*, o simplemente módulo `skillgraph verify`).

**Al arrancar sesión (gate de entrada):**
```text
skillgraph verify boot --json
→ órganos presentes · MCP/CLI · Mark · AGENTS/SPINE legibles
exit ≠ 0 ⇒ el agente debe boot/arreglar antes de Act serio
```

**Al cerrar trabajo útil (gate de salida):**
```text
skillgraph verify close --json
→ ¿hubo Memorize? ¿nota enlazada? ¿FORGE gates si profile activo?
exit ≠ 0 ⇒ no declarar “done”
```

Sin esto, SPINE/FORGE siguen siendo honor system.

### 2. Contrato FORGE ejecutable

- Cada perfil: `gates[].id` + `evidence_path` o checklist YAML embebido  
- `skillgraph forge run <id> --task "..."` emite playbook + **rubrica**  
- `skillgraph forge check <session>` valida DoD (sí/no)  
- Ensemble software-triad: no permitir `programmer` sin ADR/task pack referenciado  

Ley I deja de ser texto; Ley II se demuestra con **contrafactual guardado** en la nota de entregable.

### 3. Scorecard de sesión (resultados esperados)

Plantilla obligatoria al Memorize de trabajo no trivial:

| Campo | Pregunta |
|-------|----------|
| Objetivo | ¿Qué se pidió? |
| Órganos usados | memoria / axon / forge / tools |
| Evidencia | paths `[[...]]` |
| Gates | pass/fail |
| Delta vs genérico | 1–3 bullets “por qué esto no lo habría sostenido un chat solo” |

Si el scorecard falta → `verify close` falla.

### 4. Ampliar `doctor` → health del organismo

Hoy chequea tools. Debe chequear:

- [ ] `Home` / `AGENTS` / `spine-framework` / `axon` / `forge` existen  
- [ ] `memory/` + `skills/` no vacíos  
- [ ] MCP contract `describe` coherente  
- [ ] Mark declarado vs tools  
- [ ] (opcional) última `verify close` < N días en proyecto activo  

### 5. Smoke tests canónicos (CI local)

Suite mínima `_tools/smoke_skillgraph.py` o `skillgraph test`:

1. `describe --json` parseable  
2. `doctor` exit esperado  
3. Ingest de un PDF/txt de fixture → aparece en `memory/inbox/converted/`  
4. Lectura de 1 skill AXON + 1 perfil FORGE  
5. `verify boot` verde  

Correr tras cambios de CLI/órganos. Garantiza *funcionamiento*; no solo diseño.

### 6. API surface completa (órganos en el contrato)

`describe --json` debe listar:

```json
"organs": ["memory","axon","forge","spine","api","tools","adapters"],
"commands": { "forge": [...], "verify": [...], "axon": ["search?"] }
```

Si un órgano no tiene comando, el agente no lo “descubre” y no lo usa.

### 7. Retrieve tipado sobre AXON

- `skillgraph axon search "growth linkedin" --json` (grep/frontmatter primero; engraph después)  
- Perfiles FORGE declaran `axon_queries` default  
- Evita “el modelo recuerda skills” en vez de leer el grafo  

### 8. Política de modos (esperado vs borrador)

| Modo | Garantía |
|------|----------|
| `spine=strict` | verify boot/close obligatorios; FORGE gates on |
| `spine=draft` | permite Act sin Memorize; **no** se marca done FORGE |
| Default recomendado | `strict` en trabajo de proyecto; `draft` solo exploración |

El usuario elige; el sistema no finge que draft = resultado garantizado.

### 9. Eval harness (Ley II medible)

Para 5–10 tareas gold (research brief, growth plan, ADR+3 tasks):

- Baseline: un chat genérico sin SkillGraph  
- Contender: mismo modelo + SPINE+FORGE+AXON  
- Rubrica ciega (o checklist binaria del perfil)  
- Guardar en `memory/research/evals/`  

Sin evals, “superior a modelo potente” es fe; con evals es evidencia.

### 10. Operación multi-piloto

- Un solo `describe` como fuente  
- Adaptadores con **misma** verify  
- Alerta si Hermes/Cursor/Claude escriben fuera de `memory/` tipado  

---

## Roadmap sugerido (orden)

| Fase | Entrega | Garantiza | Estado |
|------|---------|-----------|--------|
| **A** | `verify boot/close` + scorecard template | Cierre honesto | **hecho** (CLI 0.3.0) |
| **B** | `doctor` organismo + smoke tests | Funcionamiento API | **hecho** (CLI 0.3.0) |
| **C** | `forge list/show/check/run` + gates | Resultados de rol | **hecho** (CLI 0.4.0) |
| **D** | `axon search` + queries en perfiles | Uso real del grafo | **hecho** (CLI 0.5.0) |
| **E** | Eval harness 5 tareas | Ley II medible | **hecho** (CLI 1.0.0) |
| **F** | Modo strict/draft en contract | Expectativas claras | **hecho** (`mode get/set`, `--mode`) |

### AXON (Fase D)

```bash
python -m skillgraph_cli axon search "refactor coding" --json
python -m skillgraph_cli axon for-profile researcher --json
python -m skillgraph_cli forge run researcher --with-axon --json
python -m skillgraph_cli axon stats --json
```

### FORGE (Fase C)

```bash
python -m skillgraph_cli forge list --ensembles --json
python -m skillgraph_cli forge show researcher --json
python -m skillgraph_cli forge run researcher --json
python -m skillgraph_cli forge check --profile researcher --json
python -m skillgraph_cli forge check --profile researcher --declare "G1=pass,G2=pass,G3=pass,G4=pass,G5=pass" --json
python -m skillgraph_cli forge check --profile researcher --deliverable path/to/note.md --json
```

Plantilla entregable: `_templates/forge-deliverable.md`

### Uso inmediato

```bash
python -m skillgraph_cli verify boot --json
python -m skillgraph_cli doctor --json
python -m skillgraph_cli smoke --json
# al cerrar:
python -m skillgraph_cli verify close --scorecard memory/conversations/<scorecard>.md --json
```

Plantilla: `_templates/scorecard.md`

---

## Qué no haría (aún)

- Microservicios / DB paralela al vault  
- Reescribir SPINE desde cero  
- Decenas de órganos nuevos antes de verify  
- Prometer autonomía Mk.5 sin A–C verdes  

---

## Decisión pendiente

¿Implementar Fase A+B ahora en la CLI? → abrir decisión o Act directo.

## Enlaces

- [[architecture]] · [[forge-two-laws]] · [[spine-framework]] · [[cli-architecture]]
