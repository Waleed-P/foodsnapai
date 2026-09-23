from datetime import timedelta
from fastapi import APIRouter, Response, Request, HTTPException
from app.services.jwt_handler import verify_token , create_token
from app.enum.token_varients import TokenVarients

router = APIRouter(prefix="/auth",tags=["Auth"])
ACCESS_TOKEN_AGE=timedelta(days=1)
REFRESH_TOKEN_COOKIE_AGE=2 * 24 * 60 * 60
ACCESS_TOKEN_COOKIE_AGE=1 * 24 * 60 * 60


@router.post("/refresh")
def refresh(request: Request, response: Response):
    # Extract refresh token from client's cookies
    refresh_token = request.cookies.get(TokenVarients.REFRESH_TOKEN.value)
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )
        
    payload = verify_token(refresh_token, TokenVarients.REFRESH_TOKEN.value)

    new_access_token = create_token(
        {"user_id": payload["user_id"]},
        ACCESS_TOKEN_AGE,
        TokenVarients.ACCESS_TOKEN.value
    )
    
    response.set_cookie(
        key=TokenVarients.ACCESS_TOKEN.value,
        value=new_access_token,
        httponly=True,
        secure=False,  # Set True in production (HTTPS)
        samesite="lax",
        max_age=ACCESS_TOKEN_COOKIE_AGE
    )
    return {"message": "Token refreshed"}