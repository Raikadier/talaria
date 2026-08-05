from __future__ import annotations

from pathlib import Path

from talaria_cli.vault import find_vault, looks_like_vault


def test_looks_like_vault_on_repo_root():
    root = Path(__file__).resolve().parents[1]
    assert looks_like_vault(root)


def test_find_vault_from_src_package():
    root = Path(__file__).resolve().parents[1]
    found = find_vault(str(root))
    assert found == root.absolute()
    assert (found / "AGENTS.md").is_file()
