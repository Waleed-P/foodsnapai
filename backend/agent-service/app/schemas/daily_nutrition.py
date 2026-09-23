from pydantic import BaseModel, Field


class DailyNutritionArgs(BaseModel):

    date: str = Field(
        description="The date to retrieve the user's total nutrition analysis for, in YYYY-MM-DD format."
    )


DAILY_NUTRITION_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_daily_nutrition",
        "description": (
            "Retrieve the user's total analyzed nutrition for a specific date, "
            "including calories, protein, carbohydrates, fat, and other available nutrients."
        ),
        "parameters": DailyNutritionArgs.model_json_schema(),
    },
}