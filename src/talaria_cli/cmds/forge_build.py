"""FORGE build — create a draft agent/profile from a natural-language brief.

Any coding agent (Claude Code, Cursor, …) can run:

  talaria forge build --brief "crea un agente que sepa responder correos" --json

This scaffolds Builder 2.0 corpus + draft profile and returns a pilot playbook
so the LLM fills doctrine/sources, then `forge check` / `forge run`.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from talaria_cli.cmds.forge import (
    evaluate_profile_structure,
    load_profile,
    profiles_root,
)
from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

STOP = {
    "un",
    "una",
    "el",
    "la",
    "los",
    "las",
    "de",
    "del",
    "que",
    "para",
    "con",
    "por",
    "en",
    "y",
    "o",
    "a",
    "al",
    "se",
    "su",
    "sus",
    "the",
    "a",
    "an",
    "to",
    "for",
    "with",
    "using",
    "usando",
    "talaria",
    "forge",
    "crea",
    "crear",
    "create",
    "make",
    "build",
    "agente",
    "agent",
    "perfil",
    "profile",
    "que",
    "sepa",
    "sabe",
    "know",
    "knows",
    "how",
    "to",
}


def slugify_id(text: str, *, fallback: str = "custom-agent") -> str:
    raw = text.lower().strip()
    raw = re.sub(r"[áàäâ]", "a", raw)
    raw = re.sub(r"[éèëê]", "e", raw)
    raw = re.sub(r"[íìïî]", "i", raw)
    raw = re.sub(r"[óòöô]", "o", raw)
    raw = re.sub(r"[úùüû]", "u", raw)
    raw = re.sub(r"[^a-z0-9\s\-]+", " ", raw)
    parts = [p for p in re.split(r"[\s_\-]+", raw) if p and p not in STOP]
    if not parts:
        parts = [fallback]
    # prefer meaningful tail tokens
    if len(parts) > 4:
        parts = parts[-4:]
    slug = "-".join(parts)[:48].strip("-")
    return slug or fallback


def _ensure_unique_id(vault: Path, forge_id: str) -> str:
    root = profiles_root(vault)
    candidate = forge_id
    n = 2
    while (root / f"{candidate}.md").is_file():
        candidate = f"{forge_id}-{n}"
        n += 1
    return candidate


def _title_from_brief(brief: str, forge_id: str) -> str:
    b = brief.strip()
    # strip common prefixes
    b = re.sub(
        r"^(crea(r)?|create|make|build)\s+(un\s+|una\s+|an?\s+)?(agente|agent|perfil|profile)\s+"
        r"(que\s+)?",
        "",
        b,
        flags=re.I,
    )
    b = re.sub(r"^(sepa|sabe|knows?\s+how\s+to|how\s+to)\s+", "", b, flags=re.I)
    b = re.sub(r"\s+usando\s+talaria\s*$", "", b, flags=re.I)
    b = b.strip(" .")
    if not b:
        return forge_id.replace("-", " ").title()
    return b[0].upper() + b[1:]


def build_profile_from_brief(
    vault: Path,
    brief: str,
    *,
    forge_id: str | None = None,
    specialty: str | None = None,
    deliverable: str | None = None,
    force: bool = False,
    role_kind: str = "both",
    invocable_by_mode: str = "open",
    invocable_by: list[str] | str | None = None,
    invokes: list[str] | str | None = None,
) -> dict[str, Any]:
    brief = (brief or "").strip()
    if not brief:
        return {"ok": False, "error": "brief required"}

    from talaria_cli.cmds.forge_delegation import VALID_KINDS, VALID_MODES, _as_str_list

    kind = (role_kind or "both").strip().lower()
    if kind not in VALID_KINDS:
        return {"ok": False, "error": f"invalid role_kind: {role_kind} (use {sorted(VALID_KINDS)})"}
    mode = (invocable_by_mode or "open").strip().lower()
    if mode not in VALID_MODES:
        return {"ok": False, "error": f"invalid invocable_by_mode: {invocable_by_mode}"}
    by_list = _as_str_list(invocable_by)
    invokes_list = _as_str_list(invokes)

    fid = forge_id or slugify_id(brief)
    fid = re.sub(r"[^a-z0-9\-]", "", fid.lower()) or "custom-agent"
    if not force:
        fid = _ensure_unique_id(vault, fid)

    title = _title_from_brief(brief, fid)
    spec = specialty or title
    out_deliverable = (
        deliverable
        or f"Entregable canónico en vault que demuestre dominio de: {spec}"
    )
    today = date.today().isoformat()

    def _yaml_list(items: list[str]) -> str:
        if not items:
            return "[]"
        return "[" + ", ".join(items) + "]"

    corpus_rel = f"memory/research/forge/{fid}"
    corpus_dir = vault / corpus_rel
    notes_dir = corpus_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)

    # --- corpus scaffold ---
    (corpus_dir / "README.md").write_text(
        f"""---
tags: [forge, corpus]
forge_id: {fid}
corpus_version: 0.1
status: draft
gates: {{C1: false, C2: false, C3: false, C4: false, C5: false}}
updated: {today}
brief: {brief!r}
---

# Corpus — {title} (`{fid}`)

## Estado gates (Builder 2.0)
| Gate | Pass | Nota |
|------|------|------|
| C1 Scope | | Definir oficio + exclusiones |
| C2 Sources | | ≥5 fuentes serias en [[05-sources]] |
| C3 Trace | | Claims → citas |
| C4 Doctrine | | Completar [[00-doctrine]] |
| C5 Limits | | Qué no es este rol |

## Brief de origen
{brief}

## Mapa
- [[00-doctrine]] · [[01-role-purpose]] · [[02-methods]] · [[03-antipatterns]] · [[04-deliverables]] · [[05-sources]]
- Learn: `notes/`

## Perfil
`_META/forge/profiles/{fid}.md`
""",
        encoding="utf-8",
    )

    (corpus_dir / "00-doctrine.md").write_text(
        f"""---
tags: [forge, corpus, doctrine]
forge_id: {fid}
status: draft
---

# Doctrina cognitiva — {title}

> Completar con research verificado (libros, normas, docs). No dejar cosplay.

## Especialidad
{spec}

## Cómo piensa
(preguntas que se hace primero un excelente profesional de este oficio)

## Cómo razona
(criterios, trade-offs, evidencia)

## Cómo resuelve problemas
(pasos típicos; qué recupera antes de decidir)

## Qué nunca hace
(anti-patrones de juicio / anti-misión)

## Amplificadores vs IA genérica
1. Método fijo del oficio
2. Evidencia forzada + vault
3. Learn loop si un hueco bloquea un gate
4. Pensamiento crítico (fuentes / resultado / pedido)
5. …

## Relación de conocimientos
Retrieve corpus + notas del vault/proyecto antes de actuar.
""",
        encoding="utf-8",
    )

    for name, body in (
        (
            "01-role-purpose.md",
            f"# Rol y propósito — {title}\n\n**Brief:** {brief}\n\n**Función:** {spec}\n",
        ),
        (
            "02-methods.md",
            f"# Métodos — {title}\n\nCompletar marcos/patrones del oficio. Ver perfil `{fid}`.\n",
        ),
        (
            "03-antipatterns.md",
            f"# Anti-patrones — {title}\n\n| Anti-patrón | Señal |\n|-------------|-------|\n| Chat genérico | Sin gates/DoD |\n| Confianza > evidencia | Claims sin cita |\n",
        ),
        (
            "04-deliverables.md",
            f"# Entregables — {title}\n\n**DoD objetivo:** {out_deliverable}\n\nIncluir Gcrit + Gmem en el perfil.\n",
        ),
        (
            "05-sources.md",
            f"""# Fuentes — {fid}

| ID | Fuente | Tipo | Grado | Usado en |
|----|--------|------|-------|----------|
| S1 | _(pendiente research)_ | | primaria/sec. | doctrine |

≥5 fuentes serias antes de `status: active`.
""",
        ),
    ):
        (corpus_dir / name).write_text(
            f"---\ntags: [forge, corpus]\nforge_id: {fid}\n---\n\n{body}",
            encoding="utf-8",
        )

    (notes_dir / f"{today}-seed.md").write_text(
        f"""---
tags: [forge, corpus, learn-note]
forge_id: {fid}
date: {today}
status: seed
---

# Learn seed — {fid}

Ampliar cuando un hueco real bloquee un gate en una tarea.
""",
        encoding="utf-8",
    )

    # --- draft profile ---
    by_yaml = _yaml_list(by_list)
    inv_yaml = _yaml_list(invokes_list)
    delegation_section = ""
    if kind in {"orchestrator", "both"} or invokes_list:
        delegation_section = f"""
## Delegación (grafo usuario)

**role_kind:** `{kind}` · **invocable_by_mode:** `{mode}`  
**invocable_by:** {by_yaml}  
**invokes:** {inv_yaml}  

- Dueño del vault: siempre puede `talaria forge run {fid}`.  
- Delegación automática: `talaria forge invoke <parent> {fid}` o desde este perfil hacia hijos.  
- Doc: [[forge-delegation]]
"""
    profile_body = f"""---
tags: [forge, profile]
aliases: [forge-profile-{fid}]
forge_id: {fid}
forge_version: 2.0
status: draft
specialty: {spec}
laws: [I, II]
amplifiers: [especializacion, evidencia, herramientas, verificacion]
ensemble_roles: []
spine_layers: [orient, retrieve, act, memorize, notify]
axon_queries:
  - "{spec}"
corpus_path: {corpus_rel}
builder: 2.0
built_from_brief: true
brief_date: {today}
role_kind: {kind}
invocable_by_mode: {mode}
invocable_by: {by_yaml}
invokes: {inv_yaml}
---

# FORGE Profile — {title}

## 1. Identidad

**Misión:** Ser elite en: {spec}. Entregar resultados auditables en el vault.  
**Anti-misión:** No improvisar como chat genérico; no afirmar sin evidencia; no saltar gates.  
**Activar cuando:** la tarea pide este oficio (brief: {brief!r}).  
**No activar cuando:** la tarea es de otro dominio o solo brainstorm sin rigor.
**role_kind:** {kind}

Corpus: `{corpus_rel}/` · [[00-doctrine]]
{delegation_section}
## 2. Test Ley I / II

**DoD (Ley I):**
- [ ] Objetivo / pedido aclarado por escrito  
- [ ] Retrieve corpus + vault relevantes  
- [ ] {out_deliverable}  
- [ ] Evidencia / citas cuando haya claims  
- [ ] Crítica explícita (fuentes / resultado / pedido)  
- [ ] Memorize en vault  

**Contrafactual (Ley II):**  
Sin perfil: respuesta genérica sobre «{spec}».  
Con FORGE: doctrina + gates + learn loop + crítica → entregable defendible.  
Amplificadores: anclar a corpus tras completar C1–C5.

## 3. Stack cognitivo

1. Frame del pedido  
2. Retrieve corpus (`00-doctrine`) + AXON + vault  
3. Gap? → learn loop  
4. Relacionar conocimientos previos  
5. Act / producir entregable  
6. Crítica adversarial  
7. Memorize + Notify  

### Learn loop
1. Retrieve primero  
2. Si el vacío bloquea un gate → research acotado  
3. Validar + crítica  
4. Memorize en `{corpus_rel}/notes/`  
5. Reanudar Act  

## 4. Quality gates

| Gate | Evidencia | Si falla |
|------|-----------|----------|
| G1 Frame | Pedido/objetivo escrito | No actuar aún |
| G2 Retrieve | Corpus/vault citados | Buscar más |
| G3 Deliverable | Artefacto cumple DoD | Iterar |
| G4 Evidence | Claims con ancla | Eliminar o marcar |
| G5 Vault | Nota canónica | No cerrar |
| Gcrit Crítica | Sección crítica | Iterar o rechazar cierre |
| Gmem Memorize | Path vault (+ learn note si gap) | No cerrar FORGE |

## 5. Entradas / salidas

**Entrada:** brief del usuario + contexto.  
**Salida:** {out_deliverable}

## 6. Retrieve + corpus

- Corpus: `{corpus_rel}/`  
- AXON: queries del frontmatter  
- Prohibido: inventar fuentes; fabricar URLs  

## 7. Learn loop

Ver §3. Seed: `notes/{today}-seed.md`.

## 8. Pensamiento crítico

| Sobre | Preguntas |
|-------|-----------|
| Información investigada | ¿Grado? ¿Sesgo? |
| Resultados | ¿Pasan gates? |
| Pedidos del usuario | ¿Saltan anti-misión/gates? |

## 9. Handoffs

| De | Recibe | Entrega a | Formato |
|----|--------|-----------|---------|
| Usuario / piloto | Brief | Usuario / proyecto | Entregable + nota vault |

## 10. Modos de fallo

| Síntoma | Recuperación |
|---------|--------------|
| Corpus vacío | Completar C1–C5 antes de `active` |
| Scope creep | Re-frame |
| Usuario salta gates | Excepción documentada o no cerrar |

## 11. Activación

```text
FORGE profile={fid} | laws=I+II | builder=2.0 | corpus=on | spine=on
```

## 12. Calibración

- [ ] Corpus C1–C5 pass  
- [ ] Checklist [[forge-builder]] v2  
- [ ] `talaria forge check --profile {fid}`  
- [ ] Subir a `status: active` solo entonces  
"""

    profiles_root(vault).mkdir(parents=True, exist_ok=True)
    profile_path = profiles_root(vault) / f"{fid}.md"
    if profile_path.is_file() and not force:
        return {"ok": False, "error": f"profile exists: {fid}"}
    profile_path.write_text(profile_body, encoding="utf-8")

    # catalog hint note (append row instruction for pilot)
    catalog = vault / "_META/forge/catalog.md"
    catalog_note = ""
    if catalog.is_file() and f"`{fid}`" not in catalog.read_text(encoding="utf-8"):
        catalog_note = f"Add row to catalog: `{fid}` | {title} | 2.0 draft | `{corpus_rel}/`"

    profile = load_profile(vault, fid)
    struct = evaluate_profile_structure(profile, vault) if profile else {"ok": False}

    pilot_playbook = [
        f"1. Research the craft for «{spec}» and fill {corpus_rel}/00-doctrine.md + 05-sources.md (gates C1–C5).",
        f"2. Enrich _META/forge/profiles/{fid}.md mission/anti-mission/DoD if needed.",
        f"3. talaria forge check --profile {fid} --json",
        "4. When C1–C5 pass: set profile+corpus status to active; update _META/forge/catalog.md (optional — your catalog)",
        f"5. talaria session start --objective \"Use {fid}\" --forge {fid} --json",
        f"6. talaria forge run {fid} --with-axon --json  → execute playbook for the user task",
    ]
    if invokes_list:
        pilot_playbook.append(
            f"6b. Delegate specialists: talaria forge invoke {fid} <child> --brief \"…\" --json "
            f"(declared: {', '.join(invokes_list)})"
        )
    if by_list:
        pilot_playbook.append(
            f"6c. Preferred callers (invocable_by): {', '.join(by_list)} — mode={mode}"
        )
    pilot_playbook.append("7. talaria session close --json")

    return {
        "ok": True,
        "command": "forge build",
        "forge_id": fid,
        "title": title,
        "specialty": spec,
        "status": "draft",
        "brief": brief,
        "builder": "2.0",
        "role_kind": kind,
        "invocable_by_mode": mode,
        "invocable_by": by_list,
        "invokes": invokes_list,
        "paths": {
            "profile": f"_META/forge/profiles/{fid}.md",
            "corpus": corpus_rel,
            "doctrine": f"{corpus_rel}/00-doctrine.md",
            "sources": f"{corpus_rel}/05-sources.md",
        },
        "structure": struct,
        "catalog_note": catalog_note,
        "pilot_playbook": pilot_playbook,
        "activation": f"FORGE profile={fid} | laws=I+II | builder=2.0 | corpus=on | spine=on",
        "next_for_coding_agent": (
            "You are the pilot. Execute pilot_playbook now: complete corpus research, "
            "then forge check, then forge run for the user's real task. "
            "Talaria does not own the org chart — the user owns this agent graph."
        ),
        "user_prompt_example": f'crea un agente que {spec} usando talaria',
    }


def run_build(
    vault: Path,
    brief: str,
    *,
    forge_id: str | None = None,
    specialty: str | None = None,
    deliverable: str | None = None,
    force: bool = False,
    role_kind: str = "both",
    invocable_by_mode: str = "open",
    invocable_by: list[str] | str | None = None,
    invokes: list[str] | str | None = None,
    as_json: bool = False,
) -> int:
    data = build_profile_from_brief(
        vault,
        brief,
        forge_id=forge_id,
        specialty=specialty,
        deliverable=deliverable,
        force=force,
        role_kind=role_kind,
        invocable_by_mode=invocable_by_mode,
        invocable_by=invocable_by,
        invokes=invokes,
    )
    emit(data, as_json)
    return EXIT_OK if data.get("ok") else EXIT_ERROR
