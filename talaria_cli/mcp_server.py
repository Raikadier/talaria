"""MCP stdio server — lets any MCP client drive Talaria SPINE tools.

Run:
  talaria.mcp_server --vault <path>
  talaria mcp
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _ensure_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


_ensure_path()

from talaria_cli.agent_contract import agent_contract  # noqa: E402
from talaria_cli.cmds import axon as axon_cmd  # noqa: E402
from talaria_cli.cmds import boot as boot_cmd  # noqa: E402
from talaria_cli.cmds import forge as forge_cmd  # noqa: E402
from talaria_cli.cmds import import_chats as import_cmd  # noqa: E402
from talaria_cli.cmds import ingest as ingest_cmd  # noqa: E402
from talaria_cli.cmds import smoke as smoke_cmd  # noqa: E402
from talaria_cli.cmds import status as status_cmd  # noqa: E402
from talaria_cli.cmds import verify as verify_cmd  # noqa: E402
from talaria_cli.vault import find_vault  # noqa: E402


TOOLS = [
    {
        "name": "talaria_describe",
        "description": "Return Talaria agent connection contract (commands, MCP, rules).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_doctor",
        "description": "Check tools + organism structure (Phase B doctor).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_boot",
        "description": "Install missing Talaria tools (markitdown, graphify, obsidian-mcp).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_status",
        "description": "Return suit status: vault path, Mark level, tool presence.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_vault_path",
        "description": "Return absolute path to the Talaria vault.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_verify_boot",
        "description": "SPINE entry gate: organism integrity + Mark >= Mk.1.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_verify_close",
        "description": "SPINE exit gate: validate a session scorecard markdown file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scorecard": {"type": "string", "description": "Path to scorecard .md"},
                "draft": {"type": "boolean", "description": "Allow close without done:true"},
            },
            "required": ["scorecard"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_smoke",
        "description": "Run Phase B smoke suite (describe, organism, verify, AXON, FORGE).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_forge_list",
        "description": "List FORGE profiles (and optionally ensembles).",
        "inputSchema": {
            "type": "object",
            "properties": {"ensembles": {"type": "boolean"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_show",
        "description": "Show a FORGE profile: gates, DoD, activation.",
        "inputSchema": {
            "type": "object",
            "properties": {"profile": {"type": "string"}},
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_check",
        "description": "Validate FORGE profile structure and optional deliverable gates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "deliverable": {"type": "string"},
                "declare": {"type": "string", "description": "G1=pass,G2=pass,..."},
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_run",
        "description": "Emit FORGE activation packet for agents.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "with_axon": {"type": "boolean", "description": "Include AXON search hits"},
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_search",
        "description": "Search AXON skills/ by query text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "domain": {"type": "string"},
                "tag": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_for_profile",
        "description": "Run default axon_queries from a FORGE profile.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_stats",
        "description": "AXON skill and domain counts.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_ingest_doc",
        "description": "Convert a document or URL to Markdown into memory/inbox/converted.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "File path or URL"},
                "output": {"type": "string", "description": "Optional output .md path"},
            },
            "required": ["source"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_ingest_project",
        "description": "Run Graphify on a code project and mirror outputs to memory/graphs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Project directory"},
                "name": {"type": "string", "description": "Optional graph folder name"},
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_import_chats",
        "description": "Import Hermes / Claude Code / Cursor chats into memory/conversations.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


class TalariaMCP:
    def __init__(self, vault: Path):
        self.vault = vault

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        if name == "talaria_describe":
            return agent_contract(self.vault)
        if name == "talaria_doctor":
            code = verify_cmd.run_doctor(self.vault, as_json=True)
            return {"ok": code == 0, "exit": code}
        if name == "talaria_boot":
            code = boot_cmd.run_boot(self.vault, check_only=False, as_json=True)
            return {"ok": code == 0, "exit": code}
        if name == "talaria_status":
            return status_cmd.get_status(self.vault)
        if name == "talaria_vault_path":
            return {"vault": str(self.vault)}
        if name == "talaria_verify_boot":
            return verify_cmd.evaluate_boot(self.vault)
        if name == "talaria_verify_close":
            return verify_cmd.evaluate_close(
                self.vault,
                arguments["scorecard"],
                allow_draft=bool(arguments.get("draft")),
            )
        if name == "talaria_smoke":
            code = smoke_cmd.run_smoke(self.vault, as_json=True)
            return {"ok": code == 0, "exit": code}
        if name == "talaria_forge_list":
            profiles = forge_cmd.list_profiles(self.vault)
            data: dict[str, Any] = {"ok": True, "count": len(profiles), "profiles": profiles}
            if arguments.get("ensembles"):
                data["ensembles"] = forge_cmd.list_ensembles(self.vault)
            return data
        if name == "talaria_forge_show":
            profile = forge_cmd.load_profile(self.vault, arguments["profile"])
            if not profile:
                return {"ok": False, "error": f"profile not found: {arguments['profile']}"}
            return {
                "ok": True,
                "profile": {
                    "forge_id": profile["forge_id"],
                    "path": profile["rel_path"],
                    "meta": profile["meta"],
                    "gates": profile["gates"],
                    "dod": profile["dod"],
                    "activation": profile["activation"],
                },
                "structure": forge_cmd.evaluate_profile_structure(profile),
            }
        if name == "talaria_forge_check":
            profile = forge_cmd.load_profile(self.vault, arguments["profile"])
            if not profile:
                return {"ok": False, "error": f"profile not found: {arguments['profile']}"}
            struct = forge_cmd.evaluate_profile_structure(profile)
            parts: list[dict[str, Any]] = [struct]
            overall = struct["ok"]
            if arguments.get("deliverable") or arguments.get("declare"):
                declare = forge_cmd._parse_declare(arguments.get("declare"))
                if arguments.get("deliverable"):
                    path = Path(arguments["deliverable"])
                    if not path.is_file():
                        path = self.vault / arguments["deliverable"]
                    if not path.is_file():
                        return {"ok": False, "error": f"deliverable not found: {arguments['deliverable']}"}
                    deliv = forge_cmd.evaluate_deliverable(profile, path, declare=declare)
                else:
                    import tempfile

                    with tempfile.NamedTemporaryFile(
                        "w", suffix=".md", delete=False, encoding="utf-8"
                    ) as f:
                        f.write(f"---\nforge_profile: {arguments['profile']}\n---\n")
                        for k, v in declare.items():
                            f.write(f"{k}: {v}\n")
                        tmp = Path(f.name)
                    try:
                        deliv = forge_cmd.evaluate_deliverable(profile, tmp, declare=declare)
                    finally:
                        tmp.unlink(missing_ok=True)
                parts.append(deliv)
                overall = overall and deliv["ok"]
            return {
                "ok": overall,
                "forge_id": arguments["profile"],
                "results": parts,
            }
        if name == "talaria_forge_run":
            profile = forge_cmd.load_profile(self.vault, arguments["profile"])
            if not profile:
                return {"ok": False, "error": f"profile not found: {arguments['profile']}"}
            struct = forge_cmd.evaluate_profile_structure(profile)
            if not struct["ok"]:
                return {"ok": False, "error": "profile fails structural check", "structure": struct}
            meta = profile.get("meta") or {}
            qlist = meta.get("axon_queries") or []
            if isinstance(qlist, str):
                qlist = [qlist]
            packet: dict[str, Any] = {
                "ok": True,
                "forge_id": arguments["profile"],
                "activation": profile.get("activation"),
                "gates": profile["gates"],
                "dod": profile["dod"],
                "path": profile["rel_path"],
                "specialty": meta.get("specialty"),
                "axon_queries": qlist,
            }
            if arguments.get("with_axon"):
                queries = qlist or [str(meta.get("specialty") or arguments["profile"])[:60]]
                packet["axon"] = axon_cmd.bundles_for_queries(self.vault, queries, limit=8)
            return packet
        if name == "talaria_axon_search":
            return axon_cmd.search_skills(
                self.vault,
                arguments["query"],
                domain=arguments.get("domain"),
                tag=arguments.get("tag"),
                limit=int(arguments.get("limit") or 15),
            )
        if name == "talaria_axon_for_profile":
            profile = forge_cmd.load_profile(self.vault, arguments["profile"])
            if not profile:
                return {"ok": False, "error": f"profile not found: {arguments['profile']}"}
            meta = profile.get("meta") or {}
            queries = meta.get("axon_queries") or [
                str(meta.get("specialty") or arguments["profile"])[:60]
            ]
            if isinstance(queries, str):
                queries = [queries]
            bundles = axon_cmd.bundles_for_queries(
                self.vault, queries, limit=int(arguments.get("limit") or 10)
            )
            return {
                "ok": True,
                "forge_id": arguments["profile"],
                "axon_queries": queries,
                "bundles": bundles,
            }
        if name == "talaria_axon_stats":
            return axon_cmd.axon_stats(self.vault)
        if name == "talaria_ingest_doc":
            code = ingest_cmd.run_ingest_doc(
                self.vault, arguments["source"], arguments.get("output"), as_json=True
            )
            return {"ok": code == 0, "exit": code, "source": arguments["source"]}
        if name == "talaria_ingest_project":
            code = ingest_cmd.run_ingest_project(
                self.vault, arguments["path"], arguments.get("name"), as_json=True
            )
            return {"ok": code == 0, "exit": code, "path": arguments["path"]}
        if name == "talaria_import_chats":
            code = import_cmd.run_import_chats(self.vault, as_json=True)
            return {"ok": code == 0, "exit": code}
        return {"error": f"unknown tool: {name}"}


def _read_message() -> dict[str, Any] | None:
    """Read one JSON-RPC message from stdin (Content-Length or newline JSON)."""
    # Try Content-Length framing first
    header = b""
    while True:
        ch = sys.stdin.buffer.read(1)
        if not ch:
            return None
        header += ch
        if header.endswith(b"\r\n\r\n"):
            break
        # If we somehow get a raw JSON object without headers
        if header.startswith(b"{") and b"\n" in header:
            line = header.decode("utf-8", errors="replace").strip()
            return json.loads(line)

    text = header.decode("utf-8", errors="replace")
    length = None
    for line in text.split("\r\n"):
        if line.lower().startswith("content-length:"):
            length = int(line.split(":", 1)[1].strip())
    if length is None:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def _send(msg: dict[str, Any]) -> None:
    data = json.dumps(msg, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii") + data)
    sys.stdout.buffer.flush()


def _result(req_id: Any, result: Any) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _error(req_id: Any, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def serve(vault: Path) -> int:
    api = TalariaMCP(vault)
    # silence tool print noise into stderr so stdio RPC stays clean
    # (boot/status print to stdout — redirect temporarily in call)

    while True:
        try:
            msg = _read_message()
        except Exception as e:
            # cannot recover framing
            sys.stderr.write(f"mcp read error: {e}\n")
            return 1
        if msg is None:
            return 0

        method = msg.get("method")
        req_id = msg.get("id")
        params = msg.get("params") or {}

        if method == "initialize":
            _result(
                req_id,
                {
                    "protocolVersion": params.get("protocolVersion") or "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "talaria", "version": "0.1.0"},
                },
            )
            continue
        if method == "notifications/initialized":
            continue
        if method == "tools/list":
            _result(req_id, {"tools": TOOLS})
            continue
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            try:
                # keep RPC stdout clean: capture prints
                import contextlib
                import io

                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    payload = api.call(name, arguments)
                text = json.dumps(payload, ensure_ascii=False, indent=2)
                logs = buf.getvalue().strip()
                if logs:
                    text = text + "\n\n--- logs ---\n" + logs[-4000:]
                _result(
                    req_id,
                    {"content": [{"type": "text", "text": text}], "isError": bool(payload.get("error"))},
                )
            except Exception as e:
                _result(
                    req_id,
                    {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True},
                )
            continue
        if method == "ping":
            _result(req_id, {})
            continue
        if req_id is not None:
            _error(req_id, -32601, f"Method not found: {method}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Talaria MCP server (stdio)")
    p.add_argument("--vault", help="Vault path")
    args = p.parse_args(argv)
    vault = find_vault(args.vault)
    return serve(vault)


if __name__ == "__main__":
    raise SystemExit(main())
