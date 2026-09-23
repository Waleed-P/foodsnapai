def get_nutrition_history(
    user_id: int,
    start_date: str,
    end_date: str
):
    """
    Demo tool that returns nutrition history
    for a date range.
    """

    demo_data = [
        {
            "date": "2026-09-10",
            "calories": 1750,
            "protein": 68,
            "carbohydrates": 210,
            "fat": 58,
        },
        {
            "date": "2026-09-11",
            "calories": 1920,
            "protein": 75,
            "carbohydrates": 225,
            "fat": 62,
        },
        {
            "date": "2026-09-12",
            "calories": 1850,
            "protein": 71,
            "carbohydrates": 218,
            "fat": 60,
        },
        {
            "date": "2026-09-13",
            "calories": 650,
            "protein": 18,
            "carbohydrates": 37,
            "fat": 19,
        },
        {
            "date": "2026-09-14",
            "calories": 835,
            "protein": 65.3,
            "carbohydrates": 82,
            "fat": 28.3,
        },
    ]

    result = [
        item
        for item in demo_data
        if start_date <= item["date"] <= end_date
    ]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "data": result
    }