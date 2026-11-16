from pydantic import BaseModel, Field


class NutritionHistoryArgs(BaseModel):
    start_date: str = Field(
        description="Beginning of the date range in YYYY-MM-DD format."
    )
    end_date: str = Field(
        description="End of the date range in YYYY-MM-DD format."
    )


NUTRITION_HISTORY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_nutrition_history",
        "description": (
            "Retrieve the user's daily nutrition analysis history "
            "between two dates."
        ),
        "parameters": NutritionHistoryArgs.model_json_schema(),
    },
}
