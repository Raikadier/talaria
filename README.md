# SkillGraph — Segundo cerebro de skills

Vault Obsidian con **grafo interconectado** de skills indexadas desde Hermes y Skills de David.
Sincronizado vía OneDrive.

## Resumen

| Métrica | Valor |
|--------|------:|
| Skills únicas | 1463 |
| Archivos SKILL.md escaneados | 2776 |
| Dominios | 70 |
| Notas totales (aprox.) | 1545 |
| Aristas (wiki-links generados) | 32470 |
| Tamaño vault | 284.36 MB |

### Fuentes escaneadas

1. `C:\Users\david\AppData\Local\hermes\skills\` (banco Hermes)
2. `C:\Users\david\Skills\` (agensi-free, aiskillsbank, youtube-social-pack)

Los duplicados por nombre se indexan **una sola vez**; ambas rutas aparecen en el frontmatter `sources`.

## Cómo navegar el grafo

1. Abre esta carpeta como vault en Obsidian (**Open folder as vault**).
2. Usa **Graph View** para ver el mapa; filtra por `#youtube`, `#finance`, `#coding`, etc.
3. Entra por [[taxonomy]] o por un dominio (ej. hubs en `_META/domains/`).
4. Cada skill enlaza a: hub de dominio, peers del mismo dominio, skills con tags solapados, y ejes temáticos.

### Ejes temáticos

[[youtube]] · [[finance]] · [[coding]] · [[data]] · [[marketing]] · [[agent]] · [[design]] · [[writing]] · [[research]] · [[security]] · [[productivity]]

## Top dominios

| Dominio | Skills |
|---------|-------:|
| [[community]] | 592 |
| [[agensi]] | 512 |
| [[marketing]] | 83 |
| [[aiskillsbank]] | 70 |
| [[creative]] | 24 |
| [[development]] | 19 |
| [[productivity]] | 16 |
| [[youtube]] | 14 |
| [[agensi-pachca]] | 12 |
| [[research]] | 9 |
| [[software-development]] | 9 |
| [[media]] | 8 |
| [[enterprise]] | 6 |
| [[github]] | 6 |
| [[agensi-agent-operator-utility-pack]] | 5 |
| [[autonomous-ai-agents]] | 5 |
| [[apple]] | 4 |
| [[engineering]] | 4 |
| [[messaging]] | 4 |
| [[windows]] | 4 |
| [[automation]] | 3 |
| [[utility]] | 2 |
| [[templates]] | 2 |
| [[evaluation]] | 2 |
| [[inference]] | 2 |

## Regenerar el vault

```powershell
python "D:\OneDrive - unicesar.edu.co\Business Ideas\SkillGraph\build_axon_graph.py"
```

Solo **lee** los `SKILL.md` origen; no los modifica.

## Consulta vía MCP de Obsidian

Si tienes un servidor MCP tipo `mcp-obsidian` / `obsidian-mcp`:

1. Apunta `OBSIDIAN_VAULT_PATH` (o equivalente) a:
   `D:\OneDrive - unicesar.edu.co\Business Ideas\SkillGraph`
2. Reinicia Cursor / el servidor MCP.
3. Usa herramientas tipo `search`, `list_files`, `get_file_contents` sobre notas en `skills/` y `_META/`.

Si no hay MCP de Obsidian instalado, este vault sigue siendo plenamente usable abriéndolo en la app Obsidian (desktop). OneDrive mantiene el backup en la nube automáticamente.

## Estructura

```
SkillGraph/
  README.md
  build_axon_graph.py
  _META/
    taxonomy.md
    domains/<dominio>.md
    axes/<eje>.md
  skills/<dominio>/<skill>.md
```

---
Generado automáticamente · 2026-07-29 02:36 · 257.8s
