from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.enum.token_varients import TokenVarients
from app.services.jwt_handler import verify_token
from app.model.user import UserModel
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/get_me")
def get_me(request: Request, db: Session = Depends(get_db)):
    # 1. Read token from incoming request cookies
    access_token = request.cookies.get(TokenVarients.ACCESS_TOKEN.value)
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Access token missing"
        )
    
    # 2. Verify token payload
    payload = verify_token(access_token, TokenVarients.ACCESS_TOKEN.value)
    current_user_id = payload["user_id"]

    # 3. Fetch user details from database
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )    

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }