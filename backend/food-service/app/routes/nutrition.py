from collections import defaultdict
from datetime import datetime, time, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import CurrentUserId
from app.enums.job_status import JobStatus
from app.models.food import FoodItemModel
from app.schemas.food import (
    DailyNutritionResponse,
    NutritionHistoryItem,
    NutritionHistoryResponse,
)

router = APIRouter(prefix="/food/nutrition", tags=["Nutrition"])


@router.get("/daily", response_model=DailyNutritionResponse)
async def get_daily_nutrition(
    current_user_id: CurrentUserId,
    db: Annotated[Session, Depends(get_db)],
    date: Optional[str] = Query(
        None,
        description="Target date in YYYY-MM-DD format. Defaults to today (UTC).",
    ),
):
    if not date:
        target_date = datetime.now(timezone.utc).date()
        date_str = target_date.strftime("%Y-%m-%d")
    else:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        date_str = date

    start_dt = datetime.combine(target_date, time.min, tzinfo=timezone.utc)
    end_dt = datetime.combine(target_date, time.max, tzinfo=timezone.utc)

    items = db.scalars(
        select(FoodItemModel).where(
            FoodItemModel.user_id == current_user_id,
            FoodItemModel.status == JobStatus.COMPLETED,
            FoodItemModel.created_at >= start_dt,
            FoodItemModel.created_at <= end_dt,
        )
    ).all()

    total_calories = sum(item.calories or 0.0 for item in items)
    total_protein = sum(item.protein or 0.0 for item in items)
    total_carbs = sum(item.carbohydrates or 0.0 for item in items)
    total_fats = sum(item.fats or 0.0 for item in items)

    return DailyNutritionResponse(
        date=date_str,
        total_calories=round(total_calories, 1),
        protein=round(total_protein, 1),
        carbohydrates=round(total_carbs, 1),
        fat=round(total_fats, 1),
        items_count=len(items),
    )


@router.get("/history", response_model=NutritionHistoryResponse)
async def get_nutrition_history(
    current_user_id: CurrentUserId,
    db: Annotated[Session, Depends(get_db)],
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
):
    start_dt = datetime.combine(
        datetime.strptime(start_date, "%Y-%m-%d").date(),
        time.min,
        tzinfo=timezone.utc,
    )
    end_dt = datetime.combine(
        datetime.strptime(end_date, "%Y-%m-%d").date(),
        time.max,
        tzinfo=timezone.utc,
    )

    items = db.scalars(
        select(FoodItemModel).where(
            FoodItemModel.user_id == current_user_id,
            FoodItemModel.status == JobStatus.COMPLETED,
            FoodItemModel.created_at >= start_dt,
            FoodItemModel.created_at <= end_dt,
        )
    ).all()

    daily_map = defaultdict(lambda: {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0})

    for item in items:
        day_str = item.created_at.strftime("%Y-%m-%d")
        daily_map[day_str]["calories"] += item.calories or 0.0
        daily_map[day_str]["protein"] += item.protein or 0.0
        daily_map[day_str]["carbs"] += item.carbohydrates or 0.0
        daily_map[day_str]["fats"] += item.fats or 0.0

    result = [
        NutritionHistoryItem(
            date=day,
            calories=round(stats["calories"], 1),
            protein=round(stats["protein"], 1),
            carbohydrates=round(stats["carbs"], 1),
            fat=round(stats["fats"], 1),
        )
        for day, stats in sorted(daily_map.items())
    ]

    return NutritionHistoryResponse(
        start_date=start_date,
        end_date=end_date,
        data=result,
    )
