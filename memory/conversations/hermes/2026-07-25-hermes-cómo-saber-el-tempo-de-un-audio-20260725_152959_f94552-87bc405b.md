---
date: 2026-07-25
type: conversation
source_agent: hermes
session_id: "20260725_152959_f94552"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Cómo saber el tempo de un audio"
---

# Cómo saber el tempo de un audio

**Fecha:** 2026-07-25  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260725_152959_f94552`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

como puedo saber el tempo de un audio?

### Asistente

Hay varias formas, de la más fácil a la más técnica:

**1. Online (sin instalar nada)**
- [tunebat.com](https://tunebat.com) — subes el audio y te da BPM + key.
- [songbpm.com](https://songbpm.com) — buscas por nombre o subes archivo.

**2. Audacity (gratis, escritorio)**
- `Analizar → Find beats...` (o el efecto *Tempo* en versiones nuevas). No es perfecto pero sirve para música clara.

**3. Línea de comandos con `aubio` (lo más preciso y rápido)**
```bash
pip install aubio
aubio tempo archivo.mp3
```
Devuelve el BPM estimado directamente.

**4. Python con `librosa` (si quieres control total / scripting)**
```python
import librosa
y, sr = librosa.load("archivo.mp3")
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
print(tempo)
```

**5. En tu DAW** (Ableton, FL Studio, Reaper): todos tienen detección de tempo automática al importar el audio.

---

Si quieres, **yo te lo analizo aquí mismo**: dime la ruta del archivo (mp3/wav/ogg) y lo proceso con `aubio` o `librosa` y te digo el BPM exacto. ¿Tienes el archivo a mano?

### Usuario

y como pued saber los acordes de un audio?

### Asistente

Para detectar **acordes** (no solo el tempo) ya entras en análisis de armonía. Las opciones:

**1. Online (rápido, sin instalar)**
- [moises.ai](https://moises.ai) — sepара pistas y muestra acordes en tiempo real (freemium).
- [chordai.app](https://chordai.app) — app móvil/escritorio que detecta acordes y tempo juntos.
- [tunebat.com](https://tunebat.com) — además de BPM da la tonalidad (key), no los acordes exactos.

**2. Python con `librosa` (lo más común para scripting)**
Librosa no da acordes directos, pero sí la ** tonalidad/key** y el chroma. Para acordes completos se suele combinar con un modelo:
```python
import librosa
y, sr = librosa.load("archivo.mp3")
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
# el chroma se pasa a un clasificador de acordes (p.ej. librosa + plantillas)
```

**3. `madmom` (Python, especializado en música)**
Bueno para beat y downbeats; para acordes mejor el siguiente.

**4. `crepe` / `basic-pitch` (deep learning)**
- **basic-pitch** (de Spotify) da notas con timestamps → de ahí infieres acordes.
```bash
pip install basic-pitch
basic-pitch archivo.mp3   # genera CSV de notas
```

**5. El estándar real: `chord-recognition` / `mir_eval` + modelos entrenados**
El mejor open-source para acordes es usar un modelo de plantillas sobre el chroma (algoritmo de Temperley/Harte). Hay scripts listos, pero requieren armado.

**6. En tu DAW**
Ableton Live, FL Studio y Reaper tienen detección de acordes al importar audio (Ableton `Audio → Detect Key & Scale`, Reaper `Dynamic Split` + extensión de chords).

---

**Realidad:** la detección de acordes es menos precisa que la de tempo. Para música con batería/pista completa falla más; para piano/guitarra sola acústica es bastante buena.

**Yo te lo puedo hacer aquí:** si me das la ruta del archivo (mp3/wav), lo proceso con `librosa` + un clasificador de acordes (o `basic-pitch` para notas) y te entrego una lista de acordes por segmento de tiempo. ¿Quieres que lo haga? Si sí, dime la ruta y si prefieres **acordes por sección** o **notas crudas con timestamps**.


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
