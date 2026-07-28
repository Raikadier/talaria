---
name: postgresql-table-design
domain: community
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\wshobson\\plugins\\database-design\\skills\\postgresql\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\wshobson\\plugins\\database-design\\skills\\postgresql\\SKILL.md"
tags: [data, design, community]
description: Use this skill when designing or reviewing a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features
---

# postgresql-table-design

**Dominio:** [[community]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\community\wshobson\plugins\database-design\skills\postgresql\SKILL.md`

**Descripción:** Use this skill when designing or reviewing a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features

**Cuándo usar:** - Define a **PRIMARY KEY** for reference tables (users, orders, etc.). Not always needed for time-series/event/log data. When used, prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness/opacity is needed. - **Normalize first (to 3NF)** to eliminate 

## Tags
#data #design #community

## Ejes temáticos
- [[data]]
- [[design]]

## Skills relacionadas
- [[ab-test-setup]]
- [[airflow-dag-patterns]]
- [[analytics-tracking]]
- [[competitive-teardown]]
- [[database-designer]]
- [[database-schema-designer]]
- [[gcp-cloud-architect]]
- [[gdpr-data-handling]]
- [[kpi-dashboard-design]]
- [[market-research]]
- [[microservices-patterns]]
- [[observability-designer]]
- [[pricing-strategist]]
- [[product-skills]]
- [[research-ops-skills]]
- [[saas-scaffolder]]
- [[senior-data-scientist]]
- [[sql-database-assistant]]
