from __future__ import annotations

import os
from pathlib import Path


MARKERS = ("Home.md", "AGENTS.md", "bootstrap.py")


def looks_like_vault(path: Path) -> bool:
    return all((path / m).is_file() for m in MARKERS)


def _walk_up(start: Path) -> list[Path]:
    cur = start.absolute()
    return [cur, *cur.parents]


def find_vault(explicit: str | None = None) -> Path:
    """Locate the Talaria vault root (Markdown organism).

    Prefer absolute() over resolve() so Windows junctions keep the branded path
    when TALARIA_VAULT / --vault say so.
    """
    if explicit:
        p = Path(explicit).expanduser().absolute()
        if not looks_like_vault(p):
            raise FileNotFoundError(
                f"Path is not a Talaria vault (missing Home.md/AGENTS.md/bootstrap.py): {p}"
            )
        return p

    env = os.environ.get("TALARIA_VAULT")
    if env:
        p = Path(env).expanduser().absolute()
        if looks_like_vault(p):
            return p
        raise FileNotFoundError(f"TALARIA_VAULT is set but invalid: {p}")

    cwd = Path.cwd().absolute()
    for candidate in _walk_up(cwd):
        if looks_like_vault(candidate):
            return candidate

    # Package layouts:
    #   <vault>/src/talaria_cli/vault.py  (editable / monorepo)
    #   <vault>/talaria_cli/vault.py      (legacy flat)
    #   site-packages/talaria_cli/…       (installed; vault via env/cwd only)
    pkg_dir = Path(__file__).resolve().parent
    for candidate in _walk_up(pkg_dir):
        if looks_like_vault(candidate):
            sibling = candidate.parent / "Talaria"
            if sibling.exists() and looks_like_vault(sibling):
                return sibling.absolute()
            return candidate

    raise FileNotFoundError(
        "Talaria vault not found. Use --vault PATH, set TALARIA_VAULT, "
        "or run from inside the vault after: pip install -e ."
    )
