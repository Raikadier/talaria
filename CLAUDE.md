# CLAUDE.md — SkillGraph / SPINE (Claude Code)

You are piloting the **SkillGraph** organism. This vault is the body; **SPINE** is the nervous-system protocol (formerly IRONMAN). Your built-in Claude Code tools stay on; they are sensors and actuators, not a second source of truth.

## Constitution (read first)
- `_META/organism.md` — one body, many organs
- `_META/spine-framework.md` — SPINE layers + tool ownership
- `_META/axon.md` — AXON skill network
- `_META/adapters/claude-code.md` — how your native tools map to SPINE
- `_META/agent-protocol.md` — what to write where
- `_META/forge/forge.md` — FORGE role profiles
- `Home.md` — entry map

## Native tools → SPINE
| Your tool | Layer |
|-----------|--------|
| WebFetch / Bash curl / scrapers | Ingest |
| Bash (`markitdown`, `graphify`, `yt-dlp`, …) | Ingest / Normalize / Act |
| Read / Grep / Glob on vault | Retrieve |
| Write / Edit on `memory/**` | Memorize |
| Agent / Task | Act (pass this CLAUDE.md) |
| MCP `obsidian` | Retrieve + Memorize |

## Rules
1. Canonical memory = this vault (Markdown). Session/chat memory is ephemeral.
2. Do not create a parallel notes database outside SkillGraph.
3. After useful work: write conversation/decision/learning/project notes.
4. Never store secrets in the vault.
5. Prefer Retrieve (vault + AXON) before re-ingesting the same source.
6. Respond to the user in **Spanish** unless they ask otherwise; code stays as needed.

## Boot
```bash
python bootstrap.py --check-only
# or agent discovery:
python -m skillgraph_cli describe --json
```
If deps missing: `python bootstrap.py` or `python -m skillgraph_cli boot`

Prefer MCP server `skillgraph` (tools `skillgraph_*`) + MCP `obsidian` for note CRUD. See `_META/agent-connect.md`.

## Ingest helpers
```bash
python -m skillgraph_cli ingest doc <file-or-url>
python -m skillgraph_cli ingest project <repo-path>
```
