---
tags: [moc, tools]
aliases: [herramientas, tools-index]
---

# Herramientas de ingestión

Formas estándar de meter contenido externo al segundo cerebro.

| Tool | Para | Doc |
|------|------|-----|
| [[markitdown]] | Documentos → Markdown | `tools/markitdown.md` |
| [[graphify]] | Proyectos/código → grafo | `tools/graphify.md` |
| [[mcp-obsidian]] | Agentes leen/escriben el vault | `_META/mcp-obsidian.md` |

## Bootstrap (portable)

```bash
pip install -e .
talaria boot
# o: python bootstrap.py
```

Instala lo que falte según `tools/manifest.json` + `tools/requirements.txt`.

## CLI

Ver [[cli]] — `talaria doctor|status|ingest|import`

## Helpers

```bash
talaria ingest doc <archivo|url>
talaria ingest project <ruta-proyecto>
# equivalentes:
python _tools/ingest_document.py <archivo|url>
python _tools/ingest_project.py <ruta>
```

Ver también [[PORTABILITY]] · [[cli-design]] · [[cli-architecture]].
