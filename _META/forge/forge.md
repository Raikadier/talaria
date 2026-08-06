---
tags: [meta, forge, spine, profiles, framework, organ]
aliases: [FORGE, forge-framework, profile-builder]
version: 1.0
status: active
pipeline: spine
---

# FORGE — Framework for Operational Role Generation & Excellence

**Nombre técnico:** *Framework for Operational Role Generation & Excellence*  
**Nombre de uso:** **FORGE** (acrónimo)  
**Naturaleza:** **órgano** del organismo [[organism|Talaria]] — no es un proyecto aparte.  
**Hogar:** módulo SPINE dentro del mismo vault · usable por cualquier piloto

> FORGE **fabrica perfiles** (roles operativos) que un agente se pone como módulo del traje. Trabaja **con** la memoria (`memory/`) y la skill web (`skills/`), no las sustituye. No sustituye al modelo: lo **especializa, disciplina y verifica** para superar lo que un modelo potente hace “de corrido”.

**Builder 2.0:** primero forma el **corpus del oficio** (doctrina verificada), luego talla el perfil ejecutable, y en runtime el perfil **aprende al vault** con learn loop + pensamiento crítico. Detalle: [[forge-builder]] · [[forge-corpus]]

**User-owned:** Tú creas tus agentes (`forge build`). El grafo de delegación es tuyo ([[forge-delegation]]). Los perfiles listados abajo son **semilla/ejemplo**, no tu organigrama.

## Las 2 leyes obligatorias (no negociables)

Todo perfil FORGE —y todo perfil que el builder produzca— **falla el build** si no cumple ambas:

| Ley | Nombre corto | Exigencia |
|-----|--------------|-----------|
| **I** | **Efectividad total** | El perfil define misión, anti-misión, gates de calidad y DoD verificable. Sin “buenas intenciones”: o el entregable pasa los gates o el trabajo no se declara hecho. |
| **II** | **Superior a modelo potente** | El perfil debe demostrar *por diseño* por qué supera a un frontier model en un solo hilo continuo: especialización, evidencia, herramientas, handoffs y verificación. Si un chat genérico lo iguala sin el perfil, el perfil está mal construido. |

Detalle: [[forge-two-laws]] · Builder: [[forge-builder]] · Schema: [[forge-schema]] · Catálogo: [[forge-catalog]] · Ensembles: [[forge-ensembles]] · Delegación: [[forge-delegation]]

## Por qué existe

Un modelo potente es un generalista brillante. Un **perfil FORGE** es un especialista con:

1. Método fijo (cómo piensa y en qué orden)  
2. Evidencia obligatoria (qué debe citar/probar)  
3. Gates (qué debe pasar antes de entregar)  
4. Handoffs (cómo trabaja con otros perfiles)  
5. Plantillas de salida (forma del resultado)

Eso es lo que un solo modelo “improvisando” no sostiene de forma fiable en tareas largas o multi-especialidad.

## Dónde vive en SPINE

```
ORIENT  → elegir perfil(es) FORGE según la tarea
RETRIEVE → skills + notas del vault alineadas al perfil
ACT     → ejecutar el playbook del perfil (o ensemble)
MEMORIZE → guardar evidencia / decisión / entregable canónico
NOTIFY  → actualizar proyecto + estado del ensemble
```

FORGE **no** es otra memoria canónica. Es un **protocolo de rol** sobre la verdad del vault.

## Arranque rápido (cualquier agente)

1. Leer este archivo + [[forge-two-laws]]  
2. Elegir perfil en [[forge-catalog]] **o** construir uno con [[forge-builder]]  
3. Activar: declarar `forge_profile: <id>` al inicio de la tarea  
4. Ejecutar el playbook; no saltar gates  
5. Si la tarea es multi-especialidad → [[forge-ensembles]]  

```text
Activación mínima:
FORGE profile=<id> | laws=I+II | vault=Talaria | spine=on
```

## Inventario semilla (v2 — Builder 2.0)

| ID | Perfil | Especialidad | Eval A/B |
|----|--------|--------------|----------|
| `researcher` | [[forge-profile-researcher]] | Investigación documentada | `research-brief-v2` |
| `social-advisor` | [[forge-profile-social-advisor]] | Crecimiento defendible | `growth-counsel-v2` |
| `sw-architect` | [[forge-profile-sw-architect]] | Arquitectura de software | `adr-boundaries-v2` |
| `sw-engineer` | [[forge-profile-sw-engineer]] | Ingeniería de software | `engineering-plan-v2` |
| `programmer` | [[forge-profile-programmer]] | Implementación de alto calibre | `atomic-impl-v2` |

Ensemble canónico: **Architect → Engineer → Programmer** → [[forge-ensemble-software]] (todos v2)

## Relación con skills

Los perfiles **enrutan** a skills del grafo (`skills/`, ejes, dominios). Un perfil no copia 1463 skills: declara **qué tipos** recupera y cómo los usa bajo Ley I/II.

## Versionado

- `version` / `forge_version` en frontmatter del perfil  
- Cambios de leyes o schema → bump mayor + nota en `memory/decisions/`  
- Perfiles nuevos solo vía [[forge-builder]] (checklist completa)  
- **v1** = contrato (DoD/gates). **v2** = contrato + corpus + learn loop + crítica  
- Perfiles v1 siguen válidos; elite v2 requiere Fase A (corpus C1–C5)

## Referencias

- [[spine-framework]] · [[AGENTS]] · [[agent-protocol]] · [[pilots]] · [[forge-corpus]]
