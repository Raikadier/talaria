---
date: 2026-06-08
type: conversation
source_agent: cursor
session_id: "d9614ed2-e043-4e24-8914-ec2ecb7c3816"
project: "d-Github-repos-advanced-db-final-project"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-advanced-db-final-project\\agent-transcripts\\d9614ed2-e043-4e24-8914-ec2ecb7c3816\\d9614ed2-e043-4e24-8914-ec2ecb7c3816.jsonl"
tags: [conversation, imported, cursor]
title: "ahora como conecto mongo con power bi?"
---

# ahora como conecto mongo con power bi?

**Fecha:** 2026-06-08  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-advanced-db-final-project  
**Sesión:** `d9614ed2-e043-4e24-8914-ec2ecb7c3816`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-advanced-db-final-project\agent-transcripts\d9614ed2-e043-4e24-8914-ec2ecb7c3816\d9614ed2-e043-4e24-8914-ec2ecb7c3816.jsonl`

## Mensajes

### Usuario

ahora como conecto mongo con power bi?

### Asistente

Revisando tu proyecto para ver cómo está configurado MongoDB y darte pasos concretos para Power BI.


[tool:Glob]
[tool:SemanticSearch]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Grep]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]

### Asistente

[tool:Read]

### Asistente

Para tu proyecto, la conexión es **Power BI Desktop → MongoDB Atlas** en **modo Import**. Tu modelo en `proyecto-bi/` todavía apunta a LocalDB; el DW real ya está en Atlas (`northwind_dw`) después de correr el ETL.

## Flujo general

```
ETL (pipeline.py) → MongoDB Atlas (northwind_dw) → Power BI (Import + Refresh)
```

---

## 1. Requisitos previos

**a) Datos cargados en Atlas**

```bash
cd etl
python pipeline.py
```

Verifica que existan las 8 colecciones:

- `dim_fecha`, `dim_cliente`, `dim_empleado`, `dim_producto`
- `dim_shipper`, `dim_territorio`, `dim_metas_empleado`, `fact_ventas`

**b) Atlas accesible desde tu PC**

En MongoDB Atlas → **Network Access** → agrega tu IP actual (o `0.0.0.0/0` solo para desarrollo).

**c) Usuario con permiso de lectura**

Puedes usar el mismo de `.env` (`etl_northwind`) o crear uno solo lectura para BI.

---

## 2. Conectar desde Power BI Desktop

1. Abre `proyecto-bi/northwind_bi.pbip`.
2. **Obtener datos** → busca **MongoDB**.
3. En la cadena de conexión pega tu URI (la misma de `.env`):

```
mongodb+srv://etl_northwind:TU_PASSWORD@TU_CLUSTER.mongodb.net/?retryWrites=true&w=majority
```

> Si la contraseña tiene caracteres especiales (`@`, `#`, `%`), codifícala en URL.

4. Elige la base **`northwind_dw`**.
5. Marca las **8 colecciones**.
6. En **Opciones avanzadas**, deja **Import** (no DirectQuery; MongoDB no lo soporta nativamente en PBI).
7. En el Editor de Power Query:
   - Quita la columna **`_id`** de cada tabla (no la necesitas).
   - Tus documentos son planos; no hace falta expandir anidados.
8. **Cerrar y aplicar**.

---

## 3. Reemplazar las fuentes actuales (LocalDB)

Hoy `fact_ventas` y las dimensiones construyen datos en M desde SQL Server local. Con MongoDB **solo importas** lo que ya calculó el ETL.

Ejemplo para `dim_cliente` en Power Query (M):

```powerquery
let
    Source      = MongoDB.Database("mongodb+srv://usuario:pass@cluster.mongodb.net/"),
    northwind_dw = Source{[Name="northwind_dw"]}[Data],
    dim_cliente  = northwind_dw{[Name="dim_cliente"]}[Data],
    SinId        = Table.RemoveColumns(dim_cliente, {"_id"})
in
    SinId
```

Para `fact_ventas` sería igual, cambiando el nombre de la colección. **No necesitas** el M largo que hoy une `Orders` + `Order Details` en LocalDB.

Repite para las 8 tablas o sustituye la fuente de cada partición en el modelo semántico.

---

## 4. Validar el modelo

Después del refresh:

| Tabla | Registros esperados |
|-------|---------------------|
| `fact_ventas` | ~2.155 |
| `dim_cliente` | ~91 |
| `dim_fecha` | ~672 |
| `dim_metas_empleado` | ~108 |

Comprueba que las **relaciones** sigan activas (`fecha_id`, `cliente_id`, `empleado_id`, etc.) y que las medidas DAX devuelvan valores razonables.

---

## 5. Actualizar datos (refresh)

Cada vez que corras el ETL:

1. `python pipeline.py` (recarga Atlas).
2. En Power BI: **Inicio → Actualizar** (o F5).

Si publicas en Power BI Service, configura un **gateway** y programa el refresh; la máquina que refresca también debe poder llegar a Atlas (IP en Network Access).

---

## 6. Plan B (sin red)

Si falla Atlas en la sustentación:

```bash
cd plan-b
python generate_csvs.py
```

En Power BI: **Obtener datos → Texto/CSV** desde `plan-b/csvs/`.

---

## Errores frecuentes

| Error | Solución |
|-------|----------|
| Timeout / no conecta | Revisa IP en Atlas Network Access |
| Authentication failed | Usuario, contraseña y URI |
| Tabla vacía | Corre `python pipeline.py` primero |
| Tipos incorrec

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
