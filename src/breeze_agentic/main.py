from fastapi import FastAPI

from breeze_agentic.api.routes import router
from breeze_agentic.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Modern FastAPI service with LangChain, LangGraph, and OpenAI.",
    )
    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
