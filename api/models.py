from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "koc-assistant"
    messages: List[ChatMessage]
    stream: bool = True
    max_tokens: Optional[int] = 200
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ChatCompletionChoice(BaseModel):
    index: int
    message: Optional[ChatMessage] = None
    delta: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionChoice]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime: str

class StatsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    supported_topics: int
    uptime: str
    response_time: str
    accuracy: str

class ModelInfo(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    permission: List[str]
    root: str
    parent: Optional[str]

class ModelsResponse(BaseModel):
    object: str
    data: List[ModelInfo] 