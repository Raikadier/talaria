"""Apply talaria connect snippets to client MCP config files."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from talaria_cli.agent_contract import connection_snippet
from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit


def _backup(path: Path) -> Path | None:
    if not path.is_file():
        return None
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    return bak


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def apply_cursor(vault: Path, snippet: dict[str, Any]) -> dict[str, Any]:
    cfg_path = Path.home() / ".cursor" / "mcp.json"
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    bak = _backup(cfg_path)
    cfg = _load_json(cfg_path)
    servers = cfg.get("mcpServers")
    if not isinstance(servers, dict):
        servers = {}
    fragment = snippet.get("mcpServers_fragment") or {}
    servers.update(fragment)
    cfg["mcpServers"] = servers
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "applied": True,
        "config_file": str(cfg_path),
        "backup": str(bak) if bak else None,
        "merged_keys": list(fragment.keys()),
    }


def apply_claude(vault: Path, snippet: dict[str, Any]) -> dict[str, Any]:
    # Project-local .mcp.json preferred; also try ~/.claude/settings.json mcpServers
    project = vault / ".mcp.json"
    bak = _backup(project) if project.is_file() else None
    cfg = _load_json(project)
    servers = cfg.get("mcpServers")
    if not isinstance(servers, dict):
        servers = {}
    fragment = snippet.get("mcpServers_fragment") or {}
    servers.update(fragment)
    cfg["mcpServers"] = servers
    project.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "applied": True,
        "config_file": str(project),
        "backup": str(bak) if bak else None,
        "merged_keys": list(fragment.keys()),
        "note": "Also merge into ~/.claude/settings.json if you use global MCP",
    }


def apply_connection(
    vault: Path,
    client: str,
    *,
    yes: bool = False,
) -> dict[str, Any]:
    client = (client or "generic").lower().strip()
    snippet = connection_snippet(vault, client)
    if not yes:
        return {
            "ok": False,
            "error": "refusing to write client config without --yes",
            "would_apply_to": snippet.get("config_file"),
            "fragment": snippet.get("mcpServers_fragment") or snippet.get("mcp_servers_yaml"),
            "hint": "talaria connect --client cursor --apply --yes",
        }
    if client == "cursor":
        result = apply_cursor(vault, snippet)
    elif client in {"claude", "claude-code"}:
        result = apply_claude(vault, snippet)
    elif client == "hermes":
        return {
            "ok": False,
            "error": "hermes apply writes YAML; merge manually for now",
            "config_file": snippet.get("config_file"),
            "mcp_servers_yaml": snippet.get("mcp_servers_yaml"),
            "hint": "Paste mcp_servers_yaml into Hermes config.yaml",
        }
    else:
        return {
            "ok": False,
            "error": f"apply not supported for client={client}",
            "hint": "Use --client cursor|claude",
        }
    return {
        "ok": True,
        "client": client,
        "vault": str(vault),
        **result,
        "instructions": snippet.get("instructions"),
        "next": ["Reload MCP in the client", "talaria_describe / talaria status"],
    }


def run_apply(vault: Path, client: str, *, yes: bool = False, as_json: bool = False) -> int:
    data = apply_connection(vault, client, yes=yes)
    data["command"] = "connect apply"
    emit(data, as_json or True)
    if not data.get("ok"):
        return EXIT_USAGE if "without --yes" in str(data.get("error", "")) else EXIT_ERROR
    return EXIT_OK
