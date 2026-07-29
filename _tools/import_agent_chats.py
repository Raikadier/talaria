#!/usr/bin/env python3
"""Import Hermes, Claude Code, and Cursor chats/context into SkillGraph memory."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path(r"D:\OneDrive - unicesar.edu.co\davidbarcelo0411@g\Business Ideas\Talaria")
OUT_CONV = VAULT / "memory" / "conversations"
OUT_CTX = VAULT / "memory" / "context"
OUT_LEARN = VAULT / "memory" / "learnings"
OUT_ARCH = VAULT / "memory" / "archives"

HERMES = Path(r"C:\Users\david\AppData\Local\hermes")
CLAUDE = Path(r"C:\Users\david\.claude")
CURSOR_PROJECTS = Path(r"C:\Users\david\.cursor\projects")
CURSOR_CHATS = Path(r"C:\Users\david\.cursor\chats")

MAX_ASSISTANT_CHARS = 3500
MAX_USER_CHARS = 8000
MAX_TOTAL_NOTE_CHARS = 120_000
SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|bearer|sk-[a-z0-9]{10,}|ghp_[a-z0-9]{20,}|xox[baprs]-[a-z0-9-]+)\s*[:=]\s*\S+"
)


def slug(s: str, max_len: int = 60) -> str:
    s = re.sub(r"[^\w\s\-]+", "", (s or "").strip().lower(), flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s).strip("-")
    return (s[:max_len] or "sin-titulo").strip("-")


def redact(text: str) -> str:
    if not text:
        return ""
    text = SECRET_RE.sub(r"\1=[REDACTED]", text)
    text = text.replace("\x00", "")
    return text


def yaml_escape(s: str) -> str:
    s = (s or "").replace("\r", " ").replace("\n", " ").strip()
    return json.dumps(s, ensure_ascii=False)


def extract_text_content(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text" and "text" in block:
                    parts.append(str(block["text"]))
                elif "text" in block:
                    parts.append(str(block["text"]))
                elif block.get("type") == "tool_use":
                    parts.append(f"[tool:{block.get('name','?')}]")
                elif block.get("type") == "tool_result":
                    parts.append("[tool_result]")
        return "\n".join(parts)
    if isinstance(content, dict):
        if "text" in content:
            return str(content["text"])
        return json.dumps(content, ensure_ascii=False)[:2000]
    return str(content)


def clean_user_query(text: str) -> str:
    """Prefer <user_query> body from Cursor transcripts."""
    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # strip heavy system wrappers
    text = re.sub(r"<plugin_info[\s\S]*?</plugin_info>", "", text)
    text = re.sub(r"<agent_transcripts>[\s\S]*?</agent_transcripts>", "", text)
    return text.strip()


def title_from_messages(msgs: list[tuple[str, str]], fallback: str) -> str:
    for role, content in msgs:
        if role == "user" and content.strip():
            line = clean_user_query(content).splitlines()[0].strip()
            line = re.sub(r"\s+", " ", line)
            if len(line) > 8:
                return line[:90]
    return fallback


def ts_to_date(ts) -> str:
    if ts is None:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        if isinstance(ts, (int, float)):
            # hermes often uses unix float seconds
            if ts > 1e12:  # ms
                ts = ts / 1000.0
            return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
        s = str(ts)
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s).astimezone().strftime("%Y-%m-%d")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d")


def write_conversation(
    *,
    source: str,
    session_id: str,
    title: str,
    date: str,
    project: str,
    source_path: str,
    messages: list[tuple[str, str]],
    extra_tags: list[str] | None = None,
) -> Path | None:
    if not messages:
        return None

    out_dir = OUT_CONV / source
    out_dir.mkdir(parents=True, exist_ok=True)

    short = slug(title)
    # full id hash avoids collisions when the same chat UUID appears in multiple project folders
    sid = re.sub(r"[^\w\-]+", "-", session_id)[:36]
    path_hash = hashlib.md5(source_path.encode("utf-8", errors="ignore")).hexdigest()[:8]
    fname = f"{date}-{source}-{short}-{sid}-{path_hash}.md"
    path = out_dir / fname

    tags = ["conversation", "imported", source] + (extra_tags or [])
    body_parts = []
    body_parts.append("---")
    body_parts.append(f"date: {date}")
    body_parts.append("type: conversation")
    body_parts.append(f"source_agent: {source}")
    body_parts.append(f"session_id: {yaml_escape(session_id)}")
    body_parts.append(f"project: {yaml_escape(project)}")
    body_parts.append(f"source_path: {yaml_escape(source_path)}")
    body_parts.append(f"tags: [{', '.join(tags)}]")
    body_parts.append(f"title: {yaml_escape(title)}")
    body_parts.append("---")
    body_parts.append("")
    body_parts.append(f"# {title}")
    body_parts.append("")
    body_parts.append(f"**Fecha:** {date}  ")
    body_parts.append(f"**Agente:** {source}  ")
    body_parts.append(f"**Proyecto/contexto:** {project or '—'}  ")
    body_parts.append(f"**Sesión:** `{session_id}`  ")
    body_parts.append(f"**Origen:** `{source_path}`")
    body_parts.append("")
    body_parts.append("## Mensajes")
    body_parts.append("")

    total = 0
    user_count = 0
    asst_count = 0
    for role, content in messages:
        content = redact(content or "")
        if role == "user":
            content = clean_user_query(content)
            if len(content) > MAX_USER_CHARS:
                content = content[:MAX_USER_CHARS] + "\n\n_[truncado]_"
            user_count += 1
            label = "Usuario"
        elif role == "assistant":
            # drop pure tool scaffolding
            if content.strip() in {"[REDACTED]", ""}:
                continue
            content = re.sub(r"\[REDACTED\]", "", content)
            if len(content) > MAX_ASSISTANT_CHARS:
                content = content[:MAX_ASSISTANT_CHARS] + "\n\n_[truncado]_"
            asst_count += 1
            label = "Asistente"
        elif role in {"system", "tool"}:
            continue
        else:
            label = role

        chunk = f"### {label}\n\n{content.strip()}\n"
        if total + len(chunk) > MAX_TOTAL_NOTE_CHARS:
            body_parts.append("\n_[Nota truncada por tamaño; ver archivo origen]_\n")
            break
        body_parts.append(chunk)
        total += len(chunk)

    if user_count == 0 and asst_count == 0:
        return None

    body_parts.append("")
    body_parts.append("## Enlaces")
    body_parts.append(f"- Índice: [[{source}-import-index]]")
    body_parts.append("- Home: [[Home]]")
    body_parts.append("")

    path.write_text("\n".join(body_parts), encoding="utf-8")
    return path


def import_hermes(stats: dict) -> list[Path]:
    written = []
    db = HERMES / "state.db"
    if not db.exists():
        print("[hermes] state.db missing")
        return written

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    sessions = con.execute(
        "SELECT id, source, title, display_name, cwd, started_at, ended_at, message_count, model FROM sessions ORDER BY started_at"
    ).fetchall()
    print(f"[hermes] sessions={len(sessions)}")

    for s in sessions:
        sid = s["id"]
        rows = con.execute(
            "SELECT role, content, timestamp FROM messages WHERE session_id=? AND active=1 ORDER BY id",
            (sid,),
        ).fetchall()
        msgs = []
        for r in rows:
            role = (r["role"] or "").lower()
            content = r["content"] or ""
            if role in {"user", "assistant"} and content.strip():
                msgs.append((role, content))
        if not msgs:
            continue
        title = s["title"] or s["display_name"] or title_from_messages(msgs, f"hermes-{sid}")
        date = ts_to_date(s["started_at"])
        project = s["cwd"] or s["source"] or ""
        p = write_conversation(
            source="hermes",
            session_id=sid,
            title=title,
            date=date,
            project=project,
            source_path=str(db),
            messages=msgs,
            extra_tags=[s["source"]] if s["source"] else None,
        )
        if p:
            written.append(p)

    con.close()

    # Context / soul / memories
    OUT_CTX.mkdir(parents=True, exist_ok=True)
    ctx_dir = OUT_CTX / "hermes"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    for name in ["SOUL.md", "config.yaml"]:
        src = HERMES / name
        if src.exists():
            dst = ctx_dir / name
            shutil.copy2(src, dst)
            stats["context_files"] += 1
    mem_dir = HERMES / "memories"
    if mem_dir.exists():
        for src in mem_dir.glob("*.md"):
            shutil.copy2(src, ctx_dir / src.name)
            stats["context_files"] += 1
            # also promote as learning notes
            date = datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d")
            learn = OUT_LEARN / f"{date}-hermes-{slug(src.stem)}.md"
            body = redact(src.read_text(encoding="utf-8", errors="replace"))
            learn.write_text(
                f"---\ndate: {date}\ntype: learning\nsource_agent: hermes\ntags: [learning, imported, hermes]\n---\n\n"
                f"# Hermes context: {src.stem}\n\nImportado desde `{src}`\n\n{body}\n",
                encoding="utf-8",
            )
            stats["learnings"] += 1

    # history file
    hist = HERMES / ".hermes_history"
    if hist.exists():
        shutil.copy2(hist, ctx_dir / "hermes_history.txt")
        stats["context_files"] += 1

    stats["hermes_conversations"] = len(written)
    return written


def import_claude(stats: dict) -> list[Path]:
    written = []
    root = CLAUDE / "projects"
    if not root.exists():
        print("[claude] projects missing")
        return written

    files = list(root.rglob("*.jsonl"))
    print(f"[claude] jsonl={len(files)}")

    for f in files:
        project = f.parent.name.replace("--", "/").replace("-", " ")
        # better project path decode: Claude uses D--OneDrive---...
        project = f.parent.name
        session_id = f.stem
        title = None
        msgs: list[tuple[str, str]] = []
        date = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")

        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = o.get("type")
            if t == "custom-title" and o.get("customTitle"):
                title = o["customTitle"]
            elif t == "user":
                msg = o.get("message") or {}
                content = extract_text_content(msg.get("content"))
                if content.strip():
                    msgs.append(("user", content))
                ts = o.get("timestamp")
                if ts:
                    date = ts_to_date(ts)
            elif t == "assistant":
                msg = o.get("message") or {}
                content = extract_text_content(msg.get("content"))
                # skip tool-only
                if content.strip() and not content.strip().startswith("[tool:"):
                    msgs.append(("assistant", content))

        if not msgs:
            continue
        title = title or title_from_messages(msgs, f"claude-{session_id[:8]}")
        p = write_conversation(
            source="claude-code",
            session_id=session_id,
            title=title,
            date=date,
            project=project,
            source_path=str(f),
            messages=msgs,
        )
        if p:
            written.append(p)

    # plans + settings as context
    ctx = OUT_CTX / "claude-code"
    ctx.mkdir(parents=True, exist_ok=True)
    for sub in ["plans", "settings.json"]:
        src = CLAUDE / sub
        if src.is_file():
            try:
                shutil.copy2(src, ctx / src.name)
                stats["context_files"] += 1
            except Exception as e:
                print(f"[claude] copy skip {src}: {e}")
        elif src.is_dir():
            dst = ctx / sub
            try:
                if dst.exists():
                    shutil.rmtree(dst, ignore_errors=True)
                if not dst.exists():
                    shutil.copytree(src, dst)
                    stats["context_files"] += sum(1 for _ in dst.rglob("*") if _.is_file())
                else:
                    # fallback: copy files individually
                    dst.mkdir(parents=True, exist_ok=True)
                    for f in src.rglob("*"):
                        if f.is_file():
                            target = dst / f.relative_to(src)
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(f, target)
                            stats["context_files"] += 1
            except Exception as e:
                print(f"[claude] plans copy skip: {e}")

    stats["claude_conversations"] = len(written)
    return written


def import_cursor_transcripts(stats: dict) -> list[Path]:
    written = []
    files = list(CURSOR_PROJECTS.glob("**/agent-transcripts/**/*.jsonl"))
    print(f"[cursor] transcripts={len(files)}")

    # Prefer the richest copy when the same UUID exists in multiple project folders
    best_by_id: dict[str, tuple[Path, str, list[tuple[str, str]], str]] = {}

    for f in files:
        try:
            parts = f.parts
            idx = parts.index("projects")
            project = parts[idx + 1]
        except Exception:
            project = "unknown"

        session_id = f.stem
        msgs: list[tuple[str, str]] = []
        date = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")

        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = (o.get("role") or "").lower()
            message = o.get("message") or {}
            content = extract_text_content(message.get("content"))
            if role in {"user", "assistant"} and content.strip():
                if role == "assistant" and re.fullmatch(r"(\[tool:\S+\]\s*)+", content.strip()):
                    continue
                msgs.append((role, content))

        if not msgs:
            continue

        prev = best_by_id.get(session_id)
        score = sum(len(c) for _, c in msgs)
        if prev is None or score > sum(len(c) for _, c in prev[2]):
            best_by_id[session_id] = (f, project, msgs, date)

    print(f"[cursor] unique sessions={len(best_by_id)} (deduped from {len(files)})")

    for session_id, (f, project, msgs, date) in best_by_id.items():
        title = title_from_messages(msgs, f"cursor-{session_id[:8]}")
        p = write_conversation(
            source="cursor",
            session_id=session_id,
            title=title,
            date=date,
            project=project,
            source_path=str(f),
            messages=msgs,
        )
        if p:
            written.append(p)

    stats["cursor_conversations"] = len(written)
    stats["cursor_transcript_files"] = len(files)
    return written


def import_cursor_store_dbs(stats: dict) -> list[Path]:
    """Best-effort extract from Cursor chat store.db files."""
    written = []
    if not CURSOR_CHATS.exists():
        return written
    dbs = list(CURSOR_CHATS.rglob("store.db"))
    print(f"[cursor] store.db={len(dbs)}")
    for db in dbs:
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            # heuristic: look for blobs/text with json messages
            msgs: list[tuple[str, str]] = []
            for t in tables:
                cols = [c[1] for c in con.execute(f"PRAGMA table_info([{t}])").fetchall()]
                # try common patterns
                text_cols = [c for c in cols if any(x in c.lower() for x in ("text", "content", "value", "data", "json", "message"))]
                if not text_cols:
                    continue
                col = text_cols[0]
                try:
                    rows = con.execute(f"SELECT [{col}] FROM [{t}] LIMIT 500").fetchall()
                except Exception:
                    continue
                for (val,) in rows:
                    if not val:
                        continue
                    if isinstance(val, bytes):
                        try:
                            val = val.decode("utf-8", errors="replace")
                        except Exception:
                            continue
                    s = str(val)
                    if '"role"' in s and ("user" in s or "assistant" in s):
                        try:
                            o = json.loads(s)
                        except Exception:
                            continue
                        # nested shapes
                        candidates = []
                        if isinstance(o, dict):
                            if "role" in o:
                                candidates = [o]
                            elif "messages" in o and isinstance(o["messages"], list):
                                candidates = o["messages"]
                        elif isinstance(o, list):
                            candidates = o
                        for m in candidates:
                            if not isinstance(m, dict):
                                continue
                            role = (m.get("role") or "").lower()
                            content = extract_text_content(m.get("content") or m.get("text"))
                            if role in {"user", "assistant"} and content.strip():
                                msgs.append((role, content))
            con.close()
            if not msgs:
                continue
            meta = db.parent / "meta.json"
            project = ""
            date = datetime.fromtimestamp(db.stat().st_mtime).strftime("%Y-%m-%d")
            if meta.exists():
                try:
                    md = json.loads(meta.read_text(encoding="utf-8"))
                    project = md.get("cwd") or ""
                    if md.get("createdAtMs"):
                        date = ts_to_date(md["createdAtMs"])
                except Exception:
                    pass
            sid = db.parent.name
            title = title_from_messages(msgs, f"cursor-chat-{sid[:8]}")
            p = write_conversation(
                source="cursor",
                session_id=sid,
                title=title,
                date=date,
                project=project,
                source_path=str(db),
                messages=msgs,
                extra_tags=["cursor-chat-db"],
            )
            if p:
                written.append(p)
                stats["cursor_store_dbs"] = stats.get("cursor_store_dbs", 0) + 1
        except Exception as e:
            print(f"[cursor] store.db skip {db}: {e}")
    return written


def write_indexes(paths_by_source: dict[str, list[Path]], stats: dict) -> None:
    for source, paths in paths_by_source.items():
        lines = [
            "---",
            f"tags: [moc, imported, {source}]",
            f"aliases: [{source}-chats]",
            "---",
            "",
            f"# Import {source}",
            "",
            f"Conversaciones importadas: **{len(paths)}**",
            "",
            "## Lista",
            "",
        ]
        for p in sorted(paths, key=lambda x: x.name, reverse=True):
            # link by filename stem
            lines.append(f"- [[{p.stem}]]")
        lines.append("")
        lines.append("## Ver también")
        lines.append("- [[Home]] · [[memory-index]] · [[import-master-index]]")
        (OUT_CONV / f"{source}-import-index.md").write_text("\n".join(lines), encoding="utf-8")

    master = [
        "---",
        "tags: [moc, imported]",
        "aliases: [importaciones, chats-importados]",
        "---",
        "",
        "# Índice maestro de importaciones",
        "",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Totales",
        "",
        f"- Hermes: {stats.get('hermes_conversations', 0)}",
        f"- Claude Code: {stats.get('claude_conversations', 0)}",
        f"- Cursor: {stats.get('cursor_conversations', 0)} (+ store.db: {stats.get('cursor_store_dbs', 0)})",
        f"- Learnings/context files: {stats.get('learnings', 0)} / {stats.get('context_files', 0)}",
        "",
        "## Índices por fuente",
        "",
        "- [[hermes-import-index]]",
        "- [[claude-code-import-index]]",
        "- [[cursor-import-index]]",
        "",
        "## Contexto importado",
        "",
        "- `memory/context/hermes/` (SOUL, MEMORY, USER, config)",
        "- `memory/context/claude-code/` (plans, settings)",
        "",
        "## Protocolo",
        "",
        "Nuevas sesiones útiles → escribir en `memory/conversations/` según [[agent-protocol]].",
        "Esta importación es el histórico baseline.",
        "",
    ]
    (OUT_CONV / "import-master-index.md").write_text("\n".join(master), encoding="utf-8")


def update_home_and_memory_index(stats: dict) -> None:
    home = VAULT / "Home.md"
    if home.exists():
        text = home.read_text(encoding="utf-8")
        marker = "## Última sesión registrada"
        block = (
            "## Última sesión registrada\n\n"
            f"- Import histórico: [[import-master-index]] "
            f"(Hermes {stats.get('hermes_conversations',0)} · "
            f"Claude {stats.get('claude_conversations',0)} · "
            f"Cursor {stats.get('cursor_conversations',0)})\n"
            "- [[2026-07-28-skillgraph-segundo-cerebro]] — vault + capa memoria\n"
        )
        if marker in text:
            # replace section until next ## or end
            pre, rest = text.split(marker, 1)
            # drop old section body
            if "\n## " in rest:
                _, after = rest.split("\n## ", 1)
                text = pre + block + "\n## " + after
            else:
                text = pre + block
        else:
            text = text.rstrip() + "\n\n" + block
        home.write_text(text, encoding="utf-8")

    mi = VAULT / "memory" / "memory-index.md"
    if mi.exists():
        text = mi.read_text(encoding="utf-8")
        if "import-master-index" not in text:
            text = text.rstrip() + (
                "\n\n## Importaciones históricas\n\n"
                "- [[import-master-index]] — chats Hermes / Claude Code / Cursor\n"
                "- Contexto: `memory/context/`\n"
            )
            mi.write_text(text, encoding="utf-8")


def clear_dir(d: Path) -> None:
    """Delete files in directory; tolerate OneDrive locks."""
    d.mkdir(parents=True, exist_ok=True)
    for p in list(d.glob("*")):
        try:
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
        except Exception as e:
            print(f"[warn] could not remove {p}: {e}")


def main() -> None:
    t0 = time.time()
    stats = defaultdict(int)
    print("=== Import to SkillGraph memory ===")

    # clean previous imports (idempotent re-run)
    for source in ("hermes", "claude-code", "cursor"):
        clear_dir(OUT_CONV / source)

    hermes_paths = import_hermes(stats)
    claude_paths = import_claude(stats)
    cursor_paths = import_cursor_transcripts(stats)
    cursor_paths += import_cursor_store_dbs(stats)

    by_source = {
        "hermes": hermes_paths,
        "claude-code": claude_paths,
        "cursor": cursor_paths,
    }
    write_indexes(by_source, stats)
    update_home_and_memory_index(stats)

    # migration log conversation
    date = datetime.now().strftime("%Y-%m-%d")
    log = OUT_CONV / f"{date}-importacion-historica-agentes.md"
    log.write_text(
        f"""---
date: {date}
type: conversation
tags: [conversation, import, skillgraph]
---

# Importación histórica Hermes / Claude Code / Cursor

**Fecha:** {date}
**Agente:** Cursor

## Resumen
Se migraron chats y contexto al segundo cerebro SkillGraph.

## Totales
- Hermes: {stats['hermes_conversations']} conversaciones (+ MEMORY/USER/SOUL en context)
- Claude Code: {stats['claude_conversations']} conversaciones
- Cursor transcripts: {stats['cursor_conversations']} (+ store.db: {stats.get('cursor_store_dbs', 0)})
- Context files: {stats['context_files']}
- Learnings promovidos: {stats['learnings']}

## Índices
- [[import-master-index]]
- [[hermes-import-index]] · [[claude-code-import-index]] · [[cursor-import-index]]

## Enlaces
- [[Home]] · [[SkillGraph]] · [[agent-protocol]]
""",
        encoding="utf-8",
    )

    elapsed = time.time() - t0
    summary = {
        "hermes": stats["hermes_conversations"],
        "claude_code": stats["claude_conversations"],
        "cursor": stats["cursor_conversations"],
        "cursor_store_dbs": stats.get("cursor_store_dbs", 0),
        "context_files": stats["context_files"],
        "learnings": stats["learnings"],
        "elapsed_sec": round(elapsed, 1),
        "total_notes": len(hermes_paths) + len(claude_paths) + len(cursor_paths),
    }
    (VAULT / "memory" / "archives").mkdir(parents=True, exist_ok=True)
    (OUT_ARCH / "last_import_stats.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("=== DONE ===")


if __name__ == "__main__":
    main()
