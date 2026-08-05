"""Eval harness — Phase E (Ley II measurable via gold tasks + rubrics)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from talaria_cli.util import EXIT_ERROR, EXIT_OK, emit

EVALS_DIR = Path("_META/evals")


def list_evals(vault: Path) -> list[dict[str, Any]]:
    root = vault / EVALS_DIR
    if not root.is_dir():
        return []
    out = []
    for path in sorted(root.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            out.append({"id": path.stem, "ok": False, "error": str(e)})
            continue
        out.append(
            {
                "id": data.get("id") or path.stem,
                "title": data.get("title"),
                "forge_profile": data.get("forge_profile"),
                "rubric_count": len(data.get("rubric") or []),
                "path": str(path.relative_to(vault)).replace("\\", "/"),
            }
        )
    return out


def load_eval(vault: Path, eval_id: str) -> dict[str, Any] | None:
    path = vault / EVALS_DIR / f"{eval_id}.json"
    if not path.is_file():
        for p in (vault / EVALS_DIR).glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("id") == eval_id:
                return data
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_deliverable_against_eval(
    spec: dict[str, Any], deliverable: Path
) -> dict[str, Any]:
    text = deliverable.read_text(encoding="utf-8")
    text_l = text.lower()
    checks = []
    for item in spec.get("rubric") or []:
        rid = item.get("id") or item.get("name") or "item"
        needles = item.get("must_contain") or []
        if isinstance(needles, str):
            needles = [needles]
        ok = True
        missing = []
        for n in needles:
            if n.lower() not in text_l:
                ok = False
                missing.append(n)
        # checkbox style: if require_checked
        if item.get("require_checkbox_done"):
            # look for - [x] near label
            label = (item.get("label") or "").lower()
            if label and f"[x] {label}" not in text_l and f"[X] {label}" not in text:
                # softer: any [x] count
                if text_l.count("- [x]") < 1:
                    ok = False
                    missing.append("checked checkbox")
        checks.append(
            {
                "id": rid,
                "ok": ok,
                "missing": missing,
                "weight": item.get("weight", 1),
                "description": item.get("description") or item.get("label") or "",
            }
        )
    passed = sum(1 for c in checks if c["ok"])
    total = len(checks) or 1
    score = round(100.0 * passed / total, 1)
    threshold = float(spec.get("pass_score", 80))
    return {
        "eval_id": spec.get("id"),
        "deliverable": str(deliverable),
        "passed": passed,
        "total": total,
        "score": score,
        "pass_score": threshold,
        "ok": score >= threshold,
        "checks": checks,
        "baseline_note": spec.get("baseline_note"),
        "forge_advantage": spec.get("forge_advantage"),
    }


def run_list(vault: Path, *, as_json: bool = False) -> int:
    items = list_evals(vault)
    data = {"command": "eval list", "ok": True, "count": len(items), "evals": items}
    if as_json:
        emit(data, True)
    else:
        print(f"Evals: {len(items)}")
        for e in items:
            print(f"  - {e['id']}: {e.get('title')} (rubric={e.get('rubric_count')})")
    return EXIT_OK


def run_show(vault: Path, eval_id: str, *, as_json: bool = False) -> int:
    spec = load_eval(vault, eval_id)
    if not spec:
        emit({"ok": False, "error": f"eval not found: {eval_id}"}, as_json or True)
        return EXIT_ERROR
    data = {"command": "eval show", "ok": True, "eval": spec}
    emit(data, as_json or True)
    return EXIT_OK


def run_run(
    vault: Path,
    eval_id: str,
    *,
    deliverable: str,
    as_json: bool = False,
) -> int:
    spec = load_eval(vault, eval_id)
    if not spec:
        emit({"ok": False, "error": f"eval not found: {eval_id}"}, as_json or True)
        return EXIT_ERROR
    path = Path(deliverable)
    if not path.is_file():
        path = vault / deliverable
    if not path.is_file():
        emit({"ok": False, "error": f"deliverable not found: {deliverable}"}, as_json or True)
        return EXIT_ERROR
    result = evaluate_deliverable_against_eval(spec, path)
    data = {
        "command": "eval run",
        "ok": result["ok"],
        "result": result,
        "next": "Ley II evidence recorded" if result["ok"] else "Improve deliverable to meet rubric",
    }
    if as_json:
        emit(data, True)
    else:
        print(f"eval {eval_id}: {'PASS' if result['ok'] else 'FAIL'} score={result['score']}%")
        for c in result["checks"]:
            print(f"  [{'OK' if c['ok'] else 'X'}] {c['id']}" + (f" missing={c['missing']}" if c["missing"] else ""))
    return EXIT_OK if result["ok"] else EXIT_ERROR
