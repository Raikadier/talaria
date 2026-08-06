"""AXON organ — search skills graph (Phase D) + quality loop."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

SKILLS_DIR = "skills"
QUALITY_REL = "memory/context/axon-quality.json"


def quality_path(vault: Path) -> Path:
    return vault / QUALITY_REL


def load_quality(vault: Path) -> dict[str, Any]:
    p = quality_path(vault)
    if not p.is_file():
        return {"version": 1, "skills": {}, "searches": 0}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"version": 1, "skills": {}, "searches": 0}
        data.setdefault("skills", {})
        data.setdefault("searches", 0)
        return data
    except Exception:
        return {"version": 1, "skills": {}, "searches": 0}


def save_quality(vault: Path, data: dict[str, Any]) -> None:
    p = quality_path(vault)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_search_hits(vault: Path, hits: list[dict[str, Any]], *, query: str = "") -> None:
    data = load_quality(vault)
    data["searches"] = int(data.get("searches") or 0) + 1
    data["last_search"] = datetime.now(timezone.utc).isoformat()
    data["last_query"] = query
    skills = data.setdefault("skills", {})
    for h in hits:
        rel = h.get("path") or ""
        if not rel:
            continue
        entry = skills.setdefault(rel, {"shown": 0, "useful": 0, "noise": 0, "name": h.get("name")})
        entry["shown"] = int(entry.get("shown") or 0) + 1
        entry["name"] = h.get("name") or entry.get("name")
        entry["domain"] = h.get("domain")
    save_quality(vault, data)


def record_feedback(vault: Path, skill_path: str, signal: str) -> dict[str, Any]:
    signal = signal.lower().strip()
    if signal not in {"useful", "noise"}:
        return {"ok": False, "error": "signal must be useful|noise"}
    rel = skill_path.replace("\\", "/")
    if rel.startswith("skills/") is False and not rel.endswith(".md"):
        # allow bare stem lookup later
        pass
    # normalize to vault-relative skills path if absolute
    vault_s = str(vault).replace("\\", "/")
    if rel.startswith(vault_s):
        rel = rel[len(vault_s) :].lstrip("/")
    data = load_quality(vault)
    skills = data.setdefault("skills", {})
    entry = skills.setdefault(rel, {"shown": 0, "useful": 0, "noise": 0})
    entry[signal] = int(entry.get(signal) or 0) + 1
    entry["last_feedback"] = datetime.now(timezone.utc).isoformat()
    save_quality(vault, data)
    return {"ok": True, "path": rel, "signal": signal, "entry": entry}


def quality_boost(vault: Path, rel_path: str) -> tuple[int, str | None]:
    data = load_quality(vault)
    entry = (data.get("skills") or {}).get(rel_path) or {}
    useful = int(entry.get("useful") or 0)
    noise = int(entry.get("noise") or 0)
    shown = int(entry.get("shown") or 0)
    if useful or noise:
        boost = useful * 8 - noise * 10
        return boost, f"quality:u{useful}/n{noise}"
    if shown > 5 and useful == 0:
        return -2, "quality:shown-no-feedback"
    return 0, None


def quality_report(vault: Path, *, limit: int = 20) -> dict[str, Any]:
    data = load_quality(vault)
    rows = []
    for path, entry in (data.get("skills") or {}).items():
        useful = int(entry.get("useful") or 0)
        noise = int(entry.get("noise") or 0)
        shown = int(entry.get("shown") or 0)
        score = useful * 8 - noise * 10 + min(shown, 20)
        rows.append(
            {
                "path": path,
                "name": entry.get("name"),
                "domain": entry.get("domain"),
                "shown": shown,
                "useful": useful,
                "noise": noise,
                "score": score,
            }
        )
    rows.sort(key=lambda r: (-r["score"], -r["useful"], r["path"]))
    top = rows[:limit]
    noisy = sorted(rows, key=lambda r: (-r["noise"], -r["shown"]))[:limit]
    return {
        "ok": True,
        "searches": data.get("searches", 0),
        "tracked_skills": len(rows),
        "top_useful": [r for r in top if r["useful"] > 0][:limit],
        "top_by_score": top,
        "noisy_candidates": [r for r in noisy if r["noise"] > 0][:limit],
        "path": QUALITY_REL,
    }


def search_skills(
    vault: Path,
    query: str,
    *,
    domain: str | None = None,
    tag: str | None = None,
    limit: int = 15,
    record: bool = False,
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
        boost, why_q = quality_boost(vault, rel)
        score += boost
        if why_q:
            reasons.append(why_q)
        if score <= 0:
            continue
        hits.append(
            {
                "score": score,
                "name": name,
                "domain": dom,
                "tags": tags,
                "description": desc[:220],
                "path": rel,
                "why": reasons[:5],
            }
        )

    hits.sort(key=lambda h: (-h["score"], h["name"].lower()))
    hits = hits[: max(1, limit)]
    if record and hits:
        record_search_hits(vault, hits, query=query)
    return {
        "ok": True,
        "query": query,
        "domain": domain,
        "tag": tag,
        "limit": limit,
        "hit_count": len(hits),
        "hits": hits,
        "recorded": bool(record),
    }


def axon_stats(vault: Path) -> dict[str, Any]:
    root = vault / SKILLS_DIR
    if not root.is_dir():
        return {"ok": False, "skills": 0, "domains": 0}
    files = list(root.rglob("*.md"))
    domains = {p.parent.name for p in files if p.parent != root}
    q = load_quality(vault)
    return {
        "ok": True,
        "skills_md": len(files),
        "domains": len(domains),
        "domain_sample": sorted(domains)[:20],
        "quality_searches": q.get("searches", 0),
        "quality_tracked": len(q.get("skills") or {}),
    }


def run_search(
    vault: Path,
    query: str,
    *,
    domain: str | None = None,
    tag: str | None = None,
    limit: int = 15,
    record: bool = True,
    as_json: bool = False,
) -> int:
    data = search_skills(
        vault, query, domain=domain, tag=tag, limit=limit, record=record
    )
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
    vault: Path, queries: list[str], *, limit: int = 10, record: bool = True
) -> list[dict[str, Any]]:
    bundles = []
    for q in queries:
        raw, domain, tag = parse_axon_query(str(q))
        bundles.append(
            {
                "query": q,
                "result": search_skills(
                    vault, raw, domain=domain, tag=tag, limit=limit, record=record
                ),
            }
        )
    return bundles


def run_for_profile(
    vault: Path,
    forge_id: str,
    *,
    limit: int = 10,
    record: bool = True,
    as_json: bool = False,
) -> int:
    """Run default axon_queries declared on a FORGE profile (+ corpus doctrine boost)."""
    from talaria_cli.cmds import forge as forge_cmd

    profile = forge_cmd.load_profile(vault, forge_id)
    if not profile:
        emit({"ok": False, "error": f"profile not found: {forge_id}"}, as_json or True)
        return EXIT_ERROR
    meta = profile.get("meta") or {}
    queries = _as_list(meta.get("axon_queries"))
    if not queries:
        specialty = str(meta.get("specialty") or forge_id)
        queries = [specialty.split("—")[0].strip()[:60] or forge_id]

    # Enrich with corpus doctrine keywords when Builder 2.0 corpus exists
    corpus_rel = str(meta.get("corpus_path") or "").strip()
    corpus_extra = []
    if corpus_rel:
        doctrine = vault / corpus_rel / "00-doctrine.md"
        if doctrine.is_file():
            corpus_extra.append(f"corpus:{corpus_rel}/00-doctrine.md")
            queries = list(queries) + [str(meta.get("specialty") or forge_id).split("—")[0].strip()[:40]]

    bundles = bundles_for_queries(vault, queries, limit=limit, record=record)
    data = {
        "command": "axon for-profile",
        "ok": True,
        "forge_id": forge_id,
        "axon_queries": queries,
        "corpus_path": corpus_rel or None,
        "corpus_notes": corpus_extra,
        "bundles": bundles,
        "feedback_hint": "talaria axon feedback --path <skills/...> --signal useful|noise",
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


def run_feedback(vault: Path, path: str, signal: str, *, as_json: bool = False) -> int:
    data = record_feedback(vault, path, signal)
    data["command"] = "axon feedback"
    emit(data, as_json or True)
    return EXIT_OK if data.get("ok") else EXIT_USAGE


def run_quality(vault: Path, *, limit: int = 20, as_json: bool = False) -> int:
    data = quality_report(vault, limit=limit)
    data["command"] = "axon quality"
    emit(data, as_json or True)
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
