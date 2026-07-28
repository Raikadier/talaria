---
date: 2026-06-09
type: conversation
source_agent: cursor
session_id: "d78ef100-b6ee-4b68-b0ce-19ed7e447a5a"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\98b83a2b-6872-4cda-b049-363762fadfc3\\subagents\\d78ef100-b6ee-4b68-b0ce-19ed7e447a5a.jsonl"
tags: [conversation, imported, cursor]
title: "Explore the captus-web frontend at D:\\Github repos\\captus-web. I need a comprehensive audi"
---

# Explore the captus-web frontend at D:\Github repos\captus-web. I need a comprehensive audi

**Fecha:** 2026-06-09  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `d78ef100-b6ee-4b68-b0ce-19ed7e447a5a`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\98b83a2b-6872-4cda-b049-363762fadfc3\subagents\d78ef100-b6ee-4b68-b0ce-19ed7e447a5a.jsonl`

## Mensajes

### Usuario

Explore the captus-web frontend at D:\Github repos\captus-web. I need a comprehensive audit focused on:

1. Route structure - all pages/routes and how they're defined
2. API client configuration - base URL, auth headers, how backend is called
3. Calendar page - how it loads data, error "Error al cargar las tareas"
4. Groups page - what could cause white screen
5. AI/Captus AI - chat API, conversation history sidebar
6. Settings - dark mode and font size implementation
7. Notes - how content is rendered (markdown/latex?)
8. Task creation - create task button flow
9. Dropdown components styling

Return:
- Project structure overview
- Key file paths for each feature
- Obvious bugs or issues you find in code (missing error boundaries, wrong API endpoints, unhandled promises, etc.)
- API endpoint mappings used by frontend vs what might be expected

Be very thorough - read actual source files, not just list directories.

### Asistente

Explorando el frontend de captus-web: estructura del proyecto y archivos clave de cada área.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Glob]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:UpdateCurrentStep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Glob]
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
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

# Auditoría frontend captus-web

Stack: **Vite 7 + React 18 + React Router 7 + TanStack Query + Axios + Supabase Auth + Tailwind 4 + Radix/shadcn UI**.

---

## 1. Estructura del proyecto

```
D:\Github repos\captus-web\
├── index.html
├── vite.config.js          # Proxy /api → http://localhost:4000
├── package.json
├── src/
│   ├── main.jsx            # Entry: StrictMode + App
│   ├── App.jsx             # Router, guards, providers, lazy routes
│   ├── index.css           # Design system + dark mode CSS vars
│   ├── styles/globals.css  # .font-small/medium/large (NO importado)
│   ├── context/            # AuthContext, themeContext, AchievementContext
│   ├── hooks/              # useGroups, useCourses, useEvents, useAuth…
│   ├── services/           # taskService, aiTaskService, courseService…
│   ├── shared/api/         # client.js (axios), supabase.js, adminService.js
│   ├── ui/                 # shadcn: button, dialog, dropdown-menu, select…
│   ├── components/shared/  # ErrorBoundary, AchievementNotification
│   └── features/
│       ├── auth/           # LoginForm
│       ├── dashboard/      # MainLayout, Sidebar, HomePage
│       ├── tasks/          # TaskPage, TaskForm, useTasks.ts
│       ├── calendar/       # CalendarPage + views/modals
│       ├── groups/         # GroupsPage
│       ├── chatbot/        # ChatBotPage (Captus AI)
│       ├── notes/          # NotesPage
│       ├── settings/       # SettingsPage + sections
│       ├── courses/, stats/, profile/, notifications/
│       ├── teacher/, admin/, landing/, projects/ (sin rutas)
│       └── achievements/   # placeholder de prueba
```

**Patrón arquitectónico:** feature folders + hooks/services compartidos; rutas centralizadas en `App.jsx` con code-splitting (`lazy`); layout `MainLayout` con `Sidebar`/`TeacherSidebar` y `ErrorBoundary` por página.

---

## 2. Rutas — definición y mapa completo

**Archivo central:** `D:\Github repos\captus-web\src\App.jsx`

| Ruta | Componente | Guard |
|------|------------|-------|
| `/` | LoginForm | — |
| `/home` | HomePage | ProtectedRoute + MainLayout |
| `/courses`, `/courses/:id` | StudentCoursesPage, StudentCourseDetailPage | idem |
| `/tasks` | TaskPage | idem |
| `/chatbot` | ChatBotPage | idem |
| `/notes` | NotesPage | idem |
| `/profile` | ProfilePage | idem |
| `/calendar` | CalendarPage | idem |
| `/groups` | GroupsPage | idem |
| `/stats` | StatsPage | idem |
| `/achievements` | AchievementsPage (placeholder) | idem |
| `/settings` | SettingsPage | idem |
| `/notifications` | NotificationsPage | idem |
| `/diagrams` | StudentDiagramsPage | idem |
| `/teacher/*` | TeacherHomePage, courses, tasks, reviews, stats, diagrams, calendar | + TeacherRoute |
| `/admin/*` | Admin dashboard, users, courses, grading, periods, reports, institution | + AdminRoute + AdminLayout |
| `*` | Navigate → `/home` | — |

**Guards relevantes:**

```66:86:D:\Github repos\captus-web\src\App.jsx
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  // Dev: sin login. Prod: solo con VITE_BYPASS_AUTH=true explícito
  if (import.meta.env.MODE !== 'production' || import.meta.env.VITE_BYPASS_AUTH === 'true') return children;
  ...
};
```

En **desarrollo**, las rutas protegidas se renderizan **sin autenticación**. Las llamadas API siguen yendo con token Supabase; si no hay sesión → **401 → redirect a `/`**.

**Rutas huérfanas (código existe, no hay `<Route>`):**
- `LandingPage` → `src/features/landing/LandingPag

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
