# The Lenny Growth Assistant

An enterprise-grade, retrieval-augmented conversational assistant and content engine powered by **Lenny's Podcast** transcripts. Built for product managers, growth leaders, and founders who demand battle-tested, grounded insights from top operators—without the prompt engineering overhead.

---

## Highlights & Capabilities

- **Strictly Grounded Retrieval:** Extracts tactical wisdom from 300+ podcast episodes (Brian Chesky, Elena Verna, Shreyas Doshi, Marty Cagan, etc.) with timestamped citations: `[Episode: Title, Guest: Name, Timestamp: HH:MM:SS]`.
- **Out-of-Domain Refusal Protocol:** Rejects irrelevant or ungrounded queries with a polite explanation when the archive does not support the answer.
- **Ship 30 for 30 Content Engine:** Dedicated skill transforming raw answers into high-retention ~1,250-word essays adhering to Dickie Bush & Nicolas Cole's structural heuristics (counterintuitive hooks, 1–3 sentence paragraphs, bold anchors, and actionable checklists).
- **Claude-Style Sandboxed Artifact Viewer:** Renders interactive HTML/CSS micro-tools (growth loop calculators, ROI models) and Markdown playbooks in a side-by-side drawer with live preview, code inspection, clipboard copy, and file download.
- **Untrusted HTML Security Isolation:** Hardened two-tier defense combining `DOMPurify` sanitization with strict iframe sandboxing (`sandbox="allow-scripts"` without `allow-same-origin`) to completely prevent parent window, cookie, and storage access.
- **Dynamic Dual-Runtime LLM Layer:** Seamlessly switch between local offline inference (**Ollama** with `llama3.2:3b` / `llama3.1:8b`), cloud intelligence (**Anthropic Claude 3.5 Sonnet** and **OpenAI GPT-4o**), and a deterministic **Evaluation Demo Provider** directly in the UI.
- **Zero-Dependency Persistence:** Supports PostgreSQL with `pgvector` via Docker Compose or Supabase/Railway, alongside an automatic local SQLite fallback for instant zero-dependency local evaluation.

---

## Architecture Overview

```
                  +--------------------------------------------------+
                  |               React + Vite Frontend              |
                  |  - Chat Pane (Streaming SSE, Citations, Modes)   |
                  |  - Model Selector (Ollama / Cloud / Demo)        |
                  |  - Sandboxed Artifact Viewer (DOMPurify+Iframe)  |
                  +-------------------------+------------------------+
                                            |
                                HTTP / SSE  | /api/sessions, /api/chat, /api/health
                                            v
                  +--------------------------------------------------+
                  |                 FastAPI Backend                  |
                  |  - CORS, Error Handling, Structured JSON Logging |
                  |  - Dynamic LLM Router (Ollama, Claude, OpenAI)   |
                  |  - Ship 30 for 30 Skill Engine                   |
                  |  - Artifact Extraction & Verification Parser     |
                  +------------+-------------------------+-----------+
                               |                         |
                               v                         v
                 +-----------------------+     +--------------------+
                 |    Vector Retriever   |     | Persistence Layer  |
                 | - Hybrid/Cosine RAG   |     | - Sessions         |
                 | - Strict Thresholding |     | - Messages         |
                 | - Source Attribution  |     | - Artifacts        |
                 +-----------+-----------+     +---------+----------+
                             |                           |
                             +-------------+-------------+
                                           |
                                           v
                 +--------------------------------------------------+
                 |            Database (Async SQLAlchemy)           |
                 |  - Primary: PostgreSQL 16 with pgvector          |
                 |  - Zero-Dep Fallback: SQLite + Cosine Vectors    |
                 +--------------------------------------------------+
```

---

## Quick Start (One Command)

### Option A: Local Python & Pre-built Web App (Recommended for Fast Evaluation)

The repository includes pre-seeded landmark episodes and a pre-compiled frontend bundle. You can launch the complete full-stack app on a single port (`http://localhost:8000`) in seconds:

**PowerShell (Windows):**
```powershell
.\run_local.ps1
```

**Bash (macOS / Linux / WSL):**
```bash
chmod +x run_local.sh
./run_local.sh
```

**Command Prompt (Windows):**
```cmd
run_local.bat
```

Open **http://localhost:8000** in your browser.

---

### Option B: Docker Compose (Full Multi-Container Stack)

To run PostgreSQL with native `pgvector`, FastAPI backend, and Nginx frontend in Docker:

```bash
docker-compose up --build
```

- Web Interface: `http://localhost:3000`
- API Backend & Swagger Docs: `http://localhost:8000/docs`
- Health Diagnostics: `http://localhost:8000/api/health`

---

## Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./lenny_assistant.db` | Async SQLAlchemy DB connection string (PostgreSQL or SQLite). |
| `DEFAULT_LLM_PROVIDER` | `ollama` | Active provider: `ollama`, `claude`, `openai`, or `mock`. |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint. |
| `OLLAMA_MODEL` | `llama3.2:3b` | Target local model (e.g., `llama3.2:3b`, `llama3.1:8b`). |
| `ANTHROPIC_API_KEY` | *(Optional)* | Required only for Claude 3.5 Sonnet cloud mode. |
| `ANTHROPIC_MODEL` | `claude-3-5-sonnet-20241022` | Anthropic model identifier. |
| `OPENAI_API_KEY` | *(Optional)* | Required only for OpenAI GPT-4o cloud mode. |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model identifier. |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Allowed frontend origins. |

---

## LLM Provider Setup

### 1. Local LLM (Ollama) — Mandatory for Demo Evaluation
1. Download and start [Ollama](https://ollama.com/):
   ```bash
   ollama serve
   ```
2. Pull the recommended evaluation model:
   ```bash
   ollama pull llama3.2:3b
   ```
   *(Or `llama3.1:8b` if your machine has 16GB+ RAM).*
3. The UI will automatically display **"Ollama Online"** with a green badge.

### 2. Cloud LLM (Claude or OpenAI)
- Add your `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in `.env`.
- Switch the provider badge in the top right header to **Anthropic Claude** or **OpenAI GPT-4o**.

### 3. Evaluation Demo Provider (Zero-Dependency Fallback)
- If Ollama is not installed and no API keys are available, select **"Evaluation Demo Provider"** in the header.
- Provides deterministic, streaming responses, Ship 30 essays, and interactive artifacts for offline verification.

---

## Knowledge Base & Ingestion Pipeline

Transcripts are sourced from the official [ChatPRD Lenny's Podcast Transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts) repository (303 episodes).

### How It Works:
1. **Parsing:** Extracts YAML frontmatter (`guest`, `title`, `youtube_url`, `publish_date`, `keywords`).
2. **Turn Splitting:** Identifies speaker tags and timestamps (`Speaker (HH:MM:SS):`).
3. **Windowed Chunking:** Segments dialogue into 400–600 word chunks with 50-word overlap to preserve conversational context.
4. **Vector Embeddings:** Generates normalized 384-dimensional dense vectors stored in PostgreSQL `pgvector` or SQLite.

### Running Ingestion:
To re-index or ingest the entire archive (all 303 episodes):
```bash
python backend/scripts/ingest.py 0
```
To ingest a specific number of landmark episodes (e.g., top 15):
```bash
python backend/scripts/ingest.py 15
```

---

## Artifact Security & Isolation Architecture

When users request interactive tools or dashboards, the assistant generates complete HTML/CSS/JS components inside an `<artifact>` block.

### Security Threat Model & Defense:
1. **Tier 1: HTML Sanitization (`DOMPurify`):**
   Neutralizes malicious tags and URI protocols before injecting markup.
2. **Tier 2: Hardened Sandboxed Iframe (`srcdoc`):**
   ```html
   <iframe
     title="Artifact Preview"
     srcdoc={cleanHtml}
     sandbox="allow-scripts"
     referrerpolicy="no-referrer"
   />
   ```
   **Critical Decision:** `allow-same-origin` is **intentionally omitted**. This ensures:
   - Scripts inside the artifact execute in a unique, opaque origin.
   - The artifact cannot access `window.parent`, cookies, `localStorage`, or session data.
   - Interactive widgets (sliders, inputs, canvas animations) function smoothly without security risk.

---

## Automated Tests

Run the complete backend automated test suite:

```bash
python -m pytest backend/tests -v
```

### Test Coverage (10/10 Passing):
- `test_api.py::test_root_endpoint`: Web SPA and JSON API metadata delivery.
- `test_api.py::test_health_endpoint`: Deep health check (DB latency, vector chunk count, Ollama status).
- `test_api.py::test_session_lifecycle`: Session creation, history retrieval, message persistence, and cascade deletion.
- `test_providers.py::test_provider_factory`: Dynamic model routing across Ollama, Claude, OpenAI, and Mock.
- `test_providers.py::test_mock_streaming`: Async streaming token delivery.
- `test_providers.py::test_ship30_skill_prompt`: Ship 30 prompt builder and heuristic adherence.
- `test_retrieval.py::test_retrieval_grounding`: Vector ranking and timestamped citation generation.
- `test_retrieval.py::test_out_of_domain_refusal`: Out-of-domain query detection and refusal protocol.
- `test_security.py::test_extract_artifacts`: Regex XML extraction for HTML artifacts.
- `test_security.py::test_extract_markdown_artifact`: Markdown artifact parsing and isolation.

---

## Manual Evaluator Test Plan

1. **Verify Health:** Visit `http://localhost:8000/api/health` and verify `"database": {"status": "connected"}` and `"vector_index": {"status": "ready"}`.
2. **Test Grounded RAG:** In the chat input, ask:
   > *"What was Brian Chesky's rationale for redesigning product management and moving Airbnb to one single company-wide roadmap?"*
   - Verify the answer cites `[Episode: Brian Chesky’s new playbook, Guest: Brian Chesky, Timestamp: ...]`.
   - Click the citation badge to inspect the exact transcript excerpt.
3. **Test Out-of-Domain Refusal:** Ask:
   > *"How do I bake sourdough bread with yeast in the oven?"*
   - Verify the assistant refuses: *"I do not have sufficient information in Lenny's podcast archive to answer this question..."*
4. **Test Ship 30 for 30 Skill:** Toggle the mode to **"Ship 30 for 30 Essay"** and ask:
   > *"Write a Ship 30 essay on Elena Verna's B2B growth loops and product-led sales."*
   - Verify short 1–3 sentence paragraphs, bold anchor points, and actionable takeaway frameworks.
5. **Test Artifact Generation & Viewer:** Ask:
   > *"Generate an interactive HTML/CSS ROI and Viral Coefficient calculator based on Lenny's guests' metrics."*
   - Verify the side-by-side Artifact Viewer slides open.
   - Interact with the sliders in the **Preview** tab.
   - Inspect source code in the **Source** tab, test **Copy**, and test **Download**.
6. **Test Model Switching:** Use the header dropdown to toggle between **Local Ollama**, **Claude**, **OpenAI**, and **Demo Provider**.

---

## Deliverables Index

| # | Deliverable | Location | Description |
| :- | :--- | :--- | :--- |
| 1 | Public GitHub Repository | Root directory | Clean, organized codebase with no committed secrets. |
| 2 | README.md | [README.md](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/README.md) | Comprehensive setup, architecture, and operational guide. |
| 3 | PRD | [docs/PRD.md](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/docs/PRD.md) | Persona, JTBD, metrics, assumptions, trade-offs, and risks. |
| 4 | Design Spec | [docs/design.md](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/docs/design.md) | UI/UX principles, Claude Artifact split-pane, accessibility. |
| 5 | Architecture Spec | [docs/architecture.md](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/docs/architecture.md) | DB schema, API contracts, RAG pipeline, and iframe security. |
| 6 | Agent Transcripts | [agent_transcripts/](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/agent_transcripts/) | Scaffolding, vector persistence, and skill iteration logs. |
| 7 | Automated & Manual Tests | [backend/tests/](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/backend/tests/) | 10 passing pytest cases + manual test plan. |
| 8 | Demo Video Guide | [docs/demo_video_guide.md](file:///c:/Users/agrep/OneDrive/Desktop/Lenny%20Growth%20Assistant/docs/demo_video_guide.md) | Script, recording checklist, and trade-off walkthrough. |

---

## License & Attribution

- Content grounded in [Lenny's Podcast](https://www.lennyspodcast.com/) transcripts curated by [ChatPRD](https://github.com/ChatPRD/lennys-podcast-transcripts).
- Built for the Forward Deployed Engineer (FDE) Evaluation Engagement.
