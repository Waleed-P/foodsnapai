from fastapi import APIRouter, Request, Response
from app.schema.auth import UserCreateSchema, LoginSchema
import httpx
from app.services.auth import oauth
import os
router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)
GATEWAY_CALLBACK_URL = os.environ["GATEWAY_CALLBACK_URL"]
AUTH_SERVICE_URL = os.environ["AUTH_SERVICE_URL"]

@router.post("/register")
async def register_user(payload:UserCreateSchema):

    async with httpx.AsyncClient() as client:

        auth_res = await client.post(
            f"{AUTH_SERVICE_URL}/auth/register",
            json=payload.model_dump(),
            headers={"Content-Type":"application/json"}
        )
    gateway_res = Response(
        content=auth_res.content,
        status_code=auth_res.status_code,
        headers=dict(auth_res.headers)
    )
    return gateway_res

@router.post("/login")
async def login_user(payload:LoginSchema):

    async with httpx.AsyncClient() as client:
        auth_res = await client.post(
            f"{AUTH_SERVICE_URL}/auth/login",
            json=payload.model_dump(),
            headers={"Content-Type": "application/json"}
        )

    gateway_res = Response(
        content=auth_res.content,
        status_code=auth_res.status_code,
        headers=dict(auth_res.headers)
    )

    # 4. Explicitly attach Set-Cookie headers so cookies land in browser
    for key, value in auth_res.headers.raw:
        if key.lower() == b"set-cookie":
            gateway_res.headers.append("Set-Cookie", value.decode("latin1"))

    return gateway_res

@router.post("/refresh")
async def refresh_token(request: Request):
    # 1. Read incoming cookies from client request
    incoming_cookies = request.headers.get("cookie", "")

    # 2. Proxy request to auth-service with Cookie header
    async with httpx.AsyncClient() as client:
        auth_res = await client.post(
            f"{AUTH_SERVICE_URL}/auth/refresh",
            headers={"Cookie": incoming_cookies}
        )

    # 3. Create Gateway response
    gateway_res = Response(
        content=auth_res.content,
        status_code=auth_res.status_code,
        headers=dict(auth_res.headers)
    )

    # 4. Forward Set-Cookie headers back to browser
    for key, value in auth_res.headers.raw:
        if key.lower() == b"set-cookie":
            gateway_res.headers.append("Set-Cookie", value.decode("latin1"))

    return gateway_res


@router.get("/google/login")
async def google_oauth(request: Request):
    # Generates redirect URL to Google with the gateway callback URL
    return await oauth.google.authorize_redirect(request, GATEWAY_CALLBACK_URL)

@router.get("/google/callback")
async def google_callback_proxy(request: Request):
    # Forward Google's query parameters (code, state) to the auth-service
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8001/auth/google/callback",
            params=dict(request.query_params),
            headers=dict(request.headers)
        )
    
    # Return response back to client (including cookies set by auth-service)
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )

@router.post("/logout")
async def logout_user(request: Request):
    incoming_cookies = request.headers.get("cookie", "")

    async with httpx.AsyncClient() as client:
        auth_res = await client.post(
            f"{AUTH_SERVICE_URL}/auth/logout",
            headers={"Cookie": incoming_cookies}
        )

    gateway_res = Response(
        content=auth_res.content,
        status_code=auth_res.status_code,
        headers=dict(auth_res.headers)
    )

    for key, value in auth_res.headers.raw:
        if key.lower() == b"set-cookie":
            gateway_res.headers.append("Set-Cookie", value.decode("latin1"))

    return gateway_res


@router.get("/get_me")
async def get_me_proxy(request: Request):
    # 1. Extract incoming cookies (access_token, refresh_token, etc.) from client browser
    incoming_cookies = request.headers.get("cookie", "")

    # 2. Proxy request to auth-service while attaching the Cookie header
    async with httpx.AsyncClient() as client:
        auth_res = await client.get(
            f"{AUTH_SERVICE_URL}/auth/get_me",
            headers={"Cookie": incoming_cookies}
        )

    # 3. Return response back to client with matching status code and content
    return Response(
        content=auth_res.content,
        status_code=auth_res.status_code,
        headers=dict(auth_res.headers)
    )
