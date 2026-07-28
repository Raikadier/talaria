---
name: video-processor
domain: media
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\media\\video-processor\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\media\\video-processor\\SKILL.md"
tags: [youtube, coding, design, media]
description: "Pipeline local y offline para que el agente \"procese/entienda\" un video extrayendo audio (transcrito con faster-whisper), frames clave (vistos por vision_analyze del agente) y sintetizando contexto. Usar cuando David pida \"procesa este video\", \"extrae el audio/texto de este video\", \"dime qué hay en este video\", \"analiza este mp4/YouTube\", o quiera que el agente \"vea\" contenido visual. NO es para editar/cortar (eso es auto-editor)."
---

# video-processor

**Dominio:** [[media]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\media\video-processor\SKILL.md`

**Descripción:** Pipeline local y offline para que el agente "procese/entienda" un video extrayendo audio (transcrito con faster-whisper), frames clave (vistos por vision_analyze del agente) y sintetizando contexto. Usar cuando David pida "procesa este video", "extrae el audio/texto de este video", "dime qué hay en este video", "analiza este mp4/YouTube", o quiera que el agente "vea" contenido visual. NO es para editar/cortar (eso es auto-editor).

**Cuándo usar:** Permite al agente **procesar** un video (no editarlo): extrae el audio y lo transcribe, extrae frames clave y los "ve" con su propia visión, y sintetiza el contexto. Todo **local y offline**, sin claves de API.

## Tags
#youtube #coding #design #media

## Ejes temáticos
- [[youtube]]
- [[coding]]
- [[design]]

## Skills relacionadas
- [[auto-editor]]
- [[ffmpeg-toolkit]]
- [[gif-search]]
- [[video-workflow]]
- [[yt-dlp]]
- [[heartmula]]
- [[songsee]]
