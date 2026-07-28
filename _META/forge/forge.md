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
**Naturaleza:** **órgano** del organismo [[organism|SkillGraph]] — no es un proyecto aparte.  
**Hogar:** módulo SPINE dentro del mismo vault · usable por cualquier piloto

> FORGE **fabrica perfiles** (roles operativos) que un agente se pone como módulo del traje. Trabaja **con** la memoria (`memory/`) y la skill web (`skills/`), no las sustituye. No sustituye al modelo: lo **especializa, disciplina y verifica** para superar lo que un modelo potente hace “de corrido”.

## Las 2 leyes obligatorias (no negociables)

Todo perfil FORGE —y todo perfil que el builder produzca— **falla el build** si no cumple ambas:

| Ley | Nombre corto | Exigencia |
|-----|--------------|-----------|
| **I** | **Efectividad total** | El perfil define misión, anti-misión, gates de calidad y DoD verificable. Sin “buenas intenciones”: o el entregable pasa los gates o el trabajo no se declara hecho. |
| **II** | **Superior a modelo potente** | El perfil debe demostrar *por diseño* por qué supera a un frontier model en un solo hilo continuo: especialización, evidencia, herramientas, handoffs y verificación. Si un chat genérico lo iguala sin el perfil, el perfil está mal construido. |

Detalle: [[forge-two-laws]] · Builder: [[forge-builder]] · Schema: [[forge-schema]] · Catálogo: [[forge-catalog]] · Ensembles: [[forge-ensembles]]

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
FORGE profile=<id> | laws=I+II | vault=SkillGraph | spine=on
```

## Inventario semilla (v1)

| ID | Perfil | Especialidad |
|----|--------|--------------|
| `researcher` | [[forge-profile-researcher]] | Investigación profesional documentada |
| `social-advisor` | [[forge-profile-social-advisor]] | Crecimiento de redes con decisiones defendibles |
| `sw-architect` | [[forge-profile-sw-architect]] | Arquitectura de software |
| `sw-engineer` | [[forge-profile-sw-engineer]] | Ingeniería de software (sistema) |
| `programmer` | [[forge-profile-programmer]] | Implementación de código de alto calibre |

Ensemble canónico de software: **Architect → Engineer → Programmer** → [[forge-ensemble-software]]

## Relación con skills

Los perfiles **enrutan** a skills del grafo (`skills/`, ejes, dominios). Un perfil no copia 1463 skills: declara **qué tipos** recupera y cómo los usa bajo Ley I/II.

## Versionado

- `version` en frontmatter del perfil  
- Cambios de leyes o schema → bump mayor + nota en `memory/decisions/`  
- Perfiles nuevos solo vía [[forge-builder]] (checklist completa)

## Referencias

- [[spine-framework]] · [[AGENTS]] · [[agent-protocol]] · [[pilots]]
