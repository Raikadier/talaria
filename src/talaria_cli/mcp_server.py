"""MCP stdio server — universal suit API for any MCP client.

Parity rule: if `talaria <cmd>` can do it, there is a `talaria_*` MCP tool.

Run:
  python -m talaria_cli.mcp_server --vault <path>
  talaria mcp
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any


def _ensure_path() -> Path:
    # src/ layout: …/src/talaria_cli/mcp_server.py → parents[1] = src
    src = Path(__file__).resolve().parent.parent
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return src


_ensure_path()

from talaria_cli.agent_contract import agent_contract, connection_snippet  # noqa: E402
from talaria_cli.cmds import axon as axon_cmd  # noqa: E402
from talaria_cli.cmds import boot as boot_cmd  # noqa: E402
from talaria_cli.cmds import connect_apply as connect_apply_cmd  # noqa: E402
from talaria_cli.cmds import eval_cmd  # noqa: E402
from talaria_cli.cmds import forge as forge_cmd  # noqa: E402
from talaria_cli.cmds import forge_build as forge_build_cmd  # noqa: E402
from talaria_cli.cmds import import_chats as import_cmd  # noqa: E402
from talaria_cli.cmds import ingest as ingest_cmd  # noqa: E402
from talaria_cli.cmds import session as session_cmd  # noqa: E402
from talaria_cli.cmds import smoke as smoke_cmd  # noqa: E402
from talaria_cli.cmds import status as status_cmd  # noqa: E402
from talaria_cli.cmds import verify as verify_cmd  # noqa: E402
from talaria_cli.mode import mode_contract, resolve_mode  # noqa: E402
from talaria_cli.vault import find_vault  # noqa: E402


def _capture_json_cmd(fn, *args, **kwargs) -> dict[str, Any]:
    """Run a CLI cmd that emit()s JSON to stdout; return parsed dict + exit."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = fn(*args, **kwargs, as_json=True)
    raw = buf.getvalue().strip()
    data: dict[str, Any]
    try:
        data = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        data = {"raw": raw}
    if isinstance(data, dict):
        data.setdefault("ok", code == 0)
        data["exit"] = code
    return data if isinstance(data, dict) else {"ok": code == 0, "exit": code, "data": data}


TOOLS: list[dict[str, Any]] = [
    {
        "name": "talaria_describe",
        "description": "FIRST tool: Talaria connection contract (commands, MCP, organs, rules).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_connect",
        "description": "Emit MCP/CLI connection snippet for a client (cursor|hermes|claude|generic).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "client": {
                    "type": "string",
                    "enum": ["cursor", "hermes", "claude", "claude-code", "generic"],
                },
                "apply": {
                    "type": "boolean",
                    "description": "If true, merge into client config (requires confirm=true)",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Required safety latch for apply=true",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_doctor",
        "description": "Check tools + organism structure.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_boot",
        "description": "Install missing Talaria tools (markitdown, graphify, obsidian-mcp).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_status",
        "description": "Suit status: vault, Mark level, tools.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_vault_path",
        "description": "Absolute path to the Talaria vault.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_mode_get",
        "description": "Get SPINE mode (strict|draft) and contract.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_mode_set",
        "description": "Persist SPINE mode to .talaria.mode",
        "inputSchema": {
            "type": "object",
            "properties": {"mode": {"type": "string", "enum": ["strict", "draft"]}},
            "required": ["mode"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_session_start",
        "description": "Start SPINE session: create scorecard + .talaria.session.json",
        "inputSchema": {
            "type": "object",
            "properties": {
                "objective": {"type": "string"},
                "forge_profile": {"type": "string", "description": "Optional forge_id"},
            },
            "required": ["objective"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_session_status",
        "description": "Show active SPINE session marker.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_session_close",
        "description": "Close session via verify close on the session scorecard.",
        "inputSchema": {
            "type": "object",
            "properties": {"draft": {"type": "boolean"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_verify_boot",
        "description": "SPINE entry gate: organism + Mark (+ session hint).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_verify_close",
        "description": "SPINE exit gate: validate scorecard markdown.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scorecard": {"type": "string"},
                "draft": {"type": "boolean"},
            },
            "required": ["scorecard"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_smoke",
        "description": "Run organism smoke suite.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_forge_list",
        "description": "List FORGE profiles (optional ensembles).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ensembles": {"type": "boolean"},
                "graph": {"type": "boolean"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_show",
        "description": "Show FORGE profile: gates, DoD, activation, structure.",
        "inputSchema": {
            "type": "object",
            "properties": {"profile": {"type": "string"}},
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_check",
        "description": "Validate FORGE profile and optional deliverable gates (Gaxon with require_axon).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "deliverable": {"type": "string"},
                "declare": {"type": "string"},
                "require_axon": {
                    "type": "boolean",
                    "description": "Require axon_skills cites (Gaxon)",
                },
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_run",
        "description": (
            "Emit FORGE activation packet with AXON skill bodies + memory retrieve by default. "
            "Optional pack (software-delivery, youtube-channel)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "with_axon": {
                    "type": "boolean",
                    "description": "Default true — AXON retrieve/hydrate",
                },
                "hydrate": {
                    "type": "boolean",
                    "description": "Default true — embed skill bodies",
                },
                "with_memory": {
                    "type": "boolean",
                    "description": "Default true — memory/ retrieve",
                },
                "pack": {
                    "type": "string",
                    "description": "Skill pack id (e.g. software-delivery)",
                },
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_build",
        "description": (
            "Create a draft FORGE agent/profile from a natural-language brief "
            "(Builder 2.0 + optional user-owned delegation graph). "
            "Use when the user says: create an agent that… using Talaria. "
            "Talaria is the factory — the user owns the agent org chart."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "brief": {
                    "type": "string",
                    "description": 'e.g. "crea un agente que sepa responder correos"',
                },
                "id": {"type": "string", "description": "Optional forge_id kebab-case"},
                "specialty": {"type": "string"},
                "deliverable": {"type": "string"},
                "force": {"type": "boolean"},
                "kind": {
                    "type": "string",
                    "description": "orchestrator | specialist | both",
                },
                "invocable_by_mode": {
                    "type": "string",
                    "description": "open | allowlist | deny_direct (default open)",
                },
                "invocable_by": {
                    "type": "string",
                    "description": "Comma forge_ids that may invoke this agent",
                },
                "invokes": {
                    "type": "string",
                    "description": "Comma forge_ids this agent may delegate to",
                },
            },
            "required": ["brief"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_invoke",
        "description": (
            "Delegate from parent agent to child specialist (user-owned graph). "
            "Policy: open by default; allowlist/deny_direct optional."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent": {"type": "string"},
                "child": {"type": "string"},
                "brief": {"type": "string"},
                "strict": {"type": "boolean"},
                "with_axon": {
                    "type": "boolean",
                    "description": "Default true — hydrate AXON + optional pack",
                },
                "hydrate": {"type": "boolean"},
                "with_memory": {"type": "boolean"},
                "pack": {"type": "string"},
                "deliverable": {"type": "string"},
                "artifact_in": {"type": "string"},
                "require_deliverable": {"type": "boolean"},
            },
            "required": ["parent", "child"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_graph",
        "description": "Show user-owned FORGE delegation graph (nodes + edges).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_forge_instruct",
        "description": (
            "Auto-bootstrap doctrine/corpus for a profile. "
            "Also runs automatically inside talaria_forge_build."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "all_drafts": {"type": "boolean"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_search",
        "description": "Search AXON skills/ (records quality shown counts).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "domain": {"type": "string"},
                "tag": {"type": "string"},
                "limit": {"type": "integer"},
                "record": {"type": "boolean", "description": "Default true"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_for_profile",
        "description": "Run FORGE profile axon_queries (+ corpus enrichment).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "limit": {"type": "integer"},
                "record": {"type": "boolean"},
            },
            "required": ["profile"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_stats",
        "description": "AXON skill/domain counts + quality stats.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_axon_feedback",
        "description": "Quality loop: mark a skill useful|noise.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "skills/... path"},
                "signal": {"type": "string", "enum": ["useful", "noise"]},
            },
            "required": ["path", "signal"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_quality",
        "description": "AXON quality ranking from feedback.",
        "inputSchema": {
            "type": "object",
            "properties": {"limit": {"type": "integer"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_axon_pack_list",
        "description": "List curated AXON skill packs (mission sets; curate ≠ delete).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_axon_pack_show",
        "description": "Show one AXON skill pack (queries + pinned skills).",
        "inputSchema": {
            "type": "object",
            "properties": {"pack_id": {"type": "string"}},
            "required": ["pack_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_memory_retrieve",
        "description": "Search vault memory/ Markdown for Act context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "forge_id": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_eval_list",
        "description": "List Ley II gold evals.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "talaria_eval_show",
        "description": "Show one eval spec.",
        "inputSchema": {
            "type": "object",
            "properties": {"eval_id": {"type": "string"}},
            "required": ["eval_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_eval_run",
        "description": "Score deliverable against eval, or A/B fixtures if ab=true / no deliverable.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "eval_id": {"type": "string"},
                "deliverable": {"type": "string"},
                "ab": {"type": "boolean"},
            },
            "required": ["eval_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_ingest_doc",
        "description": "Convert document/URL to Markdown in memory/inbox/converted.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "output": {"type": "string"},
            },
            "required": ["source"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_ingest_project",
        "description": "Graphify a code project into memory/graphs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "name": {"type": "string"},
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "talaria_import_chats",
        "description": "Import Hermes/Claude/Cursor chats into memory/conversations.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


class TalariaMCP:
    """Dispatcher: MCP tool name → organ function (same semantics as CLI)."""

    def __init__(self, vault: Path):
        self.vault = vault

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        try:
            return self._call(name, arguments)
        except Exception as e:  # noqa: BLE001 — surface to MCP client
            return {"ok": False, "error": str(e), "tool": name}

    def _call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "talaria_describe":
            return agent_contract(self.vault)

        if name == "talaria_connect":
            client = arguments.get("client") or "generic"
            if arguments.get("apply"):
                return connect_apply_cmd.apply_connection(
                    self.vault, client, yes=bool(arguments.get("confirm"))
                )
            data = connection_snippet(self.vault, client)
            data["apply_hint"] = "talaria_connect with apply=true and confirm=true"
            data["ok"] = True
            return data

        if name == "talaria_doctor":
            return _capture_json_cmd(verify_cmd.run_doctor, self.vault)

        if name == "talaria_boot":
            return _capture_json_cmd(boot_cmd.run_boot, self.vault, check_only=False)

        if name == "talaria_status":
            return status_cmd.get_status(self.vault)

        if name == "talaria_vault_path":
            return {"ok": True, "vault": str(self.vault)}

        if name == "talaria_mode_get":
            m = resolve_mode(self.vault)
            return {"ok": True, "command": "mode get", "mode": m, **mode_contract(m)}

        if name == "talaria_mode_set":
            mode = str(arguments["mode"]).strip().lower()
            if mode not in {"strict", "draft"}:
                return {"ok": False, "error": "mode must be strict|draft"}
            (self.vault / ".talaria.mode").write_text(mode + "\n", encoding="utf-8")
            return {"ok": True, "command": "mode set", "mode": mode, **mode_contract(mode)}

        if name == "talaria_session_start":
            return session_cmd.start_session(
                self.vault,
                objective=str(arguments["objective"]),
                forge_profile=arguments.get("forge_profile"),
            )

        if name == "talaria_session_status":
            return session_cmd.status_session(self.vault)

        if name == "talaria_session_close":
            return _capture_json_cmd(
                session_cmd.close_session,
                self.vault,
                allow_draft=bool(arguments.get("draft")),
            )

        if name == "talaria_verify_boot":
            data = verify_cmd.evaluate_boot(self.vault)
            mode = resolve_mode(self.vault)
            data["mode"] = mode
            data["mode_contract"] = mode_contract(mode)
            sess = session_cmd.status_session(self.vault)
            data["session"] = {
                "active": sess.get("active"),
                "scorecard": (sess.get("session") or {}).get("scorecard"),
                "forge_profile": (sess.get("session") or {}).get("forge_profile"),
            }
            if mode == "draft":
                data["ok"] = True
            return data

        if name == "talaria_verify_close":
            return verify_cmd.evaluate_close(
                self.vault,
                arguments["scorecard"],
                allow_draft=bool(arguments.get("draft")),
            )

        if name == "talaria_smoke":
            return _capture_json_cmd(smoke_cmd.run_smoke, self.vault)

        if name == "talaria_forge_list":
            profiles = forge_cmd.list_profiles(self.vault)
            data: dict[str, Any] = {
                "ok": True,
                "command": "forge list",
                "count": len(profiles),
                "profiles": profiles,
            }
            if arguments.get("ensembles"):
                data["ensembles"] = forge_cmd.list_ensembles(self.vault)
            if arguments.get("graph"):
                from talaria_cli.cmds import forge_delegation as dele

                data["graph"] = dele.build_delegation_graph(self.vault)
            return data

        if name == "talaria_forge_show":
            return _capture_json_cmd(forge_cmd.run_show, self.vault, arguments["profile"])

        if name == "talaria_forge_check":
            return _capture_json_cmd(
                forge_cmd.run_check,
                self.vault,
                arguments["profile"],
                deliverable=arguments.get("deliverable"),
                declare=arguments.get("declare"),
                require_axon=bool(arguments.get("require_axon")),
            )

        if name == "talaria_forge_run":
            with_axon = (
                True
                if "with_axon" not in arguments
                else bool(arguments.get("with_axon"))
            )
            hydrate = (
                True if "hydrate" not in arguments else bool(arguments.get("hydrate"))
            )
            with_memory = (
                True
                if "with_memory" not in arguments
                else bool(arguments.get("with_memory"))
            )
            return _capture_json_cmd(
                forge_cmd.run_run,
                self.vault,
                arguments["profile"],
                with_axon=with_axon,
                hydrate=hydrate and with_axon,
                with_memory=with_memory,
                pack=arguments.get("pack"),
            )

        if name == "talaria_forge_build":
            return forge_build_cmd.build_profile_from_brief(
                self.vault,
                arguments["brief"],
                forge_id=arguments.get("id"),
                specialty=arguments.get("specialty"),
                deliverable=arguments.get("deliverable"),
                force=bool(arguments.get("force")),
                role_kind=arguments.get("kind") or "both",
                invocable_by_mode=arguments.get("invocable_by_mode") or "open",
                invocable_by=arguments.get("invocable_by"),
                invokes=arguments.get("invokes"),
            )

        if name == "talaria_forge_invoke":
            with_axon = (
                True
                if "with_axon" not in arguments
                else bool(arguments.get("with_axon"))
            )
            hydrate = (
                True if "hydrate" not in arguments else bool(arguments.get("hydrate"))
            )
            with_memory = (
                True
                if "with_memory" not in arguments
                else bool(arguments.get("with_memory"))
            )
            return _capture_json_cmd(
                forge_cmd.run_invoke,
                self.vault,
                arguments["parent"],
                arguments["child"],
                brief=arguments.get("brief"),
                strict=bool(arguments.get("strict")),
                with_axon=with_axon,
                hydrate=hydrate and with_axon,
                with_memory=with_memory,
                pack=arguments.get("pack"),
                deliverable=arguments.get("deliverable"),
                artifact_in=arguments.get("artifact_in"),
                require_deliverable=bool(arguments.get("require_deliverable")),
            )

        if name == "talaria_forge_graph":
            from talaria_cli.cmds import forge_delegation as dele

            return dele.build_delegation_graph(self.vault)

        if name == "talaria_forge_instruct":
            from talaria_cli.cmds import forge_instruct as instruct_cmd

            if arguments.get("all_drafts"):
                return _capture_json_cmd(
                    instruct_cmd.run_instruct,
                    self.vault,
                    None,
                    all_drafts=True,
                )
            if not arguments.get("profile"):
                return {"ok": False, "error": "profile or all_drafts required"}
            return instruct_cmd.auto_instruct(self.vault, arguments["profile"])

        if name == "talaria_axon_search":
            record = arguments.get("record")
            return axon_cmd.search_skills(
                self.vault,
                arguments["query"],
                domain=arguments.get("domain"),
                tag=arguments.get("tag"),
                limit=int(arguments.get("limit") or 15),
                record=True if record is None else bool(record),
            )

        if name == "talaria_axon_for_profile":
            return _capture_json_cmd(
                axon_cmd.run_for_profile,
                self.vault,
                arguments["profile"],
                limit=int(arguments.get("limit") or 10),
                record=True if arguments.get("record") is None else bool(arguments.get("record")),
            )

        if name == "talaria_axon_stats":
            data = axon_cmd.axon_stats(self.vault)
            data["command"] = "axon stats"
            return data

        if name == "talaria_axon_feedback":
            data = axon_cmd.record_feedback(
                self.vault, arguments["path"], arguments["signal"]
            )
            data["command"] = "axon feedback"
            return data

        if name == "talaria_axon_quality":
            data = axon_cmd.quality_report(
                self.vault, limit=int(arguments.get("limit") or 20)
            )
            data["command"] = "axon quality"
            return data

        if name == "talaria_axon_pack_list":
            from talaria_cli.cmds.context_hydrate import list_packs

            packs = list_packs(self.vault)
            return {"ok": True, "command": "axon pack list", "packs": packs}

        if name == "talaria_axon_pack_show":
            from talaria_cli.cmds.context_hydrate import load_pack

            pack = load_pack(self.vault, arguments["pack_id"])
            if not pack:
                return {"ok": False, "error": f"pack not found: {arguments['pack_id']}"}
            return {"ok": True, "command": "axon pack show", "pack": pack}

        if name == "talaria_memory_retrieve":
            from talaria_cli.cmds.context_hydrate import memory_retrieve

            return memory_retrieve(
                self.vault,
                arguments["query"],
                forge_id=arguments.get("forge_id"),
                limit=int(arguments.get("limit") or 8),
            )

        if name == "talaria_eval_list":
            items = eval_cmd.list_evals(self.vault)
            return {"ok": True, "command": "eval list", "count": len(items), "evals": items}

        if name == "talaria_eval_show":
            spec = eval_cmd.load_eval(self.vault, arguments["eval_id"])
            if not spec:
                return {"ok": False, "error": f"eval not found: {arguments['eval_id']}"}
            return {"ok": True, "command": "eval show", "eval": spec}

        if name == "talaria_eval_run":
            return _capture_json_cmd(
                eval_cmd.run_run,
                self.vault,
                arguments["eval_id"],
                deliverable=arguments.get("deliverable"),
                compare_fixtures=bool(arguments.get("ab")),
            )

        if name == "talaria_ingest_doc":
            return _capture_json_cmd(
                ingest_cmd.run_ingest_doc,
                self.vault,
                arguments["source"],
                arguments.get("output"),
            )

        if name == "talaria_ingest_project":
            return _capture_json_cmd(
                ingest_cmd.run_ingest_project,
                self.vault,
                arguments["path"],
                arguments.get("name"),
            )

        if name == "talaria_import_chats":
            return _capture_json_cmd(import_cmd.run_import_chats, self.vault)

        return {"ok": False, "error": f"unknown tool: {name}"}


def _read_message() -> dict[str, Any] | None:
    """Read one JSON-RPC message from stdin (Content-Length or newline JSON)."""
    header = b""
    while True:
        ch = sys.stdin.buffer.read(1)
        if not ch:
            return None
        header += ch
        if header.endswith(b"\r\n\r\n"):
            break
        if len(header) > 65536:
            # fallback: treat as raw JSON line protocol
            line = header.decode("utf-8", errors="replace")
            if "\n" in line:
                return json.loads(line.strip())
            return None
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
    body = json.dumps(msg, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    sys.stdout.buffer.flush()


def _result(req_id: Any, result: Any) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _error(req_id: Any, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def serve(vault: Path) -> int:
    server = TalariaMCP(vault)
    # initialize handshake loop
    while True:
        msg = _read_message()
        if msg is None:
            return 0
        method = msg.get("method")
        req_id = msg.get("id")
        params = msg.get("params") or {}

        if method == "initialize":
            _result(
                req_id,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "talaria", "version": "1.1.0"},
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
            if not name:
                _error(req_id, -32602, "missing tool name")
                continue
            out = server.call(name, arguments)
            # MCP content: JSON text
            _result(
                req_id,
                {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(out, ensure_ascii=False, indent=2),
                        }
                    ],
                    "isError": bool(isinstance(out, dict) and out.get("ok") is False),
                },
            )
            continue
        if method == "ping":
            _result(req_id, {})
            continue
        if req_id is not None:
            _error(req_id, -32601, f"method not found: {method}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Talaria MCP stdio server")
    ap.add_argument("--vault", help="Vault path")
    args = ap.parse_args(argv)
    vault = find_vault(args.vault)
    return serve(vault)


if __name__ == "__main__":
    raise SystemExit(main())
