import json
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db_session
from app.models.db_models import Session, Message, Artifact
from app.models.schemas import ChatRequest
from app.rag.retriever import TranscriptRetriever
from app.providers import get_llm_provider
from app.skills.ship30_writer import build_ship30_prompt
from app.skills.artifact_generator import ARTIFACT_SYSTEM_INSTRUCTION, extract_artifacts
from app.config import get_settings

logger = logging.getLogger("lenny_assistant.api.chat")
settings = get_settings()

router = APIRouter(prefix="/api/chat", tags=["Chat & Streaming"])

STANDARD_SYSTEM_PROMPT = """You are the **Lenny Growth Assistant**, an expert AI copilot grounded exclusively in insights from **Lenny's Podcast**—the leading podcast on product management, growth, strategy, and startups.

Your mission is to provide rigorous, actionable, tactical advice strictly supported by what Lenny Rachitsky and his world-class guests have shared.

### Guidelines for Your Answers:
1. **Absolute Grounding:** Base your reasoning strictly on the provided transcript excerpts below. Never fabricate guests, metrics, or frameworks.
2. **Mandatory Citations:** Always cite the source using the exact format:
   `[Episode: Title, Guest: Name, Timestamp: HH:MM:SS]`
3. **Actionable Depth:** Go beyond high-level platitudes. Provide concrete mental models, metrics, heuristics, and operational steps.
4. **Acknowledging Limits:** If the provided transcript context does not contain enough evidence to answer the query, clearly state:
   "I do not have sufficient information in Lenny's podcast archive to answer this question."

{artifact_instruction}

---
### Transcript Knowledge Context:
{context_data}
"""

@router.post("")
async def chat_stream(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Streaming chat endpoint via Server-Sent Events (SSE).
    Retrieves grounded context, routes to selected LLM, streams response tokens,
    extracts artifacts, and persists session conversation history.
    """
    # 1. Verify or create session
    stmt = select(Session).where(Session.id == payload.session_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if not session:
        session = Session(id=payload.session_id, title="New Strategy Session")
        db.add(session)
        await db.commit()
        await db.refresh(session)

    # 2. Save User Message
    user_msg = Message(
        session_id=session.id,
        role="user",
        content=payload.message,
        provider=payload.provider or settings.DEFAULT_LLM_PROVIDER,
        mode=payload.mode or "default"
    )
    db.add(user_msg)
    
    # Auto-title session if still default
    if session.title == "New Strategy Session" or not session.title:
        session.title = payload.message[:45] + ("..." if len(payload.message) > 45 else "")
    session.updated_at = datetime.now(timezone.utc)
    await db.commit()

    # 3. Retrieve Grounded Transcript Chunks
    retriever = TranscriptRetriever(db)
    chunks, is_grounded = await retriever.retrieve_relevant_chunks(payload.message)

    # 4. Prepare System Prompt & Mode
    provider_name = payload.provider or settings.DEFAULT_LLM_PROVIDER
    llm = get_llm_provider(provider_name)

    async def event_generator():
        yield f"data: {json.dumps({'type': 'status', 'content': 'Searching 300+ transcripts...'})}\n\n"

        if not is_grounded:
            refusal_text = (
                "I do not have sufficient information in Lenny's podcast archive to answer this question. "
                "My answers are strictly limited to verified statements and operational frameworks discussed by Lenny Rachitsky and his product, growth, and leadership guests."
            )
            yield f"data: {json.dumps({'type': 'sources', 'sources': []})}\n\n"
            for word in refusal_text.split(" "):
                yield f"data: {json.dumps({'type': 'token', 'content': word + ' '})}\n\n"
            
            # Save assistant refusal message
            asst_msg = Message(
                session_id=session.id,
                role="assistant",
                content=refusal_text,
                sources=[],
                provider=provider_name,
                mode=payload.mode or "default"
            )
            db.add(asst_msg)
            await db.commit()
            yield "data: [DONE]\n\n"
            return

        # Send retrieved sources to client
        yield f"data: {json.dumps({'type': 'sources', 'sources': chunks})}\n\n"

        # Build prompt based on mode
        if payload.mode == "ship30":
            system_prompt = build_ship30_prompt(payload.message, chunks)
        else:
            context_formatted = "\n\n".join([
                f"--- [Source {i+1}] Episode: {c['episode']} | Guest: {c['guest']} | Timestamp: {c['timestamp']} ---\n{c['text']}"
                for i, c in enumerate(chunks)
            ])
            system_prompt = STANDARD_SYSTEM_PROMPT.format(
                artifact_instruction=ARTIFACT_SYSTEM_INSTRUCTION,
                context_data=context_formatted
            )

        messages = [{"role": "user", "content": payload.message}]

        accumulated_tokens = []
        try:
            async for token in llm.generate_response(messages, system_prompt):
                accumulated_tokens.append(token)
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        except Exception as e:
            err_msg = f"\n\n**Generation Error:** {str(e)}"
            accumulated_tokens.append(err_msg)
            yield f"data: {json.dumps({'type': 'token', 'content': err_msg})}\n\n"

        full_response = "".join(accumulated_tokens)

        # 5. Extract and persist artifacts
        clean_text, parsed_artifacts = extract_artifacts(full_response)
        
        asst_msg = Message(
            session_id=session.id,
            role="assistant",
            content=full_response,
            sources=chunks,
            provider=provider_name,
            mode=payload.mode or "default"
        )
        db.add(asst_msg)
        await db.flush()

        saved_artifacts = []
        for art in parsed_artifacts:
            artifact_record = Artifact(
                session_id=session.id,
                message_id=asst_msg.id,
                artifact_type=art["type"],
                title=art["title"],
                content=art["content"]
            )
            db.add(artifact_record)
            saved_artifacts.append({
                "id": artifact_record.id,
                "type": art["type"],
                "title": art["title"],
                "content": art["content"]
            })

        await db.commit()

        if saved_artifacts:
            yield f"data: {json.dumps({'type': 'artifact', 'artifacts': saved_artifacts})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
