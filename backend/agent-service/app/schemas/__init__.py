from app.ai_agent.schemas.food_history import FOOD_HISTORY_SCHEMA
from app.ai_agent.schemas.daily_nutrition import DAILY_NUTRITION_SCHEMA
from app.ai_agent.schemas.nutrition_history import NUTRITION_HISTORY_SCHEMA


TOOLS = [
    FOOD_HISTORY_SCHEMA,
    DAILY_NUTRITION_SCHEMA,
    NUTRITION_HISTORY_SCHEMA,
]