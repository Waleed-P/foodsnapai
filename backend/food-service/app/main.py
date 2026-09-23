from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, history, web_socket

app = FastAPI(
    title="FoodSnapAI - Food Service",
    description="Handles image uploads, analysis processing, food history, and nutrition tracking.",
    version="1.0.0",
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
app.include_router(history.router)
app.include_router(upload.router)
app.include_router(web_socket.router)