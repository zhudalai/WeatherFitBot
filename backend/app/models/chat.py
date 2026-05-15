from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .weather import WeatherResponse
from .outfit import OutfitAdvice


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime = datetime.now()
    data: Optional[dict] = None


class ChatSession(BaseModel):
    session_id: str
    messages: list[ChatMessage] = []
    last_city: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class QuickAction(BaseModel):
    label: str
    action: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    data: Optional[dict] = None
    quick_actions: list[QuickAction] = []
