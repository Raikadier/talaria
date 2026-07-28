---
date: 2026-06-10
type: conversation
source_agent: cursor
session_id: "b26f2463-111c-46cf-8c61-fd12c4772fc6"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\b26f2463-111c-46cf-8c61-fd12c4772fc6\\b26f2463-111c-46cf-8c61-fd12c4772fc6.jsonl"
tags: [conversation, imported, cursor]
title: "al intentar entrar a un curso, algo falla, investiga"
---

# al intentar entrar a un curso, algo falla, investiga

**Fecha:** 2026-06-10  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `b26f2463-111c-46cf-8c61-fd12c4772fc6`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\b26f2463-111c-46cf-8c61-fd12c4772fc6\b26f2463-111c-46cf-8c61-fd12c4772fc6.jsonl`

## Mensajes

### Usuario

al intentar entrar a un curso, algo falla, investiga

### Asistente

Investigando el fallo al entrar a un curso: busco el componente del error y el flujo de navegación.


[tool:Grep]
[tool:SemanticSearch]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Shell]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Glob]

### Asistente

Causa identificada: el backend devuelve `{ success: true, data: ... }`, pero los hooks devuelven `response.data` sin desenvolver; al renderizar, `realAssignments.map()` falla porque no es un array.


[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

Verificando en el navegador que la corrección funciona.


[tool:Glob]
[tool:Shell]

### Asistente

[tool:CallMcpTool]
[tool:Read]

### Asistente

[tool:CallMcpTool]

### Asistente

[tool:CallMcpTool]

### Asistente

[tool:CallMcpTool]

### Asistente

[tool:Shell]
[tool:CallMcpTool]

### Asistente

## Diagnóstico

El error **"Algo salió mal"** viene del `ErrorBoundary` en `MainLayout.jsx`. Ocurre cuando React lanza una excepción durante el renderizado, no por un fallo de red.

**Causa raíz:** el backend responde con este formato:

```json
{ "success": true, "data": [...] }
```

Pero los hooks de cursos (`getCourse`, `getAssignments`, `getGroups`, etc.) devolvían `response.data` **sin desenvolver** el campo `data`. En `StudentCourseDetailPage`, al terminar de cargar, el código hacía:

```javascript
realAssignments.map(a => ({ ... }))
```

Como `realAssignments` era `{ success: true, data: [...] }` y no un array, React lanzaba **`realAssignments.map is not a function`** y el `ErrorBoundary` mostraba el mensaje genérico.

Lo confirmé simulando la respuesta: el mismo patrón reproduce exactamente ese error.

## Corrección aplicada

Actualicé los hooks para usar las utilidades `unwrapData` / `unwrapList` (ya existían en el proyecto y se usaban en `useGroups`, `GroupsPage`, etc.):

- `useCourses.js` → `getCourse`
- `useAssignments.js` → `getAssignments`, `getAssignment`
- `useCourseGroups.js` → `getGroups`
- `useSubmissions.js` → `getSubmissions`
- `useEnrollments.js` → `getStudents` (mismo problema en la vista del profesor)

Con esto, al entrar a un curso deberían mostrarse correctamente el título, las tareas y el resto de la página.

Recarga la app e intenta entrar de nuevo a un curso. Si sigue fallando, expande **"Detalles del error"** en modo desarrollo y comparte el mensaje exacto.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

El fallo al entrar a un curso ya está corregido.

**Qué pasaba:** el backend devuelve `{ success: true, data: [...] }`, pero los hooks usaban esa respuesta completa como si fuera un array. Al renderizar la página del curso, `realAssignments.map(...)` fallaba y aparecía el mensaje genérico del `ErrorBoundary`.

**Qué se hizo:** se actualizaron los hooks (`useCourses`, `useAssignments`, `useCourseGroups`, `useSubmissions`, `useEnrollments`) para desenvolver la respuesta con `unwrapData` / `unwrapList`.

Recarga la app e intenta entrar de nuevo a un curso; debería cargar con normalidad.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
