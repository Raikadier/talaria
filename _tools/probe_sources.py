#!/usr/bin/env python3
"""Probe Hermes/Claude/Cursor storage shapes for import."""
import json
import sqlite3
from pathlib import Path
from collections import Counter

hermes = Path(r"C:\Users\david\AppData\Local\hermes")
f = next((hermes / "sessions").glob("*.json"))
d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
print("HERMES keys", list(d.keys()))
for k, v in d.items():
    if isinstance(v, (list, dict, str)):
        print(f"  {k}: {type(v).__name__} len={len(v)}")
    else:
        print(f"  {k}: {type(v).__name__}={v}")

# try find messages nested
def find_msgs(obj, path="$"):
    if isinstance(obj, dict):
        if "messages" in obj and isinstance(obj["messages"], list):
            print("FOUND messages at", path, "n=", len(obj["messages"]))
            if obj["messages"]:
                print("  first keys", obj["messages"][0].keys() if isinstance(obj["messages"][0], dict) else type(obj["messages"][0]))
                print("  first sample", str(obj["messages"][0])[:400])
        for k, v in obj.items():
            find_msgs(v, path + "." + k)
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict) and {"role", "content"} <= set(obj[0].keys()):
        print("FOUND role/content list at", path, "n=", len(obj))

find_msgs(d)

print("\nMEMORIES tree:")
for p in sorted((hermes / "memories").rglob("*")):
    print(" ", p.relative_to(hermes / "memories"), "file" if p.is_file() else "dir", p.stat().st_size if p.is_file() else "")

db = hermes / "state.db"
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
tables = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("\nSTATE TABLES", [t[0] for t in tables])
for (t,) in tables:
    try:
        n = con.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
        cols = [c[1] for c in con.execute(f"PRAGMA table_info([{t}])").fetchall()]
        print(f"  {t}: {n} cols={cols}")
        if n and t.lower() in {"sessions", "messages", "conversation", "conversations", "chat", "memory", "memories"}:
            row = con.execute(f"SELECT * FROM [{t}] LIMIT 1").fetchone()
            print("   sample", str(row)[:300])
    except Exception as e:
        print("  err", t, e)
con.close()

# cursor chat conversation payload
chat_root = Path(r"C:\Users\david\.cursor\chats")
for p in chat_root.rglob("*"):
    if p.is_file() and p.name != "meta.json":
        print("\nCURSOR CHAT FILE", p, p.stat().st_size)
        raw = p.read_bytes()[:200]
        print("  magic", raw[:40])
