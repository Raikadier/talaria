from __future__ import annotations

from pathlib import Path
from typing import Any

from talaria_cli import __version__
from talaria_cli.mode import mode_contract, resolve_mode


def agent_contract(vault: Path) -> dict[str, Any]:
    """Machine-readable contract so any agent can connect without tribal knowledge."""
    py = _python()
    vault_s = str(vault)
    module = "talaria_cli"
    return {
        "name": "talaria",
        "version": __version__,
        "role": "SPINE orchestration CLI + MCP for Talaria organism",
        "vault": vault_s,
        "canonical_memory": vault_s,
        "brand": {
            "commercial": "Talaria",
            "technical": "Talaria Cognitive Operating System",
            "acronym": "TCOS",
            "mythology": "Talaria — winged sandals of Hermes; the suit that lets the messenger cross worlds",
        },
        "mode": mode_contract(resolve_mode(vault)),
        "pipeline": "ingest->normalize->orient->retrieve->memorize->act->notify",
        "framework": "SPINE",
        "organs": [
            "memory",
            "axon",
            "forge",
            "spine",
            "api",
            "tools",
            "adapters",
        ],
        "guarantees": {
            "verify_boot": "talaria verify boot --json",
            "verify_close": "talaria verify close --scorecard <path> --json",
            "scorecard_template": "_templates/scorecard.md",
            "smoke": "talaria smoke --json",
            "modes": ["strict", "draft"],
        },
        "how_agents_connect": {
            "preferred": "mcp",
            "fallback": "cli_json",
            "discovery": "talaria describe --json",
            "session_start": "talaria verify boot --json",
            "session_end": "talaria verify close --scorecard <path> --json",
        },
        "cli": {
            "invoke": ["talaria"],
            "invoke_module": [py, "-m", module],
            "commands": [
                {
                    "name": "doctor",
                    "argv": ["doctor", "--json"],
                    "layer": "boot",
                    "description": "Check tools + organism structure",
                },
                {
                    "name": "boot",
                    "argv": ["boot"],
                    "layer": "boot",
                    "description": "Install missing tools (markitdown, graphify, obsidian-mcp)",
                },
                {
                    "name": "verify_boot",
                    "argv": ["verify", "boot", "--json"],
                    "layer": "boot",
                    "description": "Entry gate: organism files/dirs + Mark >= Mk.1",
                },
                {
                    "name": "verify_close",
                    "argv": ["verify", "close", "--scorecard", "<path>", "--json"],
                    "layer": "notify",
                    "description": "Exit gate: validate session scorecard (use --draft for draft mode)",
                },
                {
                    "name": "smoke",
                    "argv": ["smoke", "--json"],
                    "layer": "boot",
                    "description": "Phase B smoke suite (describe/organism/verify/AXON/FORGE)",
                },
                {
                    "name": "forge_list",
                    "argv": ["forge", "list", "--ensembles", "--json"],
                    "layer": "orient",
                    "description": "List FORGE profiles and ensembles",
                },
                {
                    "name": "forge_show",
                    "argv": ["forge", "show", "<id>", "--json"],
                    "layer": "orient",
                    "description": "Show FORGE profile gates/DoD/activation",
                },
                {
                    "name": "forge_check",
                    "argv": ["forge", "check", "--profile", "<id>", "--deliverable", "<path>", "--json"],
                    "layer": "notify",
                    "description": "Validate profile structure and deliverable gates (Ley I)",
                },
                {
                    "name": "forge_run",
                    "argv": ["forge", "run", "<id>", "--with-axon", "--json"],
                    "layer": "act",
                    "description": "Emit FORGE activation packet (optional AXON hits)",
                },
                {
                    "name": "axon_search",
                    "argv": ["axon", "search", "<query>", "--json"],
                    "layer": "retrieve",
                    "description": "Search AXON skills/ by query (optional --domain/--tag)",
                },
                {
                    "name": "axon_for_profile",
                    "argv": ["axon", "for-profile", "<forge_id>", "--json"],
                    "layer": "retrieve",
                    "description": "Run default axon_queries from a FORGE profile",
                },
                {
                    "name": "axon_stats",
                    "argv": ["axon", "stats", "--json"],
                    "layer": "retrieve",
                    "description": "AXON skill/domain counts",
                },
                {
                    "name": "eval_list",
                    "argv": ["eval", "list", "--json"],
                    "layer": "notify",
                    "description": "List Ley II gold evals",
                },
                {
                    "name": "eval_run",
                    "argv": ["eval", "run", "<id>", "--deliverable", "<path>", "--json"],
                    "layer": "notify",
                    "description": "Score a deliverable against gold rubric",
                },
                {
                    "name": "mode_get",
                    "argv": ["mode", "get", "--json"],
                    "layer": "meta",
                    "description": "Current SPINE mode (strict|draft)",
                },
                {
                    "name": "status",
                    "argv": ["status", "--json"],
                    "layer": "notify",
                    "description": "Suit status: mark level + tool presence",
                },
                {
                    "name": "vault",
                    "argv": ["vault", "--json"],
                    "layer": "meta",
                    "description": "Absolute vault path",
                },
                {
                    "name": "ingest_doc",
                    "argv": ["ingest", "doc", "<source>", "--json"],
                    "layer": "ingest+normalize",
                    "description": "Convert document/URL to Markdown in memory/inbox/converted",
                },
                {
                    "name": "ingest_project",
                    "argv": ["ingest", "project", "<path>", "--json"],
                    "layer": "ingest+normalize",
                    "description": "Graphify a code project into memory/graphs",
                },
                {
                    "name": "import_chats",
                    "argv": ["import", "chats", "--json"],
                    "layer": "ingest+memorize",
                    "description": "Import Hermes/Claude/Cursor chat history",
                },
                {
                    "name": "describe",
                    "argv": ["describe", "--json"],
                    "layer": "meta",
                    "description": "This contract (self-description for agents)",
                },
                {
                    "name": "connect",
                    "argv": ["connect", "--client", "<cursor|hermes|claude|generic>", "--json"],
                    "layer": "meta",
                    "description": "Emit MCP/CLI connection snippets for a client",
                },
            ],
        },
        "mcp": {
            "server_name": "talaria",
            "transport": "stdio",
            "command": py,
            "args": ["-m", "talaria_cli.mcp_server", "--vault", vault_s],
            "tools": [
                "talaria_doctor",
                "talaria_boot",
                "talaria_status",
                "talaria_vault_path",
                "talaria_verify_boot",
                "talaria_verify_close",
                "talaria_smoke",
                "talaria_forge_list",
                "talaria_forge_show",
                "talaria_forge_check",
                "talaria_forge_run",
                "talaria_axon_search",
                "talaria_axon_for_profile",
                "talaria_axon_stats",
                "talaria_ingest_doc",
                "talaria_ingest_project",
                "talaria_import_chats",
                "talaria_describe",
            ],
            "env": {
                "TALARIA_VAULT": vault_s,
                "PYTHONPATH": str(Path(vault_s) / "src"),
            },
        },
        "companion_mcp": {
            "name": "obsidian",
            "purpose": "Read/write vault notes (Retrieve/Memorize)",
            "vault_mcp_name": "talaria",
        },
        "constitution": [
            "AGENTS.md",
            "_META/organism.md",
            "_META/architecture.md",
            "_META/spine-framework.md",
            "_META/axon.md",
            "_META/adapters/pilots.md",
            "CLAUDE.md",
        ],
        "rules_for_agents": [
            "Canonical memory is the Talaria vault Markdown — not chat history",
            "Session start: talaria verify boot --json",
            "Specialized work: talaria forge run <id> --with-axon then forge check --deliverable",
            "Retrieve skills via talaria axon search / axon for-profile",
            "After useful work: fill scorecard + talaria verify close --scorecard <path>",
            "Use talaria_* / CLI for Ingest+Boot; use obsidian MCP for note CRUD",
            "Retrieve before re-ingesting the same source",
            "Never store secrets in the vault",
        ],
    }


def connection_snippet(vault: Path, client: str) -> dict[str, Any]:
    contract = agent_contract(vault)
    mcp = contract["mcp"]
    client = (client or "generic").lower().strip()
    base = {
        "client": client,
        "vault": str(vault),
        "describe_cmd": "talaria describe --json",
    }

    cursor_block = {
        "talaria": {
            "command": mcp["command"],
            "args": mcp["args"],
            "env": mcp["env"],
        }
    }
    claude_block = dict(cursor_block)
    hermes_block = {
        "talaria": {
            "command": mcp["command"],
            "args": mcp["args"],
            "env": {"TALARIA_VAULT": str(vault)},
            "connect_timeout": 60,
        }
    }

    if client == "cursor":
        base["config_file"] = str(Path.home() / ".cursor" / "mcp.json")
        base["mcpServers_fragment"] = cursor_block
        base["instructions"] = [
            "Merge mcpServers_fragment into ~/.cursor/mcp.json",
            "Reload Cursor MCP settings",
            "Call talaria_describe then talaria_status",
        ]
    elif client in {"claude", "claude-code"}:
        base["config_file"] = str(Path.home() / ".claude" / "settings.json")
        base["mcpServers_fragment"] = claude_block
        base["instructions"] = [
            "Merge into settings.json mcpServers (or project .mcp.json)",
            "Restart Claude Code",
            "Open Talaria folder so CLAUDE.md loads",
        ]
    elif client == "hermes":
        base["config_file"] = str(Path.home() / "AppData/Local/hermes/config.yaml")
        base["mcp_servers_yaml"] = hermes_block
        base["instructions"] = [
            "Add mcp_servers.talaria entry to Hermes config.yaml",
            "Restart Hermes gateway",
            "Follow memories/TALARIA_SPINE.md (legacy: TALARIA_SPINE.md)",
        ]
    else:
        base["mcpServers_fragment"] = cursor_block
        base["cli_fallback"] = contract["cli"]["invoke"] + ["describe", "--json"]
        base["instructions"] = [
            "Prefer MCP stdio using mcp.command/args/env",
            "Or shell out to CLI with --json on every command",
            "Always start with: talaria describe --json",
        ]
    return base


def _python() -> str:
    import sys

    return sys.executable
