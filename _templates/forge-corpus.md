---
tags: [template, forge, corpus]
aliases: [forge-corpus-template]
---

# Corpus FORGE — {{title}} (`{{id}}`)

Copiar a `memory/research/forge/{{id}}/` y completar. Gates C1–C5: [[forge-builder]].

## README.md (índice)

```markdown
---
tags: [forge, corpus]
forge_id: {{id}}
corpus_version: 0.1
status: draft
gates: {C1: false, C2: false, C3: false, C4: false, C5: false}
---

# Corpus — {{title}}

## Estado gates
| Gate | Pass |
|------|------|
| C1 Scope | |
| C2 Sources (≥5) | |
| C3 Trace | |
| C4 Doctrine | |
| C5 Limits | |

## Mapa
- [[00-doctrine]] · [[01-role-purpose]] · [[02-methods]] · [[03-antipatterns]] · [[04-deliverables]] · [[05-sources]]
- Learn notes: `notes/`

## Perfil ejecutable
`_META/forge/profiles/{{id}}.md`
```

## 00-doctrine.md (obligatorio)

```markdown
# Doctrina cognitiva — {{title}}

## Cómo piensa
(marcos mentales, preguntas que se hace primero)

## Cómo razona
(trade-offs, evidencia, criterios de decisión)

## Cómo resuelve problemas
(pasos típicos; qué recupera antes de decidir)

## Qué nunca hace un excelente {{title}}
(anti-patrones de juicio)

## Amplificadores vs IA genérica
1. …
2. …
3. …
```

## 05-sources.md (obligatorio)

```markdown
# Fuentes — {{id}}

| ID | Fuente | Tipo | Grado | URL/ref | Usado en |
|----|--------|------|-------|---------|----------|
| S1 | | libro/norma/paper/doc | primaria/sec. | | doctrine/methods |
```
