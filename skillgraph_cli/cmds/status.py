from __future__ import annotations

from pathlib import Path

from skillgraph_cli.util import EXIT_ERROR, EXIT_OK, emit, tool_present


def get_status(vault: Path) -> dict:
    tools = {
        "markitdown": _module_ok("markitdown"),
        "graphify": tool_present("graphify") or _module_ok("graphify"),
        "obsidian_mcp": _obsidian_mcp_ok(),
    }
    mark = _infer_mark(tools)
    status_note = vault / "SPINE-STATUS-CURSOR.md"
    legacy_note = vault / "IRONMAN-STATUS-CURSOR.md"
    note_present = status_note.is_file() or legacy_note.is_file()
    return {
        "vault": str(vault),
        "mark": mark,
        "tools": tools,
        "spine_status_note": note_present,
        "ironman_status_note": note_present,  # legacy key
        "pipeline": "spine",
        "framework": "SPINE",
        "cli": "skillgraph",
        "ok": bool(tools["markitdown"] and tools["graphify"] and tools["obsidian_mcp"]),
    }


def run_status(vault: Path, *, as_json: bool = False) -> int:
    data = get_status(vault)
    if as_json:
        emit(data, True)
    else:
        print(f"Vault:  {vault}")
        print(f"Mark:   {data['mark']}")
        t = data["tools"]
        print(
            f"Tools:  markitdown={t['markitdown']}  graphify={t['graphify']}  obsidian-mcp={t['obsidian_mcp']}"
        )
        print(f"Status: {'ONLINE note present' if data['spine_status_note'] else 'no status note'}")
        print("Framework: SPINE (Ingest->Normalize->Orient->Retrieve->Memorize->Act->Notify)")
    return EXIT_OK if data["ok"] else EXIT_ERROR


def _module_ok(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def _obsidian_mcp_ok() -> bool:
    home = Path.home()
    candidates = [
        home / "AppData/Roaming/npm/node_modules/obsidian-mcp/build/main.js",
        Path("/usr/local/lib/node_modules/obsidian-mcp/build/main.js"),
        home / ".npm-global/lib/node_modules/obsidian-mcp/build/main.js",
    ]
    return any(c.is_file() for c in candidates)


def _infer_mark(tools: dict) -> str:
    if tools["markitdown"] and tools["graphify"] and tools["obsidian_mcp"]:
        return "Mk.2"
    if tools["obsidian_mcp"]:
        return "Mk.1"
    return "Mk.0"
