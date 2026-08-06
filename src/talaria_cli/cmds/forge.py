"""FORGE organ — list / show / check / run profiles (Phase C)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

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
        from talaria_cli.cmds.forge_delegation import normalize_delegation

        dele = normalize_delegation(meta)
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
                "role_kind": dele["role_kind"],
                "invocable_by_mode": dele["invocable_by_mode"],
                "invocable_by": dele["invocable_by"],
                "invokes": dele["invokes"],
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


def evaluate_profile_structure(
    profile: dict[str, Any],
    vault: Path | None = None,
) -> dict[str, Any]:
    """Ley I/II structural checks on the profile note itself.

    Builder 2.0 profiles (meta.builder starts with "2") must point at an existing
    corpus doctrine file when status is active.
    """
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

    builder = str(meta.get("builder") or "1.0").strip()
    is_v2 = builder.startswith("2")
    status = str(meta.get("status") or "").lower()
    corpus_rel = str(meta.get("corpus_path") or "").strip().replace("\\", "/")
    if is_v2 and status == "active":
        add("corpus_path_declared", bool(corpus_rel), corpus_rel or "(missing corpus_path)")
        if vault is not None and corpus_rel:
            doctrine = vault / corpus_rel / "00-doctrine.md"
            add(
                "corpus_doctrine_exists",
                doctrine.is_file(),
                f"{corpus_rel}/00-doctrine.md" if doctrine.is_file() else f"missing {corpus_rel}/00-doctrine.md",
            )
        try:
            body = Path(profile["path"]).read_text(encoding="utf-8")
        except Exception:
            body = ""
        add(
            "learn_loop_section",
            bool(re.search(r"(?i)learn\s*loop|bucle\s*de\s*aprendizaje", body)),
            "section Learn loop",
        )
        add(
            "critical_thinking_section",
            bool(re.search(r"(?i)pensamiento\s*cr[ií]tico|critical\s*thinking", body)),
            "section Pensamiento crítico",
        )

    ok = all(c["ok"] for c in checks)
    return {
        "kind": "profile_structure",
        "forge_id": profile.get("forge_id"),
        "builder": builder,
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
    require_axon: bool = False,
) -> dict[str, Any]:
    """Check deliverable against profile gates (frontmatter forge_gates or --declare)."""
    text = deliverable.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    declared = dict(declare or {})
    fm_gates = meta.get("forge_gates") or {}
    if isinstance(fm_gates, dict):
        for k, v in fm_gates.items():
            raw = str(k)
            gid = raw.upper() if re.fullmatch(r"G\d+", raw, re.I) else ("G" + raw[1:].lower() if raw.upper().startswith("G") else raw)
            declared.setdefault(gid, str(v).lower())
    # also accept top-level G*: pass keys from imperfect YAML
    for k, v in meta.items():
        if re.fullmatch(r"G[A-Za-z0-9]+", str(k), re.I):
            raw = str(k)
            gid = raw.upper() if re.fullmatch(r"G\d+", raw, re.I) else ("G" + raw[1:].lower())
            declared.setdefault(gid, str(v).lower())
    # body lines like: G1: pass
    for m in re.finditer(r"^\s*(G[A-Za-z0-9]+)\s*[=:]\s*(pass|fail|n/a)\s*$", body, re.I | re.M):
        raw = m.group(1)
        gid = raw.upper() if re.fullmatch(r"G\d+", raw, re.I) else ("G" + raw[1:].lower())
        declared.setdefault(gid, m.group(2).lower())

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

    # Gaxon — skills from AXON bank cited
    pmeta = profile.get("meta") or {}
    need_axon = require_axon or bool(pmeta.get("require_axon"))
    axon_skills = meta.get("axon_skills") or meta.get("skills_used") or []
    if isinstance(axon_skills, str):
        axon_skills = [axon_skills]
    if not isinstance(axon_skills, list):
        axon_skills = []
    body_skills = re.findall(r"skills/[^\s\]`'\"<>]+", text)
    cited = [str(x).replace("\\", "/") for x in list(axon_skills) + body_skills]
    cited = [c for i, c in enumerate(cited) if c and c not in cited[:i]]
    gaxon_ok = len(cited) >= 1
    if need_axon or "Gaxon" in {g["id"] for g in (profile.get("gates") or [])} or declared.get("GAXON"):
        # if Gaxon in declared gates table as pass without cites — still fail need_axon
        val = str(declared.get("GAXON") or declared.get("Gaxon") or "").lower()
        if need_axon:
            checks.append(
                {
                    "name": "gate_Gaxon",
                    "ok": gaxon_ok,
                    "detail": f"cited={cited[:5]}" if gaxon_ok else "missing axon_skills: [skills/…] in frontmatter or body",
                }
            )
        elif val:
            checks.append(
                {
                    "name": "gate_Gaxon",
                    "ok": val == "pass" and gaxon_ok,
                    "detail": f"declared={val}; cited={cited[:5]}",
                }
            )
        elif gaxon_ok:
            checks.append(
                {
                    "name": "gate_Gaxon",
                    "ok": True,
                    "detail": f"cited={cited[:5]}",
                }
            )

    ok = all(c["ok"] for c in checks)
    return {
        "kind": "deliverable_gates",
        "forge_id": profile_id,
        "deliverable": str(deliverable),
        "ok": ok,
        "declared_gates": declared,
        "axon_skills_cited": cited,
        "checks": checks,
        "next": "FORGE done allowed" if ok else "Mark remaining gates pass in deliverable or --declare",
    }


def run_list(
    vault: Path,
    *,
    ensembles: bool = False,
    graph: bool = False,
    as_json: bool = False,
) -> int:
    profiles = list_profiles(vault)
    data: dict[str, Any] = {
        "command": "forge list",
        "ok": True,
        "count": len(profiles),
        "profiles": profiles,
    }
    if ensembles:
        data["ensembles"] = list_ensembles(vault)
    if graph:
        from talaria_cli.cmds import forge_delegation as dele

        data["graph"] = dele.build_delegation_graph(vault)
    if as_json:
        emit(data, True)
    else:
        print(f"FORGE profiles: {len(profiles)}")
        for p in profiles:
            kind = p.get("role_kind") or "both"
            print(
                f"  - {p['forge_id']:20} [{p['status']}] kind={kind} "
                f"gates={','.join(p['gates']) or '-'}  {p['specialty'][:50]}"
            )
        if ensembles:
            print(f"Ensembles: {len(data['ensembles'])}")
            for e in data["ensembles"]:
                print(f"  - {e['forge_id']}: {e['profiles']}")
        if graph:
            g = data["graph"]
            print(f"Delegation graph: {g['node_count']} nodes, {g['edge_count']} edges")
            for e in g["edges"]:
                print(f"  {e['from']} --{e['kind']}--> {e['to']}")
    return EXIT_OK


def run_show(vault: Path, forge_id: str, *, as_json: bool = False) -> int:
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR
    struct = evaluate_profile_structure(profile, vault)
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
    require_axon: bool = False,
    as_json: bool = False,
) -> int:
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR

    struct = evaluate_profile_structure(profile, vault)
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
        deliv = evaluate_deliverable(
            profile, path, declare=declared, require_axon=require_axon
        )
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
            deliv = evaluate_deliverable(
                profile, tmp, declare=declared, require_axon=require_axon
            )
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


def run_run(
    vault: Path,
    forge_id: str,
    *,
    with_axon: bool = True,
    hydrate: bool = True,
    with_memory: bool = True,
    pack: str | None = None,
    as_json: bool = False,
) -> int:
    """Emit playbook packet; default hydrates AXON skill bodies + memory retrieve."""
    profile = load_profile(vault, forge_id)
    if not profile:
        emit({"error": f"profile not found: {forge_id}", "ok": False}, as_json or True)
        return EXIT_ERROR
    struct = evaluate_profile_structure(profile, vault)
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
    pack_id = pack or str(meta.get("skill_pack") or "").strip() or None

    from talaria_cli.cmds import axon as axon_cmd
    from talaria_cli.cmds import forge_delegation as dele
    from talaria_cli.cmds import session as session_cmd
    from talaria_cli.cmds.context_hydrate import build_activation_context
    from talaria_cli.mode import mode_contract, resolve_mode

    mode = resolve_mode(vault)
    sess = session_cmd.load_session(vault)
    packet: dict[str, Any] = {
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
        "skill_pack": pack_id,
        "mode": mode,
        "mode_contract": mode_contract(mode),
        "session": sess,
        "spine_enforcement": {
            "strict_requires_session": mode == "strict",
            "session_active": bool(sess),
            "required_close": [
                "talaria forge check --profile <id> --deliverable <path> [--require-axon]",
                "scorecard forge_critical: pass + axon_skills cited",
                "talaria session close --json",
            ],
        },
        "instructions": [
            "If no session: talaria session start --objective \"...\" --forge " + forge_id,
            "READ skills_hydrated in this packet — apply them (do not skip)",
            "Use memory hits; cite paths in deliverable",
            "Execute profile playbook",
            "Deliverable frontmatter: axon_skills: [skills/…]",
            "talaria forge check --profile <id> --deliverable <path> --require-axon --json",
            "talaria session close --json",
        ],
    }

    if with_axon or with_memory:
        ctx = build_activation_context(
            vault,
            forge_id,
            specialty=str(meta.get("specialty") or forge_id),
            axon_queries=list(axon_queries) if axon_queries else None,
            pack_id=pack_id if with_axon else None,
            hydrate=bool(hydrate and with_axon),
            with_memory=with_memory,
            skill_limit=5,
            memory_limit=5,
        )
        packet["context"] = {
            "pack": ctx.get("pack"),
            "pilot_must": ctx.get("pilot_must"),
        }
        if with_axon:
            queries = (
                list(axon_queries)
                if axon_queries
                else [str(meta.get("specialty") or forge_id)[:60]]
            )
            packet["axon"] = axon_cmd.bundles_for_queries(vault, queries, limit=5)
            packet["skills_hydrated"] = ctx.get("skills_hydrated")
            packet["skill_ids_loaded"] = ctx.get("skill_ids_loaded")
        if with_memory:
            packet["memory"] = ctx.get("memory")

    packet = dele.enrich_run_packet(vault, forge_id, packet)

    if as_json:
        emit(packet, True)
    else:
        print(packet["activation"])
        print("gates:", ", ".join(g["id"] for g in packet["gates"]))
        print("DoD:", len(packet["dod"]), "items — see", packet["path"])
        if pack_id:
            print("skill_pack:", pack_id)
        ids = packet.get("skill_ids_loaded") or []
        if ids:
            print("skills_hydrated:", len(ids))
            for pth in ids[:5]:
                print("  -", pth)
        mem_n = (packet.get("memory") or {}).get("hit_count") or 0
        if mem_n:
            print("memory_hits:", mem_n)
        d = packet.get("delegation") or {}
        if d.get("invokes"):
            print("invokes:", ", ".join(d["invokes"]))
        for i, step in enumerate(packet["instructions"], 1):
            print(f"  {i}. {step}")
    return EXIT_OK


def run_graph(vault: Path, *, as_json: bool = False) -> int:
    from talaria_cli.cmds import forge_delegation as dele

    data = dele.build_delegation_graph(vault)
    if as_json:
        emit(data, True)
    else:
        print(f"FORGE delegation graph: {data['node_count']} nodes, {data['edge_count']} edges")
        print(data["note"])
        for e in data["edges"]:
            flag = "" if e["target_exists"] else " (missing)"
            print(f"  {e['from']} --{e['kind']}--> {e['to']}{flag}")
    return EXIT_OK


def run_invoke(
    vault: Path,
    parent_id: str,
    child_id: str,
    *,
    brief: str | None = None,
    strict: bool = False,
    with_axon: bool = True,
    hydrate: bool = True,
    with_memory: bool = True,
    pack: str | None = None,
    deliverable: str | None = None,
    artifact_in: str | None = None,
    require_deliverable: bool = False,
    as_json: bool = False,
) -> int:
    """Delegate from parent profile to child specialist (user-owned graph).

    With --require-deliverable, a child deliverable path is mandatory and must
    pass forge check gates before the handoff is marked complete.
    """
    from talaria_cli.cmds import forge_delegation as dele
    from talaria_cli.cmds import session as session_cmd
    from talaria_cli.mode import mode_contract, resolve_mode

    policy = dele.check_invoke_policy(vault, parent_id, child_id, strict=strict)
    if not policy["allowed"]:
        data = {
            "command": "forge invoke",
            "ok": False,
            "error": "invoke policy failed",
            "policy": policy,
        }
        emit(data, as_json or True)
        return EXIT_ERROR

    if require_deliverable and not deliverable:
        emit(
            {
                "command": "forge invoke",
                "ok": False,
                "error": "deliverable required (--deliverable PATH) when --require-deliverable",
                "hint": "Start-only packet: omit --require-deliverable; close handoff with deliverable.",
                "parent": parent_id,
                "child": child_id,
            },
            as_json or True,
        )
        return EXIT_ERROR

    child = load_profile(vault, child_id)
    if not child:
        emit({"ok": False, "error": f"child not found: {child_id}"}, as_json or True)
        return EXIT_ERROR
    struct = evaluate_profile_structure(child, vault)
    if not struct["ok"]:
        emit(
            {
                "command": "forge invoke",
                "ok": False,
                "error": "child fails structural check",
                "structure": struct,
                "policy": policy,
            },
            as_json or True,
        )
        return EXIT_ERROR

    meta = child.get("meta") or {}
    axon_queries = meta.get("axon_queries") or []
    if isinstance(axon_queries, str):
        axon_queries = [axon_queries]

    artifact_contract = {
        "required": bool(require_deliverable) or bool(deliverable),
        "artifact_in": artifact_in,
        "deliverable": deliverable,
        "handoff_status": "open",
        "rule": "Child must produce a vault deliverable; parent resumes only after forge check pass",
    }

    deliv_result = None
    if deliverable:
        path = Path(deliverable)
        if not path.is_file():
            path = vault / deliverable
        if not path.is_file():
            emit(
                {
                    "command": "forge invoke",
                    "ok": False,
                    "error": f"deliverable not found: {deliverable}",
                    "parent": parent_id,
                    "child": child_id,
                },
                as_json or True,
            )
            return EXIT_ERROR
        deliv_result = evaluate_deliverable(child, path)
        artifact_contract["handoff_status"] = (
            "complete" if deliv_result.get("ok") else "rejected"
        )
        artifact_contract["deliverable_check"] = deliv_result
        if require_deliverable and not deliv_result.get("ok"):
            emit(
                {
                    "command": "forge invoke",
                    "ok": False,
                    "error": "deliverable failed forge check",
                    "artifact_contract": artifact_contract,
                    "policy": policy,
                },
                as_json or True,
            )
            return EXIT_ERROR

    mode = resolve_mode(vault)
    packet: dict[str, Any] = {
        "command": "forge invoke",
        "ok": True,
        "parent": parent_id,
        "child": child_id,
        "brief": brief or "",
        "policy": policy,
        "forge_id": child_id,
        "activation": child.get("activation")
        or f"FORGE profile={child_id} | parent={parent_id} | laws=I+II | spine=on",
        "gates": child["gates"],
        "dod": child["dod"],
        "specialty": meta.get("specialty"),
        "path": child["rel_path"],
        "axon_queries": axon_queries,
        "mode": mode,
        "mode_contract": mode_contract(mode),
        "session": session_cmd.load_session(vault),
        "artifact_contract": artifact_contract,
        "instructions": [
            f"Delegated by parent `{parent_id}`" + (f" brief={brief!r}" if brief else ""),
            (
                f"Inbound artifact: {artifact_in}"
                if artifact_in
                else "Inbound artifact: (none declared — parent should pass --artifact-in)"
            ),
            "Execute child playbook; write deliverable with forge_profile + forge_gates (Gcrit/Gmem)",
            (
                f"Close handoff: talaria forge invoke {parent_id} {child_id} "
                "--deliverable <path> --require-deliverable --json"
                if artifact_contract["handoff_status"] == "open"
                else f"Handoff {artifact_contract['handoff_status']}; parent resumes"
            ),
            f"Parent resumes: talaria forge run {parent_id} --json",
        ],
    }
    packet = dele.enrich_run_packet(vault, child_id, packet)
    pack_id = pack or str(meta.get("skill_pack") or "").strip() or None
    packet["skill_pack"] = pack_id
    if with_axon or with_memory:
        from talaria_cli.cmds.context_hydrate import build_activation_context

        ctx = build_activation_context(
            vault,
            child_id,
            specialty=str(meta.get("specialty") or child_id),
            axon_queries=list(axon_queries) if axon_queries else None,
            pack_id=pack_id if with_axon else None,
            hydrate=bool(hydrate and with_axon),
            with_memory=with_memory,
            skill_limit=5,
            memory_limit=5,
        )
        packet["context"] = {
            "pack": ctx.get("pack"),
            "pilot_must": ctx.get("pilot_must"),
        }
        if with_axon:
            from talaria_cli.cmds import axon as axon_cmd

            queries = (
                list(axon_queries)
                if axon_queries
                else [str(meta.get("specialty") or child_id)[:60]]
            )
            packet["axon"] = axon_cmd.bundles_for_queries(vault, queries, limit=8)
            packet["skills_hydrated"] = ctx.get("skills_hydrated")
            packet["skill_ids_loaded"] = ctx.get("skill_ids_loaded")
        if with_memory:
            packet["memory"] = ctx.get("memory")

    if as_json:
        emit(packet, True)
    else:
        print(packet["activation"])
        if policy.get("warnings"):
            for w in policy["warnings"]:
                print("WARN:", w)
        print(f"invoke {parent_id} → {child_id} [{artifact_contract['handoff_status']}]")
        if brief:
            print("brief:", brief)
        for i, step in enumerate(packet["instructions"], 1):
            print(f"  {i}. {step}")
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
    current_map_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        # nested map values under a key (forge_gates: / axon_queries handled separately)
        if current_map_key and line.startswith("  ") and ":" in line and not line.lstrip().startswith("-"):
            k, v = line.strip().split(":", 1)
            d = meta.get(current_map_key)
            if not isinstance(d, dict):
                d = {}
                meta[current_map_key] = d
            d[k.strip()] = v.strip().strip("\"'")
            current_list_key = None
            continue
        if current_list_key and (line.startswith("  - ") or line.startswith("- ")):
            # promote empty dict placeholder to list if needed
            if isinstance(meta.get(current_list_key), dict) and not meta[current_list_key]:
                meta[current_list_key] = []
            item = line.lstrip().removeprefix("- ").strip().strip("\"'")
            meta.setdefault(current_list_key, [])
            if not isinstance(meta[current_list_key], list):
                meta[current_list_key] = []
            meta[current_list_key].append(item)
            current_map_key = None
            continue
        current_list_key = None
        current_map_key = None
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "[]":
            meta[key] = []
            continue
        if val == "{}":
            meta[key] = {}
            current_map_key = key
            continue
        if val == "":
            # child lines decide list vs map
            meta[key] = {}
            current_map_key = key
            current_list_key = key
            continue
        if val.startswith("{") and val.endswith("}"):
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

    def _norm_gid(gid: str) -> str:
        if re.fullmatch(r"G\d+", gid, re.I):
            return gid.upper()
        return "G" + gid[1:].lower()

    # | G1 Scope | evidence | if fail |  OR  | Gcrit Crítica | ...
    for m in re.finditer(
        r"^\|\s*(G[A-Za-z0-9]+)\s+([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
        body,
        re.M,
    ):
        gid = m.group(1)
        if gid.lower() == "gate":
            continue
        gates.append(
            {
                "id": _norm_gid(gid),
                "name": m.group(2).strip(),
                "evidence": m.group(3).strip(),
                "on_fail": m.group(4).strip(),
            }
        )
    if not gates:
        for m in re.finditer(r"^\|\s*(G[A-Za-z0-9]+)\s*\|\s*([^|]+)\|", body, re.M):
            gates.append(
                {
                    "id": _norm_gid(m.group(1)),
                    "name": "",
                    "evidence": m.group(2).strip(),
                    "on_fail": "",
                }
            )
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
