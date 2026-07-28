---
date: 2026-06-15
type: conversation
source_agent: cursor
session_id: "7dfd9ec2-5dac-49d4-95a3-ec0ef0682bb9"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\cfb90943-cbfb-477a-be09-6be7a3b4e012\\subagents\\7dfd9ec2-5dac-49d4-95a3-ec0ef0682bb9.jsonl"
tags: [conversation, imported, cursor]
title: "Explore the TOGESC Flutter project at D:\\Github repos\\togesc\\TOGESC\\togesc to understand:"
---

# Explore the TOGESC Flutter project at D:\Github repos\togesc\TOGESC\togesc to understand:

**Fecha:** 2026-06-15  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `7dfd9ec2-5dac-49d4-95a3-ec0ef0682bb9`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\cfb90943-cbfb-477a-be09-6be7a3b4e012\subagents\7dfd9ec2-5dac-49d4-95a3-ec0ef0682bb9.jsonl`

## Mensajes

### Usuario

Explore the TOGESC Flutter project at D:\Github repos\togesc\TOGESC\togesc to understand:
1. Auth flow (account_screen, auth_provider, supabase_config)
2. Progress sync (hybrid_progress_repository, supabase_progress_repository)
3. Supabase migrations in repo root
4. Routing (go_router)
5. Game modes and how they're accessed
6. CI/deploy for dart-define secrets

Return: file paths, key classes, what's implemented vs missing for Phase 4 Should items (password recovery, email verification, offline sync queue) and Phase 5 prep.

### Asistente

Explorando el proyecto TOGESC en paralelo: auth, sync, migraciones, routing y modos de juego.


[tool:UpdateCurrentStep]
[tool:Read]
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
[tool:Glob]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:UpdateCurrentStep]

### Asistente

[tool:Grep]
[tool:Grep]

### Asistente

# Exploración TOGESC — Auth, Sync, Routing, Modos y Fases 4–5

## Mapa de archivos clave

| Área | Rutas absolutas |
|------|-----------------|
| **Auth config** | `D:\Github repos\togesc\TOGESC\togesc\lib\config\supabase_config.dart` |
| **Auth providers** | `D:\Github repos\togesc\TOGESC\togesc\lib\providers\auth_provider.dart` |
| **Cuenta UI** | `D:\Github repos\togesc\TOGESC\togesc\lib\screens\account_screen.dart` |
| **Sync listener** | `D:\Github repos\togesc\TOGESC\togesc\lib\widgets\auth_sync_listener.dart` |
| **SRS + repo wiring** | `D:\Github repos\togesc\TOGESC\togesc\lib\providers\srs_provider.dart` |
| **Local persistence** | `D:\Github repos\togesc\TOGESC\togesc\lib\services\progress_repository.dart` |
| **Hybrid sync** | `D:\Github repos\togesc\TOGESC\togesc\lib\services\hybrid_progress_repository.dart` |
| **Remote sync** | `D:\Github repos\togesc\TOGESC\togesc\lib\services\supabase_progress_repository.dart` |
| **Router** | `D:\Github repos\togesc\TOGESC\togesc\lib\app\router.dart`, `...\lib\providers\router_provider.dart` |
| **Entry point** | `D:\Github repos\togesc\TOGESC\togesc\lib\main.dart` |
| **Modos juego** | `...\lib\constants\game_constants.dart`, `...\lib\screens\home_screen.dart`, `game_screen.dart`, `speed_mode_select_screen.dart`, `speed_game_screen.dart` |
| **Migración Supabase** | `D:\Github repos\togesc\supabase\migrations\20260614000000_user_progress.sql` |
| **CI** | `D:\Github repos\togesc\.github\workflows\ci.yml` |
| **Deploy web** | `D:\Github repos\togesc\.github\workflows\deploy-web.yml`, `D:\Github repos\togesc\scripts\vercel-build.sh` |
| **Docs Supabase** | `D:\Github repos\togesc\docs\supabase_setup.md` |
| **Plan fases** | `D:\Github repos\togesc\Plan\plan_fases.txt` |

---

## 1. Auth flow

### Clases y providers

- **`SupabaseConfig`** — lee `SUPABASE_URL` y `SUPABASE_ANON_KEY` vía `String.fromEnvironment`; `isConfigured` si ambos no están vacíos.
- **`supabaseClientProvider`**, **`currentUserIdProvider`**, **`currentUserEmailProvider`**, **`authStateChangesProvider`**, **`supabaseAvailableProvider`** en `auth_provider.dart`.
- **`AccountScreen`** — UI email/password= up, sign in, sign out, “Sincronizar ahora”.
- **`AuthSyncListener`** — escucha `onAuthStateChange`; en `signedIn` / `initialSession` llama `mergeOnSignIn`.
- **`main.dart`** — inicializa Supabase con PKCE solo si `SupabaseConfig.isConfigured`.

### Flujo implementado

```
App arranca → Supabase.initialize (si hay dart-define)
           → AuthSyncListener escucha sesión
Home/About → /account
Sign up/in → client.auth.signUp / signInWithPassword
           → progressSyncOnSignInProvider() → HybridProgressRepository.mergeOnSignIn()
Sign out   → client.auth.signOut (progreso local se conserva)
Sin Supabase → pantalla “Sincronización no disponible”, juego 100% local
```

### Acceso a cuenta

- Icono persona en `HomeScreen` → `/account`
- Tile “Cuenta y sincronización” en `AboutScreen` → `/account`

### Qué falta (auth)

| Item | Estado |
|------|--------|
| Email/password | Implementado |
| OAuth (Google/Apple) | No implementado (plan Must menciona “email/OAuth”) |
| Recuperación contraseña | No (`resetPasswordForEmail`, UI) |
| Verificación email | Solo mensaje textual tras sign up; sin flujo, resend ni bloqueo |
| Deep links auth (reset/verify) | No en router |

---

## 2. Progress sync

### Arquitectura

```
ProgressRepository (abstract)
├── SharedPreferencesProgressRepository  (local)
├── SupabaseProgressRepository       

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
