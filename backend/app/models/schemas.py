from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SourceCitation(BaseModel):
    episode: str
    guest: str
    timestamp: Optional[str] = "00:00:00"
    text: str
    score: float
    youtube_url: Optional[str] = None

class ArtifactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    message_id: Optional[str] = None
    session_id: str
    artifact_type: str  # 'html' or 'markdown'
    title: str
    content: str
    created_at: datetime

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    role: str
    content: str
    sources: List[Dict[str, Any]] = []
    provider: Optional[str] = None
    mode: Optional[str] = "default"
    created_at: datetime
    artifacts: List[ArtifactResponse] = []

class SessionCreate(BaseModel):
    title: Optional[str] = "New Strategy Session"

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse] = []
    artifacts: List[ArtifactResponse] = []

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, description="User question or prompt")
    provider: Optional[str] = Field(default=None, description="'ollama', 'claude', 'openai', or 'mock'")
    mode: Optional[str] = Field(default="default", description="'default' or 'ship30'")

class HealthResponse(BaseModel):
    status: str
    database: Dict[str, Any]
    ollama: Dict[str, Any]
    cloud_providers: Dict[str, Any]
    vector_index: Dict[str, Any]
    version: str = "1.0.0"
