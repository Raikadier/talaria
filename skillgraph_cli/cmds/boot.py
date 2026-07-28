from __future__ import annotations

from pathlib import Path

from skillgraph_cli.util import EXIT_ERROR, EXIT_OK, emit, run_python_script


def run_boot(vault: Path, *, check_only: bool = False, as_json: bool = False) -> int:
    script = vault / "bootstrap.py"
    if not script.is_file():
        emit({"error": f"bootstrap.py missing in {vault}"}, as_json)
        return EXIT_ERROR
    args = ["--check-only"] if check_only else []
    code = run_python_script(script, args)
    if as_json:
        emit({"command": "doctor" if check_only else "boot", "exit": code, "vault": str(vault)}, True)
    return EXIT_OK if code == 0 else EXIT_ERROR
