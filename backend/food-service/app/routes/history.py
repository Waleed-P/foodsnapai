from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import CurrentUserId
from app.models.food import FoodItemModel
from app.schemas.food import FoodHistoryResponse

router = APIRouter(prefix="/food", tags=["Food"])


@router.get("/history", response_model=FoodHistoryResponse)
async def get_user_history(
    current_user_id: CurrentUserId,
    db: Annotated[Session, Depends(get_db)],
):
    history_items = db.scalars(
        select(FoodItemModel)
        .where(FoodItemModel.user_id == current_user_id)
        .order_by(FoodItemModel.created_at.desc())
    ).all()

    return FoodHistoryResponse(history=list(history_items))
