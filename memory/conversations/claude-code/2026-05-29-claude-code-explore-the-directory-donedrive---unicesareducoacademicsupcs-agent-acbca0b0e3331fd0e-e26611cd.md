---
date: 2026-05-29
type: conversation
source_agent: claude-code
session_id: "agent-acbca0b0e3331fd0e"
project: "subagents"
source_path: "C:\\Users\\david\\.claude\\projects\\D--OneDrive---unicesar-edu-co-Academics-UPC-Semester-VII-Software-Engineering-II\\52d04b02-602f-4a90-8381-4a46b53ba87f\\subagents\\agent-acbca0b0e3331fd0e.jsonl"
tags: [conversation, imported, claude-code]
title: "Explore the directory \"D:\\OneDrive - unicesar.edu.co\\Academics\\UPC\\Semester VII\\Software E"
---

# Explore the directory "D:\OneDrive - unicesar.edu.co\Academics\UPC\Semester VII\Software E

**Fecha:** 2026-05-29  
**Agente:** claude-code  
**Proyecto/contexto:** subagents  
**Sesión:** `agent-acbca0b0e3331fd0e`  
**Origen:** `C:\Users\david\.claude\projects\D--OneDrive---unicesar-edu-co-Academics-UPC-Semester-VII-Software-Engineering-II\52d04b02-602f-4a90-8381-4a46b53ba87f\subagents\agent-acbca0b0e3331fd0e.jsonl`

## Mensajes

### Usuario

Explore the directory "D:\OneDrive - unicesar.edu.co\Academics\UPC\Semester VII\Software Engineering II" thoroughly. I need a complete picture of:
1. All files and folders (full tree structure)
2. Content of key files (documents, code, configs, notes, etc.)
3. What this project/course is about
4. Technologies, frameworks, tools used
5. Any assignments, labs, or project descriptions

Be very thorough — read as many files as needed to build a complete understanding. Search breadth: very thorough.

### Asistente

I'll conduct a thorough exploration of this directory to give you a complete picture. Let me start by examining the structure and then dive into the key files.

### Usuario

[tool_result]

### Asistente

Let me use the correct syntax for PowerShell:

### Usuario

[tool_result]

### Asistente

Good! Now let me get the complete directory tree:

### Usuario

[tool_result]

### Asistente

Perfect! Now let me read key documents to understand the content. Let me start with the main project documents:

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Asistente

Let me read the PDF files instead:

### Usuario

[tool_result]

### Usuario

[tool_result]

### Usuario

[tool_result]

### Asistente

API Error: a document in the conversation could not be processed and was removed. Re-read the file with a different approach if you still need it.

### Asistente

Let me use bash to extract text from these files instead:

### Usuario

[tool_result]

### Asistente

Now let me compile all the information I've gathered from the PDF files and directory structure.

## Complete Directory Exploration: Software Engineering II Course

### **Directory Structure**

The course is organized into 3 "Cuts" (Cortes - evaluation periods):

```
Software Engineering II/
├── Cut 1/ (Primera Evaluación)
├── Cut 2/ (Segunda Evaluación)
└── Cut 3/ (Tercera Evaluación)
```

**Total files: 47 items**

---

### **1. COURSE OVERVIEW**

**Institution:** Universidad Popular del Cesar  
**Faculty:** Ingeniería y Tecnología  
**Program:** Ingeniería de Sistemas  
**Course:** Ingeniería de Software II (Software Engineering II)  
**Instructor:** Ing. Maribel Romero Mestre  
**Location:** Valledupar, Colombia  
**Year:** 2026

---

### **2. PROJECT: CAPTUS**

**Full Name:** CAPTUS - Plataforma Web para la Gestión Académica Inteligente  
**Type:** Intelligent Web Platform for Academic Management  
**Student Author:** David Barceló  

#### **Problem Statement**
The course addresses deficiencies in AulaWeb (the institutional LMS) at Universidad Popular del Cesar, including poor usability, lack of personalization, and limited support for individual organization. Students struggle to manage personal tasks and subtasks within the academic ecosystem.

#### **Solution Description**
Captus is a modern web platform designed to improve personal academic management through:
- Modern functionalities
- Intelligent automation
- Integration with current services (Supabase, external AI)
- Unified space for students and teachers to manage tasks, activities, events, and statistics
- AI-based assistant to reduce cognitive load

---

### **3. SYSTEM REQUIREMENTS**

#### **Functional Requirements (RF)**
- **RF01:** Authentication - Login/registration via Supabase (Student/Teacher)
- **RF02:** Task Management - Create, edit, delete, list personal tasks (Student)
- **RF08:** Notifications - Send reminders 24 hours before task deadline (Student)
- **RF10:** AI Assistant - Generate tasks and events through natural language prompts (Student)

#### **Non-Functional Requirements (RNF)**
- **RNF01:** Security - Data protection via JWT and Supabase policies
- **RNF03:** Performance - Response time < 2 seconds for module loading

#### **Use Cases (CU)**
- **CU01:** Login Session (Iniciar sesión)
- **CU02:** Manage Tasks (Administrar tareas)
- **CU03:** Enroll in Course (Unirse a curso)
- **CU04:** Clear Activity (Limpiar actividad)
- **CU05:** Submit Activity (Entregar actividad)

---

### **4. SYSTEM DESIGN**

#### **Architecture**
- Client-Server architecture with cloud service integration
- Database: Supabase (PostgreSQL-based)
- Frontend-Backend communication via APIs

#### **Data Model (Class Diagram)**
Major entities:
- **Usuario** (User) - Base class with id, nombre, email, password, iniciarSesion()
- **Estudiante** - Extends Usuario; includes courseCode, registeredActivities
- **Docente** (Teacher) - Extends Usuario; includes creatActivity(), calificaEnsayos()
- **Curso** (Course) - Has id, name, code, aggregateStudents(), listActividades()
- **Tarea** (Task) - Has id, title, description, deadline, completed()
- **Subtarea** (Subtask) - Nested tasks within main tasks
- **Actividad** (Activity) - Has id, title, description, deliveryDate, publicar()
- **Entrega** (Submission) - Has id, date, file, emitir()
- **Estadística** (Statistics) - Tracks tasksComplete (int), activitiesCompleted (int), generarReporte()
- **Notificación** (Notification) - Has id, me

_[truncado]_


## Enlaces
- Índice: [[claude-code-import-index]]
- Home: [[Home]]
