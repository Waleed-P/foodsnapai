from fastapi import APIRouter, HTTPException, Request, Response, status
import httpx
from app.core.config import settings
from app.core.http_client import build_proxy_response, get_http_client
from app.schemas.auth import LoginSchema, UserCreateSchema
from app.services.auth import oauth

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register_user(payload: UserCreateSchema):
    client = get_http_client()
    try:
        auth_res = await client.post(
            f"{settings.auth_service_url}/auth/register",
            json=payload.model_dump(),
            headers={"Content-Type": "application/json"},
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(auth_res)


@router.post("/login")
async def login_user(payload: LoginSchema):
    client = get_http_client()
    try:
        auth_res = await client.post(
            f"{settings.auth_service_url}/auth/login",
            json=payload.model_dump(),
            headers={"Content-Type": "application/json"},
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(auth_res)


@router.post("/refresh")
async def refresh_token(request: Request):
    client = get_http_client()
    incoming_cookies = request.headers.get("cookie", "")
    try:
        auth_res = await client.post(
            f"{settings.auth_service_url}/auth/refresh",
            headers={"Cookie": incoming_cookies},
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(auth_res)


@router.post("/logout")
async def logout_user(request: Request):
    client = get_http_client()
    incoming_cookies = request.headers.get("cookie", "")
    try:
        auth_res = await client.post(
            f"{settings.auth_service_url}/auth/logout",
            headers={"Cookie": incoming_cookies},
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(auth_res)


@router.get("/get_me")
async def get_me_proxy(request: Request):
    client = get_http_client()
    incoming_cookies = request.headers.get("cookie", "")
    try:
        auth_res = await client.get(
            f"{settings.auth_service_url}/auth/get_me",
            headers={"Cookie": incoming_cookies},
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(auth_res)


@router.get("/google/login")
async def google_oauth(request: Request):
    return await oauth.google.authorize_redirect(request, settings.gateway_callback_url)


@router.get("/google/callback")
async def google_callback_proxy(request: Request):
    client = get_http_client()
    try:
        response = await client.get(
            f"{settings.auth_service_url}/auth/google/callback",
            params=dict(request.query_params),
            headers=dict(request.headers),
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth Service unreachable: {str(e)}",
        )
    return build_proxy_response(response)
