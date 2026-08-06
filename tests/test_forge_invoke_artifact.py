from __future__ import annotations

from talaria_cli.cmds.forge import run_invoke
from talaria_cli.cmds.forge_build import build_profile_from_brief
from talaria_cli.util import EXIT_OK


def test_invoke_require_deliverable(tmp_path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge").mkdir(parents=True)
    build_profile_from_brief(
        tmp_path, "parent orch", forge_id="p-orch", role_kind="orchestrator", invokes=["c-spec"]
    )
    build_profile_from_brief(
        tmp_path,
        "child spec",
        forge_id="c-spec",
        role_kind="specialist",
        invocable_by=["p-orch"],
    )
    code = run_invoke(
        tmp_path, "p-orch", "c-spec", require_deliverable=True, as_json=True
    )
    assert code != EXIT_OK

    deliv = tmp_path / "d.md"
    deliv.write_text(
        """---
forge_profile: c-spec
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
---

# ok
crítica
memory/x
""",
        encoding="utf-8",
    )
    code2 = run_invoke(
        tmp_path,
        "p-orch",
        "c-spec",
        deliverable=str(deliv),
        require_deliverable=True,
        as_json=True,
    )
    assert code2 == EXIT_OK
