from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.enums.token_variants import TokenVariants
from app.models.user import UserModel
from app.schemas.user import UserResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/get_me", response_model=UserResponseSchema)
def get_me(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    access_token = request.cookies.get(TokenVariants.ACCESS_TOKEN.value)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    payload = verify_token(access_token, TokenVariants.ACCESS_TOKEN.value)
    current_user_id = payload.get("user_id")

    user = db.scalar(
        select(UserModel).where(UserModel.id == current_user_id)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
