def get_daily_nutrition(user_id: int, date: str):
    """
    Demo tool that returns total nutrition analyzed
    by a user for a specific date.
    """

    demo_data = {
        "2026-09-14": {
            "date": "2026-09-14",
            "total_calories": 835,
            "protein": 65.3,
            "carbohydrates": 82,
            "fat": 28.3,
            "fiber": 8.5,
            "calcium": 320,
            "iron": 5.8,
            "vitamin_c": 42,
        },

        "2026-09-13": {
            "date": "2026-09-13",
            "total_calories": 650,
            "protein": 18,
            "carbohydrates": 37,
            "fat": 19,
            "fiber": 6.2,
            "calcium": 280,
            "iron": 4.1,
            "vitamin_c": 35,
        },
    }

    return demo_data.get(
        date,
        {
            "date": date,
            "message": "No nutrition analysis found for this date."
        }
    )