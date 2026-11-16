from app.tools.daily_nutrition import get_daily_nutrition
from app.tools.food_history import get_food_history
from app.tools.nutrition_history import get_nutrition_history

TOOL_FUNCTIONS = {
    "get_food_history": get_food_history,
    "get_daily_nutrition": get_daily_nutrition,
    "get_nutrition_history": get_nutrition_history,
}

__all__ = [
    "TOOL_FUNCTIONS",
    "get_daily_nutrition",
    "get_food_history",
    "get_nutrition_history",
]
