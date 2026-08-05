"""SPINE mode (strict|draft) — Phase F."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

MODES = ("strict", "draft")


def resolve_mode(vault: Path, explicit: str | None = None) -> str:
    if explicit:
        m = explicit.strip().lower()
        return m if m in MODES else "strict"
    env = (os.environ.get("TALARIA_MODE") or "").strip().lower()
    if env in MODES:
        return env
    marker = vault / ".talaria.mode"
    if marker.is_file():
        m = marker.read_text(encoding="utf-8").strip().lower()
        if m in MODES:
            return m
    legacy = vault / ".skillgraph.mode"
    if legacy.is_file():
        m = legacy.read_text(encoding="utf-8").strip().lower()
        if m in MODES:
            return m
    return "strict"


def mode_contract(mode: str) -> dict[str, Any]:
    if mode == "draft":
        return {
            "mode": "draft",
            "verify_boot_required": False,
            "verify_close_done_required": False,
            "forge_gates_required": False,
            "promise": "Exploración permitida; no declarar resultado FORGE/garantizado",
        }
    return {
        "mode": "strict",
        "verify_boot_required": True,
        "verify_close_done_required": True,
        "forge_gates_required": True,
        "promise": "Resultado garantizado solo si verify+forge check pasan",
    }
