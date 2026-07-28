from __future__ import annotations

from pathlib import Path

from skillgraph_cli.util import EXIT_ERROR, EXIT_OK, emit, run_python_script


def run_import_chats(vault: Path, *, as_json: bool = False) -> int:
    script = vault / "_tools" / "import_agent_chats.py"
    if not script.is_file():
        emit({"error": "import_agent_chats.py missing"}, as_json)
        return EXIT_ERROR
    code = run_python_script(script)
    if as_json:
        emit({"command": "import.chats", "exit": code}, True)
    return EXIT_OK if code == 0 else EXIT_ERROR
