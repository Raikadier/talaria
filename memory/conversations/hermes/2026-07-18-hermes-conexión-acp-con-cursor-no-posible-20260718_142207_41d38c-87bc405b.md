---
date: 2026-07-18
type: conversation
source_agent: hermes
session_id: "20260718_142207_41d38c"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Conexión ACP con Cursor no posible"
---

# Conexión ACP con Cursor no posible

**Fecha:** 2026-07-18  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260718_142207_41d38c`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

quiero que consumas todos los mcp servers configurados en cursor

### Asistente

Voy a investigar primero qué MCP servers tiene configurados Cursor y cómo funciona la integración. Cargo el skill de cursor y busco los archivos de configuración en paralelo.

### Asistente

Encontré el `mcp.json` principal de Cursor. Lo leo para ver qué servidores MCP tiene configurados.

### Asistente

Ya tengo el `mcp.json` de Cursor. Tiene **6 servidores MCP**:
- `powerbi-modeling-mcp` (stdio, exe local)
- `powerbi-report-mcp` (stdio, node local)
- `supabase-oltp`, `supabase-staging`, `Captus`, `supabase-togesc` (4 remotos HTTP/SSE de Supabase)

Para "consumirlos" de verdad, lo más sólido es registrarlos en Hermes (que ya consume MCP como anki/youtube) para que yo pueda invocar sus herramientas. Investigo cómo Hermes configura MCP y dónde están los servidores ya registrados.

### Asistente

Tengo el `mcp.json` de Cursor con 6 servidores. Hermes ya tiene comandos `hermes mcp add`. Voy a (1) ver qué MCP tiene Hermes ya, (2) leer la referencia nativa de MCP, y (3) verificar que existan los ejecutables locales de los servidores PowerBI.

### Asistente

Hermes ya tiene `anki` y `youtube` registrados y el SDK `mcp` está instalado. Voy a ver la sintaxis exacta de `hermes mcp add`, verificar soporte HTTP (los de Supabase son remotos), y comprobar que los exe de PowerBI arrancan.

### Asistente

`hermes mcp add` soporta `--url` (HTTP) y `--command/--args/--env` (stdio), y el SDK tiene soporte HTTP. Reviso el estado actual del config y si ya existe algún token de Supabase configurado (sin imprimir valores).

### Usuario

ahora, eres capaz de conectarte via acp a cursor?

### Asistente

Buena pregunta. Voy a verificar la capacidad real en vez de suponer: reviso qué hace `hermes acp` y confirmo si Cursor soporta ACP como cliente.

### Asistente

Respuesta corta: **no, no de la forma que lo planteas** — y la razón es de direccionalidad, no de falta de soporte.

## Por qué no vía ACP

ACP (Agent Client Protocol) conecta un **IDE cliente** con un **agente servidor**. La flecha va en un solo sentido:

- `hermes acp` arranca a **Hermes como servidor ACP** → espera que un IDE cliente (Zed, JetBrains) se conecte a él.
- **Cursor no actúa como cliente ACP** de un agente externo. Lo que hace Cursor con ACP es lo opuesto: expone *su propio* agente a otros IDEs (p.ej. Cursor dentro de JetBrains vía ACP, cursor como servidor). De hecho, "que Cursor soporte ACP para conectarse a agentes externos" sigue siendo una *feature request* en su foro.

O sea: no hay un modo "Hermes se conecta a Cursor por ACP". La pieza que falta (Cursor como cliente ACP) simplemente no existe.

## Cómo SÍ puedo integrarme con Cursor (lo real)

1. **MCP (lo que veníamos haciendo)** — funciona de verdad. Los 6 MCP servers de tu `mcp.json` de Cursor los registro en Hermes y yo paso a consumirlos como herramientas nativas (`mcp_powerbi_modeling_*`, `mcp_supabase_oltp_*`, etc.). Ya verifiqué:
   - `hermes mcp add` soporta `--url` (HTTP) y `--command/--args/--env` (stdio).
   - SDK `mcp` 1.26.0 con soporte `streamable_http` ✓ (los 4 de Supabase son remotos).
   - Los 2 exe/node de PowerBI existen y arrancan ✓.
   - Hermes ya tiene `anki` e `youtube` por la misma vía ✓.

2. **CLI de Cursor (`agent`) como subagente** — vía `delegate_task`/terminal usando el skill `cursor-code` (ya validado antes).

## Propuesta (modo verificación — espero tu "confirmo")

Para "consumir los MCP de Cursor" de forma real, propongo registrar estos 6 en Hermes:

| Servidor | Tipo | Comando |
|---|---|---|
| `powerbi-modeling-mcp` | stdio | `powerbi-modeling-mcp.exe --start` |
| `powerbi-report-mcp` | stdio | `node D:/Github repos/powerbi-report-mcp/dist/index.js` + env `PBIR_REPORT_PATH`, `MCP_TOOLS` |
| `supabase-oltp` | http | `https://mcp.supabase.com/mcp?project_ref=svrxnmbagwumyogxdlfu` |
| `supabase-staging` | http | `…?project_ref=crvyesiaqbqkqaslflya` |
| `Captus` | http | `…?project_ref=adretkrvrrezyvoyegkx` |
| `supabase-togesc` | http | `…?project_ref=puetlvcsrntwweuxinee` |

**Pendiente:** los 4 de Supabase son HTTP con auth de Sesión (cookie), no Bearer. Si fallan al conectar, necesitaría un token `supabase.com` (o que inicies sesión en el navegador y me pases la cookie de sesión). Lo verifico con `hermes mcp test <nombre>` tras registrarlos.

¿Confirmo el registro de los 6? (Empiezo por los 2 de PowerBI que no necesitan auth, y dejo los 4 de Supabase para validar auth aparte.)


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
