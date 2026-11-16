from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.routes import get_me, login, logout, oauth, refresh, register


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup resources on shutdown (if any)


app = FastAPI(
    title="FoodSnapAI - Auth Service",
    description="Authentication and user profile management microservice.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
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
    return {"status": "ok", "service": "auth-service"}


app.include_router(register.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(get_me.router)
app.include_router(refresh.router)
app.include_router(oauth.router)
