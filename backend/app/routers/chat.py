from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.llm_service import process_message

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return process_message(request)
