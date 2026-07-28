---
date: 2026-07-28
type: research
tags: [research, tools, skillgraph, free, local-first]
status: draft
---

# Investigación: herramientas gratis para expandir SkillGraph

**Fecha:** 2026-07-28  
**Contexto:** complementar [[markitdown]] y [[graphify]]  
**Canvas:** investigación visual en Cursor (`skillgraph-tools-research.canvas.tsx`)

## Criterios

1. Gratis / open source (ideal MIT/Apache)
2. Local-first (sin API key obligatoria)
3. CLI o MCP (usable por cualquier agente)
4. Portable con el vault (`bootstrap.py`)

## Ya tenemos

| Tool | Capa |
|------|------|
| MarkItDown | Documentos → MD |
| Graphify | Código/proyecto → grafo |
| obsidian-mcp | Agentes ↔ vault |

## Hallazgos por capa

### Documentos (más allá de MarkItDown)

| Tool | Por qué | Prioridad |
|------|---------|-----------|
| **Docling** (IBM) | Mejor en tablas, layout, papers | **P0** |
| **Marker / Surya** | Scans, OCR, fórmulas (más pesado) | P1 |
| **parse-anything** | Router markitdown/docling/mineru | P1 |

### Vault / recuperación

| Tool | Por qué | Prioridad |
|------|---------|-----------|
| **engraph** | Hybrid search 5-lane + MCP sobre Obsidian | **P0** |
| **korely-graphrag** | Grafo de entidades sobre MD + MCP | P1 |
| **claude-obsidian** | Wiki auto-organizada (Karpathy LLM Wiki) | P1 |
| Lumina / Obsilo | Plugins Obsidian potentes pero menos portables | P2 |

### Código (además de Graphify)

| Tool | Por qué | Prioridad |
|------|---------|-----------|
| **Nexus-MCP** | Search + code graph + memoria local vía MCP | **P0** |
| ast-grep | Búsqueda estructural determinista | P2 |

### Web / media

| Tool | Por qué | Prioridad |
|------|---------|-----------|
| **yt-dlp** | Video/audio/subs (YouTube+) | **P0** |
| **faster-whisper / whisper.cpp** | Transcripción local | **P0** |
| **Crawl4AI** | Web JS → Markdown (alt. gratis a Firecrawl) | **P0** |
| SearXNG | Meta-search self-hosted | P2 |

### Memoria de agente (paralela al vault)

| Tool | Por qué | Prioridad |
|------|---------|-----------|
| **PMB** | Memoria SQLite MCP, sin API key | P1 |
| Knowledge Keeper MCP | 32 tools, MD local | P1 |
| `@modelcontextprotocol/server-memory` | KG JSONL simple | P2 |
| **Ollama** | LLM local para resumir offline | P1 |

## Roadmap recomendado

### Oleada 1 (máximo ROI)
`docling` · `yt-dlp` · `faster-whisper` · `crawl4ai` · `engraph` **o** `nexus-mcp`

### Oleada 2
`parse-anything` · `korely-graphrag` · `ollama` · `pmb`

### Oleada 3
Marker/Surya · SearXNG · metodología claude-obsidian · ast-grep

## Próximo paso práctico

Añadir Oleada 1 a `tools/manifest.json` + `bootstrap.py` cuando David confirme prioridades.

## Enlaces

- [[tools-index]] · [[PORTABILITY]] · [[markitdown]] · [[graphify]] · [[mcp-obsidian]]
- [[Home]] · [[SkillGraph]]
