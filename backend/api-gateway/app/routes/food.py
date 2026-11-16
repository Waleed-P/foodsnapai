from typing import Annotated, Optional
from fastapi import APIRouter, File, HTTPException, Query, Request, Response, UploadFile, status
import httpx
from app.core.config import settings
from app.core.http_client import build_proxy_response, get_http_client

router = APIRouter(tags=["Food"])


@router.post("/upload")
async def upload_food_image(
    request: Request,
    image: Annotated[UploadFile, File(...)],
):
    file_bytes = await image.read()
    headers = {
        "cookie": request.headers.get("cookie", ""),
    }
    auth_header = request.headers.get("authorization")
    if auth_header:
        headers["authorization"] = auth_header

    files = {
        "image": (image.filename, file_bytes, image.content_type),
    }

    client = get_http_client()
    try:
        response = await client.post(
            f"{settings.food_service_url}/food/upload",
            files=files,
            headers=headers,
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Food Service unreachable: {str(e)}",
        )
    finally:
        await image.close()

    return build_proxy_response(response)


@router.get("/history")
async def get_history(request: Request):
    headers = {
        "cookie": request.headers.get("cookie", ""),
    }
    auth_header = request.headers.get("authorization")
    if auth_header:
        headers["authorization"] = auth_header

    client = get_http_client()
    try:
        response = await client.get(
            f"{settings.food_service_url}/food/history",
            headers=headers,
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Food Service unreachable: {str(e)}",
        )

    return build_proxy_response(response)


@router.get("/nutrition/daily")
async def get_daily_nutrition(
    request: Request,
    date: Optional[str] = Query(None),
):
    headers = {
        "cookie": request.headers.get("cookie", ""),
    }
    auth_header = request.headers.get("authorization")
    if auth_header:
        headers["authorization"] = auth_header

    params = {"date": date} if date else {}

    client = get_http_client()
    try:
        response = await client.get(
            f"{settings.food_service_url}/food/nutrition/daily",
            headers=headers,
            params=params,
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Food Service unreachable: {str(e)}",
        )

    return build_proxy_response(response)


@router.get("/nutrition/history")
async def get_nutrition_history(
    request: Request,
    start_date: str = Query(...),
    end_date: str = Query(...),
):
    headers = {
        "cookie": request.headers.get("cookie", ""),
    }
    auth_header = request.headers.get("authorization")
    if auth_header:
        headers["authorization"] = auth_header

    params = {"start_date": start_date, "end_date": end_date}

    client = get_http_client()
    try:
        response = await client.get(
            f"{settings.food_service_url}/food/nutrition/history",
            headers=headers,
            params=params,
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Food Service unreachable: {str(e)}",
        )

    return build_proxy_response(response)
