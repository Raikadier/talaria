#!/usr/bin/env python3
"""Scan skill banks and build an Obsidian SkillGraph vault."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import time
from collections import defaultdict
from pathlib import Path

VAULT = Path(r"D:\OneDrive - unicesar.edu.co\davidbarcelo0411@g\Business Ideas\SkillGraph")
SOURCES = [
    Path(r"C:\Users\david\AppData\Local\hermes\skills"),
    Path(r"C:\Users\david\Skills"),
]

AXES = {
    "youtube": ["youtube", "video", "thumbnail", "script", "shorts", "channel"],
    "finance": ["finance", "cfo", "budget", "accounting", "pricing", "revenue", "invoice"],
    "coding": ["coding", "code", "developer", "programming", "software", "api", "refactor"],
    "data": ["data", "analytics", "sql", "dashboard", "etl", "bi", "dataset"],
    "marketing": ["marketing", "cmo", "seo", "campaign", "brand", "ads", "growth"],
    "agent": ["agent", "orchestration", "workflow", "automation", "mcp", "tool-use"],
    "design": ["design", "ui", "ux", "figma", "visual", "layout", "typography"],
    "writing": ["writing", "copy", "blog", "content", "editorial", "narrative"],
    "research": ["research", "analysis", "investigate", "literature", "survey"],
    "security": ["security", "auth", "vulnerability", "compliance", "privacy", "crypto"],
    "productivity": ["productivity", "habits", "planning", "notion", "obsidian", "second-brain"],
}

FAOS_MAP = {
    "faos-cmo": "marketing",
    "faos-marketplace": "marketing",
    "faos-cfo": "finance",
    "faos-dev": "coding",
    "faos-cto": "coding",
    "faos-data": "data",
    "faos-design": "design",
    "faos-security": "security",
    "faos-research": "research",
    "faos-ops": "productivity",
    "faos-hr": "productivity",
    "faos-legal": "security",
    "faos-product": "product",
    "faos-sales": "marketing",
    "faos-support": "productivity",
    "faos-content": "writing",
}

MAX_DOMAIN_LINKS = 18
MAX_TAG_LINKS = 12
YAML_SCALAR = re.compile(r'^([A-Za-z0-9_-]+):\s*(.*)$')
YAML_LIST_ITEM = re.compile(r'^-\s+(.+)$')


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^\w\s\-./]", "", s, flags=re.UNICODE)
    s = s.replace("/", "-").replace(".", "-")
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "unnamed"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw, body = parts[1], parts[2]
    data: dict = {}
    current_list_key = None
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        m_item = YAML_LIST_ITEM.match(line.strip())
        if current_list_key and m_item:
            val = m_item.group(1).strip().strip("\"'")
            data.setdefault(current_list_key, []).append(val)
            continue
        m = YAML_SCALAR.match(line.strip())
        if not m:
            current_list_key = None
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw == "" or raw == "|" or raw == ">":
            current_list_key = key
            data[key] = []
            continue
        current_list_key = None
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()]
        else:
            data[key] = raw.strip("\"'")
    return data, body


def first_paragraph(body: str) -> str:
    lines = []
    for line in body.splitlines():
        t = line.strip()
        if not t:
            if lines:
                break
            continue
        if t.startswith("#"):
            continue
        if t.startswith("```"):
            break
        lines.append(t)
        if len(" ".join(lines)) > 280:
            break
    text = " ".join(lines).strip()
    return text[:400] if text else "Sin descripción disponible."


def detect_domain(skill_dir: Path, root: Path, name: str) -> str:
    try:
        rel = skill_dir.relative_to(root)
        parts = list(rel.parts)
    except ValueError:
        parts = list(skill_dir.parts)

    joined = "/".join(p.lower() for p in parts)
    name_l = name.lower()

    for prefix, domain in FAOS_MAP.items():
        if prefix in joined or name_l.startswith(prefix):
            return domain

    if "youtube-social-pack" in joined or name_l.startswith("youtube-") or "youtube" in joined:
        return "youtube"
    if "agensi-free" in joined or name_l.startswith("agensi-"):
        # subclass by immediate parent under agensi-free if useful
        for i, p in enumerate(parts):
            if p.lower() == "agensi-free" and i + 1 < len(parts) - 1:
                sub = parts[i + 1]
                if sub.lower() not in {"skills", "skill"}:
                    return f"agensi-{slugify(sub)}"
        return "agensi"
    if "aiskillsbank" in joined or name_l.startswith("aiskillsbank"):
        return "aiskillsbank"

    # parent folder as domain when nested under a bank package
    if len(parts) >= 2:
        parent = parts[-2]
        if parent.lower() not in {"skills", "skill", "local", "hermes"}:
            return slugify(parent)

    # top-level bank folder
    if parts:
        top = parts[0]
        if top.lower() not in {"skills"}:
            return slugify(top)
    return "general"


def detect_axes(text: str) -> list[str]:
    low = text.lower()
    found = []
    for axis, kws in AXES.items():
        if any(re.search(rf"\b{re.escape(kw)}\b", low) for kw in kws):
            found.append(axis)
    return found


def normalize_tags(raw) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [t.strip() for t in raw.split(",") if t.strip()]
    out = []
    for t in raw:
        t = str(t).strip().lstrip("#").lower()
        t = re.sub(r"\s+", "-", t)
        if t and t not in out:
            out.append(t)
    return out


def find_skill_files() -> list[tuple[Path, Path]]:
    found = []
    for root in SOURCES:
        if not root.exists():
            print(f"[warn] missing source: {root}")
            continue
        print(f"[scan] {root}")
        for dirpath, dirnames, filenames in os.walk(root):
            # skip heavy noise
            dirnames[:] = [d for d in dirnames if d.lower() not in {".git", "node_modules", "__pycache__", ".venv", "venv"}]
            if "SKILL.md" in filenames:
                found.append((Path(dirpath) / "SKILL.md", root))
            elif "skill.md" in filenames:
                found.append((Path(dirpath) / "skill.md", root))
    return found


def wiki(name: str) -> str:
    return f"[[{name}]]"


def yaml_escape(s: str) -> str:
    s = s.replace("\r", " ").replace("\n", " ").strip()
    if any(c in s for c in ':#{}[]&*!|>\'"%@`') or s == "":
        return json.dumps(s, ensure_ascii=False)
    return s


def main() -> None:
    t0 = time.time()
    print("=== SkillGraph builder ===")
    files = find_skill_files()
    print(f"[scan] found {len(files)} SKILL.md files")

    skills: dict[str, dict] = {}
    skipped = 0

    for path, root in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[skip] read fail {path}: {e}")
            skipped += 1
            continue

        fm, body = parse_frontmatter(text)
        name = str(fm.get("name") or path.parent.name).strip()
        if not name:
            skipped += 1
            continue

        desc = str(fm.get("description") or "").strip()
        if not desc:
            desc = first_paragraph(body)
        when = str(fm.get("when_to_use") or fm.get("when-to-use") or "").strip()
        if not when:
            # first non-empty lines after description-ish content
            when = first_paragraph(body)[:280]

        tags = normalize_tags(fm.get("tags") or fm.get("tag"))
        domain = detect_domain(path.parent, root, name)
        axes = detect_axes(f"{name} {desc} {when} {' '.join(tags)}")
        for a in axes:
            if a not in tags:
                tags.append(a)
        if domain not in tags:
            tags.append(domain)

        key = name.lower()
        abs_path = str(path.resolve())
        if key in skills:
            if abs_path not in skills[key]["sources"]:
                skills[key]["sources"].append(abs_path)
            # merge tags/axes
            for t in tags:
                if t not in skills[key]["tags"]:
                    skills[key]["tags"].append(t)
            for a in axes:
                if a not in skills[key]["axes"]:
                    skills[key]["axes"].append(a)
            continue

        skills[key] = {
            "name": name,
            "domain": domain,
            "sources": [abs_path],
            "tags": tags,
            "description": desc,
            "when_to_use": when,
            "axes": axes,
        }

    print(f"[index] unique skills={len(skills)} skipped={skipped}")

    # invert indexes
    by_domain: dict[str, list[str]] = defaultdict(list)
    by_tag: dict[str, list[str]] = defaultdict(list)
    by_axis: dict[str, list[str]] = defaultdict(list)
    for key, s in skills.items():
        by_domain[s["domain"]].append(key)
        for t in s["tags"]:
            by_tag[t].append(key)
        for a in s["axes"]:
            by_axis[a].append(key)

    for d in by_domain:
        by_domain[d].sort()
    for t in by_tag:
        by_tag[t].sort()

    # rebuild output dirs
    skills_root = VAULT / "skills"
    meta = VAULT / "_META"
    axes_dir = meta / "axes"
    domains_dir = meta / "domains"

    if skills_root.exists():
        shutil.rmtree(skills_root)
    for p in (meta, axes_dir, domains_dir, skills_root):
        p.mkdir(parents=True, exist_ok=True)

    # Obsidian config
    obsidian = VAULT / ".obsidian"
    obsidian.mkdir(exist_ok=True)
    (obsidian / "app.json").write_text(
        json.dumps({"alwaysUpdateLinks": True, "newLinkFormat": "shortest", "useMarkdownLinks": False}, indent=2),
        encoding="utf-8",
    )
    (obsidian / "core-plugins.json").write_text(
        json.dumps({"graph": True, "tag-pane": True, "outgoing-link": True, "backlink": True, "search": True}, indent=2),
        encoding="utf-8",
    )

    total_edges = 0
    note_count = 0

    # axis hubs
    for axis in AXES:
        members = sorted(by_axis.get(axis, []), key=lambda k: skills[k]["name"].lower())
        links = "\n".join(f"- {wiki(skills[k]['name'])}" for k in members[:500])
        more = f"\n\n_…y {len(members)-500} más._" if len(members) > 500 else ""
        content = (
            f"---\nname: axis-{axis}\ndomain: _axis\ntags: [axis, {axis}]\n"
            f"description: Eje temático {axis}\n---\n\n"
            f"# Eje: {axis}\n\nSkills conectadas por palabras clave ({len(members)}).\n\n"
            f"## Skills\n{links}{more}\n"
        )
        (axes_dir / f"{axis}.md").write_text(content, encoding="utf-8")
        note_count += 1
        total_edges += min(len(members), 500)

    # domain hubs
    for domain, keys in sorted(by_domain.items()):
        links = "\n".join(f"- {wiki(skills[k]['name'])}" for k in keys)
        content = (
            f"---\nname: domain-{domain}\ndomain: {domain}\ntags: [domain, {domain}]\n"
            f"description: Hub del dominio {domain}\n---\n\n"
            f"# Dominio: {domain}\n\nTotal: **{len(keys)}** skills.\n\n"
            f"## Skills\n{links}\n"
        )
        (domains_dir / f"{domain}.md").write_text(content, encoding="utf-8")
        note_count += 1
        total_edges += len(keys)

    # skill notes
    for key, s in skills.items():
        domain = s["domain"]
        related: list[str] = []
        seen = {key}

        # same domain peers (bidirectional intent via mutual listing; capped for usability)
        peers = by_domain[domain]
        # prefer peers with tag overlap
        tag_set = set(s["tags"])
        scored = []
        for pk in peers:
            if pk in seen:
                continue
            overlap = len(tag_set & set(skills[pk]["tags"]))
            scored.append((overlap, skills[pk]["name"].lower(), pk))
        scored.sort(key=lambda x: (-x[0], x[1]))
        for _, _, pk in scored[:MAX_DOMAIN_LINKS]:
            related.append(pk)
            seen.add(pk)

        # shared tags across domains
        tag_candidates = []
        for t in s["tags"]:
            if t in {domain, "skill", "skills"} or t in AXES:
                continue
            for pk in by_tag.get(t, []):
                if pk in seen:
                    continue
                overlap = len(tag_set & set(skills[pk]["tags"]))
                tag_candidates.append((overlap, skills[pk]["name"].lower(), pk))
        tag_candidates.sort(key=lambda x: (-x[0], x[1]))
        for _, _, pk in tag_candidates[:MAX_TAG_LINKS]:
            if pk not in seen:
                related.append(pk)
                seen.add(pk)

        # axis links
        axis_links = [f"[[{a}]]" for a in s["axes"]]
        # also wiki to axis note filenames under _META/axes — Obsidian resolves by note name
        # Our axis notes are titled "Eje: X" but filename is axis.md — link by filename stem via alias
        # Use explicit path-free names matching file stem
        axis_wikis = [f"[[{a}]]" for a in s["axes"]]

        # Ensure axis note names are linkable: rewrite axis hub titles to match stem
        # Already named files {axis}.md so [[youtube]] works if note name is youtube — frontmatter name is axis-youtube
        # Obsidian links by filename by default with shortest format. Filename stem = axis name. Good.

        domain_hub = f"[[{domain}]]"  # domain hub file stem
        related_lines = [f"- {wiki(skills[pk]['name'])}" for pk in related]
        sources_md = "\n".join(f"- `{src}`" for src in s["sources"])
        tags_yaml = "[" + ", ".join(s["tags"]) + "]"
        primary_source = s["sources"][0]

        body = (
            f"---\n"
            f"name: {yaml_escape(s['name'])}\n"
            f"domain: {yaml_escape(domain)}\n"
            f"source: {yaml_escape(primary_source)}\n"
            f"sources:\n" + "".join(f"  - {yaml_escape(src)}\n" for src in s["sources"]) +
            f"tags: {tags_yaml}\n"
            f"description: {yaml_escape(s['description'])}\n"
            f"---\n\n"
            f"# {s['name']}\n\n"
            f"**Dominio:** {domain_hub}  \n"
            f"**Fuente(s):**\n{sources_md}\n\n"
            f"**Descripción:** {s['description']}\n\n"
            f"**Cuándo usar:** {s['when_to_use']}\n\n"
            f"## Tags\n" + " ".join(f"#{t}" for t in s["tags"]) + "\n\n"
        )
        if axis_wikis:
            body += "## Ejes temáticos\n" + "\n".join(f"- {w}" for w in axis_wikis) + "\n\n"
        body += "## Skills relacionadas\n"
        if related_lines:
            body += "\n".join(related_lines) + "\n"
        else:
            body += f"- {domain_hub}\n"

        out_dir = skills_root / domain
        out_dir.mkdir(parents=True, exist_ok=True)
        # avoid collisions / invalid filenames
        fname = slugify(s["name"]) + ".md"
        # hash suffix if collision on disk with different key
        out_path = out_dir / fname
        if out_path.exists():
            suffix = hashlib.md5(key.encode()).hexdigest()[:6]
            out_path = out_dir / f"{slugify(s['name'])}-{suffix}.md"

        out_path.write_text(body, encoding="utf-8")
        note_count += 1
        total_edges += len(related) + len(s["axes"]) + 1  # related + axes + domain hub

    # Fix axis hub note names so [[youtube]] resolves: set filename-only linking
    # Rewrite axis files with H1 matching stem for clarity
    for axis in AXES:
        members = sorted(by_axis.get(axis, []), key=lambda k: skills[k]["name"].lower())
        links = "\n".join(f"- {wiki(skills[k]['name'])}" for k in members[:500])
        more = f"\n\n_…y {len(members)-500} más._" if len(members) > 500 else ""
        content = (
            f"---\naliases: [axis-{axis}, eje-{axis}]\ntags: [axis, {axis}]\n"
            f"description: Eje temático {axis}\n---\n\n"
            f"# {axis}\n\nEje temático **{axis}** — {len(members)} skills.\n\n"
            f"## Skills\n{links}{more}\n"
        )
        (axes_dir / f"{axis}.md").write_text(content, encoding="utf-8")

    for domain, keys in by_domain.items():
        links = "\n".join(f"- {wiki(skills[k]['name'])}" for k in keys)
        content = (
            f"---\naliases: [domain-{domain}, dominio-{domain}]\ntags: [domain, {domain}]\n"
            f"description: Hub del dominio {domain}\n---\n\n"
            f"# {domain}\n\nDominio **{domain}** — **{len(keys)}** skills.\n\n"
            f"## Skills\n{links}\n"
        )
        (domains_dir / f"{domain}.md").write_text(content, encoding="utf-8")

    # taxonomy
    tax_lines = ["# Taxonomía de dominios\n", f"Total skills únicas: **{len(skills)}**\n", f"Total dominios: **{len(by_domain)}**\n", "## Conteo por dominio\n"]
    for domain, keys in sorted(by_domain.items(), key=lambda x: (-len(x[1]), x[0])):
        tax_lines.append(f"- [[{domain}]] — {len(keys)}")
    tax_lines.append("\n## Ejes temáticos\n")
    for axis in AXES:
        tax_lines.append(f"- [[{axis}]] — {len(by_axis.get(axis, []))}")
    (meta / "taxonomy.md").write_text("\n".join(tax_lines) + "\n", encoding="utf-8")
    note_count += 1

    # stats
    def dir_size(p: Path) -> int:
        total = 0
        for root, _, files in os.walk(p):
            for f in files:
                try:
                    total += (Path(root) / f).stat().st_size
                except OSError:
                    pass
        return total

    size_bytes = dir_size(VAULT)
    size_mb = size_bytes / (1024 * 1024)

    # README
    top_domains = sorted(by_domain.items(), key=lambda x: -len(x[1]))[:25]
    domain_table = "\n".join(f"| [[{d}]] | {len(ks)} |" for d, ks in top_domains)
    readme = f"""# SkillGraph — Segundo cerebro de skills

Vault Obsidian con **grafo interconectado** de skills indexadas desde Hermes y Skills de David.
Sincronizado vía OneDrive.

## Resumen

| Métrica | Valor |
|--------|------:|
| Skills únicas | {len(skills)} |
| Archivos SKILL.md escaneados | {len(files)} |
| Dominios | {len(by_domain)} |
| Notas totales (aprox.) | {note_count} |
| Aristas (wiki-links generados) | {total_edges} |
| Tamaño vault | {size_mb:.2f} MB |

### Fuentes escaneadas

1. `C:\\Users\\david\\AppData\\Local\\hermes\\skills\\` (banco Hermes)
2. `C:\\Users\\david\\Skills\\` (agensi-free, aiskillsbank, youtube-social-pack)

Los duplicados por nombre se indexan **una sola vez**; ambas rutas aparecen en el frontmatter `sources`.

## Cómo navegar el grafo

1. Abre esta carpeta como vault en Obsidian (**Open folder as vault**).
2. Usa **Graph View** para ver el mapa; filtra por `#youtube`, `#finance`, `#coding`, etc.
3. Entra por [[taxonomy]] o por un dominio (ej. hubs en `_META/domains/`).
4. Cada skill enlaza a: hub de dominio, peers del mismo dominio, skills con tags solapados, y ejes temáticos.

### Ejes temáticos

{" · ".join(f"[[{a}]]" for a in AXES)}

## Top dominios

| Dominio | Skills |
|---------|-------:|
{domain_table}

## Regenerar el vault

```powershell
python "{VAULT / 'build_skillgraph.py'}"
```

Solo **lee** los `SKILL.md` origen; no los modifica.

## Consulta vía MCP de Obsidian

Si tienes un servidor MCP tipo `mcp-obsidian` / `obsidian-mcp`:

1. Apunta `OBSIDIAN_VAULT_PATH` (o equivalente) a:
   `{VAULT}`
2. Reinicia Cursor / el servidor MCP.
3. Usa herramientas tipo `search`, `list_files`, `get_file_contents` sobre notas en `skills/` y `_META/`.

Si no hay MCP de Obsidian instalado, este vault sigue siendo plenamente usable abriéndolo en la app Obsidian (desktop). OneDrive mantiene el backup en la nube automáticamente.

## Estructura

```
SkillGraph/
  README.md
  build_skillgraph.py
  _META/
    taxonomy.md
    domains/<dominio>.md
    axes/<eje>.md
  skills/<dominio>/<skill>.md
```

---
Generado automáticamente · {time.strftime('%Y-%m-%d %H:%M')} · {time.time()-t0:.1f}s
"""
    (VAULT / "README.md").write_text(readme, encoding="utf-8")

    stats = {
        "unique_skills": len(skills),
        "scanned_files": len(files),
        "domains": len(by_domain),
        "notes": note_count,
        "edges": total_edges,
        "size_bytes": size_bytes,
        "size_mb": round(size_mb, 2),
        "elapsed_sec": round(time.time() - t0, 1),
        "top_domains": {d: len(ks) for d, ks in top_domains},
    }
    (meta / "build_stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print("=== DONE ===")


if __name__ == "__main__":
    main()
