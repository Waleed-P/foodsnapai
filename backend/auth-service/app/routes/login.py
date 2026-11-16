from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_token, verify_password
from app.enums.token_variants import TokenVariants
from app.models.user import UserModel
from app.schemas.user import LoginSchema, MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_AGE = timedelta(days=settings.access_token_expire_days)
REFRESH_TOKEN_AGE = timedelta(days=settings.refresh_token_expire_days)
ACCESS_TOKEN_COOKIE_AGE = int(ACCESS_TOKEN_AGE.total_seconds())
REFRESH_TOKEN_COOKIE_AGE = int(REFRESH_TOKEN_AGE.total_seconds())


@router.post("/login", response_model=MessageResponse)
def login(
    data: LoginSchema,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalar(
        select(UserModel).where(UserModel.email == data.email)
    )

    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_token(
        {"user_id": user.id},
        ACCESS_TOKEN_AGE,
        TokenVariants.ACCESS_TOKEN.value,
    )
    refresh_token = create_token(
        {"user_id": user.id},
        REFRESH_TOKEN_AGE,
        TokenVariants.REFRESH_TOKEN.value,
    )

    response.set_cookie(
        key=TokenVariants.ACCESS_TOKEN.value,
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=ACCESS_TOKEN_COOKIE_AGE,
        path="/",
    )
    response.set_cookie(
        key=TokenVariants.REFRESH_TOKEN.value,
        value=refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=REFRESH_TOKEN_COOKIE_AGE,
        path="/",
    )

    return MessageResponse(message="Login successful")
