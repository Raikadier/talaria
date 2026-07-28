---
date: 2026-07-17
type: conversation
source_agent: hermes
session_id: "20260717_131217_55eb47"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Configurar arranque automático con admin"
---

# Configurar arranque automático con admin

**Fecha:** 2026-07-17  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260717_131217_55eb47`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

por favor configurate para que abras al encender la pc o al iniciar sesion en la pc con privilegios de administrador

### Asistente

Voy a investigar primero cómo está instalado Hermes en tu equipo y qué mecanismos de autoarranque tiene Windows, para proponerte la mejor opción (inicio de sesión con privilegios de administrador). Déjame reunir datos.

### Asistente

Buenísimo, ya tengo la ruta del ejecutable. Hermes está instalado en `C:\Users\david\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`. Déjame revisar si ya tiene una opción de autoarranque integrada y cómo corre (gateway/servicio) antes de proponer el método.

### Asistente

Ya hay dos tareas programadas de Hermes: `\Hermes Admin Assert` y `\Hermes_Gateway`. Justo lo que necesitamos. Déjame inspeccionar sus detalles (qué ejecutan, si corren al iniciar sesión y si lo hacen con privilegios de administrador).

### Asistente

El redirect dentro de cmd no funcionó. Déjame capturar el XML directamente desde bash.

### Asistente

Déjame obtener los detalles con formato LIST y volcarlo a archivo de forma más robusta.

### Asistente

Dos tareas de Hermes ya existen (`\Hermes_Gateway` y `\Hermes Admin Assert`), ambas en modo "Interactive only" (es decir, se disparan al iniciar sesión). Necesito ver su XML para confirmar si ya corren con privilegios de administrador (`RunLevel`) y qué ejecutan exactamente. Déjame extraerlo vía PowerShell.

### Asistente

Déjame usar PowerShell directamente, que maneja mejor el XML de las tareas.

### Asistente

El XML viene como string, no como documento. Déjame exportarlo en crudo con `Export-ScheduledTask`.

### Asistente

Ahora sí tengo los XML. Déjame leerlos.

### Asistente

Ya tengo el panorama completo. Déjame leer qué lanza exactamente el servicio del gateway para confirmar el alcance.

### Asistente

Ya tengo el panorama completo. Antes de proponer la configuración, déjame ver cómo se abre la app de escritorio de Hermes (el comando `desktop`/`gui`) y si hay un ejecutable propio, para que mi propuesta sea exacta.

### Asistente

Casi listo. Déjame confirmar dos cosas: el valor actual de UAC (que la tarea "Admin Assert" modifica) y dónde está el ejecutable real de la app de escritorio (Electron), para que el autoarranque sea robusto y no dependa de un build pesado cada vez.

### Asistente

Ya tengo todo el diagnóstico. Te explico qué encontré y qué haré, para que lo confirmes antes de ejecutarlo (tu modo verificación).

## Lo que ya está configurado en tu PC

1. **Ya corres como administrador.** Tu UAC está desactivado (`EnableLUA = 0` en el registro). De hecho ya existe una tarea programada `\Hermes Admin Assert` que, en cada inicio de sesión, vuelve a poner `EnableLUA=0` para asegurar privilegios de admin. Así que "con privilegios de administrador" ya lo tienes cubierto.

2. **El gateway (el motor de mensajería/WhatsApp/Telegram) YA se autoinicia** al iniciar sesión mediante la tarea `\Hermes_Gateway` (LogonTrigger, 30s de espera, ventana oculta). O sea que Hermes funciona en segundo plano aunque no abras la app.

3. **Lo que NO se autoinicia es la app de escritorio (la ventana con la que chateas).** Esa la abres manualmente. Ahí está el faltante.

## Lo que voy a hacer

Crear una tarea programada `\Hermes Desktop Autostart` que abra la app de escritorio (el ejecutable empaquetado `Hermes.exe`) automáticamente al iniciar sesión, con `RunLevel=HighestAvailable` (admin). No toco el gateway ni el admin assert que ya existen.

Comando exacto que ejecutaría (vía PowerShell):
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\david\AppData\Local\hermes\hermes-agent\apps\desktop\release\win-unpacked\Hermes.exe"
$trigger = New-ScheduledTaskTrigger -AtLogOn -Delay (New-TimeSpan -Seconds 5)
$principal = New-ScheduledTaskPrincipal -UserId "S-1-5-21-2436406437-1303810279-1267298763-1002" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "Hermes Desktop Autostart" -Action $action -Trigger $trigger -Principal $principal -Description "Hermes Desktop auto-launch on logon (admin)"
```

Detalles:
- Usa el `.exe` ya compilado (no reconstruye nada → arranca rápido).
- `AtLogOn` = se dispara al iniciar sesión (encender y entrar).
- 5s de delay para que el sistema se asiente.
- `Highest` = admin.
- `MultipleInstancesPolicy` por defecto evita abrirla 2 veces.

## Una advertencia honesta
Tener `EnableLUA=0` (UAC apagado) significa que **cualquier programa corre como admin sin preguntar**, lo cual baja la seguridad de Windows. Lo mantengo así porque es justo lo que pediste y ya lo tenías, pero quería que lo supieras.

---

Dime **"confirmo"** y creo la tarea. Después verifico que quedó registrada (`schtasks /query`) y te digo cómo probarla (cerrar sesión y volver a entrar, o reiniciar). Si prefieres otro delay o que también lance el gateway de forma distinta, me lo dices.


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
