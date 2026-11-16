from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import UserModel
from app.schemas.user import MessageResponse, UserCreateSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
def register(
    user: UserCreateSchema,
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = db.scalar(
        select(UserModel).where(UserModel.email == user.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return MessageResponse(message="User registered successfully")
