# Rediseño "tech keynote" de som-taller-1-4

## Context

El proyecto `D:\Github repos\som-taller-1-4\web` ya tiene 25 slides funcionales que cubren correctamente los 8 pasos metodológicos del taller SOM (Problema 1 — Estudiantes, indigo; Problema 4 — Smart Cities, amber), con datos reales, entrenamiento SOM en vivo, U-Matrix, planos de componentes, PCA y notas de presentador (tareas #1-27, todas completadas y verificadas).

El usuario pidió ahora **olvidar la normativa original como restricción de diseño** y repensar, slide por slide, **cómo exponer cada punto de la mejor manera posible**, llevando la presentación a nivel "tech keynote" (estilo Apple/OpenAI), incorporando explícitamente:
- Reutilización de la animación de red SOM (`SOMCanvas`, de `som-presentation/src/slides/01_TitleSlide.jsx`) para portadas (general, P1, P4)
- Visualización 3D del entrenamiento SOM
- Visualización interactiva de la red/topología
- Gráficas animadas y "planos interactivos"
- Texto en pantalla más cuidado/minimalista
- Estructura de slides rediseñada con criterio narrativo

**Enfoque elegido:** en vez de descartar el contenido y los cálculos ya verificados (que son correctos y obligatorios para la sustentación académica), el rediseño es una **renovación del lenguaje visual y narrativo de cada slide**: nuevos componentes "hero" reutilizables (fondo de red SOM, contador animado, stepper metodológico, reveals escalonados), una visualización 3D real del entrenamiento, una topología de red interactiva, y 2 portadas nuevas por problema. El cálculo subyacente (`lib/som.js`, `lib/stats.js`, `useP1Analysis`/`useP4Analysis`) se reutiliza tal cual.

## Nuevos componentes compartidos (Fase A)

1. **`components/ui/SOMNetworkBackground.jsx`** — extracción/parametrización de `SOMCanvas` (`som-presentation/src/slides/01_TitleSlide.jsx:5-173`): mismo sistema de grilla + interpolación bilineal de 4 esquinas + ripples + glow, pero recibe `corners` (array de 4 RGB), `cols`/`rows` y `opacity` como props. Paletas:
   - General/Título: 4 esquinas mezclando indigo/amber/violet/emerald (look "dual" del taller completo)
   - P1: esquinas en tonos indigo/violet (`[99,102,241]`, `[129,140,248]`, `[167,139,250]`, `[79,70,229]`)
   - P4: esquinas en tonos amber/emerald (`[245,158,11]`, `[251,191,36]`, `[16,185,129]`, `[217,119,6]`)

2. **`components/ui/Reveal.jsx`** — wrapper con el helper `fadeUp(delay, y, blur)` (de `01_TitleSlide.jsx:176-182`), prop `delay`/`index` para stagger automático de listas de cards/bullets.

3. **`components/ui/AnimatedNumber.jsx`** — usa `framer-motion` `useSpring`/`useTransform` sobre `motion.span` para animar un número entero/decimal desde 0 hasta `value` cuando entra en viewport (`whileInView` o trigger por cambio de slide). Props: `value`, `decimals`, `suffix`, `duration`.

4. **`components/ui/MethodologyStepper.jsx`** — fila de 8 pasos (Comprensión → Conclusiones) con el paso activo resaltado, themed indigo/amber vía prop `accent`. Se usa en las nuevas portadas P1/P4 y opcionalmente en una slide de agenda.

5. **`lib/stats.js`**: añadir `pca3(data)` — generaliza `pca2` (power iteration + deflación) a 3 componentes, reutilizando la misma lógica de iteración. Necesario para la visualización 3D.

6. **Nueva dependencia**: `three`, `@react-three/fiber`, `@react-three/drei` (añadir a `web/package.json` + `npm install`). Es la opción recomendada para la viz 3D real (vs. una pseudo-3D CSS/SVG isométrica, que sería más liviana pero no cumple "visualización 3D" de forma literal y es mucho más limitada para mostrar el plegado del mapa SOM sobre la nube de datos).

7. **`components/viz/SOM3DTrainer.jsx`** — escena react-three-fiber:
   - Calcula `pca3(normalized)` una vez (ejes fijos) → nube de puntos (datos) como `<Points>`/instancedMesh.
   - En cada frame de entrenamiento (reusando `createSOMTrainer`/`step(batch)` de `lib/som.js`, igual que `SOMTrainerPanel`), proyecta los pesos actuales de las neuronas sobre los **mismos ejes PCA** → posiciones 3D de las neuronas.
   - Dibuja líneas entre neuronas vecinas de la grilla (forma la "malla" SOM plegándose sobre la nube de datos a medida que entrena — la visual clásica y más demostrativa de un SOM).
   - Color de cada neurona según U-Matrix (heatmap) o cluster.
   - `OrbitControls` (drag para rotar/zoom), auto-rotación lenta cuando no hay interacción.
   - Panel lateral compacto con QE/lr/σ/iteración + controles ▶/⏸/↺ (mismo patrón que `SOMTrainerPanel.jsx:96-145`).

8. **`components/viz/NetworkTopology.jsx`** — diagrama SVG interactivo (usa `ZoomableSVG.jsx` existente) de la grilla de neuronas como red de nodos conectados a sus 4 vecinos: tamaño/color de nodo = nº de muestras asignadas (BMU) o cluster, hover muestra tooltip con perfil/cluster y conteo. Sustituye/enriquece la visualización actual de `p1_07_ClustersSlide`/`p1_07b_WinnerMapSlide`.

## Rediseño de slides (Fase B en adelante)

### Portadas con `SOMNetworkBackground` (Fase B)
- **`00_TitleSlide.jsx`**: añadir `SOMNetworkBackground` (paleta dual) detrás del contenido actual, aplicar `Reveal`/`fadeUp` a badge/título/subtítulo/autor (mismo patrón que `01_TitleSlide.jsx:209-292`), añadir `MethodologyStepper` o mini-agenda como elemento final.
- **Nueva `p1_00_CoverSlide.jsx`** (se inserta antes del actual `p1_00_ContextSlide`): `SOMNetworkBackground` con paleta indigo, título "Problema 1 — Segmentación de Estudiantes", 3 `AnimatedNumber` KPIs (1200 estudiantes, 12 variables, grilla 10×10), `MethodologyStepper accent="indigo"` paso 1 activo.
- **Nueva `p4_00_CoverSlide.jsx`**: igual con paleta amber, "Problema 4 — Smart Cities", KPIs (800 municipios, 12 indicadores, grilla 8×8), stepper amber.
- `p1_00_ContextSlide.jsx`/`p4_00_ContextSlide.jsx` actuales pasan a ser la 2ª slide de cada bloque (contenido igual, solo se aligera con `Reveal` en los bullets de "¿Por qué un SOM?").

### Visualización 3D del entrenamiento (Fase C)
- `p1_06_SOMSlide.jsx`/`p4_06_SOMSlide.jsx`: reemplazar `SOMTrainerPanel` por `SOM3DTrainer` (mismo `useTrainedSOM`/`somStore` para que el resultado siga alimentando las slides de interpretación posteriores). Mantener los `Pill` de configuración (lr, σ, iteraciones, grilla) arriba.

### Topología de red interactiva (Fase D)
- `p1_07_ClustersSlide.jsx`/`p4_07_ClustersSlide.jsx` y/o `p1_07b_WinnerMapSlide.jsx`/`p4_07b_WinnerMapSlide.jsx`: añadir `NetworkTopology` como visualización principal (junto a U-Matrix), con `ZoomableSVG` ya existente para pan/zoom.

### Pulido animado transversal (Fase E)
- Reemplazar números estáticos clave por `AnimatedNumber` en: slide de datos/EDA (shape, nulos=0), Winner Map (`stats.total/active/empty/max`), Conclusiones (KPIs de cierre).
- Envolver listas de bullets/cards (ej. "¿Por qué un SOM?", "Topología del mapa", conclusiones) con `Reveal` para entrada escalonada al cambiar de slide.

### Actualización de navegación (Fase F)
- `App.jsx`: insertar las 2 nuevas portadas (`p1_00_CoverSlide`, `p4_00_CoverSlide`) en `SLIDES` con `kicker`/`title`/`notes` propios (25 → 27 slides). Verificar que el contador "N/27", progress ring y dots se ajusten automáticamente (derivados de `SLIDES.length`).

## Verificación (Fase G)
1. `npm run dev` en `web/` (ya corriendo en preview, serverId conocido).
2. Navegar las 27 slides con `ArrowRight`/dots, confirmar:
   - Las 3 portadas muestran la animación de red SOM con la paleta correcta y sin caída de FPS notoria.
   - `SOM3DTrainer` entrena, anima la malla plegándose sobre la nube PCA-3D, OrbitControls responde a drag, y al completar sigue poblando `somStore` (slides de interpretación P1/P4 siguen funcionando con los mismos pesos).
   - `NetworkTopology` responde a hover/zoom y los datos coinciden con `useP1Analysis`/`useP4Analysis`.
   - `AnimatedNumber`/`Reveal` no rompen layout ni causan overflow.
   - Sin errores en consola (`preview_console_logs` tras reload).
3. Notas de presentador (`slide.notes`) revisadas/ajustadas para las 2 portadas nuevas.
