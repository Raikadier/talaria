from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2


def run_python_script(script: Path, args: list[str] | None = None) -> int:
    cmd = [sys.executable, str(script), *(args or [])]
    print(">", " ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode


def emit(data: Any, as_json: bool) -> None:
    if as_json:
        text = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        try:
            print(text)
        except UnicodeEncodeError:
            # Windows consoles (cp1252) — fall back to ASCII-escaped JSON
            print(json.dumps(data, indent=2, ensure_ascii=True, default=str))
    elif isinstance(data, dict):
        for k, v in data.items():
            line = f"{k}: {v}"
            try:
                print(line)
            except UnicodeEncodeError:
                print(line.encode("ascii", errors="replace").decode("ascii"))
    else:
        try:
            print(data)
        except UnicodeEncodeError:
            print(str(data).encode("ascii", errors="replace").decode("ascii"))


def tool_present(name: str) -> bool:
    import shutil

    return shutil.which(name) is not None
