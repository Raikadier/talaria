"""Memory organ — retrieve vault Markdown for Act context."""
from __future__ import annotations

from pathlib import Path

from talaria_cli.cmds.context_hydrate import memory_retrieve
from talaria_cli.util import EXIT_ERROR, EXIT_OK, emit


def run_retrieve(
    vault: Path,
    query: str,
    *,
    forge_id: str | None = None,
    limit: int = 8,
    as_json: bool = False,
) -> int:
    data = memory_retrieve(vault, query, forge_id=forge_id, limit=limit)
    data["command"] = "memory retrieve"
    if as_json:
        emit(data, True)
    else:
        print(f"memory retrieve: {data['hit_count']} hits for {query!r}")
        for h in data.get("hits") or []:
            print(f"  [{h['score']}] {h['path']}")
    return EXIT_OK if data.get("ok") else EXIT_ERROR
