---
date: 2026-06-09
type: conversation
source_agent: cursor
session_id: "c68a8b7a-b415-4551-b6fb-aac68c9bd14e"
project: "d-Github-repos-advanced-db-final-project"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-advanced-db-final-project\\agent-transcripts\\c68a8b7a-b415-4551-b6fb-aac68c9bd14e\\c68a8b7a-b415-4551-b6fb-aac68c9bd14e.jsonl"
tags: [conversation, imported, cursor]
title: "okey ahora mi objetivo es entender a fondo cada minima parte de este proyecto. eres un exp"
---

# okey ahora mi objetivo es entender a fondo cada minima parte de este proyecto. eres un exp

**Fecha:** 2026-06-09  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-advanced-db-final-project  
**Sesión:** `c68a8b7a-b415-4551-b6fb-aac68c9bd14e`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-advanced-db-final-project\agent-transcripts\c68a8b7a-b415-4551-b6fb-aac68c9bd14e\c68a8b7a-b415-4551-b6fb-aac68c9bd14e.jsonl`

## Mensajes

### Usuario

okey ahora mi objetivo es entender a fondo cada minima parte de este proyecto. eres un experto en docencia y en estrategias de enseñansa y formas de explicar. tu objetivo es responder a todas mis preguntas y guiar mi proceso de aprendizaje, no me contestes con demasiado contenido sino lo referente a la pregunta que te haga o tema que te consute. utiliza estrategias como la mayeutica, activve recall, space repetition, entre otras ademas de trivias, quices, .....

primero evalua bien cual es mi nivel y dominio de conocimiento para luego partir desde ahi

### Asistente

Explorando el proyecto para diseñar una evaluación diagnóstica acorde a su complejidad y tecnologías.


[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]

### Asistente

# Tu tutor para este proyecto

Antes de entrar al código, necesito ubicar **desde dónde partes**. Este repo es un sistema BI completo; no conviene estudiarlo todo a la vez.

## Qué es este proyecto (en una frase)

Northwind pasa de un **OLTP en Supabase** → **staging limpio** → **DW dimensional en MongoDB** → **Power BI** con 10 preguntas de negocio (P1–P10).

---

## Dominios que debes dominar

| Dominio | Qué cubre |
|---------|-----------|
| **A — Conceptos BI** | OLTP vs DW, ETL, esquema estrella, Kimball |
| **B — Arquitectura del proyecto** | Por qué 2 Supabase, por qué MongoDB, 2 fases |
| **C — ETL Python** | `pipeline.py`, transformaciones TR-xxx, `load_dw.py` |
| **D — Modelo dimensional** | 7 dims + 1 hecho, granularidad, segmentación |
| **E — Power BI** | TMDL, DAX, ODBC Atlas SQL, 4 páginas |

---

## Diagnóstico rápido (5 preguntas)

Responde **sin mirar el README**. Si no sabes, escribe *"no sé"* — eso también me sirve.

### 1. Conceptual (Dominio A)
¿Cuál es la diferencia entre **OLTP** y **Data Warehouse**? ¿Para qué sirve cada uno?

### 2. Arquitectura (Dominio B)
En este proyecto hay **dos proyectos Supabase** (fuente y staging).  
¿Por qué no cargar directamente de OLTP a MongoDB?

### 3. ETL (Dominio C)
¿Qué significa **full refresh** en este pipeline? ¿Qué pasa con los datos del run anterior?

### 4. Modelo (Dominio D)
`fact_ventas` tiene **2.155 filas**.  
¿Qué representa **una fila**? (pedido completo, producto, línea de pedido, cliente…)

### 5. Práctica (Dominio E)
¿Has ejecutado tú mismo `python pipeline.py` o abierto el `.pbip` en Power BI?  
Responde: **sí / parcial / no**.

---

## Cómo trabajaremos

| Estrategia | Cómo la usamos |
|------------|----------------|
| **Mayéutica** | Te pregunto antes de darte la respuesta |
| **Active recall** | Tú explicas; yo corrijo |
| **Spaced repetition** | Al final de cada tema, 2–3 preguntas de repaso |
| **Micro-quizzes** | Bloques de 3 preguntas tras cada sección |

**Regla:** una pregunta → una respuesta enfocada. Sin muros de texto.

---

## Tu turno

Responde las **5 preguntas del diagnóstico** (aunque sea breve).

Con eso te devuelvo:
1. Tu **nivel estimado** por dominio (principiante / intermedio / avanzado)
2. Por **dónde empezar** (no por el README entero)
3. Tu **primera lección** — un solo concepto, con un mini-quiz al final

¿Listo? Empieza por la pregunta 1.

### Usuario

1. el oltp es la fuente de los datos, es decir de donde se van a extraer los datos en primera instancia. el dw es una base de datos dimensional que es cargada por el etl y contiene los tados que consultara el power bi para su visualizacion
2. primero porque no tiene la misma arquitectura. el oltp por lo general suele ser relacional mientras que mongo se usa en este caso para una db dimensional, por lo que es necesario hacer todo un proceso secuencial para adaptar los datos y cargarlos en mongo
3. no se
4. pedido completo, tiene en cuenta: cliente, vendedor, factura, fecha, valor, producto, linea de pedido, entre otros
5. parcial

### Asistente

# Evaluación de tu nivel

| Dominio | Nivel | Observación |
|---------|-------|-------------|
| **A — Conceptos BI** | Intermedio-bajo | Intuición correcta; falta el *por qué* de cada capa |
| **B — Arquitectura** | Principiante | Mezclaste staging con la transición a MongoDB |
| **C — ETL** | Principiante | Full refresh: hueco claro |
| **D — Modelo dimensional** | Principiante | Error importante en granularidad de `fact_ventas` |
| **E — Práctica** | Intermedio-bajo | Has tocado el proyecto, pero faltan piezas clave |

**Conclusión:** partimos desde **arquitectura de 3 capas** y **granularidad del hecho**. Son la base de casi todo lo demás.

---

## Corrección importante (pregunta 4)

Dijiste: *"pedido completo"*. **No es correcto.**

En este proyecto:
- `stg_orders` → **830 pedidos** (cabecera)
- `fact_ventas` → **2.155 filas** = **1 línea de pedido** (OrderID + ProductID)

Un pedido con 3 productos genera **3 filas** en `fact_ventas`, no 1.

Piénsalo así: la factura tiene varias líneas; cada línea es una fila del hecho.

---

## Corrección suave (pregunta 2)

Tu respuesta hablaba de OLTP relacional → MongoDB dimensional. Eso explica **por qué existe el ETL**, pero la pregunta era otra:

> ¿Por qué **dos proyectos Supabase** (fuente **y** staging)?

Respuesta corta: el **staging no es MongoDB**. Es PostgreSQL intermedio donde el ETL deja datos **ya limpios** antes de modelar el DW.

---

## Primera lección: las 3 capas

```
OLTP (Supabase 1)     →  STAGING (Supabase 2)  →  DW (MongoDB)  →  Power BI
"¿Qué pasó?"              "Datos limpios"          "¿Cuánto vendimos?"   Visualiza
Solo lectura              TRUNCATE + INSERT        drop + insert
830 pedidos crudos        STG_ValorNeto, etc.      fact_ventas: 2.155 líneas
```

| Capa | Motor | ¿Se modifica? | Rol en una frase |
|------|-------|---------------|------------------|
| OLTP | Supabase | Solo `SELECT` | Sistema operacional simulado |
| Staging | Supabase (otro proyecto) | Se vacía y recarga cada run | Zona de aterrizaje + limpieza |
| DW | MongoDB | Se vacía y recarga cada run | Modelo estrella para BI |

**Por qué staging separado del OLTP:** si falla MongoDB, los datos limpios ya están en staging para inspeccionar; además simula extracción entre sistemas distintos (más realista).

---

## Full refresh (pregunta 3)

Cada vez que corre `python pipeline.py`:

1. **Staging:** `TRUNCATE` de cada `stg_*` → inserta todo de nuevo  
2. **MongoDB:** `drop()` de las 8 colecciones → inserta todo de nuevo  
3. **OLTP:** nunca se toca

**Ventaja:** estado predecible, sin duplicados ni registros huérfanos.  
**Costo:** recarga todo (~60–90 s), aunque Northwind es pequeño.

---

## Active recall — responde tú

Sin mirar arriba:

**A)** Si un pedido tiene 5 productos distintos, ¿cuántas filas genera en `fact_ventas`?

**B)** ¿En qué capa se calcula `STG_ValorNeto` — OLTP, staging o MongoDB?

**C)** ¿Qué capa consume Power BI directamente?

---

Cuando respondas A, B y C, seguimos con **Fase A vs Fase B del ETL** o profundizamos en lo que te haya quedado confuso. Tú eliges el ritmo.

### Usuario

okey bueno antes de entender el modelo dimensional y el etl, quiero saber que son los kpi y dax. que es eso?

### Asistente

Conectando KPI y DAX con ejemplos concretos de tu proyecto Northwind.


[tool:Grep]
[tool:Glob]

### Asistente

# KPI y DAX — explicación directa

Son conceptos distintos pero van juntos en Power BI.

---

## KPI (Key Performance Indicator)

Un **KPI** es un **número que resume si el negocio va bien o mal** respecto a un objetivo.

No es una tecnología: es una **idea de negocio**.

| Ejemplo en tu proyecto | Pregunta de negocio | ¿Qué mide? |
|------------------------|---------------------|------------|
| Total Ventas | P1 | ¿Cuánto vendimos? |
| % Cumplimiento Meta | P5 | ¿Los empleados cumplen su meta? |
| Avg Dias Entrega | P7 | ¿Qué tan rápido entregamos? |
| Margen % | P8 | ¿Qué tan rentable es cada producto? |

En el dashboard, un KPI suele verse como una **tarjeta grande** con un número:

```
┌─────────────────┐
│  Total Ventas   │
│   $1.265.793    │  ← esto es un KPI visual
└─────────────────┘
```

**Importante:** el KPI es el *concepto* (“ventas totales”). La *fórmula* que lo calcula vive en DAX.

---

## DAX (Data Analysis Expressions)

**DAX** es el **lenguaje de fórmulas de Power BI** (como Excel avanzado, pero sobre tablas relacionadas).

Sirve para crear **medidas**: cálculos que se adaptan al contexto del gráfico (filtros, segmentadores, etc.).

### Ejemplo real de tu proyecto

```dax
Total Ventas = SUM(fact_ventas[total_venta])
```

| Parte | Significado |
|-------|-------------|
| `Total Ventas` | Nombre de la medida (lo que ves en el visual) |
| `SUM(...)` | Suma todos los valores |
| `fact_ventas[total_venta]` | Columna de la tabla de hechos |

Si filtras por año 1997, DAX suma **solo** las filas de 1997. Si quitas filtros, suma todo.

### Otro ejemplo (más elaborado)

```dax
% Cumplimiento Meta = DIVIDE([Total Ventas], [Meta Periodo], 0) * 100
```

Compara ventas reales contra la meta → responde la pregunta P5.

---

## Cómo se relacionan en tu proyecto

```
MongoDB (fact_ventas, dim_*)
        ↓  Power BI importa las tablas
Modelo semántico (relaciones entre tablas)
        ↓  DAX calcula medidas en tabla _Medidas
Visuales (tarjetas, gráficos, mapas)
        ↓  Muestran KPIs al usuario
Preguntas P1–P10 respondidas
```

| Capa | Rol |
|------|-----|
| **ETL** | Prepara `total_venta`, `margen`, etc. en MongoDB |
| **DAX** | Agrega y combina esos datos según filtros del reporte |
| **KPI** | El indicador de negocio que el usuario interpreta |

**Analogía:** el ETL cocina los ingredientes; DAX es la receta; el KPI es el plato que comes.

---

## Diferencia clave: columna vs medida

| | Columna | Medida (DAX) |
|---|---------|--------------|
| Dónde vive | En la tabla (`fact_ventas[total_venta]`) | En `_Medidas` |
| Valor | Fijo por fila | Cambia según filtros del visual |
| Ejemplo | `total_venta = 45.00` en una línea | `[Total Ventas]` = suma de todas las líneas visibles |

---

## Mini-quiz (2 preguntas)

**1.** ¿`Total Ventas` es un KPI, una medida DAX, o ambos?

**2.** Si pones un gráfico de barras por mes y arrastras `[Total Ventas]`, ¿DAX suma todas las ventas históricas o solo las del mes de cada barra?

Responde y seguimos — o dime si quieres ver cómo una medida concreta responde a P5, P7 u otra pregunta de negocio.

### Usuario

1. es un kpi
2. suma todas las ventas del mes de cada barra

### Asistente

# Retroalimentación

## Pregunta 1 — Parcialmente correcta

`Total Ventas` es **las dos cosas**, según el ángulo:

| Ángulo | Qué es |
|--------|--------|
| **Negocio** | KPI — indicador clave de desempeño |
| **Técnico** | Medida DAX — la fórmula `SUM(fact_ventas[total_venta])` |

En la sustentación conviene decirlo así:

> *"`Total Ventas` es nuestro KPI principal de ingresos, implementado como medida DAX que suma la columna `total_venta` de la tabla de hechos."*

**Regla práctica:** KPI = *qué* mides · Medida DAX = *cómo* lo calculas.

---

## Pregunta 2 — Correcta

Cada barra filtra por un mes; DAX recalcula `[Total Ventas]` **solo con las filas visibles** en ese contexto.

Eso se llama **contexto de filtro** — es la idea central de DAX.

```
Barra "Jul 1996"  →  SUM solo filas con fecha_id de julio 1996
Barra "Ago 1996"  →  SUM solo filas con fecha_id de agosto 1996
```

Si no hubiera filtros, sumaría todo (~$1.265.793).

---

## Active recall — una pregunta más

En la página **Desempeño y Auditoría** (P5) hay un gráfico de ventas vs meta.

¿De dónde sale el número de **meta** — de `fact_ventas`, de `dim_metas_empleado`, o de una medida DAX que combina ambas?

Piensa antes de mirar el README.

### Usuario

okey, antes de eso explicame:

como se responde cada pregunta de negocio: que datos se necesitaron (tablas, columnas, kpi), como se calcularon los kpi en dax y cual es la respuesta final y como se responde en el reporte. esto para cada una de las preguntas

### Asistente

Revisando medidas DAX, tablas del modelo y páginas del reporte para mapear cada pregunta P1–P10 con precisión.


[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Grep]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]

### Asistente

# Mapa P1–P10: datos → DAX → reporte

Patrón común en todas las preguntas:

```
ETL prepara columnas en MongoDB  →  DAX agrega según filtros  →  Visual responde la pregunta
```

**Referencia global del dataset:** ~**$1.265.793** ventas totales · **2.155** líneas de hecho · **~31,3 %** margen promedio · periodo **jul 1996 – may 1998**.

---

## P1 — ¿Cómo han evolucionado las ventas por mes y año?

**Página:** Resumen Ejecutivo

| Capa | Detalle |
|------|---------|
| **Tablas** | `fact_ventas` + `dim_fecha` |
| **Columnas clave** | `total_venta`, `fecha_id` → `dim_fecha.anio`, `nombre_mes`, `trimestre` |
| **Origen ETL** | `total_venta` = `STG_ValorNeto` (precio × cantidad × (1 − descuento)) |

**KPIs / medidas DAX:**

| Medida | Fórmula (idea) |
|--------|----------------|
| `[Total Ventas]` | `SUM(fact_ventas[total_venta])` |
| `[Num Ordenes]` | `DISTINCTCOUNT(fact_ventas[order_id])` |
| `[Ventas YTD]` | `[Total Ventas]` filtrado con `DATESYTD(dim_fecha[fecha_completa])` |
| `[Ventas Año Anterior]` | `[Total Ventas]` con `SAMEPERIODLASTYEAR(...)` |
| `[Variación YoY %]` | `(actual − anterior) / anterior × 100` |

**Respuesta de negocio:** las ventas crecen de 1996 a 1997 y bajan en 1998; se ven picos mensuales (diciembre suele ser fuerte).

**En el reporte:**
- **Tarjetas:** `[Total Ventas]`, `[Num Ordenes]`
- **Línea:** mes (`nombre_mes`) × ventas, leyenda por `anio`
- **Columnas agrupadas:** ventas por mes, color por `trimestre`
- **Matriz:** `anio` × `trimestre` × `[Total Ventas]`
- **Segmentadores:** `anio`, `trimestre`

---

## P2 — ¿Top 10 clientes y su comportamiento en el tiempo?

**Página:** Análisis de Clientes y Geografía

| Capa | Detalle |
|------|---------|
| **Tablas** | `fact_ventas` + `dim_cliente` + `dim_fecha` |
| **Columnas** | `cliente_id`, `company_name`, `total_venta`, `order_date` |
| **ETL extra** | `dim_cliente.total_ventas_usd`, `segmento_cliente` (Premium/Regular/Nuevo/Inactivo) |

**Medidas DAX:**

| Medida | Fórmula (idea) |
|--------|----------------|
| `[Total Ventas]` | suma por cliente (vía relación) |
| `[Ranking Cliente]` | `RANKX(ALL(dim_cliente[company_name]), [Total Ventas], , DESC)` |
| `[Ventas por Cliente]` | `[Total Ventas] / [Clientes Activos]` |
| `[Clientes Activos]` | `DISTINCTCOUNT(fact_ventas[cliente_id])` |

**Respuesta de negocio:** pocos clientes concentran gran parte de ingresos; cada uno tiene curva mensual distinta.

**En el reporte:**
- **Barras horizontales Top 10:** `company_name` × `[Total Ventas]` (filtro Top N)
- **Línea temporal:** `nombre_mes` × `[Total Ventas]`, una línea por cliente seleccionado
- **Tabla:** cliente, ventas totales, ventas promedio por cliente

---

## P3 — ¿Productos con mayor volumen y contribución?

**Página:** Operaciones y Logística

| Capa | Detalle |
|------|---------|
| **Tablas** | `fact_ventas` + `dim_producto` |
| **Columnas** | `cantidad`, `total_venta`, `product_name`, `categoria` |

**Medidas DAX:**

| Medida | Fórmula (idea) |
|--------|----------------|
| `[Unidades Vendidas]` | `SUM(fact_ventas[cantidad])` |
| `[Total Ventas]` | suma por producto |
| `[% Contribución Ventas]` | ventas del producto / ventas de **todos** los productos × 100 |

**Respuesta de negocio:** identifica qué productos mueven más unidades y qué % del ingreso total aportan (no siempre coincide).

**En el reporte:**
- **Barras Top productos:** `product_name` × `[Total Ventas]`
- **Tabla:** producto, unidades, ventas, `% Contribución Ventas`

---

## P4 — ¿Categorías 

_[truncado]_

### Usuario

pero lo que quiero es que me expliques el porque de cada cosa no solo tablas sin contexto

### Asistente

# P1–P10 con el *por qué* de cada decisión

No basta con saber *qué tablas* usar. Hay que entender *por qué* cada pieza existe y cómo responde la pregunta de negocio.

---

## Idea central del proyecto

Northwind guarda **transacciones** (pedidos, líneas, fechas). Eso sirve para operar el negocio, no para responder preguntas como *“¿quién vende más?”* o *“¿hay estacionalidad?”*.

Por eso el flujo es:

1. **ETL** — convierte transacciones en un modelo pensado para analizar (esquema estrella).
2. **DAX** — agrega y compara según lo que el usuario filtre en el reporte.
3. **Visuales** — traducen números en respuestas que un gerente pueda interpretar.

---

## P1 — Evolución de ventas por mes y año

**Pregunta real:** *¿El negocio crece, se estanca o cae? ¿En qué meses sube o baja?*

**Por qué no basta con `Orders` del OLTP:**  
Allí cada fila es un pedido. Para ver tendencia temporal necesitas **sumar ingresos por periodo**. Eso exige una tabla de hechos con el valor de cada línea (`total_venta`) y una dimensión de tiempo (`dim_fecha`).

**Por qué `dim_fecha` y no solo `order_date`:**  
En BI conviene un **calendario completo** (672 días) con `anio`, `mes`, `trimestre`, `nombre_mes`. Así puedes agrupar, comparar años y usar funciones como `SAMEPERIODLASTYEAR` sin inventar lógica en cada gráfico.

**Por qué `[Total Ventas]` y no sumar `UnitPrice`:**  
El ingreso real ya incluye cantidad y descuento. El ETL calcula `STG_ValorNeto` porque esa es la métrica de negocio correcta.

**Por qué medidas como YoY:**  
Un gerente no solo quiere “cuánto vendimos”, sino **si vamos mejor que el año pasado**. YoY compara el mismo contexto temporal del año anterior.

**Por qué esos visuales:**
- **Tarjeta** → número grande, respuesta rápida.
- **Línea por mes** → muestra la *tendencia* (la esencia de P1).
- **Matriz año × trimestre** → resume patrones sin ver 36 meses sueltos.

**Respuesta que da el reporte:** ventas suben de 1996 a 1997 y bajan en 1998; hay meses claramente más fuertes que otros.

---

## P2 — Top 10 clientes y comportamiento en el tiempo

**Pregunta real:** *¿Quién nos da más dinero? ¿Esa relación es estable o un cliente compró mucho una vez y desapareció?*

**Por qué granularidad línea de pedido + dimensión cliente:**  
Un cliente puede tener muchos pedidos con muchos productos. Para saber cuánto aporta hay que **sumar todas sus líneas** → eso es `[Total Ventas]` filtrado por `cliente_id`.

**Por qué `[Ranking Cliente]`:**  
“Top 10” no es un filtro fijo en el ETL; es una **decisión de análisis**. DAX permite recalcular el ranking si cambias año o zona.

**Por qué la línea temporal por cliente:**  
Las barras dicen *quién* gana; la línea dice *cómo* compra en el tiempo (estacional, constante, en picos). Sin eso solo ves un ranking estático.

**Por qué `dim_cliente` trae `segmento_cliente` (ETL):**  
Segmentar (Premium, Regular, etc.) es regla de negocio que conviene **precalcular** una vez, no recalcular en cada clic del dashboard.

**Respuesta del reporte:** pocos clientes concentran ingresos; cada uno tiene un patrón de compra distinto mes a mes.

---

## P3 — Productos con mayor volumen y contribución

**Pregunta real:** *¿Qué movemos en cantidad? ¿Qué parte del dinero total viene de cada producto?*

**Por qué dos métricas distintas (`Unidades Vendidas` vs `Total Ventas`):**  
Un producto puede vender **muchas unidades baratas** y aportar poco dinero, o **pocas unidades caras** y ser clave. P3 pide las dos cosas a propósito.

**Por qu

_[truncado]_

### Usuario

haciendo un parentesis, para iniciar el etl basta con ejecutar el pipeline? o como?

### Asistente

Revisando requisitos previos y el flujo de arranque del ETL en el proyecto.


[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

# ¿Basta con ejecutar `pipeline.py`?

**Casi.** `python pipeline.py` es el comando único del ETL, pero **solo funciona si la infraestructura ya está lista**. No es como encender un switch sin cables conectados.

---

## Qué hace `pipeline.py` por ti

Al ejecutarlo, el propio pipeline:

1. Prueba conexión a OLTP y staging  
2. **Crea tablas staging** si no existen (`bootstrap.py` → DDL automático)  
3. Registra la ejecución en `etl_runs`  
4. Fase A: extrae → transforma → valida → carga staging  
5. Fase B: lee staging → construye dimensiones/hechos → carga MongoDB  

**No hace por ti:** crear proyectos Supabase, cargar Northwind en OLTP, ni configurar Atlas.

---

## Checklist antes del primer run

| Paso | ¿Quién lo hace? | Una vez / cada vez |
|------|-----------------|-------------------|
| 1. Proyecto Supabase **OLTP** creado | Tú (manual) | Una vez |
| 2. Ejecutar `northwind_oltp_supabase.sql` en OLTP | Tú (SQL Editor o MCP) | Una vez |
| 3. Proyecto Supabase **staging** creado | Tú (manual) | Una vez |
| 4. Cluster **MongoDB Atlas** + usuario + IP whitelist | Tú (Atlas UI) | Una vez |
| 5. Copiar `.env.example` → `.env` en la **raíz del repo** | Tú | Una vez |
| 6. Completar URLs en `.env` | Tú | Una vez |
| 7. `pip install -r requirements.txt` | Tú | Una vez (o si cambian deps) |
| 8. `python pipeline.py` | Tú | Cada actualización de datos |

El `.env` va en `advanced-db-final-project/.env`, **no** dentro de `etl/`.

---

## Flujo recomendado (primera vez)

```bash
# 1. Dependencias
cd etl/
pip install -r requirements.txt

# 2. Diagnóstico (opcional pero muy recomendable)
python _check_env.py

# 3. Prueba sin escribir nada
python pipeline.py --dry-run

# 4. Run completo
python pipeline.py
```

**`_check_env.py`** no es parte del pipeline; solo verifica que las 3 conexiones respondan y que OLTP tenga tablas.

---

## ¿Cuándo sí basta solo con `pipeline.py`?

En ejecuciones **posteriores**, si ya tienes:

- `.env` completo  
- OLTP con las 11 tablas Northwind  
- Staging accesible (tablas `stg_*` las crea el bootstrap)  
- MongoDB accesible desde tu IP  

Entonces sí:

```bash
cd etl/
python pipeline.py
```

Tarda ~60–90 segundos y deja staging + MongoDB recargados (full refresh).

---

## Flags útiles si algo falla

| Comando | Para qué |
|---------|----------|
| `--dry-run` | Probar extract + transform sin escribir |
| `--only-extract` | Solo leer OLTP (credenciales/red) |
| `--skip-dw` | Solo Fase A (si Atlas no está disponible) |
| `--skip-validate` | Más rápido en desarrollo |

---

## Cómo saber que terminó bien

- Consola: resumen final sin error, exit code 0  
- Staging: `stg_order_details` ≈ 2.155 filas  
- MongoDB: `fact_ventas` ≈ 2.155 documentos  
- `etl_runs`: última fila con `status = success`  

---

## Resumen en una frase

> **`pipeline.py` es el motor; `.env` + OLTP poblado + servicios cloud son el combustible.** La primera vez preparas infraestructura; después solo ejecutas el pipeline.

¿Quieres que en el siguiente mensaje repasemos **qué hace cada paso [1/6]…[6/6]** cuando corres `pipeline.py`?

### Usuario

enseñame a responder las preguntas de negocio con el reporte bi por favor

### Asistente

Revisando segmentadores y visuales de cada página para darte una guía práctica de lectura del reporte.


[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]

### Asistente

[tool:Grep]

### Asistente

# Cómo responder P1–P10 con el reporte BI

Guía práctica para **leer el dashboard** y **defenderlo** ante el jurado. No es teoría de DAX: es *dónde mirar, qué decir y en qué orden*.

---

## Antes de responder cualquier pregunta

### 1. Abrir y cargar datos

```
proyecto-bi/northwind_bi.pbip  →  Inicio → Actualizar
```

Si ves `(En blanco)` en todo: **Vista → Limpiar todas las segmentaciones** y vuelve a dejar `Año`, `Trimestre`, etc. en **(Todas)**.

### 2. Método de 4 pasos (úsalo en cada P)

| Paso | Qué haces |
|------|-----------|
| **1. Ubicar** | Ir a la página correcta |
| **2. Filtrar** | Ajustar segmentadores si hace falta |
| **3. Leer** | Mirar el visual clave + un número concreto |
| **4. Concluir** | Responder en lenguaje de negocio, no técnico |

### 3. Frase plantilla para la sustentación

> *"Para responder P___, voy a la página ___; uso el visual ___; con el filtro ___; el dato muestra que ___; por tanto concluyo que ___."*

---

## Mapa rápido: pregunta → página

| Pregunta | Página del reporte |
|----------|-------------------|
| P1, P10 | **Resumen Ejecutivo** |
| P2, P6, P9 | **Análisis de Clientes y Geografía** |
| P3, P4, P7 | **Operaciones y Logística** |
| P5, P8 | **Desempeño y Auditoría** |

**Números de referencia** (con datos cargados): ventas totales ~**$1.265.793** · **2.155** líneas · margen ~**31,3 %** · periodo **1996–1998**.

---

## P1 — ¿Cómo han evolucionado las ventas por mes y año?

**Página:** Resumen Ejecutivo

### Dónde mirar

| Visual | Para qué |
|--------|----------|
| Tarjeta **Total Ventas** | Cifra global |
| **Evolución Ventas Mensuales** (línea) | Tendencia mes a mes; leyenda por **año** |
| **Ventas Trimestrales por Mes** (columnas) | Comparar meses dentro de cada trimestre |
| **Ventas por Trimestre × Año** (matriz) | Resumen año × trimestre |

### Cómo interactuar

1. Segmentador **Año** → empieza en *(Todas)* para ver el panorama completo.
2. Luego filtra **1997** solo y compara con **1996**.
3. En la línea, sigue un año (ej. línea 1997) y señala meses altos y bajos.

### Qué decir (ejemplo)

> *"Las ventas totales del periodo son aproximadamente $1,26 millones. En la línea mensual se ve crecimiento de 1996 a 1997; en 1998 el volumen baja. La matriz trimestral confirma que Q4 suele ser más fuerte que Q1 en varios años."*

### Conclusión típica

El negocio **creció** en el primer biennium y **desaceleró** en 1998; hay **variación mensual** clara.

---

## P2 — ¿Top 10 clientes y comportamiento en el tiempo?

**Página:** Análisis de Clientes y Geografía

### Dónde mirar

| Visual | Para qué |
|--------|----------|
| Barras **Top 10** (por `company_name` × Total Ventas) | Quiénes lideran |
| **Comportamiento de Compra — Top Clientes** (línea) | Evolución mensual por cliente |
| Tabla con ventas por cliente | Detalle numérico |

### Cómo interactuar

1. En el Top 10, identifica el **#1** (nombre + monto en la barra).
2. En la línea, **haz clic** en un cliente del Top 10 para resaltar su curva (o usa el segmentador si hay filtro por cliente).
3. Segmentador **Año** → compara si el mismo cliente vendió más en 1997 que en 1996.

### Qué decir (ejemplo)

> *"El ranking muestra que pocos clientes concentran gran parte de las ventas. Al seguir su línea temporal, vemos que no todos compran igual: algunos tienen picos estacionales y otros compran de forma más estable."*

### Conclusión típica

Hay **concentración** de ingresos en pocos clientes; el comportamiento **no es uniforme** en el tiemp

_[truncado]_

### Usuario

como se explica esta diapositiva?

### Asistente

# Cómo explicar esta diapositiva

Es la pieza que **conecta MongoDB/Atlas con las preguntas P1–P10**. La idea central: Power BI no “dibuja gráficos sobre tablas crudas”; primero construye una **capa semántica** donde vive la lógica de negocio.

---

## Elevator pitch (20 segundos)

> *"Power BI no lee MongoDB directamente en los gráficos. Importamos los datos con Atlas SQL, los modelamos en un **motor tabular** (esquema estrella + relaciones), centralizamos **30 medidas DAX** en la tabla `_Medidas`, y los visuales solo consumen esas medidas. Así cada KPI se calcula igual en todas las páginas y podemos hacer comparaciones temporales sin tocar la base de datos."*

---

## Recorrido de la diapositiva (izquierda → derecha)

### 1. Atlas SQL (Modo Import)

**Qué es:** la conexión entre Power BI y el DW en MongoDB Atlas vía **Atlas SQL + ODBC** (no el driver `pymongo` del ETL).

**Qué decir:**
- Los datos vienen de `northwind_dw` (8 colecciones: `fact_ventas`, `dim_*`).
- **Modo Import** = los datos se copian al modelo de Power BI al hacer **Actualizar**.
- Ventaja: consultas rápidas en el dashboard; la sustentación puede funcionar offline si ya refrescaste.

**Frase útil:** *"Elegimos Import porque MongoDB no ofrece DirectQuery nativo estable en nuestro stack; el refresh programado mantiene el DW actualizado."*

---

### 2. Modelo tabular (TMDL) — el centro

**Qué es:** el **cerebro** del BI. En tu repo vive en:

```
proyecto-bi/northwind_bi.SemanticModel/
```

**TMDL** = Tabular Model Definition Language: el modelo en archivos de texto (tablas, relaciones, medidas), no solo dentro de un `.pbix` opaco.

**Qué incluye:**
- 8 tablas de datos + `_Medidas`
- Relaciones `fact_ventas` → dimensiones (fecha, cliente, producto, etc.)
- **30 medidas DAX** agrupadas por P1–P10

**"Fuente de la verdad"** significa:
- `[Total Ventas]` se define **una sola vez** en `_Medidas`.
- Todas las tarjetas y gráficos usan la **misma fórmula**.
- Si cambias la medida, cambia en todo el reporte → consistencia y auditoría.

**Frase útil:** *"No calculamos ventas en cada visual; la medida vive en el modelo y el gráfico solo la muestra."*

---

### 3. Visualizaciones

**Qué es:** las 4 páginas del reporte (Resumen Ejecutivo, Clientes, Operaciones, Desempeño).

**Qué decir:**
- Los visuales **no tienen lógica de negocio propia** (o mínima).
- Arrastran medidas como `[Total Ventas]`, `[% Cumplimiento Meta]`, `[Avg Dias Entrega]`.
- Los segmentadores (`anio`, `trimestre`, `zona`) filtran el contexto; DAX recalcula automáticamente.

**Analogía:** el modelo es la **receta**; el visual es el **plato servido**.

---

## Las dos cajas de abajo

### Arquitectura desacoplada (PBIP)

**Qué es:** el proyecto está en formato **`.pbip`**, que separa:

| Componente | Carpeta | Contenido |
|------------|---------|-----------|
| Modelo semántico | `northwind_bi.SemanticModel/` | TMDL, medidas, relaciones |
| Reporte | `northwind_bi.Report/` | PBIR, páginas, visuales |

**Por qué importa:**
- Puedes versionar en Git (como en tu repo).
- Un analista puede cambiar gráficos sin romper DAX.
- Un desarrollador puede cambiar medidas sin rediseñar todo el reporte.

**Frase útil:** *"Separamos la lógica matemática (modelo) de la representación visual (reporte). Eso es arquitectura desacoplada."*

---

### Lógica de negocio (YTD, inteligencia de tiempo)

**Qué es:** cálculos que **no existen en MongoDB** pero sí en DAX, por ejemplo:

```dax
[Ventas YTD] = CALCULATE([Total Ventas], DATESYTD(dim_f

_[truncado]_

### Usuario

donde se usa el nombre de la compra en la tabla de hechos?

### Asistente

Buscando en el modelo si existe un campo de nombre de compra en `fact_ventas` o si viene de una dimensión relacionada.


[tool:Grep]
[tool:Grep]
[tool:SemanticSearch]

### Asistente

[tool:Glob]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]

### Asistente

# ¿Dónde está el "nombre" en la tabla de hechos?

Respuesta directa: **en `fact_ventas` no hay ningún nombre** (ni del cliente, ni del producto, ni de la compra). Solo hay **claves** y **números**.

Eso es **intencional** en un esquema estrella.

---

## Qué sí tiene `fact_ventas`

| Tipo | Campos |
|------|--------|
| **Claves** | `order_detail_id`, `order_id`, `cliente_id`, `producto_id`, `empleado_id`, `fecha_id`, etc. |
| **Métricas** | `cantidad`, `total_venta`, `margen`, `dias_entrega`, etc. |
| **Fechas** | `order_date`, `shipped_date`, `required_date` |

En el ETL (`build_fact_ventas`) se construye así — sin nombres descriptivos:

```407:431:etl/etl/load_dw.py
        docs.append({
            "order_id": oid,
            "order_detail_id": f"{oid}-{pid}",
            "fecha_id": fid(o.get("OrderDate")),
            ...
            "cliente_id": cid,
            "empleado_id": _safe_int(o.get("EmployeeID")),
            "producto_id": pid,
            ...
            "total_venta": total,
            "margen": mg,
            "order_date": to_dt(o.get("OrderDate")),
            ...
        })
```

---

## Dónde están los nombres entonces

Los nombres viven en las **dimensiones** y llegan al reporte por **relaciones**:

| Si quieres ver… | Está en… | Se une con… |
|-----------------|----------|-------------|
| Nombre del **cliente** | `dim_cliente.company_name` | `fact_ventas.cliente_id` → `dim_cliente.cliente_id` |
| Nombre del **producto** | `dim_producto.product_name` | `fact_ventas.producto_id` → `dim_producto.producto_id` |
| Nombre del **empleado** | `dim_empleado.full_name` | `fact_ventas.empleado_id` → `dim_empleado.empleado_id` |
| Nombre del **transportista** | `dim_shipper.company_name` | `fact_ventas.shipper_id` → `dim_shipper.shipper_id` |
| Mes / año | `dim_fecha.nombre_mes`, `anio` | `fact_ventas.fecha_id` → `dim_fecha.fecha_id` |

**Ejemplo en el reporte (P2):** el Top 10 usa `dim_cliente.company_name` en el eje y `[Total Ventas]` como medida. Power BI cruza automáticamente por la relación; el nombre **no está** en el hecho.

---

## Si te refieres a "Última Compra Cliente" (P9)

Eso **no es una columna** en `fact_ventas`. Es una **medida DAX**:

```dax
[Última Compra Cliente] = CALCULATE(
    MAX(fact_ventas[order_date]),
    ALLEXCEPT(dim_cliente, dim_cliente[cliente_id])
)
```

| Parte | De dónde sale |
|-------|----------------|
| **Fecha** de la última compra | `fact_ventas[order_date]` (máximo por cliente) |
| **Nombre** del cliente en la tabla | `dim_cliente.company_name` (dimensión) |

En la tabla *"Clientes con Actividad en Declive"* ves ambas columnas juntas, pero vienen de tablas distintas unidas por el modelo.

---

## Por qué se diseña así

1. **Evitar redundancia** — el nombre del cliente se repetiría en 2.155 filas.
2. **Un solo lugar para actualizar** — si cambia el nombre, solo tocas `dim_cliente`.
3. **Menos espacio** — el hecho guarda IDs cortos (`"QUICK"`, `102`).
4. **Es la práctica Kimball** — hechos = números; dimensiones = contexto descriptivo.

---

## Resumen en una frase

> *"`fact_ventas` guarda **quién compró** (`cliente_id`), no **cómo se llama**; el nombre se obtiene al relacionar con `dim_cliente` en Power BI."*

---

¿Te referías al **nombre del cliente** (`company_name`), al **producto** (`product_name`), o a la medida **Última Compra Cliente**? Si me aclaras cuál, te sigo el rastro en un visual concreto.

### Usuario

lo que quiero saber es para que se usan las columnas de ship tal, ship tal... en la fuente de los datos

### Asistente

Buscando en el esquema OLTP y en el ETL cómo se usan las columnas de envío (Ship*).


[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

# Columnas `Ship*` en la fuente (OLTP)

En Northwind, casi todas están en la tabla **`Orders`** (cabecera del pedido). Describen **logística y destino del envío**, no el producto ni el precio de la línea.

---

## Contexto de negocio en el OLTP

Cuando un cliente hace un pedido, el sistema guarda:

| Grupo | Para qué sirve en la operación |
|-------|-------------------------------|
| **Fechas** | Cuándo se pidió, cuándo debía llegar, cuándo salió |
| **Transportista** | Quién lleva la mercancía |
| **Dirección Ship\*** | **A dónde** se envía (puede ser distinta a la dirección del cliente en `Customers`) |

En muchos pedidos `ShipCountry` coincide con el país del cliente, pero **no siempre**. Por eso Northwind guarda una **copia de la dirección de envío** en cada pedido: es el dato que valía **en el momento de la venta**.

---

## Cada columna `Ship*` (fuente)

| Columna OLTP | Significado | ¿Para qué existe en el ERP? |
|--------------|-------------|------------------------------|
| **`ShippedDate`** | Fecha en que se despachó | Saber si ya salió del almacén |
| **`RequiredDate`** | Fecha límite prometida al cliente | Compromiso de entrega |
| **`ShipVia`** | ID del transportista (FK → `Shippers`) | Quién hace el envío (Speedy Express, etc.) |
| **`ShipName`** | Nombre del destinatario / empresa en destino | Etiqueta del paquete |
| **`ShipAddress`** | Calle de entrega | Dirección física |
| **`ShipCity`** | Ciudad de entrega | Geografía del envío |
| **`ShipRegion`** | Estado / provincia | Geografía del envío |
| **`ShipPostalCode`** | Código postal | Geografía del envío |
| **`ShipCountry`** | País de entrega | Geografía del envío |

Relacionada pero sin prefijo `Ship`:

| Columna | Significado |
|---------|-------------|
| **`Freight`** | Costo del flete del pedido |

Y la tabla **`Shippers`**: catálogo de transportistas (`ShipperID`, `CompanyName`, `Phone`). `ShipVia` en `Orders` apunta ahí.

---

## Qué hace **tu proyecto** con cada una

No todas llegan al DW con el mismo peso. El flujo es: OLTP → staging (`stg_orders`) → MongoDB (`fact_ventas` / dimensiones).

### Muy usadas (P7 y hechos)

| Columna fuente | En el ETL | En el DW / BI |
|----------------|-----------|---------------|
| **`ShippedDate`** | `STG_DiasEntrega` = `ShippedDate − OrderDate` (TR-007) | `shipped_date`, `fecha_entrega_id`, extiende `dim_fecha` |
| **`RequiredDate`** | `STG_EntregaPuntual`: ¿llegó a tiempo? (TR-008) | `entrega_puntual` en `fact_ventas` → P7 (`% Entregas Puntuales`) |
| **`ShipVia`** | Se copia a staging | `shipper_id` en `fact_ventas` → `dim_shipper` → P7 por transportista |
| **`Freight`** | Se normaliza a decimal | `freight` en `fact_ventas` (costo envío del pedido) |

### Limpiadas en staging, pero **no** llevadas al DW en este modelo

| Columna fuente | En el ETL | En el DW |
|----------------|-----------|----------|
| **`ShipName`** | TR-001: texto en mayúsculas | Queda en `stg_orders`; no va a `fact_ventas` |
| **`ShipCity`** | Igual | Igual |
| **`ShipCountry`** | Igual | **No** se usa para territorio en el DW |

**Importante:** para geografía en el reporte (P6, mapas), el proyecto usa el **país del cliente** (`dim_cliente.country` / `dim_territorio`), no `ShipCountry`. Es una decisión de modelado: priorizaron “dónde está el cliente” frente a “dónde se envió ese pedido concreto”.

### Pasan a staging casi sin transformar

| Columna | Estado en el proyecto |
|---------|------------------------|
| **`ShipAddress`** | En `stg_orders`; no u

_[truncado]_

### Usuario

como se actualiza el etl de forma automatica? en que archivo y que linea del etl?

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Glob]
[tool:Read]

### Asistente

# Cómo se actualiza el ETL de forma automática

Respuesta corta: **la automatización no está dentro de un archivo Python con un cron**. La hace **Windows Task Scheduler** (Programador de tareas), que ejecuta el mismo comando que tú a mano.

---

## Quién dispara la actualización

| Capa | Qué hace |
|------|----------|
| **Task Scheduler (Windows)** | Ejecuta `python pipeline.py` cada X minutos |
| **`etl/pipeline.py`** | Orquesta todo el ETL (entrada única) |
| **`etl/etl/etl_meta.py`** | Registra cada corrida en `etl_runs` (prueba de que corrió) |

En el repo **no hay** un `.bat`, `.xml` ni script de cron versionado. La tarea se configura **en Windows**, fuera del código.

---

## Archivo principal: `etl/pipeline.py`

Es el punto de entrada manual **y** automático. Lo dice el propio archivo:

```15:15:etl/pipeline.py
Entrada única para ejecución manual y Task Scheduler (cron).
```

La ejecución arranca aquí:

```205:206:etl/pipeline.py
if __name__ == "__main__":
    main()
```

Cuando Task Scheduler lanza `python pipeline.py`, entra por esas líneas y corre `main()`.

### Qué hace `main()` en cada corrida automática

| Paso | Líneas aprox. | Acción |
|------|---------------|--------|
| [1/6] Conexiones | 89–104 | Prueba OLTP y staging |
| [2/6] Bootstrap + auditoría | 106–111 | DDL si falta + `etl_meta.start_run()` |
| [3/6] Extracción | 116–119 | Lee OLTP |
| [4/6] Transform + validate | 127–136 | Limpia datos |
| [5/6] Carga staging | 138–154 | Full refresh staging |
| [6/6] Carga DW | 156–162 | Full refresh MongoDB |
| Cierre éxito | 170–178 | `etl_meta.finish_run()` |
| Error | 191–202 | `etl_meta.fail_run()` |

La línea que **inicia la auditoría** de cada run automático:

```111:111:etl/pipeline.py
            run_id, batch_id = etl_meta.start_run(stg_engine, phase="full")
```

La que **cierra** con éxito:

```171:178:etl/pipeline.py
            etl_meta.finish_run(
                stg_engine,
                run_id,
                rows_loaded=rows_loaded,
                tables_ok=tables_ok,
                tables_failed=[],
                duration_sec=elapsed,
            )
```

---

## Archivo de auditoría: `etl/etl/etl_meta.py`

No programa nada; **documenta** que el ETL corrió (útil para Task Scheduler y la sustentación).

```27:48:etl/etl/etl_meta.py
def start_run(engine, phase: str = "full") -> tuple[int, str]:
    ...
    INSERT INTO etl_runs (status, batch_id, phase, source_name)
    VALUES ('running', :batch_id, :phase, 'Northwind')
```

Cada ejecución automática deja una fila en **`etl_runs`** (Supabase staging) con `started_at`, `finished_at`, `status`, `duration_sec`, etc.

---

## Cómo configurar la automatización (fuera del código)

Según el README del proyecto:

1. Abrir **Programador de tareas** de Windows.
2. Crear tarea → desencadenador cada **15–30 min**.
3. Acción:
   - Programa: `python.exe` (ruta completa)
   - Argumentos: `pipeline.py`
   - Directorio de inicio: carpeta `etl/` del repo
4. Verificar en Supabase staging:

```sql
SELECT run_id, started_at, status, duration_sec
FROM etl_runs
ORDER BY started_at DESC
LIMIT 5;
```

Si `started_at` se actualiza solo, la automatización funciona.

---

## Qué NO está automatizado (todavía)

| Mejora | Estado |
|--------|--------|
| Carga **incremental** (`watermark.py`) | Planeado, no implementado |
| ETL en la nube (GitHub Actions, etc.) | No — corre en **tu PC** |
| Refresh de Power BI | Separado — lo haces en Desktop o con gateway |

Cada run hoy es **full refr

_[truncado]_

### Usuario

es decir que no hay codigo que haga las ejecuciones automaticas? se tiene que configurar por aparte en windows scheduler?

### Asistente

**Exacto.** En este proyecto **no hay código Python** que programe ejecuciones periódicas (ni `schedule`, ni `cron`, ni `APScheduler`, ni GitHub Actions para el ETL).

Lo que sí hay en el código:

| Archivo | Rol |
|---------|-----|
| `etl/pipeline.py` | Script que **se ejecuta** cuando alguien (tú o el Scheduler) lo llama |
| `etl/etl/etl_meta.py` | **Registra** cada ejecución en `etl_runs` (auditoría) |

Lo que **no** hay en el repo:

- Tarea de Windows exportada (`.xml`)
- Script `.bat` / `.ps1` de programación
- Lógica tipo “cada 30 minutos ejecutar otra vez”

La **programación** la configuras **aparte** en el **Programador de tareas de Windows**: que cada X minutos ejecute `python pipeline.py` con el directorio de trabajo en `etl/`.

En el README el estado de Task Scheduler aparece como **opcional** (📋), no como algo ya versionado en el código.

**Analogía:** `pipeline.py` es el motor del coche; Task Scheduler es el **despertador** que lo enciende. El despertador no está en el repo, lo pones tú en Windows.

Si en la sustentación te preguntan: *“Sí, la automatización es externa al ETL; el pipeline es idempotente y deja trazabilidad en `etl_runs` para demostrar que corre de forma periódica.”*

### Usuario

que funcion del etl extrae las tablas del staging?

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

# Lectura del staging en el ETL

La extracción desde **staging** (Fase B) está en **`etl/etl/load_dw.py`**.

---

## Función que lee cada tabla

**`read_staging_table()`** — líneas **71-77**:

```71:77:etl/etl/load_dw.py
def read_staging_table(engine, table_name: str) -> list[dict]:
    """Lee una tabla stg_* completa y la convierte a lista de dicts para builders."""
    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
    records = df.to_dict("records")
    logger.info(f"  {table_name}: {len(records):,} registros leídos del staging")
    return records
```

Hace un `SELECT * FROM stg_xxx` y devuelve una lista de diccionarios.

---

## Función que orquesta la Fase B

**`load_dw()`** — líneas **449-470**: llama a `read_staging_table` **8 veces**:

| Llamada | Tabla staging |
|---------|----------------|
| línea 463 | `stg_customers` |
| línea 464 | `stg_employees` |
| línea 465 | `stg_products` |
| línea 466 | `stg_categories` |
| línea 467 | `stg_suppliers` |
| línea 468 | `stg_shippers` |
| línea 469 | `stg_orders` |
| línea 470 | `stg_order_details` |

Después construye dimensiones (`build_dim_*`) y `fact_ventas`, y carga MongoDB.

---

## Quién la invoca desde el pipeline

En **`etl/pipeline.py`**, paso **[6/6]**, línea **162**:

```python
dw_counts = load_dw(stg_engine, MONGO_URI, MONGO_DB, BATCH_SIZE)
```

---

## No confundir con la Fase A

| Fase | Origen | Archivo | Función |
|------|--------|---------|---------|
| **A** | OLTP (Supabase fuente) | `extract.py` | `extract_table()` / `extract_all()` |
| **B** | Staging (`stg_*`) | `load_dw.py` | `read_staging_table()` dentro de `load_dw()` |

**Resumen:** la función que extrae del staging es **`read_staging_table`**; quien la usa y arma el DW es **`load_dw`**.

### Usuario

en que parte se borra el staging para volverlo a cargar?

### Asistente

[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]

### Asistente

# Dónde se vacía el staging antes de recargar

Ocurre en la **Fase A**, archivo **`etl/etl/load_staging.py`**, con **`TRUNCATE TABLE`** (no `DROP` de tablas).

---

## Función que borra los datos

**`truncate_staging()`** — líneas **20-24**:

```20:24:etl/etl/load_staging.py
def truncate_staging(engine, table_name: str):
    """Vacía la tabla staging antes de recargar (full refresh)."""
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name}"))
    logger.debug(f"  Truncated {table_name}")
```

`TRUNCATE` vacía la tabla pero **mantiene la estructura** (columnas, índices).

---

## Cuándo se llama

Dentro de **`load_table()`** — líneas **45-46**, **antes** del `INSERT`:

```45:46:etl/etl/load_staging.py
    if truncate:
        truncate_staging(engine, stg_table)
```

`load_all()` recorre las 11 tablas fuente y, para cada una, llama a `load_table()` (línea **94**).

---

## Quién lo dispara desde el pipeline

En **`etl/pipeline.py`**, paso **[5/6] CARGA STAGING** — líneas **146-151**:

```146:151:etl/pipeline.py
            load_summary, load_errors = load_staging_all(
                stg_engine,
                clean_data,
                table_order=SOURCE_TABLES,
                batch_size=BATCH_SIZE,
                truncate=TRUNCATE_FIRST,
            )
```

El flag viene de **`.env`** → variable **`TRUNCATE_FIRST`** (default `true` en `etl/etl/config.py` línea 46).

Si `TRUNCATE_FIRST=false`, **no** se vacía y los datos se **añaden** encima (no es el comportamiento esperado en este proyecto).

---

## Flujo por tabla en cada run

```
Para cada tabla (Categories, Orders, etc.):
  1. TRUNCATE stg_xxx     ← truncate_staging()
  2. INSERT filas nuevas  ← to_sql(append)
```

Se repite para las **11** tablas `stg_*`.

---

## Qué NO se borra

| Tabla | ¿Se trunca? |
|-------|-------------|
| `stg_categories`, `stg_orders`, etc. | Sí, cada run |
| **`etl_runs`** | **No** — acumula historial de ejecuciones |

---

## Paralelo en MongoDB (Fase B)

El staging se trunca en Fase A; el DW se limpia en Fase B con **`drop()`** de colecciones en `load_dw.py` líneas **497-499** (equivalente al full refresh, pero en MongoDB).

---

**Resumen:** el vaciado del staging está en **`truncate_staging()`** → **`load_staging.py` líneas 20-24**, invocado desde **`load_table()`** línea 46, orquestado por **`pipeline.py`** paso 5/6.

### Usuario

como se crea la dimension tiempo

### Asistente

[tool:Read]
[tool:Grep]

### Asistente

# Cómo se crea la dimensión tiempo (`dim_fecha`)

Se construye en la **Fase B** del ETL, en **`etl/etl/load_dw.py`**, función **`build_dim_fecha()`** (líneas **121-155**). No viene de una tabla OLTP llamada "Calendar": el ETL **la genera** a partir de fechas en `stg_orders`.

---

## Cuándo se ejecuta

Dentro de **`load_dw()`**, línea **478**, después de leer staging:

```python
orders = read_staging_table(staging_engine, "stg_orders")
...
dim_fecha = build_dim_fecha(orders)
```

Luego se inserta en MongoDB como colección `dim_fecha` (~**672** documentos).

---

## Proceso en 4 pasos

### 1. Recolectar fechas del negocio

Recorre todos los pedidos en `stg_orders` y toma:

- **`OrderDate`** (fecha del pedido)
- **`ShippedDate`** (fecha de envío)

Las guarda en un `set` para no duplicar días.

```121:130:etl/etl/load_dw.py
def build_dim_fecha(orders: list[dict]) -> list[dict]:
    """Dimensión calendario: un documento por día entre min y max OrderDate/ShippedDate."""
    fechas = set()
    for o in orders:
        od = to_dt(o.get("OrderDate"))
        if od:
            fechas.add(od.date())
        shipped = to_dt(o.get("ShippedDate"))
        if shipped:
            fechas.add(shipped.date())
```

**Por qué incluir `ShippedDate`:** para que el calendario cubra también días de entrega (útil para `fecha_entrega_id` en hechos).

---

### 2. Definir el rango continuo

Con las fechas encontradas calcula **mínimo** y **máximo**:

```132:136:etl/etl/load_dw.py
    if not fechas:
        logger.warning("  Sin fechas — usando rango Northwind por defecto")
        mn, mx = date(1996, 7, 4), date(1998, 5, 6)
    else:
        mn, mx = min(fechas), max(fechas)
```

**Idea clave:** no solo los días con pedidos, sino **todos los días entre min y max** (calendario continuo). Así Power BI puede filtrar/agrupar por mes sin huecos raros en series temporales.

En Northwind: típicamente **1996-07-04 → 1998-05-06** = **672 días**.

---

### 3. Generar un documento por cada día

Bucle día a día desde `mn` hasta `mx`:

```138:153:etl/etl/load_dw.py
    docs, cur = [], mn
    while cur <= mx:
        dt = datetime(cur.year, cur.month, cur.day)
        docs.append({
            "fecha_id": cur.strftime("%Y%m%d"),
            "fecha_completa": dt,
            "anio": cur.year,
            "trimestre": (cur.month - 1) // 3 + 1,
            "mes": cur.month,
            "nombre_mes": NOMBRES_MES[cur.month],
            "semana_anio": cur.isocalendar()[1],
            "dia": cur.day,
            "nombre_dia": NOMBRES_DIA[cur.weekday()],
            "es_fin_semana": cur.weekday() >= 5,
        })
        cur += timedelta(days=1)
```

| Campo | Cómo se calcula | Para qué sirve en BI |
|-------|-----------------|----------------------|
| `fecha_id` | `"YYYYMMDD"` (ej. `"19970704"`) | Clave surrogate; une con `fact_ventas.fecha_id` |
| `fecha_completa` | datetime del día | Marcar como tabla de fechas en Power BI |
| `anio`, `mes`, `trimestre` | Del calendario | Segmentadores P1, P10 |
| `nombre_mes`, `nombre_dia` | Arrays en español | Etiquetas en gráficos |
| `semana_anio` | ISO | Análisis semanal |
| `es_fin_semana` | sáb/dom = `True` | Filtros de patrones |

---

### 4. Cargar en MongoDB

`load_dw()` hace `drop()` de `dim_fecha` y `insert_many` con esos documentos (full refresh).

---

## Cómo se enlaza con los hechos

En **`build_fact_ventas()`**, cada línea de pedido obtiene:

```python
"fecha_id": fid(o.get("OrderDate")),           # YYYYMMDD del pedido
"fecha_e

_[truncado]_

### Usuario

que es el modelo semantico de la visualizacion?

### Asistente

# ¿Qué es el modelo semántico de la visualización?

En Power BI hay **dos capas distintas**. Conviene no mezclarlas:

| Capa | Qué es | En tu proyecto |
|------|--------|----------------|
| **Modelo semántico** | El “cerebro”: tablas, relaciones, medidas DAX | `northwind_bi.SemanticModel/` (TMDL) |
| **Visualización / reporte** | Los gráficos, tarjetas, mapas, filtros | `northwind_bi.Report/` (PBIR) |

El **modelo semántico no es la visualización**. Es lo que la visualización **consume**.

---

## Analogía rápida

```
MongoDB (datos crudos en colecciones)
        ↓ Import
Modelo semántico  ←  "¿Qué significan los datos? ¿Cómo se relacionan? ¿Cómo calculamos ventas?"
        ↓
Visualizaciones   ←  "¿Cómo se ve? (barras, mapas, tarjetas)"
```

- **Datos** = números en tablas  
- **Modelo semántico** = significado + reglas de negocio  
- **Visualización** = presentación para el usuario  

---

## Qué contiene el modelo semántico

En tu proyecto incluye:

### 1. Tablas importadas
- `fact_ventas` (hechos)
- `dim_fecha`, `dim_cliente`, `dim_producto`, etc. (dimensiones)
- `_Medidas` (tabla solo para DAX)

### 2. Relaciones
Ejemplo: `fact_ventas.cliente_id` → `dim_cliente.cliente_id` (muchos a uno).

Sin relaciones, un gráfico por cliente no sabría sumar ventas correctamente.

### 3. Medidas DAX (lógica de negocio)
```dax
Total Ventas = SUM(fact_ventas[total_venta])
```
Definida **una vez** en `_Medidas`; todos los visuales la reutilizan.

### 4. Tipos de datos, formatos, jerarquías
- `total_venta` como número con formato `$`
- Jerarquía geográfica: País → Ciudad → Cliente
- `dim_fecha` marcada como tabla de fechas

Eso es **semántica**: cómo interpreta Power BI cada campo.

---

## Por qué se llama “semántico”

**Semántica** = el significado de los datos, no solo su almacenamiento.

| En MongoDB | En el modelo semántico |
|------------|------------------------|
| `total_venta` es un número en un documento | Es la **métrica de ingresos** que se suma con `[Total Ventas]` |
| `cliente_id` = `"QUICK"` | Es la **clave** que une al cliente "QUICK-Stop" en `dim_cliente` |
| `19970704` en `fecha_id` | Es el **4 de julio de 1997** con `anio`, `mes`, `trimestre` |

El modelo traduce **datos técnicos** en **conceptos de negocio** que el usuario entiende.

---

## En tu diapositiva (capa semántica)

Lo que mostraba la slide encaja así:

```
Atlas SQL (Import)  →  Modelo Tabular (TMDL)  →  Visualizaciones
     datos                 semántica                  reporte
```

- **TMDL** = archivos de texto del modelo (`tables/*.tmdl`, `relationships.tmdl`)
- **30 medidas en `_Medidas`** = fuente única de verdad para KPIs
- **PBIP desacoplado** = puedes cambiar gráficos sin reescribir DAX (y al revés)

---

## Qué NO es el modelo semántico

- No son los colores ni el layout del dashboard  
- No es el mapa ni la tarjeta KPI (eso es PBIR)  
- No es MongoDB ni el ETL (eso es la capa de datos)  

---

## Flujo completo en tu proyecto

```
ETL (Python)
  → MongoDB northwind_dw (esquema estrella físico)

Power BI Import + Atlas SQL
  → Modelo semántico (relaciones + DAX + tipos)

Usuario abre reporte
  → Visualizaciones leen el modelo (no Mongo directamente)
```

Cuando filtras **Año = 1997** en un slicer:
1. El **visual** aplica el filtro al modelo  
2. El **modelo** recalcula `[Total Ventas]` solo con filas de 1997  
3. El **gráfico** muestra el número resultante  

La magia está en el **modelo semántico**, no en el tipo de gráfico.

---

## Frase para sustentación

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
