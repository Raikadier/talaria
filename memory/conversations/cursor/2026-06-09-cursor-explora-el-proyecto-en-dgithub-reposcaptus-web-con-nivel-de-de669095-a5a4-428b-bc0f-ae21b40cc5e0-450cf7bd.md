---
date: 2026-06-09
type: conversation
source_agent: cursor
session_id: "de669095-a5a4-428b-bc0f-ae21b40cc5e0"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\2abd5ac5-ca5d-4cde-ae6a-40731c6ffab5\\subagents\\de669095-a5a4-428b-bc0f-ae21b40cc5e0.jsonl"
tags: [conversation, imported, cursor]
title: "Explora el proyecto en D:\\Github repos\\captus-web con nivel de detalle \"very thorough\". Ne"
---

# Explora el proyecto en D:\Github repos\captus-web con nivel de detalle "very thorough". Ne

**Fecha:** 2026-06-09  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `de669095-a5a4-428b-bc0f-ae21b40cc5e0`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\2abd5ac5-ca5d-4cde-ae6a-40731c6ffab5\subagents\de669095-a5a4-428b-bc0f-ae21b40cc5e0.jsonl`

## Mensajes

### Usuario

Explora el proyecto en D:\Github repos\captus-web con nivel de detalle "very thorough". Necesito que identifiques y reportes:

1. **Stack tecnológico completo**: frameworks, librerías, versiones (package.json, requirements.txt, etc.)
2. **Arquitectura**: si hay separación backend/frontend, qué carpetas existen, cómo está organizado el proyecto
3. **Módulos principales / features**: lista todas las carpetas dentro de src/, pages/, features/, components/ o similares. Descríbelas brevemente.
4. **Requisitos funcionales implícitos**: basándote en los nombres de componentes, páginas, rutas y servicios, infiere cuáles son las funcionalidades del sistema (mínimo 15 RF).
5. **Casos de uso identificables**: actores del sistema y casos de uso principales (basándote en las rutas, pages, hooks, servicios).
6. **Líneas de código aproximadas**: si hay algún archivo de conteo o puedes listar cuántos archivos .jsx, .tsx, .js, .ts, .css hay.
7. **Base de datos / backend**: si hay conexión a Supabase, Firebase, APIs REST, esquemas de tablas, edge functions, etc.
8. **Herramientas de prueba identificadas**: archivos de test, configuraciones de Cypress, Jest, Playwright, etc.
9. **Configuración de despliegue**: Vercel, variables de entorno, etc.

Reporta todos los hallazgos de forma detallada y estructurada.

### Asistente

Explorando el proyecto a fondo: estructura, dependencias y configuración.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:UpdateCurrentStep]

### Asistente

# Reporte de exploración: Captus Web

**Ruta del proyecto:** `D:\Github repos\captus-web`  
**Tipo:** Frontend SPA (monorepo de backend **no incluido** en este repositorio)

---

## 1. Stack tecnológico completo

### Runtime y build
| Tecnología | Versión | Rol |
|---|---|---|
| **React** | ^18.2.0 | UI |
| **React DOM** | ^18.2.0 | Renderizado |
| **Vite** | ^7.2.4 | Bundler y dev server |
| **@vitejs/plugin-react-swc** | ^4.1.0 | Compilación JSX con SWC |
| **TypeScript** | ^6.0.3 | Tipos (migración gradual; mayoría JS) |

### Routing, estado y datos
| Librería | Versión | Uso |
|---|---|---|
| **react-router-dom** | ^7.9.6 | Rutas SPA |
| **@tanstack/react-query** | ^5.100.14 | Cache y fetching |
| **axios** | ^1.12.2 | Cliente HTTP al backend REST |
| **@supabase/supabase-js** | ^2.75.1 | Auth + Storage (avatars) |

### UI y estilos
| Librería | Versión | Uso |
|---|---|---|
| **Tailwind CSS** | ^4.1.16 | Estilos utilitarios |
| **@tailwindcss/postcss** | ^4.1.16 | Integración PostCSS |
| **tailwindcss-animate** | ^1.0.7 | Animaciones |
| **tw-animate-css** | ^1.4.0 | Animaciones adicionales |
| **Radix UI** (múltiples paquetes) | 1.x–2.x | Primitivos accesibles (dialog, tabs, select, etc.) |
| **class-variance-authority** | ^0.7.1 | Variantes de componentes |
| **clsx** + **tailwind-merge** | ^2.x | Composición de clases |
| **lucide-react** | ^0.454.0 | Iconos |
| **framer-motion** | 12.23.24 | Animaciones |
| **sonner** | ^1.7.4 | Toasts |
| **cmdk**, **vaul**, **embla-carousel-react** | varias | UI auxiliar (command palette, drawer, carousel) |

### Formularios y validación
| Librería | Versión |
|---|---|
| **react-hook-form** | ^7.60.0 |
| **@hookform/resolvers** | ^3.10.0 |
| **zod** | 3.25.76 |

### Visualización, editor y contenido
| Librería | Versión | Uso |
|---|---|---|
| **recharts** | 2.15.4 | Gráficos/estadísticas |
| **mermaid** | ^11.12.1 | Diagramas |
| **@monaco-editor/react** | ^4.7.0 | Editor de código Mermaid |
| **cytoscape** | ^3.33.4 | Grafos (diagramas) |
| **react-markdown** | ^10.1.0 | Markdown en notas |
| **remark-math** + **rehype-katex** + **katex** | varias | Fórmulas matemáticas |
| **dompurify** | ^3.3.3 | Sanitización HTML |
| **jspdf** | ^4.2.1 | Exportación PDF |
| **date-fns** | 4.1.0 | Fechas |
| **react-day-picker** | 9.8.0 | Selector de fechas |

### Despliegue y monitoreo
| Librería | Versión |
|---|---|
| **@vercel/speed-insights** | ^2.0.0 (en `package.json`, no referenciado en código fuente visible) |

### Testing y calidad
| Herramienta | Versión |
|---|---|
| **Vitest** | ^4.1.5 |
| **@vitest/coverage-v8** | ^4.1.5 |
| **@testing-library/react** | ^16.3.2 |
| **@testing-library/jest-dom** | ^6.9.1 |
| **jsdom** | ^29.0.1 |
| **selenium-webdriver** | ^4.44.0 (devDependency) |
| **ESLint** | ^9.36.0 |

### Scripts npm (`package.json`)
- `dev` → Vite (puerto típico 5173)
- `build` → `vite build` → `dist/`
- `preview` → `vite preview`
- `lint` → ESLint
- `test` / `test:watch` → Vitest

**No hay** `requirements.txt` en la raíz; solo en `tests/selenium/requirements.txt` (`selenium>=4.6.0`).  
**No hay** Firebase en el código.

---

## 2. Arquitectura

### Modelo general
```
┌─────────────────────────────────────────────────────────┐
│  Frontend SPA (este repo: captus-web)                   │
│  React + Vite + Tailwind                                │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Features   │  │  

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
