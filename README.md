# Talaria

**Traje cognitivo** para cualquier agente de IA: memoria durable (vault Obsidian), grafo de skills (AXON), perfiles elite (FORGE) y protocolo SPINE, expuestos como **CLI + MCP**.

> Antes: SkillGraph. Ahora: **Talaria** — mismo organismo, API instalable en cualquier PC.

**Vocabulario:** el **piloto** es el modelo; el **vehículo** es Cursor / Claude Code / Hermes / etc.; **Talaria** es el traje (segundo cerebro) — no sustituye al chat ni al IDE.

## Requisitos

- Python **≥ 3.10**
- (Opcional) Node.js **≥ 20** para `obsidian-mcp`
- (Opcional) [Obsidian](https://obsidian.md) para navegar el vault

## Instalación rápida (cualquier máquina)

```bash
git clone https://github.com/Raikadier/talaria.git
cd talaria
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
# con MarkItDown + Graphify:
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WithTools
```

**macOS / Linux:**

```bash
chmod +x scripts/install.sh scripts/talaria
./scripts/install.sh
# con herramientas de ingest:
./scripts/install.sh --with-tools
```

**Manual (cross-platform):**

```bash
pip install -e .
# opcional: pip install -e ".[tools]"
python bootstrap.py          # o: talaria boot
talaria doctor --json
talaria connect --client cursor --json
```

Si ejecutas fuera del clone, exporta:

```bash
# Windows PowerShell
$env:TALARIA_VAULT = "C:\ruta\a\talaria"

# bash
export TALARIA_VAULT="/path/to/talaria"
```

## Estructura del repo

```
talaria/
├── README.md · AGENTS.md · Home.md · PORTABILITY.md
├── pyproject.toml · bootstrap.py · LICENSE
├── src/talaria_cli/          ← paquete Python (CLI + MCP)
├── scripts/                  ← install.sh / install.ps1 / launcher
├── apps/docs-web/            ← sitio web (Next.js), separado del vault
├── memory/ · skills/ · _META/← vault Obsidian (verdad durable)
├── sandbox/                  ← demos / A/B (p.ej. barbería WA)
├── tools/ · _tools/          ← manifest + ingest helpers
├── _templates/ · tests/
└── .obsidian/ · .cursor/
```

El **vault** sigue en la raíz a propósito: Obsidian y los wiki-links no se rompen. El código instalable vive en `src/`.

## Uso mínimo

```bash
talaria describe --json      # contrato para cualquier agente
talaria connect --client cursor --json
talaria status
talaria axon search "marketing" --json
talaria forge list --json
talaria mcp                  # servidor MCP stdio
```

Constitución del piloto: [`AGENTS.md`](AGENTS.md) · mapa: [`_META/architecture.md`](_META/architecture.md) · [`_META/organism.md`](_META/organism.md).

## FORGE — agentes y delegación

Talaria es la **fábrica**; **tú** eres dueño del organigrama de agentes.

```bash
# Crear agente desde lenguaje natural
talaria forge build --brief "crea un agente que…" [--kind both] [--invokes a,b] --json

# Activar (hidrata skills + memory por defecto)
talaria forge run tech-lead --pack software-delivery --json

# Delegar parent → child
talaria forge invoke <parent> <child> [--brief "…"] --json
talaria forge graph --json

# Validar entregable (Gaxon = cites axon_skills)
talaria forge check --profile tech-lead --deliverable <path> --require-axon --json
```

Vertical **software-delivery**: ensemble + perfiles activos (`tech-lead`, `backend-developer`, `qa-engineer`, …). Auto-instruct al crear perfiles (`forge instruct`).

Docs: [`_META/forge/`](_META/forge/) · [`_META/forge/delegation.md`](_META/forge/delegation.md).

## AXON — packs e hidratación

**Curar ≠ borrar.** Un pack define qué entra al Act; el banco completo sigue en `skills/`.

```bash
talaria axon pack list --json
talaria axon pack show software-delivery --json
talaria memory retrieve "software delivery" --json
```

Packs semilla: `software-delivery`, `youtube-channel` → [`_META/axon/packs.md`](_META/axon/packs.md).

`forge run` / `forge invoke` inyectan **cuerpos** de skills (`skills_hydrated`) + hits de `memory/`. El entregable debe listar:

```yaml
axon_skills:
  - skills/…/….md
```

## MCP

Parity CLI ↔ tools `talaria_*` (incl. `talaria_forge_run`, `talaria_memory_retrieve`, `talaria_axon_pack_*`).  
Mapa: [`_META/mcp-parity.md`](_META/mcp-parity.md).

```bash
talaria connect --client cursor --apply --yes
```

## Eval / A/B (barbería)

Sandbox local FastAPI + SQLite + WA mock:

| Brazo | Path | Puerto |
|-------|------|--------|
| Baseline (sin Talaria) | `sandbox/ab-barbershop-booking/baseline` | 8010 |
| FORGE + hydrate | `sandbox/ab-barbershop-booking/forge` | 8011 |

Última corrida (rúbrica M1–M8): baseline **74** · FORGE v3 **96**.  
Informes: `memory/evals/2026-08-05-ab-barbershop-booking*.md`.

```bash
cd sandbox/ab-barbershop-booking/forge
pip install -r requirements.txt
uvicorn app.main:app --port 8011
pytest -q
```

Auth demo: `admin` / `barberia123` (ver `.env.example`).

## Regenerar el grafo AXON (opcional)

Las notas en `skills/` ya viajan con el repo. Para **reescanear** bancos locales de `SKILL.md`:

```bash
# variables opcionales (separadas por OS pathsep)
export TALARIA_SKILL_SOURCES="/path/hermes/skills:/path/other/skills"
python build_axon_graph.py
```

El informe se escribe en `_META/axon-build-report.md` (no pisa el README).

## Portabilidad

Ver [PORTABILITY.md](PORTABILITY.md): qué subir al git, qué queda local, cómo cablear MCP en otra máquina.

## Licencia

MIT — ver [LICENSE](LICENSE).
