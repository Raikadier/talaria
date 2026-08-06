---
tags: [forge, corpus, methods]
forge_id: sw-architect
sources: [S1, S2, S3, S6]
---

# Métodos — Arquitecto de software

## 1. Atributos de calidad (QA)

Identificar QAs prioritarios (p. ej. modifiability, performance, security, availability) y usarlos como criterios de evaluación de opciones — S1.

## 2. ADR (Architecture Decision Record)

Plantilla mínima: contexto, decisión, alternativas, consecuencias — S2.  
En Talaria: Memorize en `memory/decisions/` o bajo el proyecto.

## 3. C4 (contexto → contenedores → componentes → código)

Usar L1/L2 para comunicar límites a humanos y a `sw-engineer`; no bajar a L4 salvo spike justificado — S3.

## 4. Module / dependency thinking

Un **grafo de módulos** muestra dependencias entre unidades de diseño (quién usa a quién). Sirve para detectar ciclos, ownership y blast radius. Si el concepto falta en el agente: learn loop → nota en `notes/` (no inventar).

## 5. ATAM-lite (riesgos)

Aunque ATAM completo sea pesado, aplicar la idea: escenarios de calidad → sensibilidades → riesgos → trade-offs — S1, S6.

## 6. Bounded contexts (cuando hay dominio complejo)

Separar modelos por contexto; evitar “un solo modelo para todo” — S4.
