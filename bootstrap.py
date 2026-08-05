#!/usr/bin/env python3
"""Bootstrap Talaria tools for any agent/machine.

- Resolves vault root relative to this file (portable)
- Ensures `pip install -e .` so `talaria` is on PATH
- Checks markitdown / graphify / obsidian-mcp
- Installs missing deps via pip/npm
- Creates ingest folders

Usage:
  python bootstrap.py
  python bootstrap.py --check-only
  python bootstrap.py --skip-npm
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent
TOOLS = VAULT / "tools"
MANIFEST = TOOLS / "manifest.json"
REQ = TOOLS / "requirements.txt"
LOCAL_CFG = VAULT / ".talaria.local.json"
LEGACY_LOCAL = VAULT / ".skillgraph.local.json"


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    print(">", " ".join(cmd))
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def ensure_dirs(manifest: dict) -> None:
    for key, rel in manifest.get("ingest_dirs", {}).items():
        p = VAULT / rel
        p.mkdir(parents=True, exist_ok=True)
        keep = p / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
        print(f"[dir] {p.relative_to(VAULT)}")


def ensure_editable_install() -> None:
    """Install this repo editable so `talaria` entry point works anywhere."""
    pyproject = VAULT / "pyproject.toml"
    if not pyproject.is_file():
        print("[warn] pyproject.toml missing; skip editable install")
        return
    print("[install] pip install -e .")
    r = run([sys.executable, "-m", "pip", "install", "-e", str(VAULT)])
    if r.returncode != 0:
        print(r.stderr[-2000:] if r.stderr else r.stdout[-2000:])
        raise SystemExit(f"editable install failed ({r.returncode})")
    print("[ok] talaria package (editable)")


def check_markitdown() -> bool:
    if which("markitdown"):
        r = run(["markitdown", "--version"])
        print("[ok] markitdown", (r.stdout or r.stderr or "").strip()[:80])
        return r.returncode == 0 or bool(r.stdout or r.stderr)
    r = run([sys.executable, "-c", "import markitdown; print(getattr(markitdown,'__version__','ok'))"])
    if r.returncode == 0:
        print("[ok] markitdown module", r.stdout.strip())
        return True
    print("[missing] markitdown")
    return False


def check_graphify() -> bool:
    if which("graphify"):
        r = run(["graphify", "--help"])
        print("[ok] graphify CLI")
        return r.returncode == 0
    r = run([sys.executable, "-c", "import graphify; print('ok')"])
    if r.returncode == 0:
        print("[ok] graphify module")
        return True
    print("[missing] graphify (pip package: graphifyy)")
    return False


def _obsidian_mcp_candidates() -> list[Path]:
    home = Path.home()
    return [
        home / "AppData/Roaming/npm/node_modules/obsidian-mcp/build/main.js",  # Windows
        home / ".npm-global/lib/node_modules/obsidian-mcp/build/main.js",
        Path("/usr/local/lib/node_modules/obsidian-mcp/build/main.js"),
        Path("/opt/homebrew/lib/node_modules/obsidian-mcp/build/main.js"),  # macOS Apple Silicon
        home / ".local/lib/node_modules/obsidian-mcp/build/main.js",
    ]


def check_obsidian_mcp() -> bool:
    for c in _obsidian_mcp_candidates():
        if c.exists():
            print(f"[ok] obsidian-mcp {c}")
            return True
    if which("npm"):
        r = run(["npm", "ls", "-g", "obsidian-mcp"])
        if r.returncode == 0 and "obsidian-mcp" in (r.stdout + r.stderr):
            print("[ok] obsidian-mcp via npm ls -g")
            return True
    print("[missing] obsidian-mcp (optional but recommended)")
    return False


def install_pip_requirements() -> None:
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(REQ)]
    print("[install] pip requirements")
    r = run(cmd)
    print(r.stdout[-2000:] if r.stdout else "")
    if r.returncode != 0:
        print(r.stderr[-2000:] if r.stderr else "")
        raise SystemExit(f"pip install failed ({r.returncode})")


def install_obsidian_mcp() -> None:
    if not which("npm"):
        print("[warn] npm not found; skip obsidian-mcp")
        return
    print("[install] npm -g obsidian-mcp")
    r = run(["npm", "install", "-g", "obsidian-mcp"])
    if r.returncode != 0:
        print(r.stderr[-1500:] if r.stderr else r.stdout[-1500:])
        print("[warn] obsidian-mcp install failed (vault still usable as folder)")
    else:
        print("[ok] obsidian-mcp installed")


def write_local_config() -> None:
    """Machine-local paths — NOT committed (see .gitignore)."""
    cfg = {
        "vault_root": str(VAULT),
        "python": sys.executable,
        "generated_by": "bootstrap.py",
        "platform": sys.platform,
    }
    LOCAL_CFG.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print(f"[local] wrote {LOCAL_CFG.name} (gitignored)")
    if LEGACY_LOCAL.exists():
        try:
            LEGACY_LOCAL.unlink()
            print(f"[local] removed legacy {LEGACY_LOCAL.name}")
        except OSError:
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Bootstrap Talaria tooling")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--skip-npm", action="store_true")
    ap.add_argument("--skip-editable", action="store_true", help="Do not pip install -e .")
    args = ap.parse_args()

    print(f"Vault: {VAULT}")
    if sys.version_info < (3, 10):
        raise SystemExit("Python >= 3.10 required")

    # Make package importable before other checks when developing from clone
    src = VAULT / "src"
    if src.is_dir():
        sp = str(src)
        if sp not in sys.path:
            sys.path.insert(0, sp)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ensure_dirs(manifest)

    if not args.check_only and not args.skip_editable:
        ensure_editable_install()

    md_ok = check_markitdown()
    gy_ok = check_graphify()
    om_ok = check_obsidian_mcp()

    if args.check_only:
        status = {"markitdown": md_ok, "graphify": gy_ok, "obsidian-mcp": om_ok, "vault": str(VAULT)}
        print(json.dumps(status, indent=2))
        raise SystemExit(0 if (md_ok and gy_ok) else 1)

    if not (md_ok and gy_ok):
        install_pip_requirements()
        md_ok = check_markitdown()
        gy_ok = check_graphify()

    if not om_ok and not args.skip_npm:
        install_obsidian_mcp()
        om_ok = check_obsidian_mcp()

    write_local_config()
    os.environ.setdefault("TALARIA_VAULT", str(VAULT))

    summary = {
        "vault": str(VAULT),
        "markitdown": md_ok,
        "graphify": gy_ok,
        "obsidian-mcp": om_ok,
        "next": [
            "talaria doctor --json",
            "talaria connect --client cursor --json",
            "Docs: README.md · PORTABILITY.md · tools/",
            "Ingest doc: python _tools/ingest_document.py <file>",
            "Graphify project: python _tools/ingest_project.py <path>",
        ],
    }
    print(json.dumps(summary, indent=2))
    if not (md_ok and gy_ok):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
