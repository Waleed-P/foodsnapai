from fastapi import APIRouter,status,HTTPException, Request, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.model.food import FoodItemModel
from app.model.user import UserModel
from app.services.jwt_handler import  verify_token
from app.enum.token_varients import TokenVarients


router = APIRouter(prefix="/food",tags=["Food"])

@router.get("/history")
async def get_user_history(
    request: Request,
    db: Session = Depends(get_db)
):
    access_token_from_req = request.cookies.get(TokenVarients.ACCESS_TOKEN.value)
    if not access_token_from_req:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing"
        )
    try:
        payload = verify_token(access_token_from_req,TokenVarients.ACCESS_TOKEN.value)
        current_user_id=payload["user_id"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )
    user=db.query(UserModel).filter(UserModel.id==current_user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    history = db.query(FoodItemModel).filter(FoodItemModel.user_id==current_user_id).all()
    return {"history":history}