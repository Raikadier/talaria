"""Eval harness — Phase E (Ley II measurable via gold tasks + rubrics)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit

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
                "has_ab_fixtures": bool(data.get("baseline_fixture") and data.get("forge_fixture")),
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
        needles_any = item.get("must_contain_any") or item.get("must_contain") or []
        needles_all = item.get("must_contain_all") or []
        if isinstance(needles_any, str):
            needles_any = [needles_any]
        if isinstance(needles_all, str):
            needles_all = [needles_all]
        ok = True
        missing: list[str] = []
        if needles_any:
            if not any(n.lower() in text_l for n in needles_any):
                ok = False
                missing.extend(needles_any)
        for n in needles_all:
            if n.lower() not in text_l:
                ok = False
                missing.append(n)
        if item.get("require_checkbox_done"):
            label = (item.get("label") or "").lower()
            if label and f"[x] {label}" not in text_l and f"[X] {label}" not in text:
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
            ab = " A/B" if e.get("has_ab_fixtures") else ""
            print(f"  - {e['id']}: {e.get('title')} (rubric={e.get('rubric_count')}){ab}")
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
    deliverable: str | None = None,
    as_json: bool = False,
    compare_fixtures: bool = False,
) -> int:
    spec = load_eval(vault, eval_id)
    if not spec:
        emit({"ok": False, "error": f"eval not found: {eval_id}"}, as_json or True)
        return EXIT_ERROR

    if compare_fixtures or not deliverable:
        base_rel = spec.get("baseline_fixture")
        forge_rel = spec.get("forge_fixture")
        if base_rel and forge_rel:
            base_path = vault / base_rel
            forge_path = vault / forge_rel
            if base_path.is_file() and forge_path.is_file():
                base_r = evaluate_deliverable_against_eval(spec, base_path)
                forge_r = evaluate_deliverable_against_eval(spec, forge_path)
                ley2 = (not base_r["ok"]) and forge_r["ok"]
                data = {
                    "command": "eval run",
                    "ok": ley2,
                    "mode": "a_b_fixtures",
                    "eval_id": eval_id,
                    "baseline": base_r,
                    "forge": forge_r,
                    "ley_II_hold": ley2,
                    "delta_score": round(forge_r["score"] - base_r["score"], 1),
                    "next": "Ley II evidence: forge fixture beats baseline"
                    if ley2
                    else "Forge fixture did not beat baseline — improve profile/rubric/fixture",
                }
                if as_json:
                    emit(data, True)
                else:
                    print(
                        f"eval {eval_id} A/B: {'PASS' if ley2 else 'FAIL'} "
                        f"baseline={base_r['score']}% forge={forge_r['score']}% "
                        f"delta={data['delta_score']}"
                    )
                return EXIT_OK if ley2 else EXIT_ERROR

    if not deliverable:
        emit(
            {
                "ok": False,
                "error": "deliverable required (or define baseline_fixture+forge_fixture)",
            },
            as_json or True,
        )
        return EXIT_USAGE

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
            miss = f" missing={c['missing']}" if c.get("missing") and not c["ok"] else ""
            print(f"  [{'OK' if c['ok'] else 'X'}] {c['id']}{miss}")
    return EXIT_OK if result["ok"] else EXIT_ERROR
