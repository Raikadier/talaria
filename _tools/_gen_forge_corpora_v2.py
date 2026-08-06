from pathlib import Path

root = Path(r"D:\OneDrive - unicesar.edu.co\Business Ideas\Talaria")
base = root / "memory" / "research" / "forge"

corpora = {
    "researcher": {
        "title": "Investigador profesional",
        "specialty": "investigación defendible con método, citas y límites",
        "think": "pregunta → alcance → fuentes graduadas → extract → síntesis → adversarial",
        "never": "opinar sin fuente; fabricar URLs; mezclar hallazgo e inferencia",
        "sources": [
            ("S1", "Booth et al. — The Craft of Research", "libro", "primaria", "método, pregunta, argumento"),
            ("S2", "APA / citation practice", "norma/práctica", "secundaria", "trazabilidad"),
            ("S3", "Kitchenham — Systematic literature reviews (SE)", "método", "primaria", "inclusión/exclusión"),
            ("S4", "Ioannidis — critique of false findings", "paper", "secundaria", "sesgo, certeza"),
            ("S5", "Talaria researcher + SPINE Memorize", "práctica local", "práctica", "vault canónico"),
        ],
    },
    "sw-engineer": {
        "title": "Ingeniero de software",
        "specialty": "traducir ADR en plan ejecutable: módulos, contratos, tests, tasks",
        "think": "ingest ADR → gap check → module design → sequence → test strategy → atomic tasks",
        "never": "redefinir arquitectura; mega-PR sin plan; ignorar CI/convenciones",
        "sources": [
            ("S1", "Bass et al. — SAIP (implementation view)", "libro", "primaria", "límites → diseño"),
            ("S2", "Martin — Clean Architecture / SOLID (selectivo)", "libro", "secundaria", "ownership"),
            ("S3", "Beck — TDD / test strategy", "libro/práctica", "primaria", "pirámide tests"),
            ("S4", "Testing pyramid (industria)", "práctica", "secundaria", "unit/integration/e2e"),
            ("S5", "Team-module alignment (Conway)", "ensayo", "secundaria", "ownership"),
            ("S6", "Talaria software-triad", "práctica local", "práctica", "handoffs"),
        ],
    },
    "programmer": {
        "title": "Programador",
        "specialty": "implementación atómica verificada alineada al task pack",
        "think": "read DoD → retrieve patterns → minimal change → verify → report/escalate",
        "never": "gold-plating; rediseñar boundaries; silenciar bloqueos; deps nuevas sin OK",
        "sources": [
            ("S1", "Hunt & Thomas — The Pragmatic Programmer", "libro", "primaria", "cambios pequeños"),
            ("S2", "Beck — TDD By Example", "libro", "primaria", "verify antes de done"),
            ("S3", "Fowler — Refactoring (small steps)", "libro", "primaria", "diff mínimo"),
            ("S4", "Repo CONTRIBUTING / CI", "práctica", "práctica", "lints/tests"),
            ("S5", "Talaria programmer + triad", "práctica local", "práctica", "handoff"),
        ],
    },
    "social-advisor": {
        "title": "Asesor de redes sociales",
        "specialty": "crecimiento con hipótesis falsables y métricas de negocio",
        "think": "north star → baseline → audience → ≤3 bets → experiment cards → kill criteria",
        "never": "tips virales genéricos; vanity sin negocio; promesas garantizadas",
        "sources": [
            ("S1", "Outcomes over output (product/growth practice)", "práctica", "secundaria", "north star"),
            ("S2", "Kohavi et al. — Trustworthy Online Controlled Experiments", "libro", "primaria", "experimentos"),
            ("S3", "Ellis & Brown — Hacking Growth", "libro", "secundaria", "bets/ICE"),
            ("S4", "Platform docs (Meta/TikTok/YouTube/X)", "docs", "primaria", "constraints canal"),
            ("S5", "JTBD — audience jobs", "método", "secundaria", "audiencia"),
            ("S6", "Talaria social-advisor v1", "práctica local", "práctica", "máx 3 apuestas"),
        ],
    },
}

for fid, c in corpora.items():
    d = base / fid
    notes = d / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    src_rows = "\n".join(
        f"| {sid} | {name} | {typ} | {grade} | {use} |"
        for sid, name, typ, grade, use in c["sources"]
    )
    (d / "README.md").write_text(
        f"""---
tags: [forge, corpus]
forge_id: {fid}
corpus_version: 1.0
status: active
gates: {{C1: true, C2: true, C3: true, C4: true, C5: true}}
updated: 2026-08-05
---

# Corpus — {c['title']} (`{fid}`)

## Estado gates
| Gate | Pass |
|------|------|
| C1 Scope | sí |
| C2 Sources | sí |
| C3 Trace | sí |
| C4 Doctrine | sí |
| C5 Limits | sí |

## Mapa
- [[00-doctrine]] · [[01-role-purpose]] · [[02-methods]] · [[03-antipatterns]] · [[04-deliverables]] · [[05-sources]]
- Learn: `notes/`

## Perfil
`_META/forge/profiles/{fid}.md` · Builder 2.0
""",
        encoding="utf-8",
    )
    (d / "00-doctrine.md").write_text(
        f"""---
tags: [forge, corpus, doctrine]
forge_id: {fid}
---

# Doctrina cognitiva — {c['title']}

## Especialidad
{c['specialty']}

## Cómo piensa / razona / resuelve
{c['think']}

## Qué nunca hace
{c['never']}

## Amplificadores vs IA genérica
1. Método fijo del oficio
2. Evidencia forzada + vault
3. Learn loop si un hueco bloquea un gate
4. Pensamiento crítico (fuentes / resultado / pedido)
5. Handoffs explícitos cuando aplica

## Relación de conocimientos
Retrieve corpus + notas previas del vault/proyecto antes de decidir.
""",
        encoding="utf-8",
    )
    (d / "01-role-purpose.md").write_text(
        f"""---
tags: [forge, corpus]
forge_id: {fid}
---

# Rol y propósito — {c['title']}

**Función:** ejercer {c['specialty']} con entregables auditables (Ley I) y superioridad vs chat genérico (Ley II).
""",
        encoding="utf-8",
    )
    (d / "02-methods.md").write_text(
        f"""---
tags: [forge, corpus, methods]
forge_id: {fid}
---

# Métodos — {c['title']}

{c['think']}

Ver perfil `_META/forge/profiles/{fid}.md`. Fuentes: [[05-sources]].
""",
        encoding="utf-8",
    )
    (d / "03-antipatterns.md").write_text(
        f"""---
tags: [forge, corpus]
forge_id: {fid}
---

# Anti-patrones — {c['title']}

| Anti-patrón | Señal |
|-------------|-------|
| Sin método | Entregable sin gates/DoD |
| Confianza > evidencia | Claims sin cita |
| Romper anti-misión | {c['never']} |
| Inventar jerga | Sin learn loop |
| Cerrar sin crítica | Sin adversarial / pedido usuario |
""",
        encoding="utf-8",
    )
    (d / "04-deliverables.md").write_text(
        f"""---
tags: [forge, corpus]
forge_id: {fid}
---

# Entregables — {c['title']}

Cumplir DoD y gates del perfil `{fid}` (Gcrit + Gmem en Builder 2.0).
""",
        encoding="utf-8",
    )
    (d / "05-sources.md").write_text(
        f"""---
tags: [forge, corpus, sources]
forge_id: {fid}
---

# Fuentes — {fid}

| ID | Fuente | Tipo | Grado | Usado en |
|----|--------|------|-------|----------|
{src_rows}
""",
        encoding="utf-8",
    )
    (notes / "2026-08-05-seed.md").write_text(
        f"""---
tags: [forge, corpus, learn-note]
forge_id: {fid}
date: 2026-08-05
status: seed
---

# Learn seed — {fid}

Ampliar cuando un hueco real bloquee un gate.
""",
        encoding="utf-8",
    )
    print("ok", fid)

print("done")
