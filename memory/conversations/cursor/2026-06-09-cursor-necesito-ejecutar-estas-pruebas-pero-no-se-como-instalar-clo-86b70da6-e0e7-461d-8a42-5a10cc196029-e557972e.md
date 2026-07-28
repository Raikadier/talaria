---
date: 2026-06-09
type: conversation
source_agent: cursor
session_id: "86b70da6-e0e7-461d-8a42-5a10cc196029"
project: "c"
source_path: "C:\\Users\\david\\.cursor\\projects\\c\\agent-transcripts\\86b70da6-e0e7-461d-8a42-5a10cc196029\\86b70da6-e0e7-461d-8a42-5a10cc196029.jsonl"
tags: [conversation, imported, cursor]
title: "necesito ejecutar estas pruebas pero no se como instalar cloc ni sonarqube:"
---

# necesito ejecutar estas pruebas pero no se como instalar cloc ni sonarqube:

**Fecha:** 2026-06-09  
**Agente:** cursor  
**Proyecto/contexto:** c  
**Sesión:** `86b70da6-e0e7-461d-8a42-5a10cc196029`  
**Origen:** `C:\Users\david\.cursor\projects\c\agent-transcripts\86b70da6-e0e7-461d-8a42-5a10cc196029\86b70da6-e0e7-461d-8a42-5a10cc196029.jsonl`

## Mensajes

### Usuario

necesito ejecutar estas pruebas pero no se como instalar cloc ni sonarqube:

1
CLOC en terminal (cloc src/ y backend)
3.2.1a — LOC por lenguaje
2
VSCodeCounter (extensión en VS Code, carpeta src/)
3.2.1 — LOC por herramienta
3
SonarQube — panel general (LOC, bugs, deuda técnica, duplicación)
3.2.1b + 3.3.4 mantenibilidad
4
SonarQube — panel de seguridad (vulnerabilidades = 0)
3.3.2 seguridad
5
SonarQube — métricas de clases (WMC, CBO, complejidad)
3.2.2 tamaño orientado a clases
6
Selenium — ejecución de tests/selenium/test_captus.py (output)
3.3.1 usabilidad
7
Lighthouse / PageSpeed desktop
3.3.5 rendimiento
8
Lighthouse / PageSpeed móvil
3.3.5 rendimiento
9
OWASP ZAP — reporte de alertas (0 críticas)
3.3.2 seguridad
10
Prueba en Chrome (app funcionando)
3.3.3 portabilidad
11
Prueba en Firefox (app funcionando)
3.3.3 portabilidad
12
Prueba en Edge (app funcionando)
3.3.3 portabilidad
13
Herramienta de estimación digital (ej. COCOMO Calculator online)
4.5 estimación con herramienta

### Asistente

Voy a explorar primero tu proyecto para darte comandos exactos y no genéricos.

 El usuario necesita ayuda instalando cloc y sonarqube, y ejecutando pruebas en su proyecto Captus. Está en Windows con PowerShell, y su workspace está en C:\. Voy a explorar la estructura del proyecto primero para entender mejor qué tenemos: hay un directorio src/, backend, y pruebas de Selenium en tests/selenium/test_captus.py.

Debería buscar el proyecto Captus en el workspace para dar instrucciones precisas sobre las rutas y configuración específica que necesita.
[tool:Glob]
[tool:Glob]

### Asistente

El workspace es `C:\` completo (muy grande), así que la búsqueda tardó. Déjame ubicar tu proyecto de forma más precisa.

 The workspace root is too broad, so I need a more targeted approach to locate the Captus project. Let me check the terminals folder to see if I can find the current working directory from there.
[tool:Shell]
[tool:Glob]

### Asistente

The Glob search is timing out when scanning from C:\, so I need to narrow the scope and search in more specific directories like Desktop or Documents instead. Let me try targeting likely development folders to locate the Captus project.
[tool:Shell]

### Asistente

The search came up empty, so the project isn't in the typical locations. Rather than digging through the entire drive, I should just ask the user directly where the Captus project is located.
[tool:Glob]

### Asistente

[tool:Shell]

### Usuario

no, no quiero que busques el proyecto, quiero que me expliques como descargar cloc

### Asistente

# Cómo instalar CLOC en Windows

**CLOC** (Count Lines of Code) cuenta líneas de código por lenguaje. En Windows tienes varias formas de instalarlo; estas son las más sencillas.

---

## Opción 1: winget (recomendada si ya lo tienes)

Abre **PowerShell** o **Terminal** y ejecuta:

```powershell
winget install AlDanial.cloc
```

Luego verifica:

```powershell
cloc --version
```

---

## Opción 2: Chocolatey

Si tienes [Chocolatey](https://chocolatey.org/) instalado:

```powershell
choco install cloc
```

---

## Opción 3: Scoop

Si usas [Scoop](https://scoop.sh/):

```powershell
scoop install cloc
```

---

## Opción 4: Descarga manual (sin gestor de paquetes)

1. Ve al repositorio oficial: [https://github.com/AlDanial/cloc/releases](https://github.com/AlDanial/cloc/releases)
2. Descarga el archivo **`cloc-2.x.x.exe`** (es un ejecutable standalone para Windows).
3. Renómbralo a `cloc.exe` si quieres.
4. Colócalo en una carpeta que esté en tu **PATH**, por ejemplo:
   - `C:\Users\david\bin\`
   - o `C:\tools\cloc\`
5. Añade esa carpeta al PATH del sistema (Configuración → Sistema → Acerca de → Configuración avanzada → Variables de entorno → Path → Editar → Nueva).

Verifica en una terminal nueva:

```powershell
cloc --version
```

---

## Opción 5: npm (si ya tienes Node.js)

```powershell
npm install -g cloc
```

---

## Cómo usarlo (para tu prueba 1)

Una vez instalado, desde la raíz de tu proyecto:

```powershell
cloc src/
cloc backend/
```

O ambos a la vez:

```powershell
cloc src/ backend/
```

La salida muestra **LOC por lenguaje** (archivos, líneas en blanco, comentarios y código), que es lo que pide la prueba **3.2.1a**.

---

## Si `cloc` no se reconoce

- Cierra y vuelve a abrir la terminal después de instalar.
- Comprueba que esté en el PATH: `where.exe cloc`
- Si usaste descarga manual, ejecuta con ruta completa: `C:\ruta\a\cloc.exe src/`

---

**Resumen:** la forma más rápida suele ser `winget install AlDanial.cloc`. Si no tienes winget, descarga el `.exe` desde GitHub y ponlo en el PATH.

¿Quieres que te explique también cómo instalar SonarQube para las pruebas 3–5?

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

La tarea en segundo plano terminó correctamente: revisó los metadatos de tus terminales y todas apuntan al directorio de trabajo `C:\` (la raíz del disco), no a una carpeta concreta de un proyecto.

Eso explica por qué las búsquedas automáticas del proyecto Captus tardaban o no daban resultados útiles. Como pediste solo la guía de instalación de CLOC, no hace falta ninguna acción adicional por ese hallazgo.

Para la prueba 1, con CLOC ya instalado bastará con ejecutar desde la carpeta raíz de tu proyecto:

```powershell
cloc src/
cloc backend/
```

Si quieres, en el siguiente mensaje te explico cómo instalar SonarQube para las pruebas 3–5.

### Usuario

y sonarqube?

### Asistente

# Cómo instalar SonarQube en Windows

SonarQube es un **servidor de análisis de código**. No analiza solo con instalarlo: necesitas levantar el servidor, escanear tu proyecto con **SonarScanner** y ver los resultados en el navegador.

---

## Requisitos previos

- **Java 17 o superior** (JDK)
- Verifica en PowerShell:

```powershell
java -version
```

Si no lo tienes, instala por ejemplo [Eclipse Temurin JDK 17](https://adoptium.net/) o con winget:

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

---

## Opción A: Docker (la más sencilla)

Si tienes [Docker Desktop](https://www.docker.com/products/docker-desktop/):

```powershell
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

Espera 1–2 minutos y abre: **http://localhost:9000**

- Usuario inicial: `admin`
- Contraseña inicial: `admin` (te pedirá cambiarla)

---

## Opción B: Instalación manual (ZIP)

1. Descarga **SonarQube Community** desde:  
   [https://www.sonarsource.com/products/sonarqube/downloads/](https://www.sonarsource.com/products/sonarqube/downloads/)

2. Descomprime el ZIP, por ejemplo en `C:\sonarqube\`

3. Inicia el servidor (PowerShell, desde la carpeta descomprimida):

```powershell
cd C:\sonarqube\bin\windows-x86-64
.\StartSonar.bat
```

4. Abre **http://localhost:9000** cuando veas en la consola que arrancó.

Para detenerlo:

```powershell
.\StopSonar.bat
```

---

## Paso 2: Instalar SonarScanner (para analizar tu código)

SonarQube solo muestra resultados; el análisis lo hace **SonarScanner**.

### Con winget:

```powershell
winget install SonarSource.SonarScanner
```

### O descarga manual:

[https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/)

Descomprime, añade `bin` al PATH y verifica:

```powershell
sonar-scanner --version
```

---

## Paso 3: Configurar y escanear tu proyecto

En la **raíz del proyecto**, crea un archivo `sonar-project.properties` con algo como:

```properties
sonar.projectKey=captus
sonar.projectName=Captus
sonar.sources=src,backend
sonar.sourceEncoding=UTF-8
sonar.host.url=http://localhost:9000
```

Luego, desde esa carpeta:

```powershell
sonar-scanner
```

La primera vez puede pedirte un **token** en SonarQube:

1. Entra a http://localhost:9000 → **My Account** → **Security** → **Generate Token**
2. Ejecuta el escaneo con el token=
sonar-scanner -Dsonar.token=
```

---

## Qué capturar para tus pruebas (3, 4 y 5)

| Prueba | Dónde verlo en SonarQube |
|--------|--------------------------|
| **3** — Panel general (LOC, bugs, deuda, duplicación) | **Overview** / **Measures** |
| **4** — Seguridad (vulnerabilidades = 0) | Pestaña **Security** / **Issues** filtrando por vulnerabilidades |
| **5** — Métricas de clases (WMC, CBO, complejidad) | **Measures** → complejidad ciclomática, cognitive complexity, etc. |

**Nota importante sobre la prueba 5:** SonarQube muestra bien **complejidad ciclomática** y métricas de mantenibilidad, pero **WMC** (Weighted Methods per Class) y **CBO** (Coupling Between Objects) son métricas orientadas a objetos clásicas que **no siempre aparecen en la edición Community** por defecto. Si tu rúbrica exige WMC/CBO explícitamente, puede que necesites un plugin, **SonarQube Developer Edition**, o una herramienta complementaria (por ejemplo análisis estático en Java con herramientas OO). Para complejidad general, SonarQube sí sirve.

---

## Altern

_[truncado]_

### Usuario

okey, como instalo sonarscanner?

### Asistente

# Cómo instalar SonarScanner en Windows

SonarScanner es la herramienta de línea de comandos que envía tu código a SonarQube (o SonarCloud) para analizarlo.

---

## Opción 1: winget (recomendada)

Abre **PowerShell** o **Terminal** y ejecuta:

```powershell
winget install SonarSource.SonarScanner
```

Cierra y vuelve a abrir la terminal, luego verifica:

```powershell
sonar-scanner --version
```

---

## Opción 2: Descarga manual

1. Ve a la documentación oficial:  
   [https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/)

2. Descarga el ZIP para **Windows** (SonarScanner CLI).

3. Descomprime en una carpeta fija, por ejemplo:
   ```
   C:\tools\sonar-scanner\
   ```

4. Añade al **PATH** la carpeta `bin` dentro de esa ruta:
   ```
   C:\tools\sonar-scanner\bin
   ```
   - Configuración → Sistema → Acerca de → Configuración avanzada del sistema → Variables de entorno → Path → Editar → Nueva

5. Abre una terminal nueva y verifica:

```powershell
sonar-scanner --version
```

---

## Requisito previo: Java

SonarScanner necesita **Java 17+** instalado:

```powershell
java -version
```

Si no lo tienes:

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

---

## Cómo usarlo (después de instalar)

1. Asegúrate de que SonarQube esté corriendo en `http://localhost:9000`.

2. En la raíz de tu proyecto, crea `sonar-project.properties` (o usa parámetros en la línea de comandos).

3. Genera un token en SonarQube: **My Account → Security → Generate Token**.

4. Desde la carpeta del proyecto, ejecuta:

```powershell
sonar-scanner -Dsonar.token=
```

O si ya está en `sonar-project.properties`:

```powershell
sonar-scanner
```

---

## Si `sonar-scanner` no se reconoce

- Cierra y reabre la terminal.
- Comprueba el PATH: `where.exe sonar-scanner`
- Si instalaste manualmente, ejecuta con ruta completa:
  ```powershell
  C:\tools\sonar-scanner\bin\sonar-scanner.bat --version
  ```

---

## Resumen

| Método | Comando |
|--------|---------|
| winget | `winget install SonarSource.SonarScanner` |
| Manual | Descargar ZIP → descomprimir → añadir `bin` al PATH |
| Verificar | `sonar-scanner --version` |

Con eso ya puedes escanear tu proyecto y ver los resultados en el panel de SonarQube.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
