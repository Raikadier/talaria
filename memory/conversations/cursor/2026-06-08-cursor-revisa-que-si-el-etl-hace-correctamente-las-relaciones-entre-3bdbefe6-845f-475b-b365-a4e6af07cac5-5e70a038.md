---
date: 2026-06-08
type: conversation
source_agent: cursor
session_id: "3bdbefe6-845f-475b-b365-a4e6af07cac5"
project: "d-Github-repos-advanced-db-final-project"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-advanced-db-final-project\\agent-transcripts\\3bdbefe6-845f-475b-b365-a4e6af07cac5\\3bdbefe6-845f-475b-b365-a4e6af07cac5.jsonl"
tags: [conversation, imported, cursor]
title: "revisa que si el etl hace correctamente las relaciones entre la tabla hechos y las dimensi"
---

# revisa que si el etl hace correctamente las relaciones entre la tabla hechos y las dimensi

**Fecha:** 2026-06-08  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-advanced-db-final-project  
**Sesión:** `3bdbefe6-845f-475b-b365-a4e6af07cac5`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-advanced-db-final-project\agent-transcripts\3bdbefe6-845f-475b-b365-a4e6af07cac5\3bdbefe6-845f-475b-b365-a4e6af07cac5.jsonl`

## Mensajes

### Usuario

revisa que si el etl hace correctamente las relaciones entre la tabla hechos y las dimensiones cuando carga a mongo porque parece que en mongo no estan las relaciones.

o... es normal y yo me estoy confundiendo?

### Asistente

Revisando cómo el ETL carga el data warehouse en MongoDB y si las claves foráneas entre hechos y dimensiones se persisten correctamente.


[tool:SemanticSearch]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

Comprobando en MongoDB si las claves foráneas de `fact_ventas` coinciden con las dimensiones.


[tool:Read]
[tool:Read]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

**Es normal: no te estás confundiendo del todo, pero tampoco hay un bug en el ETL.**

## Lo que ves en MongoDB es esperado

MongoDB **no dibuja relaciones** como SQL Server, PostgreSQL o el diagrama de Power BI. En Compass (o Atlas) ves **colecciones separadas** con campos sueltos; no hay líneas ni foreign keys físicas.

En un data warehouse en Mongo, las relaciones son **lógicas**: el hecho guarda IDs que coinciden con las dimensiones. Eso es el patrón estándar para BI con Mongo.

| En SQL | En MongoDB (tu proyecto) |
|--------|--------------------------|
| FK constraint `fact.cliente_id → dim.cliente.cliente_id` | Campo `cliente_id` en `fact_ventas` que coincide con `dim_cliente.cliente_id` |
| JOIN en consultas | `$lookup` en agregaciones, o relaciones en Power BI |
| Líneas en el diagrama ER | No existen en la UI de Mongo |

El `_id` (ObjectId) de cada documento es la clave interna de Mongo. **No es la clave dimensional.** Las relaciones del modelo estrella usan `cliente_id`, `fecha_id`, `producto_id`, etc.

## El ETL sí carga las relaciones correctamente

En `build_fact_ventas`, cada fila de hechos guarda las claves foráneas hacia las dimensiones:

```414:423:d:/Github repos/advanced-db-final-project/etl/etl/load_dw.py
        docs.append({
            "order_id": oid,
            "order_detail_id": f"{oid}-{pid}",
            "fecha_id": fid(o.get("OrderDate")),
            "fecha_entrega_id": fid(o.get("ShippedDate")),
            "cliente_id": cid,
            "empleado_id": _safe_int(o.get("EmployeeID")),
            "producto_id": pid,
            "shipper_id": _safe_int(o.get("ShipVia")),
            "territorio_id": terr_id,
```

Además crea **índices** en esos campos (equivalente a indexar FKs en SQL), pensados para consultas y Power BI:

```468:474:d:/Github repos/advanced-db-final-project/etl/etl/load_dw.py
    db.fact_ventas.create_index([("order_detail_id", ASCENDING)], unique=True, name="idx_pk_fact")
    db.fact_ventas.create_index([("fecha_id", ASCENDING)], name="idx_fv_fecha")
    db.fact_ventas.create_index([("cliente_id", ASCENDING)], name="idx_fv_cliente")
    db.fact_ventas.create_index([("empleado_id", ASCENDING)], name="idx_fv_empleado")
    db.fact_ventas.create_index([("producto_id", ASCENDING)], name="idx_fv_producto")
    db.fact_ventas.create_index([("shipper_id", ASCENDING)], name="idx_fv_shipper")
    db.fact_ventas.create_index([("territorio_id", ASCENDING)], name="idx_fv_territorio")
```

## Verificación en tu MongoDB real

Consulté `northwind_dw` y los datos están coherentes:

| Campo en `fact_ventas` | Filas huérfanas | Valores nulos |
|------------------------|-----------------|---------------|
| `fecha_id` | 0 | 0 |
| `cliente_id` | 0 | 0 |
| `empleado_id` | 0 | 0 |
| `producto_id` | 0 | 0 |
| `shipper_id` | 0 | 0 |
| `territorio_id` | 0 | 0 |

- **2.155** documentos en `fact_ventas`
- **0** claves foráneas rotas en las 6 dimensiones

Ejemplo real:

```json
{
  "order_detail_id": "10248-11",
  "fecha_id": "19960704",
  "cliente_id": "VINET",
  "producto_id": 11,
  "territorio_id": "FRA-ST"
}
```

Cada uno de esos valores existe en su dimensión correspondiente.

## Dónde “viven” las relaciones del modelo estrella

**En Mongo:** solo los IDs repetidos entre colecciones.

**En Power BI:** ahí sí están definidas las relaciones del star schema, en `relationships.tmdl`:

```1:28:d:/Github repos/advanced-db-final-project/proyecto-bi/northwind_bi.SemanticModel/definition/relationships.tmdl
relationship fv

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
