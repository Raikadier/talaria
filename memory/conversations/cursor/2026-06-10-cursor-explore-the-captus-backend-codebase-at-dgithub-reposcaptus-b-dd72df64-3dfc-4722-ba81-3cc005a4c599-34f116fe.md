---
date: 2026-06-10
type: conversation
source_agent: cursor
session_id: "dd72df64-3dfc-4722-ba81-3cc005a4c599"
project: "d-Github-repos-captus-backend"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-backend\\agent-transcripts\\3240165d-fc69-4079-8abf-8d9a7724309b\\subagents\\dd72df64-3dfc-4722-ba81-3cc005a4c599.jsonl"
tags: [conversation, imported, cursor]
title: "Explore the captus-backend codebase at D:\\Github repos\\captus-backend to understand:"
---

# Explore the captus-backend codebase at D:\Github repos\captus-backend to understand:

**Fecha:** 2026-06-10  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-backend  
**Sesión:** `dd72df64-3dfc-4722-ba81-3cc005a4c599`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-backend\agent-transcripts\3240165d-fc69-4079-8abf-8d9a7724309b\subagents\dd72df64-3dfc-4722-ba81-3cc005a4c599.jsonl`

## Mensajes

### Usuario

Explore the captus-backend codebase at D:\Github repos\captus-backend to understand:
1. How the AI agent accesses course and work group information (tasks, submissions, deliveries)
2. Any advisory/prioritization logic for tasks based on due date, complexity, development time
3. How the agent uses course content/resources to answer student questions (RAG, context injection, etc.)

Search for keywords: course, grupo, entrega, submission, priority, complexity, RAG, embedding, vector, content, resources, asesoramiento

Return file paths, relevant code snippets summary, and gaps in functionality.

### Asistente

Voy a explorar el repositorio buscando cómo el agente accede a cursos, tareas y contenido, y si hay lógica de priorización o RAG.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:UpdateCurrentStep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:UpdateCurrentStep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

## Resumen ejecutivo

El módulo AI de **captus-backend** sigue un pipeline **router → pre-fetch de contexto (“RAG-lite”) → orchestrator con function calling**. Accede a cursos y asignaciones vía servicios REST existentes, pero **no hay embeddings/vectores**, **no hay lógica de asesoramiento por complejidad/tiempo de desarrollo**, y **los grupos de trabajo y el estado de entregas del estudiante están casi sin exponer al agente**.

---

## 1. Cómo el agente accede a cursos, grupos, tareas y entregas

### Pipeline principal

| Archivo | Rol |
|---|---|
| `D:\Github repos\captus-backend\src\routes\ai.js` | Endpoint `POST /api/ai/chat` |
| `D:\Github repos\captus-backend\src\ai\routerAgent.js` | Clasifica intent + pre-fetch de contexto |
| `D:\Github repos\captus-backend\src\ai\context.js` | Inyecta datos en el prompt del sistema |
| `D:\Github repos\captus-backend\src\ai\orchestrator.js` | Bucle agentic con tools (Gemini) |
| `D:\Github repos\captus-backend\src\ai\toolRegistry.js` | Herramientas ejecutables |
| `D:\Github repos\captus-backend\src\ai\prompts.js` | Taxonomía de intents y reglas |

Flujo:

```
POST /api/ai/chat
  → routerAgent: classifyIntent + fetchUserProfile
  → fetchContextForIntent(intent)     # texto pre-cargado
  → orchestrator: tools + respuesta final
```

### Cursos (estudiante)

**Pre-fetch** (`intent: courses`):

```87:98:D:\Github repos\captus-backend\src\ai\context.js
      case "courses": {
        const courses = await courseService.getCoursesForUser(userId, userRole);
        const list = Array.isArray(courses) ? courses : courses?.data ?? [];
        if (!list.length) return "El estudiante no tiene cursos activos.";
        return (
          "CURSOS DEL ESTUDIANTE:\n" +
          list
            .map((c) =>
              `- [${c.id}] ${c.name || c.title} | Código: ${c.code || c.invite_code || "N/A"} | Docente: ${c.professor || c.teacherName || "N/A"} | Progreso: ${Math.round((c.progress || 0) * 100)}%`
            )
            .join("\n")
        );
      }
```

**Tool** `list_courses` → `CourseService.getCoursesForUser(userId, "student")` en `toolRegistry.js` (líneas 314–347).

Fuente de datos: `D:\Github repos\captus-backend\src\services\CourseService.js` → `CourseRepository` + `EnrollmentRepository`.

### Asignaciones / entregas del curso (estudiante)

**Pre-fetch** (`intent: assignments`):

```101:126:D:\Github repos\captus-backend\src\ai\context.js
      case "assignments": {
        // Get student courses first, then pending assignments
        const courses = await courseService.getCoursesForUser(userId, userRole);
        ...
        for (const course of courseList.slice(0, 5)) {
          const result = await assignmentService.getAssignmentsByCourse(course.id, userId, userRole);
          ...
        }
        return (
          "ASIGNACIONES/ENTREGAS:\n" +
          allAssignments.slice(0, 10).map(a =>
            `- [${a.id}] ${a.title} | Curso: ${a.courseName} | Vence: ${a.due_date ? ... : "sin fecha"}`
          ).join("\n")
        );
      }
```

**Tool** `list_assignments` → `AssignmentService.getAssignmentsByCourse()` (líneas 1249–1301 de `toolRegistry.js`).

Modelo de datos (`database/schema.sql`):

- `course_assignments`: título, descripción, `due_date`, `is_group_assignment`
- `assignment_submissions`: `student_id` o `group_id`, `file_url`, `graded`, `grade`, `feedback`

### Grupos de trabajo (academic groups)

Existen en el dominio, **pero no en el agente**:

| Capa | Archivo |
|---|---

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
