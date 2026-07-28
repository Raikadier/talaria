---
date: 2026-07-09
type: conversation
source_agent: hermes
session_id: "20260709_180520_3cb3c0"
project: "tui"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, tui]
title: "hermes esta configurado para iniciar cuando se encienda windows?"
---

# hermes esta configurado para iniciar cuando se encienda windows?

**Fecha:** 2026-07-09  
**Agente:** hermes  
**Proyecto/contexto:** tui  
**Sesión:** `20260709_180520_3cb3c0`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

hermes esta configurado para iniciar cuando se encienda windows?

### Asistente

Voy a revisar las configuraciones de inicio automático de Windows para Hermes. Revisaré la carpeta de inicio, las claves de registro Run, y el Programador de tareas.

### Asistente

No encontré configuración de inicio automático. Déjame confirmar dónde está el ejecutable de Hermes para darte la ruta exacta por si quieres configurarlo.

### Asistente

Revisé todas las ubicaciones donde Windows carga programas al iniciar, y **Hermes NO está configurado para arrancar automáticamente**. Estos son los hallazgos:

**Lo que revisé y está VACÍO para Hermes:**
- 📁 Carpeta de inicio del usuario (`Startup`): solo tiene Rainmeter, RoundedTB, Send to OneNote, DionysusFlow — no Hermes.
- 📁 Carpeta de inicio de todos los usuarios: solo FxSound.
- 🔑 Registro (`HKCU\...\Run` y `HKLM\...\Run`): sin entradas de Hermes.
- ⏰ Programador de tareas (Task Scheduler): ninguna tarea con "hermes".

**Dónde está Hermes instalado:**
- CLI: `C:\Users\david\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`
- Instalador: `C:\Users\david\AppData\Local\hermes\hermes-setup.exe`

---

¿Quieres que lo configure para que inicie solo con Windows? Tengo dos formas limpias de hacerlo:

1. **Acceso directo en la carpeta de inicio** (lo más simple) — creo un `.lnk` que lanza la app de escritorio de Hermes cada vez que entras a Windows.
2. **Tarea programada** (más robusta) — con trigger "al iniciar sesión", y puedo ponerle un pequeño retraso para que espere a que cargue la red.

Una duda antes de hacerlo: ¿te refieres a la **app de escritorio (interfaz gráfica/TUI)** que usas ahora mismo, o solo necesitas que corra el **CLI/servicio en segundo plano** (por ejemplo para que los cron y el reporte de Telegram funcionen aunque no abras la ventana)? Eso cambia qué ejecutable uso en el acceso directo.

Si me confirmas, lo dejo listo en un par de pasos.


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
