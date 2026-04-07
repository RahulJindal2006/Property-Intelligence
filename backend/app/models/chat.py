from pydantic import BaseModel
from typing import Optional


class ConversationExchange(BaseModel):
    question: str
    answer: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: list[ConversationExchange] = []


class ChatResponse(BaseModel):
    intent: str
    answer: str
    sql_query: Optional[str] = None
    data: Optional[list[dict]] = None
    error: Optional[str] = None
