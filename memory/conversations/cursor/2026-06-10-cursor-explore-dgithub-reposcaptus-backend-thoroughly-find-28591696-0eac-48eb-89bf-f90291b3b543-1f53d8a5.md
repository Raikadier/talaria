---
date: 2026-06-10
type: conversation
source_agent: cursor
session_id: "28591696-0eac-48eb-89bf-f90291b3b543"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\90b57349-ef63-4235-ac3b-680b5ad8283e\\subagents\\28591696-0eac-48eb-89bf-f90291b3b543.jsonl"
tags: [conversation, imported, cursor]
title: "Explore D:\\Github repos\\captus-backend thoroughly. Find:"
---

# Explore D:\Github repos\captus-backend thoroughly. Find:

**Fecha:** 2026-06-10  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `28591696-0eac-48eb-89bf-f90291b3b543`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\90b57349-ef63-4235-ac3b-680b5ad8283e\subagents\28591696-0eac-48eb-89bf-f90291b3b543.jsonl`

## Mensajes

### Usuario

Explore D:\Github repos\captus-backend thoroughly. Find:
1. Database schema/tables for tasks, notes, events, courses, groups, enrollments, assignments, subtasks
2. API routes for DELETE operations on these entities
3. Any existing seed scripts or data migration scripts
4. How courses are created (student vs teacher) and enrollments work
5. User ID lookup for davidbarcelo0411@gmail.com if mentioned
6. Categories and priorities reference data IDs

Return file paths, table names, cascade delete behavior, and recommended approach for bulk delete + seed via API or SQL script.

### Asistente

Explorando el backend de Captus para localizar esquema, rutas DELETE y scripts de datos.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

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
[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

## Informe: `D:\Github repos\captus-backend`

---

### 1. Esquema de base de datos (tablas relevantes)

**Fuente principal:** `D:\Github repos\captus-backend\database\schema.sql`  
**Migraciones adicionales:** `D:\Github repos\captus-backend\src\db\migrations\001_admin_role.sql`, `002_superadmin.sql`, `003_rls_all_tables.sql`  
**Documentación alternativa:** `D:\Github repos\captus-backend\docs\supabase-schema.sql`

| Entidad | Tabla(s) | PK | FKs principales |
|---------|----------|-----|-----------------|
| **Tasks** | `tasks` | `id` | `user_id` → `users`, `priority_id` → `priorities`, `category_id` → `categories`, `parent_task_id` → `tasks` |
| **Subtasks** | `subTask` (tabla separada) + opcional `tasks.parent_task_id` | `id_SubTask` / `id` | `id_Task` → `tasks`, `id_Category`, `id_Priority` |
| **Notes** | `notes` | `id` (bigint identity) | `user_id` → `users` |
| **Events** | `events` | `id` | `user_id` → `auth.users` |
| **Courses** | `courses` | `id` | `teacher_id` → `users`, `subject_id` → `subjects`; + `institution_id`, `period_id`, `grading_scale_id` (migración 001) |
| **Enrollments** | `course_enrollments` | `id` | `course_id` → `courses`, `student_id` → `users` |
| **Assignments** | `course_assignments` | `id` | `course_id` → `courses` |
| **Submissions** | `assignment_submissions` | `id` | `assignment_id` → `course_assignments`, `student_id` → `users`, `group_id` → `course_groups` |
| **Academic groups** | `course_groups`, `course_group_members` | `id` | `course_id` → `courses`, `created_by` → `users` |
| **Generic groups** (legacy/fase 2) | `groups`, `group_members` | `id` | No usados por rutas académicas actuales |
| **Categories** | `categories` | `id` (serial) | `user_id` → `users` (por usuario) |
| **Priorities** | `priorities` | `id` (serial) | Tabla lookup global |

**Comportamiento CASCADE en producción (schema real):**  
En `database\schema.sql` la mayoría de FKs **no declaran `ON DELETE CASCADE`**. Solo algunas migraciones lo hacen (`device_tokens`, `telegram`, `grading_scale_levels`, `academic_periods` → institution, etc.).

Implicaciones:
- Borrar un **curso** sin limpiar hijos fallará por FK (`course_enrollments`, `course_assignments`, `course_groups`, etc.).
- Borrar **assignment** con submissions fallará.
- Borrar **categoría** con tasks/subTask referenciándola fallará (salvo limpieza previa en app).
- `TaskService.delete` **sí** borra `subTask` hijos manualmente antes de borrar la task.

---

### 2. Rutas API DELETE

Prefijos en `D:\Github repos\captus-backend\src\app.js`:

| Entidad | Método + ruta | Archivo | Rol / notas |
|---------|---------------|---------|-------------|
| **Tasks** | `DELETE /api/tasks/:id` | `src\routes\TaskRoutes.js` | Usuario dueño |
| **Tasks por categoría** | `DELETE /api/tasks/category/:categoryId` | `src\routes\TaskRoutes.js` | Borra todas las tasks de esa categoría |
| **Subtasks** | `DELETE /api/subtasks/:id` | `src\routes\SubTaskRoutes.js` | Tabla `subTask` |
| **Notes** | `DELETE /api/notes/:id` | `src\routes\NotesRoutes.js` | Dueño |
| **Events** | `DELETE /api/events/:id` | `src\routes\EventsRoutes.js` | Dueño |
| **Courses** | `DELETE /api/courses/:id` | `src\routes\CourseRoutes.js` | Solo `teacher` dueño |
| **Assignments** | `DELETE /api/assignments/:id` | `src\routes\AssignmentRoutes.js` | Solo `teacher` |
| **Categories** | `DELETE /api/categories/:id` | `src\routes\CategoryRoutes.js` | Protege id=1 / nombre "General"; borra tasks de la categoría antes |
| **Enrollme

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
