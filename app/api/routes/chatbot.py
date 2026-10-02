from fastapi import APIRouter, HTTPException

from app.ai.langgraph_agent import ask_chatbot
from app.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])


@router.post("/ask", response_model=ChatResponse)
def chatbot(request: ChatRequest):
    try:
        result = ask_chatbot(request.question)
        return ChatResponse(
            question=request.question,
            answer=result["answer"],
            records_used=result["records_used"],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {exc}") from exc
