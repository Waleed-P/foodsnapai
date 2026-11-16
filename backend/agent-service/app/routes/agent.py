from typing import Optional
from fastapi import APIRouter, Request
from app.agent import Agent
from app.core.security import CurrentUserId
from app.schemas.agent import ChatRequest, ChatResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: Request,
    current_user_id: CurrentUserId,
    body: ChatRequest,
):
    # Extract auth token from cookie or header to propagate downstream
    auth_token = request.cookies.get("access_token")
    if not auth_token:
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            auth_token = auth_header.split(" ", 1)[1]

    agent = Agent(
        user_id=current_user_id,
        auth_token=auth_token,
    )
    answer = agent(body.message)

    return ChatResponse(
        response=answer,
        user_id=current_user_id,
    )
