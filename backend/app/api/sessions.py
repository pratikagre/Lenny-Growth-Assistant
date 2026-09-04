from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.database import get_db_session
from app.models.db_models import Session, Message, Artifact
from app.models.schemas import SessionCreate, SessionResponse, SessionDetailResponse, MessageResponse, ArtifactResponse

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new chat session."""
    session = Session(title=payload.title or "New Strategy Session")
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        message_count=0
    )

@router.get("", response_model=List[SessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db_session)):
    """List all chat sessions ordered by most recently updated."""
    stmt = (
        select(Session)
        .options(selectinload(Session.messages))
        .order_by(desc(Session.updated_at))
    )
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    
    return [
        SessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at,
            updated_at=s.updated_at,
            message_count=len(s.messages)
        )
        for s in sessions
    ]

@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db_session)):
    """Retrieve full message history and artifacts for a specific session."""
    stmt = (
        select(Session)
        .options(
            selectinload(Session.messages).selectinload(Message.artifacts),
            selectinload(Session.artifacts)
        )
        .where(Session.id == session_id)
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found."
        )

    # Format messages
    formatted_messages = []
    for m in session.messages:
        formatted_messages.append(
            MessageResponse(
                id=m.id,
                session_id=m.session_id,
                role=m.role,
                content=m.content,
                sources=m.sources or [],
                provider=m.provider,
                mode=m.mode,
                created_at=m.created_at,
                artifacts=[
                    ArtifactResponse(
                        id=a.id,
                        message_id=a.message_id,
                        session_id=a.session_id,
                        artifact_type=a.artifact_type,
                        title=a.title,
                        content=a.content,
                        created_at=a.created_at
                    )
                    for a in m.artifacts
                ]
            )
        )

    return SessionDetailResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        message_count=len(session.messages),
        messages=formatted_messages,
        artifacts=[
            ArtifactResponse(
                id=a.id,
                message_id=a.message_id,
                session_id=a.session_id,
                artifact_type=a.artifact_type,
                title=a.title,
                content=a.content,
                created_at=a.created_at
            )
            for a in session.artifacts
        ]
    )

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db_session)):
    """Delete a chat session and cascade delete all associated messages/artifacts."""
    stmt = select(Session).where(Session.id == session_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found."
        )

    await db.delete(session)
    await db.commit()
    return None
