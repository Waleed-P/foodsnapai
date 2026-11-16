from pydantic import BaseModel, Field


class FoodHistoryArgs(BaseModel):
    date: str = Field(
        description="The date to retrieve food analysis history for, in YYYY-MM-DD format."
    )


FOOD_HISTORY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_food_history",
        "description": (
            "Retrieve the food analysis history of the authenticated user "
            "for a specific date."
        ),
        "parameters": FoodHistoryArgs.model_json_schema(),
    },
}
