---
date: 2026-07-24
type: conversation
source_agent: cursor
session_id: "a5627b60-2ef5-4a87-b89f-33b86d7b737c"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\a5627b60-2ef5-4a87-b89f-33b86d7b737c\\a5627b60-2ef5-4a87-b89f-33b86d7b737c.jsonl"
tags: [conversation, imported, cursor]
title: "Audita de forma exhaustiva y solo lectura el repositorio D:/Github repos/togesc en pruebas"
---

# Audita de forma exhaustiva y solo lectura el repositorio D:/Github repos/togesc en pruebas

**Fecha:** 2026-07-24  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `a5627b60-2ef5-4a87-b89f-33b86d7b737c`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\a5627b60-2ef5-4a87-b89f-33b86d7b737c\a5627b60-2ef5-4a87-b89f-33b86d7b737c.jsonl`

## Mensajes

### Usuario

Audita de forma exhaustiva y solo lectura el repositorio D:/Github repos/togesc en pruebas, CI/CD, build, lint/typecheck, observabilidad, manejo de errores, performance, SEO/PWA y preparación para producción. Puedes inspeccionar scripts y configuración, pero no edites nada. Distingue ausencia real de algo frente a suposiciones. Devuelve hallazgos priorizados con evidencia ruta:líneas, impacto y recomendación, además de fortalezas verificadas. Thoroughness: very thorough.

### Asistente

Auditoría exhaustiva en solo lectura: empiezo mapeando la estructura del repo y localizando configuración de pruebas, CI/CD, build y calidad.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Grep]
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

### Asistente

[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Glob]
[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Shell]
[tool:Grep]

### Asistente

[tool:Shell]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Await]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Await]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Shell]
[tool:Grep]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Await]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Await]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

# Auditoría TOGESC — Calidad, CI/CD y preparación para producción

**Alcance:** repositorio `D:/Github repos/togesc` (Flutter en `TOGESC/togesc/`, Supabase, GitHub Actions, Vercel).  
**Modo:** solo lectura.  
**Verificación local ejecutada:** `flutter test` → **309 passed, 1 skipped** (~6,5 min); `flutter analyze` → **3 issues (info)**, exit code **1**.

---

## Resumen ejecutivo

El proyecto tiene una **base sólida de pruebas automatizadas** (pirámide real con ~47 archivos) y **CI mínimo funcional** (`analyze` + `test`). La **observabilidad está parcialmente cableada** (Sentry opcional, analytics a Supabase, uptime horario, backup semanal). Los gaps más relevantes para producción son: **deploy web sin depender de CI**, **sin métricas de cobertura**, **E2E real inexistente** (solo smoke widget), **errores silenciados sin telemetría**, **SEO/PWA incompletos** y **dos rutas de build web** (GitHub prebuilt vs `vercel.json`) con configuraciones distintas.

---

## Fortalezas verificadas (con evidencia)

| Área | Evidencia | Notas |
|------|-----------|-------|
| **Suite de tests amplia** | 47 archivos en `TOGESC/togesc/test/`; ejecución local: 309 passed | Cubre SRS, audio, sync, suscripción, widgets core |
| **Pirámide de tests** | `test/unit/` (~29), `widget/` (~10), `integration/` (4), `e2e/` (1) | Integración incluye `sync_multi_device_test`, `game_srs_integration_test` |
| **CI en push/PR a main** | `.github/workflows/ci.yml:27-31` | `flutter analyze` + `flutter test` |
| **Deploy web automatizado** | `.github/workflows/deploy-web.yml:4-55,74-75` | Build con `--dart-define` (Supabase, Stripe, Sentry, analytics) + Vercel prebuilt |
| **Uptime producción** | `.github/workflows/uptime-check.yml:4-18` | Ping horario a `https://togesc.vercel.app` (HTTP 200) |
| **Backup Supabase** | `.github/workflows/supabase-backup.yml:4-32` | Dump semanal + artifact 30 días |
| **Dependabot** | `.github/dependabot.yml:3-13` | `pub` + `github-actions`, semanal |
| **Lint base Flutter** | `TOGESC/togesc/analysis_options.yaml:10-11` | `flutter_lints` incluido |
| **Script validación pre-release** | `scripts/validate-production.ps1:9-15,19-34` | analyze + test + checks de artefactos |
| **Checklist QA manual** | `docs/qa_checklist.md:1-12,95-99` | ~45–60 min, criterios de salida |
| **Guía release móvil** | `docs/mobile_release.md:1-77` | Android AAB + iOS manual |
| **Sentry integrado (opcional)** | `TOGESC/togesc/lib/main.dart:21-30`, `lib/config/observability_config.dart:3-9` | Init vía `SENTRY_DSN` |
| **Analytics producto** | `TOGESC/togesc/lib/services/analytics_service.dart:29-40` | Insert a `analytics_events` en Supabase |
| **Webhooks con firma** | `supabase/functions/stripe-webhook/index.ts:91-103` | `stripe.webhooks.constructEvent` |
| **Idempotencia webhooks** | `supabase/functions/_shared/webhook_idempotency.ts` (referenciado en stripe-webhook:5-7) | Dedup de eventos |
| **SEO básico app web** | `TOGESC/togesc/web/index.html:19-45` | meta description, OG, Twitter, manifest |
| **Landing SEO** | `TOGESC/togesc/web/landing.html:1-18,36-46` | `lang="es"`, OG, contenido indexable |
| **PWA manifest** | `TOGESC/togesc/web/manifest.json:1-34` | standalone, iconos 192/512 + maskable |
| **Android release preparado** | `TOGESC/togesc/android/app/build.gradle.kts:31-61`, `proguard-rules.pro:1-23` | Firma condicional + reglas R8 |
| **Accesibilidad parcial piano** | `TOGESC/togesc/lib/widgets/piano_keyboard.dart:182-184,231-233` | `Semantics` en teclas y

_[truncado]_

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

La suite completa finalizó correctamente: **309 pruebas aprobadas y 1 omitida**, sin fallos. No se requieren acciones adicionales.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
