import logging
from typing import Any, Dict
import httpx
from app.core.config import settings

logger = logging.getLogger("agent.tools.daily_nutrition")


def get_daily_nutrition(user_id: int, date: str, auth_token: str | None = None) -> Dict[str, Any]:
    """
    Fetches total nutrition for a user on a specific date from Food Service.
    """
    try:
        cookies = {"access_token": auth_token} if auth_token else {}
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        with httpx.Client(timeout=5.0) as client:
            res = client.get(
                f"{settings.food_service_url}/food/nutrition/daily",
                params={"date": date},
                cookies=cookies,
                headers=headers,
            )
            if res.status_code == 200:
                return res.json()
    except Exception as e:
        logger.warning(f"Could not reach Food Service for daily nutrition: {e}")

    # Fallback response
    return {
        "date": date,
        "message": f"No nutrition records found for date {date}.",
        "total_calories": 0.0,
        "protein": 0.0,
        "carbohydrates": 0.0,
        "fat": 0.0,
    }
