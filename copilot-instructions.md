# Project GEWN — Copilot Instructions

## Project Overview

GEWN is an AI-native desktop copilot platform designed to function as an intelligent operating companion.

This is NOT a simple chatbot application.

GEWN combines:
- conversational AI
- desktop automation
- screen understanding
- semantic memory
- browser automation
- multimodal AI
- autonomous agents
- realtime voice interaction

The system is designed around modular architecture, realtime responsiveness, extensibility, and production-grade engineering principles.

---

# Core Architecture

Frontend:
- Electron desktop shell
- React frontend
- TailwindCSS
- Framer Motion animations

Backend:
- FastAPI
- WebSocket streaming
- Modular service architecture
- Async-first design

AI Layer:
- OpenAI / Gemini APIs
- LangChain
- LangGraph orchestration
- Tool-calling agents

Infrastructure:
- PostgreSQL
- Redis
- ChromaDB
- Docker

Automation:
- Playwright
- PyAutoGUI
- OCR pipelines

---

# Development Philosophy

Always prioritize:
- modularity
- scalability
- maintainability
- readability
- separation of concerns

Avoid:
- monolithic files
- deeply coupled systems
- hardcoded logic
- duplicate implementations

Every subsystem should be independently extensible.

---

# Frontend Standards

Use:
- functional React components
- reusable UI architecture
- Tailwind utility styling
- Framer Motion for smooth animations

UI style should be:
- futuristic
- minimal
- glassmorphism-inspired
- AI operating system aesthetic
- smooth and responsive

Electron windows should prioritize:
- low latency
- smooth rendering
- transparency
- overlay behavior
- desktop-native feel

---

# Backend Standards

Backend must:
- use async/await
- follow service-based architecture
- separate routes, services, and models
- use dependency injection where appropriate
- support realtime streaming

WebSocket systems should:
- support multiple connections
- handle reconnection gracefully
- avoid blocking operations

---

# AI System Standards

AI systems should:
- support tool calling
- support streaming responses
- separate reasoning from execution
- maintain memory boundaries
- avoid unsafe autonomous behavior

Agents must:
- be modular
- have isolated responsibilities
- expose clear interfaces
- support orchestration

---

# Memory Architecture

Memory is divided into:
- short-term session memory
- long-term semantic memory
- workflow memory

Never mix memory responsibilities into unrelated systems.

---

# Security Principles

Always prioritize:
- least privilege
- explicit permissions
- safe command execution
- secure file handling
- prompt injection resistance

Never generate unsafe terminal execution logic.

Avoid:
- unrestricted shell execution
- insecure path handling
- exposing secrets
- hardcoded credentials

---

# Coding Conventions

Python:
- type hints preferred
- modular services
- async-first
- clean folder separation

React:
- component-driven architecture
- avoid oversized components
- reusable hooks preferred

General:
- meaningful naming
- avoid generic filenames like utils.py
- write self-documenting code
- add comments only where architectural context matters

---

# Project Structure

Frontend:
frontend/
- electron/
- src/
- components/
- hooks/
- services/

Backend:
backend/
- app/
- routes/
- agents/
- automation/
- memory/
- rag/
- websocket/
- vision/

---

# Current Development Priority

Current milestone:
M1 — Core Desktop Overlay

Focus ONLY on:
- Electron overlay
- React UI
- transparent always-on-top window
- FastAPI backend
- WebSocket communication
- basic AI chat integration

Do NOT prematurely implement:
- autonomous agents
- plugin marketplace
- advanced orchestration
- enterprise infrastructure

---

# Expected Coding Style

Generated code should:
- be production-oriented
- be modular
- follow scalable architecture
- avoid unnecessary complexity
- prioritize clarity over cleverness

When generating code:
- explain architecture briefly when relevant
- keep files focused on one responsibility
- use realistic engineering practices