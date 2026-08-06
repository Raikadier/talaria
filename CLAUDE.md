# CLAUDE.md — Talaria / SPINE (Claude Code)

You are piloting the **Talaria** organism. This vault is the body; **SPINE** is the nervous-system protocol (formerly IRONMAN). Your built-in Claude Code tools stay on; they are sensors and actuators, not a second source of truth.

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
2. Do not create a parallel notes database outside Talaria.
3. After useful work: write conversation/decision/learning/project notes.
4. Never store secrets in the vault.
5. Prefer Retrieve (vault + AXON) before re-ingesting the same source.
6. Respond to the user in **Spanish** unless they ask otherwise; code stays as needed.

## Boot
```bash
python bootstrap.py --check-only
# or agent discovery:
talaria describe --json
```
If deps missing: `python bootstrap.py` or `talaria boot`

Prefer MCP server `talaria` (tools `talaria_*`) + MCP `obsidian` for note CRUD. See `_META/agent-connect.md`.

## Create an agent / FORGE profile
When the user asks to create an agent using Talaria (e.g. "crea un agente que sepa responder correos usando talaria"):
1. `talaria forge build --brief "<their request>" --json` **or** MCP `talaria_forge_build`
2. Optional graph: `--kind orchestrator|specialist` / `--invokes` / `--invocable-by` (user owns the org chart — see `_META/forge/delegation.md`)
3. Execute the returned `pilot_playbook` (fill corpus, `forge check`, activate, then `forge run` / `forge invoke`)
4. Do **not** invent a disposable system prompt outside the vault

## Ingest helpers
```bash
talaria ingest doc <file-or-url>
talaria ingest project <repo-path>
```
