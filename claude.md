# CLAUDE.md — Project GEWN

## Project Identity

GEWN is an AI-native desktop copilot platform.

The system is designed as a persistent intelligent operating companion that combines:
- conversational AI
- desktop automation
- realtime voice interaction
- screen understanding
- semantic memory
- browser automation
- multimodal reasoning
- autonomous workflows

GEWN is NOT a simple chatbot application.

The architecture prioritizes:
- realtime responsiveness
- modularity
- extensibility
- safe automation
- scalable system design

---

# High-Level Architecture

Frontend:
- Electron desktop shell
- React UI
- TailwindCSS
- Framer Motion

Backend:
- FastAPI
- WebSockets
- service-oriented architecture
- async-first design

AI Layer:
- OpenAI / Gemini
- LangChain
- LangGraph
- tool orchestration

Memory:
- Redis
- PostgreSQL
- ChromaDB

Automation:
- Playwright
- PyAutoGUI
- OCR pipelines

Infrastructure:
- Docker
- GitHub Actions

---

# Engineering Philosophy

The repository should evolve like a production software platform rather than a prototype.

Always prioritize:
- scalability
- maintainability
- modularity
- explicit architecture
- clean abstractions

Avoid:
- monolithic logic
- tightly coupled modules
- premature optimization
- hidden side effects
- oversized files

Every subsystem should have:
- isolated responsibilities
- clear interfaces
- future extensibility

---

# Current Development Phase

Current milestone:
M1 — Core Overlay System

Current focus:
- Electron overlay shell
- transparent always-on-top window
- React UI integration
- FastAPI backend
- WebSocket communication
- AI chat connectivity

Avoid implementing:
- autonomous agents
- advanced orchestration
- plugin marketplace
- enterprise infrastructure
- overengineered abstractions

The immediate goal is a stable functional MVP.

---

# Repository Structure

Frontend:
frontend/
- electron/
- src/
- components/
- hooks/
- animations/
- services/

Backend:
backend/
- app/
- routes/
- agents/
- memory/
- automation/
- rag/
- websocket/
- vision/
- database/

Documentation:
docs/
- architecture.md
- PRD.md
- FEATURES.md
- roadmap.md
- SECURITY_NOTES.md
- USER_FLOW.md

---

# Frontend Principles

The UI should feel:
- futuristic
- responsive
- lightweight
- intelligent
- desktop-native

Visual direction:
- glassmorphism
- soft glow aesthetics
- smooth transitions
- AI operating system feel

Frontend code should:
- use reusable components
- minimize prop drilling
- separate UI from logic
- use hooks cleanly
- avoid oversized components

Electron should prioritize:
- transparency
- low latency
- overlay behavior
- stable IPC communication

---

# Backend Principles

Backend architecture must:
- use async-first patterns
- separate routes/services/models
- support streaming
- remain modular
- avoid business logic inside routes

WebSocket systems should:
- support concurrent connections
- handle reconnects safely
- avoid blocking operations
- support streaming AI responses

---

# AI System Philosophy

AI systems should:
- separate reasoning from execution
- support tool calling
- maintain memory boundaries
- remain observable and debuggable

Agents should:
- be modular
- expose explicit interfaces
- avoid hidden autonomy
- support orchestration

Do not tightly couple AI reasoning to UI logic.

---

# Memory System Principles

Memory architecture consists of:
1. short-term session memory
2. long-term semantic memory
3. workflow memory

Memory systems must:
- remain inspectable
- support deletion
- support retrieval ranking
- avoid storing secrets

---

# Security Principles

Always prioritize:
- least privilege
- explicit permissions
- safe command execution
- secure file access
- prompt injection resistance

Never:
- hardcode secrets
- allow unrestricted shell execution
- trust external input blindly
- bypass confirmation systems

Terminal execution must:
- validate commands
- sanitize inputs
- avoid arbitrary execution paths

---

# Coding Standards

General:
- write self-documenting code
- prefer clarity over cleverness
- use meaningful naming
- keep files focused

Python:
- async/await preferred
- type hints encouraged
- service-based architecture
- modular organization

React:
- functional components only
- reusable hooks preferred
- avoid excessive state lifting

Naming:
GOOD:
- websocket_manager.py
- memory_service.py
- overlay_window.jsx

BAD:
- utils.py
- helpers.py
- stuff.py

---

# AI Assistant Guidance

When generating code:
- prioritize scalable architecture
- keep implementations modular
- explain important architectural decisions briefly
- avoid unnecessary complexity
- maintain consistency with existing structure

When uncertain:
- prefer extensibility
- prefer explicit interfaces
- prefer readable implementations

Do not generate:
- fake implementations
- unsafe automation logic
- hidden autonomous execution
- tightly coupled systems

---

# Long-Term Vision

GEWN should eventually evolve into:
- a realtime AI operating layer
- a multimodal desktop assistant
- an extensible AI workflow platform

However:
the current priority is building a stable and elegant foundation before expanding capability.