from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.enums.job_status import JobStatus


class FoodItemSchema(BaseModel):
    id: int
    name: Optional[str] = None
    calories: Optional[float] = None
    confidence: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    image_url: str
    aws_unique_name: str
    status: JobStatus
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class FoodUploadResponse(BaseModel):
    message: str
    food_item_id: int
    status: str


class FoodHistoryResponse(BaseModel):
    history: List[FoodItemSchema]


class DailyNutritionResponse(BaseModel):
    date: str
    total_calories: float
    protein: float
    carbohydrates: float
    fat: float
    items_count: int


class NutritionHistoryItem(BaseModel):
    date: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float


class NutritionHistoryResponse(BaseModel):
    start_date: str
    end_date: str
    data: List[NutritionHistoryItem]
