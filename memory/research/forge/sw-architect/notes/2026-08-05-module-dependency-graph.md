---
tags: [forge, corpus, learn-note]
forge_id: sw-architect
date: 2026-08-05
status: seed
---

# Note — Module dependency graph (seed)

**Qué es:** representación de módulos/componentes y sus dependencias (quién importa/llama a quién).

**Para qué sirve al arquitecto:** detectar ciclos, ownership, blast radius de cambios, violaciones de límites.

**Cómo hacerlo bien (mínimo):**
1. Elegir granularidad (paquete, servicio, bounded context).  
2. Extraer dependencias del repo (herramienta/graphify) o modelar L2 C4.  
3. Marcar dependencias prohibidas según ADR.  
4. Memorize hallazgos en proyecto + link desde ADR.

**Fuentes:** S3 (C4) · S1 (structures & QA modifiability) · tooling Graphify en Talaria.

Si en una tarea real se profundiza, ampliar esta nota (no duplicar: bump fecha y secciones).
