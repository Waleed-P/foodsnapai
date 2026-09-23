from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import login, register, get_me, logout, refresh, oauth
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine
app = FastAPI(
    title="FoodSnapAI - Food Service",
    description="Handles image uploads, analysis processing, food history, and nutrition tracking.",
    version="1.0.0",
)
app.add_middleware(
    SessionMiddleware,
    secret_key="your-super-secret-key-here"  # Replace with a strong, random string
)
# CORS Configuration
origins = [
    "http://api-gateway:8000",       # Internal Docker container name
    "http://127.0.0.1:8000",         # Host machine loopback (for local testing)
    "http://localhost:8000",         # Host machine localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(logout.router)
app.include_router(get_me.router)
app.include_router(refresh.router)
app.include_router(oauth.router)