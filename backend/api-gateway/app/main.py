from fastapi import FastAPI
from app.routes import food, auth, ws
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    title="FoodSnapAI API Gateway",
    version="1.0.0"
)
app.add_middleware(
    SessionMiddleware,
    secret_key="your-super-secret-key-here"  # Replace with a strong, random string
)
origins = [
    "http://127.0.0.1:3000", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(food.router)
app.include_router(ws.router)

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload