# Talaria

**Traje cognitivo** para cualquier agente de IA: memoria durable (vault Obsidian), grafo de skills (AXON), perfiles elite (FORGE) y protocolo SPINE, expuestos como **CLI + MCP**.

> Antes: SkillGraph. Ahora: **Talaria** — mismo organismo, API instalable en cualquier PC.

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

Constitución del piloto: `AGENTS.md` · mapa: `_META/architecture.md` · `_META/organism.md`.

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
