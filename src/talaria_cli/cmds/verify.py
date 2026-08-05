"""Organism health + SPINE verify gates (boot / close)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from talaria_cli.cmds import status as status_cmd
from talaria_cli.util import EXIT_ERROR, EXIT_OK, emit

REQUIRED_FILES = [
    "Home.md",
    "AGENTS.md",
    "_META/organism.md",
    "_META/architecture.md",
    "_META/spine-framework.md",
    "_META/axon.md",
    "_META/forge/forge.md",
    "_META/forge/two-laws.md",
    "_META/forge/catalog.md",
    "_templates/scorecard.md",
]

REQUIRED_DIRS = [
    "memory",
    "memory/conversations",
    "memory/decisions",
    "memory/projects",
    "skills",
    "src/talaria_cli",
    "_META/forge/profiles",
    "tools",
    "scripts",
]

ORGAN_FILES = {
    "memory": "memory",
    "axon": "_META/axon.md",
    "forge": "_META/forge/forge.md",
    "spine": "_META/spine-framework.md",
    "api": "src/talaria_cli/cli.py",
    "tools": "tools",
    "adapters": "_META/adapters/pilots.md",
}


def organism_checks(vault: Path) -> dict[str, Any]:
    missing_files = [p for p in REQUIRED_FILES if not (vault / p).is_file()]
    missing_dirs = [p for p in REQUIRED_DIRS if not (vault / p).is_dir()]
    organs = {}
    for name, rel in ORGAN_FILES.items():
        path = vault / rel
        organs[name] = path.is_file() or path.is_dir()

    skills_n = 0
    skills_root = vault / "skills"
    if skills_root.is_dir():
        skills_n = sum(1 for _ in skills_root.rglob("*.md"))

    profiles_dir = vault / "_META/forge/profiles"
    profiles = list(profiles_dir.glob("*.md")) if profiles_dir.is_dir() else []

    ok = not missing_files and not missing_dirs and all(organs.values()) and skills_n > 0
    return {
        "ok": ok,
        "missing_files": missing_files,
        "missing_dirs": missing_dirs,
        "organs": organs,
        "skills_md_count": skills_n,
        "forge_profiles": [p.stem for p in profiles],
    }


def run_doctor(vault: Path, *, as_json: bool = False) -> int:
    """Tools presence (status) + organism structure."""
    org = organism_checks(vault)
    st = status_cmd.get_status(vault)
    tools_ok = bool(st.get("ok"))
    data = {
        "command": "doctor",
        "vault": str(vault),
        "tools_ok": tools_ok,
        "organism_ok": org["ok"],
        "organism": org,
        "status": st,
        "ok": tools_ok and org["ok"],
        "framework": "SPINE",
        "hint": "If tools_ok is false: talaria boot",
    }
    if as_json:
        emit(data, True)
    else:
        print(f"Vault:     {vault}")
        print(f"Tools:     {'OK' if tools_ok else 'FAIL'} (markitdown/graphify/obsidian-mcp)")
        print(f"Organism:  {'OK' if org['ok'] else 'FAIL'}")
        if org["missing_files"]:
            print("  missing files:", ", ".join(org["missing_files"]))
        if org["missing_dirs"]:
            print("  missing dirs:", ", ".join(org["missing_dirs"]))
        print(f"AXON md:   {org['skills_md_count']}")
        print(f"FORGE:     {', '.join(org['forge_profiles']) or '(none)'}")
        print(f"Mark:      {st.get('mark')}")
        print(f"Overall:   {'PASS' if data['ok'] else 'FAIL'}")
    return EXIT_OK if data["ok"] else EXIT_ERROR


def evaluate_boot(vault: Path) -> dict[str, Any]:
    org = organism_checks(vault)
    st = status_cmd.get_status(vault)
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("organism_files", not org["missing_files"], ",".join(org["missing_files"]))
    add("organism_dirs", not org["missing_dirs"], ",".join(org["missing_dirs"]))
    add("organs_present", all(org["organs"].values()), str(org["organs"]))
    add("axon_nonempty", org["skills_md_count"] > 0, str(org["skills_md_count"]))
    add("forge_profiles", len(org["forge_profiles"]) >= 1, str(org["forge_profiles"]))
    add("mark_at_least_1", st.get("mark") not in (None, "Mk.0"), str(st.get("mark")))

    ok = all(c["ok"] for c in checks)
    return {
        "command": "verify boot",
        "gate": "entry",
        "ok": ok,
        "vault": str(vault),
        "mode": "strict",
        "checks": checks,
        "mark": st.get("mark"),
        "organism": org,
        "next": "Act allowed" if ok else "Run talaria boot / repair organism before serious Act",
    }


def run_verify_boot(vault: Path, *, as_json: bool = False) -> int:
    data = evaluate_boot(vault)
    _emit_verify(data, as_json)
    return EXIT_OK if data["ok"] else EXIT_ERROR


def evaluate_close(
    vault: Path,
    scorecard: str | Path,
    *,
    allow_draft: bool = False,
) -> dict[str, Any]:
    path = Path(scorecard)
    if not path.is_file():
        alt = vault / scorecard
        path = alt if alt.is_file() else path
    if not path.is_file():
        return {
            "command": "verify close",
            "gate": "exit",
            "ok": False,
            "error": f"scorecard not found: {scorecard}",
            "hint": "Copy _templates/scorecard.md and fill frontmatter",
            "checks": [],
        }

    text = path.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    objective = str(meta.get("objective") or "").strip()
    add("objective", bool(objective), objective[:80])

    organs = meta.get("organs_used") or []
    if isinstance(organs, str):
        organs = [organs]
    add("organs_used", len(organs) >= 1, str(organs))

    evidence = meta.get("evidence") or []
    if isinstance(evidence, str):
        evidence = [evidence]
    body_links = re.findall(r"\[\[[^\]]+\]\]", text)
    add("evidence", len(evidence) >= 1 or len(body_links) >= 1, str(evidence or body_links[:5]))

    gates = str(meta.get("gates") or "n/a").strip().lower()
    add("gates_not_fail", gates != "fail", gates)

    done = meta.get("done")
    if isinstance(done, str):
        done = done.strip().lower() in {"true", "yes", "1"}
    mode = str(meta.get("mode") or ("draft" if allow_draft else "strict")).lower()
    if allow_draft:
        mode = "draft"
    if mode == "draft":
        add("done_or_draft", True, "draft mode — done not required")
    else:
        add("done", bool(done), str(done))

    ok = all(c["ok"] for c in checks)
    return {
        "command": "verify close",
        "gate": "exit",
        "ok": ok,
        "vault": str(vault),
        "scorecard": str(path),
        "mode": mode,
        "checks": checks,
        "meta": {
            "objective": objective,
            "organs_used": organs,
            "gates": gates,
            "forge_profile": meta.get("forge_profile"),
            "done": bool(done),
        },
        "next": "Session may be declared done" if ok else "Fill scorecard / Memorize evidence / set done: true",
    }


def run_verify_close(
    vault: Path,
    scorecard: str | Path,
    *,
    allow_draft: bool = False,
    as_json: bool = False,
) -> int:
    data = evaluate_close(vault, scorecard, allow_draft=allow_draft)
    _emit_verify(data, as_json)
    return EXIT_OK if data["ok"] else EXIT_ERROR


def _emit_verify(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        emit(data, True)
        return
    print(f"{data.get('command')}: {'PASS' if data.get('ok') else 'FAIL'}")
    for c in data.get("checks") or []:
        mark = "OK" if c["ok"] else "X"
        detail = f" — {c['detail']}" if c.get("detail") else ""
        print(f"  [{mark}] {c['name']}{detail}")
    if data.get("error"):
        print("error:", data["error"])
    if data.get("next"):
        print("next:", data["next"])


def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    meta: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if current_list_key and line.startswith("  - "):
            meta.setdefault(current_list_key, []).append(line[4:].strip().strip("\"'"))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "" or val == "[]":
            if val == "[]":
                meta[key] = []
            else:
                current_list_key = key
                meta[key] = []
            continue
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            meta[key] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
        elif val.lower() in {"true", "false"}:
            meta[key] = val.lower() == "true"
        else:
            meta[key] = val.strip("\"'")
    return meta
