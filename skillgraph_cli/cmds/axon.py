"""AXON organ — search skills graph (Phase D)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from skillgraph_cli.util import EXIT_ERROR, EXIT_OK, emit

SKILLS_DIR = "skills"


def search_skills(
    vault: Path,
    query: str,
    *,
    domain: str | None = None,
    tag: str | None = None,
    limit: int = 15,
) -> dict[str, Any]:
    root = vault / SKILLS_DIR
    if not root.is_dir():
        return {"ok": False, "error": f"missing {SKILLS_DIR}/", "hits": []}

    terms = _terms(query)
    if not terms and not domain and not tag:
        return {"ok": False, "error": "empty query (and no domain/tag filter)", "hits": []}

    hits: list[dict[str, Any]] = []
    for path in root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta, body = _split_fm(text)
        dom = str(meta.get("domain") or path.parent.name)
        if domain and domain.lower() not in dom.lower():
            continue
        tags = _as_list(meta.get("tags"))
        if tag and tag.lower() not in {t.lower() for t in tags}:
            # also check #tag in body
            if f"#{tag.lower()}" not in text.lower():
                continue

        name = str(meta.get("name") or path.stem)
        desc = str(meta.get("description") or "")
        score, reasons = _score(terms, name=name, desc=desc, tags=tags, domain=dom, body=body[:2000])
        if not terms:
            score = 1
            reasons = ["filter-only"]
        if score <= 0:
            continue
        rel = str(path.relative_to(vault)).replace("\\", "/")
        hits.append(
            {
                "score": score,
                "name": name,
                "domain": dom,
                "tags": tags,
                "description": desc[:220],
                "path": rel,
                "why": reasons[:4],
            }
        )

    hits.sort(key=lambda h: (-h["score"], h["name"].lower()))
    hits = hits[: max(1, limit)]
    return {
        "ok": True,
        "query": query,
        "domain": domain,
        "tag": tag,
        "limit": limit,
        "hit_count": len(hits),
        "hits": hits,
    }


def axon_stats(vault: Path) -> dict[str, Any]:
    root = vault / SKILLS_DIR
    if not root.is_dir():
        return {"ok": False, "skills": 0, "domains": 0}
    files = list(root.rglob("*.md"))
    domains = {p.parent.name for p in files if p.parent != root}
    return {
        "ok": True,
        "skills_md": len(files),
        "domains": len(domains),
        "domain_sample": sorted(domains)[:20],
    }


def run_search(
    vault: Path,
    query: str,
    *,
    domain: str | None = None,
    tag: str | None = None,
    limit: int = 15,
    as_json: bool = False,
) -> int:
    data = search_skills(vault, query, domain=domain, tag=tag, limit=limit)
    data["command"] = "axon search"
    data["stats"] = axon_stats(vault)
    if as_json:
        emit(data, True)
    else:
        if not data.get("ok"):
            print("axon search FAIL:", data.get("error"))
            return EXIT_ERROR
        print(f"AXON search: {data['hit_count']} hits for {query!r}")
        for h in data["hits"]:
            print(f"  [{h['score']:3}] {h['name']}  ({h['domain']})  {h['path']}")
            if h.get("description"):
                print(f"        {h['description'][:100]}")
    return EXIT_OK if data.get("ok") else EXIT_ERROR


def parse_axon_query(q: str) -> tuple[str, str | None, str | None]:
    domain = tag = None
    raw = q
    if q.lower().startswith("domain:"):
        rest = q.split(":", 1)[1].strip()
        parts = rest.split(None, 1)
        domain = parts[0]
        raw = parts[1] if len(parts) > 1 else domain
    elif q.lower().startswith("tag:"):
        rest = q.split(":", 1)[1].strip()
        parts = rest.split(None, 1)
        tag = parts[0]
        raw = parts[1] if len(parts) > 1 else tag
    return raw, domain, tag


def bundles_for_queries(
    vault: Path, queries: list[str], *, limit: int = 10
) -> list[dict[str, Any]]:
    bundles = []
    for q in queries:
        raw, domain, tag = parse_axon_query(str(q))
        bundles.append(
            {
                "query": q,
                "result": search_skills(vault, raw, domain=domain, tag=tag, limit=limit),
            }
        )
    return bundles


def run_for_profile(
    vault: Path,
    forge_id: str,
    *,
    limit: int = 10,
    as_json: bool = False,
) -> int:
    """Run default axon_queries declared on a FORGE profile."""
    from skillgraph_cli.cmds import forge as forge_cmd

    profile = forge_cmd.load_profile(vault, forge_id)
    if not profile:
        emit({"ok": False, "error": f"profile not found: {forge_id}"}, as_json or True)
        return EXIT_ERROR
    meta = profile.get("meta") or {}
    queries = _as_list(meta.get("axon_queries"))
    if not queries:
        specialty = str(meta.get("specialty") or forge_id)
        queries = [specialty.split("—")[0].strip()[:60] or forge_id]

    bundles = bundles_for_queries(vault, queries, limit=limit)
    data = {
        "command": "axon for-profile",
        "ok": True,
        "forge_id": forge_id,
        "axon_queries": queries,
        "bundles": bundles,
    }
    if as_json:
        emit(data, True)
    else:
        print(f"AXON for FORGE {forge_id}: {len(queries)} queries")
        for b in bundles:
            r = b["result"]
            print(f"  query {b['query']!r} -> {r.get('hit_count', 0)} hits")
            for h in (r.get("hits") or [])[:5]:
                print(f"    - {h['name']} ({h['domain']})")
    return EXIT_OK


def _terms(query: str) -> list[str]:
    return [t for t in re.split(r"[\s,;/|]+", query.lower()) if len(t) >= 2]


def _score(
    terms: list[str],
    *,
    name: str,
    desc: str,
    tags: list[str],
    domain: str,
    body: str,
) -> tuple[int, list[str]]:
    if not terms:
        return 0, []
    score = 0
    reasons: list[str] = []
    name_l = name.lower()
    desc_l = desc.lower()
    domain_l = domain.lower()
    tags_l = " ".join(tags).lower()
    body_l = body.lower()
    for t in terms:
        if t in name_l or name_l in t:
            score += 50
            reasons.append(f"name:{t}")
        if t in domain_l:
            score += 30
            reasons.append(f"domain:{t}")
        if t in tags_l:
            score += 25
            reasons.append(f"tag:{t}")
        if t in desc_l:
            score += 15
            reasons.append(f"desc:{t}")
        elif t in body_l:
            score += 5
            reasons.append(f"body:{t}")
    return score, reasons


def _as_list(val: Any) -> list[str]:
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x) for x in val]
    if isinstance(val, str):
        s = val.strip()
        if s.startswith("[") and s.endswith("]"):
            inner = s[1:-1].strip()
            return [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
        return [s] if s else []
    return [str(val)]


def _split_fm(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, Any] = {}
    current = None
    for raw in parts[1].splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if current and line.startswith("  - "):
            meta.setdefault(current, []).append(line[4:].strip().strip("\"'"))
            continue
        current = None
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v == "":
            current = k
            meta[k] = []
        elif v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            meta[k] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
        else:
            meta[k] = v.strip("\"'")
    return meta, parts[2]
