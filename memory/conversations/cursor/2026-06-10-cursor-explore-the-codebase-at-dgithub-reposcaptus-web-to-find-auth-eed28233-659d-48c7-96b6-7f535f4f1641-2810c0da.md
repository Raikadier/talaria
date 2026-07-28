---
date: 2026-06-10
type: conversation
source_agent: cursor
session_id: "eed28233-659d-48c7-96b6-7f535f4f1641"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\90b57349-ef63-4235-ac3b-680b5ad8283e\\subagents\\eed28233-659d-48c7-96b6-7f535f4f1641.jsonl"
tags: [conversation, imported, cursor]
title: "Explore the codebase at D:\\Github repos\\captus-web to find: authentication flow, user mana"
---

# Explore the codebase at D:\Github repos\captus-web to find: authentication flow, user mana

**Fecha:** 2026-06-10  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `eed28233-659d-48c7-96b6-7f535f4f1641`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\90b57349-ef63-4235-ac3b-680b5ad8283e\subagents\eed28233-659d-48c7-96b6-7f535f4f1641.jsonl`

## Mensajes

### Usuario

Explore the codebase at D:\Github repos\captus-web to find: authentication flow, user management, how to identify users by email (davidbarcelo0411@gmail.com), database connection config, and any existing scripts to delete or reset user data. Look for .env examples, prisma/supabase/firebase config, and admin utilities. Return relevant file paths and how user IDs are resolved from email.

### Asistente

Voy a explorar el repositorio en busca del flujo de autenticación, gestión de usuarios y configuración de base de datos.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:SemanticSearch]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]

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
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Glob]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

## Resumen

`D:\Github repos\captus-web` es **solo el frontend** (`captus-frontend`). La autenticación la hace **Supabase Auth**; los datos de aplicación viven en un **backend REST** (puerto `4000`, fuera de este repo) sobre **PostgreSQL en Supabase**. No hay Prisma, Firebase ni scripts de borrado/reset de usuarios en este repositorio.

---

## 1. Flujo de autenticación

| Paso | Archivo | Qué hace |
|------|---------|----------|
| Cliente Supabase | `D:\Github repos\captus-web\src\shared\api\supabase.js` | `createClient(VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY)` |
| Contexto global | `D:\Github repos\captus-web\src\context\AuthContext.jsx` | Sesión, login, registro, logout |
| UI login/registro | `D:\Github repos\captus-web\src\features\auth\components\LoginForm.jsx` | Formulario y redirección por rol |
| Hook | `D:\Github repos\captus-web\src\hooks\useAuth.js` | Acceso al contexto |
| Rutas protegidas | `D:\Github repos\captus-web\src\App.jsx` | `ProtectedRoute`, `AdminRoute`, `TeacherRoute` |
| Cliente API | `D:\Github repos\captus-web\src\shared\api\client.js` | Axios con JWT de Supabase en `Authorization: Bearer` |

**Flujo:**

1. **Login:** `supabase.auth.signInWithPassword({ email, password })` → luego `POST /users/sync` al backend.
2. **Registro:** `POST /users/check-email` → `supabase.auth.signUp` con metadata (`name`, `role`) → `POST /users/sync` si hay sesión.
3. **Sesión:** `getSession()` al arrancar + `onAuthStateChange`.
4. **Logout:** `supabase.auth.signOut()`.
5. **Cambio de contraseña:** `D:\Github repos\captus-web\src\features\settings\sections\SeguridadSection.jsx` — revalida con `signInWithPassword` y luego `updateUser({ password })`.

**Roles:** `user.user_metadata.role` o `user.app_metadata.role` (`student`, `teacher`, `admin`).

**Nota dev:** En no-producción, `ProtectedRoute` omite login (`App.jsx` líneas 69–70).

---

## 2. Gestión de usuarios

### Perfil (usuario autenticado)
- `D:\Github repos\captus-web\src\features\settings\sections\PerfilSection.jsx`
- `D:\Github repos\captus-web\src\features\profile\ProfilePage.jsx`

Endpoints usados:
- `GET /users/profile`
- `PUT /users/:userId` (nombre, carrera, bio, avatar)
- Avatares: `supabase.storage.from('avatars').upload(...)`

### Admin (rol `admin`)
- `D:\Github repos\captus-web\src\shared\api\adminService.js`
- `D:\Github repos\captus-web\src\features\admin\pages\AdminUsersPage.jsx`

| Acción | Endpoint |
|--------|----------|
| Listar miembros | `GET /admin/users?role=` |
| Invitar | `POST /admin/users/invite` `{ email, role }` |
| Remover de institución | `DELETE /admin/users/:userId` |
| Cambiar rol | `PATCH /admin/users/:userId/role` |

### Matrículas por email (docente)
- `D:\Github repos\captus-web\src\hooks\useEnrollments.js` → `POST /enrollments/add-student` `{ courseId, email }`

### Tipos
- `D:\Github repos\captus-web\src\types\index.ts` — `AuthUser`, `UserRole`, entidades con `user_id: string`

---

## 3. Cómo identificar usuarios por email (`davidbarcelo0411@gmail.com`)

**En este repo no hay lookup email → ID en el frontend.** El ID siempre viene de la sesión Supabase o del listado admin.

### Dónde aparece ese email
- `D:\Github repos\captus-web\tests\selenium\test_captus.py` (líneas 45–46) como `TEST_EMAIL` / `TEST_PASSWORD` para Selenium.

### Cómo se resuelve el user ID

| Contexto | Mecanismo |
|----------|-----------|
| Usuario logueado | `session.user.id` (UUID Supabase Auth) |
| Perfil/settings | `supabase.auth.getSession()` → `session.user

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
