"""Smoke tests for Talaria API + organism (Phase B)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from talaria_cli.agent_contract import agent_contract
from talaria_cli.cmds import status as status_cmd
from talaria_cli.cmds import verify as verify_cmd
from talaria_cli.util import EXIT_ERROR, EXIT_OK, emit


def run_smoke(vault: Path, *, as_json: bool = False) -> int:
    results: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append({"name": name, "ok": ok, "detail": detail})

    try:
        contract = agent_contract(vault)
        check(
            "describe_parseable",
            isinstance(contract, dict) and contract.get("name") == "talaria",
            f"version={contract.get('version')}",
        )
        cmds = {c["name"] for c in contract.get("cli", {}).get("commands", [])}
        check(
            "describe_has_verify",
            any(n.startswith("verify") for n in cmds),
            str(sorted(cmds)),
        )
        check("describe_has_organs", isinstance(contract.get("organs"), list) and len(contract["organs"]) >= 5, str(contract.get("organs")))
        check("describe_has_smoke", "smoke" in cmds, "")
    except Exception as e:
        check("describe_parseable", False, str(e))

    org = verify_cmd.organism_checks(vault)
    check("organism_ok", org["ok"], f"skills={org['skills_md_count']} profiles={org['forge_profiles']}")

    boot = verify_cmd.evaluate_boot(vault)
    check("verify_boot", boot["ok"], f"mark={boot.get('mark')}")

    skill = next((vault / "skills").rglob("*.md"), None) if (vault / "skills").is_dir() else None
    check("axon_skill_readable", bool(skill and skill.is_file()), str(skill) if skill else "none")
    profile = next((vault / "_META/forge/profiles").glob("*.md"), None)
    check("forge_profile_readable", bool(profile and profile.is_file()), str(profile) if profile else "none")

    sc_dir = vault / "memory" / "inbox"
    sc_dir.mkdir(parents=True, exist_ok=True)
    sc_path = sc_dir / "_smoke_scorecard.md"
    sc_path.write_text(
        """---
date: 2026-07-28
type: scorecard
mode: strict
objective: smoke test close gate
organs_used: [spine, api]
evidence: ["[[Home]]"]
gates: pass
forge_profile: ""
delta_vs_generic: ["smoke"]
done: true
---

# Smoke scorecard
[[Home]]
""",
        encoding="utf-8",
    )
    close = verify_cmd.evaluate_close(vault, sc_path)
    check("verify_close", close["ok"], close.get("error") or "")
    try:
        sc_path.unlink(missing_ok=True)
    except Exception:
        pass

    st = status_cmd.get_status(vault)
    check("status_shape", "vault" in st and "mark" in st and st.get("pipeline") == "spine", str(st.get("mark")))

    # Phase C — FORGE
    try:
        from talaria_cli.cmds import forge as forge_cmd

        profiles = forge_cmd.list_profiles(vault)
        check("forge_list", len(profiles) >= 1, str(len(profiles)))
        sample_id = profiles[0]["forge_id"] if profiles else "researcher"
        prof = forge_cmd.load_profile(vault, sample_id)
        check("forge_show_load", prof is not None, sample_id)
        if prof:
            struct = forge_cmd.evaluate_profile_structure(prof)
            check("forge_structure", struct["ok"], sample_id)
            gate_ids = [g["id"] for g in prof.get("gates") or []]
            if gate_ids:
                import tempfile

                with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
                    f.write(f"---\nforge_profile: {sample_id}\n---\n")
                    for g in gate_ids:
                        f.write(f"{g}: pass\n")
                    tmp = Path(f.name)
                try:
                    deliv = forge_cmd.evaluate_deliverable(
                        prof, tmp, declare={g: "pass" for g in gate_ids}
                    )
                finally:
                    tmp.unlink(missing_ok=True)
                check("forge_check_deliverable", struct["ok"] and deliv["ok"], sample_id)
            else:
                check("forge_check_deliverable", False, "no gates parsed")

        # Phase D — AXON
        from talaria_cli.cmds import axon as axon_cmd

        stats = axon_cmd.axon_stats(vault)
        check("axon_stats", bool(stats.get("ok") and stats.get("skills_md", 0) > 0), str(stats.get("skills_md")))
        sr = axon_cmd.search_skills(vault, "refactor coding", limit=5)
        check("axon_search", bool(sr.get("ok") and sr.get("hit_count", 0) >= 1), str(sr.get("hit_count")))
        fp = forge_cmd.load_profile(vault, "researcher")
        aq = (fp or {}).get("meta", {}).get("axon_queries") or []
        check("axon_queries_on_profile", len(aq) >= 1, str(aq)[:80])
        if aq:
            bundles = axon_cmd.bundles_for_queries(vault, aq[:2], limit=5)
            check(
                "axon_for_profile",
                all(b["result"].get("ok") for b in bundles),
                str([b["result"].get("hit_count") for b in bundles]),
            )
        else:
            check("axon_for_profile", False, "no axon_queries")

        # Phase E/F
        from talaria_cli.cmds import eval_cmd
        from talaria_cli.mode import mode_contract, resolve_mode

        evs = eval_cmd.list_evals(vault)
        check("eval_list", len(evs) >= 5, str(len(evs)))
        fixture = vault / "_META/evals/fixtures/research-brief-pass.md"
        if fixture.is_file():
            er = eval_cmd.evaluate_deliverable_against_eval(
                eval_cmd.load_eval(vault, "research-brief"), fixture
            )
            check("eval_run_fixture", er["ok"], f"score={er['score']}")
        else:
            check("eval_run_fixture", False, "missing fixture")
        m = resolve_mode(vault)
        check("mode_resolve", m in ("strict", "draft"), m)
        check("mode_contract", "promise" in mode_contract(m), m)
    except Exception as e:
        check("forge_list", False, str(e))

    ok = all(r["ok"] for r in results)
    data = {
        "command": "smoke",
        "ok": ok,
        "vault": str(vault),
        "passed": sum(1 for r in results if r["ok"]),
        "total": len(results),
        "results": results,
    }
    if as_json:
        emit(data, True)
    else:
        print(f"Smoke: {data['passed']}/{data['total']} — {'PASS' if ok else 'FAIL'}")
        for r in results:
            print(f"  [{'OK' if r['ok'] else 'X'}] {r['name']}" + (f" — {r['detail']}" if r["detail"] else ""))
    return EXIT_OK if ok else EXIT_ERROR
