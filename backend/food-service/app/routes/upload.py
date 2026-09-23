from fastapi import APIRouter,UploadFile,File,status,HTTPException, Request, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.model.food import FoodItemModel
from app.services.jwt_handler import  verify_token
from app.enum.token_varients import TokenVarients
import os
import uuid
from app.workers.food_tasks import process_food_image
from app.utilities.upload_file import upload_file_to_s3

router = APIRouter(
    prefix="/food",
    tags=["Food Items"]
)
BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg"}
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_food_item(
    request: Request,               # 1. Non-default arguments first
    image: UploadFile = File(...),  # 2. Default/Dependency arguments next
    db: Session = Depends(get_db)
):   
    # 1. Validate Image Format
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Please upload a JPEG, JPG, or PNG."
        )

    # 2. Authentication Check via Cookies
    access_token = request.cookies.get(TokenVarients.ACCESS_TOKEN.value)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing"
        )
        
    try:
        payload = verify_token(access_token, TokenVarients.ACCESS_TOKEN.value)
        current_user_id = payload["user_id"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )

    # 3. Generate Secure S3 Path
    # Extract file extension cleanly, falling back to jpg if edge cases occur
    file_extension = image.filename.split(".")[-1].lower() if image.filename and "." in image.filename else "jpg"
    
    # Safe naming schema tied to user ID to prevent overlap
    unique_id = uuid.uuid4().hex
    print("unique id = ",unique_id)
    unique_filename = f"food_images/user_{current_user_id}_{unique_id}.{file_extension}"

    # 4. Upload to S3
    print("Uploading to S3...")
    try:
        s3_url = upload_file_to_s3(
            file_obj=image.file,
            bucket_name=BUCKET_NAME,
            object_name=unique_filename,
            content_type=image.content_type
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save food image to cloud storage."
        )
    finally:
        # Crucial to release file descriptors/memory
        await image.close()

    # 5. Database Persistence
    new_food_item = FoodItemModel(
        image_url=s3_url,
        user_id=current_user_id,
        aws_unique_name=unique_filename
    )
    
    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)
    
    process_food_image.send(new_food_item.id)

    return {
        "message": "Image uploaded successfully",
        "food_item_id": new_food_item.id,
        "status": "pending"
    }