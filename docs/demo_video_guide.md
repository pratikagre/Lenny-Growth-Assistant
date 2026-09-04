# 2–3 Minute Evaluation Demo Video Guide
## The Lenny Growth Assistant

This guide provides a structured, word-for-word script and recording checklist for the mandatory 2–3 minute video presentation with camera enabled.

---

## Pre-Recording Checklist
- [ ] **Camera & Audio:** Camera positioned at eye level; clean lighting; clear microphone.
- [ ] **Application Running:** Run `.\run_local.ps1` or `python backend/app/main.py`.
- [ ] **Browser Prepared:** Open `http://localhost:8000` in full screen (or 1080p window).
- [ ] **Ollama Status:** If Ollama is running locally, ensure `ollama serve` and `ollama pull llama3.2:3b` are completed. If testing offline demo, have Demo Provider ready.

---

## 2–3 Minute Video Script

### Scene 1: Introduction & Problem Framing (0:00 – 0:40)
**Visual:** Camera full screen or camera bubble in bottom-left corner with application home screen.
> *"Hi everyone, I'm presenting The Lenny Growth Assistant—a forward-deployed AI platform built to turn over 300 in-depth conversations from Lenny’s Podcast into an operational intelligence engine for product and growth teams.*
>
> *Product managers and growth executives face a real problem: Lenny's archive has hundreds of hours of gold-standard wisdom from people like Brian Chesky, Elena Verna, and Shreyas Doshi. But when you need to make a pricing decision or design a growth loop on a Tuesday morning, nobody has 90 minutes to listen to an episode, and generic ChatGPT answers hallucinate generic fluff.*
>
> *Our goal was to build a full-stack, enterprise-ready system that delivers verifiable, grounded answers, generates high-retention Ship 30 for 30 essays, and renders live, interactive HTML artifacts beside the chat in a sandboxed viewer—all with single-command local deployment."*

---

### Scene 2: Live Demo — Grounded RAG & Out-of-Domain Refusal (0:40 – 1:20)
**Visual:** Screen recording of `http://localhost:8000`. Click the "Brian Chesky on Roadmaps" starter.
> *"Let's look at the product in action. First, I'll ask about Brian Chesky's famous restructuring of product management at Airbnb.*
>
> *Notice three things:*
> 1. *The answer streams with sub-second latency.*
> 2. *Every claim is attributed with verifiable timestamped citations: `[Episode: Brian Chesky's new playbook, Guest: Brian Chesky, Timestamp: 00:01:27]`.*
> 3. *Clicking any citation pill opens an inspection drawer showing the exact spoken excerpt from the transcript.*
>
> *If I test the boundary by asking something completely out-of-domain, like 'How do I bake sourdough bread?', the retriever detects that similarity is below our relevance threshold and immediately enforces the refusal protocol: 'I do not have sufficient information in Lenny's podcast archive to answer this question.'"*

---

### Scene 3: Ship 30 for 30 Skill & Sandboxed Artifact Viewer (1:20 – 2:10)
**Visual:** Switch mode to "Ship 30 for 30 Essay" and click "Interactive PLG Calculator".
> *"Next is our dedicated Ship 30 for 30 content skill. Instead of a generic prompt, we hardcoded Nicolas Cole and Dickie Bush’s writing heuristics: a counterintuitive hook, 1-to-3 sentence paragraphs, bold anchor points, and an actionable Monday-morning checklist.*
>
> *Now, notice what happens when the user asks for a growth tool: The assistant generates a complete HTML/CSS artifact. Look at the right side of the screen:*
> *Our Claude-style Artifact Viewer automatically slides open beside the chat. Here is a live, interactive Product-Led Growth Viral Loop Calculator.*
> *I can adjust the invite sliders and conversion rates in real time.*
>
> *Under the hood, security is paramount: The HTML is treated as untrusted. We run it through DOMPurify and render it in an iframe with `sandbox='allow-scripts'`, but strictly omit `allow-same-origin`. The scripts can run the calculator UI, but have zero access to parent cookies, localStorage, or DOM."*

---

### Scene 4: Local Ollama & Key Technical Trade-off (2:10 – 2:50)
**Visual:** Click the Model Selector dropdown in the top header.
> *"For evaluation, the system defaults to Local Ollama running `llama3.2:3b`. You can see our real-time health indicator in the header showing local Ollama connectivity and indexed chunk counts. With one click, an evaluator can switch between local Ollama, Claude 3.5 Sonnet, OpenAI GPT-4o, or our offline Demo provider without touching a line of code.*
>
> *Let's talk about one important technical trade-off: **Local parameter size versus latency and reasoning depth**.*
> *Running an 8-billion parameter model locally on consumer hardware can have a 6-to-10 second time-to-first-token, whereas a 3-billion model like `llama3.2` achieves sub-3-second TTFT but can lose nuance on multi-step reasoning.*
> *We resolved this by offloading the reasoning burden into our retrieval pipeline: We chunk transcripts along speaker turns, inject exact timestamp references, and provide structured prompt scaffolds so that even a lightweight local 3B model produces precise, grounded tactical answers.*
>
> *Thank you, and I look forward to your evaluation!"*

---

## Video Submission Checklist
1. Upload to YouTube as **Unlisted** (or Public).
2. Set title to: `The Lenny Growth Assistant - Forward Deployed Engineer Demo`.
3. Include GitHub repository link in the description.
