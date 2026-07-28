---
date: 2026-06-10
type: conversation
source_agent: cursor
session_id: "1c02402d-65b8-4293-9069-2b9235141dc7"
project: "d-Github-repos-captus-web"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-captus-web\\agent-transcripts\\1c02402d-65b8-4293-9069-2b9235141dc7\\1c02402d-65b8-4293-9069-2b9235141dc7.jsonl"
tags: [conversation, imported, cursor]
title: "dime segun el documento proyecto de aula captus, que herramientas se usaron para cada prue"
---

# dime segun el documento proyecto de aula captus, que herramientas se usaron para cada prue

**Fecha:** 2026-06-10  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-captus-web  
**Sesión:** `1c02402d-65b8-4293-9069-2b9235141dc7`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-captus-web\agent-transcripts\1c02402d-65b8-4293-9069-2b9235141dc7\1c02402d-65b8-4293-9069-2b9235141dc7.jsonl`

## Mensajes

### Usuario

dime segun el documento proyecto de aula captus, que herramientas se usaron para cada prueba

### Asistente

Revisando el documento del proyecto Captus para identificar qué herramientas se usaron en cada prueba.


[tool:Glob]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Read]
[tool:Shell]

### Asistente

El texto extraído parece incompleto; voy a leer el `.docx` directamente para localizar las secciones de pruebas.


[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Grep]
[tool:Shell]

### Asistente

[tool:Read]

### Asistente

[tool:Await]

### Asistente

[tool:Read]

### Asistente

Según el documento **PROYECTO DE AULA - CAPTUS**, las herramientas quedan así por tipo y por prueba ejecutada:

---

## Resumen por tipo de prueba (sección 2.2.2 – Planificación)

| Tipo de prueba | Herramientas definidas en el plan |
|---|---|
| **Unitarias** | **Vitest** + **React Testing Library** |
| **Integración** | **Vitest** + **React Testing Library**, APIs simuladas del proyecto y diagramas UML de secuencia |
| **Sistema** | **OWASP ZAP**, **Lighthouse / PageSpeed Insights**, **BrowserStack** |
| **Aceptación** | **Cuestionarios y listas de verificación** (opinión del usuario final) |

El ambiente de pruebas (2.2.4) también menciona **Postman**, **Jest**, **OWASP ZAP**, **Lighthouse** y **BrowserStack**, aunque en la ejecución documentada no todas se usan igual.

---

## 2.3 – Pruebas unitarias (ejecutadas)

| Módulo | Componente | Herramienta |
|---|---|---|
| Gestión de tareas | `TaskForm.jsx` | **Vitest + React Testing Library** |
| Calendario académico | `calendarUtils.js` | **Vitest** |
| Gestión de materias | `ManageSubjectsDialog.jsx` | **Vitest + React Testing Library** |

Técnica aplicada: **caja negra** (clases de equivalencia y valores límite).

---

## 2.4 – Pruebas de integración (ejecutadas)

Todas usan **Vitest + React Testing Library**, con APIs simuladas:

| Módulo | Casos | Herramienta |
|---|---|---|
| Gestión de tareas | INT01–INT06 | Vitest + React Testing Library |
| Gestión de eventos | INT-EVT01–INT-EVT06 | Vitest + React Testing Library |
| Gestión de materias | INT-SUB01–INT-SUB06 | Vitest + React Testing Library |
| Calendario académico | INT-CAL01–INT-CAL05 | Vitest + React Testing Library |
| Pruebas basadas en hilos | T001, E001, M001 | Vitest + React Testing Library (flujos completos) |

**Postman** aparece en el ambiente planificado, pero en la ejecución documentada la integración se hizo con Vitest y mocks, no con Postman.

---

## 2.5 – Pruebas de sistema (ejecutadas)

### Seguridad (SEG01–SEG05)

| Caso | Herramienta real usada |
|---|---|
| SEG01 – Campos obligatorios en login | **Navegador web** + validaciones del formulario (prueba **manual**) |
| SEG02 – Credenciales incorrectas | **Navegador web** (manual) |
| SEG03 – Rutas protegidas | **Navegador web** (manual) |
| SEG04 – Registro con datos inválidos | **Navegador web** (manual) |
| SEG05 – Longitud mínima de contraseña | **Navegador web** (manual) |

**OWASP ZAP** está en el plan de sistema, pero en estas pruebas de seguridad funcionales se usó el navegador, no ZAP.

### Rendimiento (REN01–REN05)

| Caso | Herramienta |
|---|---|
| REN01 – Login | **Apache JMeter 5.6.3** |
| REN02 – Panel principal | **Apache JMeter 5.6.3** |
| REN03 – Registro de usuarios | **Apache JMeter 5.6.3** |
| REN04 – Calendario | **Apache JMeter 5.6.3** |
| REN05 – Módulo de tareas | **Apache JMeter 5.6.3** |

### Usabilidad (USA01–USA05)

| Caso | Herramienta |
|---|---|
| USA01 – Inicio de sesión | **Google Lighthouse** (Chrome DevTools) |
| USA02 – Panel principal | **Google Lighthouse** (Chrome DevTools) |
| USA03 – Módulo de tareas | **Google Lighthouse** (Chrome DevTools) |
| USA04 – Calendario académico | **Google Lighthouse** (Chrome DevTools) |
| USA05 – Módulo de cursos | **Google Lighthouse** (Chrome DevTools) |

### Portabilidad (POR01)

| Herramienta | Uso |
|---|---|
| **Google Chrome** | Navegación manual por Home, Tareas y Calendario |
| **Microsoft Edge** | Misma verificación comparativa |
| **Safari iOS** | Aparece en resultados de compati

_[truncado]_

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

Revisé el documento **PROYECTO DE AULA - CAPTUS** y extraje las herramientas por tipo de prueba.

**Lo principal:**
- **Unitarias e integración:** Vitest y React Testing Library (con APIs simuladas en integración).
- **Sistema — rendimiento:** Apache JMeter 5.6.3 (REN01–REN05).
- **Sistema — usabilidad:** Google Lighthouse en Chrome DevTools (USA01–USA05).
- **Sistema — seguridad:** pruebas manuales en navegador (SEG01–SEG05), no OWASP ZAP en la ejecución documentada.
- **Portabilidad:** Google Chrome y Microsoft Edge (navegación manual).
- **Aceptación:** planificadas con cuestionarios y listas de verificación, pero sin sección ejecutada en el documento.

**Diferencia plan vs. ejecución:** en la planificación aparecen Jest, Postman, OWASP ZAP y BrowserStack; en lo ejecutado predominan Vitest, JMeter, Lighthouse y navegadores reales.

### Usuario

okey ahora la tercera y cuarta parte

### Asistente

Revisando las partes 3 y 4 del documento Captus para resumir herramientas, métricas y estimaciones.


[tool:Shell]

### Asistente

[tool:Shell]
[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

Aquí va el resumen de las **partes 3 y 4** del documento, con el mismo enfoque que en la sección de pruebas.

---

## Parte 3 — Medición del software

### Objetivo general
Medir la calidad de CAPTUS con métricas **internas** (código, tamaño, complejidad) y **externas** (ISO/IEC 25010: usabilidad, seguridad, rendimiento, etc.).

### 3.1.3 — Herramientas y modelos de medición

| Modelo / herramienta | Para qué se usa |
|---|---|
| **CLOC** | Conteo de líneas de código por lenguaje |
| **SonarQube** | Análisis estático: LOC, mantenibilidad, seguridad, duplicación, complejidad, fiabilidad |
| **Puntos de Función (PF)** | Tamaño funcional independiente de tecnología |
| **Puntos de Casos de Uso (UCP)** | Esfuerzo según casos de uso y actores |
| **Puntos de Objetos (OP)** | Pantallas, informes y componentes de interfaz |
| **Puntos de Historia (SP)** | Esfuerzo ágil del equipo |
| **Google Lighthouse** | Rendimiento web (FCP, LCP, Speed Index) |
| **OWASP ZAP** | Seguridad dinámica de la aplicación web |
| **Selenium** | Usabilidad funcional automatizada |

---

### 3.2 — Atributos internos

#### 3.2.1 Tamaño del código (LOC)

| Medición | Herramienta | Resultado |
|---|---|---|
| Frontend | **CLOC** | JSX 15.916, JS 1.743, CSS 855 → **19.105 LOC** |
| Backend | **CLOC** | JS 16.696 → **18.065 LOC** |
| Total full stack | **CLOC** | **35.210 NCLOC** / 37.170 LOC |
| Solo frontend | **SonarQube** | **17.000 LOC**, duplicación 2,2 %, rating **A** en mantenibilidad y seguridad |

#### 3.2.2 Métricas orientadas a clases

| Herramienta | Qué mide |
|---|---|
| **SonarQube** | WMC, DIT, CBO y cohesión de componentes (NotesPage, TaskPage, CalendarPage, etc.) |

Complejidad ciclomática total: **2.656**.

#### 3.2.3 a 3.2.6 — Modelos de tamaño funcional

| Modelo | Herramienta / método | Resultado |
|---|---|---|
| Puntos de Función | Cálculo manual (tablas IFPUG) | PFNA = 175 → PF ajustado = **199,50** |
| Puntos de Casos de Uso | Cálculo manual (UCP) | **UCP = 81** |
| Puntos de Objetos | Cálculo manual (OP) | **OP = 358** → NOP = 268,5 |
| Puntos de Historia | Scrum / backlog | **SP = 78** (velocidad 15 SP/sprint) |

---

### 3.3 — Atributos externos (calidad ISO 25010)

| Característica | Herramienta | Métrica / resultado |
|---|---|---|
| **Usabilidad** | **Selenium** | 83,3 % (5 de 6 pruebas exitosas) |
| **Seguridad** | **SonarQube** + **OWASP ZAP** | 0 vulnerabilidades (SonarQube); ZAP: 0 High, 3 Medium, 1 Low |
| **Portabilidad** | Navegadores (Chrome, Edge) | **100 %** (2/2 navegadores OK) |
| **Mantenibilidad** | **SonarQube** | Rating **A**; deuda técnica 5 d 2 h; duplicación 2,2 % |
| **Rendimiento** | **Lighthouse** | Desktop: FCP 0,9 s, LCP 5,7 s, Performance 58; Móvil: FCP 2,7 s, LCP 25,4 s, Performance 40 |
| **Fiabilidad** | **SonarQube** | 395 issues de confiabilidad (Rating **D**) |
| **Compatibilidad** | Pruebas de integración | **100 %** en Supabase Auth y API REST |
| **Adecuación funcional** | Revisión de requerimientos | **20/20 RF = 100 %** |

---

### 3.4 — Conclusiones (parte 3)
- Tamaño real: entre **17.000 LOC** (SonarQube, frontend) y **35.210 LOC** (CLOC, full stack).
- Fortalezas: mantenibilidad y seguridad **A**, compatibilidad **100 %**, adecuación funcional **100 %**.
- Debilidades: rendimiento móvil y fiabilidad (395 issues en SonarQube).

---

## Parte 4 — Estimación del software

Se aplicaron **5 modelos** para estimar esfuerzo, tiempo, equipo y costo.

| Modelo | Tamaño base | Esfuerzo | Tiempo | Personas | Cos

_[truncado]_

### Usuario

como ejecuto las pruebas de selenium?

### Asistente

Revisando cómo están configuradas las pruebas Selenium en el proyecto.


[tool:Glob]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Grep]

### Asistente

Las pruebas Selenium están en Python, en `tests/selenium/test_captus.py`. Para ejecutarlas:

## 1. Levantar la aplicación

En una terminal, desde la raíz del proyecto:

```bash
npm run dev
```

La app debe quedar en **http://localhost:5173** (es la URL que usan los tests).

## 2. Instalar Selenium (Python)

En otra terminal:

```bash
pip install -r tests/selenium/requirements.txt
```

O directamente:

```bash
pip install selenium
```

Necesitas **Google Chrome** instalado. Con Selenium 4.6+ el ChromeDriver se descarga solo.

## 3. Ejecutar las pruebas

Desde la raíz del repo:

```bash
python -m unittest tests/selenium/test_captus.py -v
```

Eso corre las **9 suites** (57 casos): login, navegación, tareas, notas, configuración, home, calendario, estadísticas y accesibilidad.

### Ejecutar solo una suite

```bash
python -m unittest tests.selenium.test_captus.Test01_Login -v
```

Cambia `Test01_Login` por otra clase, por ejemplo `Test03_Tareas`.

### Modo headless (sin abrir ventana del navegador)

En `test_captus.py`, descomenta esta línea en `_build_driver()`:

```python
options.add_argument("--headless")
```

---

**Notas:**
- Los tests no usan el paquete npm `selenium-webdriver`; usan el paquete Python `selenium`.
- No hace falta credenciales reales para la mayoría de casos; validan DOM, navegación y formularios.
- Si fallan por timeout, confirma que `npm run dev` sigue activo en el puerto 5173.

### Usuario

quiero que pongas lo que me generaste en el resumen de la tercera y cuarta parte en un txt

### Asistente

Creando el archivo `.txt` con el resumen de las partes 3 y 4.


[tool:Write]

### Asistente

Listo. Guardé el resumen en:

`documento de software ii/resumen_parte_3_y_4.txt`

Incluye la parte 3 (medición: herramientas, atributos internos/externos y conclusiones) y la parte 4 (estimación con los 5 modelos, tabla comparativa y conclusiones).


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
