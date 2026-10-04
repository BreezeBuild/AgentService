from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from breeze_agentic.agent.graph import run_agent
from breeze_agentic.core.config import get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str
    environment: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, examples=["Plan a simple agent workflow."])


class ChatResponse(BaseModel):
    response: str


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(service=settings.app_name, environment=settings.environment)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    settings = get_settings()
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    return ChatResponse(response=run_agent(payload.message))
