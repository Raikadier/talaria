"""SPINE session — start/status/close with mandatory scorecard (enforcement)."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from talaria_cli.cmds import verify as verify_cmd
from talaria_cli.mode import mode_contract, resolve_mode
from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

SESSION_FILE = ".talaria.session.json"


def session_path(vault: Path) -> Path:
    return vault / SESSION_FILE


def load_session(vault: Path) -> dict[str, Any] | None:
    p = session_path(vault)
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def clear_session(vault: Path) -> None:
    p = session_path(vault)
    if p.is_file():
        p.unlink()


def start_session(
    vault: Path,
    *,
    objective: str,
    forge_profile: str | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Create scorecard stub + persist active session marker."""
    m = resolve_mode(vault, mode)
    today = date.today().isoformat()
    slug = (forge_profile or "general").replace("/", "-")
    rel = f"memory/conversations/{today}-session-{slug}.md"
    path = vault / rel
    path.parent.mkdir(parents=True, exist_ok=True)

    organs = ["spine", "memory"]
    if forge_profile:
        organs.append("forge")
    organs_yaml = "[" + ", ".join(organs) + "]"

    fm = f"""---
date: {today}
type: scorecard
tags: [scorecard, spine, verify, session]
status: open
mode: {m}
objective: {json.dumps(objective, ensure_ascii=False)}
organs_used: {organs_yaml}
evidence: []
gates: n/a
forge_profile: {forge_profile or ""}
forge_builder: {"2.0" if forge_profile else ""}
forge_critical: ""
forge_learned: false
forge_memorize: []
delta_vs_generic: []
done: false
projects: []
---

# Scorecard de sesión — {today}

## Objetivo
{objective}

## Partitura SPINE
1. Verify boot (si mode=strict)
2. Retrieve (vault / AXON / corpus FORGE)
3. Act (playbook del perfil si aplica)
4. Memorize evidencia (wiki-links)
5. Crítica (si FORGE) → `forge_critical: pass`
6. Verify close — este scorecard

## Evidencia
- 

## Gates
| Gate | Resultado |
|------|-----------|
| Memorize | |
| FORGE crítica | {"required" if forge_profile else "n/a"} |
| FORGE resto | {"required" if forge_profile else "n/a"} |

## Delta vs chat genérico
1.

## Cierre
- [ ] `done: true` cuando verify close deba pasar en strict
"""
    path.write_text(fm, encoding="utf-8")

    sess = {
        "started": today,
        "objective": objective,
        "forge_profile": forge_profile or "",
        "mode": m,
        "scorecard": rel,
        "partitura": [
            "verify boot",
            "retrieve",
            "act",
            "memorize",
            "critique" if forge_profile else None,
            "verify close",
        ],
    }
    sess["partitura"] = [x for x in sess["partitura"] if x]
    session_path(vault).write_text(json.dumps(sess, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "command": "session start",
        "ok": True,
        "session": sess,
        "mode_contract": mode_contract(m),
        "next": [
            f"Edit scorecard: {rel}",
            "talaria verify boot --json" if m == "strict" else "draft mode — boot soft",
            f"talaria forge run {forge_profile} --json" if forge_profile else "Act without FORGE or pick a profile",
            "talaria session close --json  # runs verify close on this scorecard",
        ],
    }


def status_session(vault: Path) -> dict[str, Any]:
    sess = load_session(vault)
    m = resolve_mode(vault)
    if not sess:
        return {
            "command": "session status",
            "ok": True,
            "active": False,
            "mode": m,
            "mode_contract": mode_contract(m),
            "hint": "talaria session start --objective \"...\" [--forge sw-architect]",
        }
    sc = vault / sess.get("scorecard", "")
    return {
        "command": "session status",
        "ok": True,
        "active": True,
        "session": sess,
        "scorecard_exists": sc.is_file(),
        "mode": m,
        "mode_contract": mode_contract(m),
    }


def close_session(vault: Path, *, as_json: bool = False, allow_draft: bool = False) -> int:
    sess = load_session(vault)
    if not sess:
        emit(
            {
                "command": "session close",
                "ok": False,
                "error": "no active session — run session start first",
            },
            as_json or True,
        )
        return EXIT_ERROR
    sc = sess.get("scorecard")
    if not sc:
        emit({"command": "session close", "ok": False, "error": "session missing scorecard"}, as_json or True)
        return EXIT_ERROR
    mode = resolve_mode(vault)
    allow = allow_draft or mode == "draft"
    data = verify_cmd.evaluate_close(vault, sc, allow_draft=allow)
    data["command"] = "session close"
    data["session"] = sess
    if data.get("ok"):
        clear_session(vault)
        data["session_cleared"] = True
        data["next"] = "Session closed; marker .talaria.session.json removed"
    else:
        data["session_cleared"] = False
        data["next"] = "Fix scorecard (forge_critical/done/evidence) then session close again"
    verify_cmd._emit_verify(data, as_json)
    return EXIT_OK if data.get("ok") else EXIT_ERROR


def run_start(
    vault: Path,
    *,
    objective: str,
    forge_profile: str | None = None,
    as_json: bool = False,
) -> int:
    if not (objective or "").strip():
        emit({"ok": False, "error": "objective required"}, as_json or True)
        return EXIT_USAGE
    data = start_session(vault, objective=objective.strip(), forge_profile=forge_profile)
    emit(data, as_json or True)
    return EXIT_OK


def run_status(vault: Path, *, as_json: bool = False) -> int:
    data = status_session(vault)
    emit(data, as_json or True)
    return EXIT_OK
