---
date: 2026-06-09
type: conversation
source_agent: cursor
session_id: "90fea85b-7952-4b23-9017-aeb98f8608c1"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\2bea268e-c588-47cb-a6a2-6475ee7a6664\\subagents\\90fea85b-7952-4b23-9017-aeb98f8608c1.jsonl"
tags: [conversation, imported, cursor]
title: "Explora el proyecto en D:\\Github repos\\captus-web y encuentra:"
---

# Explora el proyecto en D:\Github repos\captus-web y encuentra:

**Fecha:** 2026-06-09  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `90fea85b-7952-4b23-9017-aeb98f8608c1`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\2bea268e-c588-47cb-a6a2-6475ee7a6664\subagents\90fea85b-7952-4b23-9017-aeb98f8608c1.jsonl`

## Mensajes

### Usuario

Explora el proyecto en D:\Github repos\captus-web y encuentra:
1. La estructura general del proyecto (qué tipo de app es, frameworks usados)
2. Los tests de Selenium existentes - busca archivos .test.js, .spec.js, archivos en carpetas __tests__, test, tests, selenium, e2e
3. El package.json para ver dependencias y scripts
4. Las páginas/rutas principales de la aplicación (carpeta src/pages, src/app, src/features, src/components)
5. Cualquier configuración de testing (jest.config, selenium webdriver config, etc.)

Sé muy exhaustivo y reporta:
- Contenido completo de todos los archivos de test de Selenium encontrados
- Estructura de carpetas del proyecto
- Scripts en package.json
- Rutas/páginas principales disponibles en la app
- Componentes principales (LoginForm, formularios, etc.)

### Asistente

Explorando el proyecto de forma exhaustiva: estructura, tests, dependencias y rutas.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:UpdateCurrentStep]

### Asistente

# Reporte exhaustivo: captus-web

## 1. Tipo de aplicación y stack

**Captus** es una **SPA (Single Page Application) frontend** orientada a gestión educativa (estudiantes, profesores y administradores).

| Capa | Tecnología |
|------|------------|
| Bundler / dev server | **Vite 7** (`vite.config.js`) |
| UI | **React 18** + **React Router DOM 7** |
| Estilos | **Tailwind CSS 4** + Radix UI (primitivos) |
| Estado / datos | **TanStack React Query**, Context API |
| Backend / auth | **Supabase** (`@supabase/supabase-js`) |
| Formularios | **react-hook-form** + **zod** |
| Deploy | **Vercel** (`vercel.json` — rewrite SPA) |
| Lenguaje | JS/JSX principalmente; algo de TypeScript (`src/types`, `useTasks.ts`) |

No hay carpeta `src/pages` ni `src/app` (no es Next.js). La estructura sigue el patrón **feature-based** bajo `src/features/`.

---

## 2. Estructura de carpetas del proyecto

```
D:\Github repos\captus-web\
├── index.html
├── package.json
├── vite.config.js
├── vitest.config.js
├── tailwind.config.js
├── postcss.config.js
├── eslint.config.js
├── sonar-project.properties
├── vercel.json
├── README.md
├── public/
│   └── icon.svg
├── src/
│   ├── main.jsx                    # Punto de entrada
│   ├── App.jsx                     # Rutas y providers
│   ├── index.css / App.css
│   ├── setupTests.js               # Setup Vitest
│   ├── components/                 # Componentes compartidos
│   │   ├── diagrams/               # DiagramEditor, MermaidRenderer
│   │   └── shared/                 # ErrorBoundary, AchievementNotification
│   ├── context/                    # Auth, Theme, Achievement, Task
│   ├── features/                   # Módulos por dominio (auth, tasks, admin…)
│   ├── hooks/                      # useAuth, useCourses, useGroups…
│   ├── lib/                        # utils, passwordValidator, progressCalculator
│   ├── services/                   # taskService, courseService, aiTaskService…
│   ├── shared/                     # api (supabase, client), achievementsConfig
│   ├── styles/
│   ├── types/
│   ├── ui/                         # Design system (button, input, dialog…)
│   └── utils/
├── tests/
│   ├── selenium/                   # Tests E2E Selenium (Python)
│   └── verification/               # Script Playwright (no Selenium)
├── scripts/                        # Scripts Python de migración UI
├── captures/                       # Capturas de pantalla de sesiones
└── documento de software ii/       # Documentación académica del proyecto
```

**`src/features/`** (módulos principales):

- `auth` — Login/registro  
- `dashboard` — Layout, sidebar, home  
- `tasks`, `calendar`, `notes`, `courses`, `groups`, `stats`, `chatbot`  
- `teacher` — Panel docente  
- `admin` — Panel administración  
- `settings`, `profile`, `achievements`, `notifications`  
- `landing` — Landing page (existe pero **no está enrutada**)  
- `projects` — Páginas de proyectos (existen pero **no están enrutadas**)  
- `student`, `subjects`, `categories`

---

## 3. Tests de Selenium

### Resumen

| Ubicación | Tipo | Lenguaje |
|-----------|------|----------|
| `tests/selenium/test_captus.py` | **Único test Selenium real** | Python |
| `tests/selenium/requirements.txt` | Dependencia | `selenium>=4.6.0` |
| `tests/selenium/presentacion.html` | Presentación educativa sobre Selenium | HTML (no es test) |

**No hay** archivos `.test.js` / `.spec.js` de Selenium en JavaScript.  
`selenium-webdriver` está en `package.json` como devDependency pero **

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
