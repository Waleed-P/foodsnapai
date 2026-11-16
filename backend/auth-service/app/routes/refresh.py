from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, Response, status
from app.core.config import settings
from app.core.security import create_token, verify_token
from app.enums.token_variants import TokenVariants
from app.schemas.user import MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_AGE = timedelta(days=settings.access_token_expire_days)
ACCESS_TOKEN_COOKIE_AGE = int(ACCESS_TOKEN_AGE.total_seconds())


@router.post("/refresh", response_model=MessageResponse)
def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get(TokenVariants.REFRESH_TOKEN.value)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    payload = verify_token(refresh_token, TokenVariants.REFRESH_TOKEN.value)
    new_access_token = create_token(
        {"user_id": payload["user_id"]},
        ACCESS_TOKEN_AGE,
        TokenVariants.ACCESS_TOKEN.value,
    )

    response.set_cookie(
        key=TokenVariants.ACCESS_TOKEN.value,
        value=new_access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=ACCESS_TOKEN_COOKIE_AGE,
        path="/",
    )
    return MessageResponse(message="Token refreshed")
