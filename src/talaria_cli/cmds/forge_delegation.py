"""FORGE delegation graph — user-owned agent composition.

Talaria does not ship an org chart. Users create agents with `forge build`
and optionally declare who may invoke whom (`invokes` / `invocable_by`).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from talaria_cli.cmds.forge import list_profiles, load_profile


VALID_KINDS = {"orchestrator", "specialist", "both"}
VALID_MODES = {"open", "allowlist", "deny_direct"}


def _as_str_list(val: Any) -> list[str]:
    if val is None:
        return []
    if isinstance(val, str):
        return [x.strip() for x in val.split(",") if x.strip()]
    if isinstance(val, list):
        out: list[str] = []
        for x in val:
            if isinstance(x, dict):
                iid = x.get("id") or x.get("forge_id")
                if iid:
                    out.append(str(iid).strip())
            else:
                s = str(x).strip().strip("\"'")
                if s:
                    out.append(s)
        return out
    return []


def normalize_delegation(meta: dict[str, Any] | None) -> dict[str, Any]:
    meta = meta or {}
    kind = str(meta.get("role_kind") or "both").strip().lower()
    if kind not in VALID_KINDS:
        kind = "both"
    mode = str(meta.get("invocable_by_mode") or "open").strip().lower()
    if mode not in VALID_MODES:
        mode = "open"
    return {
        "role_kind": kind,
        "invocable_by_mode": mode,
        "invocable_by": _as_str_list(meta.get("invocable_by")),
        "invokes": _as_str_list(meta.get("invokes")),
    }


def delegation_for_profile(vault: Path, forge_id: str) -> dict[str, Any] | None:
    profile = load_profile(vault, forge_id)
    if not profile:
        return None
    d = normalize_delegation(profile.get("meta"))
    d["forge_id"] = profile["forge_id"]
    d["status"] = (profile.get("meta") or {}).get("status")
    d["specialty"] = (profile.get("meta") or {}).get("specialty")
    return d


def build_delegation_graph(vault: Path) -> dict[str, Any]:
    """Directed edges: A --invokes--> B and B.invocable_by --may_invoke--> B."""
    profiles = list_profiles(vault)
    nodes = []
    edges: list[dict[str, Any]] = []
    seen_edge: set[tuple[str, str, str]] = set()
    by_id = {p["forge_id"] for p in profiles}

    for p in profiles:
        full = load_profile(vault, p["forge_id"])
        d = normalize_delegation(full.get("meta") if full else {})
        nodes.append(
            {
                "forge_id": p["forge_id"],
                "status": p.get("status"),
                "specialty": p.get("specialty"),
                "role_kind": d["role_kind"],
                "invocable_by_mode": d["invocable_by_mode"],
                "invocable_by": d["invocable_by"],
                "invokes": d["invokes"],
            }
        )
        src = p["forge_id"]
        for dst in d["invokes"]:
            key = (src, dst, "invokes")
            if key not in seen_edge:
                seen_edge.add(key)
                edges.append(
                    {
                        "from": src,
                        "to": dst,
                        "kind": "invokes",
                        "target_exists": dst in by_id,
                    }
                )
        for parent in d["invocable_by"]:
            key = (parent, src, "may_invoke")
            if key not in seen_edge:
                seen_edge.add(key)
                edges.append(
                    {
                        "from": parent,
                        "to": src,
                        "kind": "may_invoke",
                        "target_exists": parent in by_id,
                    }
                )

    return {
        "ok": True,
        "command": "forge graph",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "note": (
            "User-owned graph. Talaria ships the factory (forge build), not a fixed org chart. "
            "Default invocable_by_mode=open (owner may forge run any agent)."
        ),
    }


def check_invoke_policy(
    vault: Path,
    parent_id: str,
    child_id: str,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    parent = load_profile(vault, parent_id)
    child = load_profile(vault, child_id)
    warnings: list[str] = []
    errors: list[str] = []

    if not parent:
        errors.append(f"parent not found: {parent_id}")
    if not child:
        errors.append(f"child not found: {child_id}")
    if errors:
        return {
            "ok": False,
            "allowed": False,
            "strict": strict,
            "errors": errors,
            "warnings": warnings,
        }

    p_del = normalize_delegation(parent.get("meta"))
    c_del = normalize_delegation(child.get("meta"))

    if child_id not in (p_del.get("invokes") or []):
        msg = (
            f"parent `{parent_id}` does not list `{child_id}` in `invokes` "
            "(add edge or treat as ad-hoc)"
        )
        (errors if strict else warnings).append(msg)

    mode = c_del["invocable_by_mode"]
    allow = set(c_del.get("invocable_by") or [])
    if mode == "open":
        if allow and parent_id not in allow:
            warnings.append(
                f"child `{child_id}` is open but lists preferred callers; "
                f"`{parent_id}` not in invocable_by={sorted(allow)}"
            )
    elif mode == "allowlist":
        if parent_id not in allow:
            msg = (
                f"child `{child_id}` invocable_by_mode=allowlist; "
                f"`{parent_id}` not in {sorted(allow) or '(empty)'}"
            )
            (errors if strict else warnings).append(msg)
    elif mode == "deny_direct":
        if parent_id not in allow:
            errors.append(
                f"child `{child_id}` deny_direct: only allowlisted parents may invoke "
                f"(have: {sorted(allow) or 'none'})"
            )
        else:
            warnings.append(
                "deny_direct: prefer forge invoke via parent; direct forge run is owner override"
            )

    allowed = len(errors) == 0
    return {
        "ok": allowed,
        "allowed": allowed,
        "strict": strict,
        "parent": parent_id,
        "child": child_id,
        "parent_delegation": p_del,
        "child_delegation": c_del,
        "errors": errors,
        "warnings": warnings,
        "policy_note": (
            "Human owner can always forge run any profile. "
            "Policy gates automated parent→child delegation."
        ),
    }


def enrich_run_packet(vault: Path, forge_id: str, packet: dict[str, Any]) -> dict[str, Any]:
    d = delegation_for_profile(vault, forge_id)
    if not d:
        return packet
    packet["delegation"] = {
        "role_kind": d["role_kind"],
        "invocable_by_mode": d["invocable_by_mode"],
        "invocable_by": d["invocable_by"],
        "invokes": d["invokes"],
        "how_to_delegate": (
            [
                f"talaria forge invoke {forge_id} <child_id> --brief \"…\" --json"
            ]
            if d["invokes"]
            else [
                "No invokes declared. Add `invokes:` in frontmatter or rebuild with --invokes."
            ]
        ),
        "user_owned": True,
    }
    if d["invokes"]:
        packet["instructions"] = list(packet.get("instructions") or []) + [
            "Delegation: for specialist work use "
            f"`talaria forge invoke {forge_id} <child> --json` "
            f"(declared children: {', '.join(d['invokes'])})",
        ]
    return packet
