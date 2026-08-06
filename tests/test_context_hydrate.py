from __future__ import annotations

import json

from talaria_cli.cmds.context_hydrate import (
    build_activation_context,
    hydrate_skill_body,
    list_packs,
    load_pack,
    memory_retrieve,
)
from talaria_cli.cmds.forge import evaluate_deliverable, load_profile, run_check
from talaria_cli.util import EXIT_ERROR, EXIT_OK


def _mk_skill(vault, rel: str, body: str = "# Skill\n\ndo the thing\n") -> None:
    path = vault / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {path.stem}\n---\n{body}",
        encoding="utf-8",
    )


def test_pack_load_and_list(tmp_path):
    packs = tmp_path / "_META" / "axon" / "packs"
    packs.mkdir(parents=True)
    (packs / "demo.json").write_text(
        json.dumps(
            {
                "id": "demo",
                "title": "Demo",
                "mission": "test",
                "queries": ["api"],
                "skills": ["skills/eng/demo-skill.md"],
            }
        ),
        encoding="utf-8",
    )
    _mk_skill(tmp_path, "skills/eng/demo-skill.md")
    pack = load_pack(tmp_path, "demo")
    assert pack and pack["id"] == "demo"
    listed = list_packs(tmp_path)
    assert any(p["id"] == "demo" for p in listed)


def test_hydrate_and_memory(tmp_path):
    _mk_skill(tmp_path, "skills/eng/demo-skill.md", "Use FastAPI routers.\n")
    mem = tmp_path / "memory" / "notes"
    mem.mkdir(parents=True)
    (mem / "fastapi-adr.md").write_text(
        "# FastAPI ADR\n\nPrefer routers and pytest.\n",
        encoding="utf-8",
    )
    body = hydrate_skill_body(tmp_path, "skills/eng/demo-skill.md")
    assert body["ok"] is True
    assert "FastAPI" in body["body"]

    hits = memory_retrieve(tmp_path, "fastapi pytest", limit=5)
    assert hits["hit_count"] >= 1
    assert any("fastapi" in h["path"].lower() for h in hits["hits"])


def test_activation_context_with_pack(tmp_path):
    packs = tmp_path / "_META" / "axon" / "packs"
    packs.mkdir(parents=True)
    (packs / "software-delivery.json").write_text(
        json.dumps(
            {
                "id": "software-delivery",
                "title": "SD",
                "mission": "ship",
                "skills": ["skills/eng/pinned.md"],
                "queries": [],
            }
        ),
        encoding="utf-8",
    )
    _mk_skill(tmp_path, "skills/eng/pinned.md", "Pinned body.\n")
    (tmp_path / "memory").mkdir()
    ctx = build_activation_context(
        tmp_path,
        "tech-lead",
        specialty="ship features",
        pack_id="software-delivery",
        hydrate=True,
        with_memory=True,
        skill_limit=3,
    )
    assert ctx["ok"]
    assert ctx["pack"]["id"] == "software-delivery"
    assert any(s.get("path") == "skills/eng/pinned.md" for s in ctx["skills_hydrated"])
    assert "skills/eng/pinned.md" in ctx["skill_ids_loaded"]


def test_gaxon_require_axon(tmp_path):
    profiles = tmp_path / "_META" / "forge" / "profiles"
    profiles.mkdir(parents=True)
    (profiles / "tl.md").write_text(
        """---
forge_id: tl
status: draft
specialty: test
laws: [I, II]
amplifiers: [especializacion, evidencia, verificacion]
require_axon: true
---

# Profile

## Gates
| Gate | evidence | if fail |
|---|---|---|
| G1 Scope | e | f |
| G2 Evidence | e | f |
| G3 Tools | e | f |
| Gcrit Critica | e | f |
| Gmem Memory | e | f |

## Definition of Done
- [ ] item one
- [ ] item two
- [ ] item three

## Activation
FORGE profile=tl
""",
        encoding="utf-8",
    )
    profile = load_profile(tmp_path, "tl")
    assert profile

    bad = tmp_path / "bad.md"
    bad.write_text(
        """---
forge_profile: tl
forge_gates: {G1: pass, G2: pass, G3: pass, Gcrit: pass, Gmem: pass}
---

# no skills
""",
        encoding="utf-8",
    )
    result = evaluate_deliverable(profile, bad, require_axon=True)
    assert result["ok"] is False
    assert any(c["name"] == "gate_Gaxon" and not c["ok"] for c in result["checks"])

    good = tmp_path / "good.md"
    good.write_text(
        """---
forge_profile: tl
forge_gates: {G1: pass, G2: pass, G3: pass, Gcrit: pass, Gmem: pass}
axon_skills:
  - skills/eng/pinned.md
---

# ok
crítica
memory/x
""",
        encoding="utf-8",
    )
    result2 = evaluate_deliverable(profile, good, require_axon=True)
    assert result2["ok"] is True
    assert "skills/eng/pinned.md" in result2["axon_skills_cited"]

    code = run_check(
        tmp_path, "tl", deliverable=str(good), require_axon=True, as_json=True
    )
    assert code == EXIT_OK
    code_bad = run_check(
        tmp_path, "tl", deliverable=str(bad), require_axon=True, as_json=True
    )
    assert code_bad == EXIT_ERROR
