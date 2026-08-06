"""Context hydration — inject skill bodies + memory snippets into FORGE packets.

Curation ≠ mass delete: packs promote what enters Act; noise stays in the bank
but is deprioritized via quality scores and pack allowlists.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from talaria_cli.cmds import axon as axon_cmd

PACKS_DIR = Path("_META/axon/packs")


def load_pack(vault: Path, pack_id: str) -> dict[str, Any] | None:
    path = vault / PACKS_DIR / f"{pack_id}.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    data.setdefault("id", pack_id)
    return data


def list_packs(vault: Path) -> list[dict[str, Any]]:
    root = vault / PACKS_DIR
    if not root.is_dir():
        return []
    out = []
    for p in sorted(root.glob("*.json")):
        pack = load_pack(vault, p.stem)
        if pack:
            out.append(
                {
                    "id": pack.get("id") or p.stem,
                    "title": pack.get("title"),
                    "mission": pack.get("mission"),
                    "skill_count": len(pack.get("skills") or []),
                    "query_count": len(pack.get("queries") or []),
                }
            )
    return out


def hydrate_skill_body(vault: Path, rel_path: str, *, max_chars: int = 3500) -> dict[str, Any]:
    path = vault / rel_path
    if not path.is_file():
        return {"path": rel_path, "ok": False, "error": "missing"}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"path": rel_path, "ok": False, "error": str(e)}
    # strip huge frontmatter-heavy dumps
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
    excerpt = body.strip()
    truncated = len(excerpt) > max_chars
    if truncated:
        excerpt = excerpt[:max_chars] + "\n\n…[truncated]"
    return {
        "path": rel_path.replace("\\", "/"),
        "ok": True,
        "chars": len(excerpt),
        "truncated": truncated,
        "body": excerpt,
    }


def hydrate_from_hits(
    vault: Path,
    hits: list[dict[str, Any]],
    *,
    max_skills: int = 5,
    max_chars: int = 3500,
) -> list[dict[str, Any]]:
    out = []
    for h in hits[:max_skills]:
        rel = h.get("path") or ""
        if not rel:
            continue
        item = hydrate_skill_body(vault, rel, max_chars=max_chars)
        item["name"] = h.get("name")
        item["score"] = h.get("score")
        item["domain"] = h.get("domain")
        out.append(item)
    return out


def resolve_pack_hits(vault: Path, pack: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    """Prefer explicit skill paths in pack; fill with query search."""
    hits: list[dict[str, Any]] = []
    seen: set[str] = set()
    for rel in pack.get("skills") or []:
        rel = str(rel).replace("\\", "/")
        if not rel.startswith("skills/"):
            rel = f"skills/{rel.lstrip('/')}"
        if rel in seen:
            continue
        path = vault / rel
        if path.is_file():
            seen.add(rel)
            hits.append(
                {
                    "score": 100,
                    "name": path.stem,
                    "domain": path.parent.name,
                    "path": rel,
                    "description": f"pack:{pack.get('id')}",
                    "why": ["pack-pin"],
                }
            )
        if len(hits) >= limit:
            return hits
    for q in pack.get("queries") or []:
        res = axon_cmd.search_skills(vault, str(q), limit=limit, record=True)
        for h in res.get("hits") or []:
            rel = h.get("path") or ""
            if rel in seen:
                continue
            seen.add(rel)
            hits.append(h)
            if len(hits) >= limit:
                return hits
    return hits


def memory_retrieve(
    vault: Path,
    query: str,
    *,
    forge_id: str | None = None,
    limit: int = 8,
) -> dict[str, Any]:
    """Lightweight vault memory search (Markdown under memory/)."""
    terms = [t for t in re.split(r"\s+", query.lower().strip()) if len(t) > 2]
    roots = [vault / "memory"]
    if forge_id:
        roots.append(vault / "memory" / "research" / "forge" / forge_id)
    hits: list[dict[str, Any]] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            # skip huge generated graphs html companions
            if "graphs" in path.parts and path.name.startswith("."):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            low = text.lower()
            score = 0
            why = []
            for t in terms:
                if t in low:
                    score += low.count(t)
                    why.append(t)
            if forge_id and forge_id.lower() in low:
                score += 3
                why.append("forge_id")
            if score <= 0 and terms:
                continue
            if not terms:
                score = 1
            rel = str(path.relative_to(vault)).replace("\\", "/")
            excerpt = text.strip()
            if len(excerpt) > 1200:
                excerpt = excerpt[:1200] + "\n…[truncated]"
            hits.append(
                {
                    "score": score,
                    "path": rel,
                    "why": why[:6],
                    "excerpt": excerpt,
                }
            )
    hits.sort(key=lambda h: (-h["score"], h["path"]))
    hits = hits[: max(1, limit)] if hits else []
    return {
        "ok": True,
        "command": "memory retrieve",
        "query": query,
        "forge_id": forge_id,
        "hit_count": len(hits),
        "hits": hits,
    }


def build_activation_context(
    vault: Path,
    forge_id: str,
    *,
    specialty: str = "",
    axon_queries: list[str] | None = None,
    pack_id: str | None = None,
    hydrate: bool = True,
    with_memory: bool = True,
    skill_limit: int = 5,
    memory_limit: int = 5,
) -> dict[str, Any]:
    """Full context block for forge run/invoke packets."""
    meta_pack = None
    # profile may declare skill_pack in frontmatter — caller can pass pack_id
    pack = load_pack(vault, pack_id) if pack_id else None
    queries = list(axon_queries or [])
    if not queries:
        queries = [specialty or forge_id]
    if pack:
        meta_pack = {
            "id": pack.get("id"),
            "title": pack.get("title"),
            "mission": pack.get("mission"),
        }
        hits = resolve_pack_hits(vault, pack, limit=max(skill_limit * 2, 8))
        # also run pack queries already inside resolve
    else:
        bundles = axon_cmd.bundles_for_queries(vault, queries, limit=skill_limit, record=True)
        hits = []
        seen: set[str] = set()
        for b in bundles:
            for h in (b.get("result") or {}).get("hits") or []:
                rel = h.get("path") or ""
                if rel in seen:
                    continue
                seen.add(rel)
                hits.append(h)

    hydrated = hydrate_from_hits(vault, hits, max_skills=skill_limit) if hydrate else []
    mem = (
        memory_retrieve(
            vault,
            specialty or forge_id,
            forge_id=forge_id,
            limit=memory_limit,
        )
        if with_memory
        else {"ok": True, "hits": [], "hit_count": 0}
    )

    skill_ids = [h.get("path") for h in hydrated if h.get("ok")]
    return {
        "ok": True,
        "forge_id": forge_id,
        "pack": meta_pack,
        "axon_queries": queries,
        "axon_hits": hits[: skill_limit * 2],
        "skills_hydrated": hydrated,
        "skill_ids_loaded": skill_ids,
        "memory": mem,
        "pilot_must": [
            "Apply loaded skills_hydrated bodies — do not ignore them",
            "Cite skill paths used in deliverable frontmatter: axon_skills: [paths…]",
            "Cite memory paths used: forge_memorize / memory_used",
            "talaria forge check must see Gaxon evidence (skill paths in deliverable)",
        ],
    }
