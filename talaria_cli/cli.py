from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from talaria_cli import __version__
from talaria_cli.agent_contract import agent_contract, connection_snippet
from talaria_cli.cmds import axon as axon_cmd
from talaria_cli.cmds import boot as boot_cmd
from talaria_cli.cmds import eval_cmd
from talaria_cli.cmds import forge as forge_cmd
from talaria_cli.cmds import import_chats as import_cmd
from talaria_cli.cmds import ingest as ingest_cmd
from talaria_cli.cmds import smoke as smoke_cmd
from talaria_cli.cmds import status as status_cmd
from talaria_cli.cmds import verify as verify_cmd
from talaria_cli.mode import mode_contract, resolve_mode
from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit
from talaria_cli.vault import find_vault


HELP_SPINE = """
Talaria CLI — SPINE + órganos (TCOS).

describe | connect | mcp | doctor | smoke | status
verify boot|close   forge list|show|check|run
axon search|for-profile|stats
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

    forge = sub.add_parser("forge", help="FORGE profiles (list/show/check/run)")
    _add_json(forge)
    forge_sub = forge.add_subparsers(dest="forge_kind")
    flist = forge_sub.add_parser("list", help="List profiles")
    _add_json(flist)
    flist.add_argument("--ensembles", action="store_true", help="Include ensembles")
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
    frun = forge_sub.add_parser("run", help="Emit activation packet for agents")
    _add_json(frun)
    frun.add_argument("profile_id", help="forge_id")
    frun.add_argument(
        "--with-axon",
        action="store_true",
        help="Include AXON search results from profile axon_queries",
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
    afor = axon_sub.add_parser("for-profile", help="Run profile axon_queries")
    _add_json(afor)
    afor.add_argument("profile_id", help="forge_id")
    afor.add_argument("--limit", type=int, default=10)
    astats = axon_sub.add_parser("stats", help="AXON counts")
    _add_json(astats)

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
    erun = ev_sub.add_parser("run", help="Score deliverable against rubric")
    _add_json(erun)
    erun.add_argument("eval_id")
    erun.add_argument("--deliverable", required=True)

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
            if mode == "draft":
                data["ok"] = True
                data["next"] = "Draft mode — Act allowed without hard gate (no guaranteed outcome)"
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
                vault, args.eval_id, deliverable=args.deliverable, as_json=as_json
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
                vault, ensembles=bool(getattr(args, "ensembles", False)), as_json=as_json
            )
        if args.forge_kind == "show":
            return forge_cmd.run_show(vault, args.profile_id, as_json=as_json)
        if args.forge_kind == "check":
            return forge_cmd.run_check(
                vault,
                args.profile_id,
                deliverable=getattr(args, "deliverable", None),
                declare=getattr(args, "declare", None),
                as_json=as_json,
            )
        if args.forge_kind == "run":
            return forge_cmd.run_run(
                vault,
                args.profile_id,
                with_axon=bool(getattr(args, "with_axon", False)),
                as_json=as_json,
            )
        parser.parse_args(["forge", "-h"])
        return EXIT_USAGE
    if args.command == "axon":
        if args.axon_kind == "search":
            return axon_cmd.run_search(
                vault,
                args.query,
                domain=getattr(args, "domain", None),
                tag=getattr(args, "tag", None),
                limit=int(getattr(args, "limit", 15) or 15),
                as_json=as_json,
            )
        if args.axon_kind == "for-profile":
            return axon_cmd.run_for_profile(
                vault,
                args.profile_id,
                limit=int(getattr(args, "limit", 10) or 10),
                as_json=as_json,
            )
        if args.axon_kind == "stats":
            data = axon_cmd.axon_stats(vault)
            data["command"] = "axon stats"
            emit(data, as_json or True)
            return EXIT_OK if data.get("ok") else EXIT_ERROR
        parser.parse_args(["axon", "-h"])
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
        data = connection_snippet(vault, args.client)
        if args.write:
            out_dir = vault / "tools" / "connect"
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"{args.client}.json"
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            data = {**data, "written": str(out)}
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
