---
date: 2026-06-15
type: conversation
source_agent: cursor
session_id: "95a8ac3c-8612-4f6b-8e06-27fcb0f10995"
project: "1781549212531"
source_path: "C:\\Users\\david\\.cursor\\projects\\1781549212531\\agent-transcripts\\95a8ac3c-8612-4f6b-8e06-27fcb0f10995\\95a8ac3c-8612-4f6b-8e06-27fcb0f10995.jsonl"
tags: [conversation, imported, cursor]
title: "Use the Supabase plugin in one concrete, useful way that shows why it's valuable in this w"
---

# Use the Supabase plugin in one concrete, useful way that shows why it's valuable in this w

**Fecha:** 2026-06-15  
**Agente:** cursor  
**Proyecto/contexto:** 1781549212531  
**Sesión:** `95a8ac3c-8612-4f6b-8e06-27fcb0f10995`  
**Origen:** `C:\Users\david\.cursor\projects\1781549212531\agent-transcripts\95a8ac3c-8612-4f6b-8e06-27fcb0f10995\95a8ac3c-8612-4f6b-8e06-27fcb0f10995.jsonl`

## Mensajes

### Usuario

Use the Supabase plugin in one concrete, useful way that shows why it's valuable in this workspace.

### Asistente

Voy a revisar el estado del plugin Supabase y usarlo de forma concreta en este workspace.


[tool:Read]
[tool:Glob]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:CallMcpTool]

### Asistente

El plugin ya está autenticado. Voy a auditar el proyecto Captus: tablas y avisos de seguridad/rendimiento.


[tool:CallMcpTool]
[tool:CallMcpTool]
[tool:CallMcpTool]

### Asistente

[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]

### Asistente

## Plugin Supabase — qué incluye

El plugin conecta Cursor directamente con tus proyectos de Supabase. Tiene tres capas:

**Skills** (se activan solas cuando trabajas con Supabase):
- **supabase** — base de datos, Auth, Edge Functions, RLS, migraciones, `@supabase/ssr`, etc.
- **supabase-postgres-best-practices** — optimización de queries, índices y diseño de esquema.

**Servidor MCP** (~29 herramientas), entre ellas:
- `list_projects`, `list_tables`, `execute_sql`, `apply_migration`
- `get_advisors` — auditoría de seguridad y rendimiento
- `get_logs`, `generate_typescript_types`, `deploy_edge_function`
- Gestión de ramas de base de datos y documentación (`search_docs`)

**Comandos** — puedes invocar skills y herramientas con `/` en el chat.

---

## Demostración concreta: auditoría de **Captus**

Usé el plugin contra tu proyecto activo **Captus** (`adretkrvrrezyvoyegkx`, Postgres 17, `us-east-1`).

### Esquema en un vistazo
40 tablas en `public`, la mayoría con RLS activo. Datos reales:
- 591 usuarios, 303 inscripciones a cursos, 433 entregas de tareas, 249 mensajes, etc.

### Hallazgo crítico de seguridad

**`public.course_materials` tiene RLS desactivado** — la única tabla expuesta. Cualquiera con la clave `anon` podría leer o modificar filas.

Para habilitarlo (necesitarás políticas después, o nadie podrá acceder):

```sql
ALTER TABLE public.course_materials ENABLE ROW LEVEL SECURITY;
```

Más info: [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)

### Otros avisos de seguridad
| Nivel | Problema |
|-------|----------|
| WARN | Bucket `assignments` permite listar todos los archivos a usuarios autenticados |
| WARN | Protección contra contraseñas filtradas (HaveIBeenPwned) desactivada en Auth |

### Rendimiento
Sin errores críticos. Varias sugerencias INFO, sobre todo **claves foráneas sin índice** (p. ej. `assignment_submissions.graded_by`). Útil si esas columnas se usan en filtros o JOINs frecuentes.

---

## Por qué esto es valioso

Sin el plugin habría que abrir el dashboard de Supabase, revisar tabla por tabla y buscar avisos a mano. Con el MCP, desde Cursor obtienes en segundos el mapa del esquema, el estado de RLS y una lista priorizada de problemas con enlaces de remediación — justo cuando estás escribiendo código contra esa base de datos.

¿Quieres que prepare las políticas RLS para `course_materials` o que revise el bucket `assignments`?


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
