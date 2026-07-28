---
date: 2026-05-26
type: conversation
source_agent: claude-code
session_id: "agent-a7e6b273aba2f2f07"
project: "subagents"
source_path: "C:\\Users\\david\\.claude\\projects\\D--OneDrive---unicesar-edu-co-davidbarce0411-g-UPC-Semester-VII-Artificial-Intellligence\\2523e285-8222-4ee2-bc34-f66925ccab42\\subagents\\agent-a7e6b273aba2f2f07.jsonl"
tags: [conversation, imported, claude-code]
title: "Build a complete, spectacular web presentation app about \"Métricas de Evaluación de Mapas"
---

# Build a complete, spectacular web presentation app about "Métricas de Evaluación de Mapas 

**Fecha:** 2026-05-26  
**Agente:** claude-code  
**Proyecto/contexto:** subagents  
**Sesión:** `agent-a7e6b273aba2f2f07`  
**Origen:** `C:\Users\david\.claude\projects\D--OneDrive---unicesar-edu-co-davidbarce0411-g-UPC-Semester-VII-Artificial-Intellligence\2523e285-8222-4ee2-bc34-f66925ccab42\subagents\agent-a7e6b273aba2f2f07.jsonl`

## Mensajes

### Usuario

Build a complete, spectacular web presentation app about "Métricas de Evaluación de Mapas de Kohonen (SOM)".

## Project location
Create ALL files inside:
`D:\OneDrive - unicesar.edu.co\davidbarce0411@g\UPC\Semester VII\Artificial Intellligence\Cut 3\som-presentation`

First run: `mkdir "D:\OneDrive - unicesar.edu.co\davidbarce0411@g\UPC\Semester VII\Artificial Intellligence\Cut 3\som-presentation"` to create the directory.

## Tech Stack
- Vite + React 18
- @react-three/fiber + @react-three/drei + three (3D)
- framer-motion (slide transitions + reveals)
- d3 (scatter plots, viz)
- katex + react-katex (math formulas)
- Tailwind CSS (styling)
- gsap (optional for number counters)

## Design System
Premium dark cosmic theme:
- Background: `#04040f` (near-black)
- Surface: `#0d0d2b`
- Card: `#13133a`
- Border: `rgba(99,102,241,0.25)`
- Primary: `#6366f1` (indigo)
- Secondary: `#8b5cf6` (violet)
- Accent: `#f59e0b` (amber)
- Class A: `#10b981` (emerald)
- Class B: `#f43f5e` (rose)
- Dead neuron: `#475569` (slate)
- Text: `#f1f5f9`
- Muted: `#94a3b8`

All slides are fullscreen (100vw x 100vh). Slide transitions: horizontal slide with Framer Motion AnimatePresence. Keyboard nav: ← →, Space. Show slide counter "X / 16" bottom-right, progress bar bottom.

## Example Data (use exactly these numbers throughout ALL example slides)

### Neurons (SOM 2×2 after training):
```
N1: grid(0,0), weights=[0.15, 0.20], label=A, color=#10b981
N2: grid(1,0), weights=[0.80, 0.85], label=B, color=#f43f5e
N3: grid(0,1), weights=[0.55, 0.45], label=B, color=#f43f5e (tie → B)
N4: grid(1,1), weights=[0.30, 0.60], label=null (DEAD NEURON), color=#475569
```

### Samples:
```
m1: x1=0.1, x2=0.2, class=A, BMU=N1, dist=0.050, correct=true
m2: x1=0.2, x2=0.1, class=A, BMU=N1, dist=0.112, correct=true
m3: x1=0.1, x2=0.3, class=A, BMU=N1, dist=0.112, correct=true
m4: x1=0.8, x2=0.9, class=B, BMU=N2, dist=0.050, correct=true
m5: x1=0.9, x2=0.8, class=B, BMU=N2, dist=0.112, correct=true
m6: x1=0.7, x2=0.9, class=B, BMU=N2, dist=0.112, correct=true
m7: x1=0.5, x2=0.5, class=A, BMU=N3, dist=0.071, correct=false ← MISCLASSIFIED
m8: x1=0.6, x2=0.4, class=B, BMU=N3, dist=0.071, correct=true
```

### Calculated metrics:
- QE = 0.086
- Purity = 87.5% (7/8)
- Entropy N1 = 0 (pure A), N2 = 0 (pure B), N3 = 1.0 (50/50 mix)
- Confusion matrix: Real A vs Pred A=3, Real A vs Pred B=1, Real B vs Pred A=0, Real B vs Pred B=4
- Accuracy = 87.5%
- Precision(A) = 1.00, Recall(A) = 0.75, F1(A) = 0.857
- Precision(B) = 0.80, Recall(B) = 1.00, F1(B) = 0.889

## Files to Create

### 1. `package.json`
```json
{
  "name": "som-metrics-presentation",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "@react-three/fiber": "^8.17.10",
    "@react-three/drei": "^9.117.3",
    "three": "^0.169.0",
    "framer-motion": "^11.12.0",
    "d3": "^7.9.0",
    "katex": "^0.16.11",
    "react-katex": "^3.0.1",
    "gsap": "^3.12.5"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.7",
    "tailwindcss": "^3.4.17",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.5.1"
  }
}
```

### 2. `vite.config.js`
Standard Vite React config.

### 3. `tailwind.config.js`
Extend theme with custom colors (bg-deep, surface, card, primary, secondary, accent, classA, classB). Set content to `['./index.html','./src/**/*.{js,jsx}']`.

### 4. `postcss.config.js`
Standard tailwind + autoprefixer.

### 5. `index.html`
Mount to `#root`. Import `katex/dist/katex.min.css`. Set title "SOM — Métricas de Evaluación". Dark background in body style.

### 6. `src/main.jsx`
Standard React 18 createRoot.

### 7. `src/index.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --bg-deep: #04040f;
  --bg-surface: #0d0d2b;
  --bg-card: #13133a;
  --primary: #6366f1;
  --secondary: #8b5cf6;
  --accent: #f59e0b;
  --class-a: #10b981;
  --class-b: #f43f5e;
}

body {
  background: var(--bg-deep);
  color: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

/* Glow utilities */
.glow-indigo { box-shadow: 0 0 20px rgba(99,102,241,0.4); }
.glow-emerald { box-shadow: 0 0 20px rgba(16,185,129,0.4); }
.glow-rose { box-shadow: 0 0 20px rgba(244,63,94,0.4); }

/* Formula highlight classes */
.formula-primary { color: #6366f1; }
.formula-accent { color: #f59e0b; }
.formula-a { color: #10b981; }
.formula-b { color: #f43f5e; }
```

### 8. `src/data/somData.js`
Export all the example data as constants: `neurons`, `samples`, `QE`, `purity`, `confusionMatrix`, `metrics`.

### 9. `src/App.jsx`
Presentation controller:
- State: `currentSlide` (0-15), `direction` (+1 or -1 for transition direction)
- Import all 16 slide components
- Array of slide objects: `{ component, title, part }`
- useEffect for keyboard listeners (ArrowLeft, ArrowRight, Space)
- Render: AnimatePresence with slide transition variants (x: '100%'→0→'-100%')
- Bottom: progress bar (indigo, width = (currentSlide+1)/16 * 100%)
- Bottom right: slide counter "1 / 16"
- Bottom left: current slide title in small muted text
- Top: part indicator badge (Parte 1 / Parte 2 / Parte 3)

Slide transition variants:
```js
const variants = {
  enter: (dir) => ({ x: dir > 0 ? '100%' : '-100%', opacity: 0 }),
  center: { x: 0, opacity: 1, transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] } },
  exit: (dir) => ({ x: dir < 0 ? '100%' : '-100%', opacity: 0, transition: { duration: 0.4 } }),
}
```

### 10. `src/components/som/SOMGrid3D.jsx`
React Three Fiber 3D visualization of the SOM.

```jsx
// Canvas with:
// - Black background with Stars (from drei)
// - OrbitControls (from drei) - autoRotate, enableZoom=false
// - 4 Neuron spheres at:
//   N1: (-2, 2, 0)   N2: (2, 2, 0)
//   N3: (-2, -2, 0)  N4: (2, -2, 0)
// - Each neuron: <mesh>
//   - sphereGeometry args={[0.35, 32, 32]}
//   - meshStandardMaterial color={neuron.color} emissive={neuron.color} emissiveIntensity={0.6}
//   - If dead (N4): emissiveIntensity=0.1, opacity=0.4
//   - Animated: useFrame to pulse scale (Math.sin(clock.elapsedTime * 1.5) * 0.05 + 1)
// - Neuron labels: <Text> from drei showing "N1\n[A]" etc
// - Grid connections: <Line> from drei between adjacent neurons (N1-N2, N1-N3, N2-N4, N3-N4)
//   color: rgba(99,102,241,0.5), lineWidth=1.5
// - Data points as small spheres (radius 0.12) at scaled positions:
//   Map x1,x2 from [0,1] to [-3.5,3.5]
//   Class A: #10b981, Class B: #f43f5e
// - Ambient light + directional lights
// - pointLight at each neuron position with color
// Accept props: { showDataPoints = true, animatePulse = true, showLabels = true }
```

### 11. `src/components/som/BMUScatter.jsx`
D3-based scatter plot with step-by-step BMU animation.

Props: `{ step }` — from 0 (show just points) to 8 (all BMUs assigned)

```jsx
// useRef for SVG, useEffect to render
// 400x400 SVG with padding 50
// Scales: x,y from [0,1] to [0,300]
// 
// Render neurons as diamond shapes (♦) at their weight positions
//   colored by label
// 
// Render samples as circles (r=8) colored by class
//   Labeled with their id (m1, m2, etc.)
//
// For step N: show sample m(N) highlighted with a ring
//   Show dashed distance lines from m(N) to ALL 4 neurons
//   Line to BMU neuron: solid, colored, thick
//   Line to others: dashed, muted
//   Show distance label on each line
//
// Animate with framer-motion (lines appear with pathLength animation)
// After all steps: show all BMU assignments as colored arcs/arrows
```

### 12. `src/components/metrics/FormulaBlock.jsx`
Animated formula reveal component.

Props: `{ steps }` — array of `{ latex, label, color, delay }`

```jsx
// Each step is a row: colored label + KaTeX formula
// Steps appear one by one with framer motion (opacity 0→1, y 10→0)
// Each step has a left colored border matching the step color
// Use InlineMath or BlockMath from react

_[truncado]_

### Usuario

[tool_result]

### Asistente

I'll create all the files for this spectacular SOM metrics presentation. Let me start by creating the directory and all the files systematically.

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Asistente

Now let me create the component files:

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Asistente

You've hit your session limit · resets 11:30am (America/Bogota)


## Enlaces
- Índice: [[claude-code-import-index]]
- Home: [[Home]]
