---
tags: [forge, ensemble, software]
aliases: [forge-ensemble-software, software-triad, triad-software]
forge_id: software-triad
forge_version: 1.0
status: active
laws: [I, II]
profiles: [sw-architect, sw-engineer, programmer]
---

# FORGE Ensemble — Software Triad

**Arquitecto → Ingeniero → Programador**

Objetivo: construir software con calidad de sistema que un solo modelo en un hilo continuo **no** mantiene (mezcla capas, salta tests, redefine scope a mitad).

## Secuencia canónica

```
[Brief usuario]
      │
      ▼
 sw-architect  ──ADR + boundaries──►  sw-engineer
                                          │
                                   task pack atómico
                                          │
                                          ▼
                                     programmer
                                          │
                                   reports + diffs
                                          │
                    ◄──── re-plan / escalate ────┘
                          (si boundaries cambian → architect)
```

## Contratos

| Etapa | Artefacto obligatorio | Receptor |
|-------|----------------------|----------|
| A→E | ADR + contracts | `sw-engineer` |
| E→P | Task pack (DoD por task) | `programmer` |
| P→E | Task report + verificación | `sw-engineer` |
| E→A | Change request (si boundaries) | `sw-architect` |

## DoD del conjunto (Ley I)

- [ ] ADR aceptado  
- [ ] Plan de ingeniería con tests  
- [ ] Tasks cerradas con verificación  
- [ ] Riesgos abiertos documentados  
- [ ] Memoria canónica actualizada (decisión + proyecto)  

## Superioridad (Ley II)

Sin triad: un chat genérico “arquitectura + código + tests” en un solo golpe → deuda invisible.  
Con triad: especialización + gates + handoffs → el sistema crece sin autodisolver límites.

## Activación

```text
FORGE ensemble=software-triad | laws=I+II | spine=on
start_role=sw-architect
```

Perfiles: [[forge-profile-sw-architect]] · [[forge-profile-sw-engineer]] · [[forge-profile-programmer]]
