# Product Requirements Document (PRD)
## The Lenny Growth Assistant

**Version:** 1.0.0  
**Role:** Forward Deployed Engineer (FDE)  
**Status:** Approved & Operational  
**Target Deployment:** Local (Docker / Python+Node) & Enterprise Cloud  

---

## 1. Executive Summary & Problem Framing

*Lenny's Podcast* contains over 300 in-depth conversations with premier Silicon Valley founders, growth executives, and product leaders (e.g., Brian Chesky, Shreyas Doshi, Elena Verna, Marty Cagan, Sean Ellis). While this archive represents world-class tactical knowledge on product-market fit, growth loops, pricing, organizational design, and retention, accessing it in daily decision-making is severely constrained:
- Over 250+ hours of spoken audio is unindexed for quick tactical lookup.
- Search queries in standard transcripts lack thematic synthesis and contextual grounding.
- General LLMs (e.g., vanilla ChatGPT) hallucinate generic PM advice instead of citing specific operational frameworks proven by actual operators.
- PMs and Growth teams spend hours synthesizing raw notes into executive memos or team essays.

**The Solution:**
**The Lenny Growth Assistant** is an enterprise-grade, retrieval-augmented conversational assistant that:
1. Ingests and indexes the full corpus of Lenny's Podcast transcripts.
2. Grounds all answers strictly in speaker quotes and timestamped episode references.
3. Automatically executes specialized skills—notably a **Ship 30 for 30 Content Engine** producing ~1,250-word high-retention essays.
4. Generates live, renderable interactive artifacts (HTML/CSS tools, dashboards, and Markdown strategy documents) in a secure, sandboxed side-by-side Claude-style viewer.
5. Provides a flexible dual-runtime LLM layer supporting local offline inference via **Ollama** alongside cloud providers (**Anthropic Claude** and **OpenAI**).

---

## 2. Forward Deployment Brief

### 2.1 Primary User & Persona
- **Role:** Growth Product Manager, Head of Product, or Early-Stage Founder.
- **Job to Be Done (JTBD):**
  > *"When I am designing a growth experiment, pricing change, or product strategy, I want to immediately pull battle-tested heuristics from proven operators who have solved this exact problem, so that I don't waste months reinventing the wheel or relying on generic advice."*
- **Pain Relieved:** Eliminates 3–5 hours of manual podcast search and transcript skimming per research cycle; eliminates generic, ungrounded LLM hallucinations.

### 2.2 Measurable Success Metrics
| Metric Category | Metric | Target | Verification Method |
| :--- | :--- | :--- | :--- |
| **Grounding & Accuracy** | Citation Precision Rate | $\ge 90\%$ | Proportion of claims mapped to verifiable episode & speaker timestamps. |
| **Grounding & Refusal** | Out-of-Domain Refusal Rate | $100\%$ | Explicit refusal when query falls outside the transcript archive. |
| **Performance** | Local Inference TTFT | $< 4.0\text{ s}$ | Time to First Token on standard local hardware via Ollama. |
| **Content Quality** | Ship 30 Compliance | $\approx 1,250\text{ words}$ | Adherence to hook, 1–3 sentence paragraphs, bold anchors, and takeaway checklist. |
| **Security** | Artifact Render Isolation | $0\text{ XSS}$ | Untrusted HTML execution blocked from parent cookies, storage, and DOM via sandbox. |

### 2.3 Key Assumptions (Addressing Brief Ambiguities)
1. **Model Availability:** The client evaluator may or may not have an active GPU or pre-pulled Ollama weights. The system must default to Ollama but provide seamless UI switching to Cloud LLMs or a deterministic mock provider for zero-downtime evaluation.
2. **Database Infrastructure:** While PostgreSQL + `pgvector` is the enterprise target, the application provides an automated fallback to SQLite vector search so the system can run immediately without requiring Docker or a local Postgres daemon.
3. **Artifact Interactivity:** Users require both pure Markdown strategy documents and executable HTML/CSS micro-apps (e.g., viral loop calculators, CAC:LTV estimators).

### 2.4 Scope Boundaries
- **Included in Scope:**
  - Automated transcript parsing (YAML frontmatter, speaker turns, timestamp extraction).
  - High-performance vector retrieval with cosine similarity and relevance thresholding.
  - Server-Sent Events (SSE) streaming API for real-time token delivery.
  - Chat session persistence across browser reloads.
  - Specialized Ship 30 for 30 skill with deep heuristic formatting.
  - Claude-style side-by-side Artifact Viewer with Code/Preview tabs, Copy, and Download.
  - Hardened iframe sandboxing with DOMPurify sanitization.
- **Intentionally Excluded:**
  - Live audio transcription (the system leverages high-fidelity pre-transcribed text).
  - Multi-tenant enterprise SSO (simplifies local forward-deployment evaluation).

### 2.5 Risks, Mitigations & Trade-offs
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Local LLM Hallucination** | High | System prompt strictly penalizes ungrounded statements and enforces `[Episode: Guest, Timestamp]` citations; low temperature ($0.2\text{--}0.3$). |
| **Context Window Overflow** | Medium | Dynamic chunk reranking: top-$K$ ($K=4\text{--}6$) high-similarity segments are injected rather than full transcripts. |
| **XSS / Malicious HTML in Artifacts** | Critical | Two-tier defense: `DOMPurify` HTML sanitization + strict iframe sandboxing (`sandbox="allow-scripts"` with NO `allow-same-origin`). |
| **Local Ollama Unavailability** | Medium | Health probe alerts user in UI with one-click toggle to cloud API or demo fallback. |

---

## 3. Core Functional Requirements

### 3.1 Session & Chat Persistence
- `POST /api/sessions`: Creates an isolated session with UUID and auto-generated or user-provided title.
- `GET /api/sessions`: Returns all historical chat sessions ordered by `updated_at DESC`.
- `GET /api/sessions/{session_id}`: Retrieves full message history and associated generated artifacts.
- `DELETE /api/sessions/{session_id}`: Deletes session and cascaded records.

### 3.2 Dynamic Retrieval-Augmented Generation (RAG)
- Extracts top-$K$ relevant chunks from the podcast corpus based on cosine distance.
- Applies a similarity threshold ($\ge 0.60$ cosine similarity score).
- Formats retrieved chunks into system context with metadata tags:
  ```
  [Source ID: 1] Episode: Brian Chesky's new playbook | Guest: Brian Chesky | Timestamp: 00:00:38
  ```
- If no chunks pass the threshold, executes the grounded refusal protocol:
  > *"I do not have sufficient information in Lenny's podcast archive to answer this question. My answers are strictly limited to verified statements from Lenny's guests."*

### 3.3 Ship 30 for 30 Content Skill
- Triggered either via prompt intent detection or explicit UI mode toggle ("Ship 30 for 30 Mode").
- System constructs a specialized prompt instructing the LLM:
  - **Hook:** High-tension opening statement or counterintuitive data point.
  - **Length:** Target ~1,250 words.
  - **Cadence:** Short, high-velocity paragraphs (1–3 sentences).
  - **Visual Rhythm:** Bold anchor words at the start of bullet points, sub-headers every 150–200 words.
  - **Takeaway:** Concrete operational checklist or actionable framework attributed to the guests.

### 3.4 Claude-Style Artifact Viewer
- Artifacts are emitted by the LLM using XML/HTML boundary tags:
  ```xml
  <artifact type="html" title="Product-Led Growth Loop Calculator">
    ... HTML/CSS/JS ...
  </artifact>
  ```
- The frontend parses tokens in real time, extracts the artifact, and renders a side-by-side drawer.
- Provides two viewing modes: **Preview** (live rendering) and **Code** (syntax-highlighted source).
- Allows one-click **Copy to Clipboard** and **Download File** (`.html` or `.md`).

---

## 4. Operational & Non-Functional Requirements
1. **Portability:** Single-command startup via `docker-compose up` or `run_local.ps1` / `run_local.sh`.
2. **Reliability:** Graceful error handling for missing keys, network timeouts, and model rate limits.
3. **Observability:** Structured JSON logging on every API call and retrieval query.
4. **Clean Codebase:** Full test coverage with `pytest` for API routes, retriever logic, and security filters.
