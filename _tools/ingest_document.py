#!/usr/bin/env python3
"""Convert a document into vault Markdown via MarkItDown."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[1]
OUT_DIR = VAULT / "memory" / "inbox" / "converted"


def ensure_markitdown() -> None:
    try:
        import markitdown  # noqa: F401
    except ImportError:
        print("[auto] installing markitdown[all]…")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markitdown[all]"])


def slug(name: str) -> str:
    s = re.sub(r"[^\w\s\-]+", "", name.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", s).strip("-")[:80] or "document"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="File path or URL")
    ap.add_argument("-o", "--output", help="Optional output .md path")
    args = ap.parse_args()

    ensure_markitdown()
    from markitdown import MarkItDown

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    src = args.source
    md = MarkItDown()
    result = md.convert(src)
    text = result.text_content or ""

    if args.output:
        out = Path(args.output)
    else:
        base = Path(src).stem if not src.startswith("http") else "url"
        out = OUT_DIR / f"{datetime.now().strftime('%Y-%m-%d')}-{slug(base)}.md"

    out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"---\ndate: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"type: converted-document\nsource: {src!r}\n"
        f"tags: [converted, markitdown, inbox]\n---\n\n"
        f"# Converted: {Path(src).name if not src.startswith('http') else src}\n\n"
        f"**Origen:** `{src}`\n\n---\n\n"
    )
    out.write_text(header + text, encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Next: classify via memory/inbox or link from a project note.")


if __name__ == "__main__":
    main()
