# Agent Transcript Log 03: Ship 30 for 30 Skill & Sandboxed Artifact Viewer

**Agent:** Antigravity (FDE Autonomous Pair)  
**Date:** 2026-09-04  
**Objective:** Implementing the Ship 30 for 30 essay engine, XML artifact protocol, and secure iframe renderer.

---

### Challenge 1: Encoding "Ship 30 for 30" Heuristics Accurately
- **Observation:** Merely asking an LLM to "write like Ship 30 for 30" produces generic blog posts that fail the length requirement (~1,250 words), use dense blocks of text, or ignore transcript grounding.
- **Resolution:**
  - Encoded explicit Ship 30 structural rules directly into `ship30_writer.py`:
    1. **The Hook:** High-tension opening hook in the first 2–3 sentences.
    2. **Rhythm:** Strictly enforce short paragraphs (1–3 sentences max).
    3. **Skimmability:** Use bold anchor phrases at the start of bullet points, sub-headings every 150–200 words.
    4. **Target Volume:** Calibrated system prompt to generate ~1,250 words of rich analysis.
    5. **Actionable Takeaways:** Conclude with a clear tactical framework or operational checklist.
    6. **Grounding:** Attribute specific principles directly to the interviewed guests.

### Challenge 2: Untrusted HTML Artifact Rendering Security
- **Observation:** If the LLM generates an interactive HTML/CSS component (such as a viral coefficient calculator), rendering it directly via `dangerouslySetInnerHTML` allows Cross-Site Scripting (XSS).
- **Resolution:**
  - Implemented dual-layer isolation:
    1. `DOMPurify` runs on the raw string, sanitizing illegal tags and javascript schemes while allowing safe HTML5/CSS and interactive canvas/forms.
    2. Markup is loaded into `<iframe srcdoc="..." sandbox="allow-scripts" referrerpolicy="no-referrer" />`.
    3. Noticeably omitted `allow-same-origin`: This ensures the iframe executes scripts in an isolated origin, blocking any access to parent localStorage, cookies, session IDs, or parent DOM.
  - Added unit test in `test_security.py` verifying that cookie-stealing payloads are safely sanitized and contained.
