from typing import Optional
from fastapi import Response
import httpx
from app.core.config import settings

_http_client: Optional[httpx.AsyncClient] = None


async def init_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=settings.request_timeout_seconds,
            follow_redirects=False,
        )
    return _http_client


async def close_http_client():
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None


def get_http_client() -> httpx.AsyncClient:
    if _http_client is None or _http_client.is_closed:
        # Fallback if accessed before lifespan
        return httpx.AsyncClient(timeout=settings.request_timeout_seconds, follow_redirects=False)
    return _http_client


def build_proxy_response(downstream_res: httpx.Response) -> Response:
    """
    Builds a FastAPI Response from an httpx response, properly preserving
    all Set-Cookie headers and standard HTTP headers.
    """
    excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    headers = {
        k: v for k, v in downstream_res.headers.items()
        if k.lower() not in excluded_headers and k.lower() != "set-cookie"
    }

    client_res = Response(
        content=downstream_res.content,
        status_code=downstream_res.status_code,
        headers=headers,
    )

    # Explicitly append each Set-Cookie header preserving duplicates
    for key, value in downstream_res.headers.raw:
        if key.lower() == b"set-cookie":
            client_res.headers.append("Set-Cookie", value.decode("latin1"))

    return client_res
