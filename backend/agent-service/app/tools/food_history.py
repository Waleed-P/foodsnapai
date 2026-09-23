from datetime import date


def get_food_history(user_id: int, date: str):
    """
    Demo tool that returns food analyses for a user on a specific date.
    """

    demo_data = {
        "2026-09-14": [
            {
                "food_name": "Chicken Biryani",
                "calories": 450,
                "protein": 22,
                "carbohydrates": 55,
                "fat": 16,
            },
            {
                "food_name": "Banana",
                "calories": 105,
                "protein": 1.3,
                "carbohydrates": 27,
                "fat": 0.3,
            },
            {
                "food_name": "Grilled Chicken",
                "calories": 280,
                "protein": 42,
                "carbohydrates": 0,
                "fat": 12,
            },
        ],
        "2026-09-13": [
            {
                "food_name": "Dosa",
                "calories": 168,
                "protein": 4,
                "carbohydrates": 29,
                "fat": 4,
            },
            {
                "food_name": "Egg Curry",
                "calories": 220,
                "protein": 14,
                "carbohydrates": 8,
                "fat": 15,
            },
        ],
    }

    return demo_data.get(
        date,
        []
    )