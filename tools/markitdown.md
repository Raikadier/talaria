---
tags: [tool, markitdown, documents, ingest]
aliases: [markitdown]
---

# Tool: MarkItDown

**Rol:** consumir documentos (PDF, Office, HTML, imágenes, URLs…) y convertirlos a Markdown listo para el vault / LLMs.

**Upstream:** [microsoft/markitdown](https://github.com/microsoft/markitdown)  
**Instalar:** `python bootstrap.py` o `pip install 'markitdown[all]'`

## Cuándo usar

- Metes un PDF/DOCX/PPTX/XLSX al segundo cerebro
- Quieres que un agente lea un documento sin parsers ad-hoc
- Preparas material para notes en `memory/` o `skills/`

## Uso rápido

```bash
# Desde la raíz del vault
python bootstrap.py --check-only

markitdown informe.pdf -o memory/inbox/converted/informe.md

# O vía helper portable
python _tools/ingest_document.py "C:\path\archivo.pdf"
```

## Formatos típicos

PDF · DOCX · PPTX · XLSX · HTML · imágenes · CSV · JSON · ZIP · URLs

## Salida en este vault

| Destino | Uso |
|---------|-----|
| `memory/inbox/converted/` | Markdown crudo convertido |
| `memory/inbox/` | Captura para clasificar después |

## Relación con Graphify

MarkItDown = **un documento → Markdown**.  
Graphify = **carpeta/proyecto → grafo** (código + docs). Pueden encadenarse: convertir docs y luego `/graphify` el directorio.
