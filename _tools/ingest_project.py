#!/usr/bin/env python3
"""Run Graphify on a programming project and mirror outputs into the vault."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[1]
GRAPHS = VAULT / "memory" / "graphs"


def ensure_graphify() -> str:
    exe = shutil.which("graphify")
    if exe:
        return exe
    print("[auto] installing graphifyy…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "graphifyy[pdf,office,mcp]"])
    exe = shutil.which("graphify")
    if not exe:
        raise SystemExit("graphify CLI not found after install")
    return exe


def slug(name: str) -> str:
    s = re.sub(r"[^\w\s\-]+", "", name.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", s).strip("-")[:80] or "project"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path, help="Path to code project")
    ap.add_argument("--name", help="Name for vault graph folder")
    args = ap.parse_args()

    project = args.project.resolve()
    if not project.exists():
        raise SystemExit(f"Project not found: {project}")

    graphify = ensure_graphify()
    # Prefer local AST update (no API key)
    cmd = [graphify, "update", str(project), "--force"]
    print(">", " ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        # fallback extract-style if update unsupported on older builds
        cmd2 = [graphify, "cluster-only", str(project)]
        print("[fallback]", " ".join(cmd2))
        subprocess.run(cmd2, check=False)

    src_out = project / "graphify-out"
    name = slug(args.name or project.name)
    dest = GRAPHS / name
    dest.mkdir(parents=True, exist_ok=True)

    copied = []
    if src_out.exists():
        for item in src_out.iterdir():
            target = dest / item.name
            if item.is_file():
                shutil.copy2(item, target)
                copied.append(item.name)
            elif item.is_dir() and item.name in {"converted"}:
                if target.exists():
                    shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(item, target)
                copied.append(item.name + "/")

    note = dest / "README.md"
    note.write_text(
        f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
type: project-graph
tags: [graphify, project, graph]
project_path: {project.as_posix()}
---

# Graphify: {project.name}

**Proyecto:** `{project}`
**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Archivos copiados:** {', '.join(copied) or 'ninguno (revisa graphify-out en el proyecto)'}

## Cómo consultar

- Abre `GRAPH_REPORT.md` / `graph.html` en esta carpeta si existen
- Desde CLI: `graphify explain "NodeName" --graph "{(dest / 'graph.json').as_posix()}"`
- MCP: `python -m graphify.serve "{(dest / 'graph.json').as_posix()}"`

## Enlaces

- Tools: [[graphify]] · [[tools-index|herramientas]]
- Home: [[Home]]
""",
        encoding="utf-8",
    )
    print(f"Vault graph folder: {dest}")


if __name__ == "__main__":
    main()
