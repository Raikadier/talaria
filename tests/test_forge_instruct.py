from __future__ import annotations

from talaria_cli.cmds.forge_build import build_profile_from_brief
from talaria_cli.cmds.forge_instruct import auto_instruct


def test_build_auto_instructs(tmp_path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge").mkdir(parents=True)
    data = build_profile_from_brief(
        tmp_path,
        "crea un agente tech lead",
        forge_id="tech-lead-test",
        role_kind="orchestrator",
    )
    assert data["ok"] is True
    assert data.get("instructed") is True
    doctrine = tmp_path / "memory/research/forge/tech-lead-test/00-doctrine.md"
    assert doctrine.is_file()
    text = doctrine.read_text(encoding="utf-8")
    assert "Cómo piensa" in text
    assert "(preguntas que se hace primero" not in text
    readme = (tmp_path / "memory/research/forge/tech-lead-test/README.md").read_text(
        encoding="utf-8"
    )
    assert "C1 Scope | yes" in readme


def test_instruct_known_seed(tmp_path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge" / "code-reviewer").mkdir(parents=True)
    (tmp_path / "_META/forge/profiles/code-reviewer.md").write_text(
        """---
forge_id: code-reviewer
status: draft
specialty: code review
corpus_path: memory/research/forge/code-reviewer
builder: 2.0
laws: [I, II]
amplifiers: [a, b, c]
---

# FORGE Profile — Code reviewer

## 2. Test Ley I / II
**DoD (Ley I):**
- [ ] a
- [ ] b
- [ ] c

## 4. Quality gates
| G1 Frame | x | y |
| G2 Retrieve | x | y |
| G3 Deliverable | x | y |

```text
FORGE profile=code-reviewer | laws=I+II
```
""",
        encoding="utf-8",
    )
    out = auto_instruct(tmp_path, "code-reviewer", specialty="code review")
    assert out["ok"] is True
    assert out["seed"] == "code-reviewer"
    assert out["sources_count"] >= 5
    src = (tmp_path / "memory/research/forge/code-reviewer/05-sources.md").read_text(
        encoding="utf-8"
    )
    assert "S1" in src
