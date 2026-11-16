from app.schemas.daily_nutrition import DAILY_NUTRITION_SCHEMA
from app.schemas.food_history import FOOD_HISTORY_SCHEMA
from app.schemas.nutrition_history import NUTRITION_HISTORY_SCHEMA

TOOLS = [
    FOOD_HISTORY_SCHEMA,
    DAILY_NUTRITION_SCHEMA,
    NUTRITION_HISTORY_SCHEMA,
]

__all__ = [
    "TOOLS",
    "DAILY_NUTRITION_SCHEMA",
    "FOOD_HISTORY_SCHEMA",
    "NUTRITION_HISTORY_SCHEMA",
]
