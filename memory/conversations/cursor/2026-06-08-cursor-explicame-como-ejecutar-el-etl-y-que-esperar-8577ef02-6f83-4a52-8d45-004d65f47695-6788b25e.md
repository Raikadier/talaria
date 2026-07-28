---
date: 2026-06-08
type: conversation
source_agent: cursor
session_id: "8577ef02-6f83-4a52-8d45-004d65f47695"
project: "d-Github-repos-advanced-db-final-project"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-advanced-db-final-project\\agent-transcripts\\8577ef02-6f83-4a52-8d45-004d65f47695\\8577ef02-6f83-4a52-8d45-004d65f47695.jsonl"
tags: [conversation, imported, cursor]
title: "explicame como ejecutar el etl y que esperar"
---

# explicame como ejecutar el etl y que esperar

**Fecha:** 2026-06-08  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-advanced-db-final-project  
**Sesión:** `8577ef02-6f83-4a52-8d45-004d65f47695`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-advanced-db-final-project\agent-transcripts\8577ef02-6f83-4a52-8d45-004d65f47695\8577ef02-6f83-4a52-8d45-004d65f47695.jsonl`

## Mensajes

### Usuario

explicame como ejecutar el etl y que esperar

### Asistente

Revisando la documentación y el código del ETL para explicarte cómo ejecutarlo y qué esperar.


[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

Revisando un log reciente para mostrarte la salida real del pipeline.


[tool:Read]
[tool:Read]

### Asistente

[tool:Read]

### Asistente

# Cómo ejecutar el ETL y qué esperar

El pipeline vive en `etl/` y hace un **full refresh** en dos fases: lee Northwind desde Supabase OLTP, lo deja limpio en Supabase Staging y construye el modelo estrella en MongoDB Atlas.

## Antes de ejecutar (setup una sola vez)

1. **Supabase OLTP** (`northwind-oltp`): aplicar `etl/sql/northwind_oltp_supabase.sql` (11 tablas con datos).
2. **Supabase Staging** (`northwind-staging`): no hace falta DDL manual; el pipeline lo crea en la primera corrida.
3. **MongoDB Atlas**: cluster, usuario con permisos de escritura y tu IP en *Network Access*.
4. **`.env` en la raíz del repo** (no dentro de `etl/`):

```bash
# Copiar plantilla
cp .env.example .env
# Completar SOURCE_DATABASE_URL, STAGING_DATABASE_URL, MONGO_URI
```

5. **Dependencias Python**:

```bash
cd etl/
pip install -r requirements.txt
```

### Diagnóstico previo (recomendado)

```bash
cd etl/
python _check_env.py
```

Debe mostrar `OK` para OLTP, Staging y MongoDB, y listar tablas/colecciones. No carga datos.

---

## Ejecución

### Comando principal (ciclo completo)

```bash
cd etl/
python pipeline.py
```

### Variantes útiles

| Comando | Qué hace |
|---------|----------|
| `python pipeline.py --dry-run` | Prueba conexión, extract y transform **sin escribir** en staging ni MongoDB |
| `python pipeline.py --only-extract` | Solo lee el OLTP y muestra conteos; se detiene ahí |
| `python pipeline.py --skip-dw` | Solo Fase A (staging); útil si Atlas no está disponible |
| `python pipeline.py --skip-validate` | Omite reglas de calidad (más rápido en desarrollo) |

---

## Qué hace paso a paso (6 etapas)

```
Supabase OLTP  →  [Tu PC: Python]  →  Supabase Staging  →  MongoDB Atlas
   (solo lectura)     transform            stg_*              dim_* / fact_*
```

| Paso | Nombre | Acción |
|------|--------|--------|
| **1/6** | Conexiones | Prueba OLTP y Staging (`SELECT 1`) |
| **2/6** | Bootstrap | Crea tablas `stg_*` y `etl_runs` si no existen; abre auditoría (`status=running`) |
| **3/6** | Extracción | Lee las 11 tablas fuente completas |
| **4/6** | Transformación | Limpia, normaliza y calcula métricas (`STG_ValorNeto`, días de entrega, etc.) |
| **4b** | Validación | Revisa calidad (warnings en log; no detiene el pipeline por defecto) |
| **5/6** | Carga Staging | `TRUNCATE` + insert por lotes de 500 filas |
| **6/6** | Carga DW | Lee staging, arma 7 dimensiones + `fact_ventas`, borra colecciones y recarga MongoDB |

**Importante:** el OLTP **nunca se modifica**. Cada ejecución vacía y recarga staging y MongoDB (full refresh).

---

## Qué esperar en una ejecución exitosa

Según tu último log (`etl_run_20260608_002016.log`), una corrida completa tarda **~60–90 segundos** y termina así:

```
Tablas extraídas   : 11/11
Errores extract    : 0
Registros staging  : 3,308
Docs DW            : 3,184
Duración total     : 72s
```

### Conteos esperados

**Fase A — Staging (3.308 filas en total):**

| Tabla | Registros |
|-------|-----------|
| `stg_order_details` | 2.155 |
| `stg_orders` | 830 |
| `stg_customers` | 91 |
| `stg_products` | 77 |
| `stg_territories` | 53 |
| `stg_employee_territories` | 49 |
| `stg_suppliers` | 29 |
| `stg_categories` | 8 |
| `stg_employees` | 9 |
| `stg_shippers` | 3 |
| `stg_region` | 4 |

**Fase B — MongoDB `northwind_dw` (3.184 documentos):**

| Colección | Documentos |
|-----------|------------|
| `fact_ventas` | 2.155 (1 fila = 1 línea de pedido) |
| `dim_fecha` | 672 (calendario jul 1996 — may 1998) |
| `dim_meta

_[truncado]_

### Usuario

revisa si en el staging se carga correctamente los datos. porque veo que la db de nortwind en el oltp es una db relacional con tablas y sus relaciones pero en el staging las tablas no estan relacionadas. investiga

### Asistente

Investigando el esquema de staging, el DDL y la carga del ETL para ver si los datos mantienen integridad aunque no haya FKs.


[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

Consultando OLTP y staging para comparar conteos y comprobar integridad referencial de los datos.


[tool:CallMcpTool]
[tool:CallMcpTool]
[tool:CallMcpTool]

### Asistente

[tool:CallMcpTool]
[tool:CallMcpTool]
[tool:CallMcpTool]
[tool:Read]

### Asistente

[tool:CallMcpTool]
[tool:CallMcpTool]
[tool:Grep]

### Asistente

# Investigación: staging sin relaciones visibles

Tu observación es correcta: en Supabase el **diagrama de staging no muestra flechas entre tablas** como en el OLTP. Eso no significa que los datos estén mal cargados. Revisé el esquema, el ETL y los datos reales en ambos proyectos.

## Conclusión rápida

| Aspecto | Estado |
|---------|--------|
| Conteos OLTP vs staging | **Idénticos** en las 11 tablas |
| Integridad referencial lógica | **0 huérfanos** en todas las relaciones |
| Valores transformados | **Coinciden** con el OLTP (ej. `STG_ValorNeto`) |
| JOINs entre tablas staging | **Funcionan** correctamente |
| Foreign Keys en DDL staging | **No existen** (solo PK + índices) |

**Los datos sí se cargan bien.** Lo que falta en staging son las **constraints de FK en el esquema**, no las columnas de relación.

---

## Por qué el staging “no se ve relacionado”

### OLTP (`northwind-oltp`)

Tiene 10 foreign keys explícitas, por ejemplo:

- `Orders` → `Customers`, `Employees`, `Shippers`
- `Order Details` → `Orders`, `Products`
- `Products` → `Categories`, `Suppliers`
- etc.

### Staging (`northwind-staging`)

El DDL en `etl/sql/northwind_staging_supabase.sql` define:

- **Primary keys** en cada `stg_*`
- **Índices** en columnas que actúan como FK (`CustomerID`, `EmployeeID`, `OrderID`, `ProductID`, etc.)
- **Sin ningún `FOREIGN KEY`**

Esto está documentado en el README:

> *"Las dimensiones van antes que los hechos para respetar dependencias lógicas (aunque el staging no tiene FK entre `stg_*`)."*

Es un patrón habitual en **landing zones / staging areas**:

1. **Carga más simple**: `TRUNCATE` + `INSERT` masivo sin preocuparse por el orden estricto de FKs.
2. **Full refresh**: cada run vacía y recarga todo; las FKs añaden fricción sin beneficio real en un dataset pequeño.
3. **Staging ≠ modelo relacional final**: es una zona intermedia **limpia y enriquecida**; las relaciones analíticas se materializan en la **Fase B** (MongoDB) con joins en Python.

Las columnas de relación **sí están** en staging:

```174:181:etl/sql/northwind_staging_supabase.sql
CREATE TABLE stg_orders (
    "OrderID"           INT              NOT NULL,
    "CustomerID"        CHAR(5),
    "EmployeeID"        INT,
    ...
    "ShipVia"           INT,
```

```200:203:etl/sql/northwind_staging_supabase.sql
CREATE TABLE stg_order_details (
    "OrderID"           INT              NOT NULL,
    "ProductID"         INT              NOT NULL,
```

Solo que Supabase no dibuja líneas porque no hay constraints `REFERENCES`.

---

## Verificación de datos (consultas reales)

### 1. Conteos: OLTP = Staging

| Tabla | OLTP | Staging |
|-------|------|---------|
| Categories | 8 | 8 |
| Customers | 91 | 91 |
| Orders | 830 | 830 |
| Order Details | 2.155 | 2.155 |
| Products | 77 | 77 |
| … | … | … |

**Total staging: 3.308 filas** — coincide con el último run exitoso del ETL.

### 2. Integridad referencial lógica (huérfanos)

Ejecuté LEFT JOINs equivalentes a cada FK del OLTP:

| Relación | Huérfanos |
|----------|-----------|
| orders → customers | **0** |
| orders → employees | **0** |
| orders → shippers | **0** |
| order_details → orders | **0** |
| order_details → products | **0** |
| products → categories | **0** |
| products → suppliers | **0** |
| territories → region | **0** |
| employee_territories → employees/territories | **0** |
| employees → reports_to | **0** |

Los datos mantienen la misma integridad que en el OLTP, aunque el motor no la imponga con FK.

### 3.

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
