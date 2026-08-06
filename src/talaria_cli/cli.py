from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from talaria_cli import __version__
from talaria_cli.agent_contract import agent_contract, connection_snippet
from talaria_cli.cmds import axon as axon_cmd
from talaria_cli.cmds import boot as boot_cmd
from talaria_cli.cmds import connect_apply as connect_apply_cmd
from talaria_cli.cmds import eval_cmd
from talaria_cli.cmds import forge as forge_cmd
from talaria_cli.cmds import forge_build as forge_build_cmd
from talaria_cli.cmds import forge_instruct as forge_instruct_cmd
from talaria_cli.cmds import import_chats as import_cmd
from talaria_cli.cmds import ingest as ingest_cmd
from talaria_cli.cmds import memory_cmd
from talaria_cli.cmds import session as session_cmd
from talaria_cli.cmds import smoke as smoke_cmd
from talaria_cli.cmds import status as status_cmd
from talaria_cli.cmds import verify as verify_cmd
from talaria_cli.mode import mode_contract, resolve_mode
from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit
from talaria_cli.vault import find_vault


HELP_SPINE = """
Talaria CLI — SPINE + órganos (TCOS).

describe | connect [--apply --yes] | mcp | doctor | smoke | status
session start|status|close
verify boot|close   forge list|show|check|run|build|instruct|invoke|graph
axon search|for-profile|stats|feedback|quality|pack
memory retrieve
eval list|show|run   mode get|set
Global: --vault PATH  --json  --mode strict|draft
"""


def _add_json(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("--json", action="store_true", help="JSON output")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="talaria",
        description="Talaria CLI — SPINE orchestration + agent connector (TCOS)",
    )
    p.add_argument("--vault", help="Absolute path to Talaria vault")
    p.add_argument("--json", action="store_true", help="JSON output when supported")
    p.add_argument(
        "--mode",
        choices=["strict", "draft"],
        help="SPINE mode (default: .talaria.mode or TALARIA_MODE or strict)",
    )
    p.add_argument("--version", action="version", version=f"talaria {__version__}")
    sub = p.add_subparsers(dest="command")

    for name, help_txt in (
        ("boot", "Install/verify tools"),
        ("doctor", "Check tools + organism structure"),
        ("status", "Show suit status"),
        ("vault", "Print vault path"),
        ("help", "Short command map"),
        ("describe", "Agent connection contract (JSON)"),
        ("mcp", "Run MCP stdio server for agents"),
        ("smoke", "Run Phase B smoke tests"),
    ):
        sp = sub.add_parser(name, help=help_txt)
        _add_json(sp)

    verify = sub.add_parser("verify", help="SPINE entry/exit gates")
    _add_json(verify)
    verify_sub = verify.add_subparsers(dest="verify_kind")
    vboot = verify_sub.add_parser("boot", help="Entry gate: organism + Mark")
    _add_json(vboot)
    vclose = verify_sub.add_parser("close", help="Exit gate: scorecard")
    _add_json(vclose)
    vclose.add_argument("--scorecard", required=True, help="Path to filled scorecard .md")
    vclose.add_argument(
        "--draft",
        action="store_true",
        help="Allow close without done: true (draft mode)",
    )

    forge = sub.add_parser("forge", help="FORGE profiles (list/show/check/run/build/invoke/graph)")
    _add_json(forge)
    forge_sub = forge.add_subparsers(dest="forge_kind")
    flist = forge_sub.add_parser("list", help="List profiles")
    _add_json(flist)
    flist.add_argument("--ensembles", action="store_true", help="Include ensembles")
    flist.add_argument("--graph", action="store_true", help="Include user delegation graph")
    fshow = forge_sub.add_parser("show", help="Show one profile")
    _add_json(fshow)
    fshow.add_argument("profile_id", help="forge_id e.g. researcher")
    fcheck = forge_sub.add_parser("check", help="Validate profile and/or deliverable gates")
    _add_json(fcheck)
    fcheck.add_argument("--profile", required=True, dest="profile_id", help="forge_id")
    fcheck.add_argument("--deliverable", help="Path to deliverable .md with forge_gates")
    fcheck.add_argument(
        "--declare",
        help="Comma gates e.g. G1=pass,G2=pass,G3=pass",
    )
    fcheck.add_argument(
        "--require-axon",
        action="store_true",
        help="Require axon_skills cites (Gaxon) in deliverable",
    )
    frun = forge_sub.add_parser("run", help="Emit activation packet for agents")
    _add_json(frun)
    frun.add_argument("profile_id", help="forge_id")
    frun.add_argument(
        "--with-axon",
        action="store_true",
        default=True,
        help="Include AXON search (default on)",
    )
    frun.add_argument(
        "--no-axon",
        action="store_true",
        help="Skip AXON retrieve/hydrate",
    )
    frun.add_argument(
        "--no-hydrate",
        action="store_true",
        help="Search hits only — do not embed skill bodies",
    )
    frun.add_argument(
        "--no-memory",
        action="store_true",
        help="Skip memory retrieve",
    )
    frun.add_argument(
        "--pack",
        help="AXON skill pack id (e.g. software-delivery, youtube-channel)",
    )
    fbuild = forge_sub.add_parser(
        "build",
        help="Create draft FORGE agent/profile from a natural-language brief (Builder 2.0)",
    )
    _add_json(fbuild)
    fbuild.add_argument(
        "--brief",
        required=True,
        help='e.g. "crea un agente que sepa responder correos"',
    )
    fbuild.add_argument("--id", dest="forge_id", help="Optional forge_id (kebab-case)")
    fbuild.add_argument("--specialty", help="Override specialty one-liner")
    fbuild.add_argument("--deliverable", help="Override DoD deliverable description")
    fbuild.add_argument(
        "--kind",
        dest="role_kind",
        default="both",
        choices=["orchestrator", "specialist", "both"],
        help="User-owned role kind (default both)",
    )
    fbuild.add_argument(
        "--invocable-by-mode",
        default="open",
        choices=["open", "allowlist", "deny_direct"],
        help="Who may auto-invoke this agent (default open — owner always can forge run)",
    )
    fbuild.add_argument(
        "--invocable-by",
        help="Comma forge_ids that may invoke this specialist",
    )
    fbuild.add_argument(
        "--invokes",
        help="Comma forge_ids this orchestrator may delegate to",
    )
    fbuild.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing profile/corpus id",
    )
    finvoke = forge_sub.add_parser(
        "invoke",
        help="Delegate parent → child specialist (user-owned graph)",
    )
    _add_json(finvoke)
    finvoke.add_argument("parent_id", help="Parent / orchestrator forge_id")
    finvoke.add_argument("child_id", help="Child / specialist forge_id")
    finvoke.add_argument("--brief", help="Delegation brief for the child")
    finvoke.add_argument(
        "--strict",
        action="store_true",
        help="Hard-fail policy (missing invokes edge / allowlist)",
    )
    finvoke.add_argument(
        "--with-axon",
        action="store_true",
        default=True,
        help="Include AXON hydrate (default on)",
    )
    finvoke.add_argument(
        "--no-axon",
        action="store_true",
        help="Skip AXON retrieve/hydrate",
    )
    finvoke.add_argument(
        "--no-hydrate",
        action="store_true",
        help="Hits only — no skill bodies",
    )
    finvoke.add_argument(
        "--no-memory",
        action="store_true",
        help="Skip memory retrieve",
    )
    finvoke.add_argument(
        "--pack",
        help="AXON skill pack id for child activation",
    )
    finvoke.add_argument(
        "--deliverable",
        help="Child deliverable path to validate and close handoff",
    )
    finvoke.add_argument(
        "--artifact-in",
        help="Path/id of inbound artifact from parent",
    )
    finvoke.add_argument(
        "--require-deliverable",
        action="store_true",
        help="Fail unless --deliverable is provided and passes forge check",
    )
    fgraph = forge_sub.add_parser("graph", help="Show user delegation graph")
    _add_json(fgraph)
    finstruct = forge_sub.add_parser(
        "instruct",
        help="Auto-bootstrap doctrine/corpus for a profile (also runs inside forge build)",
    )
    _add_json(finstruct)
    finstruct.add_argument("profile_id", nargs="?", help="forge_id")
    finstruct.add_argument(
        "--all-drafts",
        action="store_true",
        help="Instruct all draft / built_from_brief profiles",
    )

    axon = sub.add_parser("axon", help="AXON skill search")
    _add_json(axon)
    axon_sub = axon.add_subparsers(dest="axon_kind")
    asearch = axon_sub.add_parser("search", help="Search skills/")
    _add_json(asearch)
    asearch.add_argument("query", help="Search terms")
    asearch.add_argument("--domain", help="Filter by domain folder/name")
    asearch.add_argument("--tag", help="Filter by tag")
    asearch.add_argument("--limit", type=int, default=15, help="Max hits (default 15)")
    asearch.add_argument("--no-record", action="store_true", help="Do not update axon-quality.json")
    afor = axon_sub.add_parser("for-profile", help="Run profile axon_queries")
    _add_json(afor)
    afor.add_argument("profile_id", help="forge_id")
    afor.add_argument("--limit", type=int, default=10)
    afor.add_argument("--no-record", action="store_true", help="Do not update axon-quality.json")
    astats = axon_sub.add_parser("stats", help="AXON counts")
    _add_json(astats)
    afeed = axon_sub.add_parser("feedback", help="Mark a skill useful|noise (quality loop)")
    _add_json(afeed)
    afeed.add_argument("--path", required=True, help="skills/... path")
    afeed.add_argument("--signal", required=True, choices=["useful", "noise"])
    aqual = axon_sub.add_parser("quality", help="Show AXON quality ranking")
    _add_json(aqual)
    aqual.add_argument("--limit", type=int, default=20)
    apack = axon_sub.add_parser("pack", help="Skill packs (curated mission sets)")
    apack_sub = apack.add_subparsers(dest="pack_kind")
    apack_list = apack_sub.add_parser("list", help="List packs")
    _add_json(apack_list)
    apack_show = apack_sub.add_parser("show", help="Show one pack")
    _add_json(apack_show)
    apack_show.add_argument("pack_id")

    mem = sub.add_parser("memory", help="Vault memory retrieve")
    _add_json(mem)
    mem_sub = mem.add_subparsers(dest="memory_kind")
    mret = mem_sub.add_parser("retrieve", help="Search memory/ Markdown")
    _add_json(mret)
    mret.add_argument("query", help="Search terms")
    mret.add_argument("--forge", dest="forge_id", help="Bias to forge corpus id")
    mret.add_argument("--limit", type=int, default=8)

    sess = sub.add_parser("session", help="SPINE session start/status/close (scorecard enforcement)")
    _add_json(sess)
    sess_sub = sess.add_subparsers(dest="session_kind")
    sstart = sess_sub.add_parser("start", help="Create scorecard + active session")
    _add_json(sstart)
    sstart.add_argument("--objective", required=True, help="Session objective")
    sstart.add_argument("--forge", dest="forge_profile", help="Optional forge_id")
    sstat = sess_sub.add_parser("status", help="Show active session")
    _add_json(sstat)
    sclose = sess_sub.add_parser("close", help="verify close on session scorecard")
    _add_json(sclose)
    sclose.add_argument("--draft", action="store_true", help="Allow draft close")

    connect = sub.add_parser("connect", help="Emit MCP/CLI snippets for a client")
    _add_json(connect)
    connect.add_argument(
        "--client",
        default="generic",
        choices=["cursor", "hermes", "claude", "claude-code", "generic"],
        help="Target agent/runtime",
    )
    connect.add_argument(
        "--write",
        action="store_true",
        help="Write fragment under tools/connect/<client>.json",
    )
    connect.add_argument(
        "--apply",
        action="store_true",
        help="Merge MCP fragment into the client config file",
    )
    connect.add_argument(
        "--yes",
        action="store_true",
        help="Required with --apply to confirm writing client config",
    )

    ingest = sub.add_parser("ingest", help="Ingest external content")
    _add_json(ingest)
    ingest_sub = ingest.add_subparsers(dest="ingest_kind")
    doc = ingest_sub.add_parser("doc", help="Convert document/URL via MarkItDown")
    _add_json(doc)
    doc.add_argument("source", help="File path or URL")
    doc.add_argument("-o", "--output", help="Optional output .md path")
    proj = ingest_sub.add_parser("project", help="Graphify a code project")
    _add_json(proj)
    proj.add_argument("path", help="Project directory")
    proj.add_argument("--name", help="Name under memory/graphs/")

    imp = sub.add_parser("import", help="Import historical data")
    _add_json(imp)
    imp_sub = imp.add_subparsers(dest="import_kind")
    chats = imp_sub.add_parser("chats", help="Import Hermes/Claude/Cursor chats")
    _add_json(chats)

    ev = sub.add_parser("eval", help="Ley II eval harness (gold tasks)")
    _add_json(ev)
    ev_sub = ev.add_subparsers(dest="eval_kind")
    elist = ev_sub.add_parser("list", help="List gold evals")
    _add_json(elist)
    eshow = ev_sub.add_parser("show", help="Show eval spec")
    _add_json(eshow)
    eshow.add_argument("eval_id")
    erun = ev_sub.add_parser("run", help="Score deliverable against rubric (or A/B fixtures)")
    _add_json(erun)
    erun.add_argument("eval_id")
    erun.add_argument(
        "--deliverable",
        required=False,
        default=None,
        help="Path to deliverable; omit to run baseline_fixture vs forge_fixture A/B",
    )
    erun.add_argument(
        "--ab",
        action="store_true",
        help="Force A/B comparison using fixtures in the eval spec",
    )

    mode_p = sub.add_parser("mode", help="Get/set SPINE mode strict|draft")
    _add_json(mode_p)
    mode_sub = mode_p.add_subparsers(dest="mode_kind")
    mget = mode_sub.add_parser("get", help="Show current mode")
    _add_json(mget)
    mset = mode_sub.add_parser("set", help="Persist mode to .talaria.mode")
    _add_json(mset)
    mset.add_argument("value", choices=["strict", "draft"])

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    if not argv:
        print(HELP_SPINE.strip())
        return EXIT_OK

    args = parser.parse_args(argv)
    as_json = bool(getattr(args, "json", False))

    if args.command in (None, "help"):
        print(HELP_SPINE.strip())
        return EXIT_OK

    try:
        vault = find_vault(args.vault)
    except FileNotFoundError as e:
        emit({"error": str(e)}, as_json or True)
        return EXIT_ERROR

    if args.command == "boot":
        return boot_cmd.run_boot(vault, check_only=False, as_json=as_json)
    if args.command == "doctor":
        return verify_cmd.run_doctor(vault, as_json=as_json)
    if args.command == "smoke":
        return smoke_cmd.run_smoke(vault, as_json=as_json)
    if args.command == "verify":
        mode = resolve_mode(vault, getattr(args, "mode", None))
        if args.verify_kind == "boot":
            data = verify_cmd.evaluate_boot(vault)
            data["mode"] = mode
            data["mode_contract"] = mode_contract(mode)
            sess = session_cmd.status_session(vault)
            data["session"] = {
                "active": sess.get("active"),
                "scorecard": (sess.get("session") or {}).get("scorecard"),
                "forge_profile": (sess.get("session") or {}).get("forge_profile"),
            }
            if mode == "draft":
                data["ok"] = True
                data["next"] = "Draft mode — Act allowed without hard gate (no guaranteed outcome)"
            elif not sess.get("active"):
                data["next"] = (
                    (data.get("next") or "")
                    + " | Recommended: talaria session start --objective \"...\" [--forge <id>]"
                ).strip(" |")
            verify_cmd._emit_verify(data, as_json)
            return EXIT_OK if data["ok"] else EXIT_ERROR
        if args.verify_kind == "close":
            allow = bool(getattr(args, "draft", False)) or mode == "draft"
            return verify_cmd.run_verify_close(
                vault,
                args.scorecard,
                allow_draft=allow,
                as_json=as_json,
            )
        parser.parse_args(["verify", "-h"])
        return EXIT_USAGE
    if args.command == "eval":
        if args.eval_kind == "list":
            return eval_cmd.run_list(vault, as_json=as_json)
        if args.eval_kind == "show":
            return eval_cmd.run_show(vault, args.eval_id, as_json=as_json)
        if args.eval_kind == "run":
            return eval_cmd.run_run(
                vault,
                args.eval_id,
                deliverable=args.deliverable,
                as_json=as_json,
                compare_fixtures=bool(getattr(args, "ab", False)),
            )
        parser.parse_args(["eval", "-h"])
        return EXIT_USAGE
    if args.command == "mode":
        if args.mode_kind == "get":
            m = resolve_mode(vault, getattr(args, "mode", None))
            emit({"command": "mode get", "mode": m, **mode_contract(m)}, as_json or True)
            return EXIT_OK
        if args.mode_kind == "set":
            (vault / ".talaria.mode").write_text(args.value + "\n", encoding="utf-8")
            emit(
                {"command": "mode set", "mode": args.value, **mode_contract(args.value)},
                as_json or True,
            )
            return EXIT_OK
        parser.parse_args(["mode", "-h"])
        return EXIT_USAGE
    if args.command == "forge":
        if args.forge_kind == "list":
            return forge_cmd.run_list(
                vault,
                ensembles=bool(getattr(args, "ensembles", False)),
                graph=bool(getattr(args, "graph", False)),
                as_json=as_json,
            )
        if args.forge_kind == "show":
            return forge_cmd.run_show(vault, args.profile_id, as_json=as_json)
        if args.forge_kind == "check":
            return forge_cmd.run_check(
                vault,
                args.profile_id,
                deliverable=getattr(args, "deliverable", None),
                declare=getattr(args, "declare", None),
                require_axon=bool(getattr(args, "require_axon", False)),
                as_json=as_json,
            )
        if args.forge_kind == "run":
            no_axon = bool(getattr(args, "no_axon", False))
            return forge_cmd.run_run(
                vault,
                args.profile_id,
                with_axon=not no_axon,
                hydrate=not no_axon and not bool(getattr(args, "no_hydrate", False)),
                with_memory=not bool(getattr(args, "no_memory", False)),
                pack=getattr(args, "pack", None),
                as_json=as_json,
            )
        if args.forge_kind == "build":
            return forge_build_cmd.run_build(
                vault,
                args.brief,
                forge_id=getattr(args, "forge_id", None),
                specialty=getattr(args, "specialty", None),
                deliverable=getattr(args, "deliverable", None),
                force=bool(getattr(args, "force", False)),
                role_kind=getattr(args, "role_kind", "both") or "both",
                invocable_by_mode=getattr(args, "invocable_by_mode", "open") or "open",
                invocable_by=getattr(args, "invocable_by", None),
                invokes=getattr(args, "invokes", None),
                as_json=as_json,
            )
        if args.forge_kind == "invoke":
            no_axon = bool(getattr(args, "no_axon", False))
            return forge_cmd.run_invoke(
                vault,
                args.parent_id,
                args.child_id,
                brief=getattr(args, "brief", None),
                strict=bool(getattr(args, "strict", False)),
                with_axon=not no_axon,
                hydrate=not no_axon and not bool(getattr(args, "no_hydrate", False)),
                with_memory=not bool(getattr(args, "no_memory", False)),
                pack=getattr(args, "pack", None),
                deliverable=getattr(args, "deliverable", None),
                artifact_in=getattr(args, "artifact_in", None),
                require_deliverable=bool(getattr(args, "require_deliverable", False)),
                as_json=as_json,
            )
        if args.forge_kind == "graph":
            return forge_cmd.run_graph(vault, as_json=as_json)
        if args.forge_kind == "instruct":
            return forge_instruct_cmd.run_instruct(
                vault,
                getattr(args, "profile_id", None),
                all_drafts=bool(getattr(args, "all_drafts", False)),
                as_json=as_json,
            )
        parser.parse_args(["forge", "-h"])
        return EXIT_USAGE
    if args.command == "session":
        if args.session_kind == "start":
            return session_cmd.run_start(
                vault,
                objective=args.objective,
                forge_profile=getattr(args, "forge_profile", None),
                as_json=as_json,
            )
        if args.session_kind == "status":
            return session_cmd.run_status(vault, as_json=as_json)
        if args.session_kind == "close":
            return session_cmd.close_session(
                vault, as_json=as_json, allow_draft=bool(getattr(args, "draft", False))
            )
        parser.parse_args(["session", "-h"])
        return EXIT_USAGE
    if args.command == "axon":
        if args.axon_kind == "search":
            return axon_cmd.run_search(
                vault,
                args.query,
                domain=getattr(args, "domain", None),
                tag=getattr(args, "tag", None),
                limit=int(getattr(args, "limit", 15) or 15),
                record=not bool(getattr(args, "no_record", False)),
                as_json=as_json,
            )
        if args.axon_kind == "for-profile":
            return axon_cmd.run_for_profile(
                vault,
                args.profile_id,
                limit=int(getattr(args, "limit", 10) or 10),
                record=not bool(getattr(args, "no_record", False)),
                as_json=as_json,
            )
        if args.axon_kind == "stats":
            data = axon_cmd.axon_stats(vault)
            data["command"] = "axon stats"
            emit(data, as_json or True)
            return EXIT_OK if data.get("ok") else EXIT_ERROR
        if args.axon_kind == "feedback":
            return axon_cmd.run_feedback(
                vault, args.path, args.signal, as_json=as_json
            )
        if args.axon_kind == "quality":
            return axon_cmd.run_quality(
                vault, limit=int(getattr(args, "limit", 20) or 20), as_json=as_json
            )
        if args.axon_kind == "pack":
            from talaria_cli.cmds.context_hydrate import list_packs, load_pack

            if getattr(args, "pack_kind", None) == "list":
                packs = list_packs(vault)
                emit({"ok": True, "command": "axon pack list", "packs": packs}, as_json or True)
                return EXIT_OK
            if getattr(args, "pack_kind", None) == "show":
                pack = load_pack(vault, args.pack_id)
                if not pack:
                    emit({"ok": False, "error": f"pack not found: {args.pack_id}"}, True)
                    return EXIT_ERROR
                emit({"ok": True, "command": "axon pack show", "pack": pack}, as_json or True)
                return EXIT_OK
            parser.parse_args(["axon", "pack", "-h"])
            return EXIT_USAGE
        parser.parse_args(["axon", "-h"])
        return EXIT_USAGE
    if args.command == "memory":
        if getattr(args, "memory_kind", None) == "retrieve":
            return memory_cmd.run_retrieve(
                vault,
                args.query,
                forge_id=getattr(args, "forge_id", None),
                limit=int(getattr(args, "limit", 8) or 8),
                as_json=as_json,
            )
        parser.parse_args(["memory", "-h"])
        return EXIT_USAGE
    if args.command == "status":
        return status_cmd.run_status(vault, as_json=as_json)
    if args.command == "vault":
        emit({"vault": str(vault)} if as_json else str(vault), as_json)
        return EXIT_OK
    if args.command == "describe":
        emit(agent_contract(vault), True)  # always JSON — for agents
        return EXIT_OK
    if args.command == "connect":
        if getattr(args, "apply", False):
            return connect_apply_cmd.run_apply(
                vault, args.client, yes=bool(getattr(args, "yes", False)), as_json=True
            )
        data = connection_snippet(vault, args.client)
        if args.write:
            out_dir = vault / "tools" / "connect"
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"{args.client}.json"
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            data = {**data, "written": str(out)}
        data["apply_hint"] = "talaria connect --client cursor --apply --yes"
        emit(data, True)
        return EXIT_OK
    if args.command == "mcp":
        from talaria_cli.mcp_server import serve

        return serve(vault)
    if args.command == "ingest":
        if args.ingest_kind == "doc":
            return ingest_cmd.run_ingest_doc(vault, args.source, args.output, as_json=as_json)
        if args.ingest_kind == "project":
            return ingest_cmd.run_ingest_project(
                vault, args.path, getattr(args, "name", None), as_json=as_json
            )
        parser.parse_args(["ingest", "-h"])
        return EXIT_USAGE
    if args.command == "import":
        if args.import_kind == "chats":
            return import_cmd.run_import_chats(vault, as_json=as_json)
        parser.parse_args(["import", "-h"])
        return EXIT_USAGE

    emit({"error": f"unknown command: {args.command}"}, as_json)
    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())
