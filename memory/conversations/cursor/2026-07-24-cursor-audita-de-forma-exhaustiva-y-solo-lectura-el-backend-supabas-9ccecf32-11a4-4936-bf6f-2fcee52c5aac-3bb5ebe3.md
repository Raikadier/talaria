---
date: 2026-07-24
type: conversation
source_agent: cursor
session_id: "9ccecf32-11a4-4936-bf6f-2fcee52c5aac"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\2149fb3f-8908-4916-a807-27d252ddd8da\\subagents\\9ccecf32-11a4-4936-bf6f-2fcee52c5aac.jsonl"
tags: [conversation, imported, cursor]
title: "Audita de forma exhaustiva y solo lectura el backend, Supabase, autenticación, autorizació"
---

# Audita de forma exhaustiva y solo lectura el backend, Supabase, autenticación, autorizació

**Fecha:** 2026-07-24  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `9ccecf32-11a4-4936-bf6f-2fcee52c5aac`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\2149fb3f-8908-4916-a807-27d252ddd8da\subagents\9ccecf32-11a4-4936-bf6f-2fcee52c5aac.jsonl`

## Mensajes

### Usuario

Audita de forma exhaustiva y solo lectura el backend, Supabase, autenticación, autorización y seguridad del repositorio D:/Github repos/togesc. Revisa migraciones/RLS, funciones, validación, secretos, exposición de datos, lógica de negocio, concurrencia, integridad, privacidad y límites de confianza. No hagas cambios ni operaciones remotas. Verifica en código y migraciones reales, no solo en docs/auditoria. Devuelve hallazgos por severidad con evidencia ruta y líneas exactas, escenario de impacto/explotación y mitigación concreta; señala controles sólidos ya presentes. Thoroughness: very thorough.

### Asistente

Iniciando auditoría de seguridad en solo lectura: exploraré migraciones Supabase, RLS, autenticación y código del repositorio.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Grep]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
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
[tool:Read]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

# Auditoría de seguridad — TOGESC (solo lectura)

**Alcance:** `D:/Github repos/togesc` — migraciones Supabase, Edge Functions, cliente Flutter (auth/sync/monetización), CI/scripts.  
**Método:** revisión de código y migraciones reales (no solo `docs/auditoria`).  
**Nota:** varios hallazgos documentados en `docs/auditoria/` ya están **corregidos** en código (merge por nota, idempotencia webhooks, fail-closed parcial en `ProRouteGuard`). Este informe refleja el estado **actual** del repo.

---

## Resumen ejecutivo

| Severidad | Cantidad | Tema principal |
|-----------|----------|----------------|
| **CRÍTICO** | 1 | Escalada de privilegios Pro vía RLS en `user_subscriptions` |
| **ALTO** | 3 | Vistas de métricas expuestas; lectura cruzada de analytics anónimos; monetización confiable solo en cliente |
| **MEDIO** | 6 | Trial repetible, spam analytics, pérdida concurrente en `save()`, cache local manipulable, webhooks sin validación de usuario, backup con PII |
| **BAJO** | 5 | Errores silenciados, email no exigido, TOCTOU idempotencia, IDs de proyecto en repo, comparación Bearer no constante |
| **INFORMATIVO** | — | Controles sólidos ya presentes (detalle al final) |

---

## CRÍTICO

### C-01 — Escalada de privilegios Pro: el cliente puede escribir `user_subscriptions`

**Evidencia (RLS permite INSERT/UPDATE al propio usuario):**

```25:38:D:/Github repos/togesc/supabase/migrations/20260615000000_user_subscriptions.sql
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

grant select, insert, update on public.user_subscriptions to authenticated;
```

**Evidencia (app escribe directamente desde cliente — trial manual):**

```121:137:D:/Github repos/togesc/TOGESC/togesc/lib/services/subscription_service.dart
  Future<void> startTrial() async {
    final repo = _repo;
    if (!SubscriptionConfig.isActive || repo == null) return;

    final trialEnds = DateTime.now().add(
      const Duration(days: SubscriptionConstants.trialDays),
    );

    await repo.upsert(
      SubscriptionStatus(
        plan: 'pro',
        status: 'trialing',
        source: 'manual',
        trialEndsAt: trialEnds,
        expiresAt: trialEnds,
      ),
    );
  }
```

**Evidencia (upsert REST desde repositorio):**

```32:41:D:/Github repos/togesc/TOGESC/togesc/lib/services/supabase_subscription_repository.dart
  Future<void> upsert(SubscriptionStatus status, {String? externalId}) async {
    await _client.from(userSubscriptionsTable).upsert({
      'user_id': _userId,
      'plan': status.plan,
      'status': status.status,
      'source': status.source,
      'external_id': ?externalId,
      'trial_ends_at': ?status.trialEndsAt?.toIso8601String(),
      'expires_at': ?status.expiresAt?.toIso8601String(),
    });
  }
```

**Escenario de explotación:**  
Usuario autenticado (JWT + anon key del bundle web) ejecuta:

```http
POST /rest/v1/user_subscriptions
Authorization: Bearer <JWT>
apikey=
Content-Type: application/json
Prefer: resolution=merge-duplicates

{"user_id":"<uuid_propio>","plan":"pro","status":"active","source":"manual","expires_at":"2099-12-31T00:00:00Z"}
```

O usa el botón de prueba en paywall (`paywall_screen.dart:90`). Resultado: **Pro + sync en n

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
