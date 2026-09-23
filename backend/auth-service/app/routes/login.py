from fastapi import APIRouter,Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.model.user import UserModel
from app.schema.user import LoginSchema
from app.database import get_db
from datetime import timedelta
from app.enum.token_varients import TokenVarients
from app.services.auth import verify_password
from app.services.jwt_handler import create_token

ACCESS_TOKEN_AGE=timedelta(days=1)
REFRESH_TOKEN_AGE=timedelta(days=2) #minutes_15
REFRESH_TOKEN_COOKIE_AGE=2 * 24 * 60 * 60
ACCESS_TOKEN_COOKIE_AGE=1 * 24 * 60 * 60

router = APIRouter(prefix="/auth",tags=["Auth"])
@router.post("/login")
def login(
    data: LoginSchema,
    response:Response,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(
        UserModel.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_token(
        {"user_id": user.id},
        ACCESS_TOKEN_AGE,
        TokenVarients.ACCESS_TOKEN.value
        )
    refresh_token = create_token(
        {"user_id": user.id},
        REFRESH_TOKEN_AGE,
        TokenVarients.REFRESH_TOKEN.value
    )
    response.set_cookie(
        key=TokenVarients.ACCESS_TOKEN.value,
        value=access_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=ACCESS_TOKEN_COOKIE_AGE  # 15 days
    )

    response.set_cookie(
        key=TokenVarients.REFRESH_TOKEN.value,
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=REFRESH_TOKEN_COOKIE_AGE # 30 days
    )

    return {
        "message": "Login successful"
    } 