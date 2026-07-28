---
tags: [tool, graphify, code, graph, ingest]
aliases: [graphify]
---

# Tool: Graphify

**Rol:** consumir proyectos de programación (y docs asociados) como **grafo de conocimiento consultable**, en lugar de leer archivo por archivo.

**Upstream:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)  
**PyPI:** `graphifyy` (el CLI se llama `graphify`)  
**Instalar:** `python bootstrap.py` o `pip install 'graphifyy[pdf,office,mcp]'`

## Cuándo usar

- Onboarding a un repo desconocido
- Preguntas del tipo “qué conecta X con Y”
- Mapear arquitectura antes de refactorizar
- Indexar un proyecto dentro del segundo cerebro

## Uso rápido

```bash
python bootstrap.py --check-only

# Extracción local de código (AST, sin API key)
graphify update "D:\Github repos\mi-proyecto" --force

# Helper portable → guarda salida bajo memory/graphs/
python _tools/ingest_project.py "D:\Github repos\mi-proyecto"

# Instalar skill en Cursor / Hermes
graphify cursor install
graphify install --platform hermes
```

## Salidas típicas

Dentro del proyecto: `graphify-out/graph.json`, `GRAPH_REPORT.md`, `graph.html`  
En el vault (vía helper): `memory/graphs/<nombre-proyecto>/`

## MCP (opcional)

```bash
python -m graphify.serve graphify-out/graph.json
```

Expone queries al grafo para el agente.

## Relación con MarkItDown

Para PDFs/Office sueltos → MarkItDown.  
Para repos/código (+ docs del repo) → Graphify.  
Para corpus mixto: convierte docs con MarkItDown a `.md` y luego Graphify el directorio.
