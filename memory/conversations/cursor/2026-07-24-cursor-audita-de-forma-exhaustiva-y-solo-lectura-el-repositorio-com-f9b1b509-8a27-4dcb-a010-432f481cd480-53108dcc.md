---
date: 2026-07-24
type: conversation
source_agent: cursor
session_id: "f9b1b509-8a27-4dcb-a010-432f481cd480"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\f9b1b509-8a27-4dcb-a010-432f481cd480\\f9b1b509-8a27-4dcb-a010-432f481cd480.jsonl"
tags: [conversation, imported, cursor]
title: "Audita de forma exhaustiva y solo lectura el repositorio completo en D:/Github repos/toges"
---

# Audita de forma exhaustiva y solo lectura el repositorio completo en D:/Github repos/toges

**Fecha:** 2026-07-24  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `f9b1b509-8a27-4dcb-a010-432f481cd480`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\f9b1b509-8a27-4dcb-a010-432f481cd480\f9b1b509-8a27-4dcb-a010-432f481cd480.jsonl`

## Mensajes

### Usuario

Audita de forma exhaustiva y solo lectura el repositorio completo en D:/Github repos/togesc. Enfócate en arquitectura, estructura, mantenibilidad, deuda técnica, gestión de estado, dependencias, configuración, errores lógicos y consistencia general. No edites archivos. Verifica los hallazgos directamente en el código; no te limites a los documentos existentes de docs/auditoria. Devuelve: (1) resumen de la arquitectura real, (2) hallazgos priorizados como crítico/alto/medio/bajo, (3) para cada hallazgo evidencia con ruta y líneas exactas, impacto y recomendación concreta, (4) aspectos bien resueltos para evitar falsos positivos. Thoroughness: very thorough.

### Asistente

Voy a auditar el repositorio completo en solo lectura: primero mapeo la estructura y la arquitectura real del código.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Read]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Grep]
[tool:Glob]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Shell]

### Asistente

[tool:Shell]
[tool:Shell]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Await]
[tool:Await]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Await]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Await]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Shell]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

# Auditoría exhaustiva — TOGESC (`D:/Github repos/togesc`)

Verificación directa en código ejecutada: `dart analyze lib` → **0 issues**; `flutter test` → **309 passed, 1 skipped** (~4 min).

---

## 1. Resumen de la arquitectura real

El repositorio es un **monorepo** cuyo producto activo es una app **Flutter** en `TOGESC/togesc/`, con backend **Supabase** ya integrado (más allá del MVP “sin backend” descrito en documentación antigua).

```
┌─────────────────────────────────────────────────────────────┐
│  UI: screens/ + widgets/  (español, Material 3, go_router) │
├─────────────────────────────────────────────────────────────┤
│  Estado: Riverpod providers/ (19 providers)                   │
│    gameSession, speedSession, srsSystem, subscription, sync │
├─────────────────────────────────────────────────────────────┤
│  Dominio: services/                                         │
│    SRSSystem, AudioGenerator, AudioPlayerService, NoteParser│
│    SubscriptionService, SyncCoordinator, AnalyticsService │
├─────────────────────────────────────────────────────────────┤
│  Persistencia: ProgressRepository (interface)               │
│    SharedPreferencesProgressRepository (local)              │
│    SupabaseProgressRepository (remoto, RLS)                 │
│    HybridProgressRepository (local-first + merge + pending) │
├─────────────────────────────────────────────────────────────┤
│  Backend: supabase/                                         │
│    migrations (user_progress, user_subscriptions, analytics)│
│    Edge Functions: stripe-webhook, revenuecat-webhook       │
├─────────────────────────────────────────────────────────────┤
│  CI/CD: .github/workflows (ci, deploy-web, build-android)   │
└─────────────────────────────────────────────────────────────┘
```

**Flujo de juego:** `GameSessionNotifier` → `SRSSystem.selectNotes()` → `AudioGenerator`/`AudioPlayerService` → respuesta → `updateAfterResponse()` → `saveProgress()` → flush sync opcional.

**Bootstrap (`main.dart`):** Sentry opcional → Supabase opcional (`--dart-define`) → `SharedPreferences` → `GoRouter` con override en `ProviderScope` → listeners globales (startup, auth/sync, CSAT, checkout).

**Dependencias clave (`pubspec.yaml`):** `flutter_riverpod`, `go_router`, `flutter_soloud`, `shared_preferences`, `supabase_flutter`, `purchases_flutter`, `sentry_flutter`, `record`, `google_fonts`.

**Tests:** pirámide real con 47 archivos en `test/{unit,integration,widget,e2e}/` — buena cobertura de SRS, sync multi-dispositivo, monetización y navegación.

---

## 2. Hallazgos priorizados

### CRÍTICO

#### C1 — Escalada de privilegios: el cliente puede auto-concederse Pro en Supabase

**Evidencia:**

RLS permite `INSERT`/`UPDATE` de la fila propia sin restringir `plan`/`status`:

```18:36:D:/Github repos/togesc/supabase/migrations/20260615000000_user_subscriptions.sql
create policy "user_subscriptions_insert_own"
  on public.user_subscriptions
  for insert
  to authenticated
  with check ((select auth.uid()) = user_id);

create policy "user_subscriptions_update_own"
  on public.user_subscriptions
  for update
  to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
```

El cliente escribe directamente `plan: 'pro'`:

```121:137:D:/Github repos/togesc/TOGESC/togesc/lib/services/subscription_service.dart
  Future<void> startTrial() async {
    final repo = _repo;
    if (!SubscriptionConfig.isActive || repo == null) return;
    // ...
   

_[truncado]_

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

Corrección del resultado: `flutter analyze` finalizó con **3 avisos informativos en tests** (una API obsoleta y dos underscores innecesarios), sin errores de producción. `flutter test` sí pasó: **309 tests, 1 omitido**. No se requieren acciones adicionales para esta auditoría de solo lectura.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
