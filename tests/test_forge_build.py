from __future__ import annotations

from pathlib import Path

from talaria_cli.cmds.forge_build import build_profile_from_brief, slugify_id


def test_slugify_email_brief():
    assert "responder" in slugify_id("crea un agente que sepa responder correos usando talaria")
    assert "correos" in slugify_id("crea un agente que sepa responder correos usando talaria")


def test_forge_build_creates_draft(tmp_path: Path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge").mkdir(parents=True)

    data = build_profile_from_brief(
        tmp_path,
        "crea un agente que sepa responder correos usando talaria",
        forge_id="email-responder-test",
    )
    assert data["ok"] is True
    assert data["forge_id"] == "email-responder-test"
    assert data["status"] == "draft"
    assert data["pilot_playbook"]
    profile = tmp_path / "_META/forge/profiles/email-responder-test.md"
    doctrine = tmp_path / "memory/research/forge/email-responder-test/00-doctrine.md"
    assert profile.is_file()
    assert doctrine.is_file()
    text = profile.read_text(encoding="utf-8")
    assert "status: draft" in text
    assert "builder: 2.0" in text


def test_forge_build_no_overwrite_without_force(tmp_path: Path):
    (tmp_path / "_META" / "forge" / "profiles").mkdir(parents=True)
    (tmp_path / "memory" / "research" / "forge").mkdir(parents=True)
    first = build_profile_from_brief(
        tmp_path, "agente de prueba alpha", forge_id="alpha-agent"
    )
    assert first["ok"] is True
    second = build_profile_from_brief(
        tmp_path, "agente de prueba alpha", forge_id="alpha-agent"
    )
    # without force, unique id suffix
    assert second["ok"] is True
    assert second["forge_id"] == "alpha-agent-2"

    blocked = build_profile_from_brief(
        tmp_path,
        "overwrite attempt",
        forge_id="alpha-agent",
        force=False,
    )
    # ensure_unique still yields -3
    assert blocked["ok"] is True
    assert blocked["forge_id"] == "alpha-agent-3"

    overwrite = build_profile_from_brief(
        tmp_path,
        "overwrite attempt",
        forge_id="alpha-agent",
        force=True,
    )
    assert overwrite["ok"] is True
    assert overwrite["forge_id"] == "alpha-agent"
