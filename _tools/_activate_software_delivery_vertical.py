"""Activate software-delivery vertical (8 agents) + write ensemble."""
from __future__ import annotations

import re
from pathlib import Path

from talaria_cli.cmds.forge import evaluate_profile_structure, load_profile, profiles_root
from talaria_cli.vault import find_vault

VERTICAL = [
    "product-manager",
    "software-architect",
    "tech-lead",
    "backend-developer",
    "frontend-developer",
    "code-reviewer",
    "qa-engineer",
    "devops-sre",
]


def _set_status(path: Path, status: str = "active") -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return
    parts = text.split("---", 2)
    fm, body = parts[1], parts[2] if len(parts) > 2 else ""
    if re.search(r"(?m)^status:\s*", fm):
        fm = re.sub(r"(?m)^status:\s*.*$", f"status: {status}", fm)
    else:
        fm = fm.rstrip() + f"\nstatus: {status}\n"
    if "vertical:" not in fm:
        fm = fm.rstrip() + "\nvertical: software-delivery\n"
    path.write_text(f"---{fm}---{body}", encoding="utf-8")


def main() -> int:
    vault = find_vault()
    results = []
    for fid in VERTICAL:
        p = profiles_root(vault) / f"{fid}.md"
        if not p.is_file():
            results.append({"forge_id": fid, "ok": False, "error": "missing"})
            continue
        _set_status(p, "active")
        corpus_readme = vault / "memory" / "research" / "forge" / fid / "README.md"
        if corpus_readme.is_file():
            _set_status(corpus_readme, "active")
        prof = load_profile(vault, fid)
        struct = evaluate_profile_structure(prof, vault) if prof else {"ok": False}
        results.append(
            {
                "forge_id": fid,
                "ok": bool(struct.get("ok")),
                "structure_ok": bool(struct.get("ok")),
                "status": "active",
            }
        )

    ens = vault / "_META" / "forge" / "ensembles" / "software-delivery.md"
    ens.write_text(
        """---
tags: [forge, ensemble, software, user-owned]
aliases: [forge-ensemble-software-delivery, software-delivery]
forge_id: software-delivery
forge_version: 1.0
status: active
laws: [I, II]
profiles:
  - product-manager
  - software-architect
  - tech-lead
  - backend-developer
  - frontend-developer
  - code-reviewer
  - qa-engineer
  - devops-sre
vertical: software-delivery
eval: software-delivery-v1
---

# FORGE Ensemble — Software Delivery (vertical calibrado)

Objetivo: entregar una feature E2E con handoffs por **artefacto obligatorio**.  
No es el organigrama canónico de Talaria: es un vertical **user-owned** calibrado para medición Ley II.

## Secuencia

```
product-manager
      │  product brief
      ▼
software-architect
      │  ADR + boundaries
      ▼
tech-lead
      │  tech plan / slices
      ├──────────────┬──────────────┐
      ▼              ▼              ▼
backend-dev    frontend-dev    devops-sre
      │              │              │
      └──────► code-reviewer ◄──────┘
                    │
                    ▼
               qa-engineer
                    │
                    ▼
            release notes / verify
```

## Contratos (artefacto obligatorio)

| De → A | Artefacto | Comando |
|--------|-----------|---------|
| PM → Architect | Product brief | `forge invoke product-manager software-architect --deliverable … --require-deliverable` |
| Architect → Tech Lead | ADR + boundaries | idem |
| Tech Lead → Backend/Frontend/DevOps | Task pack | idem |
| * → Code Reviewer | Diff summary + riesgos | idem |
| * → QA | Test plan / reporte | idem |

Sin `--deliverable` + `--require-deliverable`, el handoff **no cierra**.

## DoD del conjunto

- [ ] Brief de producto con outcomes  
- [ ] ADR aceptado  
- [ ] Plan técnico con slices  
- [ ] Impl backend + frontend (o justificación N/A)  
- [ ] Review con riesgos  
- [ ] QA plan/reporte  
- [ ] Notas de release/ops  
- [ ] Memorize en vault + scorecard  

## Activación

```text
FORGE ensemble=software-delivery | laws=I+II | spine=on
start_role=product-manager
eval=software-delivery-v1
```

```bash
talaria eval run software-delivery-v1 --ab --json
```

Perfiles del vertical: todos `status: active` con corpus auto-instruct + calibración vertical.
""",
        encoding="utf-8",
    )

    # catalog patch
    catalog = vault / "_META" / "forge" / "catalog.md"
    if catalog.is_file():
        t = catalog.read_text(encoding="utf-8")
        if "software-delivery" not in t:
            t = t.rstrip() + (
                "\n\n## Ensembles — vertical calibrado\n\n"
                "| ID | Nota |\n|----|------|\n"
                "| `software-delivery` | [[forge-ensemble-software-delivery]] — 8 agentes active + eval `software-delivery-v1` |\n"
            )
            catalog.write_text(t, encoding="utf-8")

    ok = all(r.get("ok") for r in results)
    print({"ok": ok, "activated": results, "ensemble": "software-delivery"})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
