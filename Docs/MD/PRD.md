# Project GEWN — Product Requirements Document

**Version:** 1.1.0
**Status:** Active — Pre-Development
**Last Updated:** 2025
**Classification:** Internal — Core Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Product Vision](#3-product-vision)
4. [Goals and Objectives](#4-goals-and-objectives)
5. [Target Audience](#5-target-audience)
6. [User Pain Points](#6-user-pain-points)
7. [Feature Specifications](#7-feature-specifications)
8. [Functional Requirements](#8-functional-requirements)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [User Flows and Scenarios](#10-user-flows-and-scenarios)
11. [AI Behavior and Safety Model](#11-ai-behavior-and-safety-model)
12. [Security Architecture](#12-security-architecture)
13. [MVP Scope](#13-mvp-scope)
14. [Development Roadmap](#14-development-roadmap)
15. [Technical Architecture](#15-technical-architecture)
16. [Risk Analysis](#16-risk-analysis)
17. [Success Metrics](#17-success-metrics)
18. [Future Scalability](#18-future-scalability)
19. [Constraints](#19-constraints)
20. [Glossary](#20-glossary)

---

## 1. Executive Summary

**Project GEWN** is an AI-native desktop copilot platform that operates as an intelligent layer directly above the user's operating system. It combines conversational AI, real-time screen understanding, desktop and browser automation, persistent semantic memory, and a multi-agent orchestration framework into a single unified companion.

Unlike existing AI assistants that operate in isolated browser tabs or standalone chat applications, GEWN is embedded in the desktop environment itself — always available, always contextually aware, and capable of taking meaningful action across the entire computing surface.

GEWN is designed for developers, knowledge workers, students, and power users who spend the majority of their day inside complex workflows and need an intelligent collaborator that understands what they're working on and can act on their behalf.

The platform is engineered for phased delivery across seven discrete, independently shippable milestones — from a functional MVP (floating overlay + conversational AI + basic automation) through to a full autonomous multi-agent ecosystem with a plugin marketplace and cross-device synchronization.

---

## 2. Problem Statement

### 2.1 The Core Gap

Modern personal computing remains fundamentally manual. Despite decades of productivity tooling and a recent surge in AI chatbot adoption, the relationship between user and operating system has not meaningfully changed. The computer waits. The user operates.

Users today:

- Manually switch between five or more applications to complete a single workflow
- Repeat the same setup routines and file organization tasks daily
- Retrieve information by remembering where they stored it rather than what it contains
- Copy and paste content across tools that have zero awareness of each other
- Lose cognitive bandwidth navigating the operating system instead of focusing on actual work

### 2.2 Why Existing AI Tools Fall Short

Current AI assistants — including frontier models accessed via web chat — fail to address this gap because they are architecturally disconnected from the computing environment they're supposed to assist with:

- They operate inside isolated browser windows with no awareness of what else is on screen
- They cannot read files, launch applications, execute commands, or interact with the OS in any meaningful way
- They have no persistent memory of the user across sessions; every conversation starts cold
- They respond only when explicitly prompted — they cannot observe, detect, or proactively surface relevant assistance
- They offer no workflow automation; the user must translate AI output into manual action themselves

### 2.3 The Opportunity

There is no production-ready, AI-native operating layer that:

- Understands what is on the user's screen in real time
- Maintains persistent, evolving knowledge of the user's preferences, workflows, and context
- Can take action across the file system, applications, browser, and system settings
- Coordinates multiple specialized AI agents to handle complex, multi-step goals autonomously
- Does all of this within a cohesive, safe, and transparent user experience

GEWN is built to fill this gap.

---

## 3. Product Vision

### 3.1 Vision Statement

To build the world's first truly ambient AI operating companion — a system that understands what you're working on, remembers how you work, and acts intelligently on your behalf, so that the computer adapts to the human rather than the other way around.

### 3.2 Design Philosophy

GEWN is not a chatbot with desktop access. It is designed from first principles as an operating companion — a system whose primary context is the user's entire computing environment, not a single conversation thread.

The system is built around four core beliefs:

**AI should be ambient.** It should exist at the edges of awareness — available instantly, but not demanding attention. GEWN floats above the desktop, always reachable, never in the way.

**AI should be contextual.** Effective assistance requires understanding what the user is doing *right now*, not just what they've typed in a text box. GEWN reads the screen, understands applications, and infers context continuously.

**AI should be proactive.** The best assistant doesn't wait to be asked for things it already knows you need. GEWN surfaces relevant help, detects errors, and flags opportunities without requiring explicit prompts.

**AI should act, not just advise.** The last mile of AI usefulness is execution. GEWN closes the loop between recommendation and action — it doesn't just tell you how to organize your downloads folder; it organizes it.

### 3.3 Long-Term North Star

The long-term vision for GEWN is a fully AI-native computing ecosystem in which the operating system itself becomes intelligent and adaptive. Future versions envision:

- Autonomous background agents that manage research, scheduling, and file organization without interrupting the user
- Multimodal reasoning across screen content, voice, documents, and real-time data
- A personalized AI environment that evolves continuously with the user's habits and preferences
- An open plugin ecosystem through which developers extend GEWN into specialized domains

---

## 4. Goals and Objectives

### Goal 1 — Ambient Desktop Presence
Deliver a persistent, always-available AI assistant that integrates directly into the desktop environment via a floating overlay, accessible in under two seconds via keyboard shortcut or wake word from any application.

### Goal 2 — Real-Time Context Awareness
Enable GEWN to understand the user's current application state, screen content, open files, and workflow context — providing assistance that is situationally relevant rather than generically prompted.

### Goal 3 — Actionable Automation
Allow users to automate repetitive file management, application control, and multi-step workflows using natural language — with safe, tiered execution and full transparency into what actions are being taken.

### Goal 4 — Intelligent Assistance Across Domains
Provide proactive, context-injected AI assistance across coding, research, studying, writing, and general productivity workflows — with specialized behavior per domain.

### Goal 5 — Persistent Semantic Memory
Build a three-layer memory architecture (session, long-term semantic, workflow pattern) that evolves with the user and allows GEWN to provide increasingly personalized assistance over time.

### Goal 6 — Autonomous Multi-Agent Orchestration
Develop a multi-agent framework of specialized AI agents (Coding, Research, Automation, Memory, Scheduling) capable of decomposing complex goals into executable plans and running extended workflows with user oversight.

### Goal 7 — Trust Through Transparency
Ensure every action GEWN takes — file operations, terminal commands, API calls — is visible, explainable, and reversible where possible, with a four-tier permission system that gives users complete control without friction.

---

## 5. Target Audience

### 5.1 Primary Audiences

**Developers and AI Engineers**
Software engineers, AI/ML practitioners, and open-source contributors who spend most of their working day in code editors, terminals, and documentation. They have complex, multi-application workflows, benefit significantly from context-aware coding assistance and automation, and are tolerant of advanced configuration in exchange for power.

*Primary use cases:* Inline error detection and fix suggestion, terminal command automation, codebase navigation, documentation Q&A via RAG, workspace setup automation.

**Students and Researchers**
Computer science students, academic researchers, and learning-focused users who regularly consume, synthesize, and produce large volumes of written content. They benefit from document intelligence, note generation, research assistance, and semantic memory that tracks ongoing projects.

*Primary use cases:* PDF summarization and Q&A, research synthesis, study workflow management, semantic search across notes.

**Knowledge Workers**
Analysts, writers, strategists, and consultants who operate across many tools simultaneously. They need to move information across platforms efficiently, reduce context-switching overhead, and maintain organized knowledge bases.

*Primary use cases:* Cross-application workflow automation, intelligent file organization, meeting prep automation, information retrieval.

**Creative Professionals**
Designers, video editors, and digital creators whose workflows span complex, multi-application creative suites. They benefit from workspace automation, reference material retrieval, and AI assistance integrated directly into their environment.

*Primary use cases:* Asset organization, reference retrieval via RAG, workspace launch automation.

### 5.2 Secondary Audiences

**Power Users and Automation Enthusiasts**
Users who heavily customize their computing environments and are comfortable building personal automation systems. They represent early adopters and are likely to engage with the plugin SDK and workflow scripting.

**AI-Forward Early Adopters**
Users motivated by cutting-edge AI systems who want to experience the frontier of autonomous AI interaction. They generate valuable feedback during early phases and drive word-of-mouth growth.

---

## 6. User Pain Points

| Pain Point | Current Reality | GEWN's Resolution |
|---|---|---|
| **Workflow Fragmentation** | Users manually switch between 5–10 applications per complex task | GEWN understands cross-application context and automates transitions and handoffs |
| **Repetitive Task Overhead** | Daily setup routines, file organization, and copy-paste workflows consume hours per week | Natural language workflow automation executes these at instruction |
| **Context-Blind AI** | Existing AI assistants have no awareness of screen content, open files, or application state | Real-time screen capture, OCR, and multimodal analysis give GEWN full situational awareness |
| **Zero Memory Continuity** | Every AI conversation starts cold; users re-explain context repeatedly | Persistent three-layer memory system maintains continuity across sessions and evolves over time |
| **Advice Without Action** | AI outputs require the user to manually implement every recommendation | GEWN closes the execution loop — it acts, with tiered permission safety |
| **Cognitive Load of Navigation** | Mental energy spent managing applications rather than doing actual work | GEWN absorbs operational overhead, letting the user focus on the work itself |
| **File Discovery Friction** | Files are found by remembering their location rather than their content | Semantic tagging and vector-indexed file retrieval find files by meaning |
| **Fragmented Integrations** | Productivity tools (Notion, GitHub, Gmail, Slack) don't talk to each other | GEWN's plugin system bridges these as first-class integrations with a unified AI interface |

---

## 7. Feature Specifications

### 7.1 Floating Desktop Overlay

The primary user interface is a transparent glassmorphism overlay rendered via Electron's always-on-top transparent window, built in React with Framer Motion animations.

**Interface Properties**
- Always-on-top rendering above all desktop applications
- Draggable to any screen position; position persists across sessions
- Resizable panel with minimize-to-icon mode
- Configurable opacity and size
- Instant focus via configurable global keyboard shortcut (default: `Ctrl+Space`)
- Smooth animated transitions between states (expanded, minimized, voice mode)
- Futuristic dark UI theme with glassmorphism aesthetics

**Interaction Modes**

| Mode | Description | Activation |
|---|---|---|
| Standard | General conversation and assistance | Default |
| Focus | Minimized footprint; GEWN suppresses unsolicited suggestions | Manual toggle or smart detection |
| Research | Document analysis and structured output optimized | Contextual or manual |
| Automation | Step-by-step workflow execution with inline confirmation | Triggered by automation requests |
| Voice | Full-screen voice visualization; real-time conversation | Wake word or hotkey hold |

---

### 7.2 Conversational AI Engine

**Core Capabilities**
- Multi-provider LLM integration (OpenAI, Google Gemini) with hot-swappable model selection
- Streaming response rendering for perceived low latency
- Full conversation history maintained per session and optionally persisted across sessions
- Context injection from: current screen state, active application, long-term memory, RAG retrieval, and workflow state
- Markdown and syntax-highlighted code rendering in the chat panel
- Follow-up understanding and multi-turn reasoning within session context
- Domain-aware prompt orchestration (coding mode, research mode, productivity mode)

**AI Behavioral Standards** *(see Section 11 for full specification)*
- Leads with direct, capable responses — avoids excessive hedging or filler
- Transparently surfaces uncertainty; never fabricates file system or screen state
- Respects scope boundaries; does not expand to unasked actions without surfacing the opportunity first

---

### 7.3 Desktop Automation

All automation actions are classified by risk tier and handled accordingly (see Section 11.1).

**File System Operations**
- Create, rename, move, copy, and delete files and folders
- Batch operations across directory trees
- Semantic file tagging for content-aware organization
- Intelligent categorization and organization of directories by file type, date, or semantic content
- Natural language file search (e.g., "find the Q3 report I was editing last week")

**Application Control**
- Launch, focus, and close applications by name or category
- Window arrangement and multi-monitor workspace configuration
- Application-specific workflow presets (e.g., "prepare my coding workspace")

**System Utilities**
- Clipboard monitoring and intelligent clipboard history
- Screenshot capture (on-demand and periodic for context)
- System notifications and smart reminders
- Global shortcut registration
- Terminal command execution with safety validation and argument sandboxing

**Browser Automation** *(Playwright-powered)*
- Web navigation, content extraction, and structured summarization
- Form interaction and submission (with T3 approval)
- Multi-tab research workflows
- File download management

---

### 7.4 Screen Awareness and Vision System

**Capture and Analysis Pipeline**
- On-demand screenshot capture via keyboard shortcut or voice command
- Passive periodic capture for proactive context awareness (configurable, opt-in)
- PaddleOCR primary / Tesseract fallback for text extraction from screenshots
- Multimodal LLM analysis for UI understanding, layout comprehension, and semantic content interpretation

**Contextual Assistance**
- Real-time coding error detection from screen content
- UI/UX analysis and improvement suggestion from visual inspection
- Document and form understanding from screen capture
- "What is this?" quick-explain overlay for unfamiliar UI elements

**Visual Overlay System**
- Transparent annotation layer rendered above all content using Electron's overlay window
- Step-by-step interactive guidance rendered directly on screen
- Highlight and annotation of referenced screen elements during AI explanation

---

### 7.5 Voice Interaction System

**Pipeline Architecture**

```
Wake Word (Porcupine) → STT (Whisper local / Deepgram cloud) → LLM → TTS (ElevenLabs / Coqui)
                                    ↑ WebSocket audio stream ↑
```

**Capabilities**
- Wake word activation ("Hey GEWN") with configurable sensitivity
- Hold-to-talk alternative for privacy-preferred environments
- High-accuracy continuous speech-to-text with end-of-speech detection
- Interruption handling during TTS playback
- Emotion-aware text-to-speech with natural cadence
- Sub-1.5-second perceived response latency target
- Local STT fallback (Whisper) for Privacy Mode operation

---

### 7.6 AI Memory System

**Architecture: Three-Layer Memory**

| Layer | Technology | Scope | Description |
|---|---|---|---|
| Short-Term | Redis | Session | Current conversation state, recent screen context, active workflow state |
| Long-Term Semantic | PostgreSQL + ChromaDB | Persistent | User preferences, interaction history, learned behavioral patterns, stored knowledge |
| Workflow Memory | ChromaDB | Task-Specific | Recurring task patterns, workflow templates derived from observed user behavior |

**Memory Transparency and Control**
- Users can query what GEWN remembers at any time ("What do you know about me?")
- All stored memories are viewable, editable, and individually deletable via the Memory Panel
- GEWN never stores credentials, passwords, or private keys in the memory system
- Memory contents are encrypted at rest (AES-256-GCM)

**Second Brain Mode**
- Explicit knowledge storage: users can instruct GEWN to remember specific facts, preferences, or project context
- Semantic retrieval: stored knowledge is surfaced contextually during relevant conversations
- Manual knowledge management interface for reviewing and curating stored information

---

### 7.7 RAG — Document Intelligence

**Ingestion Pipeline**
- PDF, Markdown, plain text, and rich text document upload
- Chunking, embedding generation, and vector indexing via ChromaDB
- Automatic document summarization on ingestion

**Retrieval and Interaction**
- Natural language Q&A against uploaded document corpus
- Semantic search returning ranked, source-attributed excerpts
- Cross-document synthesis for research workflows
- Context-aware injection: retrieved content automatically enriches AI reasoning context for related queries
- Note and insight generation from document analysis

---

### 7.8 Autonomous AI Agent Framework

**Agent Roster**

| Agent | Responsibility |
|---|---|
| Coding Agent | Code review, error explanation, fix generation, terminal interaction |
| Research Agent | Web browsing, document synthesis, structured output generation |
| Automation Agent | File system operations, application control, workflow execution |
| Memory Agent | Memory retrieval, storage, pattern extraction, knowledge management |
| Scheduling Agent | Calendar integration, reminder creation, time-based workflow triggers |

**Orchestration Model**
- LangGraph-powered multi-agent coordination with shared context store
- Planning engine decomposes complex goals into ordered, dependency-aware task graphs
- Agents run sequentially or in parallel based on dependency structure
- Background execution with live progress visibility in the overlay
- User cancellation available at every checkpoint
- Full execution log persisted per workflow run

**Safety Constraints on Agents**
- Agents cannot initiate T3/T4 actions without explicit in-session user approval
- Scope enforcement: agents do not expand beyond the boundaries of the user's stated goal
- Failed steps surface clearly with options to retry, skip, or abort — no silent continuation

---

### 7.9 Plugin System *(Phase 6)*

- Python SDK for third-party developers to build custom commands, agents, workflows, and API integrations
- Plugins run in isolated subprocesses with declared permission scopes and resource caps (25% CPU, 512MB RAM)
- No direct access to GEWN's internal memory or the broader file system outside a plugin-specific sandbox directory
- Plugins are code-signed against the GEWN plugin registry

**Core Built-in Integrations**

GitHub · Notion · Gmail · Google Calendar · Slack · Discord · Linear

---

## 8. Functional Requirements

### 8.1 User Interface

- FR-UI-01: GEWN overlay must render above all applications on all active displays at all times
- FR-UI-02: Overlay must be draggable, resizable, and support minimize-to-icon state
- FR-UI-03: A configurable global keyboard shortcut must focus the overlay from any application within 200ms
- FR-UI-04: Chat panel must support streaming response rendering, Markdown, and syntax-highlighted code blocks
- FR-UI-05: Dark futuristic UI theme must be applied consistently; a high-contrast accessibility mode must be available
- FR-UI-06: Interaction mode switching (Standard / Focus / Research / Automation / Voice) must be accessible from the overlay header

### 8.2 Authentication and Session

- FR-AUTH-01: Secure user login and registration with session token management
- FR-AUTH-02: Session persistence across application restarts
- FR-AUTH-03: All credentials and API keys stored in OS-native secure storage (Keychain / Credential Manager / Secret Service)
- FR-AUTH-04: Local encrypted storage for conversation history and user data using AES-256-GCM

### 8.3 AI Interaction

- FR-AI-01: LLM integration must support streaming token delivery to the frontend via WebSocket
- FR-AI-02: Context injection pipeline must combine screen state, memory retrieval, and RAG content before each inference call
- FR-AI-03: Model selection must be configurable; the system must support at minimum OpenAI and Google Gemini providers
- FR-AI-04: Conversation history must be maintained per session and optionally persisted across sessions

### 8.4 Automation

- FR-AUTO-01: All automation actions must be classified into one of four risk tiers before execution
- FR-AUTO-02: T1 actions execute silently; T2 actions display a dismissable toast; T3 actions require explicit approval; T4 actions require typed confirmation with full action preview
- FR-AUTO-03: File path operations must validate against an authorized scope allowlist before execution
- FR-AUTO-04: Terminal commands must be constructed as discrete subprocess argument arrays — never via string interpolation of user input
- FR-AUTO-05: All executed automation actions must be logged with timestamps and outcomes in the tamper-evident audit log

### 8.5 Vision and Screen

- FR-VIS-01: Screenshot pipeline must support on-demand and configurable periodic capture
- FR-VIS-02: OCR extraction must produce text output within 2 seconds for standard screen content
- FR-VIS-03: Multimodal LLM analysis must identify UI elements, code, and document content from screen captures
- FR-VIS-04: Visual overlay system must render transparent annotations above all applications without interfering with user interaction

### 8.6 Voice

- FR-VOICE-01: Wake word detection must operate with configurable sensitivity and less than 300ms activation latency
- FR-VOICE-02: STT pipeline must support both local (Whisper) and cloud (Deepgram) processing, switchable at runtime
- FR-VOICE-03: End-to-end voice response latency (wake word → TTS playback start) must not exceed 1.5 seconds under normal conditions
- FR-VOICE-04: Voice pipeline must handle speaker interruption gracefully

### 8.7 Memory

- FR-MEM-01: Short-term memory must persist for the duration of each session and expire on close unless explicitly promoted
- FR-MEM-02: Long-term memory must persist across sessions and be semantically indexed for retrieval
- FR-MEM-03: Users must be able to view, edit, and delete any stored memory via the Memory Panel
- FR-MEM-04: GEWN must never store credentials, passwords, or private keys in any memory layer

### 8.8 RAG

- FR-RAG-01: Document ingestion must support PDF, Markdown, and plain text formats
- FR-RAG-02: Embedding generation and vector indexing must complete within 30 seconds for documents up to 100 pages
- FR-RAG-03: Semantic search must return source-attributed results with relevance scores
- FR-RAG-04: Retrieved content must be injected into the AI context window automatically for related queries

### 8.9 Agent System

- FR-AGENT-01: Planning engine must decompose multi-step goals into ordered task graphs before execution begins
- FR-AGENT-02: Agents must share state via a common context store accessible to all active agents in a workflow
- FR-AGENT-03: Background workflow execution must display live progress in the overlay with a cancel control at every checkpoint
- FR-AGENT-04: Failed agent steps must surface actionable options (retry / skip / abort) — silent continuation is not permitted

---

## 9. Non-Functional Requirements

### 9.1 Performance

| Metric | Target |
|---|---|
| Overlay focus latency (keyboard shortcut) | < 200ms |
| First token rendered (LLM streaming) | < 800ms |
| Wake word → TTS start | < 1.5 seconds |
| OCR extraction (standard screen) | < 2 seconds |
| Vector retrieval (semantic search) | < 500ms |
| Document ingestion (100 pages) | < 30 seconds |

### 9.2 Reliability

- Graceful degradation when AI providers are unreachable (cached responses, local model fallback)
- Automation safety checks prevent partial execution from leaving the file system in an undefined state
- Agent workflows support checkpoint-based rollback for reversible action sequences
- All T3/T4 actions require explicit approval before execution — no automatic retry on failure

### 9.3 Security

- All external API communication encrypted via TLS 1.3
- Credentials and API keys stored exclusively in OS-native secure enclaves
- All secrets absent from application files, logs, and memory system
- File system operations validated against an authorized scope allowlist; path traversal blocked by design
- Sensitive file patterns (`.env`, private keys, SSH credentials, browser credential stores) blocked from all operations
- Plugin execution sandboxed with resource limits and no internal system access

### 9.4 Privacy

- Privacy Mode routes all processing to local models (Ollama) and local storage; zero external data transmission
- Persistent visual indicator confirms Privacy Mode active state
- Screen capture and OCR data never persisted beyond the immediate inference call unless explicitly instructed by the user
- Prompt injection defense: external content always marked as `[EXTERNAL_CONTENT]` and architecturally separated from system instructions

### 9.5 Scalability

- Modular service architecture with clean boundaries between frontend, API gateway, AI engine, automation layer, vision module, voice pipeline, and memory system
- Each module independently deployable and replaceable
- Agent framework extensible via new agent definitions without core system modification
- Plugin system allows capability extension without modifying the core codebase

### 9.6 Usability

- All critical functions reachable within two interactions from any state
- Permission approval UX designed to be safe without being obstructive
- Reversible actions offer an undo window within the active session
- All AI reasoning and action decisions explainable on request

### 9.7 Maintainability

- Clear module boundaries documented in `ARCHITECTURE.md`
- Backend services containerized via Docker for consistent local and production environments
- CI/CD via GitHub Actions for automated testing and build validation
- Audit log is tamper-evident, append-only, user-owned, and exportable

---

## 10. User Flows and Scenarios

### Scenario 1 — Real-Time Coding Assistance

**User:** A software engineer encounters a runtime error in VS Code.

**Flow:**
1. GEWN's passive screen capture detects an exception stack trace in the active window
2. GEWN proactively surfaces a toast: *"Looks like a TypeError on line 47 — want me to explain it?"*
3. User clicks the toast or says "Yes"
4. GEWN analyzes the stack trace via multimodal LLM, explains the root cause in plain language
5. GEWN offers a corrected code snippet with diff highlighting
6. User clicks "Apply Fix" → GEWN copies the corrected code to clipboard with a confirmation toast
7. Full interaction logged; memory system stores that the user is working on this codebase

---

### Scenario 2 — Natural Language Workflow Automation

**User:** "Organize my downloads folder."

**Flow:**
1. GEWN enters Automation Mode, displays a planning step: *"I'll scan Downloads, categorize by type, and create subfolders. Want me to show you the plan first?"*
2. User confirms
3. GEWN displays a structured plan: folders to be created, categorization logic, estimated file count per category
4. User approves (T2 action — create folders) via single click
5. GEWN executes: creates subdirectories, moves files, reports summary ("Moved 47 files across 6 categories")
6. Reversible undo option displayed for 30 seconds post-completion

---

### Scenario 3 — Research and Document Intelligence

**User:** Uploads three research PDFs, asks: "What are the main arguments across these papers?"

**Flow:**
1. GEWN ingests all three PDFs: chunks, embeds, indexes in ChromaDB
2. Research Agent performs cross-document synthesis via multi-source RAG retrieval
3. GEWN returns a structured comparative summary with source attribution per claim
4. User asks follow-up: "Which author disagrees with the second paper's methodology?"
5. GEWN retrieves relevant passages, identifies the disagreement, surfaces attributed quotes
6. User requests: "Generate study notes from all three" → GEWN produces a structured Markdown note file

---

### Scenario 4 — Workspace Automation

**User:** "Set up my morning coding workspace."

**Flow:**
1. GEWN references workflow memory: user's coding workspace preset (VS Code + Chrome tabs + Notion)
2. If no preset exists, GEWN asks: *"What applications and tabs should I open?"* and stores the answer
3. T1 actions (open apps) execute silently
4. GEWN reports completion: *"Your workspace is ready — VS Code, Chrome with your GitHub dashboard, and Notion are open."*

---

### Scenario 5 — Autonomous Research Agent Workflow

**User:** "Research the top 5 AI agent frameworks and summarize their trade-offs."

**Flow:**
1. Planning engine decomposes the goal into a task graph: [search for frameworks] → [fetch each documentation page] → [compare features] → [synthesize report]
2. Research Agent executes each step via browser automation with live progress displayed
3. At each consequential step (form interaction, downloads), user approval is requested
4. GEWN compiles a structured comparison report and offers to save it as a Markdown file
5. Full workflow run persisted in audit log

---

### Scenario 6 — Proactive Memory Assistance

**User:** Returns to work after a week away and opens their project folder.

**Flow:**
1. GEWN detects the active application context (VS Code, known project path)
2. GEWN cross-references long-term memory: last session context, open issues, incomplete tasks
3. GEWN surfaces a non-intrusive context card: *"Welcome back — last week you were working on the auth module. You left a TODO on line 142. Want to pick up there?"*
4. User clicks "Yes" → GEWN navigates to the relevant line in VS Code

---

## 11. AI Behavior and Safety Model

### 11.1 Risk Tier Classification

Every action GEWN takes is classified into one of four tiers before execution. The tier governs how approval is handled:

| Tier | Examples | User Experience |
|---|---|---|
| **T1 — Low Risk** | Read files, open apps, summarize screen content, web browsing | Execute silently; brief status in overlay |
| **T2 — Medium Risk** | Create files/folders, rename, move items | Dismissable toast with undo option |
| **T3 — High Risk** | Delete files, run terminal commands, send web form data | Blocking confirmation dialog with full action preview; required every time |
| **T4 — Critical Risk** | Modify system settings, send external communications, access sensitive paths | Typed confirmation required + complete action preview |

### 11.2 Core Behavioral Principles

**Capable and Direct** — GEWN leads with answers and actions. It does not over-explain, hedge unnecessarily, or pad responses with disclaimers. It is explicitly honest about the limits of its knowledge.

**Scope Enforcement** — GEWN does not expand beyond what the user requested. If it identifies an opportunity outside the task scope, it surfaces the observation as a suggestion and waits for explicit authorization before acting.

**Hallucination Prevention** — GEWN never generates factual claims about the user's files, system state, or external services without first reading them directly. Uncertainty is surfaced as uncertainty — not filled with plausible-sounding inference.

**Honest Failure Handling** — When a tool fails or a workflow partially completes, GEWN reports clearly: what succeeded, what failed, and what the available options are. It does not automatically retry T3/T4 actions.

**Memory Transparency** — GEWN answers accurately and completely when asked what it remembers. It never stores sensitive personal or credential data in the memory system.

**Prompt Injection Defense** — All external content (documents, web pages, OCR output, clipboard) is injected into the AI context as clearly marked `[EXTERNAL_CONTENT]` data, architecturally isolated from system instructions. Output validation confirms that inferred actions align with the original user request before execution proceeds.

---

## 12. Security Architecture

### 12.1 Threat Model

GEWN operates with screen access, file system control, terminal execution capability, browser automation, and AI reasoning — a high-privilege attack surface that requires defense-in-depth. The security model is designed to contain compromise at every layer.

### 12.2 Key Security Controls

**Principle of Least Privilege** — Every module starts with zero permissions. Access is granted only for the specific resource and minimum duration required.

**File System Safety** — File paths are canonicalized and validated against an authorized scope allowlist before any operation. Path traversal via `../`, symlinks, and encoded separators is blocked by design. Sensitive patterns (private keys, `.env`, SSH credentials, browser credential stores) are blocked from all GEWN operations.

**Command Execution Safety** — Terminal commands are never constructed via string interpolation of user input. Arguments are always passed as discrete subprocess parameters. An allowlist governs which command categories GEWN can invoke without elevated confirmation.

**API Key Security** — All secrets are stored in OS-native secure storage (macOS Keychain, Windows Credential Manager, Linux Secret Service). Keys are never written to application files, logs, or the memory system. All API communication uses TLS 1.3.

**Local Encryption** — Long-term memory, conversation history, and user data are encrypted at rest using AES-256-GCM. The encryption master key is stored in the OS secure enclave and never written to disk in plaintext.

**Plugin Sandboxing** — Plugins execute in isolated subprocesses with declared permission scopes, resource limits (25% CPU, 512MB RAM), and no direct access to GEWN's internal memory or the broader file system outside a plugin-specific directory. Plugins are code-signed against the GEWN plugin registry.

**Privacy Mode** — When activated, all processing routes exclusively to local models and local storage. Zero data is transmitted to external services. A persistent visual indicator confirms Privacy Mode active status.

**Audit Log** — A tamper-evident, append-only log records all consequential actions (file operations, terminal commands, API calls, permission grants) with timestamps and outcomes. The log is user-owned and exportable at any time.

---

## 13. MVP Scope

### 13.1 Included in MVP (Phase 1)

The MVP delivers a functional, useful product that establishes the core value proposition: a floating AI assistant that understands the desktop, can act on it safely, and remembers the user across sessions.

**Floating Overlay UI**
- Draggable, resizable transparent overlay
- Dark futuristic glassmorphism UI theme
- Chat interface with streaming, Markdown, and code rendering
- Global keyboard shortcut activation
- Minimize-to-icon mode

**Conversational AI**
- Multi-provider LLM integration (OpenAI, Gemini)
- Streaming responses via WebSocket
- Session conversation history
- Long-term memory with basic semantic retrieval
- Context injection from screen state and memory

**Desktop Automation**
- Open, close, and switch applications
- Create, rename, move, and organize files and folders
- Four-tier permission system with tiered approval UX
- Basic terminal command execution (T3-gated)

**Screen Awareness**
- On-demand screenshot capture
- OCR text extraction from screen
- Multimodal LLM analysis of screen content
- Contextual assistance based on detected application state

**Voice Interaction**
- Wake word detection
- Speech-to-text (Whisper local + Deepgram cloud)
- Text-to-speech (ElevenLabs cloud + Coqui local)
- Basic real-time voice conversation mode

**Document Intelligence (Basic RAG)**
- PDF and text document upload
- Semantic search and contextual Q&A
- Source-attributed retrieval

**Security Baseline**
- OS-native credential storage
- AES-256-GCM local encryption
- Audit log (append-only)
- Prompt injection defense
- Authorized file scope enforcement

### 13.2 Explicitly Excluded from MVP

The following capabilities are architecturally planned but deferred to later phases to maintain MVP focus:

- Advanced multi-agent orchestration and planning engine (Phase 5)
- Browser automation via Playwright (Phase 3)
- Visual overlay annotation system (Phase 4)
- Plugin SDK and marketplace (Phase 6)
- Cross-device sync and mobile companion (Phase 7)
- Local LLM via Ollama for full Privacy Mode (Phase 7)
- Calendar and scheduling integrations (Phase 6)
- Enterprise collaboration features (Phase 7)
- AR/VR interface layer (post-Phase 7)

---

## 14. Development Roadmap

GEWN is delivered in seven discrete phases, each independently shippable and each building on stable foundations from the previous phase. No phase begins until its predecessor reaches production stability.

| Phase | Focus | Key Deliverables | Timeline Estimate |
|---|---|---|---|
| **Phase 1 — MVP Core** | Floating overlay, conversational AI, basic memory, file/app control, basic RAG | Working desktop companion with conversation, memory, and safe automation | 10–16 weeks |
| **Phase 2 — Voice AI** | Full voice pipeline, wake word, STT/TTS, real-time voice mode | Hands-free operation; sub-1.5s end-to-end latency | 8–12 weeks |
| **Phase 3 — Desktop Automation** | Advanced file management, browser automation (Playwright), workflow presets, task scheduler | Complex cross-application automation; web research workflows | 10–14 weeks |
| **Phase 4 — Vision and Context** | Full OCR pipeline, screen understanding, coding error detection, visual overlay annotations, proactive assistance | GEWN detects and responds to screen events without prompting | 10–14 weeks |
| **Phase 5 — Autonomous Agents** | Multi-agent orchestration (LangGraph), planning engine, background task execution, agent coordination | Complex multi-step autonomous goals; background agent workflows | 12–16 weeks |
| **Phase 6 — Plugin Ecosystem** | Developer SDK, plugin sandboxing, core integrations (GitHub, Notion, Gmail, Slack, Linear, Calendar), plugin registry | Extensible platform; third-party developer support | 12–16 weeks |
| **Phase 7 — Multi-Device and Enterprise** | Cross-device sync, mobile companion app, local LLM (Ollama), enterprise workspace features | Full offline capability; mobile extension; team features | 14–20 weeks |

**Guiding Principle:** Ship something genuinely useful before adding something ambitious. Each phase must produce a better product than the previous phase — not just more features.

### 14.1 Phase 1 Milestones

| Milestone | Deliverable |
|---|---|
| M1.1 | Electron overlay shell: window launches, floats, drags, minimizes |
| M1.2 | Chat interface with streaming LLM responses via WebSocket |
| M1.3 | Short-term session memory; conversation history persistence |
| M1.4 | Basic file and application automation with T1/T2/T3 permission UX |
| M1.5 | On-demand screenshot capture and OCR extraction |
| M1.6 | Long-term semantic memory (ChromaDB) with basic retrieval |
| M1.7 | PDF ingestion and basic RAG Q&A |
| M1.8 | Security baseline: credential storage, encryption, audit log |

---

## 15. Technical Architecture

### 15.1 System Overview

```
┌──────────────────────────────────────────────────┐
│             Electron Desktop Overlay              │
│          React UI  ·  Voice UI  ·  Overlays       │
└───────────────────────┬──────────────────────────┘
                        │  WebSocket + REST
                        ▼
┌──────────────────────────────────────────────────┐
│              FastAPI Backend Core                  │
│      API Gateway  ·  Auth  ·  Orchestration       │
└──────┬──────────────┬─────────────────┬───────────┘
       │              │                 │
       ▼              ▼                 ▼
┌──────────┐  ┌──────────────┐  ┌──────────────────┐
│ AI Engine│  │ Automation   │  │  Vision Module   │
│ + Agents │  │ Tool Layer   │  │  OCR + Screen    │
└────┬─────┘  └──────┬───────┘  └──────────────────┘
     │               │
     ▼               ▼
┌──────────┐  ┌──────────────────────────────────┐
│ Memory   │  │         Database Layer            │
│ System   │  │  PostgreSQL · Redis · ChromaDB    │
└──────────┘  └──────────────────────────────────┘
```

### 15.2 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Desktop Framework | Electron | Cross-platform overlay with OS-level access and transparent window support |
| UI Framework | React + Tailwind CSS + Framer Motion | Component-based UI with performant animation and utility-first styling |
| Backend | Python + FastAPI + WebSockets | High-performance async API with native AI/ML library ecosystem |
| LLM Providers | OpenAI API, Google Gemini API | Frontier model access; multi-provider for resilience and model selection |
| Agent Orchestration | LangChain + LangGraph | Tool-calling abstraction and stateful multi-agent coordination |
| Wake Word | Porcupine | Lightweight on-device wake word detection; low CPU overhead |
| Speech-to-Text | Whisper (local), Deepgram (cloud) | Local for Privacy Mode; cloud for quality and speed |
| Text-to-Speech | ElevenLabs (cloud), Coqui TTS (local) | Natural voice quality; local fallback for Privacy Mode |
| Desktop Automation | PyAutoGUI | Cross-platform OS-level GUI interaction |
| Browser Automation | Playwright | Modern, reliable browser control with async support |
| OCR | PaddleOCR (primary), Tesseract (fallback) | High accuracy; open-source; local execution |
| Vector Database | ChromaDB (local), Pinecone (cloud option) | Semantic embedding storage and retrieval for memory and RAG |
| Relational Database | PostgreSQL | Structured persistent storage for user data and conversation history |
| Cache / Session | Redis | Fast in-memory session state and short-term memory |
| Local LLM | Ollama | Full offline inference for Privacy Mode (Phase 7) |
| DevOps | Docker + GitHub Actions | Consistent environments; automated CI/CD |

### 15.3 Data Flow — Standard Query

```
User Input (text or voice)
    → Frontend captures input and current screen state
    → WebSocket sends to FastAPI
    → Memory Agent retrieves relevant long-term context
    → RAG pipeline retrieves relevant document context (if applicable)
    → Context assembled: [system prompt] + [screen state] + [memory] + [RAG] + [user input]
    → LLM inference with streaming
    → Stream tokens back to frontend via WebSocket
    → If action detected: classify tier → request approval → execute → log
```

---

## 16. Risk Analysis

### 16.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| LLM API latency degrades real-time UX | Medium | High | Streaming rendering; multi-provider fallback; local model option in Privacy Mode |
| OCR accuracy insufficient for complex UIs | Medium | Medium | Multi-engine fallback (PaddleOCR + Tesseract); multimodal LLM as verification layer |
| Desktop automation breaks across OS updates | High | Medium | Comprehensive OS compatibility testing; abstraction layer over PyAutoGUI |
| Memory system context window overflow on long sessions | Medium | Medium | Intelligent memory summarization and compression; tiered eviction policy |
| Agent orchestration complexity introduces reliability failures | Medium | High | Checkpoint-based execution; explicit failure surfacing; no silent continuation |

### 16.2 Security Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Prompt injection via malicious document content | Medium | High | Architectural separation of external content; output validation against original intent |
| Unauthorized file system access via crafted inputs | Low | Critical | Path canonicalization; scope allowlist enforcement; sensitive pattern blocklist |
| API key exfiltration | Low | Critical | OS-native secure storage only; keys absent from all logs and memory |
| Plugin executing malicious code | Low | High | Code signing; sandboxed subprocess execution; resource limits |

### 16.3 Privacy Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Screen content containing sensitive data sent to cloud LLM | Medium | High | User-configurable screen capture controls; Privacy Mode for full local processing |
| Memory system storing inadvertently sensitive information | Medium | Medium | Explicit blocklist for credential patterns; full user memory transparency and deletion |
| Voice pipeline transmitting audio to cloud STT without consent | Low | High | Clear disclosure of STT provider; local Whisper option; no audio retention |

### 16.4 Product and Business Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| AI hallucinations cause incorrect automation actions | Medium | High | Require confirmation for all file-modifying actions; no silent automation of T3/T4 |
| System performance impact from passive screen monitoring | Medium | Medium | Configurable capture frequency; smart activation only when GEWN is focused |
| Cross-platform inconsistency (macOS / Windows / Linux) | High | Medium | Platform abstraction layers; phased OS support (macOS first, then Windows) |
| User trust loss from unexpected autonomous action | Low | Critical | Strict permission tier enforcement; comprehensive audit log; undo windows |

---

## 17. Success Metrics

### 17.1 Product Health Metrics

| Metric | Description | Target (90 days post-launch) |
|---|---|---|
| Daily Active Users | Unique users opening GEWN on a given day | Growth trend; absolute target TBD by market size |
| Session Duration | Average time GEWN is actively used per day | > 20 minutes |
| Day-7 Retention | % of new users returning after 7 days | > 40% |
| Day-30 Retention | % of new users returning after 30 days | > 25% |
| Automation Adoption | % of MAU who execute at least one automation per week | > 50% |
| Memory Utilization | % of MAU whose long-term memory contains > 10 stored facts | > 60% |

### 17.2 AI Quality Metrics

| Metric | Description | Target |
|---|---|---|
| Task Completion Rate | % of user-initiated tasks that reach the user's intended outcome | > 80% |
| Automation Success Rate | % of automation workflows that complete without user-initiated abort | > 90% |
| RAG Retrieval Relevance | User-rated relevance of document Q&A responses (sampled) | > 4.0 / 5.0 |
| Context Accuracy | % of responses that correctly reference current screen or session state | > 85% |
| Memory Retrieval Quality | % of memory retrievals rated as relevant by users (sampled) | > 4.0 / 5.0 |

### 17.3 User Experience Metrics

| Metric | Target |
|---|---|
| Overlay activation latency | < 200ms p95 |
| First token rendered (LLM) | < 800ms p95 |
| Voice end-to-end latency | < 1.5 seconds p95 |
| User satisfaction (post-session survey, sampled) | > 4.2 / 5.0 |
| Permission dialog abandonment rate (T3/T4) | < 10% |

### 17.4 Leading Indicators (Early Validation)

- Number of automation workflows saved as presets (indicates perceived utility)
- Number of explicit memory store requests per user (indicates trust in memory system)
- RAG document upload count per user (indicates adoption of document intelligence)
- Plugin installations per active user (Phase 6 onward)

---

## 18. Future Scalability

### 18.1 Multi-Agent Ecosystem Expansion

Beyond the five core agents in Phase 5, the agent framework is designed to support an unlimited registry of specialized agents. Planned future agents include a Writing Agent (long-form content generation and editing), a Finance Agent (budget and transaction analysis), and a Health Agent (habit tracking and wellness workflow automation).

### 18.2 Plugin Marketplace

A developer-facing plugin marketplace enabling third-party builders to extend GEWN with new commands, agents, workflow templates, and API integrations. Revenue model options include revenue sharing on premium plugins and a free tier for open-source contributions.

### 18.3 Cross-Device Continuity

A mobile companion app (iOS + Android) that extends GEWN's memory and AI context to mobile workflows. Cross-device sync allows memory, conversation history, and workflow state to be available across all user devices. End-to-end encrypted sync via user-controlled cloud storage.

### 18.4 Local AI Infrastructure

Full offline operation via Ollama-based local LLM inference, eliminating dependency on cloud AI providers for users who require complete data sovereignty or operate in air-gapped environments.

### 18.5 Enterprise AI Workspace

Team-level GEWN deployment with shared workflow templates, centralized IT policy control, audit log aggregation, and collaborative agent workflows. Enterprise tier supports SSO, custom plugin allowlists, and admin dashboards.

### 18.6 Adaptive Operating System Layer

Long-term exploration of GEWN as an OS-level capability — integrating with kernel-level APIs, accessibility frameworks, and system event hooks to provide even deeper context awareness and lower-latency automation with reduced screen-scraping dependency.

---

## 19. Constraints

### 19.1 Technical Constraints

- Desktop automation depends on OS-level permission grants that vary by platform and OS version; some capabilities require explicit user permission on macOS (Accessibility, Screen Recording, Full Disk Access)
- LLM inference latency is subject to provider API performance; real-time responsiveness targets cannot be guaranteed under API degradation
- Local resource consumption (CPU, RAM) must be actively managed to avoid impacting the user's primary workflows; passive monitoring must be configurable

### 19.2 Platform Constraints

- Phase 1 targets macOS as the primary development platform; Windows support follows in Phase 3; Linux community support in Phase 4
- Electron's cross-platform window management has documented inconsistencies between platforms that require platform-specific handling

### 19.3 Financial Constraints

- LLM API usage costs scale directly with active user count and context window size; cost modeling must be incorporated into pricing design from Phase 1
- Vector database scaling costs (Pinecone cloud option) require monitoring at scale
- Voice pipeline cloud costs (Deepgram STT, ElevenLabs TTS) require usage caps or tiered plans for cost management

### 19.4 Regulatory Constraints

- Screen content capture and processing may be subject to data protection regulation (GDPR, CCPA) in certain markets; Privacy Mode and local-only processing options are the primary compliance strategy
- Enterprise deployments may require SOC 2 compliance consideration before Phase 7

---

## 20. Glossary

| Term | Definition |
|---|---|
| **Overlay** | The Electron-powered transparent floating window that serves as GEWN's primary interface |
| **Automation Tier** | The risk classification (T1–T4) assigned to each action before execution |
| **RAG** | Retrieval-Augmented Generation — the pipeline for injecting retrieved document content into LLM reasoning context |
| **Memory Agent** | The AI agent responsible for storing, retrieving, and managing all layers of GEWN's memory system |
| **Planning Engine** | The LangGraph-powered component that decomposes complex multi-step goals into ordered, executable task graphs |
| **Second Brain Mode** | The explicit user-directed knowledge storage mode that allows intentional information storage in long-term memory |
| **Privacy Mode** | The operational mode in which all processing routes to local models and local storage; zero external data transmission |
| **Glassmorphism** | The frosted-glass UI aesthetic applied to GEWN's overlay: semi-transparent background with blur effect |
| **Context Injection** | The process of combining screen state, memory retrieval, and RAG content into the LLM input before each inference call |
| **Scope Enforcement** | The behavioral constraint that prevents GEWN from taking actions outside the explicit boundaries of a user request |
| **Audit Log** | The tamper-evident, append-only record of all consequential actions taken by GEWN |
| **Plugin Registry** | The code-signed distribution system for third-party GEWN plugins |

---

*This document is the source of truth for Project GEWN's product requirements. All feature development, architectural decisions, and scope trade-offs should be evaluated against the goals, constraints, and principles defined here. This document is maintained by the GEWN core team and versioned alongside the codebase.*

*Related documents: `ARCHITECTURE.md` · `FEATURES.md` · `ROADMAP.md` · `AI_BEHAVIOR.md` · `SECURITY_NOTES.md` · `USER_FLOW.md`*
