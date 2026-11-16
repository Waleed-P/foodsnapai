from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Request, status
import httpx
from app.core.config import settings
from app.core.http_client import build_proxy_response, get_http_client

router = APIRouter(tags=["Agent"])


@router.post("/chat")
async def chat_with_agent(
    request: Request,
    payload: Dict[str, Any],
):
    headers = {
        "cookie": request.headers.get("cookie", ""),
        "Content-Type": "application/json",
    }
    auth_header = request.headers.get("authorization")
    if auth_header:
        headers["authorization"] = auth_header

    client = get_http_client()
    try:
        response = await client.post(
            f"{settings.agent_service_url}/agent/chat",
            json=payload,
            headers=headers,
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Agent Service unreachable: {str(e)}",
        )

    return build_proxy_response(response)
