"""FORGE organ — list / show / check / run profiles (Phase C)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from skillgraph_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

PROFILES_DIR = Path("_META/forge/profiles")
ENSEMBLES_DIR = Path("_META/forge/ensembles")


def profiles_root(vault: Path) -> Path:
    return vault / PROFILES_DIR


def ensembles_root(vault: Path) -> Path:
    return vault / ENSEMBLES_DIR


def list_profiles(vault: Path) -> list[dict[str, Any]]:
    root = profiles_root(vault)
    if not root.is_dir():
        return []
    out = []
    for path in sorted(root.glob("*.md")):
        meta, body = _read_md(path)
        gates = _parse_gates(body)
        dod = _parse_dod(body)
        out.append(
            {
                "forge_id": meta.get("forge_id") or path.stem,
                "path": str(path.relative_to(vault)).replace("\\", "/"),
                "status": meta.get("status", "unknown"),
                "specialty": meta.get("specialty", ""),
                "version": meta.get("forge_version", ""),
                "laws": meta.get("laws") or [],
                "amplifiers": meta.get("amplifiers") or [],
                "ensemble_roles": meta.get("ensemble_roles") or [],
                "gates": [g["id"] for g in gates],
                "dod_count": len(dod),
                "axon_queries": meta.get("axon_queries") or [],
            }
        )
    return out


def list_ensembles(vault: Path) -> list[dict[str, Any]]:
    root = ensembles_root(vault)
    if not root.is_dir():
        return []
    out = []
    for path in sorted(root.glob("*.md")):
        meta, _body = _read_md(path)
        out.append(
            {
                "forge_id": meta.get("forge_id") or path.stem,
                "path": str(path.relative_to(vault)).replace("\\", "/"),
                "status": meta.get("status", "unknown"),
                "profiles": meta.get("profiles") or [],
                "laws": meta.get("laws") or [],
            }
        )
    return out


def load_profile(vault: Path, forge_id: str) -> dict[str, Any] | None:
    path = profiles_root(vault) / f"{forge_id}.md"
    if not path.is_file():
        # try match forge_id in frontmatter
        for p in profiles_root(vault).glob("*.md"):
            meta, body = _read_md(p)
            if meta.get("forge_id") == forge_id:
                path = p
                break
        else:
            return None
    meta, body = _read_md(path)
    gates = _parse_gates(body)
    dod = _parse_dod(body)
    activation = _parse_activation(body)
    return {
        "forge_id": meta.get("forge_id") or path.stem,
        "path": str(path),
        "rel_path": str(path.relative_to(vault)).replace("\\", "/"),
        "meta": meta,
        "gates": gates,
        "dod": dod,
        "activation": activation,
        "body_chars": len(body),
    }


def evaluate_profile_structure(profile: dict[str, Any]) -> dict[str, Any]:
    """Ley I/II structural checks on the profile note itself."""
    meta = profile.get("meta") or {}
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("forge_id", bool(meta.get("forge_id")), str(meta.get("forge_id")))
    add("status_active_or_draft", str(meta.get("status", "")).lower() in {"active", "draft"}, str(meta.get("status")))
    add("specialty", bool(str(meta.get("specialty") or "").strip()), str(meta.get("specialty", ""))[:80])
    laws = meta.get("laws") or []
    if isinstance(laws, str):
        laws = [laws]
    laws_norm = [str(x).upper().replace("LEY ", "").strip() for x in laws]
    add("laws_I_II", "I" in laws_norm and "II" in laws_norm, str(laws))
    amps = meta.get("amplifiers") or []
    if isinstance(amps, str):
        amps = [amps]
    add("amplifiers_ge_3", len(amps) >= 3, str(amps))
    gates = profile.get("gates") or []
    add("gates_ge_3", len(gates) >= 3, str([g["id"] for g in gates]))
    dod = profile.get("dod") or []
    add("dod_ge_3", len(dod) >= 3, str(len(dod)))
    add("activation_present", bool(profile.get("activation")), (profile.get("activation") or "")[:60])

    ok = all(c["ok"] for c in checks)
    return {
        "kind": "profile_structure",
        "forge_id": profile.get("forge_id"),
        "ok": ok,
        "checks": checks,
        "gates": gates,
        "dod": dod,
    }


def evaluate_deliverable(
    profile: dict[str, Any],
    deliverable: Path,
    *,
    declare: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Check deliverable against profile gates (frontmatter forge_gates or --declare)."""
    text = deliverable.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    declared = dict(declare or {})
    fm_gates = meta.get("forge_gates") or {}
    if isinstance(fm_gates, dict):
        for k, v in fm_gates.items():
            declared.setdefault(str(k), str(v).lower())
    # body lines like: G1: pass
    for m in re.finditer(r"^\s*(G\d+)\s*[=:]\s*(pass|fail|n/a)\s*$", body, re.I | re.M):
        declared.setdefault(m.group(1).upper(), m.group(2).lower())

    checks: list[dict[str, Any]] = []
    profile_id = profile.get("forge_id")
    fm_profile = str(meta.get("forge_profile") or "").strip()
    checks.append(
        {
            "name": "forge_profile_match",
            "ok": not fm_profile or fm_profile == profile_id,
            "detail": f"frontmatter={fm_profile or '(none)'} expected={profile_id}",
        }
    )

    for g in profile.get("gates") or []:
        gid = g["id"]
        val = str(declared.get(gid, "")).lower().strip()
        ok = val == "pass"
        checks.append(
            {
                "name": f"gate_{gid}",
                "ok": ok,
                "detail": val or "missing (declare pass/fail)",
                "evidence_required": g.get("evidence", ""),
            }
        )

    # optional DoD checkboxes in deliverable
    dod_done = _parse_dod(body)
    if dod_done:
        done_n = sum(1 for d in dod_done if d.get("done"))
        checks.append(
            {
                "name": "deliverable_dod_progress",
                "ok": done_n == len(dod_done) and len(dod_done) > 0,
                "detail": f"{done_n}/{len(dod_done)} checked",
            }
        )

    ok = all(c["ok"] for c in checks)
    return {
        "kind": "deliverable_gates",
        "forge_id": profile_id,
        "deliverable": str(deliverable),
        "ok": ok,
        "declared_gates": declared,
        "checks": checks,
        "next": "FORGE done allowed" if ok else "Mark remaining gates pass in deliverable or --declare",
    }


def run_list(vault: Path, *, ensembles: bool = False, as_json: bool = False) -> int:
    profiles = list_profiles(vault)
    data: dict[str, Any] = {
        "command": "forge list",
        "ok": True,
        "count": len(profiles),
        "profiles": profiles,
    }
    if ensembles:
        data["ensembles"] = list_ensembles(vault)
    if as_json:
        emit(data, True)
    else:
        print(f"FORGE profiles: {len(profiles)}")
        for p in profiles:
            print(f"  - {p['forge_id']:16} [{p['status']}] gates={','.join(p['gates']) or '-'}  {p['specialty'][:60]}")
        if ensembles:
            print(f"Ensembles: {len(data['ensembles'])}")
            for e in data["ensembles"]:
                print(f"  - {e['forge_id']}: {e['profiles']}")
    return EXIT_OK


def run_show(vault: Path, forge_id: str, *, as_json: bool = False) -> int:
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR
    struct = evaluate_profile_structure(profile)
    data = {
        "command": "forge show",
        "ok": True,
        "profile": {
            "forge_id": profile["forge_id"],
            "path": profile["rel_path"],
            "meta": profile["meta"],
            "gates": profile["gates"],
            "dod": profile["dod"],
            "activation": profile["activation"],
        },
        "structure": struct,
    }
    if as_json:
        emit(data, True)
    else:
        m = profile["meta"]
        print(f"FORGE profile: {profile['forge_id']} ({m.get('status')})")
        print(f"  specialty: {m.get('specialty')}")
        print(f"  path: {profile['rel_path']}")
        print(f"  amplifiers: {m.get('amplifiers')}")
        print("  gates:")
        for g in profile["gates"]:
            print(f"    {g['id']}: {g.get('evidence', '')}")
        print(f"  DoD items: {len(profile['dod'])}")
        aq = m.get("axon_queries") or []
        if aq:
            print(f"  axon_queries: {aq}")
        if profile["activation"]:
            print("  activation:")
            print(f"    {profile['activation']}")
        print(f"  structure: {'PASS' if struct['ok'] else 'FAIL'}")
    return EXIT_OK


def run_check(
    vault: Path,
    forge_id: str,
    *,
    deliverable: str | None = None,
    declare: str | None = None,
    as_json: bool = False,
) -> int:
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR

    struct = evaluate_profile_structure(profile)
    parts = [struct]
    overall_ok = struct["ok"]

    if deliverable:
        path = Path(deliverable)
        if not path.is_file():
            path = vault / deliverable
        if not path.is_file():
            emit({"error": f"deliverable not found: {deliverable}", "ok": False}, as_json or True)
            return EXIT_ERROR
        declared = _parse_declare(declare) if declare else {}
        deliv = evaluate_deliverable(profile, path, declare=declared)
        parts.append(deliv)
        overall_ok = overall_ok and deliv["ok"]
    elif declare:
        import tempfile

        declared = _parse_declare(declare)
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(f"---\nforge_profile: {forge_id}\n---\n")
            for k, v in declared.items():
                f.write(f"{k}: {v}\n")
            tmp = Path(f.name)
        try:
            deliv = evaluate_deliverable(profile, tmp, declare=declared)
        finally:
            tmp.unlink(missing_ok=True)
        parts.append(deliv)
        overall_ok = overall_ok and deliv["ok"]

    data = {
        "command": "forge check",
        "forge_id": forge_id,
        "ok": overall_ok,
        "results": parts,
        "next": "Gates satisfied" if overall_ok else "Fix failing checks before declaring FORGE done",
    }
    if as_json:
        emit(data, True)
    else:
        print(f"forge check {forge_id}: {'PASS' if overall_ok else 'FAIL'}")
        for part in parts:
            print(f"  [{part['kind']}] {'PASS' if part['ok'] else 'FAIL'}")
            for c in part.get("checks") or []:
                print(f"    [{'OK' if c['ok'] else 'X'}] {c['name']}" + (f" — {c['detail']}" if c.get("detail") else ""))
        print("next:", data["next"])
    return EXIT_OK if overall_ok else EXIT_ERROR


def run_run(vault: Path, forge_id: str, *, with_axon: bool = False, as_json: bool = False) -> int:
    """Emit playbook packet for an agent to execute the profile."""
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR
    struct = evaluate_profile_structure(profile)
    if not struct["ok"]:
        data = {
            "command": "forge run",
            "ok": False,
            "error": "profile fails structural check; fix profile before run",
            "structure": struct,
        }
        emit(data, as_json or True)
        return EXIT_ERROR

    meta = profile.get("meta") or {}
    axon_queries = meta.get("axon_queries") or []
    if isinstance(axon_queries, str):
        axon_queries = [axon_queries]

    packet = {
        "command": "forge run",
        "ok": True,
        "forge_id": forge_id,
        "activation": profile.get("activation")
        or f"FORGE profile={forge_id} | laws=I+II | spine=on",
        "gates": profile["gates"],
        "dod": profile["dod"],
        "specialty": meta.get("specialty"),
        "path": profile["rel_path"],
        "axon_queries": axon_queries,
        "instructions": [
            "Activate with the activation string",
            "Retrieve via: skillgraph axon for-profile <id> --json (or axon search)",
            "Execute profile playbook in the profile note",
            "Write deliverable with forge_profile + forge_gates frontmatter (G1: pass, ...)",
            "Run: skillgraph forge check --profile <id> --deliverable <path> --json",
            "Then skillgraph verify close --scorecard <scorecard> --json",
        ],
    }
    if with_axon:
        from skillgraph_cli.cmds import axon as axon_cmd

        queries = list(axon_queries) if axon_queries else [str(meta.get("specialty") or forge_id)[:60]]
        packet["axon"] = axon_cmd.bundles_for_queries(vault, queries, limit=8)

    if as_json:
        emit(packet, True)
    else:
        print(packet["activation"])
        print("gates:", ", ".join(g["id"] for g in packet["gates"]))
        print("DoD:", len(packet["dod"]), "items — see", packet["path"])
        if axon_queries:
            print("axon_queries:", axon_queries)
        for i, step in enumerate(packet["instructions"], 1):
            print(f"  {i}. {step}")
        if with_axon and packet.get("axon"):
            for b in packet["axon"]:
                print(f"  AXON {b['query']!r}: {b['result'].get('hit_count', 0)} hits")
    return EXIT_OK


def _parse_declare(s: str | None) -> dict[str, str]:
    if not s:
        return {}
    out: dict[str, str] = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
        elif ":" in part:
            k, v = part.split(":", 1)
        else:
            continue
        out[k.strip().upper()] = v.strip().lower()
    return out


def _read_md(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    return _split_frontmatter(text)


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return _parse_yaml_lite(parts[1]), parts[2]


def _parse_yaml_lite(block: str) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if current_list_key and (line.startswith("  - ") or line.startswith("- ")):
            item = line.lstrip().removeprefix("- ").strip().strip("\"'")
            meta.setdefault(current_list_key, []).append(item)
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "" or val == "[]":
            meta[key] = []
            if val == "":
                current_list_key = key
            continue
        if val.startswith("{") and val.endswith("}"):
            # simple {G1: pass, G2: fail}
            inner = val[1:-1].strip()
            d: dict[str, str] = {}
            if inner:
                for pair in inner.split(","):
                    if ":" in pair:
                        a, b = pair.split(":", 1)
                        d[a.strip()] = b.strip().strip("\"'")
            meta[key] = d
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            meta[key] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
        elif val.lower() in {"true", "false"}:
            meta[key] = val.lower() == "true"
        else:
            meta[key] = val.strip("\"'")
    return meta


def _parse_gates(body: str) -> list[dict[str, str]]:
    gates: list[dict[str, str]] = []
    # | G1 Scope | evidence | if fail |
    for m in re.finditer(
        r"^\|\s*(G\d+)\s+([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
        body,
        re.M,
    ):
        gid = m.group(1).upper()
        if gid.lower() == "gate":
            continue
        gates.append(
            {
                "id": gid,
                "name": m.group(2).strip(),
                "evidence": m.group(3).strip(),
                "on_fail": m.group(4).strip(),
            }
        )
    # fallback: bare G1 in table first column
    if not gates:
        for m in re.finditer(r"^\|\s*(G\d+)\s*\|\s*([^|]+)\|", body, re.M):
            gates.append({"id": m.group(1).upper(), "name": "", "evidence": m.group(2).strip(), "on_fail": ""})
    return gates


def _parse_dod(body: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    # Prefer section under DoD
    section = body
    m = re.search(r"DoD.*?\n((?:\s*-\s*\[[ xX]\].*\n?)+)", body, re.I)
    if m:
        section = m.group(1)
    for m in re.finditer(r"-\s*\[([ xX])\]\s*(.+)", section):
        items.append({"done": m.group(1).lower() == "x", "text": m.group(2).strip()})
    return items


def _parse_activation(body: str) -> str:
    m = re.search(r"```(?:text)?\n(FORGE[^\n`]+)\n```", body)
    if m:
        return m.group(1).strip()
    m = re.search(r"(FORGE profile=[^\n]+)", body)
    return m.group(1).strip() if m else ""
