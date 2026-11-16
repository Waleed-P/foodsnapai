from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_token
from app.enums.token_variants import TokenVariants
from app.models.user import UserModel
from app.services.oauth import oauth

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_AGE = timedelta(days=settings.access_token_expire_days)
REFRESH_TOKEN_AGE = timedelta(days=settings.refresh_token_expire_days)
ACCESS_TOKEN_COOKIE_AGE = int(ACCESS_TOKEN_AGE.total_seconds())
REFRESH_TOKEN_COOKIE_AGE = int(REFRESH_TOKEN_AGE.total_seconds())


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authorization failed: {str(e)}",
        )

    user_info = token.get("userinfo")
    if not user_info or "email" not in user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not retrieve user info from Google",
        )

    email = user_info["email"]
    name = user_info.get("name")

    user = db.scalar(
        select(UserModel).where(UserModel.email == email)
    )
    if not user:
        user = UserModel(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)

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

    redirect_url = f"{settings.frontend_url.rstrip('/')}/home"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

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

    return response
