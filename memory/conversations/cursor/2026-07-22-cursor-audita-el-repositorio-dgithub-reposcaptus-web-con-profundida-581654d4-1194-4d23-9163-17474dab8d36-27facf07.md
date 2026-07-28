---
date: 2026-07-22
type: conversation
source_agent: cursor
session_id: "581654d4-1194-4d23-9163-17474dab8d36"
project: "empty-window"
source_path: "C:\\Users\\david\\.cursor\\projects\\empty-window\\agent-transcripts\\581654d4-1194-4d23-9163-17474dab8d36\\581654d4-1194-4d23-9163-17474dab8d36.jsonl"
tags: [conversation, imported, cursor]
title: "Audita el repositorio d:\\Github repos\\captus-web con profundidad muy exhaustiva. No edites"
---

# Audita el repositorio d:\Github repos\captus-web con profundidad muy exhaustiva. No edites

**Fecha:** 2026-07-22  
**Agente:** cursor  
**Proyecto/contexto:** empty-window  
**Sesión:** `581654d4-1194-4d23-9163-17474dab8d36`  
**Origen:** `C:\Users\david\.cursor\projects\empty-window\agent-transcripts\581654d4-1194-4d23-9163-17474dab8d36\581654d4-1194-4d23-9163-17474dab8d36.jsonl`

## Mensajes

### Usuario

Audita el repositorio d:\Github repos\captus-web con profundidad muy exhaustiva. No edites nada. Revisa estado git, arquitectura, configuración, integración real con backend, auth, seguridad cliente, variables de entorno, errores manifiestos, TODO/FIXME, calidad UX accesibilidad, dependencias y tests/build/lint. Ejecuta verificaciones no destructivas razonables. Devuelve hallazgos priorizados por severidad con evidencia exacta (archivo y línea cuando sea posible), separando fallos confirmados de riesgos, e indica verificaciones realizadas.

### Asistente

Auditando captus-web en profundidad: explorando el repositorio y ejecutando verificaciones no destructivas.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Shell]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Shell]
[tool:Read]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:UpdateCurrentStep]
[tool:Grep]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Shell]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Shell]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Shell]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Shell]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Shell]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Glob]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Shell]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Shell]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:UpdateCurrentStep]

### Asistente

# Auditoría exhaustiva — `d:\Github repos\captus-web`

Auditoría **solo lectura** del frontend Captus (Vite + React 18, Supabase Auth, Axios → `/api`). Sin cambios en el repositorio.

---

## Verificaciones realizadas

| Verificación | Resultado |
|---|---|
| `git status`, `git log -5`, ramas | OK — `main` alineada con `origin/main`; untracked: `captures/`, `documento de software ii/` |
| `.env` en git | OK — ignorado por `.gitignore:4`; **no** hay `.env.example` en repo |
| Nombres de variables en `.env` local | `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_API_BASE_URL`, `VITE_API_URL`, `VITE_CLARITY_PROJECT_ID`, `VITE_TELEGRAM_BOT_NAME` |
| `npm run lint` | **FALLA** — 4 errores, 4 warnings |
| `npm run test` (vitest) | **FALLA parcial confirmada** — al menos 4 tests en `TaskForm.test.jsx`; suite completa muy lenta (>8 min sin resumen final en este entorno) |
| `npm run build` | **No completó** en ~7+ min (quedó en fase `transforming...`) |
| `npm audit --audit-level=moderate` | **Vulnerabilidades reportadas** en axios, dompurify, vite, esbuild, undici, etc. |
| Exploración estática | Auth, rutas, servicios API, mocks, a11y, deps, CI |
| `.github/workflows` | **No existe** CI en el repo |

---

## Arquitectura (resumen)

- **Entrada:** `src/main.jsx` → `App.jsx` con `QueryClientProvider`, `AuthProvider`, rutas lazy-loaded.
- **Auth:** Supabase (`src/shared/api/supabase.js`) + JWT en Axios (`src/shared/api/client.js`).
- **Backend:** `VITE_API_BASE_URL` o proxy dev `/api` → `http://localhost:4000` (`vite.config.js:24-31`).
- **Capas:** `features/*` (UI), `hooks/*`, `services/*`, `shared/api/*`, UI Radix en `src/ui/`.
- **Despliegue:** `vercel.json` solo SPA rewrite; **sin proxy API** en producción (depende de `VITE_API_BASE_URL` en build).

---

## Hallazgos priorizados

### Crítico (confirmado o alto impacto en producción)

1. **Bypass de autenticación en producción si se configura mal**  
   `ProtectedRoute` deja pasar todo si `VITE_BYPASS_AUTH === 'true'` en producción.  
   Evidencia: `src/App.jsx:69-70`

2. **Código de telemetría/debug hacia localhost en chatbot (producción)**  
   Tres `fetch` a `http://127.0.0.1:7697/ingest/...` con metadatos de sesión/errores API.  
   Evidencia: `src/features/chatbot/ChatBotPage.jsx:41-42`, `:46-47`, `:130-131`  
   Riesgo: intentos de red inútiles en usuarios reales; fuga de contexto de errores si hubiera listener local; código de agente olvidado.

3. **Autorización solo en cliente (admin/teacher)**  
   `AdminRoute` / `TeacherRoute` leen `user_metadata` / `app_metadata` sin validación server-side visible en el front.  
   Evidencia: `src/App.jsx:75-86`  
   **Riesgo confirmado en el front:** escalada si el backend confía en el mismo metadata que el usuario puede influir en registro.

4. **Registro self-service como profesor**  
   El formulario envía `role: 'teacher'` en `signUp` options.  
   Evidencia: `src/features/auth/components/LoginForm.jsx:128-130`, `src/context/AuthContext.jsx:131-140`  
   **Fallo confirmado en UX/registro;** severidad de seguridad depende de Supabase triggers / `/users/sync` (no auditado aquí el backend).

5. **Datos mock mezclados con datos reales en flujos docente/estudiante**  
   - Entregas mock siempre visibles: `TeacherReviewsPage.jsx:33-36`, `84-96`  
   - Curso mock si falla API: `StudentCourseDetailPage.jsx:66-99`, `208`, `220`  
   - Detalle curso docente: `TeacherCourseDetailPage.jsx:33-96`  
   **Confirmado:** usuarios ven contenido ficticio ju

_[truncado]_

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

Sin novedades: estos resultados ya quedaron incorporados en la auditoría anterior. No se requieren acciones adicionales.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

Actualización: `npm run build` **sí completó correctamente** (`exit_code 0`) en 13m 20s. Generó `dist/`, con advertencias por chunks superiores a 600 kB; no requiere seguimiento inmediato.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

Actualización de tests: **86 pruebas pasaron**, pero Vitest terminó con código 1 por **10 errores de workers agotando el tiempo**, no por aserciones fallidas en esta ejecución. Esto apunta a un problema de recursos/configuración del pool.

**Evaluating test results**

I’m noticing that there were 4 failures before the first test command, but this separate run shows 86 passed and 10 worker errors. That’s a considerable difference! I think it might be best to keep things brief and concise for a follow-up. I probably won't need to do that since an audit will likely cover everything needed. I’ll add a note to correct or clarify anything relevant.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

**Evaluating final output success**

I need to inspect the final output, as its success might be surprising due to the use of a semicolon. It's interesting how the structure can influence the results, even when there are errors involved. I wonder if I can replicate this success in future outputs. It’s kind of exciting and perplexing at the same time! I want to ensure that I get it right every time.
[tool:ReadFile]

### Asistente

Resultado combinado confirmado:

- **Lint:** falla con 4 errores y 4 advertencias.
- **Tests:** 4 timeouts en `TaskForm` y 10 errores de workers.
- **Build:** exitoso en 4m 26s, con dos chunks superiores a 600 kB.

No se requieren más acciones para cerrar la auditoría.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed).

### Asistente

Sin novedades adicionales: el fallo de Vitest ya está documentado como timeouts y errores al iniciar workers. No hace falta otra acción.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
