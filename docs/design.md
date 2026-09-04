# UI/UX Design Specification
## The Lenny Growth Assistant

**Version:** 1.0.0  
**Design System:** Modern Minimalist / High-Signal Editorial (Tailwind CSS)  
**Reference Model:** Claude Artifacts + Lenny's Newsletter Aesthetic  

---

## 1. Design Philosophy & Principles

1. **Substance Over Gimmicks:** The assistant exists to answer high-stakes product strategy questions. Typography, spacing, and hierarchy should feel like reading a premier product essay, not a generic toy chatbot.
2. **Side-by-Side Co-creation:** Inspired by Claude Artifacts, generated tools, essays, and HTML components live alongside the conversation rather than being lost in an endless chat thread.
3. **Transparent Grounding:** Every claim has a visible citation pill. Clicking or hovering a citation reveals the guest, episode title, and timestamp.
4. **Immediate Operability:** The user can instantly switch models (Ollama vs. Cloud), create new sessions, toggle the Ship 30 for 30 engine, and copy or download artifacts with zero friction.

---

## 2. Information Architecture & Spatial Layout

The workspace is organized into a clean 3-zone layout:

```
+------------------+----------------------------------+------------------------------------+
|  Navigation /    |          Chat Workspace          |          Artifact Viewer           |
|  Session Drawer  |                                  |        (Claude-Style Drawer)       |
|  (260px)         |          (Flexible 50-60%)       |         (Flexible 40-50%)          |
+------------------+----------------------------------+------------------------------------+
| [New Chat +]     | Header: Model Selector & Health  | Header: Title, Type Pill, Actions  |
|                  |                                  | Tabs: [Preview] [Source Code]      |
| Recent Sessions: | Message Stream:                  |                                    |
| - Chesky Airbnb  | - User bubble                    | Main Render Window:                |
| - PLG Loops      | - Assistant bubble               | - Sandboxed iframe or              |
| - Pricing Power  |   - Grounded Answer Markdown     | - Formatted Markdown reader        |
|                  |   - [Source Pills]               |                                    |
| Footer:          |   - [<Artifact Card>]            | Footer:                            |
| - Storage Mode   |                                  | - [Copy Code] [Download File]      |
| - Health Status  | Input Area:                      | - [Close Artifact X]               |
|                  | - Mode Toggle (Default / Ship30) |                                    |
|                  | - Textarea & Send Button         |                                    |
+------------------+----------------------------------+------------------------------------+
```

### 2.1 Zone 1: Navigation & Session Drawer (Collapsible)
- **Top:** "New Chat" button with keyboard shortcut (`Cmd/Ctrl + K`).
- **List:** Chronologically sorted chat sessions grouped by "Today", "Previous 7 Days", and "Older".
- **Bottom:** Operational telemetry widget showing DB status, Ollama connection status, and version tag.

### 2.2 Zone 2: Main Conversational Area
- **Header Bar:**
  - Application Title with Lenny's Podcast badge.
  - **Dynamic Model Selector:** Badge displaying active model (`Ollama: llama3.2`, `Claude 3.5 Sonnet`, `GPT-4o`, `Demo Mode`) with latency indicators.
  - Health probe status indicator (Green = healthy, Amber = degraded, Red = offline).
- **Chat Stream:**
  - Markdown-rendered assistant responses with rich table, bold, and code formatting.
  - **Citation Pills:** Interactive source tags formatted as `[1: Brian Chesky, 00:04:12]`. Clicking opens an inline drawer with the exact transcript excerpt.
  - **Artifact Trigger Card:** When an artifact is generated, a card appears in the chat:
    ```
    +-------------------------------------------------------------+
    | [Icon] Interactive HTML: Product-Led Growth ROI Calculator  |
    | Generated for this session                 [Open Artifact ->] |
    +-------------------------------------------------------------+
    ```
- **Composer / Prompt Bar:**
  - Auto-expanding textarea.
  - **Mode Selector:** Toggle between **"Standard RAG"** (tactical Q&A) and **"Ship 30 for 30"** (long-form essay engine).
  - Quick Suggestion Prompts for instant discovery (e.g., *"How did Brian Chesky restructure PM at Airbnb?"*, *"What are Elena Verna's 4 B2B growth loops?"*).

### 2.3 Zone 3: Claude-Style Artifact Viewer
- Slides out smoothly from the right when an artifact is emitted or clicked.
- **Top Actions:**
  - Title and Artifact Type Badge (`HTML/CSS Interactive` or `Markdown Document`).
  - **View Tabs:** `[Preview]` (live execution) and `[Source]` (raw syntax-highlighted code).
  - **Utility Buttons:** Copy to Clipboard (with copied confirmation checkmark), Download (`.html` or `.md`), Expand to Fullscreen, and Close (`X`).
- **Body Area:**
  - For HTML: Mounts the sandboxed `iframe` with inline CSS/JS.
  - For Markdown: Renders clean editorial typography with KaTeX math and GFM table support.

---

## 3. Interaction States & Transitions

| State | User Experience & Visual Treatment |
| :--- | :--- |
| **Empty State** | Clean hero view with prompt starters, explanation of knowledge base, and model readiness status. |
| **Retrieval State** | Animated pulsing indicator: *"Searching 300+ Lenny transcripts..."* with guest names matched. |
| **Streaming State** | Real-time token streaming with smooth auto-scroll. If an artifact tag is detected, the artifact drawer opens automatically. |
| **Refusal State** | Friendly informational callout when a query is out-of-domain: *"I do not have sufficient information in Lenny's podcast archive..."* with suggested related product topics. |
| **Offline Ollama State** | Prominent notification banner: *"Ollama is offline on localhost:11434. Automatically falling back to Demo Provider or Cloud Provider."* |

---

## 4. Accessibility & Responsive Design

- **WCAG 2.1 AA Compliance:** Minimum contrast ratio of 4.5:1 for all normal text, 3:1 for large headers.
- **Keyboard Navigation:** Full tab order navigation across sidebar, chat input, mode toggle, and artifact controls. Esc key closes modal drawers and fullscreen views.
- **Screen Reader Support:** Semantic ARIA labels for streaming regions (`aria-live="polite"`), buttons, and iframe titles.
- **Responsive Layout:**
  - Large Screens ($\ge 1280\text{px}$): Full 3-column layout (Sidebar + Chat + Artifact).
  - Medium Screens ($768\text{px}\text{--}1279\text{px}$): Collapsible sidebar; Chat and Artifact share split view.
  - Mobile ($< 768\text{px}$): Single-column stack with tabs switching between "Chat" and "Artifact".
