---
date: 2026-07-13
type: conversation
source_agent: hermes
session_id: "20260713_174315_fa687e"
project: "tui"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, tui]
title: "Descarga de playlists y cookies yt-dlp"
---

# Descarga de playlists y cookies yt-dlp

**Fecha:** 2026-07-13  
**Agente:** hermes  
**Proyecto/contexto:** tui  
**Sesión:** `20260713_174315_fa687e`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

quiero que hagas un balance de todas mis playlist de youtube pero enfocandote en la watchlist. quiero saber que tipos de video estan etc

### Asistente

Voy a cargar la skill de YouTube para ver qué herramientas tengo disponibles para analizar tus playlists.

### Asistente

Hay varias versiones. Veamos la más completa (la del marketing-skill, que suele ser la más detallada).

### Asistente

Antes de meterme con tu cuenta, déjame revisar qué herramientas tengo disponibles localmente (esto es solo lectura de mi entorno, no toca tu cuenta).

### Asistente

Entiendo el objetivo: quiero cruzar **todas tus playlists de YouTube** y luego hacer un análisis profundo de la **watchlist** (tipos de video, temas, duración, canales, etc.).

El detalle clave es **cómo llego a tus datos**. Hay un par de situaciones reales:

- **"Watch later" (Mi lista de más tarde)** es privada por diseño de YouTube → no se puede leer solo con un link, necesita acceso autenticado a tu cuenta.
- El resto de tus playlists (si son públicas) sí se pueden leer con solo su URL.
- Para análisis de contenido (tipos de video, categorías) uso TranscriptAPI (tiene 100 créditos gratis, sin tarjeta) o `yt-dlp` local.

Antes de correr cualquier cosa, necesito que decidas el camino de acceso:

### Asistente

Quedo a la espera de tu elección. En resumen, lo que haré será:

1. **Recopilar** tus playlists (públicas vía URL, y la watchlist según el método que elijas).
2. **Extraer** el listado de videos de cada una (título, canal, duración, fecha).
3. **Analizar la watchlist** en profundidad: tipo de contenido (tutorial, noticia, entretenimiento, etc.), temas/categorías, canales más frecuentes, duración promedio, antigüedad, y cualquier patrón que encuentre.
4. **Cruzar** con el resto de playlists para ver solapamientos y darte el panorama completo.

Solo dime por cuál de las 4 opciones quieres ir y arrancamos.

### Usuario

haz todo

### Asistente

¡Perfecto, "haz todo"! Voy a ejecutar el flujo completo de forma local usando `yt-dlp` con las cookies de tu Chrome (así leo también la **Watch later** privada sin que tengas que exportar nada). Te dejo el plan y arranco.

### Asistente

La instalación salió bien (yt-dlp 2026.7.4). El `--version` se colgó raro; lo reintento por la ruta directa del binario.

### Asistente

yt-dlp funciona. Ahora extraigo la **Watch Later (WL)** usando tus cookies de Chrome. Esto puede tardar si la lista es grande, así que lo corro en background y te aviso al terminar.

### Asistente

Mientras corre la extracción de la Watch Later (puede tardar según el tamaño de tu lista), déjame intentar detectar tus otras playlists. La vía directa es que me pases las URLs, pero intento ver si hay forma de listarlas con las cookies.

Mientras, te pregunto: **¿tienes las URLs de tus otras playlists públicas a mano?** Si me las pasas ahora, paralelizo la extracción de esas y el análisis va más rápido. Si no, puedo intentar descubrirlas por tu nombre de canal/cuentas.

Déjame revisar el estado de la extracción en un momento.

### Asistente

La extracción chocó con un bloqueo real: **Chrome cifra sus cookies con protección App-Bound (DPAPI)** y yt-dlp no puede descifrarlas desde fuera del navegador. Eso impide leer la **Watch Later** privada automáticamente. No es un tema de permiso, es técnico.

Antes de pedirte un paso manual, déjame probar si tienes las cookies de YouTube en otro navegador (Edge/Firefox) que sí se puedan leer.

### Asistente

Encontré un **bloqueo técnico real** y te lo digo claro: en Windows, Chrome/Edge/Brave cifran las cookies con *App-Bound Encryption* (una capa de seguridad de Chrome 127+), y yt-dlp no puede descifrarlas desde fuera del navegador (error DPAPI conocido: yt-dlp issue #10927). Por eso no puedo leer tu **Watch Later** privada solo con las cookies. Firefox ni siquiera está instalado.

No es falta de permiso: es que el acceso automático está bloqueado por diseño del navegador. Para seguir necesito un paso manual de tu parte (o las URLs de las públicas para avanzar ya).

### Asistente

Quedo a la espera de tu elección. Mientras tanto, por si eliges la opción 2, **pásame las URLs de tus playlists públicas** y las analizo en paralelo; y si eliges la opción 1 o 4, te guío al instante a exportar las cookies para desbloquear también la Watch Later.

Para que tengas contexto del bloqueo técnico (no es permiso, es el navegador):
- Chrome/Edge/Brave en Windows cifran las cookies con *App-Bound Encryption*, y yt-dlp no puede descifrarlas desde fuera → error DPAPI (issue #10927 de yt-dlp).
- Las únicas vías limpias son: (a) exportar `cookies.txt` con la extensión **"Get cookies.txt LOCALLY"** (lee desde dentro del navegador, 2 min), o (b) Google Takeout.

Dime por cuál vamos y seguimos.

### Usuario

no se como lo vas a hacer. simplemente encuentra la mejor solucion

### Asistente

Decidido. La **mejor solución** dado el bloqueo técnico (Chrome cifra las cookies con App-Bound Encryption y yt-dlp no puede leerlas solo) es: exportar un `cookies.txt` desde dentro del navegador. Es el camino más limpio, completo (incluye la **Watch Later** privada) y rápido (2 minutos, sin instalar nada raro ni dar contraseñas).

Te dejo el pipeline armado y listo para correr en cuanto me deses el archivo. Mientras, te explico exactamente qué haces:

**Lo que tú haces (2 minutos, sin riesgo):**
1. En Chrome (donde tienes sesión en YouTube), instala la extensión **"Get cookies.txt LOCALLY"** (de suderman, la que dice LOCALLY — no manda nada a la nube).
2. Entra a **youtube.com** (con tu sesión ya abierta) y haz clic en el icono de la extensión → botón **"Export"** / "Get cookies.txt" → descarga el archivo.
3. Guárdalo en: `C:\Users\david\yt_analyzer\cookies.txt` y me dices "listo".

**Lo que yo hago en automático** en cuanto tenga el archivo:
- Leo tu **Watch Later** completa + cualquier otra playlist que me pases.
- Analizo la watchlist: tipos de video (tutorial, noticia, entretenimiento, música, etc.), temas, canales más frecuentes, duración promedio, antigüedad, y solapamientos con tus otras playlists.

Armo el pipeline ahora para que no esperes nada más.

### Asistente

Listo. El pipeline está armado y esperando tu `cookies.txt`. No puedo leer la Watch Later hasta tener ese archivo (por el bloqueo técnico de Chrome que te expliqué), así que el siguiente paso es tuyo.

**Resumen de la mejor solución que elegí:**
- Pipeline local con `yt-dlp` + `cookies.txt` exportado desde el navegador → lee todo (incluida la watchlist privada) sin exponer contraseñas ni depender de APIs de pago.
- Análisis cruzado de todas tus playlists + desglose profundo de la watchlist.

**Tu acción (2 min):**
1. Instala en Chrome la extensión **"Get cookies.txt LOCALLY"** (de suderman).
2. Entra a youtube.com con tu sesión → clic en la extensión → **Export** → descarga el `.txt`.
3. Guárdalo en `C:\Users\david\yt_analyzer\cookies.txt` y dime "listo". (Y si quieres que analice tus otras playlists también, pásame sus URLs ahora y las incluyo en el mismo paso.)

En cuanto me digas "listo", corro la extracción y te entrego el balance completo. Si prefieres otra ruta (Takeout, o solo las URLs públicas), dímelo y ajusto.

### Usuario

ya la instale pero en brave

### Usuario

listo ya lo instale pero en brave no en chrome

### Asistente

Brave es Chromium, igual funciona perfecto — lo importante es que la extensión lea las cookies **desde dentro del navegador** (que es justo lo que hace "LOCALLY"), no importa si es Brave o Chrome. El `cookies.txt` resultante sirve igual para yt-dlp.

Déjame verificar si ya guardaste el archivo en la ruta.

### Asistente

No está todavía. Haces el export en Brave y me lo dejas en la ruta. Dos formas:

**Opción A (recomendada):** En Brave, con youtube.com abierto y tu sesión iniciada → clic en el icono de "Get cookies.txt LOCALLY" → **Export** → descarga el `.txt` → muévelo/guárdalo en:
`C:\Users\david\yt_analyzer\cookies.txt`

**Opción B (si no sabes dónde cayó la descarga):** Después de exportar, dime y yo mismo lo busco en tu carpeta de Descargas y lo copio a la ruta. Por ejemplo, dame el nombre del archivo (suele ser `youtube.com_cookies.txt`).

En cuanto el archivo esté en `C:\Users\david\yt_analyzer\cookies.txt`, me dices "listo" y corro la extracción de la Watch Later + lo que me pases. ¿Quieres que también te analice tus otras playlists? Si sí, pásame sus URLs ahora para incluirlas en el mismo paso.

### Usuario

listo, puedes encontrar el txt en D:\OneDrive - unicesar.edu.co\Downloads

### Asistente

Voy a buscar el archivo en esa carpeta. Puede haber más de uno, así que listo lo que haya.

### Asistente

Lo encontré: `www.youtube.com_cookies.txt`. Lo copio a la ruta del pipeline y valido que tenga el formato Netscape correcto antes de extraer.

### Asistente

`cookies.txt` está en formato Netscape válido y lo copié al pipeline. Ahora extraigo tu **Watch Later** completa. Lo corro en background porque puede tardar según el tamaño de tu lista.

### Asistente

Sigue corriendo (la Watch Later puede ser grande). Espero un poco más.

### Asistente

¡Excelente! Extraje tu **Watch Later completa: 1.578 videos**. Ahora la analizo en profundidad (tipos, temas, canales, duración, antigüedad). También necesito tus otras playlists para el cruce — pero primero dejo el análisis de la watchlist corriendo y reviso si encuentro pistas de tus otras playlists.

Arranco el análisis de la watchlist ya.

### Asistente

Tengo los datos duros: **1.578 videos, 609,8 horas de contenido, promedio 23,2 min por video**. Pero la clasificación por palabras clave quedó muy floja (68% "Otro") y faltan fechas. Voy a mejorarla usando el perfil de cada canal (midudev, Fazt, Veritasium, TwoSetViolin, etc. son claramente de un tipo) y un léxico más amplio en ES+EN. Primero inspecciono qué campos trae cada video para enriquecer.

### Asistente

Buenas noticias: hay campo `timestamp`/`release_timestamp` (para fechas) y `description` (para clasificar mejor). Y el perfil de canal es muy fuerte (rubius→gaming/entretenimiento, midudev/Fazt→tech, Veritasium→ciencia). Mejoro el análisis con: (1) mapeo de canales conocidos por categoría, (2) léxico ampliado ES+EN usando título+descripción, (3) fechas reales.

### Asistente

Mejoró bastante (bajó de 68% a 51% "Otro"). Pero quiero caracterizar mejor ese 51% y entender los 51 videos "??" (sin canal). Hago un pase extra con frecuencia de palabras (temas reales) y mapeo más canales.

### Asistente

Ahora el cuadro se aclara mucho. Las palabras frecuentes revelan lo que el clasificador inicial perdía: un gran cluster de **música cristiana (Álvaro Torres: 35 menciones)**, **ajedrez** (Magnus Carlsen), **anime** (Blue Lock), **hacking/seguridad** (Kali Linux), y **política/noticias** (Venezuela). Hago el pase final para encasillar bien eso y los videos eliminados/privados.

### Asistente

Tengo el análisis completo de la watchlist. Antes de redactar, saco dos cifras más para el reporte (canales distintos totales y concentración).

### Asistente

¡Listo! Analicé tu **Watch Later completa** (la extracción funcionó con las cookies de Brave). Aquí el balance.

> ⚠️ Nota honesta: solo pude analizar la **Watch Later** porque no me pasaste las URLs de tus *otras* playlists. El cruce con el resto queda pendiente — pásame esas URLs y lo hago en el mismo formato. Aun así, la watchlist sola ya da un perfil muy claro.

---

## 📊 Balance de tu Watch Later

**Volumen:** 1.578 videos · **609,8 horas** de contenido (~25 días viéndolo sin parar) · promedio **23,2 min**, mediana **13,4 min**.
**Limpieza:** 10 videos eliminados + 15 privados = 25 ya no disponibles (1.553 analizables).
**Fuentes:** 1.159 canales distintos, pero **989 canales aparecen con UN solo video** → tu lista es una cola-larga gigante de intereses dispersos, no un puñado de canales fijos.

### ⏱️ Distribución por duración
- 5–15 min: **707** (45%)
- 15–30 min: **439** (28%)
- 1–5 min: 129 · 30–60 min: 163 · >60 min: **107** (videos largos, charlas/conferencias) · <1 min: 33

### 🏷️ Tipos de contenido (clasificación por canal + texto ES/EN)
| Categoría | Videos | % |
|---|---|---|
| Tech / Programación | 224 | 14,2% |
| Tutorial / How-to | 195 | 12,4% |
| Ciencia / Educación | 131 | 8,3% |
| Música | 88 | 5,6% |
| Entretenimiento / Gaming | 57 | 3,6% |
| Religión (música cristiana, Álvaro Torres) | 44 | 2,8% |
| Deportes (fútbol, Davoo) | 32 | 2,0% |
| Noticias / Actualidad | 26 | 1,6% |
| Ajedrez | 21 | 1,3% |
| Anime | 18 | 1,1% |
| Seguridad / Hacking | 10 | 0,6% |
| Negocios / Finanzas | 8 | 0,5% |
| **Otro / sin clasificar** | **715** | **45,3%** |

El 45% "Otro" es real: es la cola-larga de 989 canales únicos. Pero al mirar las **palabras más frecuentes en títulos**, el perfil se afina:

- **Álvaro Torres** (35 menciones) + "pastor/predicador/IPUC" → bloque grande de **música cristiana/adoración**.
- **IA / dev**: "Claude Code vs Codex", "Large Language Models", "Why Python Can't Find Your File", "Funciones de activación (Redes neuronales)" → sigues muy metido en **IA y programación**.
- **Ajedrez**: Magnus Carlsen, "Blue Lock" (anime), "Kali Linux" / hacking → nichos claros.
- **Ciencia/mates**: "The Language of Calculus", "Computer Science", "historia completa", "cómo funciona".
- **Política/noticias**: Venezuela, mundial 2026, Manchester United.

### 🎯 Perfil que se deduce de tu watchlist
Eres **perfil dev/tech con hambre de aprendizaje**: programación, IA y tutoriales son el núcleo duro (~27% combinado). Alrededor giran **ciencia/educación (TED-Ed, Veritasium, Kurzgesagt)**, **música variada** (clásica/jazz con TwoSetViolin, Jacob Collier, Rick Beato + cristiana con Álvaro Torres), y un entretenimiento ligero (rubius, midulive). Tienes también **nichos pequeños pero definidos**: ajedrez, anime, seguridad/hacking y fútbol.

**Top canales:** midulive (15), EZ (13), midudev (13), Fazt (12), Sé Curioso–TED-Ed (11), WIRED (9), Predicador Unicitario (9), Davoo Xeneize (8), Fireship (8).

---

### 🔧 Limitaciones reales (para que sepas qué tan sólido es)
1. **Fechas:** la Watch Later no expone la fecha de subida en la extracción plana, así que **no pude medir antigüedad/recencia** ni decir "qué tan vieja está la lista". Si quieres eso, hay que extraer con metadata completa (más lento).
2. **45% sin clasificar:** es cola-larga legítima, no un fallo del script. Si quieres, puedo bajar ese % mapeando más canales o leyendo descripciones completas.
3. **Otras playlists:** pendientes de URLs para el cruce que pediste.

¿Quieres qu

_[truncado]_


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
