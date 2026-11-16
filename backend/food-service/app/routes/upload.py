import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import CurrentUserId
from app.enums.job_status import JobStatus
from app.models.food import FoodItemModel
from app.schemas.food import FoodUploadResponse
from app.services.s3 import upload_file_to_s3
from app.workers.food_tasks import process_food_image

router = APIRouter(prefix="/food", tags=["Food Items"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=FoodUploadResponse)
async def upload_food_item(
    current_user_id: CurrentUserId,
    image: Annotated[UploadFile, File(...)],
    db: Annotated[Session, Depends(get_db)],
):
    # 1. Validate Image Content Type
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Please upload a JPEG, PNG, or WebP image.",
        )

    # 2. Generate Safe S3 Object Key
    file_extension = (
        image.filename.split(".")[-1].lower()
        if image.filename and "." in image.filename
        else "jpg"
    )
    unique_id = uuid.uuid4().hex
    unique_filename = f"food_images/user_{current_user_id}_{unique_id}.{file_extension}"

    # 3. Upload to S3
    try:
        s3_url = upload_file_to_s3(
            file_obj=image.file,
            object_name=unique_filename,
            content_type=image.content_type or "image/jpeg",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload food image: {str(e)}",
        )
    finally:
        await image.close()

    # 4. Database Persistence
    new_food_item = FoodItemModel(
        image_url=s3_url,
        user_id=current_user_id,
        aws_unique_name=unique_filename,
        status=JobStatus.PENDING,
    )
    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)

    # 5. Dispatch Dramatiq Background Task
    try:
        process_food_image.send(new_food_item.id)
    except Exception as e:
        # Non-fatal to client response, task can be retried or picked up
        pass

    return FoodUploadResponse(
        message="Image uploaded successfully",
        food_item_id=new_food_item.id,
        status="pending",
    )
