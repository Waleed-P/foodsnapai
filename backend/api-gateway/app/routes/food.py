from fastapi import APIRouter, Request, UploadFile, File, Response, HTTPException
import httpx
import os
router = APIRouter(
    prefix="/api/food",
    tags=["Food"]
)

FOOD_SERVICE_URL = os.environ["FOOD_SERVICE_URL"]

@router.post("/upload")
async def upload_food_image(
    request: Request,
    image: UploadFile = File(...)
):
    # Read the uploaded file bytes
    file_bytes = await image.read()

    # Pass client cookies along to the internal service
    headers = {
        "cookie": request.headers.get("cookie", "")
    }

    files = {
        "image": (image.filename, file_bytes, image.content_type)
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FOOD_SERVICE_URL}/food/upload",
            files=files,
            headers=headers
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code, 
            detail=response.json().get("detail", "Error from Food Service")
        )

    return response.json()


@router.get("/history")
async def get_history(request: Request):
    headers = {
        "cookie": request.headers.get("cookie", "")
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FOOD_SERVICE_URL}/food/history",
            headers=headers
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code, 
            detail=response.json().get("detail", "Error from Food Service")
        )

    return response.json()