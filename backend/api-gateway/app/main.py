from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.core.http_client import close_http_client, init_http_client
from app.routes import agent, auth, food, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize shared high-performance HTTP client on startup
    await init_http_client()
    yield
    # Gracefully shut down HTTP client on shutdown
    await close_http_client()


app = FastAPI(
    title="FoodSnapAI API Gateway",
    description="Unified API Gateway routing traffic to Auth, Food, and Agent microservices.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
)

# Secure CORS: credentials require explicit non-wildcard origins
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
        "service": "api-gateway",
        "downstream": {
            "auth_service": settings.auth_service_url,
            "food_service": settings.food_service_url,
            "agent_service": settings.agent_service_url,
        },
    }


# Primary API routes
app.include_router(auth.router, prefix="/api/auth")
app.include_router(food.router, prefix="/api/food")
app.include_router(agent.router, prefix="/api/agent")

# Compatibility aliases without /api prefix
app.include_router(auth.router, prefix="/auth", include_in_schema=False)
app.include_router(food.router, prefix="/food", include_in_schema=False)
app.include_router(agent.router, prefix="/agent", include_in_schema=False)

# WebSocket routes
app.include_router(ws.router)
