from __future__ import annotations

import os
from pathlib import Path


MARKERS = ("Home.md", "AGENTS.md", "bootstrap.py")


def looks_like_vault(path: Path) -> bool:
    return all((path / m).is_file() for m in MARKERS)


def find_vault(explicit: str | None = None) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not looks_like_vault(p):
            raise FileNotFoundError(
                f"Path is not a SkillGraph vault (missing Home.md/AGENTS.md/bootstrap.py): {p}"
            )
        return p

    env = os.environ.get("SKILLGRAPH_VAULT")
    if env:
        p = Path(env).expanduser().resolve()
        if looks_like_vault(p):
            return p
        raise FileNotFoundError(f"SKILLGRAPH_VAULT is set but invalid: {p}")

    cur = Path.cwd().resolve()
    for candidate in [cur, *cur.parents]:
        if looks_like_vault(candidate):
            return candidate

    # Package lives inside the vault: SkillGraph/skillgraph_cli/
    pkg_root = Path(__file__).resolve().parent.parent
    if looks_like_vault(pkg_root):
        return pkg_root

    raise FileNotFoundError(
        "SkillGraph vault not found. Use --vault PATH, set SKILLGRAPH_VAULT, "
        "or run from inside the vault."
    )
