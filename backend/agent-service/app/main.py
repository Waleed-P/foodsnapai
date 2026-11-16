from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="FoodSnapAI - Agent Service",
    description="Conversational AI Nutrition Intelligence Service powered by Groq LLM and tool calling.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "agent-service",
        "model": settings.groq_model,
        "food_service_url": settings.food_service_url,
    }


app.include_router(agent.router)
