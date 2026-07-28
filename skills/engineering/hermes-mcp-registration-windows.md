---
name: hermes-mcp-registration-windows
domain: engineering
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\engineering\\hermes-mcp-registration-windows\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\engineering\\hermes-mcp-registration-windows\\SKILL.md"
tags: [agent, writing, engineering]
description: "Build and register a custom MCP server with Hermes Agent on Windows. Covers the non-obvious Windows gotchas: Hermes config lives in %LOCALAPPDATA%/hermes (NOT ~/.hermes), native backslash paths required in config.yaml (CreateProcess spawns MCP subprocess, MSYS /c/ paths fail with WinError 2), write_file is blocked from writing config.yaml, and a no-Hermes handshake smoke test. Use after scaffolding any MCP server (e.g. via mcp-server-builder) that you want Hermes to call as mcp_* tools."
---

# hermes-mcp-registration-windows

**Dominio:** [[engineering]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\engineering\hermes-mcp-registration-windows\SKILL.md`

**Descripción:** Build and register a custom MCP server with Hermes Agent on Windows. Covers the non-obvious Windows gotchas: Hermes config lives in %LOCALAPPDATA%/hermes (NOT ~/.hermes), native backslash paths required in config.yaml (CreateProcess spawns MCP subprocess, MSYS /c/ paths fail with WinError 2), write_file is blocked from writing config.yaml, and a no-Hermes handshake smoke test. Use after scaffolding any MCP server (e.g. via mcp-server-builder) that you want Hermes to call as mcp_* tools.

**Cuándo usar:** You built an MCP server (stdio, `@mcp.tool()` via `mcp.server.fastmcp.FastMCP`). Now make it appear inside Hermes Agent as `mcp_<name>_*` tools. The Python scaffolding is covered by the `mcp-server-builder` skill; this skill covers the **Windows registration + verification** that

## Tags
#agent #writing #engineering

## Ejes temáticos
- [[agent]]
- [[writing]]

## Skills relacionadas
- [[hermes-mcp-server]]
- [[minimalist]]
- [[strict-api]]
