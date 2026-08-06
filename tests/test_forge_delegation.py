from __future__ import annotations

from pathlib import Path

from talaria_cli.cmds.forge_build import build_profile_from_brief
from talaria_cli.cmds.forge_delegation import (
    build_delegation_graph,
    check_invoke_policy,
)


def _scaffold_pair(tmp: Path) -> None:
    (tmp / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp / "memory" / "research" / "forge").mkdir(parents=True)
    build_profile_from_brief(
        tmp,
        "orquestador demo",
        forge_id="orch-demo",
        role_kind="orchestrator",
        invokes=["spec-demo"],
    )
    build_profile_from_brief(
        tmp,
        "especialista demo",
        forge_id="spec-demo",
        role_kind="specialist",
        invocable_by_mode="allowlist",
        invocable_by=["orch-demo"],
    )


def test_delegation_graph_and_policy(tmp_path: Path):
    _scaffold_pair(tmp_path)
    g = build_delegation_graph(tmp_path)
    assert g["ok"] is True
    assert g["node_count"] >= 2
    kinds = {e["kind"] for e in g["edges"]}
    assert "invokes" in kinds or "may_invoke" in kinds

    ok = check_invoke_policy(tmp_path, "orch-demo", "spec-demo", strict=True)
    assert ok["allowed"] is True

    bad = check_invoke_policy(tmp_path, "unknown-parent", "spec-demo", strict=True)
    assert bad["allowed"] is False


def test_build_with_delegation_fields(tmp_path: Path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge").mkdir(parents=True)
    data = build_profile_from_brief(
        tmp_path,
        "logo designer",
        forge_id="logo-designer",
        role_kind="specialist",
        invocable_by_mode="allowlist",
        invocable_by="ui-ux,sw-orch",
        invokes="",
    )
    assert data["ok"] is True
    assert data["role_kind"] == "specialist"
    assert data["invocable_by"] == ["ui-ux", "sw-orch"]
    text = (tmp_path / "_META/forge/profiles/logo-designer.md").read_text(encoding="utf-8")
    assert "role_kind: specialist" in text
    assert "invocable_by_mode: allowlist" in text
